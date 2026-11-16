---
name: plainsight-brand
description: "Plainsight visual design system and brand guidelines. Use this skill whenever creating ANY visual output for Plainsight: LinkedIn carousels, single-image posts, PowerPoint presentations, website components or pages, branded diagrams, React artifacts, SVG visuals, or HTML layouts. Trigger on any mention of 'Plainsight', 'carousel', 'LinkedIn post', 'branded slide', 'website layout', or when asked to create visuals that should follow Plainsight brand identity. Also trigger when editing or reviewing existing Plainsight visuals for brand consistency. If the output should look like it comes from Plainsight, use this skill."
---

<!-- GENERATED FILE. Do not edit.
     Values come from assets/templates/brand.json; prose comes from skill/template.md.
     Regenerate with: python skill/generate_skill.py
     CI fails if this file is not identical to a fresh regeneration. -->

# Plainsight Brand Visual Skill

Generated from `brand.json` v1.5.0 (updated 2026-11-16). Source of truth: https://github.com/PlainsightPro/brand-kit. When any other document disagrees with the manifest, the manifest wins.

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
| PowerPoint deck | 16:9 | the official .potx, never a blank deck |
| Claude Slides or HTML deck | the slide canvas under Layout | Layout, Never look like AI and Make it look curated below |
| Proposal, offer or document | page or web page | Make it look curated below, per format |
| Website | responsive | the CSS tokens and Tailwind config in `assets/templates/` |
| Power BI report | n/a | the Power BI theme in `assets/templates/` and the Charts rules |

Client work (proposals, offers, decks, documents, reports, dashboards,
artifacts) has one more rule on top of everything here: it must never look
AI-generated. Read **Never look like AI** before you draw a single box.

## Colors

| Name | Hex | Role |
|---|---|---|
| blue | `#000075` | Primary. Headings, dark backgrounds, default text on light. |
| orange | `#d5693a` | Accent only. CTAs, links, highlights, bullets, badges. Never a full-section or full-slide background. |
| orange svg variant | `#BD5428` | Only appears inside triangle-orange.svg. Do not use as a UI color. |
| cream | `#fcf8f3` | Default page and slide background. |
| white | `#ffffff` | Cards and content containers. |
| mist | `#f6f6fa` | Light background variant. |
| muted cream | `#F3ECE4` | Alternating section backgrounds (web). Quiet panels, table headers and the one highlighted row or column. |
| dark text | `#1a1a3e` | Body text on light backgrounds (softer navy). |
| muted blue | `#8888bb` | Secondary metadata, labels, counters. |
| light navy | `#b0b0d0` | Subtitle text on dark backgrounds. |
| light gray | `#e8e8e8` | Subtle card borders. Decorative only. |

- Blue and cream alternate as backgrounds; white is for cards.
- Orange is always an accent, never a background fill for a section or slide.
- One accent per slide or section: one numeral, one call to action, or one highlighted bar or row in orange.
- Text on blue = white or light navy. Text on cream = blue or dark text.
- Text on an orange fill is blue (4.70:1). White on orange (3.55:1) only at large sizes, from 18.66 px bold or 24 px regular.
- Light gray borders are decorative only (1.16:1). A border that carries meaning, like a table header line, an input border or a chart baseline, is blue.
- All pairings must meet WCAG AA contrast.

## Typography

| Use | Family | Fallback |
|---|---|---|
| Headings | **Titillium Web** | Segoe UI, Arial, sans-serif |
| Body | **Inter** | Segoe UI, Arial, sans-serif |

Heading style: Bold. Uppercase with wider tracking for section headings, labels and buttons. Action titles, the full-sentence titles that state a conclusion, in sentence case.

**Never use:** `Quicksand`, `Quicksand Light`, `Bahnschrift`, `Tw Cen MT`, `Calibri`, `Calibri Light`, `Epilogue`

A file may specify one of these anyway. The deck master's own layouts and theme do (Bahnschrift, Tw Cen MT, Calibri). Override it: this manifest wins over any template, layout, text box or inherited theme. Only the families above are Plainsight typography, with the listed fallbacks when they are not installed.

