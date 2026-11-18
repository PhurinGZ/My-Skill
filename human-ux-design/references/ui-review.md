# UI Review — passes, scoring, caps, fix order

Use in REVIEW mode (SKILL.md [R]). Judge the UI against what it is FOR, not against personal taste.

## Contents
1. Inputs & what you can verify
2. Context: page or app screen?
3. Visual passes (look at the render)
4. Scoring — 8 dimensions, weighted by kind
5. Caps (override the arithmetic)
6. Severity
7. Objective vs convention vs taste
8. AI-tell check
9. What to fix first
10. Output format
11. Rounds, calibration, before/after

---

## 1. Inputs & what you can verify
| Input | How to review | Limits |
|---|---|---|
| Screenshot | `view` the image; run the visual passes (§3) | Contrast, sizes, spacing are ESTIMATES — say "approx." |
| Code (HTML/CSS/JSX) | Read it; compute contrast from real color values; read sizes, line-heights, states, ARIA | Can't see the render → say what you couldn't verify |
| Code + a way to render | Render at 375px and 1280px and review the screenshots, not the source | Only if tools exist; otherwise skip silently |
| URL | `web_fetch` returns markup/text, not pixels → review structure/semantics; ask for a screenshot for visual judgment | Never claim to have "seen" the page |

Review the render, not the intention. The author of code reads their own intent into it; pictures show only what is there. When reviewing UI Claude itself just built, re-judge it as a stranger who didn't write it.
Never invent details. Anything not visible/provided goes under "Not verified".

