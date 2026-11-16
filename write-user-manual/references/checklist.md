# Audit checklist (run before delivering)

Go through every item. Fix failures; if one cannot be fixed, report it to the user.

## Accuracy
- [ ] Every step, button name, field name and menu path was verified in code, a screenshot, an existing manual, or the user's words. Nothing was guessed.
- [ ] UI labels match the screen exactly (spelling, language, capitalization).
- [ ] Step order matches the real screen flow; screenshot count matches the steps that need one.
- [ ] Limits, rules and numbers in the text appear in the sources.
- [ ] Anything unverified is marked `[ต้องตรวจ]` and listed in the final message.
- [ ] The manual states a real system version (release number or commit), not "current" or "development build".
- [ ] Every fact stated in more than one place (limits, permissions, recovery steps) agrees everywhere; contradictions are marked `[ต้องตรวจ]` in both places and reported.
- [ ] Examples use neutral data; no real client e-mails, domains, phones or names.

## Structure
- [ ] Organized by reader tasks, not by menu items.
- [ ] Each task section has: goal, steps, example, and troubleshooting (before-you-start and related tasks where relevant).
- [ ] One action per step (no `A → B → C` chains inside a step); each step starts with a verb; every task section has numbered steps.
- [ ] Expected result is stated wherever the reader could be unsure a step worked.
- [ ] Each section has one content type (quick start / task / reference / concept); explanations are not buried inside steps.
- [ ] Procedures have about 7 steps or fewer; longer ones are split or use sub-steps; prerequisites sit before the steps.
- [ ] Every delete / cancel / void / close / reset / adjust step, in every module, has a warning placed immediately before the step (level, consequence, how to avoid); no more than one per section.
- [ ] Glossary and error-message table exist if the system has enough terms/messages to need them; error text comes from the code.

## Accessibility
- [ ] Every screenshot has meaningful alt text; nothing depends on color alone; link text is descriptive; heading levels are not skipped.

## Language
- [ ] Wording suits the audience chosen in the interview.
- [ ] Active voice, present tense, one idea per sentence.
- [ ] Technical terms are defined at first use or avoided.
- [ ] Same term used for the same thing throughout.
- [ ] No padding or marketing language.

## Format-specific
- [ ] **JSON:** same key set in every language; no renamed or deleted existing keys; new keys follow the naming pattern; `check_manual_json.py` reports no problems.
- [ ] **Markdown:** `scripts/lint_manual_md.py` run and every finding reviewed.
- [ ] **Markdown / HTML:** anchors and table of contents work; image paths are consistent.
- [ ] **Word / PDF:** rendered and inspected visually; Thai text displays correctly; page breaks do not split a step list awkwardly.

## Final message to the user
State briefly: what was produced and where, which items are `[ต้องตรวจ]`, assumptions made, and (when editing) which keys were changed or added.
