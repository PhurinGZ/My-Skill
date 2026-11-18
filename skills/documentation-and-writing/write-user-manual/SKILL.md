---
name: write-user-manual
author: PhurinGZ
description: Write end-user / admin manuals for a software system or module (คู่มือการใช้งานระบบ) as Markdown, JSON (per-paragraph i18n keys, th/en), Word/PDF, or HTML. Interviews the user first (format, audience, language, scope), studies the real system (code, existing manuals, screenshots, the user's explanation), then writes task-based steps and audits them before delivery. Make sure to use this skill whenever the user asks to write, draft, improve, translate, or extend a manual, user guide, how-to guide, คู่มือ, วิธีใช้, manual.json, or in-app help for any system, module, or feature — even if they don't say "manual" explicitly.
---

# Write a user manual

A manual's job is to let a reader finish a task with the system, not to describe every feature. Write from the reader's goal, verify every step against the real system, and never invent behavior. A wrong step in a manual is worse than a missing one, because readers trust it.

## Workflow

Follow these phases in order. Do not start writing before phase 1 is answered.

### 1. Interview (always ask, never assume)

Ask these before anything else. If the environment has a tappable-question tool, use it; otherwise ask in one short message. Skip a question only if the user already answered it in this conversation.

1. **Output format** — offer all four, multiple allowed: `.md`, `.json` (one key per paragraph, for i18n), `.docx`/`.pdf`, `.html`. Details per format are in `references/formats.md`.
2. **Audience** — ask every time, even if it seems obvious. Options: general non-technical users, system admins, developers (API/code), mixed. The answer decides vocabulary, depth, and which tasks appear. For "mixed", split into separate sections per role rather than blending them.
3. **Language** — Thai only, English only, or both. Default to Thai wording that a non-specialist can follow; keep UI labels exactly as they appear on screen.
4. **Scope and version** — which module/feature, and which version of the system. Get a real identifier (release number, or git commit hash from `package.json`/`git describe`/the user); if none can be found, ask. Never write "current", "latest" or "development build" as the version, because a reader cannot tell which release the manual matches.
5. **Screenshots** — whether to include screenshot placeholders (with alt text), or none.

### 2. Study the system before writing

Use every source the user gives, in this order of trust:

1. **Code / project** (routes, views, form fields, i18n files, permissions) — the ground truth for what the system does and what labels the user sees.
2. **Existing manual** — ground truth for the house style and for keys/sections that already exist. Reuse its structure; see "Editing an existing manual" below.
3. **Screenshots** — ground truth for what the screen looks like. Read labels from them.
4. **The user's explanation** — ground truth for business intent: why a step exists, real-world examples, terminology.

If the sources conflict, say so and ask which is current; do not silently pick one. The same applies **inside the manual you write**: after drafting, list every fact that is stated in more than one place (who can do something, time limits, lengths, what a button does, how to recover from a mistake) and make sure all places agree. When two places disagree and you cannot settle it from the code or the user, do not publish either as fact: mark **both** places `[ต้องตรวจ]` and put the contradiction at the top of your final message.

**When reading the code still leaves a step unclear** (hidden conditions, unclear business rule, a button whose effect you cannot trace), stop and ask the user to explain that specific point. Ask one focused question at a time. Mark anything still unverified as `[ต้องตรวจ]` in the draft rather than guessing, and list those items at the end.

### 3. Plan

List the tasks the reader wants to do (verbs: "รับซื้อของ", "ปิดบิล", "ตั้งค่าโต๊ะ"), not the menu items. Order them by how a first-time user would meet them: setup → daily tasks → occasional tasks → reports/admin → troubleshooting. For a large manual, show the outline and get a yes before writing everything.

Give every section exactly one content type, because readers in different moments need different things and mixed sections serve none of them well (Diátaxis):

- **Quick start** — one short end-to-end first success for a new user.
- **Task** (how-to) — steps to reach one goal; the bulk of the manual.
- **Reference** — tables the reader looks things up in: field meanings, statuses, permissions per role, error messages and their fixes.
- **Concept** — short explanation of "why/what is it". Keep it out of task steps; link to it instead.

Also plan these supporting parts when the system has enough content to justify them: a **glossary** of the system's own terms, and an **error-message table** built from the validation/error strings found in the code.

### 4. Write

Each task section uses this shape, in this order:

1. **Goal** — one sentence: what the reader will have achieved.
2. **Before you start** — permissions, data that must exist first. Place it before the steps, never inside them. Omit if none.
3. **Steps** — numbered, one action per step, imperative verb first (Thai: start with the verb, e.g. กด, เลือก, กรอก). Name UI elements exactly as shown, in bold (for example: กดปุ่ม **บันทึก**). Put the result in the same step, right after the action, when the reader could be unsure it worked. Keep a procedure to about 7 steps; if it grows longer, split it into sub-tasks or use sub-steps (a, b, c). A procedure with a single action is a bullet, not "1.". If the same procedure appears in several places, write it once and link to it.
4. **Example** — one realistic case with concrete numbers/names, so the reader can check their own result against it.
5. **If something goes wrong** — the 2–4 most likely problems with cause and fix. Take them from the code (validation messages, permission checks) rather than inventing them.
6. **Related tasks** — links or key names of the next likely tasks.

Warnings go **immediately before the step they protect**, because readers jump into the middle of a manual and skip anything placed earlier (ANSI Z535.6 practice, adapted for software). Use them only for actions that lose data, cannot be undone, move money or stock, or affect other users — for example deleting, cancelling or voiding a bill, closing a day, resetting, adjusting points or stock, changing a price list. **Every step like that gets a warning**; check each module for them, because it is easy to warn in one module and forget the next. A warning states: the level, what can go wrong, the consequence, and how to avoid it. Levels: **คำเตือน** (data loss / irreversible / money), **ข้อควรระวัง** (recoverable problem), **หมายเหตุ** (useful but harmless). Use them sparingly: at most one per section and never two in a row, otherwise readers stop noticing them.

Writing rules, and why they matter:

- Active voice and present tense ("ระบบแสดงรายการสินค้า"), because it is shorter and unambiguous, and translates better.
- One idea per sentence; short sentences translate and read more reliably.
- One action per step, because readers follow along with the system open and lose their place in compound steps.
- Plain words; define a technical term once at first use, because most readers are not the people who built the system.
- Say what the reader sees, not what the system does internally.
- Keep step order and screenshot count identical to what the real screen flow does. Put a screenshot placeholder where the reader would otherwise be unsure which screen they are on, not after every step.
- Do not pad. If a feature has no reader task attached, leave it out or give it a single reference line.
- Never state a limit, price, or rule you did not see in the code, a screenshot, or the user's words.
- Use neutral example data (`user@example.com`, "คุณสมชาย", round invented amounts). Never copy real customer or client e-mails, domains, phone numbers or names that you saw in the code or screenshots; a manual gets passed to other people.
- Do not chain several actions inside one step with arrows (`A → B → C`). Make each action its own numbered step. Arrows are fine in a reference table or to show a fixed status flow (e.g. รอทำ → กำลังทำ → รอเสิร์ฟ), and a single menu path (**ตั้งค่า** > **ข้อมูลบริษัท**) counts as one action.
- A task section always has numbered steps. If it has none, it is really a concept or reference section: give it that type, or turn it into steps.
- Use the same word for the same thing everywhere, and match the system's own label; add it to the glossary if it is not obvious. Inconsistent terms make readers think there are two features.
- Accessibility: every screenshot gets alt text that says what it shows (not "image1"); never rely on color alone ("press the red button" → "press **ลบ**, the red button"); link text describes its target; headings follow a logical hierarchy.
- Maintenance: record the system version and the date at the top, and keep paragraph/key names stable, so that when the system changes the manual can be updated in place instead of rewritten.

### 5. Produce the file(s)

Read `references/formats.md` for the format(s) chosen in phase 1 and follow it exactly. When more than one format is chosen, write the content once in the draft and derive the others from it so they cannot drift apart.

### 6. Audit before delivering

First run the mechanical lint on Markdown output and review every finding (they are prompts to check, not proof of a bug; a status flow with arrows or a filter "clear" button can be a legitimate false alarm):

```bash
python scripts/lint_manual_md.py <manual-dir-or-file>
```

It flags: procedures over 7 steps, steps that chain actions with arrows, task sections without numbered steps, destructive steps with no warning in the section, missing or placeholder version, real-looking e-mail domains, and leftover `[ต้องตรวจ]`. Then run through `references/checklist.md`. If the user asks why a rule exists, `references/standards.md` lists the source of each one. For JSON output also run:

```bash
python scripts/check_manual_json.py <path/to/th/manual.json> <path/to/en/manual.json>
```

It reports keys missing from one language, empty values, and leftover `[ต้องตรวจ]` markers. Fix what it reports, then tell the user: what was written, which items are still `[ต้องตรวจ]`, and any assumptions made.

## Editing an existing manual

When the user already has a manual (especially a keyed `.json` or a draft with key tags):

- **Never rename or delete an existing key.** Other code and translations point at it. Change the text only.
- New paragraphs get new keys that follow the file's existing naming pattern.
- Keep step order and screenshot count in line with the page the manual is shown on.
- Improving "clarity" means: split compound steps, add the expected result, add an example, add a troubleshooting entry. It does not mean rewriting the structure.
- Show a short list of what changed (keys edited / keys added) at the end.
