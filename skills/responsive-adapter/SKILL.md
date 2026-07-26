---
name: responsive-adapter
description: Take an existing landing page, admin panel, dashboard, or any web page that is not responsive (or only partially responsive) and make it fully adaptive across every real viewport width from 320px phones up to 2560px+ widescreens — without changing the visual design or brand. Triggers on requests to make a page responsive, fix mobile layout, fix breakpoints, adapt a landing or admin to phones / tablets / desktops / widescreens, or symptom descriptions like horizontal scroll, elements overflowing, text unreadable on mobile, sidebar broken on tablet, empty space on widescreen. Use even when the user only describes the symptom and never says the word "responsive" — adapting layouts to viewports is what this skill does. Performs a static anti-pattern scan, applies fixes using modern CSS primitives (clamp, container queries, dvh/svh/lvh, aspect-ratio, grid auto-fit), then verifies in a real browser at the device matrix and reports remaining issues.
---

# Responsive Adapter

You are a **responsive-layout engineer**. Your job: take a page that someone already designed and built, and make it work at every real viewport width from **320px to 2560px+** without changing the visual identity. "Works" has measurable criteria — see Phase 4 verification checklist.

The visual *style* (colors, typography choices, brand, hierarchy, decorative elements that fit the screen) stays. The *layout* adapts: stacks columns on mobile, collapses sidebars to drawers, switches dense tables to cards or scroll, fluid-scales typography, and uses modern CSS primitives (`clamp`, container queries, `dvh`/`svh`, `aspect-ratio`, `grid auto-fit`) to avoid hard-coded breakpoint hell.

## Core principle: preserve, don't redesign

**The desktop visual is the source of truth. Every other width is a graceful adaptation of it.** Never re-pick fonts, never change the color system, never invent new components, never reflow content the designer wouldn't recognize. You are not redesigning — you are making the existing design hold up under stress at every viewport.

If you find yourself "improving" something that wasn't broken on responsiveness grounds, stop. That's scope creep. Mention it in the report, don't touch it.

## What you may and may not change

| Allowed | Forbidden |
|---|---|
| Any CSS / Tailwind utility class | Color palette, brand colors |
| Adding `<meta name="viewport">` if missing | Font families |
| Wrapping elements (`<div class="overflow-x-auto">` around a wide table) | Iconography, illustrations, content |
| Adding `hidden md:block` / `md:hidden` toggle for an off-canvas menu | New components, redesigns of existing ones |
| A small hamburger toggle (≤15 lines, or native `<dialog>`) | Replacing established UI library with another |
| Restructuring grid columns (`grid-cols-3` → `grid-cols-1 md:grid-cols-3`) | Removing sections that "don't fit" — adapt them instead |
| Replacing fixed `px` widths with fluid units | Changing copy / wording |
| Adding `aria-label` where mobile UX needs it for an icon button | Heavy refactor beyond what responsiveness demands |

Rule of thumb: if someone takes a desktop screenshot before and after, they should be indistinguishable except where you intentionally stacked or collapsed.

## Recommended breakpoint set (Material 3-aligned)

```
xs:  320px   — ultra-small, foldable cover
sm:  390px   — iPhone baseline (covers iPhone 12-16)
md:  600px   — M3 Compact→Medium (iPad mini portrait, large phone landscape)
lg:  840px   — M3 Medium→Expanded (iPad portrait, foldable inner)
xl:  1200px  — M3 Expanded→Large (laptop / large tablet landscape)
2xl: 1600px  — M3 Large→Extra-large (desktop)
```

If the project already uses a different breakpoint system (default Tailwind 640/768/1024/1280/1536, or Bootstrap-style), **extend it, don't replace it**. Introducing a second parallel system creates a maintenance nightmare. Adapt the recommended logic to whatever exists.

## Workflow (5 phases — run in order)

Each phase has a clear exit criterion. Finish the phase, then move to the next. Don't interleave.

### Phase 1 — Discover

Detect what you're working with before you touch anything.

1. **Identify the project root.** If the user didn't say, ask once.
2. **Detect the stack.** Look at file extensions, `package.json`, imports:
   - `.html` + `<style>` or `<link>` to `.css` → **vanilla** → read `references/vanilla-css.md`
   - `tailwind.config.*`, `@tailwind`, or `class="... md:..."` patterns → **Tailwind** → read `references/tailwind.md`
   - `styled-components`, `@emotion`, `.styled.ts` → **CSS-in-JS** → read `references/css-in-js.md`
   - `*.module.css` → CSS Modules (treat as vanilla)
   - Mix is common — record what each file uses.
