# Responsive Anti-Patterns — Catalog & Fixes

Each anti-pattern has: detection (regex / visual symptom), why it breaks, fix.

---

## A1. Missing or broken viewport meta

**Detect:** No `<meta name="viewport">` in `<head>`, or `width` is anything except `device-width`.

**Symptom:** Mobile browsers render at 980px logical width and shrink-fit. Fluid CSS frozen. Tap-targets sub-pixel. `100vw` broken.

**Fix:**

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

`viewport-fit=cover` REQUIRED for `env(safe-area-inset-*)` to resolve to non-zero on notched / Dynamic-Island devices.

---

## A2. Disabled pinch-zoom (WCAG 1.4.4 VIOLATION)

**Detect:** `maximum-scale=`, `minimum-scale=`, or `user-scalable=no` in viewport meta.

**Symptom:** Low-vision users physically cannot zoom. Lighthouse and axe-core flag automatically.

**Fix:** Remove the attributes. If suppressing to stop iOS input zoom — fix root cause (A4) instead.

---

## A3. Fixed pixel width / `min-width` lock-out

**Detect:**

- `width:\s*\d{3,}px` on containers
- `min-width:\s*\d{3,}px` on layout elements

**Symptom:** Element refuses to shrink, blows out body, horizontal page scroll on viewports narrower than the value. `min-width` is the silent killer — nothing visually overflows at desktop sizes.

**Fix:**

```css
.container { width: 100%; max-width: 75rem; margin-inline: auto; }
.card      { min-width: 0; inline-size: 100%; }
/* min-width: 0 is MANDATORY on flex/grid children that wrap long content */
```

---

## A4. Inputs with `font-size < 16px` (iOS auto-zoom)

**Detect:** Selectors matching `input`, `textarea`, `select`, `[contenteditable]` with `font-size` < 16px.

**Symptom:** iOS Safari zooms viewport on focus, doesn't zoom back. Still reproduces iOS 18 / iPhone 16 as of late 2025.

**Fix (simple):**

```css
input, textarea, select { font-size: 16px; }
```

**Fix (if 14px visual mandatory):**

```css
@supports (-webkit-touch-callout: none) {
  input, textarea, select {
    font-size: 16px;
    transform: scale(0.875);
    transform-origin: left top;
  }
}
```

Never fix this with `maximum-scale=1` — see A2.

---

## A5. `100vh` on mobile

**Detect:** `height:\s*100vh` or `min-height:\s*100vh` on hero/full-screen elements.

**Symptom:** `vh` is calculated against the largest viewport (chrome retracted). With URL bar visible at load, the element is taller than screen. iOS 18 still doesn't update `window.innerHeight` when address bar expands.

**Fix:**

```css
.hero {
  height: 100vh;       /* fallback for very old browsers */
  height: 100svh;      /* small viewport — stable, no jank */
  min-height: 100dvh;  /* if you need fill */
}
```

- `svh` = chrome visible — best for hero, no jank
- `lvh` = chrome hidden — immersive full-bleed
- `dvh` = dynamic — NEVER animate to/from `dvh`, causes jitter

Baseline since June 2025.

---

## A6. Tap targets < 44 CSS px

**Detect:** Interactive elements (button, a, [role=button], input[type=checkbox/radio/submit]) with width/height < 44px on mobile widths.

**Symptom:** Fails WCAG 2.2 SC 2.5.8 (24×24 minimum). 25%+ mis-tap rate per Apple's research.

**Fix:**

```css
.icon-btn {
  inline-size: 44px;
  block-size: 44px;
  display: inline-grid;
  place-items: center;
}
/* Or extend hit area without growing visual: */
.icon-btn { position: relative; }
.icon-btn::before { content: ""; position: absolute; inset: -10px; }
```

---

## A7. Tables without overflow wrapper

**Detect:** `<table>` not wrapped in any element with `overflow-x`, OR wrapped element lacks `role="region"` + `tabindex="0"`.

**Symptom:** Wide table forces document width to its intrinsic content width → body-level horizontal scroll.

**Fix (with a11y):**

```html
<div role="region" aria-labelledby="tbl-cap" tabindex="0" class="table-wrap">
  <table>
    <caption id="tbl-cap">Q4 results</caption>
    ...
  </table>
</div>
```

```css
.table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.table-wrap:focus-visible { outline: 2px solid currentColor; }
```

`tabindex="0"` + `role="region"` exposes scroll area to keyboard + AT.

---

## A8. Non-fluid images

**Detect:** `<img>` without `max-width: 100%` rule applying.

**Symptom:** Image renders at intrinsic pixel width, pushing viewport wider.

**Fix (global rule):**

```css
img, svg, video, canvas {
  max-inline-size: 100%;
  block-size: auto;
}
```

Keep `width`/`height` HTML attrs — browser uses them for CLS-preventing aspect ratio reservation.

---

## A9. `position: fixed` ignoring mobile chrome

**Detect:** `position: fixed; bottom: 0` (or `inset: auto 0 0 0`) without `env(safe-area-inset-bottom)` consideration.

**Symptom:** Sits under iOS home indicator / Android nav gestures.

**Fix:**

```css
.bottom-nav {
  position: fixed;
  inset: auto 0 0 0;
  padding-block-end: max(12px, env(safe-area-inset-bottom));
}
```

