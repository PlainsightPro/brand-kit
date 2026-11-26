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
VISUALS = ROOT / "assets" / "visuals" / "visuals.json"
PHOTOS_DIR = "assets/photos"
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
    # The small token files ride along. A skill that points at a file without
    # shipping it is a skill that tells the reader to improvise, which is the
    # exact failure this program exists to remove.
    "templates/plainsight-powerbi-theme.json": "assets/templates/plainsight-powerbi-theme.json",
    "templates/plainsight-tokens.css": "assets/templates/plainsight-tokens.css",
    "templates/tailwind.config.js": "assets/templates/tailwind.config.js",
}

#: Referenced but deliberately NOT bundled, and rendered with this prefix so a
#: reader can see it lives upstream. The PowerPoint master is 36 MB; putting it in
#: every colleague's skill directory serves nobody.
UPSTREAM_ONLY_PREFIX = "brand-kit:"

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
    never = typography.get("never_use")
    if isinstance(never, list) and never:
        families = ", ".join(f"`{item}`" for item in never if isinstance(item, str))
        lines.extend(["", f"**Never use:** {families}"])
        if note := typography.get("override_note"):
            lines.extend(["", str(note)])
    if change := typography.get("change_note"):
        lines.extend(["", str(change)])
    if rules := _bullets(typography.get("rules")):
        lines.extend(["", rules])
    return "\n".join(lines)


def render_known_issues(manifest: dict[str, Any]) -> str:
    """Render the open defects in the brand assets themselves.

    An asset can disagree with the manifest, and when it does the reader needs to
    know before they trust the asset. Silence here means someone keeps whatever
    the template offered them.
    """
    issues = manifest.get("known_issues")
    if not isinstance(issues, list) or not issues:
        return "None recorded. Nothing currently disagrees with the manifest."
    parts: list[str] = []
    for issue in issues:
        if not isinstance(issue, dict):
            continue
        # Prefixed unless the file is actually in the bundle, so the reader knows
        # where to look and the dangling-reference guard stays meaningful.
        path = str(issue.get("file", "")).strip()
        bundled = {source: local for local, source in BUNDLED_ASSETS.items()}
        label = f"assets/{bundled[path]}" if path in bundled else f"{UPSTREAM_ONLY_PREFIX}{path}"
        parts.append(f"**`{label or 'unknown asset'}`**")
        parts.append("")
        if affects := issue.get("also_affects"):
            parts.append(f"- Also affects: {affects}")
        parts.append(f"- Problem: {issue.get('problem', '')}")
        parts.append(f"- What to do: {issue.get('rule', '')}")
        status = str(issue.get("status", "")).strip()
        reported = str(issue.get("reported", "")).strip()
        if status or reported:
            parts.append(f"- Status: {status or 'unknown'}{f', reported {reported}' if reported else ''}")
        parts.append("")
    return "\n".join(parts).rstrip()


def render_triangle_rule(manifest: dict[str, Any]) -> str:
    triangles = manifest.get("triangles", {})
    parts = [triangles.get("rule", ""), ""]
    if signature := triangles.get("signature"):
        parts.extend([str(signature), ""])
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
    documents = placement.get("documents")
    if isinstance(documents, dict):
        parts.append("**Documents.**")
        parts.append("")
        for key, value in documents.items():
            if isinstance(value, dict):
                parts.append(f"- {key.replace('_', ' ')}:")
                parts.extend(f"  - {inner.replace('_', ' ')}: {text}" for inner, text in value.items())
            else:
                parts.append(f"- {key.replace('_', ' ')}: {value}")
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
        # Not bundled, so prefixed: nobody should look for it inside this skill.
        parts.append(f"- In brand-kit: `{UPSTREAM_ONLY_PREFIX}{master.get('file', '')}`")
        if live := master.get("live_version"):
            parts.append(f"- Live version: {live}")
        parts.append("")
    for key, word_template in templates.items():
        if not (key.startswith("word_") and isinstance(word_template, dict)):
            continue
        parts.append(f"**{word_template.get('name', key)}.** {word_template.get('rule', '')}")
        parts.append("")
        parts.append(f"- In brand-kit: `{UPSTREAM_ONLY_PREFIX}{word_template.get('file', '')}`")
        if live := word_template.get("live_version"):
            parts.append(f"- Live version: {live}")
        parts.append("")
    design_system = templates.get("claude_design_system")
    if isinstance(design_system, dict):
        parts.append(f"**{design_system.get('name', 'Design system in Claude')}.** {design_system.get('rule', '')}")
        if status := design_system.get("status"):
            parts.extend(["", f"- Status: {status}"])
        parts.append("")

    bundled_sources = {source: local for local, source in BUNDLED_ASSETS.items()}
    rows = [(key, value) for key, value in templates.items() if isinstance(value, str)]
    if rows:
        parts.extend(["| Asset | Path | Bundled |", "|---|---|---|"])
        for key, value in rows:
            local = bundled_sources.get(value)
            path = f"assets/{local}" if local else f"{UPSTREAM_ONLY_PREFIX}{value}"
            parts.append(f"| {key.replace('_', ' ')} | `{path}` | {'yes' if local else 'no'} |")
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

    if conventions := _bullets(voice.get("conventions")):
        parts.extend(["**Conventions.**", "", conventions, ""])

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


