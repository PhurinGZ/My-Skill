# Styles, Palettes & Typography

## Style movements

Pick one as a primary direction, or blend two deliberately (e.g., minimalism + one bento-grid section). Don't pick a style because it's trendy in AI output right now (see `frontend-design`'s calibration notes on the three over-used AI defaults) — pick it because it matches the product and audience below.

| Style | Description | Best for | Common failure mode |
|---|---|---|---|
| Swiss / Minimalism | Grid-driven, generous whitespace, restrained type scale, little ornament | Enterprise apps, docs, dashboards | Becomes bland without a strong type or grid decision to carry it |
| Neumorphism | Soft extruded/inset shadows on a matching background | Wellness, meditation, single-purpose controls | Fails contrast badly if not paired with a separate high-contrast text layer |
| Glassmorphism | Frosted-glass translucency, blur, thin light borders | Modern SaaS, overlays, modals | Illegible over busy backgrounds; needs a contrast-safe fallback |
| Brutalism / Neubrutalism | Raw structure, visible grid lines, bold flat color, thick borders, no border-radius | Portfolios, indie/Gen-Z brands | Reads as "unfinished" to non-target audiences (enterprise, healthcare) |
| Bento grid | Modular card grid of varying sizes, each cell one idea | Feature showcases, dashboards, product pages | Becomes visual noise past ~9-12 cells without a clear hierarchy |
| Dark mode (OLED-aware) | True near-black background, restrained accent color, elevated surfaces via lightness not shadow | Dev tools, media/streaming, night use | Text contrast and pure-black banding if not tested on real OLED |
| Soft UI / elevated cards | Rounded cards, soft shadow elevation, muted palette | Modern enterprise SaaS | Generic if the palette isn't specific to the brand |
| Editorial / magazine grid | Multi-column text grid, hairline rules, strong type hierarchy | Blogs, news, long-form content | Needs real (not lorem ipsum) content to justify the structure |
| Data-dense / functional | High information density, monospace for numbers, minimal chrome | Trading, analytics, ops dashboards | Overwhelming if hierarchy and grouping aren't disciplined |
| Skeuomorphic accents | Selective realistic texture/material cues (not full 2000s skeuomorphism) | Premium products, music/creative tools | Dated fast if overused across the whole UI rather than one signature element |
| Maximalist / Gen-Z | Saturated color blocks, mixed type weights, playful motion | Youth brands, music, entertainment | Undermines trust for anything financial, medical, or B2B |
| Organic / biophilic | Rounded organic shapes, natural color palette, soft gradients | Wellness, sustainability, health | Can feel unserious for technical/regulated products |
| Sci-fi / HUD | Angular panels, scanlines, glow accents, monospace | Gaming, crypto, developer tools with a "console" feel | Hurts readability and accessibility if overused for body text |
| Accessible-first / inclusive | High contrast by default, large touch targets, plain language, minimal reliance on color | Government, healthcare, education, public services | None when done well — the risk is treating it as optional rather than default |

## Color palette construction

Build a system, not a swatch:

1. **Neutral scale** — 8–10 steps from background to text, usually a very slightly warm or cool gray (pure #000/#FFF reads harsh). This carries ~80% of the UI.
2. **Primary** — one brand color, used for primary actions and key emphasis. Pick a hue, then generate a full lightness ramp (50–900) so you have a hover/active/disabled variant without inventing ad hoc colors later.
3. **Accent** (optional) — a second color for a specific purpose (a highlight, a secondary CTA) — resist adding a third or fourth "just in case."
4. **Semantic set** — success, warning, error, info — chosen for clear differentiation from each other and from the primary, and each checked for contrast against both light and dark backgrounds.
5. **Contrast-check every pairing you'll actually use** (text on background, icon on fill, border on background) against the ratios in `ux-and-accessibility.md` — don't assume a palette that looks fine on a design tool's white canvas will hold up against a dark or colored surface.

### Starter palettes by mood

These are original starting points, not a fixed catalog — adjust hue/saturation to the actual brand rather than using them verbatim.

| Mood | Neutral | Primary | Accent | Notes |
|---|---|---|---|---|
| Calm / wellness | Warm gray `#F7F5F2` → `#2B2926` | Sage `#5B8A72` | Warm clay `#C98A6B` | Low saturation throughout; avoid neon |
| Trustworthy fintech | Cool gray `#F5F7FA` → `#1A1F2B` | Deep blue `#2451B8` | Teal `#16A394` | Avoid purple/pink AI-gradient defaults; keep contrast crisp |
| Premium / luxury | Near-black `#0E0E10` → `#F5F3EE` | Muted gold `#B8944F` | Deep burgundy `#5A1F2B` | Restraint matters more than saturation here |
| Playful / consumer | Off-white `#FAFAF7` → `#23211E` | Coral `#FF5A5F` | Sunny yellow `#FFC53D` | High energy — pair with generous whitespace so it doesn't overwhelm |
| Developer / technical | True dark `#0D1117` → `#E6EDF3` | Electric blue `#4C8DFF` | Lime `#9EF01A` (sparingly) | Monospace-friendly; keep accent usage rare and purposeful |
| Healthcare / clinical | Cool white `#F4F8F9` → `#1E2A2E` | Medical blue `#1D6FA5` | Soft green `#3FA772` | Prioritize the accessible-first row above all else |

## Typography pairing

**Method:** pick a display face with real personality used sparingly (headlines, hero, key numbers) and a body face optimized for reading at small sizes, then check they don't compete — either contrast in style (serif display + grotesque body) or share enough structure to feel intentional rather than accidental. Set an actual type scale (e.g., a 1.25 or 1.333 ratio from a base of 16px) instead of picking sizes ad hoc, and don't skip a utility/mono face for data, code, or captions if the product needs one.

### Example pairings by mood

| Mood | Display | Body | Utility/mono |
|---|---|---|---|
| Editorial / elegant | Fraunces or Playfair Display | Inter or Source Sans 3 | JetBrains Mono |
| Modern SaaS | Space Grotesk | Inter | IBM Plex Mono |
| Warm / approachable | Fredoka or Recoleta | Nunito Sans | — |
| Technical / developer | Söhne or General Sans | Inter | JetBrains Mono or IBM Plex Mono |
| Luxury / premium | Canela or Cormorant Garamond | Neue Montreal or Söhne | — |
| Clinical / accessible-first | System UI stack (San Francisco / Roboto / Segoe UI) | Same as display | Roboto Mono |

Pull actual weights and variable-font ranges from the type foundry or Google Fonts before committing — availability and licensing vary, and a "similar" open-source substitute is often needed for anything not on Google Fonts (e.g., Inter or Public Sans in place of a paid grotesque).
