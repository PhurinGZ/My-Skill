---
name: debug-and-test
author: PhurinGZ
description: >
  A skill for systematically debugging code, analyzing errors, and writing test cases.
  Use this skill whenever the user: shares code that is broken or not working as expected,
  pastes an error message, stack trace, or log output, asks why something is failing or
  crashing, wants help writing unit or integration tests, describes a bug in plain language,
  or shares a project with multiple files and asks for help finding the issue.
  Works with all programming languages, with strong focus on JavaScript, TypeScript, and Python.
  Trigger even if the user just says "it doesn't work", "I'm getting an error", "help me test this",
  or pastes code without much explanation — assume they want full debug + fix + tests.
---

# Debug & Test Skill

Help the user find bugs, understand errors, and write tests — systematically and clearly.

---

## Step 1: Understand the Input

The user may provide any combination of:
- **Buggy code** (single file or multiple files)
- **Error message / stack trace / log**
- **Natural language description** of the problem
- **Expected vs actual behavior**

If critical information is missing (e.g., no error and no code), ask one focused question.
Otherwise, proceed immediately — don't ask multiple clarifying questions upfront.

---

## Step 2: Classify the Bug

Before diving in, classify the bug type — it determines the debugging approach:

| Type | Signal | Strategy |
|------|--------|----------|
| **Crash / Exception** | Error message + stack trace | Read error → trace stack → root cause |
| **Wrong output** | No crash, bad result | Binary search + logging |
| **Intermittent** | Works sometimes | Race condition or state mutation |
| **Works locally, fails in prod** | Environment-specific | Config/env bug — check vars, secrets, migrations |
| **Performance** | Too slow, high memory | Profiling + N+1 check |

For deep error classification → load `references/error-taxonomy.md` (has decision tree + root cause map).
For complex/intermittent bugs → load `references/debugging-strategies.md` (8 proven strategies).
For framework-specific bugs (FastAPI, Django, Next.js, Express, Prisma) → load `references/frameworks.md`.

---

## Step 3: Analyze the Root Cause

Work through the problem systematically:

1. **Read the error message carefully** — identify the error type, line number, and file
2. **Trace the stack** — follow the call chain from where it crashed back to the root cause
3. **Identify the root cause** — not just the symptom, but *why* it happened
4. **Check common patterns** for the language/framework (see Language Notes and reference files)

**Commit to a diagnosis** — don't say "it might be X". Form a hypothesis, state it clearly, then verify it.

---

## Step 4: Output Format

Always structure your response with these sections (use emoji headers for clarity):

### 🔍 สาเหตุของปัญหา (Root Cause)
Explain clearly in 2–4 sentences what went wrong and why.
- Be specific: mention variable names, line numbers, function names
- Explain the *why*, not just the *what*

### ✅ วิธีแก้ไข (Fix)
- Show the corrected code (full function or relevant block, not just a diff)
- If there are multiple issues, fix them all
- Add a brief comment in the code if the fix needs explanation

### 🧪 Test Cases
Write tests that:
- Cover the bug that was just fixed (regression test)
- Cover the happy path (normal expected behavior)
- Cover edge cases (null, empty, boundary values, etc.)

Match the testing framework to the language:
- **Python** → `pytest` (preferred) or `unittest`
- **JavaScript/TypeScript** → `Jest` or `Vitest`
- **Other** → use idiomatic testing for that language, or plain assert statements

Format:
```language
# or // Test file example
def test_<function_name>_<scenario>():
    ...
```

### 💡 คำแนะนำเพิ่มเติม (Optional)
Only include if there's a meaningful improvement to suggest beyond the fix — e.g., a better pattern, a common pitfall to avoid, or a useful library. Keep it brief.

---

## Language Notes

For in-depth bug patterns, error message decoder tables, and framework-specific testing syntax, read the relevant reference file:

- **`references/language-patterns.md`** — Python, JavaScript, TypeScript, React, multi-file debugging patterns
- **`references/testing-frameworks.md`** — pytest, Jest, Vitest, Go testing syntax and coverage targets

Quick summary (load reference files for details):

### Python
- Common bugs: mutable default arguments, `None` not checked, off-by-one, wrong indentation scope
- Watch for: `AttributeError`, `TypeError`, `KeyError`, `IndexError`
- Test with: `pytest` — use `assert` statements, fixtures for setup

### JavaScript / TypeScript
- Common bugs: `undefined` vs `null`, async/await not awaited, `this` binding issues, type coercion
- Watch for: `TypeError: cannot read properties of undefined`, unhandled promise rejections
- TS-specific: type mismatches, missing `?.` optional chaining, wrong generic types
- Test with: `Jest` or `Vitest` — use `describe/it/expect` blocks

### General (any language)
- Always check: off-by-one errors, null/nil/None handling, wrong data types, scope issues
- For multi-file projects: trace imports/exports and check if the right module is being used

---

## Handling Multi-File Projects

If the user shares multiple files:
1. Identify which files are relevant to the error
2. Trace how data flows between files
3. Look for mismatches at module boundaries (wrong exports, mismatched function signatures)
4. Show the fix in context of the correct file

See `references/language-patterns.md` → "General Multi-File Debugging" for a full checklist.

---

## Bundled Resources

### References (load as needed)
- `references/error-taxonomy.md` — error classification tree, root cause map for all major error types, HTTP status codes
- `references/debugging-strategies.md` — 8 systematic strategies (binary search, delta debugging, hypothesis-driven, MRE, etc.)
- `references/frameworks.md` — FastAPI, Django, Next.js, Express, Prisma bug patterns + anti-patterns in tests
- `references/language-patterns.md` — Python, JavaScript, TypeScript, React, multi-file debugging patterns
- `references/testing-frameworks.md` — pytest, Jest, Vitest, Go syntax and coverage targets

### Assets & Eval
- `assets/debug-cheatsheet.html` — visual cheatsheet of common bugs and test templates by language
- `eval-viewer/evals.json` — 8 test cases for evaluating skill quality
- `agents/grader.md` — grading rubric for evaluating debugging responses
- `agents/comparator.md` — blind A/B comparison instructions
- `agents/analyzer.md` — analyzing why one response beat another
- `scripts/` — skill packaging and eval loop scripts

---

## Tone & Style

- Be direct and specific — name the exact variable, line, or function that's wrong
- Don't be vague ("there might be an issue with...") — commit to the diagnosis
- Use Thai if the user writes in Thai, English if they write in English, or mix if they do
- Keep explanations concise but complete — no padding
