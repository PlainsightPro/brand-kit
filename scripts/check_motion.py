#!/usr/bin/env python3
"""Check the moving twins in `assets/visuals/` against the motion rule.

A visual in the catalogue may carry `motion`: `assets/visuals/<slug>.svg`,
an SVG of the same picture whose parts move by CSS animation written inside
the file. The Plainsight Brain shows it on an offer page as an image, and
prints the still PNG. Two checks run here, as they do in the Brain's sync:

- `check_svg`, the structural allowlist: what may be in the file at all.
  No script, no event attributes, no external references, no text (an SVG
  shown as an image loads no font, so text is outlined), no foreign objects.
- `check_calm`, the brand rule: how much it may move. Every number comes
  from `brand.json` → `motion`; this file restates none of them.

The two functions are copied from plainsight-brain
`src/services/offer_visual_motion.py`, the master. Refresh them by hand when
that file changes. Standard library only, like the skill generator: a guard
that needs a lockfile to run is a guard that stops running.

Usage: python scripts/check_motion.py   (from the repository root; exit 1 on a problem)
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
from typing import Any

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
MOTION_MAX_BYTES = 400 * 1024

ALLOWED_ELEMENTS = frozenset({
    "svg", "g", "defs", "title", "desc", "symbol", "use",
    "path", "rect", "circle", "ellipse", "line", "polyline", "polygon",
    "linearGradient", "radialGradient", "stop", "clipPath", "mask", "style",
})
PLACEMENT_PROPERTIES = frozenset({"transform-origin", "transform-box"})
_FORBIDDEN_CSS = ("@import", "@font-face", "expression(", "behavior", "-moz-binding")
_URL_RE = re.compile(r"url\(\s*(['\"]?)([^)'\"]*)\1\s*\)", re.IGNORECASE)
_DOCTYPE_RE = re.compile(r"<!(?:DOCTYPE|ENTITY)", re.IGNORECASE)
_PI_RE = re.compile(r"<\?(?!xml[\s?])")
_TIME_RE = re.compile(r"^(\d+(?:\.\d+)?)(ms|s)$", re.IGNORECASE)
_DECL_RE = re.compile(r"([a-zA-Z-]+)\s*:\s*([^;{}]+)")
_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
_DURATION_RE = re.compile(r"(?<![\w-])animation-duration\s*:\s*([^;}]+)", re.IGNORECASE)
_SHORTHAND_RE = re.compile(r"(?<![\w-])animation\s*:\s*([^;}]+)", re.IGNORECASE)


def _local(tag: str) -> tuple[str, str]:
    if tag.startswith("{"):
        ns, _, name = tag[1:].partition("}")
        return ns, name
    return "", tag


def _bad_urls(text: str) -> bool:
    return any(not target.startswith("#") for _quote, target in _URL_RE.findall(text))


def _check_css(css: str) -> list[str]:
    problems: list[str] = []
    lowered = css.lower()
    for token in _FORBIDDEN_CSS:
        if token in lowered:
            problems.append(f"stylesheet uses {token}")
    if _bad_urls(css):
        problems.append("stylesheet references a url() outside the file")
    return problems


def check_svg(raw: bytes, *, cap: int = MOTION_MAX_BYTES) -> list[str]:
    """Every structural problem with a twin; an empty list is a pass."""
    if len(raw) > cap:
        return [f"{len(raw)} bytes exceeds the {cap} byte cap"]
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return ["not UTF-8 text"]
    problems: list[str] = []
    if _DOCTYPE_RE.search(text):
        problems.append("DOCTYPE and entity declarations are not allowed")
    if _PI_RE.search(text):
        problems.append("processing instructions are not allowed")
    if problems:
        return problems
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        return [f"not well-formed XML: {exc}"]
    ns, name = _local(root.tag)
    if ns != SVG_NS:
        return ["the root element must be in the SVG namespace"]
    if name != "svg":
        return ["the root element must be <svg>"]
    if not (root.get("viewBox") or "").strip():
        problems.append("the root <svg> needs a viewBox")
    ids = {element.get("id") for element in root.iter() if element.get("id")}
    for element in root.iter():
        ns, name = _local(element.tag)
        if ns != SVG_NS or name not in ALLOWED_ELEMENTS:
            problems.append(f"<{name}> is not allowed")
            continue
        for attr, value in element.attrib.items():
            attr_ns, attr_name = _local(attr)
            if attr_name.lower().startswith("on"):
                problems.append(f"<{name}> carries an event attribute {attr_name}")
            internal = value.startswith("#") and value[1:] in ids
            if attr_name == "href" and attr_ns in ("", XLINK_NS) and not internal:
                problems.append(f"<{name}> href must point inside the file, got {value!r}")
            if _bad_urls(value):
                problems.append(f"<{name}> {attr_name} references a url() outside the file")
        if name == "style":
            problems.extend(_check_css(element.text or ""))
    return problems


def _stylesheet(raw: bytes) -> str:
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return ""
    parts: list[str] = []
    for element in root.iter():
        if _local(element.tag)[1] == "style":
            parts.append(element.text or "")
        inline = element.get("style")
        if inline:
            parts.append(inline + ";")
    return _COMMENT_RE.sub("", "\n".join(parts))


def _at_rule_blocks(css: str, name: str) -> list[str]:
    blocks: list[str] = []
    start = 0
    while True:
        at = css.find(name, start)
        if at < 0:
            return blocks
        open_brace = css.find("{", at)
        if open_brace < 0:
            return blocks
        depth, i = 0, open_brace
        while i < len(css):
            if css[i] == "{":
                depth += 1
            elif css[i] == "}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        blocks.append(css[open_brace + 1:i])
        start = i + 1


def _split_animations(declaration: str) -> list[str]:
    """Split an `animation` list on the commas between animations, not those inside `cubic-bezier()`."""
    parts, depth, current = [], 0, []
    for ch in declaration:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(depth - 1, 0)
        if ch == "," and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(ch)
    parts.append("".join(current))
    return [part for part in parts if part.strip()]


def _seconds(token: str) -> float | None:
    match = _TIME_RE.match(token.strip())
    if not match:
        return None
    value = float(match.group(1))
    return value / 1000 if match.group(2).lower() == "ms" else value


def check_calm(raw: bytes, rules: Any) -> list[str]:
    """Every way the twin breaks the brand's motion rule; an empty list is a pass."""
    usable = (
        isinstance(rules, dict)
        and isinstance(rules.get("min_cycle_seconds"), (int, float))
        and isinstance(rules.get("animated_properties"), list)
        and isinstance(rules.get("min_opacity"), (int, float))
    )
    if not usable:
        return [
            "the brand manifest carries no usable motion rules "
            "(min_cycle_seconds, animated_properties, min_opacity)"
        ]
    min_cycle = float(rules["min_cycle_seconds"])
    movable = {str(prop).lower() for prop in rules["animated_properties"]}
    allowed = movable | PLACEMENT_PROPERTIES
    min_opacity = float(rules["min_opacity"])
    css = _stylesheet(raw)
    problems: list[str] = []
    if "steps(" in css:
        problems.append("stepped timing (steps()) is not calm")
    for declaration in _DURATION_RE.findall(css):
        for token in declaration.replace(",", " ").split():
            seconds = _seconds(token)
            if seconds is not None and seconds < min_cycle:
                problems.append(f"animation-duration {token} is under the {min_cycle:g}s minimum")
    for declaration in _SHORTHAND_RE.findall(css):
        for one in _split_animations(declaration):
            times = [s for s in (_seconds(t) for t in one.split()) if s is not None]
            if not times:
                problems.append(f"animation {one.strip()!r} has no duration")
            elif times[0] < min_cycle:
                problems.append(f"animation {one.strip()!r} is under the {min_cycle:g}s minimum")
    blocks = _at_rule_blocks(css, "@keyframes")
    if not blocks:
        problems.append("no @keyframes: a twin without animation is a still")
    for block in blocks:
        for prop, value in _DECL_RE.findall(block):
            prop = prop.lower()
            if prop not in allowed:
                problems.append(
                    f"@keyframes animates {prop}; only {', '.join(sorted(movable))} may move"
                )
            if prop == "opacity":
                try:
                    if float(value.strip()) < min_opacity:
                        problems.append(
                            f"opacity {value.strip()} is under the {min_opacity:g} minimum"
                        )
                except ValueError:
                    problems.append(f"opacity {value.strip()!r} is not a number")
    return problems


