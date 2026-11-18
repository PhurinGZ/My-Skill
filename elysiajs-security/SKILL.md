---
name: elysiajs-security
description: Audit ElysiaJS (Bun/TypeScript backend framework) code for security vulnerabilities. Use this skill whenever the user asks to review, audit, check, or harden the security of an Elysia/ElysiaJS server or API — including authentication (JWT/session/macros/guards), authorization, input validation, CORS, cookies, rate limiting, WebSocket auth, error handling/info leakage, and file uploads. Trigger this even if the user just pastes Elysia route code and asks "is this safe?", "ตรวจสอบความปลอดภัย", "audit security", "review this for vulnerabilities", or asks to harden a server before deploying to production.
---

# ElysiaJS Security Audit Skill

A focused checklist-driven skill for reviewing ElysiaJS backend code (or a whole
project) for security weaknesses, and suggesting concrete Elysia-idiomatic fixes.

This skill is for **defensive review only**: finding and fixing weaknesses in
code the user owns or is authorized to assess. Do not use it to help attack or
find weaknesses in systems the user doesn't control.

## Workflow

1. **Locate the surface to review.** If the user gives a repo/folder, look for:
   - Entry file (`src/index.ts`, `app.ts`) and all `new Elysia()` chains
   - Route definitions (`.get`, `.post`, `.guard`, `.group`)
   - Auth logic (`.macro`, `.derive`, `.resolve`, `.beforeHandle`, JWT/session/cookie plugins)
   - `package.json` for security-relevant plugins/deps (`@elysiajs/jwt`, `@elysiajs/cors`,
     `@elysiajs/cookie`, `@elysiajs/bearer`, rate-limit packages, ORM packages)
   - `.env` / config for secrets handling
2. **Walk through `references/checklist.md`** category by category against the
   actual code — don't just recite the checklist, check each item against
   what's really there and cite the file/line.
3. **Report findings** grouped by severity (Critical / High / Medium / Low),
   each with: what's wrong, why it matters, and a concrete Elysia code fix.
4. **Don't invent findings.** If a category doesn't apply (e.g. no WebSocket
   code exists), skip it silently rather than padding the report.
5. If asked to "fix" rather than just "check", apply the fixes directly to the
   files (using the read/edit tools available) instead of only describing them.

Load `references/checklist.md` for the full category-by-category checklist with
vulnerable/fixed code pairs. Load `references/owasp-api-mapping.md` only if the
user wants findings mapped to OWASP API Security Top 10 for a formal report.

## Output format

For a code review, prefer this structure:

```
## Summary
[1-3 sentences: overall posture, count of findings by severity]

## Findings

### [SEVERITY] Short title
- **Where:** file/route
- **Issue:** what's wrong
- **Risk:** what an attacker could do
- **Fix:**
  ```ts
  // corrected code
  ```

## Not checked / out of scope
[anything you couldn't verify, e.g. no access to infra config]
```

Keep it concrete and grounded in the actual code shown — avoid generic security
essays. If the user only pasted a snippet, scope findings to that snippet and
note what else would be worth checking (e.g. "also review how JWT_SECRET is
stored").
