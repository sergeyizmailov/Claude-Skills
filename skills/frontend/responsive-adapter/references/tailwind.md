# Tailwind Responsive Patterns (v3 + v4)

## Default breakpoint system (mobile-first)

| Prefix | Min width | Class |
|--------|-----------|-------|
| (none) | 0px       | Mobile-first base |
| `sm:`  | 640px     | Large phone / small tablet |
| `md:`  | 768px     | Tablet |
| `lg:`  | 1024px    | Laptop |
| `xl:`  | 1280px    | Desktop |
| `2xl:` | 1536px    | Large desktop |

Mobile-first principle: write base styles first (no prefix), then override at breakpoints upward. Never use `max-*:` breakpoints when `sm:`/`md:`/`lg:` would do — desktop-first cascade is harder to maintain.

## Cross-platform breakpoint override (Material 3-aligned)

In `tailwind.config.js` (v3) or `@theme` (v4):

```js
// tailwind.config.js
module.exports = {
  theme: {
    screens: {
      sm: '390px',   // iPhone baseline
      md: '600px',   // M3 Compact→Medium
      lg: '840px',   // M3 Medium→Expanded
      xl: '1200px',  // M3 Expanded→Large
      '2xl': '1600px' // M3 Large→Extra-large
    }
  }
}
```

```css
/* Tailwind v4 */
@theme {
  --breakpoint-sm: 390px;
  --breakpoint-md: 600px;
  --breakpoint-lg: 840px;
  --breakpoint-xl: 1200px;
  --breakpoint-2xl: 1600px;
}
```

## Container queries (Tailwind v4 native, v3 via `@tailwindcss/container-queries`)

```html
<div class="@container">
  <div class="grid @md:grid-cols-2 @lg:grid-cols-3">
    <!-- adapts to its container, not viewport -->
  </div>
</div>
```

Named containers:
```html
<div class="@container/card">
  <div class="@md/card:grid-cols-2">...</div>
</div>
```

Container query units: `cqi`, `cqw`, `cqh`, `cqb`, `cqmin`, `cqmax`. In Tailwind: `text-[clamp(0.875rem,3cqi,1.5rem)]`.

## Patterns

### Stack → row at breakpoint
```html
<div class="flex flex-col md:flex-row gap-4">
  <div class="flex-1">A</div>
  <div class="flex-1">B</div>
</div>
```

### Grid columns adapt
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
```

### Auto-fit RAM pattern (the 320px-safe grid)
```html
<div class="grid gap-4
            [grid-template-columns:repeat(auto-fit,minmax(min(100%,16rem),1fr))]">
```

### Show/hide based on viewport
```html
<nav class="hidden md:flex">...desktop nav...</nav>
<button class="md:hidden">menu</button>
```

### Fluid spacing & type
```html
<section class="py-[clamp(2rem,5vw,6rem)] px-[clamp(1rem,4vw,3rem)]">
  <h1 class="text-[clamp(2rem,1rem+4vw,4rem)] leading-tight">
```

### Container width pattern
```html
<div class="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8">
```

Or with `min()`:
```html
<div class="mx-auto w-[min(100%-2rem,80rem)]">
```

### Safe-area aware mobile nav
```html
<nav class="fixed inset-x-0 bottom-0
            pb-[max(0.75rem,env(safe-area-inset-bottom))]
            bg-white border-t">
```

### Mobile drawer with `<dialog>`
```html
<dialog class="ml-auto m-0 h-dvh w-[85vw] max-w-[20rem]
               border-0 p-4 open:translate-x-0
               backdrop:bg-black/50">
  <button autofocus formmethod="dialog">×</button>
  <nav>...</nav>
</dialog>
```

### Sticky table with first-column lock
```html
<div role="region" tabindex="0" class="overflow-x-auto focus:outline-2">
  <table class="min-w-full">
    <thead class="bg-gray-50">
      <tr>
        <th class="sticky left-0 bg-gray-50 z-10 px-3 py-2">ID</th>
        <th class="px-3 py-2">...</th>
      </tr>
    </thead>
  </table>
</div>
```

## Arbitrary values — when to use

Use arbitrary values for one-off fluid scaling:
- `text-[clamp(...)]` — fluid font-size
- `py-[clamp(...)]` — fluid padding
- `w-[min(100%-2rem,80rem)]` — capped fluid container
- `h-[100dvh]` — dynamic viewport
- `gap-[clamp(0.75rem,2vw,1.5rem)]` — fluid gap

Don't use arbitrary values for values you'll repeat — promote to design tokens in `theme.extend` instead.

## Common Tailwind sins (don't do)

- `w-screen` for full-bleed → uses `100vw` which includes scrollbar. Use `w-full` inside a `w-[min(100vw,100%)]` parent, or `w-full` + breakout via `margin-inline: calc(50% - 50vw)`.
- `h-screen` for hero → uses `100vh`. Use `h-svh` / `min-h-dvh` (Tailwind v3.4+).
- `text-xs` on inputs → 12px → iOS zoom. Use `text-base` minimum, or `text-[16px]`.
- `hidden md:block` on critical CTA → button disappears on mobile. Make sure mobile has alternative.
- `space-y-4` on responsive flex/grid that changes direction → spacing breaks. Use `gap-4` everywhere.
- `lg:p-12` without smaller-screen baseline padding → mobile gets 0 padding from missing class.

## Plugins worth using
- `@tailwindcss/container-queries` (Tailwind v3; v4 has it built in)
- `@tailwindcss/forms` — sane defaults for form controls (16px font, proper sizing)
- `@tailwindcss/aspect-ratio` (v3; v4 has `aspect-*` built in)
- `tailwind-utopia` — Utopia fluid type/space scale as utilities

## Tailwind v4 highlights
- Native container queries (no plugin)
- CSS-first config via `@theme {}`
- `@variant` for custom variants
- Improved JIT compile
- `dvh`/`svh`/`lvh` units built into `h-*` / `min-h-*` / `max-h-*` utilities

## Sources
- tailwindcss.com/docs/responsive-design
- tailwindcss.com/docs/container-queries
- tailwindcss.com/docs/v4