3. **Enumerate pages/components in scope.** For a single HTML file: just that file. For a Next.js project: `app/` or `pages/` routes. For an admin: each route under the panel.
4. **Note the existing breakpoint system** if any. Don't introduce a parallel one — extend the existing one.
5. **Open the page in a browser** (via the `agent-browser` skill or a dev server the user is running) at desktop width 1440px and capture a **baseline screenshot**. This is the visual contract — every later screenshot must preserve its spirit.

**Exit criterion:** you can list (a) stack per file, (b) every file you will touch, (c) the existing breakpoint conventions, (d) you have a desktop baseline screenshot.

### Phase 2 — Static scan

Before fixing anything, find every anti-pattern in the code. The bundled script does most of the grep work:

```bash
bash ~/.claude/skills/responsive-adapter/scripts/scan.sh <project-root>
```

It outputs a structured issue list grouped by severity (CRITICAL / MAJOR / MINOR) with file:line references. Read `references/anti-patterns.md` for the full catalog explaining each pattern and its fix.

Critical things the scan catches:

- **A1** — missing/broken `<meta name="viewport">`
- **A2** — `maximum-scale=1` / `user-scalable=no` (WCAG 1.4.4 violation)
- **A3** — fixed `width: Npx` / large `min-width` blocking shrinkage
- **A4** — inputs with `font-size < 16px` (iOS Safari auto-zoom on focus, still broken as of iOS 18)
- **A5** — `100vh` without `dvh`/`svh` fallback (mobile URL-bar issue)
- **A8** — no fluid-image baseline rule
- **A9** — `position: fixed` bottom without `safe-area-inset-bottom`
- **A13** — `100vw` (includes scrollbar — may overflow)
- **A14** — `overflow: hidden` on body (masking root cause)

In addition, manually inspect for:

- Tables not wrapped in `overflow-x: auto` ancestor
- Sidebars/nav always rendered open
- Hover-only menus without `:focus-within` fallback (touch device hostility)
- Tap targets — WCAG 2.2 SC 2.5.8 AA floor is 24×24 CSS px; ship target is 44×44 (matches HIG / WCAG 2.5.5 AAA). See `references/touch-targets.md` for the full nuance (inline-link exception, spacing exception, MD3 48dp).

**Exit criterion:** written issue list grouped by severity with file:line references.

### Phase 3 — Apply fixes

Two rules govern the fixes:

**Rule A: use modern primitives, not breakpoint salad.** Modern CSS lets you solve most adaptivity with `clamp()`, `min()`/`max()`, container queries, `dvh/svh/lvh`, `aspect-ratio`, `grid auto-fit/minmax` — *without* writing five media queries per component. See `references/modern-primitives.md`.

**Rule B: stack-appropriate patterns.** Open the reference for the stack each file uses (Tailwind / vanilla / CSS-in-JS — see Phase 1) and follow its idioms.

Order of fixes (earlier fixes prevent later breakage):

1. **Foundation** — viewport meta with `viewport-fit=cover`, `box-sizing: border-box`, `-webkit-text-size-adjust: 100%`, base `font-size: 100%` (16px), `overflow-x: clip` on html (NOT hidden — see anti-patterns A14), fluid-image rule `img, svg, video { max-inline-size: 100%; block-size: auto; }`.

2. **Fluid typography** — replace hard-coded heading sizes with `clamp(MIN_rem, fluid_with_rem_component, MAX_rem)`. WCAG-safe rule: `MAX ≤ 2.5 × MIN`. See `references/fluid-typography.md` for the canonical formula and Utopia-style scales.

3. **Container sizing** — replace any `width: Npx` with `max-width: Npx; width: 100%;` and sensible `padding-inline`. Use `inline-size: min(100% - 2rem, 1280px)` for centered containers (one-liner replaces `max-width + padding` + media queries).

4. **Layout primitives** — wrap flex/grid with sane wrapping. Switch fixed grids to:
   ```css
   grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
   ```
   `min(100%, 280px)` is the magic that makes 320px viewports safe.

5. **Breakpoint adaptations** — at small viewports: stack columns, hide decorative side elements (`hidden md:block`), collapse sidebar to off-canvas drawer (preferably native `<dialog>` — see `references/menus-drawers.md`), switch tables to scroll wrapper or card transformation (see `references/admin-patterns.md`).

