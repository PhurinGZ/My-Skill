---
name: fastapi-performance
description: Diagnose and fix FastAPI performance problems — slow endpoints, low requests-per-second, high latency under load, event-loop stalls, or "why is my API slow in production" questions. Use this whenever the user asks to optimize, speed up, profile, scale, or tune a FastAPI app or service, mentions throughput/RPS/latency/benchmarks for FastAPI, is deciding between async def and def, is configuring Uvicorn/Gunicorn workers, is picking a response/serialization strategy, or reports symptoms like "fine locally but slow under load" — even if they don't say the word "performance". Also covers Thai phrasing like "fastapi ช้า", "ปรับ performance fastapi", "optimize fastapi ให้หน่อย". Grounded in the official FastAPI/Starlette docs rather than assumed knowledge, since a lot of popular blog advice on this topic (ORJSONResponse, 2×cores+1 workers, etc.) is outdated.
---

# FastAPI Performance Optimization

FastAPI's own benchmarks are already fast — most real-world slowness comes from how the app is *used*, not from the framework itself. This skill is a diagnose-first checklist: find where the time is actually going before changing anything, because the fixes for "event loop is blocked," "database is the bottleneck," and "only using 1 of 8 CPU cores" are completely different, and applying the wrong one wastes effort without moving the needle.

## How to use this skill

1. **Ask what "slow" means concretely** if it isn't already clear: high latency on a single request, low throughput (RPS) under concurrent load, or fine-locally-but-degrades-under-load. These point in different directions (see the table below).
2. **Read the code before prescribing fixes.** Grep for the smells below rather than applying tips speculatively — the point of this skill is targeted fixes, not a checklist to blindly apply.
3. **Fix in this order of expected impact**: (1) blocking calls inside `async def` — this alone can cause 10-100x regressions and silently stalls *every* concurrent request, not just the slow one; (2) database/N+1 issues; (3) worker/process count; (4) everything else (middleware, serialization, dependency graph). Framework-level micro-optimizations rarely matter if #1 or #2 is wrong.
4. If the user wants to *measure* rather than guess, point them to the "Measure, don't guess" section before/after changes.

## Symptom → likely cause → where to look

| Symptom | Likely cause | Section |
|---|---|---|
| Works fine with 1 user, falls over with concurrent load | Blocking call inside `async def` stalling the event loop | §1 |
| High latency, but CPU usage looks low | Waiting on DB/HTTP calls synchronously, or pool exhaustion | §1, §4 |
| Only using a fraction of available CPU cores | Single Uvicorn process, no worker replication | §6 |
| Slow only on endpoints returning large payloads | Serialization overhead, no pagination/streaming | §2, §7 |
| Latency grows the more middleware/features you add | `BaseHTTPMiddleware` overhead stacking up | §5 |
| DB connection errors under load ("too many connections" / timeouts) | Pool misconfigured relative to worker count | §4 |
| List endpoints get slower as data grows | N+1 queries | §4 |
| CPU-heavy request (image processing, ML inference, PDF generation) blocks other requests | CPU-bound work running on the event loop or thread pool instead of a process pool / task queue | §7 |

---

## 1. Async correctness — the single biggest lever

FastAPI runs `async def` path operations and dependencies directly on the event loop. It runs plain `def` ones in an external thread pool (default cap: 40 threads) so they don't block the loop. This is the most consequential decision in the whole app: get it wrong and *one* slow request can stall every other concurrent request, even ones on completely unrelated endpoints — because they all share the same event loop.

**The rule:**
- If you call something with a library that requires `await` (async DB driver, `httpx.AsyncClient`, etc.), the enclosing function must be `async def`.
- If you call a blocking/sync library (`requests`, `time.sleep`, a sync DB driver, blocking file I/O, sync boto3, etc.), either keep the function as plain `def` (FastAPI offloads it to the thread pool automatically) or explicitly `await asyncio.to_thread(blocking_call, ...)` inside an `async def`.
- Never call a blocking function directly inside `async def` without offloading it. This is the #1 cause of "fine in dev, falls over under load."
- The same rule applies to **dependencies**, not just path operations — a blocking `def` dependency runs in the thread pool; a blocking call left inside an `async def` dependency blocks the loop just as badly as in the endpoint itself.
- If you genuinely don't know whether a call blocks, default to plain `def` — FastAPI will thread-pool it safely. Guessing wrong toward `async def` is the expensive mistake; guessing wrong toward `def` only costs thread-pool overhead.

