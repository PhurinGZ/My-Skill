# Testing Frameworks Reference

Quick reference for test syntax across frameworks. Load this when you need specific API details for writing tests.

---

## Python — pytest

### Installation
```bash
pip install pytest pytest-cov
```

### Basic Structure
```python
# test_mymodule.py
def test_<function>_<scenario>():
    # Arrange
    input_data = ...
    expected = ...
    
    # Act
    result = my_function(input_data)
    
    # Assert
    assert result == expected
```

### Key Assertions
```python
assert result == expected           # equality
assert result != unexpected         # inequality
assert result is None               # None check
assert result is not None           # not None
assert "substring" in result        # string/list membership
assert len(result) == 3             # length
assert isinstance(result, list)     # type check
```

### Exceptions
```python
import pytest

def test_raises_value_error():
    with pytest.raises(ValueError):
        my_function(bad_input)

def test_raises_with_message():
    with pytest.raises(ValueError, match="must be positive"):
        my_function(-1)
```

### Fixtures
```python
@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()

def test_query(db_connection):
    result = query(db_connection, "SELECT 1")
    assert result is not None
```

### Parametrize
```python
@pytest.mark.parametrize("input,expected", [
    ([], 0),
    ([1], 1),
    ([1, 2, 3], 6),
    ([-1, 1], 0),
])
def test_sum(input, expected):
    assert my_sum(input) == expected
```

### Running Tests
```bash
pytest                          # run all
pytest test_users.py            # specific file
pytest -v                       # verbose
pytest -k "test_null"           # filter by name
pytest --cov=mymodule           # coverage
```

---

## JavaScript / TypeScript — Jest

### Installation
```bash
npm install --save-dev jest @types/jest ts-jest
```

### Basic Structure
```typescript
import { myFunction } from './myModule';

describe('myFunction', () => {
  it('description of what it does', () => {
    // Arrange
    const input = ...;
    
    // Act
    const result = myFunction(input);
    
    // Assert
    expect(result).toBe(expected);
  });
});
```

### Key Matchers
```typescript
expect(val).toBe(exact)           // strict equality (===)
expect(val).toEqual(obj)          // deep equality
expect(val).toBeNull()            // null
expect(val).toBeUndefined()       // undefined
expect(val).toBeTruthy()          // truthy
expect(val).toBeFalsy()           // falsy
expect(val).toContain(item)       // array/string contains
expect(val).toHaveLength(n)       // length
expect(val).toMatchObject(shape)  // partial object match
expect(fn).toThrow('message')     // throws with message
```

### Async Tests
```typescript
// Promise-based
it('fetches data', async () => {
  const result = await fetchData('123');
  expect(result).toHaveProperty('id', '123');
});

// With done callback (older style)
it('calls callback', (done) => {
  asyncFn((result) => {
    expect(result).toBe('done');
    done();
  });
});
```

### Mocking
```typescript
// Mock entire module
jest.mock('./api');
import { fetchUser } from './api';
(fetchUser as jest.Mock).mockResolvedValue({ id: '1', name: 'Alice' });

// Mock a function
const mockFn = jest.fn().mockReturnValue(42);

// Spy on method
const spy = jest.spyOn(obj, 'method').mockReturnValue('mocked');
```

### Running Tests
```bash
npx jest                        # run all
npx jest --watch                # watch mode
npx jest myModule.test.ts       # specific file
npx jest --coverage             # coverage report
```

---

## JavaScript / TypeScript — Vitest

Vitest is a drop-in replacement for Jest when using Vite. API is nearly identical:

```typescript
import { describe, it, expect, vi } from 'vitest';
import { myFunction } from './myModule';

describe('myFunction', () => {
  it('works correctly', () => {
    expect(myFunction('input')).toBe('expected');
  });

  it('mocks correctly', () => {
    const fn = vi.fn().mockReturnValue(42);
    expect(fn()).toBe(42);
  });
});
```

```bash
npx vitest          # watch mode
npx vitest run      # single run
npx vitest --coverage
```

---

## Go — testing package

```go
func TestMyFunction_NormalCase(t *testing.T) {
    result := MyFunction("input")
    if result != "expected" {
        t.Errorf("got %q, want %q", result, "expected")
    }
}

// Table-driven tests
func TestMyFunction(t *testing.T) {
    tests := []struct{
        name  string
        input string
        want  string
    }{
        {"empty", "", ""},
        {"normal", "hello", "HELLO"},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := MyFunction(tt.input); got != tt.want {
                t.Errorf("got %q, want %q", got, tt.want)
            }
        })
    }
}
```

---

## Test Coverage Targets

| Situation | Target Coverage |
|-----------|----------------|
| Bug fix (regression) | 100% of the fixed path |
| New feature | 80%+ of new code |
| Existing legacy code | Improve incrementally |
| Critical business logic | 90%+ |

**Minimum tests to write for any fix:**
1. Regression test — proves the bug is fixed
2. Happy path — proves normal behavior still works
3. One edge case — empty input, null, boundary value
