---
name: react-performance-optimization
description: Expert guidance for diagnosing and fixing slow React apps — unnecessary re-renders, large bundles, janky lists, and slow initial loads. Covers React DevTools Profiler workflow, React.memo/useMemo/useCallback, the React Compiler (React 19+), state/context restructuring, code splitting with lazy/Suspense, and list virtualization. Use this skill whenever the user reports a React app or component feels slow or laggy, asks to "optimize" or "speed up" a React component/page, mentions unnecessary re-renders, large bundle size, slow initial load, janky scrolling on long lists, or wants a React DevTools Profiler / Lighthouse / Core Web Vitals result explained. Trigger even if they don't say "performance" explicitly — e.g. "this list stutters when I scroll", "the dashboard takes forever to load", "why does typing in this input lag", "the bundle is huge".
---

# React Performance Optimization

Expert guidance for optimizing React application performance through profiling, memoization, code splitting, virtualization, and state/rendering architecture — built for React 18 and 19, on any bundler (Vite, webpack, Next.js).

Adapted from the public `react-performance-optimization` skill pattern (nickcrew/claude-ctx-plugin) and cross-checked against the official React docs (react.dev) as of July 2026.

## The Golden Rule: Measure, Don't Guess

Never apply an optimization technique without first confirming it addresses a *measured* bottleneck. Premature memoization adds code complexity, hurts readability, and can occasionally make things slower (memo comparison overhead, stale-closure bugs). The workflow is always:

1. **Profile** — find the actual slow component/interaction (React DevTools Profiler, or Chrome Performance/Lighthouse for load-time issues)
2. **Diagnose** — classify the bottleneck using the table below
3. **Fix** — apply the narrowest technique that addresses it
4. **Re-measure** — confirm the fix actually helped; revert if it didn't

Read `references/profiling.md` first if the user hasn't already identified the bottleneck — don't jump straight to "wrap it in useMemo."

## First, Check: Is React Compiler Available?

This changes almost everything about which techniques apply. **React Compiler shipped stable in late 2025** and auto-memoizes components, values, and callbacks at build time — removing most manual need for `useMemo`/`useCallback`/`React.memo`.

- **Project is React 19+ with `babel-plugin-react-compiler` (or `eslint-plugin-react-hooks` v6+/rc flag) enabled**: Do NOT recommend manual `useMemo`/`useCallback`/`React.memo` for ordinary render-cost optimization — the compiler already does this, and hand-written memoization can conflict with or shadow its analysis. Point manual memoization only at things the compiler can't do: referential stability crossing a memo/effect-dependency boundary the compiler doesn't see, or explicit skip logic. Optimization work shifts to architecture: server/client boundary, data fetching waterfalls, code splitting, virtualization. Verify current compiler config/status by checking the project's `vite.config`/`babel.config`/`.eslintrc` for `babel-plugin-react-compiler` — don't assume.
- **Project is React 18 (like most existing Vite + TS apps, and Bas's current stack)**: Manual memoization is still the primary tool. `references/memoization.md` applies in full. Compiler adoption on React 18 is not supported — it requires React 19's APIs at runtime for some optimizations, so don't suggest installing it as a quick fix on an 18 codebase without discussing the upgrade first.

Always confirm which situation applies before advising — check `package.json` for the React version and search for compiler config, rather than assuming.

## Diagnose → Fix Quick Reference

| Symptom | Likely cause | Reference file |
|---|---|---|
| Typing in an input is laggy; a component re-renders on every keystroke elsewhere on the page | Unnecessary re-renders from state placed too high, unstable prop references, or missing memoization (React 18) | `references/rendering-state.md`, `references/memoization.md` |
| React DevTools Profiler shows many components re-rendering when only one value changed | Context value not memoized; state colocated too high; missing `key` splitting | `references/rendering-state.md` |
| Initial page load is slow; Lighthouse flags large JS bundle | Everything bundled into one chunk; no route/component-level splitting | `references/code-splitting.md` |
| Scrolling a list/table of 500+ rows is janky | All rows mounted and rendered at once (no windowing) | `references/virtualization.md` |
| Expensive calculation (sort/filter/aggregate) reruns every render | Missing memoization of derived values, or derived value recomputed instead of memoized | `references/memoization.md` |
| Not sure where the slowness actually is yet | — start here | `references/profiling.md` |

Load only the reference file(s) relevant to the diagnosed symptom — don't read all of them into context for a single-issue fix.

## Core Techniques (summary)

- **Memoization** (React 18, or targeted React 19 cases) — `React.memo` for components, `useMemo` for expensive derived values, `useCallback` for function references passed to memoized children or effect dependencies. Full rules and pitfalls in `references/memoization.md`.
- **State & rendering architecture** — colocate state as close as possible to where it's used, split contexts by update frequency, lift state down instead of up, avoid creating new object/array/function literals inline as props to memoized children. Details in `references/rendering-state.md`.
- **Code splitting** — `React.lazy` + `Suspense` for route- and component-level chunks, dynamic `import()`, prefetch/preload hints, analyzing bundle composition with `rollup-plugin-visualizer` (Vite) or `source-map-explorer` (webpack/CRA). Details in `references/code-splitting.md`.
- **Virtualization** — render only visible rows for long lists/tables/grids using `@tanstack/react-virtual` or `react-window`. Details in `references/virtualization.md`.

## Anti-Patterns — Flag These When Reviewing Code

- Wrapping every component in `React.memo` "just in case" without profiling first (adds comparison overhead, and is actively counterproductive once React Compiler is present)
- `useMemo`/`useCallback` on trivial computations or on values not passed to memoized children/effect deps — pure overhead, no benefit
- Defining a new object/array/inline function literal directly in JSX props of a `memo`-wrapped child (`<Child style={{color: 'red'}} />`) — defeats the memoization every time
- Storing derived data in state and syncing it with `useEffect` instead of just computing it during render (or memoizing the computation)
- One giant context provider at the app root holding frequently-changing values — causes wide re-render blast radius; split contexts by change frequency instead
- Rendering full unvirtualized lists for data that can grow past ~100–200 rows
- Optimizing before profiling — always ask "did you confirm this is the actual bottleneck?" if the user jumps straight to a fix

## Verification Checklist (after applying a fix)

1. Re-run the React DevTools Profiler recording for the same interaction — confirm render count/duration actually dropped
2. For bundle-size fixes, re-check bundle analyzer output and/or Lighthouse performance score
3. For list virtualization, confirm scroll performance in the browser's Performance panel (target 60fps / <16ms per frame)
4. Check for regressions: stale closures from `useCallback` deps, broken keyboard nav or accessibility from virtualization, layout shift from lazy-loaded chunks
5. If the fix didn't measurably help, revert it — don't leave dead-weight memoization in the codebase

## Sources

- React docs: react.dev (rendering behavior, `useMemo`/`useCallback`/`memo` API references, React Compiler docs)
- Pattern and reference-file structure adapted from the community `react-performance-optimization` skill (nickcrew/claude-ctx-plugin, via skills.sh)
