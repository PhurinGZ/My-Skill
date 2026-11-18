# Known Critical/High Next.js & React CVEs

Compiled from public advisories current as of **September 2026**. Vulnerability
disclosure is continuous — always cross-check with `npm audit`, the
[GitHub Advisory Database](https://github.com/advisories?query=next.js), and
https://nextjs.org/blog (search "security") for anything newer than this date.

For each entry: check the installed `next` (and `react`/`react-dom` where noted)
version against the affected range. If it falls inside, this is a Critical/High
finding regardless of how the app is configured — most of these require no
special app code to be exploitable.

---

## CVE-2025-29927 — Middleware Authorization Bypass (`x-middleware-subrequest`)
- **Severity:** Critical (CVSS 9.1)
- **Affected:** 11.1.4–12.3.4, 13.0.0–13.5.8, 14.0.0–14.2.24, 15.0.0–15.2.2
- **Fixed in:** 12.3.5, 13.5.9, 14.2.25, 15.2.3
- **Impact:** Sending a crafted `x-middleware-subrequest` header let an attacker skip middleware entirely, bypassing any authentication/authorization logic that lived only in `middleware.ts`, with no credentials.
- **Lesson for the audit:** middleware must never be the *only* place auth is enforced — see checklist.md's Auth Boundary section. This is the origin of that rule.

## CVE-2025-55182 / CVE-2025-66478 — "React2Shell": RSC Deserialization RCE
- **Severity:** Critical (CVSS 10.0) — pre-authentication remote code execution
- **Affected:** React 19 and any RSC-based framework using the vulnerable `react-server` packages; Next.js 15.x and 16.0.0–16.0.6 (App Router). Also hit specific Next.js 14 canary builds (≥14.3.0-canary.77) — stable 14.x and Pages Router were not affected.
- **Fixed in:** Next.js 15.0.5, 15.1.9, 15.2.6, 15.3.6, 15.4.8, 15.5.7, 16.0.7; React 19.0.1, 19.1.2, 19.2.1
- **Impact:** Attacker-controlled input in the RSC "Flight" protocol (via the `Next-Action` header / Server Function endpoint) could reach a deserialization path leading to arbitrary server-side code execution — a single unauthenticated HTTP request, no session or CSRF token needed. A stock `create-next-app` build was vulnerable out of the box.
- **Note:** CVE-2025-66478 was later merged into CVE-2025-55182 in NVD as the same root cause.

## CVE-2026-44575 / CVE-2026-45109 — Middleware/Proxy Bypass via Segment-Prefetch Routes
- **Severity:** High (CVSS 7.5), CWE-288 (Authentication Bypass by Alternate Path)
- **Affected:** `next` >= 15.2.0 < 15.5.18, >= 16.0.0 < 16.2.6 (the second CVE, GHSA-26hh-7cqf-hhc6, is an incomplete-fix follow-up specifically for `middleware.ts` under Turbopack)
- **Fixed in:** 15.5.18, 16.2.6
- **Impact:** App Router apps that gate access via middleware/proxy checks could be bypassed with specially crafted `.rsc` / segment-prefetch URL variants that resolve to the same page but aren't matched by the middleware's matcher config — reaching protected content with no auth check.
- **Workaround if upgrade isn't possible yet:** enforce authorization in the route/page/Server Action itself, not only in middleware (same lesson as CVE-2025-29927).

## Next.js 16.2.6 bundled security fixes (May 2026 release) — check all if below 16.2.6 / 15.5.18
Next.js 16.2.6 (and the parallel 15.5.18 release) bundled fixes for a cluster of advisories; if the installed version predates it, treat all of these as open:
- **GHSA-8h8q-6873-q5fj** (High) — Denial of Service with Server Components
- **GHSA-267c-6grr-h53f** (High) — Middleware/Proxy bypass via segment-prefetch routes (= CVE-2026-44575, see above)
- **GHSA-26hh-7cqf-hhc6** (High) — Same, incomplete-fix follow-up (= CVE-2026-45109)
- **GHSA-mg66-mrh9-m8jx** (High) — DoS via connection exhaustion in apps using Cache Components
- **GHSA-492v-c6pp-mqqv** (High) — Middleware/Proxy bypass through dynamic route parameter injection
- **GHSA-c4j6-fc7j-m34r** (High) — SSRF in applications using WebSocket upgrades
- **GHSA-36qx-fr4f-26g5** (High) — Middleware/Proxy bypass in Pages Router applications using i18n
- **GHSA-ffhc-5mcf-pf4q** (Moderate) — XSS in App Router applications using CSP nonces
- **GHSA-gx5p-jg67-6x7h** (Moderate) — XSS in `beforeInteractive` scripts with untrusted input
- **GHSA-h64f-5h5j-jqjh** (Moderate) — DoS in the Image Optimization API
- **GHSA-wfc6-r584-vfw7** (Moderate) — Cache poisoning in React Server Component responses
- **GHSA-vfv6-92ff-j949** (Low) — Cache poisoning via collisions in RSC cache-busting
- **GHSA-3g8h-86w9-vwmq** (Low) — Middleware/Proxy redirects can be cache-poisoned

For any of these, the fix is simply: **upgrade to `next@16.2.6`/`15.5.18` or later.** Don't try to hand-verify each one against source — version comparison is sufficient and far more reliable than trying to spot these patterns manually.

## Related infra note: `proxy.ts` rename
Recent Next.js releases (documented alongside the 16.2.6 line) rename/relocate middleware-adjacent config under `proxy.ts` in some setups — if the codebase still only has a `middleware.ts` and the installed version expects `proxy.ts`, flag it as a **configuration/upgrade-migration risk** (protections silently not applied), not a CVE per se. Verify against the current Next.js upgrade guide for the specific version in use before asserting this as a confirmed finding.

---

## How to use this file in the audit

1. Extract `next` and `react`/`react-dom` resolved versions (prefer the lockfile over the `package.json` range).
2. Walk each entry above; mark match/no-match.
3. Every match is Critical or High in the final report — do not downgrade severity because "we don't use that feature," unless you can concretely show the vulnerable code path is unreachable (e.g. Pages-Router-only app for an App-Router-only CVE).
4. Recommend the exact fixed version from the entry, not just "upgrade Next.js."
