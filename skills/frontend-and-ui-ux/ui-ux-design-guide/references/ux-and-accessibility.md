# Usability Heuristics & Accessibility

## Nielsen's 10 usability heuristics

Use these as a review checklist against any interface, regardless of visual style. They're broad rules of thumb, not literal rules — hold the design up against each and see where users are likely to get lost, frustrated, or surprised.

1. **Visibility of system status** — the system always tells the user what's happening, with feedback in a reasonable time (loading indicators, save confirmations, progress bars).
2. **Match between system and the real world** — speak the user's language, use familiar concepts and conventions, follow real-world order (e.g., a checkout flow follows the order a person actually pays: cart → shipping → payment → review).
3. **User control and freedom** — support undo/redo and a clear "emergency exit" for mistaken actions (cancel, back, close) without a forced multi-step process.
4. **Consistency and standards** — don't make users guess whether different words, situations, or actions mean the same thing; follow platform conventions rather than inventing new ones.
5. **Error prevention** — better than a good error message is a design that prevents the problem in the first place (confirmation on destructive actions, constraints that make invalid states hard to reach).
6. **Recognition rather than recall** — minimize memory load by keeping objects, actions, and options visible; don't make users remember information from one part of the interface to use in another.
7. **Flexibility and efficiency of use** — accelerators (shortcuts, saved views, bulk actions) that are invisible to novices but speed up experts, without punishing either group.
8. **Aesthetic and minimalist design** — every extra unit of information competes with the relevant ones; remove or de-emphasize anything not needed most of the time.
9. **Help users recognize, diagnose, and recover from errors** — plain-language error messages that state the problem and suggest a fix, not error codes or blame.
10. **Help and documentation** — ideally the system needs none, but where it's needed, it should be easy to search, focused on the user's task, and not overwhelming.

## WCAG 2.2 — what's actually new (beyond the 2.1 baseline)

WCAG 2.2 is fully backward-compatible with 2.1 — everything you already know still applies. It adds nine new success criteria (six at A/AA, three at AAA) and removes one obsolete 2.1 criterion (4.1.1 Parsing). For a product targeting AA conformance, the six A/AA additions are the ones that actually change what you build:

| Criterion | Level | What it requires |
|---|---|---|
| 2.4.11 Focus Not Obscured (Minimum) | AA | When an element receives keyboard focus, at least part of it must stay visible — not fully hidden behind a sticky header/footer or non-modal dialog |
| 2.5.7 Dragging Movements | AA | Anything operated by dragging must also be operable with a single pointer action, no dragging (e.g. a reorderable list also needs up/down buttons or tap-to-move) |
| 2.5.8 Target Size (Minimum) | AA | Pointer targets ≥ 24×24 CSS px, unless the target is inline in text, has an equivalent larger target elsewhere, or is a required legacy/browser-default control |
| 3.2.6 Consistent Help | A | If a help mechanism (contact link, chatbot, FAQ) appears on multiple pages, it stays in the same relative location and order across them |
| 3.3.7 Redundant Entry | A | Information the user already provided earlier in the same process is auto-populated or offered for re-selection, not re-typed from scratch |
| 3.3.8 Accessible Authentication (Minimum) | AA | Login can't rely purely on a cognitive test (e.g. solve a puzzle, transcribe a CAPTCHA, remember a password with no paste/autofill/password-manager support) unless an alternative exists |

The three AAA additions (Focus Not Obscured Enhanced, Focus Appearance, Accessible Authentication Enhanced) are worth aiming for in accessible-first products (government, healthcare, education) even when the overall target is AA.

## The accessibility floor (2.0/2.1 baseline, still fully in force)

- **Contrast**: normal text ≥ 4.5:1 against its background; large text (≥24px, or ≥19px/14pt bold) and meaningful UI component boundaries/icons ≥ 3:1.
- **Keyboard**: every interactive element reachable and operable by keyboard alone, in a logical tab order, with a visible focus indicator at all times (not just `:focus-visible` suppressed by a reset).
- **Touch targets**: WCAG 2.2 sets 24×24 CSS px as the accessibility floor. Platform conventions ask for more — see `platforms-and-stacks.md` for the iOS (44×44pt) and Material (48×48dp) minimums, which this skill treats as the practical default over the WCAG floor.
- **Color isn't the only signal**: never convey state (error, success, required field, selected) through color alone — pair it with an icon, label, or pattern.
- **Motion**: respect `prefers-reduced-motion`; provide a non-animated or reduced-motion path for anything beyond a subtle transition, and never auto-play motion that can't be paused if it lasts more than 5 seconds.
- **Alt text and labels**: every meaningful image has alt text; every icon-only control has an accessible name (`aria-label` or equivalent) — an icon alone is not a label.
- **Forms**: every input has a visible, programmatically-associated label (not just a placeholder — placeholders disappear on input and often fail contrast).

## Loading, empty, and error states

Design all three for every async view or collection — the happy path alone is an incomplete design:

- **Loading**: prefer skeleton screens or inline progress over a full-screen blocking spinner for anything the user is likely to wait more than ~1 second for; a full-page spinner reads as "frozen" rather than "working."
- **Empty**: give the empty state a reason to exist — explain what will appear here and offer the action that fills it (e.g., "No projects yet — create your first one"), rather than a bare "No data."
- **Error**: state what went wrong in plain language, and — where possible — what to do next (retry action, link to support, corrected input). Avoid raw error codes or stack traces in user-facing surfaces.

## Form validation

- Validate inline, next to the field that has the problem — not only in a single banner at the top of the form.
- Be specific: "Password needs at least 8 characters" beats "Invalid input."
- Validate on blur or submit for most fields; validate live only for things with an obvious immediate signal (password strength, username availability) — validating every keystroke on a normal text field reads as nagging.
- Never rely on red border color alone to mark an error — pair it with an icon and text.
- Preserve entered data on a failed submit; never force the user to re-enter a whole form because one field failed.

## Common anti-patterns to avoid

- **Dark patterns**: confirm-shaming ("No thanks, I don't want to save money"), hidden costs revealed only at the final step, pre-checked opt-ins for marketing/upsells, disguised ads that mimic content. These erode trust and are increasingly regulated — avoid them even if requested, and say so.
- **Mystery meat navigation**: icon-only nav items with no label and no accessible name, forcing users to hover/tap to discover what something does.
- **Fake urgency**: countdown timers or "only 2 left!" messaging not backed by real inventory/time data.
- **Double-barreled confirmation dialogs**: a generic "Are you sure?" with no context on what will actually happen, on every action regardless of severity — reserve confirmation dialogs for genuinely destructive or irreversible actions.
- **Full-page blocking spinners** on repeat visits to already-fetched data — cache and show stale-while-revalidate instead where feasible.
- **Layout shift on load**: reserve space for images, ads, and async content so the page doesn't jump as it loads (this is also a Core Web Vitals concern — Cumulative Layout Shift).