Note: sticky inside `overflow: auto` or transformed ancestors breaks on iOS Safari — bug as of iOS 18.

---

## A10. Sidebars always rendered open

**Detect:** `aside`, `nav`, `.sidebar` rendered with fixed width and no responsive collapse.

**Symptom:** Permanently steals viewport width on mobile.

**Fix:**

```css
.layout { display: grid; grid-template-columns: minmax(0, 1fr); }
@media (min-width: 64rem) {
  .layout { grid-template-columns: 18rem minmax(0, 1fr); }
}
```

For mobile sidebar reveal, use `<dialog>` + `showModal()` — see `menus-drawers.md`.

---

## A11. Hard-coded `px` everywhere

**Detect:** `font-size`, `padding`, `margin` in `px` on typography and layout elements.

**Symptom:** User text-size preferences and zoom >200% can't rescale UI proportionally. Defeats WCAG 1.4.4.

**Fix:**

```css
:root { font-size: 100%; } /* respect user default */
.heading {
  font-size: clamp(1.5rem, 1rem + 2vw, 2rem);
  padding-block: 1.5rem;
  padding-inline: 1rem;
}
```

`rem` for typography & spacing, `clamp()` for fluid scaling, `em` for component-local rhythm.

---

## A12. `text-align: justify` on narrow widths

**Detect:** `text-align: justify` without media query restricting to wide screens.

**Symptom:** Rivers (vertical gaps). Severely harms legibility on mobile, dyslexia-affecting.

**Fix:**

```css
p { text-align: start; hyphens: auto; }
@media (min-width: 60rem) {
  .prose p { text-align: justify; hyphens: auto; }
}
```

---

## A13. Horizontal scroll from transforms / negative margins

**Detect:** `margin-left:\s*-?\d+vw`, `width:\s*100vw`, `transform.*scale\s*\(\s*[\d.]+\s*\)` on full-bleed sections.

**Symptom:** `100vw` includes scrollbar width on desktop. Transforms create new containing blocks that escape parent clipping.

**Fix:**

```css
html { overflow-x: clip; }   /* `clip` does NOT create scroll container, unlike `hidden` */
.full-bleed {
  width: 100%;
  margin-inline: calc(50% - 50cqw); /* container-relative */
}
```

`overflow: clip` (Baseline) preferred — `overflow: hidden` on `<body>` breaks `position: sticky` in descendants.

---

## A14. `overflow: hidden` on body as "fix"

**Detect:** `body { overflow-x: hidden }` or `html { overflow-x: hidden }`.

**Symptom:** Symptom-masking. Disables `position: sticky` everywhere below. Breaks scroll restoration. Doesn't fix root overflow.

**Fix:** Find offender via `* { outline: 1px solid red; }`. Fix root cause (A3 / A8 / A13). If you MUST clip, use `overflow-x: clip` on `html`.

---

## A15. Hover-only interactions on touch

**Detect:** `:hover` reveals interactive content (menus, tooltips with actions) without a `:focus-within` or click/tap fallback.

**Symptom:** Touch devices simulate hover on first tap → double-tap with no affordance. Stylus / keyboard blocked.

**Fix:**

```css
.menu:has(:focus-within) .submenu,
.menu:hover .submenu { display: block; }
@media (hover: none) and (pointer: coarse) {
  .menu .submenu { /* always show or aria-expanded-driven */ }
}
```

Gate hover-only effects: `(hover: hover) and (pointer: fine)`.

---

## A16. Mobile-only z-index regressions

**Detect:** Mobile menu/dialog visually behind sticky header or under iOS URL bar overlay.

**Symptom:** New stacking contexts created by `transform`, `opacity < 1`, `filter`, `will-change`, `backdrop-filter` reset z-index inside themselves.

**Fix:** Use `<dialog>` + `::backdrop` for top-layer rendering (escapes all stacking contexts). Otherwise audit ancestors for stacking-context properties.

---

## A17. `<meta http-equiv="X-UA-Compatible">` (legacy)

**Detect:** `<meta http-equiv="X-UA-Compatible" content="IE=edge">`.

**Symptom:** Targets IE / pre-Chromium Edge. Adds noise, no effect in 2026.

**Fix:** Remove.

---

## Lint-checkable rules (for static scan script)

These three regex checks catch ~70% of responsiveness sins:

1. `width:\s*\d{3,}px` on layout containers without an accompanying `max-width: 100%`
2. `maximum-scale=1|user-scalable=no` in viewport meta
3. `input|textarea|select.*font-size:\s*(0\.\d|1[0-5])(px|rem)` (inputs with < 16px font)

Plus structural:
4. No `<meta name="viewport">` in `<head>`
5. `<table>` not wrapped in `overflow-x:auto` ancestor
6. `100vh` without `dvh`/`svh` fallback
7. `position:\s*fixed.*bottom` without `safe-area-inset-bottom`
8. Sidebar with `width:\s*\d+(px|rem)` and no media query collapsing it

---

## Sources

- web.dev/articles, defensivecss.dev
- ishadeed.com responsive guide
- css-tricks.com (responsive tables, fluid typography)
- savvy.co.il, aravishack.medium (dvh/svh/lvh)
- W3C WAI WCAG 2.2 (target-size-minimum, viewport-zoom)
