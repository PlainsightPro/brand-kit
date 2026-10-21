# Plainsight Brand Kit

Self-contained, multi-page brand kit. No build step, no internet required (except for Google Fonts to load Titillium Web and Inter — falls back to Arial gracefully).

## How to use it

1. Unzip the folder anywhere.
2. Open `index.html` in any modern browser.
3. Navigate using the left sidebar.

That's it. No server needed — every page works as a local file.

## What's inside

```
plainsight-brand-kit/
├── index.html              # Overview / landing page
├── guidelines.html         # 01 The six rules + checklist
├── templates.html          # 02 Templates + downloads
├── logos.html              # 03 Logo variants + rules
├── colors.html             # 04 Color swatches (click hex to copy)
├── fonts.html              # 05 Typography specimens
├── voice.html              # 06 How we sound (do/don't)
├── photos.html             # 07 Photography rules
├── graphics.html           # 08 Triangles & rockets
├── icons.html              # 09 Iconography (Tabler outline)
├── charts.html             # 10 Chart palette + Power BI theme
│
├── css/
│   └── style.css           # Shared stylesheet
│
└── assets/
    ├── logos/
    │   ├── plainsight-logo-blue.svg
    │   ├── plainsight-logo-blue.png
    │   ├── plainsight-logo-white.svg
    │   └── plainsight-logo-white.png
    ├── graphics/
    │   ├── triangle-blue.svg    # canonical triangle shapes — always place these,
    │   ├── triangle-orange.svg  # never redraw them
    │   ├── triangle-white.svg
    │   ├── triangle-blue.png
    │   ├── triangle-orange.png
    │   ├── triangle-white.png
    │   ├── rocket-vertical.png
    │   └── rocket-diagonal.png
    ├── visuals/
    │   ├── visuals.json         # catalogue of approved reusable visuals (slug, title, alt,
    │   │                        # description, source, added); the Brain mirrors it into offers
    │   └── <slug>.png | .jpg    # one file per entry, PNG or JPEG, at most 400 KB, generic only
    └── templates/
        ├── brand.json           # machine-readable brand manifest (for tools & AI agents)
        ├── plainsight-deck-master-2026.potx   # canonical PowerPoint template (snapshot;
        │                                      # live version on SharePoint)
        ├── plainsight-tokens.css
        ├── tailwind.config.js
        └── plainsight-powerbi-theme.json
```

## For tools and AI agents

`assets/templates/brand.json` is the machine-readable version of this kit: colors, typography, logo and triangle rules (including exact placement geometry), voice principles, and a final checklist. It is the single source of truth for automated brand output. Agents should read it whole and place the triangle/logo asset files directly instead of redrawing them. The triangle SVGs draw their wireframe outline as a filled path internally; that is an SVG implementation detail — the triangle itself is never rendered as a solid filled shape.

`assets/visuals/visuals.json` lists approved reusable visuals (diagrams such as the maturity scan) by slug. The Plainsight Brain mirrors this folder into its offer renderer, so an offer places a visual with `{"kind": "figure", "visual": "<slug>"}` and never pastes image bytes. This repository is public: only generic visuals belong here, never a client name or client data. To add one: export the approved artwork as PNG (about 1600 px wide), add the file and a catalogue entry (`slug`, `file`, `title`, `alt`, `description`, `source`, `added`), open a PR; CI checks both.

## Updating

This kit is a static site — to change anything, edit the HTML directly. The shared layout (sidebar, header, footer) is duplicated in each page; if you change the navigation, update all 11 files. The shared CSS is in `css/style.css`.

## Version

v1.0 — maintained by the Plainsight team. Canonical reference: [plainsight.pro](https://www.plainsight.pro).