6. **Mobile nav** — if there's no mobile toggle, prefer native `<dialog>` + `showModal()`. It gives you focus management, Escape, focus trap, top-layer rendering, and `::backdrop` for free. See `references/menus-drawers.md` for the drop-in pattern.

7. **Touch & tap** — ensure tap targets ≥ 44 px on touch widths. Inputs ≥ 16 px font-size. See `references/touch-targets.md`.

8. **Safe areas** — pad bottom-fixed elements with `max(12px, env(safe-area-inset-bottom))`. Requires `viewport-fit=cover` in viewport meta. See `references/platform-quirks.md`.

9. **Edge widths** — at ultra-wide (≥1920px) the page often looks empty. Use `max-width` on main content (e.g. `max-w-[1400px] mx-auto`) so content doesn't stretch infinitely. At 320px verify nothing has `min-width` larger than `viewport - 2 × padding`.

10. **Component-level vs page-level queries:**
    - **`@media`** for app shell, OS preferences (`prefers-color-scheme`, `prefers-reduced-motion`), image `srcset sizes`, print.
    - **`@container`** for reusable components (cards, widgets, sidebars) that need to adapt to their slot, not the viewport.
    - Heuristic: if removing the component from the page would change what styles apply → `@container`. If only resizing browser would → `@media`.

After all fixes, do a **diff sanity check**: scan your own changes for the forbidden list (changed fonts, changed colors, removed sections). If you find any, revert.

**Exit criterion:** every issue in Phase-2 list is fixed or explicitly marked "won't fix because <reason>". No forbidden changes introduced.

### Phase 4 — Browser verification

Static scans miss runtime issues (computed layouts, JS-driven UI, font fallbacks, real iOS Safari behavior). Verify in a real browser.

Use the `agent-browser` skill to:

1. **Start a local server** for the page if not running:
   - Static HTML: `python3 -m http.server 8000` (or `npx serve`)
   - Project: run its dev script
2. **Take screenshots at the device matrix.** Read `references/device-matrix.md` for the full list. Always include the **minimum 8-width matrix**:

   | Width × Height | Class |
   |---|---|
   | 360 × 780 | Android baseline |
   | 390 × 844 | iPhone 12-14 |
   | 393 × 852 | iPhone 15/16 |
   | 430 × 932 | iPhone Pro Max |
   | 768 × 1024 | iPad portrait (sm/md handoff) |
   | 1024 × 768 | iPad landscape / small laptop |
   | 1440 × 900 | Designer's baseline |
   | 1920 × 1080 | Full HD desktop |

   For thorough QA, add the extended matrix: 320 (smallest), 884-984 (foldable inner — often breaks), 1280/1366 (cheap laptops), 1536 (Windows scaling), 2560/3440 (large/ultrawide).

3. **For each width, examine the screenshot for:**

   | Category | Specific checks |
   |---|---|
   | Layout integrity | No horizontal scrollbar. Nothing bleeds past viewport. No content cut off behind another element. |
   | Typography | Body text ≥ 14px effective. Inputs ≥ 16px (iOS zoom). Heading hierarchy still visible. |
   | Tap targets | Buttons/links ≥ 24×24 (WCAG 2.5.8 AA floor) with ≥ 8px gap; ship target 44×44 on widths ≤ 1024. Inline text links exempt. |
   | Content density | Multi-column layouts stacked correctly. Sidebar collapsed ≤ 768. Tables in scroll wrapper or cards. |
   | Ultra-wide (≥1920) | Content not stretched edge-to-edge. No vast empty regions. |
   | 320px specifically | Nothing has `min-width > viewport - 2 × padding`. Hero text not gigantic from clamp overshoot. |
   | Interactive state | If page has modal/menu/drawer, open it at mobile widths and re-screenshot. |

4. **If a JS-driven mobile menu exists,** click it on a mobile screenshot to confirm it opens, covers the screen, can be closed (Escape + backdrop click + close button).

**Exit criterion:** screenshot at every width in the matrix, with annotated issues for any that fail.

### Phase 5 — Report

Output a structured report. Use this exact format:

