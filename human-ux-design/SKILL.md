---
name: human-ux-design
author: PhurinGZ
description: Design and build frontend interfaces with exceptional UX/UI quality that is indistinguishable from human-crafted design, and review or audit existing UIs to judge whether they are good or not. Use this skill whenever the user asks to build, redesign, or improve any frontend UI, including websites, web apps, dashboards, landing pages, components, forms, or any visual interface in React, HTML/CSS, Vue, Svelte, or any other framework. Also use it whenever the user asks to review, critique, audit, rate, score, or check a UI, screenshot, mockup, or page (for example "is this design good", "review my UI", "what's wrong with this layout", "ตรวจ UI", "รีวิวหน้าเว็บ", "UI นี้ดีไหม", "ช่วยดูดีไซน์"). Trigger this skill even for small UI tasks like "make this look better", "design a login page", or "improve the UX of this form" - the goal is always human-quality output that doesn't look AI-generated.
---

Produce frontend UI indistinguishable from a senior product designer, and judge existing UI with the same standard. Adaptive — learns user preferences across sessions.

**MODE ROUTER:** user wants something built/changed → **BUILD** (sections [0]–[10]). User wants an existing UI judged (review, critique, audit, rate, "is this good?", ตรวจ/รีวิว/ดีไหม) → **REVIEW** (section [R] + `references/ui-review.md`). Both → review first, then build the fixes.

---

## [0] MEMORY (BUILD mode · always first, silent)

Key: `human-ux-design:profile` · Schema: `{preferences, dislikes[], projects{}, components[], feedbackLog[]}`

**Ask vs infer:** +3 prefs in memory · +2 project known · +2 code/files present · +1 type obvious · +1 brand named · +1 style given
≥6→silent+1-line note · 3–5→1 question · <3→"Any existing colors/code?" · Never ask on tweaks/known projects/fast iteration

**Priority:** message > project tokens > global prefs > memory
**Learn:** `avoid X`→dislikes · `love this`→lock · `minimal/dense`→density · `like [X]`→designRef · `dark/light`→colorScheme
**Prune:** feedbackLog≤20 · components≤30 · save after every design

---

## [1] DESIGN PROCESS — BUILD mode, mandatory every time

Never skip these steps. They are the difference between AI output and human craft.

### Step 1: Intent
Answer silently: Who uses this? What emotion should it evoke? What ONE detail makes it memorable?
**Subject inventory (client work):** jot 5–8 things specific to THIS client and no competitor — its name and meaning, trade vocabulary, the physical artifacts of its world (receipt, ledger, price tag, form, menu, ticket), its constraints (hours, one counter, offline, Thai/English staff), its place and materials. Take the design idea from one of them; use the domain's real words and artifacts in labels, empty states and sample data instead of generic "Items / Data / Dashboard". Page vs app screen: a page is read and scrolled; an app screen (POS, ERP, dashboard) is worked in — there, quiet borders and repeated rows are normal, and decoration, glows and invented vanity numbers are not.
Pick an archetype and commit: Editorial · Precision · Consumer · Craft · Luxury · Expressive.

### Step 2: Visual language decisions (make all before coding)
- **Color:** What 1–2 hues anchor the palette? What's warm vs cool? What's the accent?
- **Type:** What display font + body font pair? What scale ratio?
- **Space:** Dense (dashboard) or airy (marketing)? What's the base unit?
- **Radius:** Tight (2–4px, precision), medium (8–12px, consumer), soft (16–24px, friendly) — pick one and apply consistently
- **Motion:** Snappy or floaty? What easing personality?

### Step 3: Self-critique before output
Before writing any code, ask: *"If I screenshot this and showed it to a Figma designer — would they cringe?"*
Check: hierarchy clear? States handled? Icons SVG? Images have overlays? Nothing lorem ipsum? Typography intentional?

### Step 4: Self-critique after writing code
Read through output once. Flag and fix:
- Any emoji used as icon → replace with SVG
- Any placeholder that's solid black/gray → replace with gradient using brand colors
- Any 3+ elements at identical visual weight → add hierarchy
- Any missing hover/focus state → add
- Any hardcoded color value → move to CSS variable
- Layout doesn't match the archetype's skeleton, or hits an anti-pattern in `references/layout-patterns.md` §11 → restructure

---

## [2] LAYOUT — pick the archetype first, then the grid

