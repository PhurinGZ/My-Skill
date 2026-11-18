# Layout Patterns by Product Type

Each pattern below is the expected/conventional structure — the one a user's mental model is already trained on. Deviating is fine when the brief calls for it, but it should be a deliberate choice, not an accident of not knowing the convention.

## Landing page

Structure, top to bottom:
1. **Nav** — logo, 3–6 links max, one clear primary CTA button (visually distinct from nav links).
2. **Hero** — one sentence of value proposition (not a paragraph), one supporting line, one primary + optionally one secondary CTA, and a visual (product screenshot, illustration, or short video) that shows rather than tells what the product does.
3. **Social proof** — logos, review counts, or a stat, placed early; this is a trust signal, not decoration.
4. **Feature sections** — alternate text/visual sides section to section to avoid monotony; one idea per section, not a wall of features.
5. **How it works** (optional) — 3–4 numbered steps if the product needs explaining.
6. **Testimonials/case studies** (optional) — real quotes with names/roles/companies, not generic praise.
7. **Pricing** (if applicable) — 3 tiers is the sweet spot (fewer feels limited, more causes decision paralysis); highlight the recommended tier visually.
8. **Final CTA** — repeat the primary action once more before the footer; don't make users scroll back up.
9. **Footer** — sitemap, legal, social, secondary links.

Common failure: burying the actual value proposition under a generic hero headline ("The future of X") that doesn't say what the product does.

## SaaS dashboard / admin panel

- **Persistent left sidebar nav** (collapsible) is the default for anything with >5 top-level sections; a top nav bar works for ≤5 sections.
- **Page structure**: page title + primary action top-right, then filters/search, then the main data view (table, cards, or charts), consistently across pages.
- **Density**: default to data-dense for internal/ops tools (the user is a repeat, trained user); default to more generous spacing for tools aimed at occasional/non-technical users.
- **Tables** need: sortable columns where useful, a visible empty state, pagination or virtualization past ~50 rows, and row-level actions that don't require a separate page for simple edits.
- **Global search / command palette** (⌘K pattern) is now a baseline expectation for any tool with more than a handful of resources.
- Common failure: a dashboard that's just a grid of KPI cards with no drill-down — treat KPI cards as an entry point to detail, not the whole feature.

## E-commerce

- **Product grid**: consistent aspect ratio across product images, price and key differentiator (rating, badge) visible without a click, wishlist/quick-add affordance on hover (desktop) or always-visible (mobile).
- **Product detail page**: image gallery left/top, price + CTA persistently visible (sticky on scroll on mobile), reviews and detailed specs below the fold — but linked from an anchor near the top.
- **Cart & checkout**: show cost breakdown (subtotal, shipping, tax, total) before the final step, never introduce new costs only at payment; guest checkout as an option, not a forced account creation.
- **Filters**: faceted filters on the left (desktop) or a filter sheet (mobile), with the active filter count visible and a one-tap "clear all."
- Common failure: hiding shipping cost until the last checkout step — a major cause of cart abandonment.

## Mobile onboarding

- **3–5 screens max** for a walkthrough; every screen after that loses a meaningful fraction of users.
- Ask for permissions (location, notifications, camera) **in context**, right before the feature that needs them — not all at once at first launch.
- Progressive disclosure: collect only the minimum to get the user to their first "aha moment"; defer profile completion, preferences, etc. to later, optional steps.
- Always include a visible skip option unless a step is legally or functionally required.
- Common failure: a generic feature-tour carousel that explains the app instead of letting the user experience it.

## Admin / data-heavy tool

- Favor **tables and dense lists** over cards; cards waste space when the primary need is scanning many rows.
- **Bulk actions**: multi-select with a persistent action bar, not a per-row-only action model, once past a handful of items.
- **Inline edit** for small field-level changes; a full modal/page only for multi-field edits.
- Keyboard shortcuts and a command palette pay off disproportionately for tools used daily by the same person.

## Content site (blog, docs, news)

- **Single, clear reading column** (~60–75 characters per line) for body text; resist full-bleed body text on wide viewports.
- **Table of contents** for anything over ~1500 words, sticky on desktop.
- Real typographic hierarchy (not just bold text) to separate headings, subheadings, and body.
- Related content / next-article suggestions at the end, not just a "back to home" dead end.

## Chart-type selection for data-heavy UI

Start from the question being answered, not from what "looks good":

| Question | Chart |
|---|---|
| How do categories compare? | Bar / column chart (horizontal bar if labels are long) |
| How does a value change over time? | Line or area chart |
| How do parts make up a whole? | Bar chart if precision matters; pie/donut only for 2–5 categories where one is clearly dominant — readability drops fast past that many slices |
| Is there a relationship between two numeric variables? | Scatter plot; add a third variable via bubble size if needed |
| How is a value distributed? | Histogram or box plot |
| How does a total break down and change across a sequence of steps? | Waterfall chart |
| How does data vary across two categorical dimensions? | Heatmap |
| How does a metric compare against a goal at a glance? | Single-value KPI card, not a full chart |

General rules: bar/column charts are the safe default for category comparisons, line charts for trends over time; keep the y-axis starting at zero for bar charts so height differences aren't visually distorted; avoid 3D effects, which distort perception without adding information; and don't cram more series into one chart than a viewer can hold distinct colors for at a glance (in practice, 5–7 is a reasonable ceiling before splitting into small multiples).
