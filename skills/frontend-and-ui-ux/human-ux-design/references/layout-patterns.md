# Layout Patterns by Page Archetype

Read the section for the archetype you identified in SKILL.md [2], BEFORE writing code.
Conventional structure = what the user's mental model already expects. Deviate on purpose, never by accident.
Each section ends with an **Evidence** line: what is backed by research/standards vs. what is convention or rule of thumb.

## Contents
1. Scan patterns (F / Z / layer-cake)
2. Responsive behavior & breakpoints
3. Landing / marketing
4. SaaS dashboard & admin
5. E-commerce
6. Content (blog, docs, news)
7. Auth & forms
8. Mobile app
9. Adaptive canonical layouts (feed, list-detail, supporting pane)
10. Thai / long-string layouts
11. Layout anti-patterns

---

## 1. Scan patterns — pick by content density

| Pattern | Use for | How to design for it |
|---|---|---|
| **F** | Text-heavy / dense: articles, search results, docs, tables, data dashboards | Key info top-left and along the first horizontal scan; bold lead-ins; descriptive headings; left-aligned text |
| **Z** | Sparse, visual: landing, product, portfolio, light summary screens | Brand/nav across the top → diagonal through the visual → CTA at the end of the Z (bottom-right). Few elements, ONE primary CTA |
| **Layer-cake** | Pages with clear headings/sections | Users jump heading to heading, so every heading must be informative on its own |

Evidence: F-pattern = NN/g eye-tracking (2006) on text-heavy pages; Z and "layer-cake" are descriptive heuristics. They tell you WHERE the important thing goes — never contort a layout to draw a letter. Western left-to-right assumption; mirror for RTL.

## 2. Responsive behavior

Mobile-first. Breakpoints follow content (break where the layout looks wrong); defaults:

| Class | Width | Typical layout |
|---|---|---|
| Compact | < 600px | 1 column, bottom nav, stacked sections |
| Medium | 600–839px | 1–2 columns, navigation rail or bottom bar |
| Expanded | 840–1199px | 2 panes, sidebar visible |
| Large | ≥ 1200px | 2–3 panes, capped container; extra width = margins, not stretched content |

Rules:
- Layouts must flex BETWEEN breakpoints — never fixed widths per breakpoint (Material guidance).
- Grids: `grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr))`; components living in different containers → container queries.
- Page padding `clamp(16px, 4vw, 48px)`; container `max-width: 1200–1280px; margin-inline: auto`.
- `100dvh`, not `100vh`, for full-height mobile layouts.
- Collapse order on narrow screens: sidebar → drawer/bottom nav; secondary pane → stacked below or behind a tap; table → card list, or horizontal scroll with sticky first column.
- Navigation morphs with width but keeps the same destinations in the same order: bottom bar (phone) → rail (tablet) → permanent sidebar/drawer (large).

Evidence: 600/840 = Material 3 / Android window size classes (compact/medium/expanded); 1200+ tiers also defined by Material. Container max-width and padding values are conventions.

## 3. Landing / marketing (Z + layer-cake)

```
[logo  link link link  ········ (Primary CTA)]   ← nav: 3–6 links, 1 CTA
[ H1: outcome / what it does         ┌─────────┐ ]
[ subhead · (CTA) · secondary link   │ product │ ]   ← hero: show, don't tell
[ 1 line of proof                    └─────────┘ ]
[ logos / stat / rating ]                            ← proof right after hero
[ feature  text | visual ]  [ visual | text ] ...   ← alternate, 1 idea each
[ how it works: ≤4 steps ]   (optional)
[ testimonials: real name + role + result ]
[ pricing: 3 tiers, recommended highlighted ]  /  [ objections / FAQ ]
[ final CTA ]  [ footer ]
```
- Two kinds of page — decide first:
  - **Marketing homepage / long-scroll:** full nav, CTA repeated after proof and after major feature blocks (2–3 instances), final CTA before footer.
  - **Single-goal campaign page:** one conversion goal, minimal or no nav, one CTA repeated (same action).
- Hero: outcome-led headline ("Close more deals"), not feature or slogan ("The future of X"). Primary CTA visible without scrolling, including on mobile; if a one-line proof pushes the CTA below the fold on mobile, drop the proof line.
- Proof: a few specific items beat a long gallery; put a named testimonial near a CTA or decision point.
- Vary section rhythm (full-bleed band / split / centered / grid). Same card grid repeated = AI tell.
- Section vertical padding: 72–128px desktop, 48–72px mobile.