- Weights: Titillium Web 700 for headings, labels and numerals; Inter 400 for everything you read.
- Maximum 2 font weights per slide or section.
- No italics anywhere. A quote is set apart by size and colour, not by slant.
- Emphasis comes from colour (blue) or a small uppercase label, never bold Inter.
- Short blocks: 1-2 sentences per paragraph on slides.

## Layout

Applies to: Decks, proposals, offers, documents, reports, dashboards and pages generated for a client or prospect. The website component library and the LinkedIn carousel templates keep their own documented layouts (templates.html).

**Slide canvas.** 1280x720 px with 64 px margins. Scale the canvas, never re-flow it.

- Prefer asymmetric splits: 5/7 for a claim and its evidence, 2/10 for a quote and its label. Equal columns only when the content is equal, like options compared on the same criteria.
- One idea per slide. If a slide needs a second chart, it becomes two slides.
- Left-aligned by default. Centre only a single short statement on its own slide.
- Every slide or page that shows data has a source line, bottom left, in a small uppercase label.
- Corners are square in decks and print. A 2 px radius on buttons, inputs and badges is the only rounding there. Pages on the web follow the website: 8 to 12 px on cards and photos.

**Motion on slides.** No slide transitions and no build animations. A deck shows the still PNG of a visual; its moving twin is for web pages, offers and artifacts.

## The triangle

The Plainsight triangle is a WIREFRAME OUTLINE with rounded corners. It is never a solid filled triangle. Always place the canonical SVG/PNG files below; never redraw the shape. The SVG paths use a fill attribute internally to paint the outline strokes; that is an implementation detail, not permission to fill the triangle.

The triangle is what makes a piece recognisably Plainsight before anyone reads a word. Generic output is fixed with format rules (never_look_like_ai), never by removing the triangles.

**Hard rules.**

- Never fill the triangle with a solid color.
- Never redraw or approximate the triangle; place the asset files.
- Only three colors exist: blue, orange, white.
- One motif per piece: triangles or rocket, not both.
- No triangle larger than one third of the page. Accents, not heroes.
- Decorative only: never obscure text or interactive content (pointer-events: none, aria-hidden).
- Never use the triangle as a bullet, an icon or a ▲ glyph.

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

- cream sections: Top-right pair, blue at 10-15% opacity.
- navy sections: Top-right and bottom-left pairs, white at 5-10% opacity. CTA and footer only.
- hero: One pair, top-right.

**Documents.**

- principle: Proposals, offers and other long-form documents carry the triangles where the reader turns to a new part of the story: one asymmetric top-right pair on the opening screen, cropped by the page edges, one pair on every chapter opener or section divider that starts on its own page or band, and one pair on the closing page. Pages that carry the argument (running text, tables, charts) stay free of triangles so the content reads clean.
- opacity: Blue at 10-15% on cream, white at 5-10% on blue.
- top right pair:
  - back: Aligned to the top-right page corner, about 40% of the triangle cropped away by the top and right edges.
  - front: The same triangle shifted 90 px left and 60 px down from the back one, so the two overlap.
- chapter openers: Top-right pair as on the opening screen, or the bottom-left pair when the chapter title sits top-right. Same opacity. Never on a page that also holds a table or chart.

**Presentations.** Title, section divider and closing slides carry a corner pair. Content slides may carry a subtle pair in a free corner, as long as it never touches text, a chart or a table.

## The logo

| Variant | File | Use on |
|---|---|---|
| blue | `assets/logo-blue.svg` | light backgrounds |
| white | `assets/logo-white.svg` | blue or dark backgrounds |

- **Linkedin.** Bottom-right, 150 px wide, 36 px from bottom edge. Blue version.
- **Website.** Header 160x28 px. Blue on light, white on navy footer.
- **Presentations.** Title and closing slides only, bottom-right, matched to slide background.
- **Documents.** On the cover. A running header or footer may carry it small; never a second large logo inside the document.

## Photos

Only real Plainsight people, our own office and our own events, placed from the files in the catalogue. Never stock photos of people, never AI-generated people or offices.

- **Proposals and documents.** One photo, two at most, where the reader meets the people: the 'who we are' or team section, or the closing page. Never on a page that carries the argument.
- **Decks.** A photo gets its own slide or the 5 column of a 5/7 split, bled to the slide edge: the about-us slide, the team slide or the closing slide.
- **Headshots.** Portraits of a proposed team come from the website's meet-the-team pages, not from this catalogue.