def main() -> int:
    manifest = json.loads(pathlib.Path("assets/templates/brand.json").read_text("utf-8"))
    rules = manifest.get("motion")
    catalogue = json.loads(pathlib.Path("assets/visuals/visuals.json").read_text("utf-8"))
    problems: list[str] = []
    for entry in catalogue:
        motion = entry.get("motion")
        if not motion:
            continue
        slug = entry.get("slug", "?")
        if motion != f"assets/visuals/{slug}.svg":
            problems.append(f"{slug}: motion must be assets/visuals/{slug}.svg, got {motion!r}")
            continue
        path = pathlib.Path(motion)
        if not path.is_file():
            problems.append(f"{slug}: missing {motion}")
            continue
        raw = path.read_bytes()
        for problem in check_svg(raw) or check_calm(raw, rules):
            problems.append(f"{slug}: {problem}")
    for path in sorted(pathlib.Path("assets/visuals").glob("*.svg")):
        if not any(entry.get("motion") == path.as_posix() for entry in catalogue):
            problems.append(f"twin without a catalogue entry: {path.as_posix()}")
    if problems:
        print("motion twins check FAILED:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    moving = sum(1 for entry in catalogue if entry.get("motion"))
    print(f"motion twins are sound: {moving} moving visual(s), every twin calm and catalogued.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