Evidence: section order and single-primary-CTA are consistent across NN/g-derived guidance and CRO sources. Reported "% lift" figures from blogs are NOT reliable — don't quote them. Padding values = convention.

## 4. SaaS dashboard & admin (F for dense, Z for light)

```
┌────────┬───────────────────────────────────────┐
│ logo   │ Page title             (Primary action)│
│ nav    ├───────────────────────────────────────┤
│ nav    │ [KPI][KPI][KPI][KPI]   ← top-left = #1  │
│ nav    │ charts that explain the KPIs            │
│ ...    │ search · filters · view toggle          │
│ user   │ table (detail)                          │
└────────┴───────────────────────────────────────┘
```
- Sidebar: fixed/collapsible, 240–280px (56–72px collapsed). Top-bar for search, user, global actions. Sidebar for >5 sections (scales to dozens with collapsible groups); top nav for ≤5.
- Same page skeleton on every page: title + primary action top-right → filters → content.
- Most important metric top-left; second-most along the top strip. KPI strip: about 4–6 cards max, fewer is better; asymmetric grid (big chart + narrow side column) instead of equal tiles.
- Layout order: summary (KPIs) → explanation (charts) → detail (table). KPI cards drill down on click; never the whole page.
- Density: dense (4px base, 32–36px rows) for daily/ops users; airy for occasional users.
- Tables: sticky header, sortable columns, empty state, pagination/virtualization > ~50 rows, row actions, **bulk-action bar on multi-select** (missing bulk actions is a classic admin failure), inline edit for single fields.
- Command palette (⌘K) once there are more than a handful of resources.
- Chart choice follows the question: compare → bar · trend → line · parts of whole → bar (pie only 2–5 slices) · relationship → scatter · goal at a glance → KPI card. Bar y-axis starts at zero.

Evidence: F-pattern top-left placement, sidebar+topbar+cards shell, KPI→charts→table order = widely repeated practice, source quality mixed. Pixel sizes and KPI count vary by source → treat as defaults.

## 5. E-commerce

- **Listing grid:** locked image aspect ratio; price + one differentiator (rating/badge) visible without a click; quick-add on hover (desktop) / always visible (mobile). Facet filters left on desktop, bottom-sheet on mobile; show active-filter count and one-tap "clear all".
- **Product page:**
  - Gallery left/top, buy box right; desktop buy box stays visible on scroll; mobile sticky bottom add-to-cart bar.
  - **Show thumbnails for additional images, also on mobile** — hiding/truncating extra images makes many users overlook them (Baymard).
  - **Don't put main product sections (description, specs, reviews) in horizontal tabs**; use stacked, scannable sections with an anchor/jump link to reviews near the top (Baymard).
  - Price, stock, and delivery estimate beside the CTA. Show shipping/free-shipping where the buyer decides, not only in a site-wide banner.
  - "Add to cart" primary; "Buy now"/express checkout secondary.
- **Cart/checkout:** full cost breakdown (subtotal, shipping, tax, total) BEFORE the final step; guest checkout; progress indicator; single column on mobile.

Evidence: thumbnails, no horizontal tabs, shipping visibility = Baymard research findings. Sticky add-to-cart = common, widely recommended; reported lift percentages are vendor claims — don't quote.

## 6. Content (blog, docs, news) — F

- One reading column: 60–75 characters (`max-width: 65ch`); never full-bleed body text.
- Docs: 3 columns on desktop — nav left (≈240px) · content center · sticky "on this page" TOC right (≈200px); TOC for > ~1500 words. Collapse to a top dropdown on mobile.
- Real hierarchy: size + weight + spacing, not bold alone. More space above a heading than below it.
- Ending: related / next article, not a dead end.

Evidence: measure (45–75 chars) = long-standing typography consensus; the 3-column docs shell and TOC thresholds = convention, not researched here.

## 7. Auth & forms

