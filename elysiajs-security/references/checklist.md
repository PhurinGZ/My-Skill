# ElysiaJS Security Checklist

Go through each category that applies. Each item lists what to look for, why
it matters, and an Elysia-idiomatic fix.

## 1. Authentication

- **Secrets in code / weak secrets.** JWT secret, session secret hardcoded or
  short/guessable.
  ```ts
  // ❌ Vulnerable
  .use(jwt({ name: 'jwt', secret: 'secret123' }))

  // ✅ Fixed
  .use(jwt({ name: 'jwt', secret: process.env.JWT_SECRET! }))
  // and: fail fast if process.env.JWT_SECRET is missing/short at boot
  ```
- **No expiry / no algorithm pinning on JWT.** Tokens that never expire, or
  verification that doesn't pin the algorithm (alg confusion attacks).
  ```ts
  // ❌ sign without exp
  const token = await jwt.sign({ userId: user.id })

  // ✅ always set exp, and verify (not just decode) on every protected route
  const token = await jwt.sign({ userId: user.id, exp: Math.floor(Date.now()/1000) + 60 * 60 })
  ```
- **`derive`/`resolve` trusts client-supplied identity instead of verifying it.**
  Look for code that reads a user id straight from headers/body instead of
  from a verified token/session.
  ```ts
  // ❌ Vulnerable — trusts an unsigned header
  .derive(({ headers }) => ({ userId: headers['x-user-id'] }))

  // ✅ Fixed — identity comes from a verified JWT
  .derive(async ({ jwt, headers, status }) => {
    const token = headers.authorization?.replace(/^Bearer /, '')
    const payload = token && await jwt.verify(token)
    if (!payload) return status(401)
    return { userId: payload.sub }
  })
  ```
- **Auth check placed in the wrong lifecycle hook**, or missing entirely on a
  route/group that should require it. `beforeHandle`/guard is the right place
  to reject unauthenticated requests before the handler runs; a bare
  `derive` that just sets `userId: undefined` and lets the handler run is a
  common miss.
- **Password handling:** plaintext storage, weak hashing (MD5/SHA1/unsalted),
  or timing-unsafe comparison. Should use bcrypt/argon2 and constant-time
  compare (library-provided compare functions already do this).
- **No rate limiting / lockout on login or token-refresh endpoints**, enabling
  credential stuffing or brute force. See Rate Limiting section.

## 2. Authorization (access control)

- **Missing ownership checks (IDOR).** Route validates that a resource ID
  exists but not that it belongs to the requesting user.
  ```ts
  // ❌ Vulnerable — any authenticated user can read any order
  .get('/orders/:id', ({ params }) => db.getOrder(params.id))

  // ✅ Fixed
  .get('/orders/:id', ({ params, userId, status }) => {
    const order = db.getOrder(params.id)
    if (!order || order.userId !== userId) return status(404)
    return order
  })
  ```
- **Role/permission checks done ad hoc per-route** instead of via a shared
  `macro`/`guard`, causing routes to be added later without the check. Prefer
  a reusable macro (`isAuth`, `requireRole`) applied via `.guard()` on route
  groups so new routes can't accidentally skip it.
- **Mass assignment.** Handler spreads the entire validated body into a DB
  update, letting a client set fields it shouldn't (e.g. `role`, `isAdmin`,
  `balance`).
  ```ts
  // ❌ Vulnerable
  .patch('/users/:id', ({ params, body }) => db.update(params.id, body))

  // ✅ Fixed — schema only allows editable fields, and still whitelist explicitly
  .patch('/users/:id', ({ params, body }) => db.update(params.id, {
    name: body.name,
    email: body.email
  }), {
    body: t.Object({ name: t.String(), email: t.String() }) // no `role` field accepted
  })
  ```

## 3. Input validation

- **Missing or partial schemas.** Any route accepting `body`, `params`,
  `query`, or `headers` without a `t.Object(...)` schema (or Zod/Valibot
  equivalent) is unvalidated — check every route, not just the "important"
  ones.
- **Overly loose schemas:** `t.Any()`, `t.Unknown()`, or optional-everything
  objects that don't actually constrain shape/type/length.
- **No bounds on strings/numbers/arrays** that get used in loops, DB queries,
  or allocations (potential DoS via huge payloads). Use `t.String({ maxLength })`,
  `t.Array(..., { maxItems })`, `t.Number({ minimum, maximum })`.
- **Raw SQL string interpolation** with request data anywhere near the
  handler (even if an ORM is present elsewhere) — check for `db.query(`...`${body.x}`...`)`
  style code. Should use parameterized queries / the ORM's query builder.