**Step A — identify the archetype, then read `references/layout-patterns.md` (that archetype's section) BEFORE coding.**

| Archetype | Skeleton | Scan |
|---|---|---|
| Landing / marketing | nav → hero (outcome + one primary CTA + visual) → proof → alternating features → pricing/FAQ → final CTA → footer (campaign page: single goal, minimal nav) | Z / layer-cake |
| SaaS dashboard / admin | left sidebar (>5 sections) → page header (title + primary action right) → filters → table/cards/charts | F (tables) |
| E-commerce | facet filters + locked-ratio grid · product page: gallery with thumbnails + sticky buy box, stacked sections (no horizontal tabs) | grid |
| Content / docs / blog | one 65ch column · sticky TOC · related content at end | F |
| Auth / forms | single column 360–480px · labels above · one primary action | top-down |
| Mobile app | bottom nav 3–5 · thumb-zone actions · sticky CTA | feed / list-detail |
| Master-detail (mail, settings, orders) | list + detail (expanded) / list OR detail (compact) | list-detail |

**Step B — universal rules**
- **Grid:** 8px base (4px for dense UIs). Spacing scale 4·8·12·16·24·32·48·64·96. Container `max-width:1200–1280px`, side padding `clamp(16px,4vw,48px)`.
- **Hierarchy:** ONE dominant element per viewport. Prefer asymmetric splits (7/5, 8/4) over 6/6. Group by proximity: gap inside a group ≤ ½ the gap between groups.
- **Responsive:** mobile-first; defaults 600 / 840 / 1200px; layouts flex between breakpoints (`repeat(auto-fit, minmax(min(100%,260px),1fr))`, container queries). Wide screens add margin, not stretched content.
- **Mobile:** `clamp()` type, ≥44px touch targets, safe-area insets (`env(safe-area-inset-bottom)`), `100dvh` not `100vh`.
- **Thai/long strings:** line-height 1.6–1.8, buttons grow with `min-width` (no fixed `width`), browsers break Thai natively (keep `word-break:normal`; `overflow-wrap:anywhere` only for long unbroken strings), no clipped single-line containers, Thai-capable font for every role.
- **Vary section rhythm** (full-bleed band / split / centered / grid) — never the same card grid section after section.

Layout anti-patterns are listed at the end of the reference file — check them in Step 4 self-critique.

---

## [3] TYPE

Never Inter/Roboto/Arial/system-ui as primary. Use character fonts: Fraunces · Syne · Instrument Serif · Cabinet Grotesk · Satoshi · Unbounded · DM Serif · Playfair Display. Always pair display+body.

Rules: Headings lh 1.2–1.3, ls −0.02em, `text-wrap:balance`. Body lh 1.6, max-width 65ch. Labels ls +0.05em. Scale 1.25×. Clamp all text: `font-size:clamp(min,vw,max)`.

---

## [4] COLOR SYSTEM

Always output token block first — enables consistency across components:
```
--color-bg · --color-surface · --color-surface-raised
--color-border · --color-border-strong
--color-text · --color-text-muted · --color-text-subtle
--color-accent · --color-accent-hover · --color-accent-text
--color-danger · --color-success · --color-warning
```
HSL only. No pure #000/#fff. 2–3 hues. WCAG AA (4.5:1 body, 3:1 large).

**Dark mode:** bg ~#0f0f0f (never pure black) · surface slightly lighter · text ~#e8e8e6 warm · accent desaturated · elevation = lightness difference, not box-shadow.

**Gradient placeholder colors:** derive from brand accent, not random. A teal card and a purple card in the same grid with no relationship = AI tell.

---

## [5] ICONS — SVG only, always

Emoji as icons = the #1 AI tell. No exceptions.
- Library: Lucide · Phosphor · Heroicons · Tabler — ONE per project, never mix outline+filled
- Sizes: 16px inline · 20px buttons · 24px standalone — stroke-width: 1.5 or 2px, consistent
- Always `currentColor`. Decorative: `aria-hidden="true"`. Meaningful: `aria-label` on parent.

**Replace immediately:** ⭐→SVG star (fill toggle) · 👁→SVG eye · 📖→SVG book · ♡→SVG heart · 🔥→SVG flame or trend-line path · →→SVG arrow · ≡→SVG menu lines

---

## [6] IMAGE & MEDIA

**Hero/banner:** Never solid-color or solid-black overlay. Always cinematic gradient derived from image or brand:
```css
/* Multi-stop overlay that feels like depth, not a gray blanket */
background: linear-gradient(
  to top,
  hsl(var(--scene-hue) 20% 6% / 0.95) 0%,
  hsl(var(--scene-hue) 15% 10% / 0.6) 40%,
  hsl(var(--scene-hue) 10% 15% / 0.1) 100%
);
```
The hue should relate to the content's dominant color — a night scene uses cool hue, a fantasy scene uses warm amber.

**Book/content cards:**
- `aspect-ratio: 2/3` locked always
- Gradient placeholder: derive hue from genre or accent — never random, never solid gray
- Title: `-webkit-line-clamp: 2` always
- Badge: `position:absolute; top:8px; right:8px` — pill with semi-transparent bg, SVG icon + label
- Info below: title (medium weight) → author (muted, smaller) → stats (smallest, muted) — three distinct levels

**Skeleton loading:** same dimensions as final content, shimmer animation, never spinner for content areas.

---

## [7] COMPONENT HIERARCHY

AI treats everything equal weight. Hierarchy is how humans read design quality.

**Buttons:** Primary (filled accent) · Secondary (ghost/outline, less prominent) · Tertiary (text). Never same weight in same row. Metadata stats beside a CTA button = smaller + muted, no competing weight.

**Navigation:**
- Top tabs: active = bottom border indicator (2–3px, accent color) or very subtle bg shift. NOT heavy pill.
- Bottom nav (mobile): active = filled icon + colored label + top indicator line. Inactive = stroke + muted. Safe-area padding required.
- Category scroll: horizontal scroll, no scrollbar, fade-out right edge (`mask-image: linear-gradient(to right, black 80%, transparent 100%)`), all pills same height.

**Tags/pills:** Subtle bg (6–10% opacity), no heavy border, scale to match surrounding text, consistent horizontal padding.

**Stats row:** Separate with spacing only — never borders between inline stats. Value (larger, normal weight) over label (smaller, muted). Use `gap` not dividers.

---

## [8] STATES — where AI design consistently fails

Required for every interactive component:
- **Hover/Focus/Active:** All. Focus-visible outline: `2px solid var(--color-accent); outline-offset: 2px`
- **Loading:** Skeleton (same aspect ratio as content), shimmer. Button: replace label with spinner, keep width.
- **Empty:** Illustration or icon + prompt + action CTA. Never blank white/black.
- **Error:** Inline, specific ("Email already in use"), actionable. Not just red border.
- **Success:** Confirm then auto-dismiss (2–3s). Checkmark animation.
- **Disabled:** Reduced opacity + `cursor:not-allowed`. Keep in tab order if the reason matters.

---

## [9] ANIMATION

Purpose > decoration. `prefers-reduced-motion` always respected.
Timing: hover <150ms · micro-interaction 150–250ms · transition 250–400ms · entry 300–500ms.
Easing: `cubic-bezier(0.16,1,0.3,1)` spring · `ease-out` for entries · never `linear`.
Stagger lists: 30–60ms/item.

Specific: btn press `scale(0.97)` · card hover `translateY(-3px)` + shadow · skeleton shimmer · success checkmark draw · error shake · focus ring grow.

---

## [10] A11Y

`<button>` not `<div onClick>`. Logical heading order. Landmark regions. Every input has `<label>`. Icon-only buttons: `aria-label`. ARIA where semantic HTML insufficient: `aria-expanded` `aria-live="polite"` `role="alert"` `aria-current`. Escape closes overlays. Logical Tab order.

---

## [R] REVIEW MODE — judge an existing UI

Read `references/ui-review.md` first. Skip BUILD steps 1–4 and the memory ask/infer logic. Do not write code unless asked.

1. **Page or app screen?** They're judged differently (a page is read and scrolled; an app screen — POS, ERP, dashboard, form — is worked in). Then archetype, platform, the one task, any brand/design system (it outranks this skill's taste defaults), language.
2. **Look at the render, not the intention.** Screenshot → `view` it; code → read it and compute real contrast/sizes; URL → markup only (ask for a screenshot). Re-judge your own output as a stranger. List gaps under *Not verified*; never claim to have seen what you haven't.
3. **Run the 12 visual passes** one at a time: 1s/5s · squint · task path · swap test · edges & holes · grouping · sameness · type · color proportions · imagery & content · fullness (austere ≠ restrained) · phone & collisions.
4. **Score 8 dimensions 1–5, weighted by kind** (page vs app weights in the reference) → score out of 100 → Good ≥85 · Needs work 65–84 · Weak 45–64 · Poor <45. **Apply the caps** and state them.
5. **Findings by severity** (Blocker / Major / Minor / Polish), each WHERE + EVIDENCE + FIX, phrased like a designer to a colleague. Max ~10, group repeats.
6. **Objective, convention, taste stay separate.** Taste rules (font bans, radius, gradients) are never defects alone → *Suggestions (taste)*. Flag inconsistency, not deliberate style.
7. **Top 3 priorities in fix order:** purpose → hierarchy → composition → type → imagery/content → color → states/detail → motion. Don't refill removed ornaments with new ornaments.
8. **Output** with the template in the reference, in the user's language. Be honest: praise only what's real, don't round scores up, don't soften Blockers. End by offering to apply fixes (BUILD mode, max 3 fix-and-recheck rounds).

---

## NEVER

emoji as icons · random gradient colors in card grids · solid black/gray image placeholder · image without depth overlay · gray blanket overlay on hero (use hue-matched gradient) · heavy nav pill active state · equal-weight buttons in same row · borders where spacing works · Inter/Roboto as primary · uniform border-radius · equal-weight content grids · "Learn More →" or "ดูทั้งหมด →" with no visual weight · gradient-text as substitute for design · looping decoration · lorem ipsum · missing states · purple→blue gradient heroes · mixing icon styles · full-width stretched body text · identical card-grid repeated across sections · sidebar for ≤4 sections · fixed-width buttons/containers that break between breakpoints
