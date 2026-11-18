# Static Pattern Audit Checklist

For each category: run the search patterns, open real matches in context, and
decide Confirmed / False positive / N/A. Patterns use `rg` (ripgrep) syntax;
substitute `grep -rn` if `rg` isn't available. Always exclude `node_modules`,
`.next`, `dist`, `build`, and test fixtures.

```
EXCLUDE='--glob !node_modules --glob !.next --glob !dist --glob !build'
```

---

## 1. Auth boundary — middleware used as the *only* gate

**Why it matters:** CVE-2025-29927 and CVE-2026-44575/45109 both let attackers
reach a route while completely bypassing `middleware.ts`. If the only auth
check for a protected route lives in middleware, that route has no real
protection on a vulnerable/misconfigured version — and even on a patched
version, defense-in-depth means it shouldn't be the *only* check.

```
rg $EXCLUDE -n "export (async )?function middleware" middleware.ts src/middleware.ts
rg $EXCLUDE -n "getServerSession|auth\(\)|requireAuth|verifySession" app/**/route.ts app/**/actions.ts app/**/page.tsx
```

For every protected path referenced in `middleware.ts`'s matcher, check
whether the corresponding Route Handler / Server Action / Server Component
also independently verifies the session — not just reads a header middleware
set (an attacker who bypasses middleware won't have set that header either,
but relying on "middleware sets a trusted header" is itself fragile — the
underlying check should hit the actual session/DB, per the Data Access Layer
pattern).

**Severity:** Critical if a route handling sensitive data/actions has no
independent check; Medium (defense-in-depth gap) if there is a check but it's
weaker than middleware's.

---

## 2. Server Actions & Route Handlers — missing validation/authz

**Why it matters:** Server Actions are directly callable HTTP endpoints once
deployed — the client-side form/button around them isn't a security boundary.

```
rg $EXCLUDE -n "use server" -A5
rg $EXCLUDE -n "export async function (POST|PUT|PATCH|DELETE)" app/**/route.ts
```

For each match, verify:
- Input is validated against a schema (Zod/Yup/etc.) before use, not just
  TypeScript-typed (types vanish at runtime for untrusted input).
- The action re-checks authorization for the specific resource being
  mutated (e.g. "does this session own this `orderId`") — not just "is
  someone logged in."
- No raw SQL string interpolation of action inputs (check ORM usage too —
  even Prisma/Drizzle can be misused with `$queryRawUnsafe`/raw fragments).

```
rg $EXCLUDE -n "queryRawUnsafe|\\\$executeRawUnsafe|sql\`.*\\\$\{"
```

**Severity:** Critical for unauthenticated mutation/data-access endpoints;
High for missing per-resource authz (IDOR); Medium for missing input
validation where the downstream code happens to be safe anyway.

---

## 3. Secrets & env var exposure

```
rg $EXCLUDE -n "NEXT_PUBLIC_[A-Z_]*(SECRET|KEY|TOKEN|PASSWORD|CREDENTIAL)"
rg $EXCLUDE -n "process\.env\.[A-Z_]+" app/ pages/ components/ --glob "*client*"
rg $EXCLUDE -n "\"use client\"" -l | xargs -I{} rg -n "process\.env" {}
```

Any `NEXT_PUBLIC_` variable is bundled into client JS and world-readable —
flag any that look like API secrets, DB credentials, internal service URLs,
or third-party keys that aren't meant to be public (a public analytics/Stripe
publishable key is fine and not a finding). Also flag any non-`NEXT_PUBLIC_`
env var referenced inside a file marked `"use client"` — that's a build-time
leak into the client bundle even without the prefix.

**Severity:** Critical if a genuine secret (private API key, DB connection
string, signing key) is exposed; Info if it's a legitimately-public value.

---

## 4. XSS

```
rg $EXCLUDE -n "dangerouslySetInnerHTML"
rg $EXCLUDE -n "<Script" -A3 | rg "beforeInteractive"
rg $EXCLUDE -n "eval\(|new Function\("
```

For each `dangerouslySetInnerHTML`, trace the value back to its source — is
it sanitized (DOMPurify or equivalent) immediately before use, or does it
come from user input / CMS content with no sanitization? `beforeInteractive`
scripts that interpolate untrusted input are a known XSS vector
(GHSA-gx5p-jg67-6x7h) — check for template-string interpolation of
user-controlled data into inline script content.