def render_layout(manifest: dict[str, Any]) -> str:
    layout = manifest.get("layout", {})
    if not isinstance(layout, dict) or not layout:
        return "No layout rules recorded."
    parts: list[str] = []
    if applies := layout.get("applies_to"):
        parts.extend([f"Applies to: {applies}", ""])
    if canvas := layout.get("slide_canvas"):
        parts.extend([f"**Slide canvas.** {canvas}", ""])
    if rules := _bullets(layout.get("rules")):
        parts.extend([rules, ""])
    if slides := manifest.get("motion", {}).get("slides"):
        parts.extend([f"**Motion on slides.** {slides}", ""])
    return "\n".join(parts).rstrip()


def render_charts(manifest: dict[str, Any]) -> str:
    charts = manifest.get("charts", {})
    if not isinstance(charts, dict) or not charts:
        return "No chart rules recorded."
    parts: list[str] = []
    palette = charts.get("palette")
    if isinstance(palette, list) and palette:
        parts.append("Palette in order: " + ", ".join(f"`{value}`" for value in palette if isinstance(value, str)) + ".")
    if accent := charts.get("accent"):
        parts.append(f"Accent, for the one point the title is about: `{accent}`.")
    if parts:
        parts.append("")
    if rules := _bullets(charts.get("rules")):
        parts.append(rules)
    return "\n".join(parts).rstrip()


def render_iconography(manifest: dict[str, Any]) -> str:
    icons = manifest.get("iconography", {})
    if not isinstance(icons, dict) or not icons:
        return "No icon rules recorded."
    parts: list[str] = []
    if icon_set := icons.get("set"):
        parts.extend([f"**Set.** {icon_set}", ""])
    if rules := _bullets(icons.get("rules")):
        parts.append(rules)
    return "\n".join(parts).rstrip()


def load_photo_catalogue() -> list[dict[str, Any]]:
    """Return the catalogue entries that are photos, in catalogue order.

    Only entries under assets/photos/ are rendered, so a new diagram added to
    the visuals catalogue never makes the committed skill stale.
    """
    try:
        catalogue = json.loads(VISUALS.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GeneratorError(f"{VISUALS} is missing") from exc
    except json.JSONDecodeError as exc:
        raise GeneratorError(f"{VISUALS} is not valid JSON: {exc}") from exc
    if not isinstance(catalogue, list):
        raise GeneratorError(f"{VISUALS} must hold a list")
    return [
        entry
        for entry in catalogue
        if isinstance(entry, dict) and str(entry.get("file", "")).startswith(PHOTOS_DIR + "/")
    ]


def render_photos(manifest: dict[str, Any]) -> str:
    photos = manifest.get("photos", {})
    if not isinstance(photos, dict) or not photos:
        return "No photo rules recorded."
    parts: list[str] = []
    if rule := photos.get("rule"):
        parts.extend([str(rule), ""])
    use = photos.get("use")
    if isinstance(use, dict):
        parts.extend(f"- **{key.replace('_', ' ').capitalize()}.** {value}" for key, value in use.items())
        parts.append("")
    if treatment := _bullets(photos.get("treatment")):
        parts.extend(["**Treatment.**", "", treatment, ""])
    if note := photos.get("catalogue_note"):
        parts.extend([str(note), ""])
    base_url = str(photos.get("base_url", "")).rstrip("/")
    entries = load_photo_catalogue()
    if entries:
        # Prefixed, not bundled: the photos stay in brand-kit and are served
        # from its public site, so nobody looks for them inside this skill.
        parts.extend(["| Slug | URL | Shows |", "|---|---|---|"])
        for entry in entries:
            url = f"{base_url}/{entry.get('file', '')}" if base_url else f"{UPSTREAM_ONLY_PREFIX}{entry.get('file', '')}"
            parts.append(f"| `{entry.get('slug', '')}` | {url} | {entry.get('alt', '')} |")
    return "\n".join(parts).rstrip()


def render_never_look_like_ai(manifest: dict[str, Any]) -> str:
    never = manifest.get("never_look_like_ai", {})
    if not isinstance(never, dict) or not never:
        return "No rules recorded."
    parts: list[str] = []
    if principle := never.get("principle"):
        parts.extend([str(principle), ""])
    if applies := never.get("applies_to"):
        parts.extend([f"Applies to: {applies}", ""])
    if test := _bullets(never.get("test")):
        parts.extend(["**Before you use any element, check both:**", "", test, ""])
    if forbidden := _bullets(never.get("never")):
        parts.extend(["**Never.**", "", forbidden, ""])
    formats = never.get("formats")
    if isinstance(formats, list) and formats:
        parts.extend(["| Format | Looks AI-generated when | Plainsight version |", "|---|---|---|"])
        for item in formats:
            if isinstance(item, dict):
                parts.append(
                    f"| {item.get('format', '')} | {item.get('looks_ai_when', '')} | {item.get('plainsight_version', '')} |"
                )
    return "\n".join(parts).rstrip()


def render_agency_principles(manifest: dict[str, Any]) -> str:
    agency = manifest.get("agency_principles", {})
    if not isinstance(agency, dict) or not agency:
        return "No principles recorded."
    parts: list[str] = []
    if scope := agency.get("scope"):
        parts.extend([str(scope), ""])
    principles = agency.get("principles")
    if isinstance(principles, list):
        parts.extend(f"{index}. {text}" for index, text in enumerate(principles, start=1) if isinstance(text, str))
        parts.append("")
    per_format = agency.get("per_format")
    if isinstance(per_format, dict):
        parts.extend(["### Per format", ""])
        parts.extend(f"- **{key.replace('_', ' ').capitalize()}.** {value}" for key, value in per_format.items())
        parts.append("")
    if final := _bullets(agency.get("final_check")):
        parts.extend(["### Final check before anything leaves Plainsight", "", final, ""])
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
    "KNOWN_ISSUES": render_known_issues,
    "LAYOUT": render_layout,
    "CHARTS": render_charts,
    "ICONOGRAPHY": render_iconography,
    "PHOTOS": render_photos,
    "NEVER_LOOK_LIKE_AI": render_never_look_like_ai,
    "AGENCY_PRINCIPLES": render_agency_principles,
    "VOICE": render_voice,
    "CHECKLIST": render_checklist,
}


