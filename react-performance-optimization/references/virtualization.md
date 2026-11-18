# Virtualization — Long Lists and Tables

If the DOM has hundreds/thousands of rendered rows (mounted, in the DOM, even if scrolled out of view), scrolling and updates get janky because the browser has to lay out and paint all of them. Virtualization renders only the rows currently visible (plus a small overscan buffer) and swaps content as the user scrolls.

**When to reach for this:** confirmed via Profiler/Performance tab that render cost scales with total row count, not just visible rows — typically relevant past ~100–200 rows, and increasingly important as row complexity grows (rich cells, images, nested components).

## `@tanstack/react-virtual` (recommended default — actively maintained, framework-agnostic core, works for lists, tables, and grids)

```bash
npm install @tanstack/react-virtual
```

```tsx
import { useVirtualizer } from '@tanstack/react-virtual'
import { useRef } from 'react'

function OrderList({ orders }: { orders: Order[] }) {
  const parentRef = useRef<HTMLDivElement>(null)

  const virtualizer = useVirtualizer({
    count: orders.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 56, // approximate row height in px
    overscan: 8,
  })

  return (
    <div ref={parentRef} style={{ height: 600, overflow: 'auto' }}>
      <div style={{ height: virtualizer.getTotalSize(), position: 'relative' }}>
        {virtualizer.getVirtualItems().map((virtualRow) => {
          const order = orders[virtualRow.index]
          return (
            <div
              key={order.id}
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: virtualRow.size,
                transform: `translateY(${virtualRow.start}px)`,
              }}
            >
              <OrderRow order={order} />
            </div>
          )
        })}
      </div>
    </div>
  )
}
```

## `react-window` (lighter weight, simpler API, list/grid only)

```bash
npm install react-window
```

```tsx
import { FixedSizeList } from 'react-window'

function OrderList({ orders }: { orders: Order[] }) {
  return (
    <FixedSizeList height={600} itemCount={orders.length} itemSize={56} width="100%">
      {({ index, style }) => (
        <div style={style}>
          <OrderRow order={orders[index]} />
        </div>
      )}
    </FixedSizeList>
  )
}
```
Use `VariableSizeList` if rows have differing heights. `react-window` hasn't seen much active development recently compared to `@tanstack/react-virtual` — prefer the latter for new work unless there's a strong reason (existing codebase already uses it, need its smaller footprint).

## Variable / dynamic row heights

Both libraries support measuring actual rendered height instead of a fixed estimate — needed when row content varies (wrapping text, optional images). With `@tanstack/react-virtual`, use `measureElement`:
```tsx
const virtualizer = useVirtualizer({
  count: orders.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 56,
  measureElement: (el) => el.getBoundingClientRect().height,
})
```

## Table virtualization

For data tables (as opposed to simple lists), pair `@tanstack/react-virtual` with `@tanstack/react-table` — they're built by the same maintainer and designed to compose together for virtualized sortable/filterable tables.

## Trade-offs and gotchas to flag

- **Browser find-in-page (Ctrl+F) and screen readers won't see off-screen rows** — they don't exist in the DOM. If accessibility or in-page search matters, this is a real cost; discuss with the user rather than silently applying virtualization.
- **Scroll-to-item / scroll restoration** needs the library's API (`virtualizer.scrollToIndex(...)`) rather than plain DOM scroll — don't assume `element.scrollIntoView()` on a specific row works, since it may not be mounted yet.
- **`overscan`** controls how many extra rows render outside the visible area — too low causes flicker/blank flashes on fast scroll, too high defeats the purpose. Start around 5–10 and tune based on real scroll speed testing.
- Don't virtualize short lists (under ~50–100 items depending on row complexity) — the overhead and lost simplicity isn't worth it below the threshold where it actually helps; verify with profiling rather than applying it by default.
