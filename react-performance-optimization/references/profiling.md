# Profiling — Find the Real Bottleneck First

Always start here if the user hasn't already pinpointed the slow component or interaction. There are two distinct classes of "slow," and they need different tools.

## Class 1: Slow interaction / re-render (typing, clicking, toggling feels laggy)

Use the **React DevTools Profiler** (browser extension, "Profiler" tab).

1. Open the Profiler tab, click the record (circle) button
2. Perform the slow interaction in the app (type a character, click the toggle, etc.)
3. Stop recording
4. Read the **flame graph**:
   - Each bar is a component; width = render duration
   - Yellow/orange/red bars = comparatively expensive renders — investigate these first
   - Gray bars = component did not re-render that commit (good)
5. Click a slow component and check "Why did this render?" (enable the setting via the gear icon if not visible) — it tells you exactly which prop or state changed
6. Use the **ranked** view to see the single slowest component in a commit at a glance

**What you're looking for:**
- A component re-rendering that has no reason to (its props/state didn't meaningfully change) → rendering/memoization issue, see `rendering-state.md` and `memoization.md`
- A component that legitimately needs to update but the computation inside it is expensive → memoize the expensive value, see `memoization.md`
- Many components re-rendering together from one state change → state is colocated too high, or a context value changed → see `rendering-state.md`

Command to remember for the user:
```bash
# React DevTools as a standalone (useful outside the browser, e.g. React Native or headless)
npx react-devtools
```

## Class 2: Slow initial load / large bundle

Use **browser DevTools Performance/Network tabs**, **Lighthouse**, and a **bundle analyzer** — the Profiler tab won't help here since the problem is before React even mounts.

### Lighthouse (Chrome DevTools → Lighthouse tab, or `npx lighthouse <url>`)
Look at:
- **Largest Contentful Paint (LCP)** — target < 2.5s
- **Total Blocking Time (TBT)** — large JS bundles parsing/executing on the main thread block this
- **JS bundle size flags** — Lighthouse explicitly calls out unused/oversized JS

### Bundle composition — Vite projects (Bas's stack)
```bash
npm install -D rollup-plugin-visualizer
```
```ts
// vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer'

export default defineConfig({
  plugins: [
    react(),
    visualizer({ open: true, gzipSize: true, brotliSize: true }),
  ],
})
```
Run `npm run build` — it opens an interactive treemap of what's actually in each chunk. Look for:
- A single dependency dominating the main chunk that could be lazy-loaded or swapped for a lighter alternative
- Duplicate copies of a library (version mismatch across dependencies)
- Entire routes/features bundled into the initial chunk instead of split — see `code-splitting.md`

### Bundle composition — webpack/CRA projects
```bash
npx source-map-explorer build/static/js/*.js
# or
npm install -D webpack-bundle-analyzer
```

## Class 3: Janky scrolling on long lists

Use the **Performance tab** (not Profiler) — record while scrolling, look at the frame rate. Frames taking >16ms (target 60fps) show up as long tasks. If the flame graph during scroll shows hundreds of row components rendering per frame, that's the signal for virtualization — see `references/virtualization.md`.

## When NOT to optimize

- The Profiler shows the actual render/commit taking single-digit milliseconds — not worth touching regardless of how it "feels"
- The interaction is slow because of a network request (API call), not rendering — that's a data-fetching/caching problem, not a render-performance problem
- The component only renders rarely (e.g., once on mount, or on an infrequent user action) — optimizing render cost there has near-zero user-facing impact