```python
# BAD — blocks the whole event loop for every concurrent request
@app.get("/rates")
async def get_rates():
    resp = requests.get("https://api.example.com/rates")  # sync call inside async def
    return resp.json()

# GOOD — either drop async...
@app.get("/rates")
def get_rates():
    resp = requests.get("https://api.example.com/rates")  # runs in thread pool
    return resp.json()

# ...or use an async-native client
@app.get("/rates")
async def get_rates():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.example.com/rates")
        return resp.json()
```

For genuinely CPU-bound sync work (hashing, image resizing, parsing large files) inside a `def` function, be aware it still competes for the same shared thread pool — a burst of CPU-heavy requests can starve I/O-bound ones. See §7 for offloading that properly.

## 2. Response serialization

**Current best practice (check this — a lot of older tutorials get it wrong):** `ORJSONResponse` and `UJSONResponse` are now deprecated in FastAPI. Since Pydantic v2 serializes to JSON using the same Rust core that `orjson` uses internally, declaring a `response_model` or a return type annotation and letting FastAPI serialize it directly is now *faster* than manually wrapping the response in `ORJSONResponse` — and it's free, no extra dependency.

```python
# Best: annotate the return type / response_model and let FastAPI+Pydantic v2 handle it
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int) -> Item:
    return await get_item(item_id)
```

Other serialization notes:
- Avoid calling `jsonable_encoder()` yourself and then also returning through a `response_model` — that's double work. Let one mechanism own serialization.
- `response_model_exclude_unset=True` / `exclude_none=True` reduce payload size for sparse objects, which matters more for network time than CPU time on large lists.
- For genuinely huge payloads (bulk exports, large lists), prefer pagination or `StreamingResponse` over building one giant response object in memory.

## 3. Dependency injection

- `Depends(...)` caches a dependency's result **per request only** (`use_cache=True` is the default) — it prevents the same dependency from re-running multiple times within one request's dependency graph, not across requests. Don't expect it to behave like a global cache.
- For something that should only run once at process startup (loading a config file, an ML model, a compiled regex set), do it in the `lifespan` context or at module import time — not as a per-request dependency, and not with `functools.lru_cache` if you're running multiple worker processes (Gunicorn/Uvicorn workers each get their own memory, so `lru_cache` state doesn't share across them; use Redis or similar if you need cross-process caching).
- Keep dependency graphs shallow (roughly 1-3 levels). Deep chains of sub-dependencies are rarely the actual bottleneck (each hop costs microseconds), but they do make it harder to spot where a blocking call is hiding — flatten them when debugging performance, not just for the sake of it.
- A dependency that yields (`def get_db(): ... yield session ...`) is the standard pattern for setup/teardown (DB sessions, request-scoped clients) — this is correct and not a performance concern by itself; the concern is what happens *inside* it (see §4).

## 4. Database & I/O

This is usually the actual bottleneck, more often than FastAPI itself.

- **Use an async driver end to end.** `asyncpg` (Postgres), `asyncmy`/`aiomysql` (MySQL), `motor` (Mongo) — not their sync counterparts inside `async def` code. Mixing a sync driver into async code reintroduces the exact blocking problem from §1.
- **Size the connection pool relative to worker count**, not in isolation. Every Uvicorn/Gunicorn worker process gets its own engine and its own pool, so:
  `total_connections ≈ workers × (pool_size + max_overflow)` — keep this comfortably under the database's `max_connections`. A common mistake is setting a generous `pool_size` per worker and then running out of DB connections once you scale workers up.
