# Plainsight Brand Kit

Self-contained, multi-page brand kit. No build step, no internet required (except for Google Fonts to load Inter, which falls back to Segoe UI, Calibri or Arial gracefully).

## How to use it

1. Unzip the folder anywhere.
2. Open `index.html` in any modern browser.
3. Navigate using the left sidebar.

That's it. No server needed — every page works as a local file.

## What's inside

```
plainsight-brand-kit/
├── index.html              # 00 Overview / landing page
├── positioning.html        # 01 Positioning
├── guidelines.html         # 02 The six rules, never look like AI, checklist
├── templates.html          # 03 Templates, presentation and document rules, downloads
├── logos.html              # 04 Logo variants + rules
├── colors.html             # 05 Color swatches (click hex to copy)
├── fonts.html              # 06 Typography specimens
├── voice.html              # 07 How we sound (do/don't)
├── photos.html             # 08 Photo library + where photos go
├── graphics.html           # 09 Triangles & rockets
├── icons.html              # 10 Iconography (Tabler outline)
├── charts.html             # 11 Chart palette + Power BI theme
│
├── css/
│   └── style.css           # Shared stylesheet
│
└── assets/
    ├── logos/
    │   ├── plainsight-logo-blue.svg
    │   ├── plainsight-logo-blue.png
    │   ├── plainsight-logo-white.svg
    │   ├── plainsight-logo-white.png
    │   └── tools/
    │       ├── tools.json       # catalogue of third-party tool logos (Fabric, Power BI, dbt, ...)
    │       └── <slug>.svg | .png  # the vendor's mark, unchanged; PNG rendered from the SVG, 320 px
    ├── graphics/
    │   ├── triangle-blue.svg    # canonical triangle shapes — always place these,
    │   ├── triangle-orange.svg  # never redraw them
    │   ├── triangle-white.svg
    │   ├── triangle-blue.png
    │   ├── triangle-orange.png
    │   ├── triangle-white.png
    │   ├── rocket-vertical.png
    │   └── rocket-diagonal.png
    ├── photos/
    │   └── <slug>.jpg           # real Plainsight people only, at most 400 KB, no EXIF;
    │                            # catalogued in visuals/visuals.json, served on GitHub Pages
    ├── visuals/
    │   ├── visuals.json         # catalogue of approved reusable visuals (slug, title, alt,
    │   │                        # description, source, added); the Brain mirrors it into offers
    │   └── <slug>.png | .jpg    # one file per entry, PNG or JPEG, at most 400 KB, generic only;
    │                            # an entry may instead point at an existing assets/photos file
    └── templates/
        ├── brand.json           # machine-readable brand manifest (for tools & AI agents)
        ├── plainsight-deck-master-2026.potx   # canonical PowerPoint template (snapshot;
        │                                      # live version on SharePoint)
        ├── plainsight-tokens.css
        ├── tailwind.config.js
        └── plainsight-powerbi-theme.json
```

## For tools and AI agents

`assets/templates/brand.json` is the machine-readable version of this kit: colors, typography, layout, charts, icons, photos, logo and triangle rules (including exact placement geometry), voice principles, the `never_look_like_ai` and `agency_principles` rules for client work, and a final checklist. It is the single source of truth for automated brand output. Agents should read it whole and place the triangle/logo asset files directly instead of redrawing them. The triangle SVGs draw their wireframe outline as a filled path internally; that is an SVG implementation detail — the triangle itself is never rendered as a solid filled shape.

`assets/visuals/visuals.json` lists approved reusable visuals (diagrams such as the maturity scan) by slug. The Plainsight Brain mirrors this folder into its offer renderer, so an offer places a visual with `{"kind": "figure", "visual": "<slug>"}` and never pastes image bytes. This repository is public: only generic visuals belong here, never a client name or client data. To add one: export the approved artwork as PNG (about 1600 px wide), add the file and a catalogue entry (`slug`, `file`, `title`, `alt`, `description`, `source`, `added`), open a PR; CI checks both. The photos under `assets/photos/` are catalogued the same way, with the alt text from `photos.html`, so an offer can place one by its file stem. Anything else (a deck, a document, an artifact) uses the public URL `https://plainsightpro.github.io/brand-kit/assets/photos/<slug>.jpg`; `brand.json` → `photos` says where a photo goes and how it is treated. Only add a photo of people who are still at Plainsight and agree to it: this repository and its Pages site are public.

A visual may also carry a moving twin for the offer page: `assets/visuals/<slug>.svg`, listed under `motion` in its catalogue entry. Draw it as SVG with every text outlined (the page shows it as an image, which loads no font), animate it with CSS inside the file, and keep it calm: `brand.json` → `motion` carries the rule (a cycle of at least 8 seconds, transform and opacity only, nothing flashes). CI runs `scripts/check_motion.py`. The PNG stays required: it is what the PDF prints, and it must be the twin at rest.

`assets/logos/tools/` holds third-party logos, the marks of the products we work with (Microsoft Fabric, Power BI, Databricks, dbt, SAP, ...), so the Brain's offer tool can name a tool in a proposal or a diagram. They are for referential use next to the product name, never as Plainsight branding, and they stay as the vendor ships them: no recolouring, cropping or redrawing. Each logo is `<slug>.svg` (the product mark, no text) plus `<slug>.png` rendered from it, with an entry in `tools.json`. To add one: take the SVG from the vendor's official icon set first (Microsoft publishes Fabric, Azure, Power Platform and Dynamics 365 sets), else from an Iconify collection such as `@iconify-json/logos`; strip editor metadata and filters; render the PNG with `npx -y @resvg/resvg-js-cli --fit-width 320 <slug>.svg <slug>.png` (`--fit-height` for a tall mark); add the entry with a `source` precise enough to fetch the file again; run `python scripts/render_tool_logos.py` to refresh `logos.html`. CI checks the catalogue, the SVG allowlist (at most 48 KB) and the PNG (320 px on its longest side, at most 64 KB).

## Updating

This kit is a static site — to change anything, edit the HTML directly. The shared layout (sidebar, header, footer) is duplicated in each page; if you change the navigation, update all 12 files. The shared CSS is in `css/style.css`.

## Version

Pages v1.0, manifest v1.5.0 (`brand.json` → `meta.version`) — maintained by the Plainsight team. Canonical reference: [plainsight.pro](https://www.plainsight.pro).
