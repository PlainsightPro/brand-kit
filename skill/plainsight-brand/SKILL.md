---
name: plainsight-brand
description: "Plainsight visual design system and brand guidelines. Use this skill whenever creating ANY visual output for Plainsight: LinkedIn carousels, single-image posts, PowerPoint presentations, website components or pages, branded diagrams, React artifacts, SVG visuals, or HTML layouts. Trigger on any mention of 'Plainsight', 'carousel', 'LinkedIn post', 'branded slide', 'website layout', or when asked to create visuals that should follow Plainsight brand identity. Also trigger when editing or reviewing existing Plainsight visuals for brand consistency. If the output should look like it comes from Plainsight, use this skill."
---

<!-- GENERATED FILE. Do not edit.
     Values come from assets/templates/brand.json; prose comes from skill/template.md.
     Regenerate with: python skill/generate_skill.py
     CI fails if this file is not identical to a fresh regeneration. -->

# Plainsight Brand Visual Skill

Generated from `brand.json` v1.1.0 (updated 2026-08-15). Source of truth: https://github.com/PlainsightPro/brand-kit. When any other document disagrees with the manifest, the manifest wins.

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

| Name | Hex | Role |
|---|---|---|
| blue | `#000075` | Primary. Headings, dark backgrounds, default text on light. |
| orange | `#d5693a` | Accent only. CTAs, links, highlights, bullets, badges. Never a full-section or full-slide background. |
| orange svg variant | `#BD5428` | Only appears inside triangle-orange.svg. Do not use as a UI color. |
| cream | `#fcf8f3` | Default page and slide background. |
| white | `#ffffff` | Cards and content containers. |
| mist | `#f6f6fa` | Light background variant. |
| muted cream | `#F3ECE4` | Alternating section backgrounds (web). |
| dark text | `#1a1a3e` | Body text on light backgrounds (softer navy). |
| muted blue | `#8888bb` | Secondary metadata, labels, counters. |
| light navy | `#b0b0d0` | Subtitle text on dark backgrounds. |
| light gray | `#e8e8e8` | Subtle card borders. |

- Blue and cream alternate as backgrounds; white is for cards.
- Orange is always an accent, never a background fill for a section or slide.
- Text on blue = white or light navy. Text on cream = blue or dark text.
- All pairings must meet WCAG AA contrast.

## Typography

| Use | Family | Fallback |
|---|---|---|
| Headings | **Titillium Web** | Segoe UI, Arial, sans-serif |
| Body | **Inter** | Segoe UI, Arial, sans-serif |

Heading style: Bold, uppercase for section headings, wider tracking.

- Maximum 2 font weights per slide or section.
- No italics in carousels or slides.
- Short blocks: 1-2 sentences per paragraph on slides.

## The triangle

The Plainsight triangle is a WIREFRAME OUTLINE with rounded corners. It is never a solid filled triangle. Always place the canonical SVG/PNG files below; never redraw the shape. The SVG paths use a fill attribute internally to paint the outline strokes; that is an implementation detail, not permission to fill the triangle.

**Hard rules.**

- Never fill the triangle with a solid color.
- Never redraw or approximate the triangle; place the asset files.
- Only three colors exist: blue, orange, white.
- One motif per piece: triangles or rocket, not both.
- No triangle larger than one third of the page. Accents, not heroes.
- Decorative only: never obscure text or interactive content (pointer-events: none, aria-hidden).

| Variant | File | Use on |
|---|---|---|
| blue | `assets/triangle-blue.svg` | light / cream backgrounds |
| orange | `assets/triangle-orange.svg` | blue or cream backgrounds (hero accents) |
| white | `assets/triangle-white.svg` | blue or dark backgrounds |

Native size: 313 x 358 px.

### Placement

**Principle.** Triangles appear in asymmetric pairs at canvas corners, partially cropped: 60% visible, 40% bleeding off the canvas edge. Never centered in a clear frame.

**LinkedIn slides.**

- Scale: 1.1
- Effective size: 344 x 394 px
- top right pair:
  - back: `x = canvas_width - triangle_width + 30, y = canvas_height - 0.4 * triangle_height`
  - front: `back position shifted left 90 px and down 60 px`
- bottom left pair:
  - left lower: `x = -30, y = -0.4 * triangle_height - 60`
  - right higher: `x = left_x + 120, y = -0.4 * triangle_height`
