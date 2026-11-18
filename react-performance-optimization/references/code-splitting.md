# Code Splitting — Smaller Initial Bundle, Faster First Load

Confirm the bottleneck with a bundle analyzer first (see `profiling.md`) before splitting arbitrarily — split around what's actually large, usually route-level pages or heavy third-party libraries (chart libs, rich text editors, PDF viewers, map libraries).

## React.lazy + Suspense — the baseline pattern

```tsx
import { lazy, Suspense } from 'react'

const AnalyticsDashboard = lazy(() => import('./AnalyticsDashboard'))

function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <AnalyticsDashboard />
    </Suspense>
  )
}
```
`AnalyticsDashboard` and everything it imports become a separate chunk, fetched only when this component actually renders.

## Route-based splitting (highest-leverage, do this first)

Split at the page/route level before anything else — it's the biggest win for initial load with the least code churn.

**React Router v6.4+ (data router):**
```tsx
const router = createBrowserRouter([
  {
    path: '/orders',
    lazy: async () => {
      const { OrdersPage } = await import('./pages/OrdersPage')
      return { Component: OrdersPage }
    },
  },
])
```

**React Router (plain `<Routes>`):**
```tsx
const OrdersPage = lazy(() => import('./pages/OrdersPage'))

<Routes>
  <Route
    path="/orders"
    element={
      <Suspense fallback={<PageSkeleton />}>
        <OrdersPage />
      </Suspense>
    }
  />
</Routes>
```

## Component-level splitting for heavy, conditionally-shown UI

Good candidates: modals, rarely-opened settings panels, rich text/chart/map libraries, admin-only views.

```tsx
const ChartLibraryModal = lazy(() => import('./ChartLibraryModal'))

function Toolbar() {
  const [showChart, setShowChart] = useState(false)
  return (
    <>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      {showChart && (
        <Suspense fallback={<Spinner />}>
          <ChartLibraryModal />
        </Suspense>
      )}
    </>
  )
}
```
Don't lazy-load things that render immediately on first paint — that just adds a network waterfall for no benefit. Lazy-load what's conditional or below the fold.

## Prefetching to hide the loading flash

If you know a lazy chunk will likely be needed soon (e.g., hovering a nav link before clicking), trigger the dynamic `import()` early to warm the cache without rendering yet:

```tsx
function NavLink() {
  return (
    <Link
      to="/orders"
      onMouseEnter={() => import('./pages/OrdersPage')}
    >
      Orders
    </Link>
  )
}
```

## Vite-specific notes (Bas's stack)

- Vite/Rollup automatically code-splits on dynamic `import()` — no extra config needed for the pattern above
- Manual chunk control when needed (e.g., forcing a large stable vendor library into its own long-term-cacheable chunk):
```ts
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
        },
      },
    },
  },
})
```
- Re-run `rollup-plugin-visualizer` (see `profiling.md`) after splitting to confirm chunks actually separated the way you expect — sometimes a shared dependency pulls unrelated code back into the same chunk

## Don't over-split

Excessive splitting (a separate chunk per tiny component) adds HTTP request overhead and can hurt more than it helps, especially on HTTP/1.1 or high-latency connections. Split at meaningful boundaries: routes, heavy conditional UI, large third-party libraries — not every component.
