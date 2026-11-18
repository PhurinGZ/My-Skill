# Debugging Strategies

When the bug isn't immediately obvious from the error message, use these systematic strategies. Load this for complex or intermittent bugs.

---

## Strategy 1: Minimal Reproducible Example (MRE)

The most powerful debugging technique. Strip the code down to the smallest version that still exhibits the bug.

**Process:**
1. Start with the failing code
2. Remove unrelated features one by one
3. Replace real data with hardcoded minimal data
4. Stop when removing anything more makes the bug disappear

**Why it works:** Forces you to understand which part is actually broken. Often you find the bug *while making* the MRE.

```python
# Instead of debugging 200 lines, isolate:
def test_minimal():
    data = {"name": None}  # minimal input that triggers bug
    result = process(data)
    print(result)  # does it crash here?
```

---

## Strategy 2: Binary Search Debugging

When you have a large block of code and don't know where the bug is.

**Process:**
1. Add a print/log at the halfway point
2. If the value is already wrong → bug is in the first half
3. If the value is correct → bug is in the second half
4. Repeat until you've narrowed to 1–5 lines

```python
def process_pipeline(data):
    data = step_one(data)
    print("After step_one:", data)   # <-- checkpoint A (middle)
    
    data = step_two(data)
    data = step_three(data)
    print("After step_three:", data)  # <-- checkpoint B
    
    data = step_four(data)
    return data

# If checkpoint A looks wrong → bug is in step_one
# If checkpoint A is fine but B is wrong → bug is in step_two or step_three
```

---

## Strategy 3: Rubber Duck Debugging

Explain the code out loud, line by line, to an imaginary listener.

**Why it works:** Forcing yourself to articulate *what each line does* often reveals the assumption that's wrong.

**Prompt yourself with:**
- "What does this line actually do?"
- "What am I *assuming* this returns?"
- "What would happen if this value was `None`?"
- "Have I seen this exact pattern fail before?"

---

## Strategy 4: Delta Debugging (What Changed?)

When code was working before and suddenly broke.

**Process:**
1. Check git diff — what changed since it last worked?
2. If no git history: comment out recent changes one by one
3. Check if the environment changed (new package version, config change, different data)

```bash
git log --oneline -20          # recent commits
git diff HEAD~1                # what changed in last commit
git bisect start               # binary search through commits
git bisect bad                 # current commit is broken
git bisect good <hash>         # this commit was working
# Git will checkout commits for you to test
```

---

## Strategy 5: Hypothesis-Driven Debugging

Form a specific, testable hypothesis before making any change.

**Template:**
> "I believe the bug is **[specific thing]** because **[evidence]**. I will verify by **[test]**. If correct, I expect **[outcome]**."

**Example:**
> "I believe the bug is that `user_id` is `None` when passed to `get_permissions()` because the error occurs there and the user login flow could return early. I will verify by printing `user_id` before the call. If correct, the print will show `None`."

This prevents "flailing" — randomly changing code and hoping something fixes it.

---

## Strategy 6: Log-Driven Debugging

Add strategic logging to understand program flow over time. Especially useful for intermittent bugs.

**What to log:**
- Function entry/exit with parameters
- State changes
- External calls (DB queries, API calls) and their responses
- Branch conditions ("taking the else branch because x=None")

```python
import logging
logger = logging.getLogger(__name__)

def process_order(order_id: str, user_id: str):
    logger.debug(f"process_order called: order_id={order_id}, user_id={user_id}")
    
    order = db.get_order(order_id)
    logger.debug(f"fetched order: {order}")
    
    if order is None:
        logger.warning(f"Order {order_id} not found")
        return None
    
    result = apply_discount(order, user_id)
    logger.debug(f"after discount: {result}")
    return result
```

**Log levels:**
- `DEBUG` — detailed flow, values, intermediate states
- `INFO` — significant events (user logged in, order created)
- `WARNING` — unexpected but handled (retrying, fallback used)
- `ERROR` — something failed (exception caught)
- `CRITICAL` — system cannot continue

---

## Strategy 7: Test-First Debugging (TDD for bugs)

Write the failing test *before* fixing the code. This:
1. Proves you can reproduce the bug
2. Defines exactly what "fixed" means
3. Prevents regression automatically

```python
# Step 1: Write a test that reproduces the bug
def test_parse_name_with_none_should_return_empty():
    # This test FAILS right now — that's the point
    result = parse_name({"name": None})
    assert result == ("", "")

# Step 2: Run the test → confirm it fails
# Step 3: Fix the code
# Step 4: Run the test → confirm it passes
# Step 5: Run all tests → confirm nothing else broke
```

---

## Strategy 8: State Inspection

For complex bugs, dump the full state at the point of failure.

```python
# Python — dump all local variables
import traceback

def process(data):
    try:
        result = complex_operation(data)
    except Exception as e:
        import pprint
        print("=== STATE AT FAILURE ===")
        print(f"data: {pprint.pformat(data)}")
        print(f"locals: {pprint.pformat(locals())}")
        traceback.print_exc()
        raise
```

```javascript
// JavaScript — structured logging
function process(data) {
  try {
    return complexOperation(data);
  } catch (err) {
    console.error('Process failed:', {
      input: data,
      error: err.message,
      stack: err.stack,
    });
    throw err;
  }
}
```

---

## Choosing the Right Strategy

| Situation | Best Strategy |
|---|---|
| Error message with line number | Go directly to the line — standard analysis |
| Large codebase, bug location unknown | Binary Search |
| Works sometimes, fails sometimes | Log-Driven + State Inspection |
| Code worked before, now broken | Delta Debugging (git diff) |
| Complex logic, can't see the bug | Rubber Duck + Hypothesis-Driven |
| Want to prevent regression | Test-First Debugging |
| Can't reproduce with real data | Minimal Reproducible Example |
| Many interacting components | Minimal Reproducible Example + Binary Search |

---

## Red Flags While Debugging

Stop and reconsider if you're:
- Making changes without understanding why
- Trying the same fix multiple times
- Adding workarounds on top of workarounds
- Saying "it should work" — it doesn't, so something is wrong
- Spending >30 min on one bug without progress

**When stuck >30 minutes:**
1. Take a break (seriously — fresh eyes find bugs)
2. Explain the problem to someone else (rubber duck)
3. Search for the exact error message
4. Check if a library was recently updated (check changelog)
5. Create a minimal reproduction
