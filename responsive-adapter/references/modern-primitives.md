# Modern CSS Responsive Primitives — 2026 Reference

## 1. `clamp(min, fluid, max)`

**Browser support:** Baseline Widely available since April 2020. ~97-98%.

**Recipe:**
```css
html { font-size: clamp(1rem, 0.875rem + 0.5vw, 1.25rem); }
h1 { font-size: clamp(1.75rem, 1.25rem + 2.5vw, 3.5rem); line-height: 1.1; }
.section {
  padding-block: clamp(2rem, 5vw, 6rem);
  padding-inline: clamp(1rem, 4vw, 3rem);
}
```

**Pitfalls:**
- Pure viewport-only preferred (`clamp(1rem, 5vw, 2rem)`) breaks WCAG 1.4.4 (zoom to 200%). Always mix `rem` into middle.
- If `max < min`, browsers use `min` and silently ignore — easy to miss.
- WCAG rule: `max ≤ 2.5 × min`.

**Use:** typography, padding, gaps, border-radius, gradient stops, widths.
**Don't:** icon sizes that must stay pixel-perfect, grid cell counts.

---

## 2. `min()` and `max()` for container widths

**Browser support:** Baseline Widely available since April 2020. ~97-98%.

**Recipe — page wrapper:**
```css
.wrapper {
  width: min(100% - 2rem, 1200px);
  margin-inline: auto;
}

.sidebar { flex-basis: max(30%, 280px); }

/* Full-bleed inside constrained parent */
.full-bleed {
  width: min(100vw, 100%);
  margin-inline: calc(50% - 50vw);
}
```

**Pitfall:** `min()` picks **smaller** at compute time — `min(80%, 780px)` means "whichever is smaller now". Acts opposite to `min-width`.

**Use:** classic max-width + padding wrapper in one line, button/modal constraints.
**Don't:** when you need hard breakpoints.

---

## 3. Container queries

**Browser support:** Baseline Widely available since February 2023. Size queries ~94-95%. Style queries Chrome/Edge only. Scroll-state queries Chrome 133+.

**Recipe:**
```css
.card {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card__layout { grid-template-columns: 1fr 2fr; }
  .card__title { font-size: clamp(1.25rem, 4cqi, 1.75rem); }
}
```

**Pitfalls:**
- `container-type: inline-size` creates layout containment — container can no longer be sized by children's intrinsic widths.
- Don't put `container-type` on `html`/`body` — breaks `vh`-based child layouts.
- Container query units (`cqi`, `cqb`, `cqw`, `cqh`) without eligible container ancestor **silently fall back to small viewport**.
- Always pair query units with explicit `container-type` ancestor.

**Use:** reusable components in varying contexts (cards in sidebar vs main).
**Don't:** page-level layout shifts — use media queries (cheaper, no containment).

---

## 4. `dvh`, `svh`, `lvh`

**Browser support:** Baseline Widely available. Safari 15.4+ (March 2022), Chrome 108+ (Nov 2022), Firefox 101+. ~95%+.

- `svh` = browser UI fully expanded (smallest)
- `lvh` = UI retracted (largest)
- `dvh` = changes live as UI shows/hides

**Recipe:**
```css
.hero { min-height: 100svh; }
.mobile-menu { position: fixed; inset: 0; height: 100dvh; }

/* Fallback chain */
.fullscreen {
  height: 100vh;
  height: 100dvh;
}
```

**Pitfalls:**
- `dvh` triggers reflows as address bar animates — never use on `font-size` or anything causing layout shift.
- **On-screen keyboard does NOT shrink viewport** — `100dvh` ignores it. Use `visualViewport` API in JS or `interactive-widget=resizes-content` meta.
- None of the units account for scrollbar width — `100vw` overflows by scrollbar size on desktops.

**Use:** hero sections (`100svh`), modals, full-screen menus.
**Don't:** typography, animations, body height (breaks scroll on iOS).

---

## 5. `aspect-ratio`

**Browser support:** Baseline Widely available since September 2021. ~97%.

**Recipe:**
```css
.video-embed { aspect-ratio: 16 / 9; width: 100%; }

.avatar {
  aspect-ratio: 1;
  width: clamp(48px, 8vw, 96px);
  border-radius: 50%;
  object-fit: cover;
}

.card__media {
  aspect-ratio: 4 / 3;
}
.card__media img {
  width: 100%; height: 100%; object-fit: cover;
}
```

**Pitfalls:**
- Ignored if **both** dimensions constrained — `width: 200px; height: 200px; aspect-ratio: 16/9` does nothing.
- `min-content`/`max-content` on flex/grid children can win over ratio.
- On `<img>`, intrinsic ratio from width/height attributes takes precedence unless `aspect-ratio: auto 16/9`.