- **Single column**, one field per row. Short, logically paired fields (city + postal code, first + last name, card expiry + CVC) may share a row. Form width 360–480px.
- **Labels above fields**, left-aligned. Helper text under the field; error text replaces helper text in place. Never placeholder-only labels (disappears when typing, fails contrast).
- Group related fields visually (spacing/fieldset). Keep it short — ask for less; defer optional fields.
- Long forms → multi-step with progress; keep entered data on error; validate inline, not prematurely.
- Primary button: full-width on mobile; on desktop align with the fields' left edge. Secondary action (cancel/back) is visually lighter.
- Split-screen auth (form + brand visual) only ≥1024px; drop the visual on mobile.

Evidence: single column + top labels + no placeholder-as-label = NN/g, Baymard, and Google eye-tracking-based guidance (top labels need fewer eye fixations). Multi-column can win for long forms with many short fields in some A/B tests → exception, not default.

## 8. Mobile app

- Primary nav: **bottom bar with 3–5 destinations, icon + label**, current item clearly marked. 5+ destinations → drawer / "More". Tablet → navigation rail; large screens → permanent sidebar. Keep destinations and order identical across forms.
- Bar height ≈ 80dp (Material 3) / 49pt + safe area (iOS). Always pad with `env(safe-area-inset-bottom)`.
- Primary actions in the lower two-thirds / thumb zone; sticky primary CTA above the bottom bar or safe-area.
- Touch targets ≥ 44pt (iOS) / 48dp (Android), ≥ 8px between targets.
- Lists: full-bleed rows, 16px side padding; use bottom sheets rather than modals for selection and filters.
- Onboarding: 3–5 screens max, skippable, ask permissions in context.

Evidence: 3–5 destinations, 44/48 targets, bar dimensions = platform guidelines (HIG / Material 3). Thumb-zone placement = widely accepted ergonomic guidance.

## 9. Adaptive canonical layouts (Material 3)

| Layout | Use when | Compact | Expanded |
|---|---|---|---|
| **Feed** | Equivalent items to browse (cards, posts, products) | 1 column | multi-column grid; make 1–2 items larger for hierarchy |
| **List-detail** | Select an item to see its content (mail, settings, orders) | list OR detail (back button) | list + detail side by side, selection highlighted |
| **Supporting pane** | Secondary content that only makes sense next to the main content (tools, comments, info) | below main or in a sheet | main ≈ 2/3 + side pane ≈ 1/3, best in landscape |

Max 3 panes. Test: a list-detail's detail still makes sense alone; a supporting pane doesn't.

Evidence: Material 3 / Android canonical layouts documentation.

## 10. Thai / long-string layouts

- Thai separates phrases, not words, with spaces. Modern browsers do dictionary-based Thai line breaking natively — keep `word-break: normal`; add `overflow-wrap: anywhere` only as a safety net for long unbroken strings (URLs, IDs, numbers). Prefer `text-wrap: pretty` for body paragraphs.
- Line-height: use 1.6–1.8 for Thai body text (tone marks and vowels above/below need room) — a practical rule of thumb, not a standard; verify with your chosen font. Never clip with fixed heights or `overflow:hidden` on single lines.
- Thai labels/buttons are often longer than English: buttons grow (`min-width` + padding, not fixed `width`); avoid truncating key labels; test with the longest real string.
- Every font role (display + body) must include Thai glyphs (e.g. Noto Sans Thai, Sarabun, IBM Plex Sans Thai, Prompt, Kanit); check that the needed weights exist in Thai.
- Justified text in Thai is risky — default to left-aligned.

Evidence: no-word-spaces and shaping behavior = W3C Thai Layout Requirements; line-height value = rule of thumb.

## 11. Layout anti-patterns (AI tells)

- Everything centered; no asymmetry or dominant element.
- The same identical card grid repeated section after section.
- 3 equal feature columns with icon + title + 2 lines as the default feature section.
- Sidebar for ≤ 4 sections; top nav stuffed with > 6 links.
- Dashboard = only a grid of equal KPI cards, no drill-down.
- Full-width stretched body text on desktop.
- Equal spacing everywhere (no grouping by proximity). Rule: gap inside a group ≤ half the gap between groups.
- Fixed pixel widths that break between breakpoints.
- Horizontal tabs hiding core product info; hamburger menu hiding 3–5 primary mobile destinations.
- Placeholder as the only label; two competing primary CTAs in one viewport.