- **File upload validation missing:** no MIME-type allowlist, no size cap, no
  filename sanitization (path traversal via `../` in a client-supplied name).
  ```ts
  // ✅ Fixed
  .post('/upload', ({ body: { file } }) => saveFile(file), {
    body: t.Object({
      file: t.File({ type: ['image/png', 'image/jpeg'], maxSize: '5m' })
    })
  })
  ```

## 4. CORS

- **`origin: true` or `origin: '*'` in `@elysiajs/cors`** combined with
  `credentials: true` — this combination lets any website make authenticated
  cross-origin requests using the user's cookies.
  ```ts
  // ❌ Vulnerable
  .use(cors({ origin: true, credentials: true }))

  // ✅ Fixed — explicit allowlist
  .use(cors({
    origin: ['https://app.example.com'],
    credentials: true
  }))
  ```
- Wildcard origin is fine only when `credentials` is false and the API is
  truly public/unauthenticated.

## 5. Cookies & sessions

- Session/auth cookies missing `httpOnly`, `secure`, or an appropriate
  `sameSite` setting.
  ```ts
  // ✅ Fixed
  cookie.session.set({
    value: sessionId,
    httpOnly: true,
    secure: true,
    sameSite: 'strict',
    maxAge: 60 * 60
  })
  ```
- No `secure` flag will still work over plain HTTP in dev — flag it as a
  production requirement, not a hard fail, if the code clearly branches on
  `NODE_ENV`.
- Sessions with no expiry/rotation, or session IDs that are predictable
  (sequential, timestamp-based) rather than cryptographically random.

## 6. Rate limiting & abuse

- No `onRequest` hook or rate-limit plugin on public/auth-sensitive routes
  (login, signup, password reset, token refresh, search, anything hitting a
  paid downstream API).
  ```ts
  // ✅ Minimal example using onRequest
  .onRequest(({ ip, set }) => {
    if (isRateLimited(ip)) { set.status = 429; return 'Too Many Requests' }
  })
  ```
- No request body size limit at the server level, allowing large-payload DoS.

## 7. Error handling & information disclosure

- **Raw error/stack traces returned to the client**, especially DB errors
  that can leak schema/query details.
  ```ts
  // ❌ Vulnerable
  .onError(({ error }) => ({ message: error.message, stack: error.stack }))

  // ✅ Fixed — generic message to client, full detail only in server logs
  .onError(({ error, code }) => {
    logger.error(error)
    if (code === 'VALIDATION') return { message: 'Invalid request' }
    return { message: 'Internal server error' }
  })
  ```
- Verbose 404 vs 403 behavior that confirms resource existence to
  unauthorized users (prefer 404 over 403 for other users' private resources
  to avoid enumeration, when that matches the product's threat model).
- Sensitive data (passwords, tokens, full card numbers, internal IDs meant to
  stay internal) present in logs or included in response payloads that don't
  need them.

## 8. WebSockets

- No authentication on `ws` open — anyone can connect and consume the
  connection/actions.
  ```ts
  // ✅ Fixed — verify token during upgrade
  .ws('/chat', {
    beforeHandle: async ({ query, jwt, status }) => {
      const payload = await jwt.verify(query.token)
      if (!payload) return status(401)
    },
    message(ws, message) { /* ... */ }
  })
  ```
- No per-message validation schema (`body` on `.ws`), no rate limiting on
  message frequency, and no re-authorization when a message triggers a
  privileged action (relying only on the initial handshake check).

## 9. Dependencies & config

- Outdated `elysia` core or plugin versions with known CVEs — check
  `package.json` versions against current releases if the user wants this
  checked.
- Secrets (`JWT_SECRET`, DB URLs, API keys) committed in `.env` files tracked
  by git, or hardcoded as string literals anywhere in source.
- Debug/dev tooling (e.g. verbose Swagger/OpenAPI exposing internal-only
  routes, GraphQL introspection) left enabled in a production build.
- Missing common security headers (e.g. no `@elysiajs/helmet`-style headers
  plugin) — lower severity, worth a mention if nothing else is set at all.

## 10. Encapsulation pitfalls (Elysia-specific)

- Relying on state/derive from a plugin instance without understanding
  Elysia's encapsulation: a `.derive()`/`.state()` defined inside a plugin is
  NOT visible outside that plugin unless explicitly exported with `.as('plugin')`
  or similar — code that *assumes* a security-relevant field (like `userId`)
  is present because "the plugin sets it" can silently receive `undefined` in
  a sibling instance. Always verify with a null/undefined check right before
  using an identity/role field pulled from `derive`.
