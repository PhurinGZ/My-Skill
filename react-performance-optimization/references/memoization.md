# Memoization — React.memo, useMemo, useCallback

**Check React Compiler status first (see main SKILL.md).** If the project runs React 19+ with the compiler enabled, most of this file's manual techniques are unnecessary and can even be counterproductive — the compiler auto-memoizes. This file is written for React 18 (Bas's Wald Pottery stack) and for the compiler-unsupported cases on React 19.

## React.memo — skip re-rendering a component when props haven't changed

```tsx
type RowProps = { id: string; label: string; onSelect: (id: string) => void }

const Row = React.memo(function Row({ id, label, onSelect }: RowProps) {
  return <button onClick={() => onSelect(id)}>{label}</button>
})
```

`React.memo` does a shallow comparison of props. It only helps if:
1. The component actually re-renders often as a *sibling* effect of a parent state change (confirmed via Profiler), and
2. Its props are usually the same between those re-renders

**It will silently do nothing** if you pass a new object/array/function literal as a prop each render — see the "stable references" section below. This is the #1 reason `React.memo` "doesn't work."

Custom comparison (rarely needed, use sparingly — it's easy to introduce bugs):
```tsx
const Row = React.memo(RowImpl, (prev, next) => prev.id === next.id && prev.label === next.label)
```

## useMemo — cache an expensive computed value

```tsx
const sortedItems = useMemo(
  () => items.slice().sort((a, b) => a.price - b.price),
  [items]
)
```

Use for:
- Expensive derivations (sorting/filtering/aggregating non-trivial arrays, heavy calculations)
- Producing a stable object/array reference that's passed as a prop to a `memo`-wrapped child or used as an effect dependency

Don't use for:
- Cheap operations (`items.length`, simple string concatenation) — the memoization bookkeeping costs more than the computation
- Values that change every render anyway

## useCallback — stable function reference

```tsx
const handleSelect = useCallback((id: string) => {
  setSelectedId(id)
}, [])
```

Only matters when the function is:
- Passed as a prop to a `React.memo`-wrapped child (otherwise the child re-renders anyway regardless of memo), or
- Used as a dependency in another hook's dependency array (`useEffect`, `useMemo`, etc.) where you need referential stability to avoid re-running that effect every render

A `useCallback` with no consumer that cares about referential identity does nothing useful — it still creates a new function each render in React 18 pre-compiler terms conceptually, it just returns the memoized one; the win only exists if something downstream compares identity.

**Stale closure trap:** if the dependency array is missing values the callback actually uses, you'll capture outdated variables. Use the `eslint-plugin-react-hooks` `exhaustive-deps` rule — don't manually suppress it without a documented reason.

## Stable references — the prerequisite for all of the above

None of `memo`/`useMemo`/`useCallback` help if you're still creating new literals on every render at the call site:

```tsx
// ❌ defeats memo — new object every render
<Row style={{ color: 'red' }} onSelect={(id) => setSelectedId(id)} />

// ✅ stable — hoisted constant + useCallback
const rowStyle = { color: 'red' } // module-level constant if it never changes
const handleSelect = useCallback((id: string) => setSelectedId(id), [])
<Row style={rowStyle} onSelect={handleSelect} />
```

If a value truly never changes across renders (a style object, a config object, a static array of options), define it **outside the component** (module scope) rather than memoizing it inside — it's simpler and has zero per-render cost.

## Memoizing context values

A very common re-render bomb: a context provider value created inline.

```tsx
// ❌ every render of the provider creates a new object → every consumer re-renders
<MyContext.Provider value={{ user, setUser }}>

// ✅ memoize the value object
const value = useMemo(() => ({ user, setUser }), [user])
<MyContext.Provider value={value}>
```

Also consider splitting one context into multiple contexts by update frequency — see `rendering-state.md`.

## React Compiler notes (React 19+)

When the compiler is active:
- Don't add manual `useMemo`/`useCallback`/`React.memo` for ordinary render-cost reasons — trust the compiler's static analysis, which handles the common cases automatically and is verified via `eslint-plugin-react-hooks`'s compiler-aware rules
- The compiler bails out of optimizing a component if it detects rule-of-hooks violations, mutation of props/state during render, or other unsafe patterns — fix those instead of manually memoizing around them
- Manual memoization is still valid for cases the compiler doesn't cover: stabilizing values that cross a boundary the compiler can't statically analyze (e.g., values handed to non-React code, some ref patterns), or intentionally skipping an expensive computation based on custom equality logic
- Verify the compiler is actually configured before assuming its behavior applies — check `vite.config`/`next.config`/babel config for `babel-plugin-react-compiler`
