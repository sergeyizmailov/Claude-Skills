# Admin / Dashboard Responsive Patterns

The hard cases that landing-page advice doesn't cover.

## Sidebar navigation across widths

| Width | Pattern | Width spec | Examples |
|---|---|---|---|
| ≥1240px | Persistent expanded | 240-280px | Linear, Stripe, Notion |
| 905-1239px | Rail (icons + on-hover label) | 72-80px | Vercel collapsed |
| 600-904px | Modal drawer / sheet | Off-canvas | Most SaaS |
| <600px | Hamburger + sheet OR bottom nav | full-width | Stripe mobile |

- Sidebar items: 36px tall on desktop (mouse precision), 44px on tablet for touch.
- Bottom-nav vs hamburger on mobile: bottom nav for ≤5 high-frequency sections (Stripe, banking apps). Hamburger for deep hierarchies (Notion).

```css
.app { display: grid; grid-template-columns: auto 1fr; }
.sidebar { width: 16rem; transition: width 200ms ease; }
.sidebar[data-collapsed] { width: 4rem; }

@media (max-width: 768px) {
  .app { grid-template-columns: 1fr; }
  .sidebar {
    position: fixed;
    inset: 0 auto 0 0;
    transform: translateX(-100%);
    transition: transform 200ms ease;
  }
  .sidebar[data-open] { transform: translateX(0); }
}
```

For accessible mobile drawer, use `<dialog>` — see `menus-drawers.md`.

## Data tables → mobile

Five strategies. Pick based on **how the user reads the data**.

| Strategy | Use when | Implementation |
|----------|----------|----------------|
| Horizontal scroll | Comparison across columns matters (financials) | `overflow-x: auto` + sticky first column |
| Card transformation | Each row independent (users, orders) | `display: block` rows + `data-label` pseudo-content |
| Hide non-essential | Few decorative columns | Priority columns + "show more" toggle |
| Sticky first column | Identifier matters across scroll | `position: sticky; left: 0; bg; z-index` |
| Master-detail | Heavy row detail | Row list → tap → detail view |

### Horizontal scroll + sticky first column (default)
```html
<div role="region" aria-labelledby="tbl-cap" tabindex="0" class="table-wrap">
  <table>
    <caption id="tbl-cap">Orders Q4</caption>
    <thead><tr><th class="sticky-col">ID</th><th>Date</th>...</tr></thead>
    <tbody>
      <tr><td class="sticky-col">#1042</td><td>2026-04-12</td>...</tr>
    </tbody>
  </table>
</div>
```
```css
.table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.table-wrap:focus-visible { outline: 2px solid currentColor; }
.sticky-col {
  position: sticky;
  left: 0;
  background: white;
  z-index: 1;
}
```

### Card transformation (independent rows)
```css
.table-wrap { container-type: inline-size; }

@container (max-width: 640px) {
  table, thead, tbody, th, td, tr { display: block; }
  thead { position: absolute; left: -9999px; } /* visually hide but keep semantics */
  tr {
    border: 1px solid #ddd;
    border-radius: 8px;
    margin-block-end: 1rem;
    padding: 0.75rem;
  }
  td {
    padding-inline-start: 50%;
    position: relative;
    border: 0;
  }
  td::before {
    content: attr(data-label);
    position: absolute;
    inset-inline-start: 0;
    inline-size: 45%;
    font-weight: 600;
  }
}
```
Requires `<td data-label="Date">` on each cell.

Semantics: keep `<table>`. `role="grid"` is for editable spreadsheet-style widgets, NOT display tables.

## Dense forms on mobile

- **Always single column below ~500px.** NN/g studies: 15.4s faster completion.
- **Top labels universally on mobile.** Left labels save space but break tap-flow and i18n.
- **Floating labels** — fine for sparse forms; problematic with autofill (state desyncs).
- **Inline validation** — on blur, not keystroke. Success passive, errors active. Push messages **below** field (not right — gets clipped).
- **Inputs that must NOT shrink:** `<input type="date">` (date picker), `<input type="file">` (system picker), color picker. Set `min-width` and let them push width via container.

```css
.form-grid {
  container-type: inline-size;
  display: grid;
  gap: 1rem;
}
@container (min-width: 36rem) {
  .form-grid { grid-template-columns: 1fr 1fr; }
}

input, textarea, select {
  font-size: 16px;            /* iOS zoom prevention */
  min-block-size: 44px;
  width: 100%;
  padding: 0.5rem 0.75rem;
}
label {
  display: block;             /* top labels on mobile */
  margin-block-end: 0.25rem;
}
```

## Charts / data visualization

- **One question per screen.** Don't shrink desktop dashboard — re-author.
- Limits: bar ≤7 bars, pie ≤7 slices (better: don't use pie), line ≤3 series.
- **Aspect ratio matters more than width.** Force 16:9 or 4:3 via `aspect-ratio`; never shorter than 200px tall.
- Below ~400px container: swap chart type. Stacked-bar → grouped-bar → sparkline → single KPI number.
- Pinch-zoom + swipe-pan beat shrinking.

```css
.chart-wrap {
  container-type: inline-size;
  aspect-ratio: 16 / 9;
  min-block-size: 200px;
}
.chart-wrap svg {
  width: 100%;
  height: 100%;
}

@container (max-width: 25rem) {
  .chart-full { display: none; }
  .chart-sparkline { display: block; }
}
```

## Modal / dialog adaptations

The 2026 consensus: **Drawer-on-mobile, Dialog-on-desktop swap** (Vaul / shadcn `Drawer`):

```tsx
const isDesktop = useMediaQuery("(min-width: 768px)");
return isDesktop ? <Dialog>...</Dialog> : <Drawer>...</Drawer>;
```

| Pattern | Width | Trigger | Dismiss |
|---------|-------|---------|---------|
| Centered modal | ≥768px | Action buttons, edit flows | Esc, backdrop click |
| Bottom sheet | <768px | Action sheets, filters, forms | Swipe down, backdrop |
| Side drawer | Any | Detail views, settings | Esc, backdrop, swipe |

Bottom sheets: `pointer-events: none` on backdrop when scrollable inside; respect `safe-area-inset`.

## Toolbars and action bars

- **Overflow menu collapse:** visible actions sized by container; rest go into `MoreHorizontal` → dropdown. Measure with `ResizeObserver`, not media queries. Radix `DropdownMenu` for overflow.
- **Sticky bottom action bar on mobile:** primary actions (Save, Submit, Pay) glued to bottom with `position: sticky; bottom: 0; padding-block-end: env(safe-area-inset-bottom)`. Desktop puts them inline at form end.

**Anti-pattern:** Floating action button (FAB) on web. Mobile-Android convention that confuses web users — use only if your dashboard has Material Design lineage.

## Layout-aware widget grid (the dashboard primitive)

```css
.dashboard-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
}
.widget { container-type: inline-size; }

@container (min-width: 30rem) {
  .widget__body { grid-template-columns: auto 1fr; }
}
@container (min-width: 45rem) {
  .widget__chart { display: block; }
  .widget__sparkline { display: none; }
}
```

Same widget renders as stacked at 280px, side-by-side at 480px, with chart at 720px+ — driven entirely by its own width, not the viewport.

## Sources
- ishadeed.com/article/css-container-query-guide
- ui.shadcn.com/docs/components/radix/sidebar, Drawer
- m3.material.io/components/navigation-rail/guidelines, navigation-drawer/guidelines
- css-tricks.com/responsive-data-tables (Chris Coyier classic)
- nngroup.com (form best practices)
- vercel.com/blog (Vercel dashboard architecture)