```
# Responsive Adaptation Report

## Stack detected
- <stack summary per file group>

## Files modified
- <path>:<line range> — <one-line reason>
- ...

## Anti-patterns fixed
- [CRITICAL] <name> (×N occurrences) — <how fixed>
- [MAJOR]    <name> (×N) — <how fixed>
- [MINOR]    <name> (×N) — <how fixed>

## Verification results
| Width | Status | Issues |
|-------|--------|--------|
| 360   | PASS   | — |
| 390   | PASS   | — |
| 393   | PASS   | — |
| 430   | PASS   | — |
| 768   | PASS   | — |
| 1024  | PASS   | — |
| 1440  | PASS   | — |
| 1920  | PASS   | — |

## Screenshots
- <relative path per width>

## Won't-fix items
- <issue> — <reason>

## Remaining concerns
- <anything the user should know>
```

If any breakpoint failed verification, **don't claim done**. Iterate on Phase 3 for the specific issues, re-verify only the affected widths, re-report.

## Reference files

Read these only when the workflow phase points to them — don't read all upfront.

| File | When to read |
|------|--------------|
| `references/anti-patterns.md` | Phase 2 — full catalog of every anti-pattern with detection + fix |
| `references/modern-primitives.md` | Phase 3 — `clamp`, `min/max`, container queries, `dvh/svh`, `aspect-ratio`, grid auto-fit, subgrid, logical props, `:has()`, `@supports` |
| `references/fluid-typography.md` | Phase 3, fluid type step — Utopia scale, clamp formula, accessibility-safe ratios |
| `references/device-matrix.md` | Phases 1 & 4 — full device list with rationale, what to check at each width |
| `references/design-systems.md` | When uncertain about breakpoint values — Material 3 + Apple HIG guidance |
| `references/admin-patterns.md` | Working on a dashboard/admin — sidebar collapse, tables→cards, dense forms, modals, widget grids |
| `references/menus-drawers.md` | Adding/fixing mobile nav — `<dialog>` drawer, bottom sheet, accessibility |
| `references/touch-targets.md` | Verifying tap targets — WCAG 2.5.8 vs 2.5.5, MD3 vs HIG |
| `references/platform-quirks.md` | iOS Safari / Android Chrome quirks (input zoom, safe-area, dvh, foldables) |
| `references/tailwind.md` | Stack is Tailwind |
| `references/vanilla-css.md` | Stack is vanilla CSS / CSS Modules |
| `references/css-in-js.md` | Stack is styled-components / Emotion / vanilla-extract |

## Bundled scripts

- `scripts/scan.sh <project-root>` — static anti-pattern scanner. Run in Phase 2.

## Anti-patterns in *your own* execution

Things to NOT do while running this skill:

- **Don't rewrite the page from scratch.** Even if existing CSS is ugly, surgically adapt it.
- **Don't add a CSS framework** the project doesn't use. Vanilla CSS project → don't pull in Tailwind.
- **Prefer CSS over JS for layout adaptation.** `clamp`, container queries, `dvh/svh`, RAM grid, `:has()` cover ~90% of cases without `react-responsive`/`useMediaQuery`-style hooks (which also produce SSR hydration flashes). Legit JS use: `ResizeObserver` for canvas/chart sizing, virtualized tables, dynamic font measurement.
- **Don't write 12 media queries when 1 `clamp()` does the job.** Modern primitives over breakpoint salad.
- **Don't claim done after fixing CSS without running Phase 4.** A page that "looks right in the diff" is not a page that works on 320px. Verification is non-negotiable.
- **Don't silently regress widths outside the user's stated focus.** If they say "make it work on mobile", the desktop visual must still render correctly — re-screenshot at 1440px after your changes and compare to the Phase-1 baseline.
- **Don't gate work on `prefers-reduced-motion`, dark mode, RTL, or other tangentially related things.** Stay in scope.
- **Don't use `overflow: hidden` on body to mask overflow.** Find the root cause. Use `overflow-x: clip` on `html` only if you truly can't fix the source.
- **Don't add `maximum-scale=1` / `user-scalable=no`** to "fix" iOS input zoom. Fix input font-size instead (A4).
- **Don't use pure `vw` for fluid type** (`clamp(1rem, 4vw, 2rem)` — middle doesn't move on zoom). Always mix `rem` into middle: `clamp(1rem, 0.875rem + 1vw, 2rem)`.

## When to stop

You're done when:

1. Phase-5 report shows PASS at every width in the device matrix.
2. Desktop baseline screenshot from Phase 1 and post-adaptation desktop screenshot are visually equivalent (same hierarchy, colors, fonts, components).
3. No forbidden changes were introduced.
4. The user has the report and the screenshots.

If you can't reach PASS at every width, say so explicitly — list the failing widths and what's blocking. Don't pretend.
