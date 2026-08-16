#!/usr/bin/env python3
"""Generate the team `plainsight-brand` agent skill from brand.json.

The skill is generated, never hand-written, because a hand-written copy of the
brand rules is how the wrong ones ship: a document that describes the triangle
instead of pointing at the file invites a tool to redraw it, and a colour table
pasted into a second place drifts from the first.

So the split is strict. Values come from `assets/templates/brand.json`. Prose
comes from `skill/template.md`, which is checked to contain no colour or font
values of its own. Assets are copied byte-for-byte from the repository.

Usage:
    python skill/generate_skill.py            # write the skill
    python skill/generate_skill.py --check    # fail if the committed skill is stale
"""

from __future__ import annotations

import argparse
import filecmp
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "templates" / "brand.json"
TEMPLATE = ROOT / "skill" / "template.md"
SKILL_DIR = ROOT / "skill" / "plainsight-brand"
SKILL_FILE = SKILL_DIR / "SKILL.md"
SKILL_ASSETS = SKILL_DIR / "assets"

#: Local skill filename -> path in the repository. Byte-for-byte copies, under the
#: names the Plainsight Brain also advertises, so an agent reading either surface
#: asks for the same thing.
BUNDLED_ASSETS: dict[str, str] = {
    "triangle-blue.svg": "assets/graphics/triangle-blue.svg",
    "triangle-orange.svg": "assets/graphics/triangle-orange.svg",
    "triangle-white.svg": "assets/graphics/triangle-white.svg",
    "logo-blue.svg": "assets/logos/plainsight-logo-blue.svg",
    "logo-white.svg": "assets/logos/plainsight-logo-white.svg",
    "brand.json": "assets/templates/brand.json",
}

#: The prose template may describe procedure and layout maths. It may NOT carry a
#: brand value: those live in brand.json alone. Enforced, because "just this one
#: hex" is exactly how the second source of truth gets started.
FORBIDDEN_IN_TEMPLATE = (
    (re.compile(r"#[0-9a-fA-F]{6}\b"), "a hex colour"),
    (re.compile(r"\bTitillium\b"), "a font family"),
    (re.compile(r"\bInter\b"), "a font family"),
    (re.compile(r"\bEpilogue\b"), "a font family"),
)


class GeneratorError(RuntimeError):
    """The manifest or the template cannot produce a correct skill."""


def load_manifest() -> dict[str, Any]:
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GeneratorError(f"{MANIFEST} is missing") from exc
    except json.JSONDecodeError as exc:
        raise GeneratorError(f"{MANIFEST} is not valid JSON: {exc}") from exc
    required = ("meta", "colors", "typography", "logos", "triangles", "voice", "agent_checklist")
    if missing := [key for key in required if key not in manifest]:
        raise GeneratorError(f"brand.json is missing required keys: {', '.join(missing)}")
    return manifest


def check_template(text: str) -> None:
    for pattern, description in FORBIDDEN_IN_TEMPLATE:
        if match := pattern.search(text):
            raise GeneratorError(
                f"skill/template.md contains {description} ({match.group(0)!r}). "
                "Brand values belong in brand.json; reference them by role instead."
            )


def check_asset_references(manifest: dict[str, Any]) -> list[str]:
    """Return every asset path in the manifest that does not exist on disk."""
    missing: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)
        elif isinstance(node, str) and node.startswith("assets/") and not (ROOT / node).is_file():
            missing.append(node)

    walk(manifest)
    return sorted(set(missing))


def _bullets(items: Any) -> str:
    return "\n".join(f"- {item}" for item in items if isinstance(item, str)) if isinstance(items, list) else ""


def render_meta(manifest: dict[str, Any]) -> str:
    meta = manifest.get("meta", {})
    return (
        f"Generated from `brand.json` v{meta.get('version', '?')} "
        f"(updated {meta.get('updated', '?')}). Source of truth: "
        f"{meta.get('source_of_truth', 'https://github.com/PlainsightPro/brand-kit')}. "
        "When any other document disagrees with the manifest, the manifest wins."
    )


def render_color_table(manifest: dict[str, Any]) -> str:
    rows = ["| Name | Hex | Role |", "|---|---|---|"]
    for name, spec in manifest.get("colors", {}).items():
        if not isinstance(spec, dict):
            continue
        label = name.replace("_", " ")
        rows.append(f"| {label} | `{spec.get('hex', '')}` | {spec.get('role', '')} |")
    return "\n".join(rows)


def render_color_rules(manifest: dict[str, Any]) -> str:
    return _bullets(manifest.get("colors", {}).get("rules"))


