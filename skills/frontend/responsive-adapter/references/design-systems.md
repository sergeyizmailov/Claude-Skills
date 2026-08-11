# Material 3 + Apple HIG — Adaptive Guidelines

## Material Design 3 — Window Size Classes

| Class | Width | Device coverage (Google's stat) |
|---|---|---|
| Compact     | < 600dp        | 99.96% phones portrait |
| Medium      | 600 – 839dp    | 93.73% tablets portrait, foldable inner portrait |
| Expanded    | 840 – 1199dp   | 97.22% tablets landscape, foldable inner landscape |
| Large       | 1200 – 1599dp  | Large tablets |
| Extra-large | ≥ 1600dp       | Desktop |

Height classes:
| Class | Height |
|---|---|
| Compact   | < 480dp |
| Medium    | 480 – 899dp |
| Expanded  | ≥ 900dp |

dp ≈ CSS px at DPR 1. M3 breakpoints translate directly to CSS `min-width`.

## M3 layout recommendations per class

| Class | Columns | Margins | Gutters | Navigation |
|-------|---------|---------|---------|------------|
| Compact (< 600)     | 4  | 16dp                  | 16dp | Bottom navigation bar |
| Medium (600-839)    | 8  | 24dp                  | 24dp | Navigation rail (80dp wide) |
| Expanded (840-1199) | 12 | 24dp (up to 200dp)    | 24dp | Nav rail + optional drawer |
| Large (1200-1599)   | 12 | up to 200dp           | 24dp | Permanent drawer / multi-pane |
| Extra-large (≥1600) | 12 | up to 200dp           | 24dp | Permanent drawer + multi-pane |

Other M3 specifics:
- Pane padding: 16dp internal, 24dp spacing between panes.
- Max content line length: 60 characters on large screens.
- **Touch target: 48dp minimum.**
- 8dp baseline grid.
- Canonical responsive patterns: Feed, List/Detail, Supporting Pane.

## Apple HIG — Size Classes

Two values per axis: Compact (C) and Regular (R). No numeric breakpoints in points — OS reports via trait collection.

| Device / state | H | V |
|----------------|---|---|
| All iPhones portrait | C | R |
| Standard iPhones landscape | C | C |
| Plus/Max iPhones landscape | R | C |
| iPad full-screen any orientation | R | R |
| iPad Slide Over | C | R |
| iPad Split View 1/2 | C | R for both |
| iPad Pro 12.9/13" 1/2 landscape | R | R |
| iPad 2/3-1/3 landscape | Primary R, secondary C | R |

**Vertical size class on iPad is always Regular.** Design focuses on horizontal.

## HIG specifics

- **Minimum hit target: 44 × 44 pt** ("Provide ample touch targets... 44pt × 44pt for all controls").
- Standard layout margins: 16pt compact (iPhone), 20pt regular (iPad).
- Readable content width: adapts per device (Apple's "readable content guide").
- **Safe area:** `safe-area-inset-top/right/bottom/left` env vars on web — REQUIRED for notch, Dynamic Island, home indicator. Need `viewport-fit=cover` in viewport meta.
- 8pt grid (4pt for tight controls).

## iPad multitasking

Slide Over, Split View, Stage Manager can produce app window widths from ~320pt to 1366pt. Apple forbids hard-coding device widths.

- **Slide Over:** forces compact (~320-375pt) regardless of device.
- **Split View 1/2:** most iPads compact for both; only 12.9/13" Pro yields regular for both.
- **Stage Manager:** arbitrary resizable windows.

## Web applicability

- HIG numeric thresholds not directly CSS-addressable (no "compact" media query). Map via viewport width: ~390-440 CSS px = compact (iPhone), ~744+ = regular (iPad).
- Apple's 44pt = 44 CSS px on iOS Safari. WCAG 2.5.5 (enhanced) = 44px, WCAG 2.5.8 (minimum) = 24px.
- M3 dp = CSS px 1:1. M3's grid (4/8/12 columns at 600/840/1200/1600) is the most ergonomic cross-platform numeric ladder for web.

## Recommendation

Build web breakpoints from Material 3 numbers (600 / 840 / 1200 / 1600), layer Apple's 44pt touch target and `safe-area-inset` rules on top. This combination gives you Android-correct, iOS-friendly, and WCAG 2.2-compliant defaults.

## Sources
- m3.material.io/foundations/layout/applying-layout/window-size-classes
- developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes
- developer.apple.com/design/human-interface-guidelines/layout
- useyourloaf.com/blog/size-classes (iOS size-class reference)