#: Every `assets/...` path the generated skill names must exist inside the skill.
#: The first version of this generator rendered brand.json's repo-relative template
#: paths verbatim, so the shipped skill pointed at four files that were not in it.
#: The manifest's own references were already checked; the OUTPUT's were not.
_ASSET_REFERENCE_RE = re.compile(r"`assets/([^`]+)`")


def check_bundled_line_endings() -> list[str]:
    """Return bundled text assets that contain a carriage return.

    These files are LF in this repository and their sha256 is recorded downstream
    (the Plainsight Brain keeps a digest per file). `check_skill` compares
    working-tree bytes, which on Windows can be CRLF on BOTH sides and so agrees
    with itself while the stored blobs diverge. That happened: the bundled copies
    were committed with CRLF while their sources stayed LF, and every downstream
    digest would have broken. A carriage return in one of these files is always a
    line-ending accident, never intent.
    """
    offenders: list[str] = []
    for local_name in BUNDLED_ASSETS:
        target = SKILL_ASSETS / local_name
        if target.is_file() and b"\r" in target.read_bytes():
            offenders.append(f"assets/{local_name}")
    return offenders


def check_generated_references(content: str) -> list[str]:
    """Return the asset paths the generated skill names but does not ship."""
    missing: list[str] = []
    for reference in sorted(set(_ASSET_REFERENCE_RE.findall(content))):
        target = SKILL_ASSETS / reference.rstrip("/")
        if not (target.is_dir() if reference.endswith("/") else target.is_file()):
            missing.append(f"assets/{reference}")
    return missing


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
        target = SKILL_ASSETS / local_name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / source, target)
        written.append(str(target.relative_to(ROOT)).replace("\\", "/"))
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
        if dangling := check_generated_references(content):
            print("error: the skill names assets it does not ship:", file=sys.stderr)
            for path in dangling:
                print(f"  {path}", file=sys.stderr)
            return 1
        if crlf := check_bundled_line_endings():
            print("error: bundled assets contain carriage returns:", file=sys.stderr)
            for path in crlf:
                print(f"  {path}", file=sys.stderr)
            print(
                "Renormalize: delete them, `git checkout -- assets/`, then regenerate.",
                file=sys.stderr,
            )
            return 1
        print(f"skill is current ({len(content)} chars, {len(BUNDLED_ASSETS)} assets)")
        return 0

    for path in write_skill(content):
        print(f"wrote {path}")

    # Checked after writing, because the references are resolved against what was
    # just shipped. A dangling reference still fails the build.
    if dangling := check_generated_references(content):
        print("error: the skill names assets it does not ship:", file=sys.stderr)
        for path in dangling:
            print(f"  {path}", file=sys.stderr)
        return 1
    if crlf := check_bundled_line_endings():
        print("error: bundled assets contain carriage returns:", file=sys.stderr)
        for path in crlf:
            print(f"  {path}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
