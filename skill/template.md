---
name: plainsight-brand
description: "Plainsight visual design system and brand guidelines. Use this skill whenever creating ANY visual output for Plainsight: LinkedIn carousels, single-image posts, PowerPoint presentations, website components or pages, branded diagrams, React artifacts, SVG visuals, or HTML layouts. Trigger on any mention of 'Plainsight', 'carousel', 'LinkedIn post', 'branded slide', 'website layout', or when asked to create visuals that should follow Plainsight brand identity. Also trigger when editing or reviewing existing Plainsight visuals for brand consistency. If the output should look like it comes from Plainsight, use this skill."
---

<!-- GENERATED FILE. Do not edit.
     Values come from assets/templates/brand.json; prose comes from skill/template.md.
     Regenerate with: python skill/generate_skill.py
     CI fails if this file is not identical to a fresh regeneration. -->

# Plainsight Brand Visual Skill

{{META}}

## The one rule that matters most

**Place the asset files. Never draw the shape.**

The triangle and the logo exist as SVG and PNG files in `assets/`. Every time
someone has described the triangle in prose and let a tool draw it from the
description, the result has been wrong: filled instead of outlined, sharp instead
of rounded, or subtly the wrong proportions. A description is not a shape.

So: embed or place `assets/triangle-blue.svg` (and its siblings). Do not trace
them, do not approximate them, do not generate a polygon that looks like them.

If you are connected to the Plainsight Brain over MCP, `brand_get_kit` returns
this same specification plus the asset markup in one call, and `brand://manifest`
serves it as a resource.

## Quick reference

| Output type | Canvas / medium | Start from |
|---|---|---|
| LinkedIn carousel | 1080 x 1350 px (4:5) | Template A or B below |
| LinkedIn single post | 1080 x 1350 px (4:5) | Template B below |
| Presentation | 16:9 | the official .potx, never a blank deck |
| Website | responsive | the CSS tokens and Tailwind config in `assets/templates/` |
| Power BI report | n/a | the Power BI theme in `assets/templates/` |

## Colors

{{COLOR_TABLE}}

{{COLOR_RULES}}

## Typography

{{TYPOGRAPHY}}

## The triangle

{{TRIANGLE_RULE}}

{{TRIANGLE_PLACEMENT}}

## The logo

{{LOGO_PLACEMENT}}

## Templates and tokens

{{TEMPLATE_FILES}}

## LinkedIn visuals

### Canvas

1080 x 1350 px (4:5 ratio). Margins 72 px on all sides, so content width is 936 px.

### Two layouts

**Template A, "warm accent".** Cream background, triangles in both corner pairs,
thick accent lines (160 x 6 px) in the accent colour, punchline cards filled with
the primary colour (24 px radius), closing cards filled with the accent colour
(20 px radius).

**Template B, "bold statements".** Cream background, bottom-left triangle pair
only, oversized typography, accent underline bars (180 x 7 px) beneath titles,
prominent statement cards.

### Seven-slide narrative arc

Carousels follow this structure. It is the shape of the argument, not decoration:

1. **Hook.** A statement that creates curiosity or tension. Max 6 words per line, 3 lines plus a subtitle.
2. **Recognition.** What the reader already sees day to day, so they think "that is us".
3. **Reframe.** The deeper issue underneath, shifting the perspective.
4. **Trade-off.** The two sides in tension, stated fairly.
5. **Practical.** Guardrails or steps someone can actually apply.
6. **Perspective.** The Plainsight point of view, in three or four clear statements.
7. **Closing.** A reflective line that stays with the reader. Not a pitch.

### Slide furniture

- **Position dots.** Top-right, 5 px radius, 18 px spacing. Active dot uses the accent colour; inactive dots use the subtle border colour from the palette.
- **Slide counter.** Bottom-left, "1 / 7" format, in the muted metadata colour, 14 pt.
- **Topic badge.** Top-left pill, uppercase. Primary-colour fill on Template A, accent fill on Template B.
- **Logo.** Bottom-right, 150 px wide, 36 px from the bottom edge.

### Cards and accents

- Rounded corners throughout, 16 to 24 px radius.
- Punchline cards take the primary fill, closing cards the accent fill, content cards white.
- Left accent bars 6 to 8 px wide with rounded ends.
- Bullets are filled circles, 5 px radius, with a 24 px text indent.
- Number badges are 42 to 50 px circles in accent or primary fill, with white text.

### Content density

One idea per slide, and stop before the slide is full:

- Slide 1: one title (max 3 lines) plus one subtitle (max 2 lines)
- Slide 2: title, 3 to 5 observation lines, one punchline
- Slide 3: title, intro, 3 to 5 bullets, closing line
- Slide 4: title, two contrast boxes (each a title plus 3 to 4 bullets), closing line
- Slide 5: title, intro, 3 to 5 cards of title plus description
- Slide 6: title, 3 to 4 statement cards
- Slide 7: one statement (max 3 lines) plus one line of subtext

### Offerings and badge labels

| Offering | Badge label | Typical topics |
|---|---|---|
| AI & GenAI | `AI & GENAI · PLAINSIGHT` | AI pilots, production AI, shadow AI, guardrails |
| Data & Analytics | `DATA & ANALYTICS · PLAINSIGHT` | Data foundations, reporting trust, platform adoption |
| Strategy & Governance | `STRATEGY & GOVERNANCE · PLAINSIGHT` | Ownership, prioritisation, maturity, governance |

## Website

- Alternate cream and primary-colour sections down the page; white is for cards sitting on top of them.
- One triangle maximum in a hero, top-right, at low opacity.
- Decorative elements are always `pointer-events: none` and `aria-hidden="true"`.
- CTA buttons are pill-shaped, uppercase, with wide letter spacing and semibold weight.
- Use the CSS custom properties and Tailwind config from `assets/templates/` rather than hardcoding values.

## Presentations

- Start from the official .potx. Do not rebuild slide layouts from scratch.
- Cream for content slides, primary colour for section dividers and the closing slide.
- Logo on the title and closing slides only, bottom-right, matched to the slide background.
- Triangles are corner decoration only, subtle, never over content.
- One idea per slide, one or two sentences per block.

## Voice

{{VOICE}}

## Before you ship

{{CHECKLIST}}

## Bundled reference

| Path | What it is |
|---|---|
| `assets/triangle-blue.svg` | Canonical wireframe triangle for light and cream backgrounds |
| `assets/triangle-orange.svg` | Canonical wireframe triangle for accent use |
| `assets/triangle-white.svg` | Canonical wireframe triangle for primary-colour and dark backgrounds |
| `assets/logo-blue.svg` | Logo for light backgrounds |
| `assets/logo-white.svg` | Logo for primary-colour and dark backgrounds |
| `assets/brand.json` | The machine-readable manifest every value above came from |

Larger assets stay in the brand-kit repository rather than in this skill: the
PowerPoint master, photography, the rocket motif, PNG variants, the Power BI
theme, and the CSS and Tailwind token files.
