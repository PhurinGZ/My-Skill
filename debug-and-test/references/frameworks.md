# Framework-Specific Bug Patterns

Common bugs and gotchas for popular frameworks. Load the relevant section when the user is working with a specific framework.

---

## Python Frameworks

### FastAPI

#### Common Bugs

**Async endpoint calling sync DB code**
```python
# Wrong — blocks the event loop
@app.get("/users")
async def get_users():
    return db.query(User).all()  # sync SQLAlchemy call!

# Fix — use run_in_executor or async ORM (SQLAlchemy 2.0 async)
@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()
```

**Dependency not yielding — session not closed**
```python
# Wrong — session never closed on error
def get_db():
    return SessionLocal()

# Correct — yield ensures cleanup
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Pydantic v2 breaking changes (if migrating from v1)**
- `__fields__` → `model_fields`
- `validator` → `field_validator`
- `.dict()` → `.model_dump()`
- `orm_mode = True` → `model_config = ConfigDict(from_attributes=True)`

**422 Unprocessable Entity — validation error**
- Check the response body: FastAPI returns detailed field errors
- Most common: wrong field name, wrong type, missing required field
- Use `response.json()` in tests to see the exact validation error

#### Testing FastAPI
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user_missing_field():
    response = client.post("/users", json={})
    assert response.status_code == 422
```

---

### Django / Django REST Framework

#### Common Bugs

**`RelatedObjectDoesNotExist` / `DoesNotExist`**
```python
# Wrong — crashes if not found
user = User.objects.get(id=user_id)

# Fix — handle missing
try:
    user = User.objects.get(id=user_id)
except User.DoesNotExist:
    return Response({"error": "Not found"}, status=404)

# Or with get_object_or_404
from django.shortcuts import get_object_or_404
user = get_object_or_404(User, id=user_id)
```

**N+1 query — forgetting `select_related`**
```python
# N+1 — fires one query per post
posts = Post.objects.all()
for post in posts:
    print(post.author.name)  # extra query each time!

# Fix
posts = Post.objects.select_related('author').all()
```

**Migrations out of sync**
```bash
# When you see: "column does not exist" or "table does not exist"
python manage.py makemigrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

**DRF: Serializer `is_valid()` not called**
```python
# Wrong — skips validation
serializer = UserSerializer(data=request.data)
serializer.save()

# Correct
serializer = UserSerializer(data=request.data)
if serializer.is_valid():
    serializer.save()
else:
    return Response(serializer.errors, status=400)
```

---

## JavaScript / TypeScript Frameworks

### Next.js

#### Common Bugs

**`window is not defined` (SSR error)**
- Cause: accessing browser globals during server-side rendering
```typescript
// Wrong — crashes on server
const width = window.innerWidth;

// Fix — guard with typeof
const width = typeof window !== 'undefined' ? window.innerWidth : 0;

// Or use useEffect (client-only)
useEffect(() => {
  const width = window.innerWidth;
}, []);
```

**Hydration mismatch**
- Symptom: `Error: Hydration failed because the initial UI does not match what was rendered on the server`
- Cause: Server and client render different HTML (timestamps, random values, browser-only checks)
- Fix: Use `suppressHydrationWarning` for intentional differences, or `useEffect` for client-only rendering

**`getServerSideProps` / `getStaticProps` not typed correctly**
```typescript
import type { GetServerSideProps, NextPage } from 'next';

export const getServerSideProps: GetServerSideProps = async (context) => {
  const data = await fetchData();
  return { props: { data } };
};
```

**App Router vs Pages Router confusion**
- `use client` directive required for hooks, event handlers, browser APIs
- Server Components cannot use `useState`, `useEffect`, or context
- `cookies()`, `headers()` only available in Server Components

---

### Express.js

#### Common Bugs

**Middleware order matters**
```javascript
// Wrong — route defined before JSON parser
app.get('/api/data', handler);
app.use(express.json());  // too late!

// Correct — middleware before routes
app.use(express.json());
app.use(cors());
app.get('/api/data', handler);
```

**Async error not caught**
```javascript
// Wrong — unhandled promise rejection
app.get('/users', async (req, res) => {
  const users = await db.findAll();  // if this throws, Express hangs
  res.json(users);
});

// Fix — wrap or use express-async-errors
app.get('/users', async (req, res, next) => {
  try {
    const users = await db.findAll();
    res.json(users);
  } catch (err) {
    next(err);  // passes to error handler
  }
});
```

**Response sent twice**
- Symptom: `Cannot set headers after they are sent to the client`
- Cause: `res.json()` or `res.send()` called more than once (missing `return`)
```javascript
// Wrong
if (!user) {
  res.status(404).json({ error: 'Not found' });
}
res.json(user);  // also runs!

// Fix
if (!user) {
  return res.status(404).json({ error: 'Not found' });
}
res.json(user);
```

---

### Prisma (ORM)

#### Common Bugs

**Schema out of sync**
```bash
# When you see: "The table does not exist" or field missing
npx prisma migrate dev     # dev environment
npx prisma generate        # regenerate client after schema change
npx prisma db push         # push schema without migration (prototyping)
```

**Relation not included**
```typescript
// Wrong — author is undefined
const posts = await prisma.post.findMany();
posts[0].author  // undefined!

// Fix — use include
const posts = await prisma.post.findMany({
  include: { author: true }
});
```

**Unique constraint violation**
- Symptom: `PrismaClientKnownRequestError` with code `P2002`
- Cause: Trying to create a record with a duplicate unique field
- Fix: Use `upsert` or check existence first

```typescript
// Handle gracefully
try {
  await prisma.user.create({ data: { email } });
} catch (e) {
  if (e.code === 'P2002') {
    return { error: 'Email already exists' };
  }
  throw e;
}
```

---

## Testing Anti-Patterns to Catch

These are bugs *in the tests themselves* — not in the application code.

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Testing implementation not behavior | Test breaks when you refactor | Test inputs and outputs, not internal calls |
| No assertion | Test always passes | Every test needs at least one `assert`/`expect` |
| Tests that depend on each other | Flaky when run in isolation | Each test should be fully independent |
| Mocking too much | Tests pass but real code broken | Mock only external dependencies (DB, API) |
| Hardcoded timestamps/IDs | Flaky due to timing | Use fixed dates or relative comparisons |
| Not resetting state between tests | Side effects bleed between tests | Use `beforeEach` / `setUp` / fixtures |
| Asserting on the wrong thing | Bug exists but test passes | Double-check what you're asserting |

---

## Debugging Tools Quick Reference

### Python
```bash
# Interactive debugger
import pdb; pdb.set_trace()   # old style
breakpoint()                   # Python 3.7+ 

# Logging
import logging
logging.basicConfig(level=logging.DEBUG)
logging.debug(f"Value of x: {x}")

# Pretty print complex objects
from pprint import pprint
pprint(complex_dict)
```

### JavaScript / Node.js
```javascript
// Browser devtools
console.log({ variable });          // log with label
console.table(arrayOfObjects);      // table view
console.trace();                    // print call stack

// Node.js debugger
node --inspect-brk server.js       // pause at start
// Then open chrome://inspect

// VS Code: add "debugger;" statement or set breakpoints
```

### Network / API
```bash
# Test endpoint directly
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'

# With auth token
curl -H "Authorization: Bearer <token>" http://localhost:3000/api/me
```
