# Where the rules come from

Use this file to explain or defend a rule when the user asks why. Sources were checked on 2026-11-16. The full text of ISO/IEC/IEEE standards is paywalled; the points below come from the public scope descriptions and published summaries, not from the full standard text, so do not quote clause numbers from here.

| Rule in this skill | Source |
|---|---|
| Plan from the user's tasks and information needs; accuracy, consistency, minimalism, accessibility; information types (concept, instruction, reference, troubleshooting, error messages) and glossaries | ISO/IEC/IEEE 26514:2022 (design and development of information for users) |
| Instructions, safety information and their placement follow the principles of user-instruction standards | IEC/IEEE 82079-1 (preparation of instructions for use) |
| Safety messages: signal word, hazard, consequence, how to avoid; placed immediately before the hazardous step | ANSI Z535.6 (product safety information in manuals) |
| One content type per section: tutorial / how-to / reference / explanation, do not mix | Diátaxis (diataxis.fr) |
| Numbered steps, one action per step, imperative verbs, result after the action in the same step, prerequisites before steps, sub-steps, link instead of repeating a procedure | Google developer documentation style guide (Procedures); Microsoft Writing Style Guide (procedures checklist); GitHub Docs style guide |
| About 7 steps or fewer per procedure; a single step is a bullet | Microsoft Writing Style Guide; Adobe Experience League style guide |
| UI element names in bold, exactly as on screen | Google developer documentation style guide (UI elements) |
| Active voice, present tense, short sentences | Google and GitHub style guides |
| Task-based structure, scannable, plain language, expected result, troubleshooting, keep versions in sync | Common user-manual guidance (Mintlify, Ferndesk, Haiku and similar practitioner guides) |

Thai-specific note: these guides are written for English. Their principles (one action per step, bold UI labels, active voice) carry over, but surface rules such as "omit the word 'button'" or "sentence-case headings" do not apply to Thai, so keep natural Thai phrasing such as "กดปุ่ม **บันทึก**".

## Not covered by sources
The in-app keyed JSON format (stable per-paragraph keys, `th`/`en` files, `[ต้องตรวจ]` markers, the checker script) is this skill's own convention for i18n workflows, not an external standard.
