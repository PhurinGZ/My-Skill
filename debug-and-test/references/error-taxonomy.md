# Error Taxonomy & Root Cause Map

A systematic classification of errors by type, with the most likely root causes and first-steps for each. Load this when the user shares an error message you need to quickly categorize.

---

## Tier 1: Runtime Errors (program crashes during execution)

### Null / Undefined Reference
**Signatures:**
- Python: `AttributeError: 'NoneType' object has no attribute 'X'`
- JS/TS: `TypeError: Cannot read properties of undefined (reading 'X')`
- Java: `NullPointerException`
- Go: `nil pointer dereference`
- Rust: (prevented by compiler — look for unwrap panics instead)

**Most likely causes (in order):**
1. A function returned `None`/`null`/`undefined` but return value wasn't checked
2. An async call wasn't awaited — still a Promise
3. A dict/object key doesn't exist and wasn't defaulted
4. An optional field was accessed without a guard
5. A variable was declared but never assigned before use

**First steps:**
- Find the exact line — what variable is `None`?
- Trace backwards: who assigned that variable? What could make it `None`?
- Add a null check or use optional chaining

---

### Type Errors
**Signatures:**
- Python: `TypeError: unsupported operand type(s) for +: 'int' and 'str'`
- TS: `Argument of type 'X' is not assignable to parameter of type 'Y'`
- JS: `NaN` appearing in calculations

**Most likely causes:**
1. String received where number expected (or vice versa) — often from user input or JSON parsing
2. Function signature mismatch — wrong argument order
3. `parseInt`/`int()` not called on string input
4. TypeScript generic not inferred correctly

**First steps:**
- Print/log the actual type: `type(x)` in Python, `typeof x` in JS
- Trace where the variable was first created — is the type correct at origin?

---

### Index / Key Errors
**Signatures:**
- Python: `IndexError: list index out of range`, `KeyError: 'name'`
- JS: Accessing `arr[n]` returns `undefined` silently
- Go: `index out of range`

**Most likely causes:**
1. Off-by-one — loop goes one too far or `range(len(x)-1)` goes one too short
2. Dict/object key doesn't exist — should use `.get()` or optional chaining
3. List is empty — no guard for empty case
4. Data structure changed shape (API response missing a field)

---

### Recursion / Stack Overflow
**Signatures:**
- Python: `RecursionError: maximum recursion depth exceeded`
- JS: `RangeError: Maximum call stack size exceeded`
- Most languages: stack overflow

**Most likely causes:**
1. Missing base case in recursive function
2. Base case is never reached (off-by-one in termination condition)
3. Mutual recursion: A calls B calls A infinitely
4. React: component renders → state update → render → infinite loop

---

## Tier 2: Logic Errors (program runs but gives wrong answers)

These are the hardest bugs — no crash, just wrong output.

### Silent Wrong Value
**Symptoms:** Calculation is off, output is unexpected, tests pass but behavior is wrong.

**Debugging approach:**
1. Add print/log at each step to trace intermediate values
2. Use a minimal reproducing case — strip away everything not needed
3. Binary search: comment out half the code, is the value still wrong?
4. Check: integer division vs float division (`5/2 = 2` in Python 2, `2.5` in Python 3)
5. Check: operator precedence — `a + b * c` vs `(a + b) * c`

### Off-By-One (logic variant)
**Symptoms:** Result is one element short/long, boundary conditions fail.

**Checklist:**
- Is the range `[0, n)` or `[0, n]`? Should it be inclusive or exclusive?
- Does the loop start at 0 or 1?
- Is `<` used where `<=` is needed (or vice versa)?
- Does the last element get processed?

### State Mutation Bug
**Symptoms:** Works on first call, fails on second; tests pass in isolation but fail together.

**Most likely causes:**
1. Mutable default argument (Python)
2. Shared mutable state — global variable, class variable
3. Object passed by reference and mutated inside function
4. React state mutated directly instead of spread