def render_typography(manifest: dict[str, Any]) -> str:
    typography = manifest.get("typography", {})
    lines = ["| Use | Family | Fallback |", "|---|---|---|"]
    for role in ("headings", "body"):
        spec = typography.get(role)
        if isinstance(spec, dict):
            lines.append(f"| {role.title()} | **{spec.get('family', '')}** | {spec.get('fallback', '')} |")
    headings = typography.get("headings", {})
    if isinstance(headings, dict) and headings.get("style"):
        lines.append("")
        lines.append(f"Heading style: {headings['style']}")
    if rules := _bullets(typography.get("rules")):
        lines.extend(["", rules])
    return "\n".join(lines)


def render_triangle_rule(manifest: dict[str, Any]) -> str:
    triangles = manifest.get("triangles", {})
    parts = [triangles.get("rule", ""), ""]
    if hard_rules := _bullets(triangles.get("hard_rules")):
        parts.extend(["**Hard rules.**", "", hard_rules, ""])
    assets = triangles.get("assets", {})
    if isinstance(assets, dict) and assets:
        parts.extend(["| Variant | File | Use on |", "|---|---|---|"])
        for name, spec in assets.items():
            if isinstance(spec, dict):
                filename = Path(str(spec.get("svg", ""))).name
                parts.append(f"| {name} | `assets/{filename}` | {spec.get('use_on', '')} |")
    size = triangles.get("native_size_px")
    if isinstance(size, dict):
        parts.extend(["", f"Native size: {size.get('width')} x {size.get('height')} px."])
    return "\n".join(parts)


def render_triangle_placement(manifest: dict[str, Any]) -> str:
    placement = manifest.get("triangles", {}).get("placement", {})
    if not isinstance(placement, dict):
        return ""
    parts = ["### Placement", ""]
    if principle := placement.get("principle"):
        parts.extend([f"**Principle.** {principle}", ""])

    slides = placement.get("linkedin_slides")
    if isinstance(slides, dict):
        parts.append("**LinkedIn slides.**")
        parts.append("")
        if scale := slides.get("scale"):
            parts.append(f"- Scale: {scale}")
        effective = slides.get("effective_size_px")
        if isinstance(effective, dict):
            parts.append(f"- Effective size: {effective.get('width')} x {effective.get('height')} px")
        for pair_name in ("top_right_pair", "bottom_left_pair"):
            pair = slides.get(pair_name)
            if isinstance(pair, dict):
                parts.append(f"- {pair_name.replace('_', ' ')}:")
                parts.extend(f"  - {key.replace('_', ' ')}: `{value}`" for key, value in pair.items())
        for key in ("template_a", "template_b"):
            if key in slides:
                parts.append(f"- {key.replace('_', ' ').title()}: {slides[key]}")
        parts.append("")

    website = placement.get("website")
    if isinstance(website, dict):
        parts.append("**Website.**")
        parts.append("")
        parts.extend(f"- {key.replace('_', ' ')}: {value}" for key, value in website.items())
        parts.append("")
    if presentations := placement.get("presentations"):
        parts.extend([f"**Presentations.** {presentations}", ""])
    return "\n".join(parts).rstrip()


def render_logo_placement(manifest: dict[str, Any]) -> str:
    logos = manifest.get("logos", {})
    parts = ["| Variant | File | Use on |", "|---|---|---|"]
    for name in ("blue", "white"):
        spec = logos.get(name)
        if isinstance(spec, dict):
            parts.append(f"| {name} | `assets/logo-{name}.svg` | {spec.get('use_on', '')} |")
    placement = logos.get("placement")
    if isinstance(placement, dict):
        parts.append("")
        parts.extend(f"- **{key.title()}.** {value}" for key, value in placement.items())
    return "\n".join(parts)


def render_template_files(manifest: dict[str, Any]) -> str:
    templates = manifest.get("templates", {})
    parts: list[str] = []
    master = templates.get("powerpoint_master")
    if isinstance(master, dict):
        parts.append(f"**{master.get('name', 'PowerPoint master')}.** {master.get('rule', '')}")
        parts.append("")
        parts.append(f"- Bundled snapshot: `{master.get('file', '')}`")
        if live := master.get("live_version"):
            parts.append(f"- Live version: {live}")
        parts.append("")
    rows = [(key, value) for key, value in templates.items() if isinstance(value, str)]
    if rows:
        parts.extend(["| Asset | Path |", "|---|---|"])
        parts.extend(f"| {key.replace('_', ' ')} | `{value}` |" for key, value in rows)
    return "\n".join(parts)


