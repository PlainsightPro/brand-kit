# The `plainsight-brand` agent skill

A distributable Claude Code / agent skill generated from this repository, so any
Plainsight colleague gets the same brand rules and the same asset files their
teammates have, without copying a document that then drifts.

## Install

Copy the skill folder into your personal skills directory:

```bash
# macOS / Linux
cp -r skill/plainsight-brand ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse skill\plainsight-brand $HOME\.claude\skills\
```

Restart your client. It activates on its own when you ask for anything branded: a
carousel, a deck, a one-pager, a proposal, a branded page or visual.

Already have an older `plainsight-brand` skill? Replace it. If you have added your
own tooling inside it (a carousel generator, extra assets), keep those files and
replace `SKILL.md` and `assets/` only. Note that the bundled assets use the
canonical names (`triangle-blue.svg`, `logo-blue.svg`), so a script of yours that
refers to older filenames needs its paths updated.

## If you use the Plainsight Brain

You do not need this skill to get the rules. `brand_get_kit` returns the whole
specification plus the asset markup in one MCP call, `brand://manifest` serves the
same content as a resource, and `brand_start` pushes a short brand briefing on any
task that produces branded output. The skill is for clients and colleagues that
are not connected to the Brain, and for working offline.

## How it is built, and why it is generated

`SKILL.md` is generated. Do not edit it: your change is overwritten on the next
regeneration, and CI fails the moment the committed copy differs from a fresh one.

| Input | Contains |
|---|---|
| `assets/templates/brand.json` | every brand VALUE: colours, typography, geometry, placement, voice, checklist |
| `skill/template.md` | the PROSE and procedure: layouts, the narrative arc, density limits, workflow |

```bash
python skill/generate_skill.py            # regenerate SKILL.md and assets
python skill/generate_skill.py --check    # verify the committed copy is current
```

The generator refuses to run if `template.md` contains a hex colour or a font
family name, because that is precisely how a second source of truth begins. It
also fails if `brand.json` points at an asset that no longer exists.

To change a brand value, edit `brand.json`. To change how it is explained, edit
`template.md`. Then regenerate and commit both.