Check for a Content-Security-Policy:
```
rg $EXCLUDE -n "Content-Security-Policy" next.config.* middleware.ts
```
No CSP at all is a Medium finding (defense-in-depth gap) on its own, higher
if combined with any confirmed injection point above. If a CSP nonce
strategy is used, cross-check the installed Next.js version against
GHSA-ffhc-5mcf-pf4q (nonce-related XSS, fixed in 16.2.6).

**Severity:** Critical/High if untrusted input reaches `dangerouslySetInnerHTML`
or an inline script with no sanitization; Medium for missing CSP alone.

---

## 5. SSRF — server-side fetches built from user input

```
rg $EXCLUDE -n "fetch\(.*(req\.|params\.|searchParams\.|body\.)" app/ pages/api/
rg $EXCLUDE -n "axios\.(get|post)\(.*(req\.|params\.|body\.)"
```

Flag any server-side HTTP call (webhook forwarding, "fetch this URL and show
a preview", image/avatar-from-URL features, proxy endpoints) where the
target host/URL is wholly or partially attacker-controlled with no allowlist.
Also check WebSocket upgrade handling against GHSA-c4j6-fc7j-m34r if on an
affected version.

**Severity:** High/Critical if the URL is fully attacker-controlled and the
server can reach internal/private network ranges (cloud metadata endpoints,
internal services); Medium if partially constrained.

---

## 6. Open redirects

```
rg $EXCLUDE -n "redirect\(" app/ | rg -v "redirect\(['\"]/"
rg $EXCLUDE -n "NextResponse\.redirect\("
```

Flag any `redirect()` / `NextResponse.redirect()` whose target is built from
a query parameter, header, or other user input without validating it's a
relative path or an allowlisted host (classic phishing vector — `?next=` /
`?returnUrl=` params).

**Severity:** Medium (High if chained with an OAuth/login flow where the
redirect target affects token delivery).

---

## 7. Cookies & token storage

```
rg $EXCLUDE -n "localStorage\.(setItem|getItem).*(token|session|jwt|auth)" -i
rg $EXCLUDE -n "cookies\(\)\.set\(|set-cookie" -i
```

Session tokens/JWTs in `localStorage` are readable by any injected script
(any XSS becomes full account takeover). Prefer `httpOnly` cookies. For
cookie-setting code found, verify `httpOnly: true`, `secure: true` (in
production), and an explicit `sameSite` (`lax` or `strict` for session
cookies).

**Severity:** High for tokens in `localStorage`/`sessionStorage`; Medium for
cookies missing `httpOnly`/`secure`/`SameSite`.

---

## 8. `next/image` remote patterns

```
rg $EXCLUDE -n "remotePatterns|images:\s*\{" next.config.*
```

A wildcard like `hostname: '**'` (or the older `domains` array set overly
broad) lets the Image Optimization API be used as an open SSRF/DoS proxy —
also relevant to GHSA-h64f-5h5j-jqjh (DoS in Image Optimization API, fixed
16.2.6). Flag any wildcard or overly broad pattern; confirm the installed
version if this is present.

**Severity:** High if wildcarded with no other mitigation; Medium if scoped
but still broader than necessary.

---

## 9. Security headers

```
rg $EXCLUDE -n "headers\(\)\s*\{|async headers" next.config.*
```

Check `next.config.*` (or middleware) for: `Strict-Transport-Security`,
`X-Frame-Options` or `frame-ancestors` in CSP, `X-Content-Type-Options:
nosniff`, `Referrer-Policy`. Absence of all of these is a Medium finding;
absence of frame protection specifically is higher if the app handles
sensitive actions (clickjacking risk).

**Severity:** Medium (Low if only one or two minor headers are missing).

---

## 10. Source maps / debug info in production

```
rg $EXCLUDE -n "productionBrowserSourceMaps" next.config.*
```

If `productionBrowserSourceMaps: true` with no justification, or if
`.map` files are found alongside a production build output, flag it — full
source maps in production make reverse-engineering internal logic and
finding other issues trivial.

**Severity:** Low/Medium depending on what the source reveals (internal API
structure, comments, etc.).

---

## 11. Dependency hygiene

```
test -f package-lock.json -o -f pnpm-lock.yaml -o -f yarn.lock || echo "NO LOCKFILE COMMITTED"
rg -n "\"next\":\s*\"\\*\"|\"react\":\s*\"\\*\"" package.json
```

No committed lockfile, or `*`/unpinned ranges on `next`/`react`, means the
exact deployed version can drift silently — flag as a process/Info finding
that undermines being able to trust any version-based check above.

**Severity:** Info/Low on its own; escalates the confidence of any CVE
finding down since the "installed version" is uncertain.