- Template A: both corner pairs
- Template B: bottom-left pair only

**Website.**

- cream sections: Top-right corner, blue at 10-15% opacity.
- navy sections: Top-right and bottom-left, white at 5-10% opacity. CTA and footer only.
- hero: One triangle maximum, top-right.

**Presentations.** Corner decoration only, subtle, never obscuring content.

## The logo

| Variant | File | Use on |
|---|---|---|
| blue | `assets/logo-blue.svg` | light backgrounds |
| white | `assets/logo-white.svg` | blue or dark backgrounds |

- **Linkedin.** Bottom-right, 150 px wide, 36 px from bottom edge. Blue version.
- **Website.** Header 160x28 px. Blue on light, white on navy footer.
- **Presentations.** Title and closing slides only, bottom-right, matched to slide background.

## Templates and tokens

**2026 PowerPoint template (rebranding).** All Plainsight decks start from this template. Do not rebuild slide layouts from scratch. SharePoint holds the live version; the bundled file is a snapshot.

- In brand-kit: `brand-kit:assets/templates/plainsight-deck-master-2026.potx`
- Live version: SharePoint > Plainsight > General > Digital Templates > Office Templates > 2026_PWP Sjabloon Plainsight rebranding.potx

| Asset | Path | Bundled |
|---|---|---|
| power bi theme | `assets/templates/plainsight-powerbi-theme.json` | yes |
| css tokens | `assets/templates/plainsight-tokens.css` | yes |
| tailwind config | `assets/templates/tailwind.config.js` | yes |

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

Senior practitioners who respect the reader's time. Knowledge first, in clear human language. We must never sound like AI wrote it, and never sound like every other consultancy.

- **Clear, not clever.** Short sentences. Plain English or plain Dutch. Trade the buzzword for the thing it describes.
- **Concrete, not vague.** Numbers, timeframes, named technologies. '30% faster' beats 'significantly faster'.
- **Confident, not loud.** No caps-shouting, no stacked exclamation marks. The work speaks; we describe it.
- **Expert, not jargon.** For output leaving Plainsight, keep technical language light. Show expertise through concrete examples and honest observations, not through vocabulary.

### Never sound like AI wrote it

- No em dashes or en dashes as separators. Use commas, periods, or restructure.
- No AI-style anecdote openers ('This was my Tuesday morning', 'I'm thrilled to announce').
- No dramatic rule-of-three ('innovation, inspiration, and impact'). Use the natural number of items.
- No numbered lists of obvious advice, no generic conclusions ('The future looks bright'), no signposting.
- If a sentence could appear on any consultancy's feed, rewrite it or cut it.

**Banned words and phrases:** `genuinely`, `straightforward`, `it's worth noting`, `let's dive in`, `in today's landscape`, `leverage`, `game-changer`, `cutting-edge`, `pivotal`, `ecosystem`, `foster`, `elevate`, `moreover`, `furthermore`, `showcase`, `delve`, `key takeaway`, `utilize`, `synergy`, `tapestry`, `navigate (metaphorical)`

**Culture.**

- Transparent by default: we say what we do, why, and what comes next.
- We share feedback openly, and knowledge beyond the boundaries of our own organisation.
- Not corporate, no hierarchy in tone. Taking responsibility means ownership, not being the boss of someone else.

**Sound like.**

- Human, warm, intelligent
- Accessible, calm confidence
- Smart friend over coffee, not a press release

**Avoid.**

- Generic consultancy speak
- Inflated claims and hype language
- Buzzwords without substance
- Anything that reads as AI-generated

**LinkedIn.** Knowledge-sharing first: every post should teach something, from a practitioner's perspective. One point per post, made well, under 150 words. Concrete examples from real situations. Never sound like all the others.

## Before you ship

- [ ] Background is cream #fcf8f3 or blue #000075, never orange.
- [ ] Triangles placed from asset files, wireframe, rounded, in asymmetric corner pairs, 60% visible.
- [ ] Orange used only as accent.
- [ ] Max 2 font weights; headings Titillium Web bold uppercase, body Inter.
- [ ] Logo from asset files, correct variant for the background.
- [ ] Decks start from the official .potx template.
- [ ] Copy passes the voice test: clear, concrete, confident; no buzzwords, no banned words, no em dashes.
- [ ] One motif (triangles or rocket), decorations never obscure content.

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
