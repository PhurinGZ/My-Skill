# Platform Conventions & Stack Notes

## iOS (Apple Human Interface Guidelines)

- **Touch targets**: minimum 44×44pt, including secondary/icon-only actions. Visual size can be smaller than the tappable area — extend the hit area with padding rather than shrinking the target.
- **Navigation**: tab bar for apps with multiple top-level sections (not a hamburger menu — it's an Android/web pattern that hides discoverability on iOS); `NavigationStack`/push navigation for drill-down flows; preserve the edge swipe-back gesture even with a custom back button.
- **Sheets & modals**: avoid stacking a sheet on top of a sheet — use in-sheet navigation instead. Every sheet needs a clear, obvious dismissal (swipe down or explicit close).
- **Typography**: SF Pro, Dynamic Type–aware; body text minimum 17pt; don't hardcode font sizes — use text styles so layouts reflow correctly at larger accessibility text sizes without clipping.
- **Icons**: SF Symbols as the default icon system — they scale with Dynamic Type, adapt to weight/scale settings, and align to SF Pro automatically, which a custom icon set won't do for free.
- **Color**: use semantic colors (`label`, `systemBackground`, etc.) rather than hardcoded hex so light/dark mode both work without separate theming logic.
- **Spacing**: 8pt grid with 4pt subdivisions is the de facto convention (not an explicit Apple mandate, but near-universal in practice).
- **Avoid**: permission requests at first launch before context justifies them; full-screen blocking spinners (prefer skeleton/inline progress); splash screens with logos (the launch screen should mirror the first real screen, not brand-delay it).

## Material Design 3 (Android / cross-platform Material)

- **Touch targets**: minimum 48×48dp.
- **Dynamic color**: M3's signature feature — a full tonal palette (light/dark, multiple roles: primary/secondary/tertiary each with an `on-` pairing for guaranteed readable contrast) generated from a single source color, often extracted from the user's wallpaper on Android but equally usable from a brand color for a web/app theme.
- **Elevation**: M3 favors tonal surface color shifts over heavy drop shadows to indicate elevation — a component gets a lighter/more prominent tone as it "rises," with shadow as a secondary cue rather than the primary one.
- **Typography**: a defined type scale from `display` down to `label` sizes (display-large/medium/small, headline, title, body, label) — use the scale rather than ad hoc sizes so hierarchy stays consistent.
- **Shape**: each component has a default corner-radius family (small/medium/large) that can be themed as a set, not per-component.
- **Components**: buttons, cards, text fields, chips, navigation bar/rail/drawer (choose nav pattern by breakpoint — bar for mobile, rail for tablet, drawer for desktop/wide).

## Responsive web breakpoints

No single official standard exists, but the values below are the de facto convention shared across Tailwind, Bootstrap, and most design tools — using them means the layout matches what every other modern web product already trained the user to expect:

| Breakpoint | Width | Typical target |
|---|---|---|
| `xs` (base) | ~375px | Small mobile |
| `sm` | 640px | Large mobile / small tablet portrait |
| `md` | 768px | Tablet portrait |
| `lg` | 1024px | Tablet landscape / small laptop |
| `xl` | 1280px | Desktop |
| `2xl` | 1536px | Large desktop |

Design and test at minimum: 375px, 768px, 1024px, and 1440px. Mobile-first (base styles for the smallest viewport, then progressively enhance with `min-width` media queries) is the default approach — it forces content prioritization instead of cramming a desktop layout down.

## Stack-specific implementation notes

### React + Tailwind
Utility-first; keep components small and composition-driven. Use Tailwind's config for the actual design tokens (colors, spacing, type scale) rather than arbitrary values (`w-[123px]`) sprinkled through markup — arbitrary values defeat the point of having a token system. Co-locate hover/focus/dark-mode variants (`hover:`, `focus-visible:`, `dark:`) directly on the element rather than separate stylesheets.

### Next.js
Same component conventions as React; additionally decide Server vs Client Components deliberately — interactive/stateful UI (forms, anything with `useState`/`useEffect`) needs `"use client"`, while static/data-fetching shells should stay server components for performance. Use the built-in `<Image>` component for automatic responsive sizing and layout-shift prevention rather than raw `<img>`.

### Vue
Prefer the Composition API (`<script setup>`) for new components. Scoped styles (`<style scoped>`) or a utility framework (Tailwind works the same way as in React) rather than global CSS bleed. Use `v-show` vs `v-if` deliberately — `v-show` for frequently toggled elements (cheaper re-toggle, stays in the DOM), `v-if` for rarely-shown or conditionally-expensive content.

### Svelte
Leans on scoped-by-default component styles — you often need less utility-class boilerplate than React/Vue for the same result. Reactive declarations (`$:`) replace most `useEffect`-style derived-state code; don't reach for a store when local component state is enough.

### SwiftUI
Native iOS — apply the iOS HIG section above directly. Use `NavigationStack` for drill-down flows, system-provided modifiers for Dynamic Type and Dark Mode rather than hardcoded values, and SF Symbols via `Image(systemName:)` instead of custom icon assets wherever a suitable symbol exists.

### Flutter
Material widgets by default (`ThemeData` with M3 enabled: `useMaterial3: true`) for Android-first apps; use `Cupertino*` widgets when targeting an iOS-native feel. Keep a single `ThemeData` as the source of truth for colors/type/shape rather than styling widgets ad hoc, so theming (including dark mode) stays centralized.

### HTML/CSS (framework-free)
CSS custom properties (`--color-primary`, `--space-4`, etc.) as the token layer, consumed everywhere via `var()` — this is what gives you a single place to adjust the whole system, similar to what a framework's config file provides. Prefer modern layout primitives (`grid`, `flexbox`, `clamp()` for fluid type) over fixed-pixel layouts and media-query-only responsiveness.