- **`pool_pre_ping=True`** avoids errors from stale connections (e.g. after a DB restart or a cloud provider's idle timeout); **`pool_recycle`** (e.g. 1800s) proactively recycles connections before the DB kills them itself.

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine(
    DATABASE_URL,               # e.g. postgresql+asyncpg://...
    pool_size=5,                # start small, scale up based on measured load
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=1800,
)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

- **N+1 queries** are the classic "fast with test data, slow in production" trap: a list endpoint that lazy-loads a relationship per row issues one query per row. Use eager loading (`selectinload`, `joinedload` in SQLAlchemy 2.0) for relationships you know you'll access.
- Always close/release sessions properly (the `yield`-dependency pattern above handles this) — leaked sessions quietly exhaust the pool over time and show up as mysterious timeouts under sustained load, not immediately.

## 5. Middleware

`BaseHTTPMiddleware` (the common `class Foo(BaseHTTPMiddleware)` / `dispatch()` pattern) has measurable overhead — it wraps the request/response and, notably, breaks the ability to run cleanup code after a client disconnects, on top of the raw performance cost. Real-world measurements put pure-ASGI middleware at roughly 20-40% faster than an equivalent `BaseHTTPMiddleware` stack under load, and the gap compounds with each additional middleware layer.

- For simple, single-purpose middleware, the `@app.middleware("http")` decorator form is usually enough and lighter than a full `BaseHTTPMiddleware` subclass.
- For hot-path, high-throughput middleware (auth checks, logging on every request), write it as a plain ASGI callable (`async def __call__(self, scope, receive, send)`) if profiling shows middleware overhead actually matters for your traffic.
- This is a second-order optimization — reach for it once §1 (blocking calls) and §4 (database) are already clean; don't rewrite a working middleware stack pre-emptively without evidence it's the bottleneck.
- Keep the stack itself minimal and ordered deliberately — every middleware layer runs on every request regardless of route.

## 6. Concurrency & deployment

- Install `uvicorn[standard]` (not bare `uvicorn`) — it pulls in `uvloop` and `httptools`, which meaningfully improve throughput under concurrent load over the pure-Python fallback. This is easy to miss and free once fixed.
- **A single Uvicorn process only uses one CPU core.** To use the rest of the machine, run multiple worker processes:
  - `fastapi run main.py --workers 4`, or
  - Gunicorn as the process manager with Uvicorn's worker class: `gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker`
  - Guideline: start with **one worker per available CPU core**, then measure. The classic "`(2 × cores) + 1`" rule is for *synchronous* WSGI workers (Flask/Django with blocking workers) — it doesn't directly apply to async Uvicorn workers, which each already handle many concurrent connections via the event loop. Treat it as a starting point to benchmark from, not a fixed formula.
- Never run with `--reload` (or `fastapi dev`) in production — it's a development convenience with real overhead and is explicitly documented as dev-only.
- In Docker/Kubernetes, the common pattern is **one process per container**, scaling out via replicas instead of in-container workers — this gives the orchestrator (not Gunicorn) control over restarts, health checks, and horizontal scaling. Multi-worker-per-container is still valid for simpler VM-style deployments; pick based on how you're already scaling infra.

## 7. CPU-bound and heavy work

- The thread pool that handles plain `def` functions is meant for I/O-bound blocking calls, not CPU-bound work — CPU-bound code still fights the GIL there and can starve other requests. For genuinely CPU-heavy work (image/video processing, large PDF generation, ML inference), offload to a `ProcessPoolExecutor` (real parallelism, separate GIL) or, better, a dedicated worker.
- `BackgroundTasks` (FastAPI's built-in) is for small, fire-and-forget work after the response is sent (e.g. sending a notification email) — it still runs in the same process, so it's not a substitute for offloading heavy or long-running work.
- For heavy or long-running jobs, use a real task queue (Celery, arq, Dramatiq, etc.) so the API process stays responsive and the job survives a restart/deploy. This is a bigger architectural decision — flag it rather than trying to make `BackgroundTasks` do a task queue's job.
- For large responses (bulk exports, big lists), prefer pagination or `StreamingResponse` over materializing everything in memory at once — this helps both latency and memory footprint.

## 8. Measure, don't guess

Before and after any change, confirm it actually moved the needle rather than assuming from the checklist above:

- **Load testing**: `hey`, `wrk`, or `locust` against a realistic endpoint and payload — watch RPS *and* p95/p99 latency, not just averages, since averages hide the requests that are actually stalling.
- **Profiling a running process**: `py-spy` (sampling profiler, works on live/production processes without code changes) to see where wall-clock time is actually going — this is the fastest way to confirm "is this blocking?" instead of reasoning about it in the abstract.
- **Per-request timing**: a small ASGI middleware adding an `X-Process-Time` header, or proper tracing (OpenTelemetry), to see which endpoints or downstream calls dominate.
- If concurrent-load tests don't scale with added workers/cores at all, that's itself a strong signal something is blocking the event loop (§1) rather than a deployment/sizing problem (§6).

---

## Quick wins checklist

- [ ] No sync/blocking calls inside `async def` (endpoints *and* dependencies)
- [ ] `uvicorn[standard]` installed (uvloop + httptools)
- [ ] Multiple worker processes, sized to CPU cores and re-measured
- [ ] Async DB driver end to end; pool sized against `workers × (pool_size + max_overflow)` vs. DB `max_connections`
- [ ] No N+1 queries on list/relationship-heavy endpoints
- [ ] Response models / return-type annotations used instead of manual `ORJSONResponse` wrapping
- [ ] Middleware stack minimal; `BaseHTTPMiddleware` only where its convenience is worth the overhead
- [ ] CPU-bound work off the event loop and off the default thread pool (process pool or task queue)
- [ ] `--reload` off, docs endpoints reviewed for production
- [ ] Changes verified with a load test or profiler, not assumed