```python
# Classic Python mutation bug
def add(item, lst=[]):   # lst is shared!
    lst.append(item)
    return lst

# Fix
def add(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

### Async / Race Condition
**Symptoms:** Works sometimes, fails sometimes; order-dependent failures.

**Most likely causes:**
1. Two async operations that depend on each other run in wrong order
2. `await` missing — next line runs before async op completes
3. `Promise.all` not used when multiple async ops needed in parallel
4. Database transaction not awaited before reading result

---

## Tier 3: Integration Errors (system boundaries)

### Import / Module Errors
**Signatures:**
- Python: `ImportError`, `ModuleNotFoundError`, `cannot import name X`
- JS/TS: `Cannot find module`, `is not a function`

**Checklist:**
1. Is the package installed? (`pip list`, `npm list`)
2. Is the import path correct (relative vs absolute)?
3. Is the exported name spelled correctly (case-sensitive)?
4. Named export vs default export confusion in JS?
5. Circular imports?

### Environment / Config Errors
**Symptoms:** Works on dev, fails on prod; env var is `None`/`undefined`.

**Checklist:**
1. Is the `.env` file loaded? (dotenv, python-decouple, etc.)
2. Is the variable name spelled correctly — exact case?
3. Is the variable set in the deployment environment (CI, Docker, cloud)?
4. Is a required secret missing from the secrets manager?

### Database / ORM Errors
**Signatures:**
- `OperationalError: no such column`
- `IntegrityError: UNIQUE constraint failed`
- `DetachedInstanceError` (SQLAlchemy)
- `N+1 query problem` (performance, not a crash)

**Checklist:**
1. Did migrations run? (`alembic upgrade head`, `python manage.py migrate`)
2. Is the schema in sync with the model?
3. Is the session closed before accessing a lazy-loaded relationship?
4. Is there a missing `.select_related()` / `populate()` causing N+1?

### HTTP / API Errors
**Status code quick reference:**

| Code | Meaning | Common cause |
|------|---------|--------------|
| 400 | Bad Request | Wrong request body shape, missing required field |
| 401 | Unauthorized | Missing or expired auth token |
| 403 | Forbidden | Token valid but insufficient permissions |
| 404 | Not Found | Wrong URL, resource doesn't exist, wrong ID |
| 409 | Conflict | Duplicate key, already exists |
| 422 | Unprocessable | Validation error — body parses but fails validation |
| 429 | Rate Limited | Too many requests — add retry with backoff |
| 500 | Server Error | Crash on the server — check server logs |
| 502/503 | Bad Gateway / Unavailable | Server not running, deployment failed |
| CORS Error | (browser only) | Server missing CORS headers, wrong origin |

---

## Tier 4: Performance Errors (correct but too slow)

### N+1 Query
**Symptom:** Page loads correctly but slowly; DB query count explodes with data size.
**Fix:** Use `select_related`/`prefetch_related` (Django), `populate` (Mongoose), `include` (Prisma), `JOIN` (raw SQL).

### Memory Leak
**Symptom:** Memory grows over time; eventually crashes.
**Common causes:** Event listeners not removed, large objects held in closures, circular references, infinite accumulation in a list.

### Blocking the Event Loop (Node.js)
**Symptom:** Server handles one request at a time; high latency under load.
**Fix:** Move CPU-intensive work to worker threads; never use sync file I/O in request handlers.

---

## Quick Diagnosis Decision Tree

```
Error received?
│
├─ Has a line number? → Go to that line first
│
├─ "None/null/undefined" in error? → Null reference bug
│
├─ "Cannot find" / "No module" / "ImportError"? → Import/module bug
│
├─ "Type" in error? → Type mismatch bug
│
├─ "Index" / "out of range"? → Off-by-one or empty collection
│
├─ No error, wrong output? → Logic bug — add logging, binary search
│
├─ Works sometimes? → Race condition or state mutation
│
└─ Works locally, fails in prod? → Environment/config bug
```
