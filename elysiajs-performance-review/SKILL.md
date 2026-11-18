---
name: elysiajs-performance-review
description: Audit ElysiaJS (Bun TypeScript backend framework) code specifically for PERFORMANCE issues — not general code review. Use this whenever the user asks to check, review, audit, or optimize the performance/speed of an Elysia server, route, plugin, or service; asks "why is my Elysia app slow"; asks about AOT vs dynamic mode, JIT compilation, precompile, startup time, throughput, or benchmark results; or pastes Elysia code and asks for a performance pass. Always trigger this before giving performance advice on Elysia code, even if the user only mentions "Elysia" + "slow/fast/optimize/benchmark" without using the word "performance."
---

# ElysiaJS Performance Review

A focused checklist for auditing ElysiaJS code for **performance only** (not style, security, or general best practice — use the general `elysiajs` skill for that if available). Elysia's speed comes from Ahead-of-Time (AOT) compilation, static code analysis, and TypeBox schema compilation; most performance bugs come from code patterns that silently disable or bypass these optimizations.

Always consult [elysiajs.com/llms.txt](https://elysiajs.com/llms.txt) for the latest API details if something here seems out of date.

## How to run this review

1. Read through the user's Elysia code (or ask for it if not provided).
2. Walk the checklist below **in order** — each item includes what to look for and how to flag it.
3. Report findings as a short table or list: **Issue → Why it hurts performance → Fix**. Don't rewrite the whole file unless asked; show the specific diff/snippet for each finding.
4. If nothing in a section applies, skip it silently — don't pad the report with "no issues found" for every category.
5. If the user wants to *measure* rather than just *read* performance, point them to `@elysiajs/server-timing` (see Section 7) or a load-testing tool (`autocannon`, `bombardier`) rather than guessing.

---

## 1. Inline handlers (AOT-breaking pattern — check this first)

Elysia's compiler statically analyzes the **handler function passed directly to the route** to generate optimized code and infer types. Extracting handlers into named functions/classes breaks this.

❌ Flag:
```ts
const getUser = (ctx) => Service.find(ctx.params.id)
app.get('/user/:id', getUser)
```

✅ Correct:
```ts
app.get('/user/:id', ({ params: { id } }) => Service.find(id))
```

The fix is always the same: keep the function passed to `.get/.post/...` **inline**, and delegate actual logic to a plain function/service called from inside that inline wrapper.

## 2. Method chaining broken

```ts
// ❌ loses type inference AND can affect Elysia's internal optimization tracking
const app = new Elysia()
app.state('build', 1)
app.get('/', (c) => c.store.build)

// ✅
new Elysia()
  .state('build', 1)
  .get('/', ({ store }) => store.build)
```
Flag any place where the return value of an Elysia method isn't chained onto the next call.

## 3. Plugin re-execution / missing deduplication

A plugin without a `name` re-runs its setup **every time it's `.use()`d**, including in every module that imports it. For plugins used across many modules (auth, db connection, logging), this multiplies work at startup and can duplicate decorators/state.

❌ Flag:
```ts
export const auth = new Elysia().decorate('Auth', Auth) // no name → reruns every .use()
```

✅ Fix:
```ts
export const auth = new Elysia({ name: 'Auth.Service' }).decorate('Auth', Auth) // singleton across instances
```

## 4. Unnecessary global-scope lifecycle hooks

`{ as: 'global' }` (or top-level `.onRequest`/`.onBeforeHandle` on the root instance) runs on **every route in the app**, including ones that don't need it. Heavy logic here (DB calls, crypto, big JSON parsing) taxes every single request regardless of route.

- Flag any `onRequest`/`onBeforeHandle`/`onTransform`/`onAfterHandle` marked `global` or declared on the root app that does non-trivial work.
- Prefer `local` (default) or `scoped`, and only elevate to `global` for genuinely cheap, universal work (CORS headers, request ID stamping).
- Suggest `guard()` or a scoped plugin instead of a global hook when the logic only applies to a subset of routes.

## 5. Heavy work in the wrong "kind" of service

- **Non-request-dependent logic** (pure functions, computation, formatting) that's implemented as a stateful class gets allocated an instance per use. Flag classes with no instance state — recommend `abstract class` + `static` methods to skip allocation:
  ```ts
  // ❌ allocates an instance for pure logic
  class Calc { fibo(n: number) { ... } }

  // ✅ no allocation
  abstract class Calc { static fibo(n: number) { ... } }
  ```
- **Request-dependent logic** (needs cookies/headers/auth) implemented as a bare class taking `Context` loses type integrity and re-derives context shape per call — recommend modeling it as an Elysia instance/macro instead (see Section 3).

## 6. Schema / validation overhead

- **Zod / Valibot / ArkType in hot paths**: Standard Schema libraries are not AOT-compiled the way TypeBox (`t`) is — TypeBox validation is compiled ahead of time and is dramatically faster. Flag heavy use of `z.object(...)` etc. on high-traffic routes and suggest `t.Object(...)` (TypeBox) where throughput matters. It's fine to keep Zod for low-traffic/internal routes if the team prefers its ergonomics — flag as a tradeoff, not an error.
- **Duplicate inline schemas**: the same `t.Object({...})` shape typed out repeatedly across routes doesn't get cached/named — recommend `.model({...})` + string reference (`body: 'auth.Sign'`) so the schema is registered once and reused, which also speeds up TypeScript inference.
- **Missing `response` schema on hot routes**: without a `response` schema, Elysia can't optimize/validate the output shape ahead of time. Not always necessary, but worth flagging for high-throughput endpoints.
- **Unnecessary `t.Any()` / permissive schemas**: wide-open schemas skip the fast-path validation Elysia can otherwise compile — flag and suggest tightening.

## 7. Startup vs per-request tradeoffs (AOT / precompile / dynamic mode)

Ask what runtime/deployment target the app uses before flagging these — the "right" answer depends on it.

| Setting | Effect | When to flag |
|---|---|---|
| `aot: false` (dynamic mode) | Uses JIT instead of AOT; faster startup, slower steady-state throughput; some features (e.g. `trace`) unavailable | Flag if set on a long-running server (Bun/Node/Docker) where steady-state throughput matters more than boot time — dynamic mode should really only be used because the runtime **requires** it (e.g. Cloudflare Workers, which forces it on by default) |
| `precompile: true` | Moves JIT compilation to startup instead of first-request; slower boot, zero first-request latency spike | Suggest enabling for latency-sensitive services (e.g. behind strict p99 SLOs) where a cold first hit per route is unacceptable; not needed for most apps since first-request JIT overhead is normally <0.005ms/route |
| No settings changed | Elysia already defaults to AOT + on-demand JIT, which is right for most apps | Don't flag — this is the sane default |

Recommend `@elysiajs/server-timing` to actually measure where time goes (compile vs handler vs validation) instead of guessing.

## 8. Route-level red flags

- **Routes ordered to fight the router**: Elysia already prioritizes static > dynamic > wildcard internally, so don't suggest manual reordering for that reason — but do flag overlapping wildcard routes shadowing more specific ones.
- **Synchronous CPU-heavy work directly in a handler** (recursive algorithms, big sync JSON transforms, sync crypto) blocks the event loop on Bun/Node the same as any JS server — flag and suggest offloading (worker, streaming, or async chunking) regardless of framework.
- **Returning large payloads without streaming** where a generator/stream (`function* () { yield ... }`) would let the client start consuming earlier.
- **File responses not using `file()`** — Elysia's built-in `file()` helper is optimized for static/local file responses; hand-rolled `fs.readFile` + manual headers loses those optimizations.

## 9. Reporting the findings

Structure output like this (only include rows that actually apply):

| # | Finding | Impact | Fix |
|---|---|---|---|
| 1 | Handler extracted to named function on `/user/:id` | Breaks AOT static analysis | Inline the handler, keep logic in a plain function |
| 2 | `AuthService` plugin has no `name` | Re-executes setup on every `.use()` | Add `{ name: 'Auth.Service' }` |

End with a one-line summary of whether the app is already following Elysia's performance defaults well, or has systemic issues (e.g. "mostly fine, one AOT-breaking pattern" vs "several patterns fighting the framework's optimizations").
