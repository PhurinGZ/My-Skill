---
name: nextjs-security-audit
description: Runs a full-codebase security audit of a Next.js project (App Router or Pages Router) — checks the installed Next.js/React version against known critical CVEs (middleware/proxy auth bypass, RSC deserialization RCE, cache poisoning, SSRF, DoS), then greps the codebase for common misconfigurations (auth logic living only in middleware, secrets leaked via NEXT_PUBLIC_, unvalidated Server Actions, dangerouslySetInnerHTML/XSS, open redirects, SSRF-prone fetches, missing security headers/CSP, insecure cookies, wildcard image remotePatterns, exposed source maps). Produces a severity-ranked report with concrete fixes and file:line references. Trigger for "audit", "security check", "pentest", "review the security of", "harden", or "ตรวจสอบความปลอดภัย" / "เช็ค security" a Next.js/React app, or asking if it's safe/vulnerable/up to date — even for one narrow concern (e.g. "is my middleware auth safe?"), since that's a good entry point to the fuller audit.
---

# Next.js Security Audit

A systematic, whole-repo security audit for Next.js apps (App Router and Pages Router). Two passes: (1) **version/CVE check** against known critical Next.js/React advisories, (2) **static pattern audit** of the actual source for the misconfigurations that cause most real-world Next.js breaches.

This skill is a checklist and grep methodology, not a vulnerability scanner with 100% recall — always tell the user this is a strong first pass, not a substitute for a professional pentest before a real launch, and that CVE data has a knowledge cutoff (see `references/known-cves.md` header) so a live `npm audit` / GitHub Advisory Database check should also be run for anything disclosed after that date.

## Step 0 — Scope and locate the app

1. Find the Next.js project root(s) — look for `next.config.js`/`.ts`/`.mjs` and `package.json` with a `next` dependency. If the user pointed at a specific path, use it; otherwise search the workspace/repo.
2. Note App Router (`app/`) vs Pages Router (`pages/`) vs both — several checks are router-specific.
3. If this is a monorepo, run the audit per Next.js app, not once globally.

## Step 1 — Version and known-CVE check

1. Read the `next` and `react`/`react-dom` versions from `package.json` (and lockfile if present, since `package.json` may have a range).
2. Open `references/known-cves.md` and compare the installed version against each entry's affected range.
3. For anything flagged, also run (if a package manager is available in the sandbox): `npm audit` / `pnpm audit` / `yarn audit` as a supplement — it will catch advisories published after this skill's cutoff that aren't in the reference file.
4. Any match against a **Critical/High** entry goes at the **top** of the final report, above the static-analysis findings, with the CVE ID, affected range, and the exact upgrade target.

Do not skip this step even if the codebase "looks fine" — CVE-2025-66478 / CVE-2025-55182 (React2Shell) and the CVE-2026-44575 family of middleware bypasses affect a stock, unmodified `create-next-app` project with no code changes required to be vulnerable, so version alone determines exposure.

## Step 2 — Static pattern audit

Work through `references/checklist.md` category by category. For each category, run the listed search patterns (`grep -rn`/`rg`) across the app source (exclude `node_modules`, `.next`, test fixtures), inspect real matches in context, and classify each finding as a confirmed issue, a likely false positive, or not applicable to this router type. Don't just report raw grep hits — read enough surrounding code to judge whether it's actually exploitable (e.g. a `dangerouslySetInnerHTML` fed from a sanitizer is not the same finding as one fed from raw user input).

Categories in `references/checklist.md`:
- Middleware/proxy used as the *only* auth boundary
- Server Actions & Route Handlers missing input validation / auth checks
- Secrets and env var exposure (`NEXT_PUBLIC_` misuse, secrets in client bundles)
- XSS (`dangerouslySetInnerHTML`, unsanitized `next/script`, missing/weak CSP)
- SSRF (server-side `fetch`/`axios` calls built from user input)
- Open redirects (`redirect()`, `NextResponse.redirect()` from user input)
- Insecure cookies / token storage (`localStorage` for sessions, missing `httpOnly`/`secure`/`SameSite`)
- `next/image` and `remotePatterns`/`domains` wildcards (SSRF/DoS via image optimizer)
- Missing security headers (CSP, `X-Frame-Options`, `Strict-Transport-Security`, `Referrer-Policy`)
- Source map / debug exposure in production builds
- Dependency hygiene (lockfile committed, no `*` version ranges on `next`/`react`)

## Step 3 — Report

Produce one Markdown report (as a file if the user wants to keep/share it — check the docx/md conventions already in effect — otherwise inline is fine for a quick check). Structure:

1. **Summary** — one line per severity tier, counts only.
2. **Critical/High: version & CVE findings** — from Step 1.
3. **Findings by category** — from Step 2, each with: severity (Critical/High/Medium/Low/Info), file:line, a short explanation of the actual risk (not just "this pattern is bad"), and a concrete fix (code-level, not generic advice).
4. **Not applicable / checked, clean** — brief, so the user knows what was actually checked vs skipped.
5. **Recommended next steps** — upgrade targets, and a pointer to run `npm audit`/Snyk/GitHub Dependabot for continuous coverage since this is a point-in-time check.

Sort findings within each severity by exploitability (unauthenticated/remote first), not by file order. Never invent a finding to pad the report — "clean" categories are a legitimate and useful result.

## Notes on judgment calls

- A `middleware.ts` doing auth checks is not automatically Critical — it's Critical/High only if there's *no* corresponding check in the Route Handler/Server Action/Data Access Layer underneath it (defense-in-depth missing entirely), per the CVE-2025-29927 and CVE-2026-44575 lesson that middleware is a routing layer, not a security boundary.
- `NEXT_PUBLIC_` vars are findings only when they contain something that shouldn't be public (API secrets, internal URLs meant to be private) — a public analytics ID is not a finding.
- Flag `dangerouslySetInnerHTML` and raw `<div dangerouslySetInnerHTML>`-style patterns even when a sanitizer library is present nearby — verify the sanitizer is actually applied to that exact value, not just imported somewhere in the file.
- If the user asks about a live, deployed app rather than source code they can share, this skill can't run without the code — offer to do a lighter external check (response headers, cookie flags, exposed `/_next/` paths) using web tools instead, and say plainly that's a much smaller subset of this audit.