**Treatment.**

- Never tint, duotone or overlay a photo. The colour comes from the layout around it.
- No text on top of a photo. A title or caption sits next to it.
- Square corners in decks and print; 8 to 12 px radius on the web. No circles, blobs or decorative borders.
- A triangle pair may sit near a photo, never on it.
- Every placed photo carries its alt text from the catalogue.

Every catalogue entry whose file sits in assets/photos/ is a photo, with alt text that says who and what. Pick by that alt text. Offers place one by slug; anything else uses the file under base_url.

| Slug | URL | Shows |
|---|---|---|
| `jobs-culture` | https://plainsightpro.github.io/brand-kit/assets/photos/jobs-culture.jpg | The full Plainsight team posing together for a group portrait in front of greenery |
| `about-team-1` | https://plainsightpro.github.io/brand-kit/assets/photos/about-team-1.jpg | Four Plainsight team members goofing around with an indoor exercise bike at the office |
| `experts-how-we-work` | https://plainsightpro.github.io/brand-kit/assets/photos/experts-how-we-work.jpg | Two Plainsight consultants in animated conversation at the office lounge |
| `experts-team-1` | https://plainsightpro.github.io/brand-kit/assets/photos/experts-team-1.jpg | Three Plainsight consultants working side by side on laptops in a vaulted workspace |
| `experts-team-2` | https://plainsightpro.github.io/brand-kit/assets/photos/experts-team-2.jpg | A Plainsight consultant presenting to a small audience seated at the back of a meeting room |
| `events-knowledge-1` | https://plainsightpro.github.io/brand-kit/assets/photos/events-knowledge-1.jpg | A Plainsight speaker holding a microphone and engaging the audience at a knowledge-sharing event |
| `events-knowledge-2` | https://plainsightpro.github.io/brand-kit/assets/photos/events-knowledge-2.jpg | Workshop attendees following a Plainsight presentation projected on a big screen |
| `events-knowledge-3` | https://plainsightpro.github.io/brand-kit/assets/photos/events-knowledge-3.jpg | Two Plainsight panelists with microphones speaking at an event |
| `events-knowledge-4` | https://plainsightpro.github.io/brand-kit/assets/photos/events-knowledge-4.jpg | A large audience seated in green chairs at a Plainsight knowledge-sharing session |
| `events-img-5345` | https://plainsightpro.github.io/brand-kit/assets/photos/events-img-5345.jpg | Engaged audience with hands raised during a Plainsight workshop |
| `projects-webres-88` | https://plainsightpro.github.io/brand-kit/assets/photos/projects-webres-88.jpg | Five Plainsight colleagues around a small round table in the office lounge, one writing notes |
| `projects-webres-15` | https://plainsightpro.github.io/brand-kit/assets/photos/projects-webres-15.jpg | Plainsight consultants working at their desks, seen through a window framed by leaves |
| `projects-webres-180` | https://plainsightpro.github.io/brand-kit/assets/photos/projects-webres-180.jpg | Seven Plainsight colleagues around a meeting table, following one laptop while one of them points at the screen |
| `projects-webres-28` | https://plainsightpro.github.io/brand-kit/assets/photos/projects-webres-28.jpg | Four Plainsight colleagues chatting in the office kitchen by a dartboard |
| `strategy-webres-86` | https://plainsightpro.github.io/brand-kit/assets/photos/strategy-webres-86.jpg | Plainsight colleagues talking around a small round table by the window, one taking notes |
| `strategy-webres-55` | https://plainsightpro.github.io/brand-kit/assets/photos/strategy-webres-55.jpg | A Plainsight consultant standing beside the Plainsight rocket mural while a colleague works at a laptop, seen through a window |
| `scans-ai` | https://plainsightpro.github.io/brand-kit/assets/photos/scans-ai.jpg | Four Plainsight consultants working at a shared wooden table in a vaulted office |
| `scans-dashboard` | https://plainsightpro.github.io/brand-kit/assets/photos/scans-dashboard.jpg | A Plainsight consultant analyzing a dashboard on a desktop monitor |
| `office-gent-team` | https://plainsightpro.github.io/brand-kit/assets/photos/office-gent-team.jpg | The Plainsight team gathered for a cheerful group photo on the floor of the Gent office |
| `office-gent-collaboration` | https://plainsightpro.github.io/brand-kit/assets/photos/office-gent-collaboration.jpg | Plainsight colleagues laughing together around a laptop at the long desks of the Gent office |
| `office-gent-floor` | https://plainsightpro.github.io/brand-kit/assets/photos/office-gent-floor.jpg | A wide view of the Gent office with Plainsight consultants at work behind rows of monitors |
| `office-gent-pairing` | https://plainsightpro.github.io/brand-kit/assets/photos/office-gent-pairing.jpg | A Plainsight consultant leaning over to help a colleague at a screen while another looks on |
| `office-gent-colleagues` | https://plainsightpro.github.io/brand-kit/assets/photos/office-gent-colleagues.jpg | Two Plainsight colleagues smiling at each other across their desks in the Gent office |
| `office-gent-focus` | https://plainsightpro.github.io/brand-kit/assets/photos/office-gent-focus.jpg | A Plainsight consultant typing at a laptop while a colleague works at a standing desk in the background |
| `office-gent-screen` | https://plainsightpro.github.io/brand-kit/assets/photos/office-gent-screen.jpg | A Plainsight consultant working on a data application on a large monitor in the Gent office |
| `office-gent-headphones` | https://plainsightpro.github.io/brand-kit/assets/photos/office-gent-headphones.jpg | A smiling Plainsight consultant with headphones at a laptop in the Gent office |
| `office-gent-conversation` | https://plainsightpro.github.io/brand-kit/assets/photos/office-gent-conversation.jpg | Two Plainsight consultants in conversation across their desks in the Gent office |
| `office-gent-meeting-room` | https://plainsightpro.github.io/brand-kit/assets/photos/office-gent-meeting-room.jpg | Two Plainsight colleagues in a meeting room, seen through the glass wall of the Gent office |
| `office-gent-rocket` | https://plainsightpro.github.io/brand-kit/assets/photos/office-gent-rocket.jpg | A Plainsight consultant at a laptop by the window, the Plainsight rocket in the background |