def render_voice(manifest: dict[str, Any]) -> str:
    voice = manifest.get("voice", {})
    parts: list[str] = []
    if summary := voice.get("summary"):
        parts.extend([summary, ""])

    principles = voice.get("principles")
    if isinstance(principles, list):
        for principle in principles:
            if isinstance(principle, dict):
                parts.append(f"- **{principle.get('name', '')}.** {principle.get('detail', '')}")
        parts.append("")

    never = voice.get("never_sound_like_ai")
    if isinstance(never, dict):
        parts.extend(["### Never sound like AI wrote it", ""])
        if hard := _bullets(never.get("hard_rules")):
            parts.extend([hard, ""])
        banned = never.get("banned_words")
        if isinstance(banned, list) and banned:
            words = ", ".join(f"`{word}`" for word in banned if isinstance(word, str))
            parts.extend([f"**Banned words and phrases:** {words}", ""])

    for key, heading in (("culture", "Culture"), ("sound_like", "Sound like"), ("avoid", "Avoid")):
        if bullets := _bullets(voice.get(key)):
            parts.extend([f"**{heading}.**", "", bullets, ""])
    if linkedin := voice.get("linkedin"):
        parts.extend([f"**LinkedIn.** {linkedin}", ""])
    return "\n".join(parts).rstrip()


def render_checklist(manifest: dict[str, Any]) -> str:
    items = manifest.get("agent_checklist")
    if not isinstance(items, list):
        return ""
    return "\n".join(f"- [ ] {item}" for item in items if isinstance(item, str))


RENDERERS = {
    "META": render_meta,
    "COLOR_TABLE": render_color_table,
    "COLOR_RULES": render_color_rules,
    "TYPOGRAPHY": render_typography,
    "TRIANGLE_RULE": render_triangle_rule,
    "TRIANGLE_PLACEMENT": render_triangle_placement,
    "LOGO_PLACEMENT": render_logo_placement,
    "TEMPLATE_FILES": render_template_files,
    "VOICE": render_voice,
    "CHECKLIST": render_checklist,
}


def build_skill(manifest: dict[str, Any], template: str) -> str:
    check_template(template)
    rendered = template
    for token, renderer in RENDERERS.items():
        placeholder = "{{" + token + "}}"
        if placeholder not in rendered:
            raise GeneratorError(f"skill/template.md is missing the {placeholder} placeholder")
        rendered = rendered.replace(placeholder, renderer(manifest))
    if leftover := re.findall(r"\{\{[A-Z_]+\}\}", rendered):
        raise GeneratorError(f"unreplaced placeholders remain: {', '.join(sorted(set(leftover)))}")
    return rendered.rstrip() + "\n"


def write_skill(content: str) -> list[str]:
    """Write the skill and its assets. Returns the paths written, repo-relative."""
    SKILL_ASSETS.mkdir(parents=True, exist_ok=True)
    SKILL_FILE.write_bytes(content.encode("utf-8"))
    written = [str(SKILL_FILE.relative_to(ROOT)).replace("\\", "/")]
    for local_name, source in BUNDLED_ASSETS.items():
        shutil.copyfile(ROOT / source, SKILL_ASSETS / local_name)
        written.append(str((SKILL_ASSETS / local_name).relative_to(ROOT)).replace("\\", "/"))
    return written


def check_skill(content: str) -> list[str]:
    """Return the paths that differ from a fresh generation."""
    stale: list[str] = []
    if not SKILL_FILE.is_file() or SKILL_FILE.read_bytes() != content.encode("utf-8"):
        stale.append(str(SKILL_FILE.relative_to(ROOT)).replace("\\", "/"))
    for local_name, source in BUNDLED_ASSETS.items():
        target = SKILL_ASSETS / local_name
        if not target.is_file() or not filecmp.cmp(ROOT / source, target, shallow=False):
            stale.append(str(target.relative_to(ROOT)).replace("\\", "/"))
    return stale


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the plainsight-brand agent skill from brand.json.")
    parser.add_argument("--check", action="store_true", help="verify the committed skill is current; write nothing")
    args = parser.parse_args()

    try:
        manifest = load_manifest()
        if missing := check_asset_references(manifest):
            raise GeneratorError("brand.json references assets that do not exist: " + ", ".join(missing))
        content = build_skill(manifest, TEMPLATE.read_text(encoding="utf-8"))
    except GeneratorError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.check:
        if stale := check_skill(content):
            print("error: the committed skill is stale:", file=sys.stderr)
            for path in stale:
                print(f"  {path}", file=sys.stderr)
            print("\nRun `python skill/generate_skill.py` and commit the result.", file=sys.stderr)
            return 1
        print(f"skill is current ({len(content)} chars, {len(BUNDLED_ASSETS)} assets)")
        return 0

    for path in write_skill(content):
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
