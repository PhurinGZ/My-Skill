# Language-Specific Bug Patterns

Reference guide for common bugs, error messages, and debugging strategies by language. Load this when working on a specific language to supplement the main SKILL.md.

---

## Python

### Most Common Bugs

| Bug | Trigger | Fix |
|-----|---------|-----|
| Mutable default argument | `def f(lst=[]):` | Use `None` default: `def f(lst=None): lst = lst or []` |
| `None` not checked | Accessing attr on a function that can return `None` | Add guard: `if result is not None:` |
| Off-by-one in `range()` | `range(len(arr) - 1)` skips last element | Use `range(len(arr))` or `for item in arr:` |
| `KeyError` | `dict['key']` where key may not exist | Use `dict.get('key', default)` |
| Shadowing builtins | Variable named `list`, `id`, `type`, `str` | Rename variable |
| Late binding closure | Lambda/function in loop captures loop variable | Use default arg: `lambda x=x: x` |

### Error Message Decoder

- `AttributeError: 'NoneType' object has no attribute 'X'` → something returned `None` unexpectedly
- `TypeError: 'X' object is not subscriptable` → tried to index something that isn't a list/dict
- `RecursionError: maximum recursion depth exceeded` → missing base case or infinite recursion
- `IndentationError` → mixed tabs/spaces, or wrong block level
- `UnboundLocalError: local variable 'X' referenced before assignment` → variable assigned inside an `if` but used before

### Testing with pytest

```python
# Preferred patterns
def test_function_scenario():
    assert my_func(input) == expected

def test_raises_on_invalid():
    with pytest.raises(ValueError, match="expected message"):
        my_func(bad_input)

@pytest.mark.parametrize("input,expected", [
    ([], 0),
    ([1], 1),
    ([1, 2, 3], 6),
])
def test_sum_parametrized(input, expected):
    assert my_sum(input) == expected

@pytest.fixture
def sample_user():
    return {"name": "Alice", "age": 30}
```

---

## JavaScript / TypeScript

### Most Common Bugs

| Bug | Trigger | Fix |
|-----|---------|-----|
| Missing `await` | `const data = fetch(url)` — gets Promise not value | Add `await` |
| Accessing undefined | `obj.prop.nested` when `obj.prop` may be undefined | Use `obj?.prop?.nested` |
| Wrong `this` in callback | Regular function passed as callback loses `this` | Use arrow function |
| `var` in loop closure | `for (var i=0; ...)` captured by closure | Replace `var` with `let` |
| NaN comparison | `if (x === NaN)` always false | Use `Number.isNaN(x)` |
| Off-by-one in splice/slice | `arr.slice(0, n-1)` misses last element | Check inclusive/exclusive endpoints |

### TypeScript-Specific

- `Type 'X \| undefined' is not assignable to type 'X'` → add null check or use non-null assertion (`!`) with caution
- `Argument of type 'string' is not assignable to parameter of type 'number'` → type mismatch at call site
- `Property 'X' does not exist on type 'Y'` → wrong type, or need to extend the interface
- Generic types not inferred → provide type arguments explicitly: `useState<User | null>(null)`

### Testing with Jest / Vitest

```typescript
import { myFunction } from './myModule';

describe('myFunction', () => {
  it('handles normal input', () => {
    expect(myFunction('hello')).toBe('HELLO');
  });

  it('throws on invalid input', () => {
    expect(() => myFunction(null)).toThrow('Input required');
  });

  it('resolves async correctly', async () => {
    const result = await fetchUser('123');
    expect(result).toMatchObject({ id: '123' });
  });
});

// Mocking
jest.mock('./api', () => ({
  fetchUser: jest.fn().mockResolvedValue({ id: '123', name: 'Alice' }),
}));
```

---

## React-Specific Bugs

### Common Patterns

- **Infinite re-render loop** — `useEffect` sets state that is also in its dependency array
- **Stale closure** — callback captures old state value; fix with functional update `setState(prev => ...)`
- **Missing `key` prop** — React can't efficiently reconcile list items
- **State mutation** — `state.push(item)` won't trigger re-render; use spread: `[...state, item]`
- **Async setState after unmount** — component unmounts before async operation completes; use cleanup function in `useEffect`

```javascript
// Stale closure fix
const [count, setCount] = useState(0);
// Wrong:
setTimeout(() => setCount(count + 1), 1000); // captures old count
// Right:
setTimeout(() => setCount(prev => prev + 1), 1000);
```

---

## General Multi-File Debugging

When a project spans multiple files, use this checklist:

1. **Check the import path** — is it correct relative to the importer?
2. **Check the export** — is the function/class actually exported? Named vs default?
3. **Check the name** — exact spelling including case (`calculateTax` vs `calc_tax`)
4. **Check circular imports** — A imports B, B imports A → move shared code to a third file
5. **Check which file the error is in** — trace the stack frame by frame

```
ImportError: cannot import name X from Y
→ Check: does Y actually define and export X?
→ Check: are you importing from the right file path?
→ Check: is there a typo in the import name?
```