**Use:** media, avatars, square cards.
**Don't:** fixed pixel both axes; text-wrapping elements without `overflow: hidden`.

---

## 6. Grid `auto-fit/auto-fill` + `minmax(min(100%, Npx), 1fr)` (RAM pattern)

**Browser support:** ~98%. Grid auto-fit since 2017, min() since 2020.

**Recipe:**
```css
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr));
  gap: clamp(0.75rem, 2vw, 1.5rem);
}

/* auto-fill — preserves empty tracks */
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 200px), 1fr));
}
```

**Pitfall — THE 320px fix:** Plain `minmax(250px, 1fr)` overflows on viewports < 250px. Wrapping with `min(100%, 250px)` forces min to collapse to 100% of parent at narrow widths.

- `auto-fit` collapses empty tracks — single item stretches full-width.
- `auto-fill` reserves tracks — keeps last item at "card width".

**Use:** card grids, product listings, "fit as many per row".
**Don't:** exact column count at given breakpoints (use container queries).

---

## 7. CSS subgrid

**Browser support:** Baseline Newly available since September 2023. Firefox 71+, Safari 16+, Chrome 117+. ~92-93%.

**Recipe — aligned card internals:**
```css
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
  gap: 1rem;
}

.card {
  display: grid;
  grid-row: span 3;
  grid-template-rows: subgrid;
  gap: 0.5rem;
}
```

**Pitfalls:**
- Subgrid child must first span tracks: `grid-row: span 3` BEFORE `grid-template-rows: subgrid`.
- Subgrid doesn't create implicit tracks; must exist on parent.
- Gap on subgrid child overrides parent's gap for those tracks.

**Use:** card-internal alignment, form labels with inputs, footer columns sharing baseline.
**Don't:** independent inner layouts — use nested grid.

---

## 8. Logical properties

**Browser support:** Baseline Widely available. ~96%.

**Recipe:**
```css
.container {
  padding-inline: clamp(1rem, 4vw, 3rem);
  padding-block: 2rem;
  margin-inline: auto;
  max-inline-size: 65ch;
}

.toast {
  position: fixed;
  inset-block-end: 1rem;
  inset-inline-end: 1rem;
}

.callout {
  border-inline-start: 4px solid currentColor;
  padding-inline-start: 1rem;
}
```

**Pitfalls:**
- Mixing physical (`padding-left`) and logical (`padding-inline-start`) creates cascade chaos.
- RTL flips inline-start to right; block-start stays top unless `writing-mode: vertical-*`.

**Use:** any new code. RTL-friendly, future-proof.
**Don't:** patching legacy where mixing creates risk — convert in one pass.

---

## 9. `:has()` selector

**Browser support:** Baseline Newly available December 2023. ~94%.

**Recipe:**
```css
.grid:has(> :nth-child(4)) { grid-template-columns: repeat(2, 1fr); }

.form-row:has(input:required) label::after { content: " *"; color: red; }

body:has(dialog[open]) { overflow: hidden; }

.card:has(img) { grid-template-columns: 1fr 2fr; }
.card:not(:has(img)) { grid-template-columns: 1fr; }

@supports selector(:has(*)) { /* :has() rules here */ }
```

**Pitfalls:**
- `:has()` is unforgiving — invalid selectors inside invalidate the whole rule.
- Performance fine for typical DOM, but `*:has(...)` or deep chains can degrade in large apps.

**Use:** quantity queries, state-based layout, parent-conditional styling without JS.
**Don't:** complex chains that become unmaintainable.

---

## 10. `@supports`

**Browser support:** Baseline Widely available since 2015. ~99%. `@supports selector()` since 2022.

**Recipe:**
```css
@supports (aspect-ratio: 1) { .media { aspect-ratio: 16 / 9; } }
@supports selector(:has(*)) { .card:has(img) { grid-template-columns: 1fr 2fr; } }
@supports not (display: grid) { .layout > * { display: inline-block; width: 32%; } }
@supports (display: grid) and (gap: 1rem) { .layout { display: grid; gap: 1rem; } }
```

**Pitfalls:**
- Only tests **syntax** parsing — can't detect bugs in feature.
- `@supports not (X)` true in browsers without `@supports` itself AND those without X.

**Use:** leading-edge CSS (View Transitions, anchor positioning, `@scope`).
**Don't:** Baseline Widely available features — dead code.

---

## Sources

- ishadeed.com (Ahmad Shadeed) — definitive guides on all primitives
- web.dev/articles/baseline-in-action-* — Baseline features
- web.dev/patterns/layout/repeat-auto-minmax — RAM pattern
- joshwcomeau.com/css/has/ — `:has()` practical guide with perf data
- MDN refs for each property