## Charts

Palette in order: `#000075`, `#3939A0`, `#7373AA`, `#ADADD4`.
Accent, for the one point the title is about: `#d5693a`.

- Bars and lines in blue. The series or bar the title is about in orange. Nothing else is coloured.
- Several series with no semantic difference take the blue tints of the palette in order. Never a new hue.
- Label data directly and drop the legend when labels fit. Axis titles and notes in small labels or captions.
- Sort bars by value unless the axis is time.
- No 3D, no pie charts with more than three slices, no donut KPIs, no gauges.
- Power BI: templates.power_bi_theme carries this palette, with the accent last so it is set by hand on the point that matters.

## Icons

**Set.** Tabler Icons, outline variant (https://tabler.io/icons). MIT-licensed.

- Use an icon where it helps recognition (a UI control, a process step with a distinct object), not as decoration. A label often does the job better.
- Outline only, 1.5 px stroke at 24 px, one size per layout.
- Blue on light, white on blue. Orange only next to an orange call to action or highlight.
- Never inside a tinted circle or square, and never one above every heading or bullet.

## Never look like AI

Nothing we send should look AI-generated. What gives AI output away is a default used without a reason: the same shape repeated to fill space, decoration that carries no information, numbers without context. Formats are allowed when they help the client understand something; what changes is how we draw them.

Applies to: Everything generated for a client or prospect: proposals, offers, decks, documents, reports, dashboards, spreadsheets, artifacts and one-off pages. The website component library and the LinkedIn carousel templates are designed systems with their own documented shapes (templates.html) and keep them.

**Before you use any element, check both:**

- The element carries information specific to this client: a real number, a named role, a date, a choice.
- It is drawn the Plainsight way, not with a generic default.

**Never.**

- Gradients of any kind, including gradient text and buttons.
- Drop shadows, glow, glassmorphism, blurred or frosted panels, noise textures. Separation comes from a muted cream panel, a hairline or space.
- Emoji.
- Decorative icons, such as an icon in a tinted circle above every heading or bullet.
- Rows of identical boxes: three or four cards, tiles or columns of the same shape, each with a title and a vague line.
- Cards with a coloured left border as the accent.
- Check and cross marks or traffic-light dots standing in for words.
- Stock 3D illustrations, abstract blobs, isometric people, AI-generated images.
- Dark slate or charcoal 'tech' themes. The dark ground is blue.
- Rainbow charts.
- Pill shapes and large rounded corners.

| Format | Looks AI-generated when | Plainsight version |
|---|---|---|
| KPI tiles | Numbers with a label and nothing else, an arrow icon, tiles added to fill a row. | A row of at most four figures under a blue rule, each with a comparison, the period and a status word; the one that needs attention marked in orange. When one figure carries the point, show it alone, large, with its comparison and source. |
| Cards side by side | Identical boxes with an icon, a title and two vague lines. | A comparison table: options as columns, criteria as rows, the advised option highlighted. Recommendations as a numbered list of decisions, each with an owner and a date. |
| Timeline | Evenly spaced dots on a line, activities without outcomes. | Phases as bands sized by their real duration, each with the outcome it delivers, and a marker for today. |
| Agenda | Numbered circles. | A short list with small numbers, or a section divider slide per chapter. |
| Checkmarks, before and after | Check and cross marks as decoration, red against green. | A table with words ('Yes', 'Partly', 'From Q3'). Colour only backs up the word. |
| Status indicators | A traffic-light dot alone. | The status as a word ('On track', 'Behind'), with orange marking the one that needs attention. |
| Summary or takeaway | A generic box at the bottom repeating the slide. | The conclusion goes in the action title. A deck summary is a numbered list of decisions. |
| Icons | One above every heading. | Tabler outline icons per iconography, only where they help recognition. |
| Photos | Stock people pointing at screens, AI-generated offices, a photo used as a background behind text. | Our own people from the photos catalogue, next to the text, never under it. |
| Centred text | The default for everything. | Left-aligned by default. Centre only a single short statement on its own slide. |
| Title, subtitle and three bullets | Every slide has this shape. | Vary the slide by what the content needs: claim and evidence, one big number, a quote, a table, a photo of the team. Bullets are fine for a real list. |

## Make it look curated

Everything made for Plainsight or its clients: decks, documents, web pages, dashboards, spreadsheets and visual designs. The aim is work that looks curated by a design agency for this one client: editing first, then a few custom moments, then precise finishing. Decoration does not get it there.

1. Summary first. The first screen, slide or paragraph holds the whole story: the decision in one sentence, the advice in numbers, the key figure with its comparison, and the ask.
2. Argument, then appendix. The main body keeps only what builds the argument: five or six chapters at most, each with an action title. Detail tables, full comparisons, assumptions and sources go to an appendix marked A, B, C, and each chapter points to the appendix that backs it.
3. One grid, one left edge. Every page, slide and section sits on a strict grid with all text starting on one edge. Long documents and pages put the chapter number and label in a left margin column; slides use the 5/7 and 2/10 splits.
4. One signature graphic per argument. Look in the visuals catalogue (assets/visuals/visuals.json) first: a catalogued visual that fits beats a new one. Otherwise find the picture only this client's situation has and draw it to scale, such as one dot per employee to show who a choice reaches, or cost against reach to compare options of different size. A new graphic that works goes back into the catalogue.
5. Precise finishing. Numbers and their units never break across lines ('€ 107', '± 600'). Product names stay on one line. Tables, charts and key numbers use figures of equal width. Sources are numbered footnotes linking to a numbered source list. One number format per piece (Dutch: 15.000 and 4,0; English: 15,000 and 4.0).

### Per format

- **Decks.** Title slide, summary slide, then per chapter a section divider followed by the content slides the story needs, then roadmap, decisions, closing slide and appendix slides. One signature graphic on its own slide, at least 760 px wide on the 1280x720 canvas, labels 14 px or larger. A team photo on the about-us, team or closing slide, per photos.use.
- **Documents.** A summary block first, then numbered chapters with action-title headings, then appendices. Headings Titillium Web 700, body Inter 400 at 11 pt in print. Tables with an uppercase header over a blue rule and hairlines between rows, no shading except one highlighted row. Logo and a triangle pair on the cover, a pair on each chapter opener and the closing page (triangles.placement.documents). A team photo where the reader meets the people (photos.use). Sources as numbered footnotes or a numbered list at the end.
- **Web pages and artifacts.** The summary on the first screen, chapters on the margin grid, the appendix at the end. One look in every viewer setting: no dark mode unless the brief asks for one.
- **Dashboards.** One line that says what changed and what needs attention, then at most four key figures, each with a comparison, period and status word. Detail charts below in blue, the point that needs attention in orange. Every number shows its source and refresh date.
- **Spreadsheets.** Header row in uppercase on muted cream with a blue bottom rule, no fill colours in the body. Numbers right-aligned with consistent decimals and thousands separators. One highlight colour (muted cream) for the row or column that matters. Inputs and assumptions on their own labelled tab.
- **Visual designs.** One message, one figure or image, one accent.

### Final check before anything leaves Plainsight

- The first screen or slide tells the whole story.
- Detail sits in the appendix, not in the argument.
- There is one signature graphic, drawn to scale.
- Nothing from never_look_like_ai.never appears; other formats are in their Plainsight version.
- Orange appears once per slide or section, as an accent.
- Every number has a source. Numbers and units don't break across lines.
- Photos come from the photos catalogue, or there are none.
- The agent_checklist passes.

## Templates and tokens

**2026 PowerPoint template (rebranding).** All Plainsight PowerPoint files start from this template. Do not rebuild its slide layouts from scratch. Decks generated in Claude Slides or as HTML cannot start from a .potx: they follow layout, never_look_like_ai and agency_principles in this manifest on the same 1280x720 canvas. SharePoint holds the live version; the bundled file is a snapshot.

- In brand-kit: `brand-kit:assets/templates/plainsight-deck-master-2026.potx`
- Live version: SharePoint > Plainsight > General > Digital Templates > Office Templates > 2026_PWP Sjabloon Plainsight rebranding.potx

**Plainsight design system (Claude).** A design system in Claude (slide layouts, components, tokens) is generated from this manifest and owned with this repository, never kept as a separate source. When the two disagree, this manifest wins and the design system is regenerated.

- Status: Proposed, not yet published. Until it is, Claude Slides decks and artifacts are built from this manifest directly.

| Asset | Path | Bundled |
|---|---|---|
| power bi theme | `assets/templates/plainsight-powerbi-theme.json` | yes |
| css tokens | `assets/templates/plainsight-tokens.css` | yes |
| tailwind config | `assets/templates/tailwind.config.js` | yes |

## Known problems in the assets

**`brand-kit:assets/templates/plainsight-deck-master-2026.potx`**

- Also affects: the live SharePoint version of the same template
- Problem: The layouts and text boxes carry fonts that are not Plainsight typography. The bundled snapshot's four themes use Bahnschrift, Tw Cen MT, Calibri Light and Calibri; the live SharePoint file additionally has Quicksand Light on layout text boxes and resists being changed there.
- What to do: Start from the template for the layouts and the geometry, then set type from typography above. Never keep the inherited font because the template offered it.
- Status: open, reported 2026-08-16

**`brand-kit:`**

- Problem: colors.rules requires WCAG AA on every pairing, and these two cannot meet it as body-size text on cream. Orange #d5693a reaches 3.36:1 and muted_blue #8888bb 3.16:1, where AA asks 4.5:1 for normal text. Both clear the 3:1 bar for large text, borders, icons and other non-text UI, and both pass on the blue ground (4.70:1 and 5.00:1). Their stated roles put them on small text, so an agent following the roles literally on cream produces text that fails AA.
- What to do: On cream or white, use these two for borders, bullets, icons, badges and other non-text accents, or for large text from 18.66px bold upward. For body-size text on a light ground use blue #000075 or dark_text #1a1a3e, and carry hierarchy with size and weight rather than a lighter colour. On the blue ground both are fine for text.
- Status: accepted, reported 2026-08-16

## LinkedIn visuals

The LinkedIn templates are a designed system of their own. Their pills, rounded
cards, accent bars and number badges stay as described here; the **Never look
like AI** rules are for client work, not for these carousels.

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
- One pair in a hero, top-right, at low opacity. Never a lone triangle.
- Decorative elements are always `pointer-events: none` and `aria-hidden="true"`.
- CTA buttons are pill-shaped, uppercase, with wide letter spacing and semibold weight.
- Use the CSS custom properties and Tailwind config from `assets/templates/` rather than hardcoding values.

These rules describe the plainsight.pro component library. A page or artifact
generated for a client follows Layout and Never look like AI instead: no pills,
no shadows, 8 to 12 px corners at most.

## Presentations

- PowerPoint decks start from the official .potx. Do not rebuild its slide layouts from scratch.
- Claude Slides and HTML decks cannot start from a .potx. They use the slide canvas and splits under Layout, and the deck order under Make it look curated.
- Cream for content slides, primary colour for the title, section dividers and the closing slide.
- Logo on the title and closing slides only, bottom-right, matched to the slide background.
- A triangle pair on the title, every section divider and the closing slide. A content slide may carry a subtle pair in a free corner, never touching text, a chart or a table.
- Every content slide has an action title: one sentence, sentence case, stating the conclusion.
- One idea per slide, one or two sentences per block.
- A team photo from the Photos table on the about-us, team or closing slide.
- No transitions and no build animations.

## Voice

Senior practitioners who respect the reader's time. Knowledge first, in clear human language. We must never sound like AI wrote it, and never sound like every other consultancy.

- **Clear, not clever.** Short sentences. Plain English or plain Dutch. Trade the buzzword for the thing it describes.
- **Concrete, not vague.** Numbers, timeframes, named technologies. '30% faster' beats 'significantly faster'.
- **Confident, not loud.** No caps-shouting, no stacked exclamation marks. The work speaks; we describe it.
- **Expert, not jargon.** For output leaving Plainsight, keep technical language light. Show expertise through concrete examples and honest observations, not through vocabulary.

**Conventions.**

- Action titles: every content slide or chapter title is a full sentence that states the conclusion. Someone who reads only the titles gets the argument.
- Person: 'we' for Plainsight, 'you' for the client. Never 'the client' in a document the client reads.
- No emoji in client work: proposals, offers, decks, documents, reports and dashboards. LinkedIn follows voice.linkedin.

### Never sound like AI wrote it

- No em dashes or en dashes as separators. Use commas, periods, or restructure. A dash in a range (2027–2029, Jan–Feb) is fine.
- No AI-style anecdote openers ('This was my Tuesday morning', 'I'm thrilled to announce').
- No dramatic rule-of-three ('innovation, inspiration, and impact'). Use the natural number of items.
- No numbered lists of obvious advice, no generic conclusions ('The future looks bright'), no signposting.
- If a sentence could appear on any consultancy's feed, rewrite it or cut it.

**Banned words and phrases:** `genuinely`, `straightforward`, `it's worth noting`, `let's dive in`, `in today's landscape`, `leverage`, `game-changer`, `cutting-edge`, `pivotal`, `ecosystem`, `foster`, `elevate`, `moreover`, `furthermore`, `showcase`, `delve`, `key takeaway`, `utilize`, `synergy`, `tapestry`, `navigate (metaphorical)`, `unlock`, `empower`, `seamless`, `robust`, `journey (for a project)`

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
- [ ] Triangles placed from asset files, wireframe, rounded, in asymmetric corner pairs, 60% visible: on the cover or title slide, on chapter openers and on the closing page.
- [ ] Orange used only as accent, once per slide or section.
- [ ] Max 2 font weights; headings Titillium Web bold, uppercase for section headings and labels, sentence case for action titles; body Inter.
- [ ] If a template, layout or text box specifies another font, override it to the typography above: the deck master does this and it is a known defect.
- [ ] Logo from asset files, correct variant for the background.
- [ ] PowerPoint decks start from the official .potx template. Claude Slides and HTML decks follow layout and agency_principles.
- [ ] Photos only from the photos catalogue: real Plainsight people, untinted, never under text.
- [ ] Copy passes the voice test: clear, concrete, confident; no buzzwords, no banned words, no em dashes.
- [ ] Output passes the never_look_like_ai test and the agency_principles final check.
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
PowerPoint master, the rocket motif and the PNG variants. Photography is served
from the brand kit's public site; the Photos table above gives each photo's URL
and alt text.