## 2. Context: page or app screen?
Decide first — the two are judged differently.
- **Page** = read and scrolled (landing, marketing, portfolio, event, content). Judged on first-screen clarity, hierarchy, substance, imagery, a point of view.
- **App screen** = worked in (dashboard, POS, admin, forms, lists, settings, ERP views). Judged on task speed, clarity under density, states, data realism, keyboard/touch ergonomics. Quiet borders, small labels, repeated panels/rows are NORMAL here; decoration (gradients, glows, icon-in-tinted-square, rainbow charts, invented vanity numbers) is the problem.
- A marketing page that shows a product UI = page, but the product fragment is judged by app-screen rules.
Also identify: archetype (SKILL.md [2]) · platform · who uses it and the one task · existing brand/design system (outranks this skill's taste defaults) · language (Thai?).

## 3. Visual passes (one at a time, don't blend them)
1. **1 second, then 5.** Glance and look away: what did you see? There should be one answer. Then 5 seconds as a stranger: can you say what this is, who it's for, what to do next? App screens: can you spot the primary action and the current state?
2. **Squint.** Text becomes grey bars; the screen should reduce to 2–3 masses of clearly different size. Many medium masses = nothing leads.
3. **Task path (app screens).** Do the main task: how many taps/clicks, any dead ends, any step that needs reading a paragraph? Frequent actions in reach? Destructive actions guarded?
4. **Swap test (pages).** Replace the name and key nouns with a competitor's. Still valid? Then it's generic. App screens: does it use the domain's own vocabulary and real artifacts (receipt, invoice, form, shelf, ledger), or generic "Items / Data / Dashboard"?
5. **Edges & holes.** Trace the left edge of every text block: 2–3 distinct x-positions = composed; 6 = placed one by one. Left/right margins equal? Any accidental hole (empty region beside a short column), or a half-width section with the other half empty?
6. **Grouping.** Related things close, unrelated far; gap between groups clearly larger than gaps inside a group.
7. **Sameness.** Name each section's layout in one word (split, list, grid, statement, table…). Same word 3 times, or twice in a row = template showing.
8. **Type.** Decisive jump from body to heading? ≤5 sizes? Orphan words, over-75ch paragraphs, centered multi-line paragraphs, Thai clipping?
9. **Color.** Name the proportions: ground / support / accent. Accent in ten places means nothing; accent on the action + one detail means "here". Status not by color alone.
10. **Imagery & content.** Every image has a job; consistent crops/treatment; no grey boxes, stretched photos, fake charts made of bars, lorem or "Item 1". Data realistic (adds up, believable values, real units/currency).
11. **Fullness.** Austere ≠ restrained. If it could be mistaken for an unfinished wireframe (grey text, one small column, dead ground), it's underbuilt. Does each screen deliver what the user came for, at readable size? Removing ornaments must not remove substance.
12. **Phone & collisions.** Is mobile its own composition or a squeezed desktop? Anything overlapping a heading/button, running off-screen, or scrolling sideways by accident?

## 4. Scoring — 8 dimensions, 1–5 each, weighted by kind
Scale: 5 excellent · 4 good · 3 acceptable with issues · 2 weak · 1 broken/harmful.

| # | Dimension | Check (objective items first) | Page wt | App wt |
|---|---|---|---|---|
| 1 | **Layout & structure** | Archetype skeleton (`layout-patterns.md`) · one dominant element per viewport · grouping · consistent grid/spacing scale · no horizontal scroll at 375px · width capped | 15 | 15 |
| 2 | **Visual hierarchy** | #1/#2/#3 clear in 3s · primary/secondary/tertiary actions differ · no 3+ equal-weight elements | 20 | 10 |
| 3 | **Typography** | Body ≥16px (≥14 dense) · line-height ≥1.5 · 45–75ch · scale ≥1.2× · ≤2 families · Thai: Thai font, lh 1.6–1.8, no clipping | 15 | 10 |
| 4 | **Color & contrast** | Text 4.5:1 (large 3:1) · UI/icons 3:1 · tokens not hardcoded · 1–3 hues · status not color-only · dark mode not pure black/white | 10 | 10 |
| 5 | **Components & states** | hover/focus/active/disabled · loading · empty · error (inline, specific) · success · consistent radius/button styles | 5 | 20 |
| 6 | **Imagery, icons & content** | One SVG icon set, no emoji icons · images have jobs · no placeholder/lorem · realistic labels and data · substance present | 15 | 5 |
| 7 | **Accessibility** | Semantics (`button`, `label`, landmarks, heading order) · visible `:focus-visible` · keyboard path · targets ≥44px / 48dp · `aria-label` on icon buttons · reduced-motion · 200% zoom | 10 | 15 |
| 8 | **Responsive & usability** | 375 / 768 / 1280 · nav fits size (bottom bar ≤5 / sidebar) · thumb zone · safe-area · forms single column, labels above · clear next step | 10 | 15 |

Weights sum to 100. **Score = Σ weight × (rating ÷ 5)**, out of 100. N/A dimension → drop it and rescale.

| Score | Verdict |
|---|---|
| 85–100 | **Good** — ship with polish |
| 65–84 | **Needs work** — solid base, fix Majors first |
| 45–64 | **Weak** — structural problems; rework before polishing |
| < 45 | **Poor** — rebuild the affected parts |

## 5. Caps (override the arithmetic)
- Any **Blocker** → can't be Good (cap the score at 84). Two or more Blockers → cap at 64.
- Fails the 5-second test (can't tell what it is / what to do) → hierarchy ≤ 2.
- Primary action not identifiable on first screen → hierarchy ≤ 3.
- Body-text contrast < 3:1 anywhere → color ≤ 2.
- Horizontal overflow at 375px, or controls off-screen → responsive ≤ 2.
- Core action not reachable by keyboard / no focus indication → accessibility ≤ 2.
- Any placeholder (lorem, grey box, "Item 1", "Image here") → imagery/content ≤ 2.
- Missing loading/empty/error state on a data screen → components ≤ 3.
- Two or more mostly-empty screens, or small grey running text → layout ≤ 3.
- Anything covering a heading/button at any scroll position → responsive ≤ 2.
State every cap you applied.

## 6. Severity
- **Blocker** — users can't complete the task or it harms them: unreadable text (<3:1), unreachable controls, no keyboard path for core actions, broken mobile layout, data loss, deceptive UI.
- **Major** — clearly hurts usability/trust: weak hierarchy, missing key states, 3–4.5:1 text, small targets, inconsistent components, wrong nav pattern.
- **Minor** — noticeable, not harmful: off-scale spacing, weak empty-state copy, mixed radius.
- **Polish** — refinement: easing, micro-interactions, fine alignment.

## 7. Objective vs convention vs taste
- **Objective** (measurable): contrast, sizes, line length, missing states, semantics, overflow → findings with numbers.
- **Convention** (research/guideline-backed: top labels, bottom nav 3–5, no horizontal tabs for product info) → findings, state the basis.
- **Taste/house style** (font choice, radius, gradient style, "ban Inter") → NEVER a defect alone. Brand or design system present → follow it; if it forces a device this skill dislikes, keep it and say so. Put under "Suggestions (taste)".
- Don't penalize a deliberate, consistent choice; do flag inconsistency.

## 8. AI-tell check (list only items present)
Emoji icons · random-hue gradient cards · purple→blue gradient hero · equal-weight everything · identical card grid repeated · centered-everything · generic hero slogan · lorem / grey image boxes · missing states · uniform radius everywhere · looping decoration · gradient text as the only "design" · fake KPI numbers. Say "reads as generic" + the specific fix. Caution: removing tells alone can leave a thin page — pass 11 decides whether substance survived.

## 9. What to fix first (later items can't rescue earlier ones)
1. **Purpose** — page: the idea/promise; app: the main task path.
2. **Hierarchy** — one dominant element per screen.
3. **Composition** — edges, spacing, rhythm, holes.
4. **Typography** — scale, line breaks, measure, leading.
5. **Imagery & content** — real, specific, consistent.
6. **Color** — proportions, accent discipline.
7. **States & detail** — hover/focus/loading/empty/error, alignments, mobile refinements.
8. **Motion** — last.
When removing something leaves a gap, don't refill it with an ornament: close the gap, enlarge what remains, or give the space to real content.

## 10. Output format (tight; reply in the user's language — Thai if they write Thai)
```
## ผลตรวจ UI / UI Review
**Verdict:** Needs work · 71/100   **Kind:** page | app screen
**Context:** <archetype · platform · task> · **Reviewed from:** <screenshot/code/…>
**Seen in 1s:** …   **5-second test:** pass/fail — …

### Scores (weights for this kind)
| Dimension | Rating | Wt | One-line reason |
(8 rows)   **Caps applied:** … or none

### What's working (2–3, only if real)
### Findings (by severity)
1. **[Blocker|Major|Minor|Polish] Title** — where · evidence (numbers/what you see) · why it matters · **Fix:** concrete change (CSS/JSX when code exists)
### Top 3 priorities (in fix order, §9)
### Suggestions (taste, optional)
### Not verified
```
Every finding = WHERE + EVIDENCE + FIX, phrased like a designer to a colleague ("the total row sits 40px left of the table edge"), never "could be more polished". Max ~10 findings; group repeats. A review stops at the critique — offer to apply fixes (BUILD mode), don't rewrite code unless asked.

## 11. Rounds, calibration, before/after
- Fixing after review: fix the top 3 → re-check the render → re-score; at most 3 rounds. Stop early when a stranger would notice nothing new.
- Calibrate honestly: 85+ is uncommon; if your first score of work you built is ≥90, score it again as someone who didn't build it. Don't round up. If round 3 is still < 65, say so plainly and list what remains.
- Before/after: re-score the same 8 dimensions, show the delta per dimension, and list findings resolved / new / still open. Interactions that worked before (links, forms, menus) must still work.
