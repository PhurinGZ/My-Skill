# Rendering & State Architecture

Most re-render problems are architectural, not "missing a `useMemo`." Fix the shape of state and component tree before reaching for memoization.

## Colocate state as close as possible to where it's used

State declared high in the tree re-renders everything below it on every update, even components that don't read that state (unless they're memoized with stable props).

```tsx
// ❌ isOpen lives in the page component — the whole page re-renders on toggle
function Page() {
  const [isOpen, setIsOpen] = useState(false)
  return (
    <div>
      <ExpensiveChart />
      <Sidebar isOpen={isOpen} onToggle={() => setIsOpen(!isOpen)} />
    </div>
  )
}

// ✅ isOpen lives inside Sidebar — only Sidebar re-renders on toggle
function Page() {
  return (
    <div>
      <ExpensiveChart />
      <Sidebar />
    </div>
  )
}
function Sidebar() {
  const [isOpen, setIsOpen] = useState(false)
  // ...
}
```

## "Lifting content up" instead of memoizing (the `children` prop trick)

If a state change in a parent must stay in the parent (e.g., it also affects a sibling), pass unaffected subtrees as `children`/props from an ancestor that doesn't re-render, rather than memoizing them:

```tsx
// ✅ ExpensiveChart is passed as children from App (which doesn't re-render on toggle),
// so React skips re-rendering it even though Page itself re-renders
function App() {
  return (
    <Page>
      <ExpensiveChart />
    </Page>
  )
}
function Page({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false)
  return (
    <div>
      {children}
      <Sidebar isOpen={isOpen} onToggle={() => setIsOpen(!isOpen)} />
    </div>
  )
}
```
This works because React bails out of re-rendering `children`/`props.something` elements that were created by a parent higher up that didn't itself re-render — no memoization needed.

## Split contexts by update frequency

One context holding both frequently-changing and rarely-changing values forces all consumers to re-render on every change to any of it.

```tsx
// ❌ one context, mixed frequency
const AppContext = createContext({ theme, cursorPosition, user })

// ✅ split by how often each value changes
const ThemeContext = createContext(theme)          // rarely changes
const CursorContext = createContext(cursorPosition) // changes constantly
const UserContext = createContext(user)             // rarely changes
```
Components that only read `ThemeContext` never re-render when `cursorPosition` updates.

## Derive, don't duplicate + sync

```tsx
// ❌ derived state stored separately and kept in sync with an effect — extra render + bug surface
const [items, setItems] = useState<Item[]>([])
const [total, setTotal] = useState(0)
useEffect(() => {
  setTotal(items.reduce((sum, i) => sum + i.price, 0))
}, [items])

// ✅ compute during render (memoize only if the computation is actually expensive)
const [items, setItems] = useState<Item[]>([])
const total = useMemo(() => items.reduce((sum, i) => sum + i.price, 0), [items])
```
Storing derived values in state and syncing with `useEffect` causes an extra render pass and is a common source of stale-data bugs. Compute it inline; only wrap in `useMemo` if profiling shows the computation itself is expensive.

## `key` prop for intentional full remounts

Changing a component's `key` forces React to discard and recreate it (unmount + fresh mount) rather than reconciling — useful for intentionally resetting all internal state (e.g., a form) instead of writing manual reset logic:

```tsx
<UserForm key={selectedUserId} userId={selectedUserId} />
```
Use deliberately — it's a full remount, not free, so don't reach for it as a general-purpose "just re-render everything" tool.

## Avoid prop drilling through many layers of unrelated components

If a deeply nested component needs a value from far up the tree, every intermediate component re-renders when that value changes (unless each is individually memoized with stable props). Prefer `context` (split appropriately, per above) or component composition (`children`) over drilling through 4+ layers.
