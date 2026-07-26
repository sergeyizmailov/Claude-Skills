# Device Matrix — 2026

## Minimum useful test matrix (8 widths — covers >95% real traffic)

| Width × Height | Class | Why |
|---|---|---|
| 360 × 780  | Android baseline (Galaxy S24/S25)        | Most common Android |
| 390 × 844  | iPhone 12/13/14                          | Largest iPhone share |
| 393 × 852  | iPhone 15/16 / Pixel 7-9 family          | Current Apple flagship cluster |
| 430 × 932  | iPhone 15/16 Pro Max                     | Biggest phone |
| 768 × 1024 | iPad portrait (legacy boundary)          | Tablet pivot |
| 1024 × 768 | iPad landscape / small laptop            | sm/md/lg handoff |
| 1440 × 900 | Desktop / MacBook Pro 13-14"             | Designer's typical baseline |
| 1920 × 1080| FHD desktop                              | Largest desktop share (~19% global) |

## Extended matrix (+7 widths for thorough QA)

| Width | Why |
|---|---|
| 320  | Smallest meaningful — iPhone SE 1st gen, narrow foldable covers (Z Fold 5 outer) |
| 412  | Pixel 8/9, Galaxy S25 Ultra |
| 884–984 | Foldable inner (Z Fold 5/6 = 884, Z Fold 7 = 984). Triggers Material 3 "Expanded" on small physical screen — most often breaks layouts |
| 1280 | Smallest common laptop, 720p screens |
| 1366 | Cheap laptop default (~6.6% globally still — significant in EMEA/LATAM) |
| 1536 | 1920×1080 @ 125% Windows scaling (~8.5% of desktop) |
| 2560 / 3440 | QHD / ultrawide |

## Top mobile resolutions (StatCounter, April 2026 worldwide)

| Resolution | Share | Device class |
|------------|-------|--------------|
| 414 × 896 | 12.70% | iPhone XR/11/Plus class |
| 360 × 800 | 9.23%  | Mid-range Android, Galaxy S base, Pixels |
| 390 × 844 | 6.71%  | iPhone 12/13/14 |
| 375 × 812 | 4.23%  | iPhone X/XS/11 Pro/SE3 |
| 384 × 832 | 4.03%  | Pixel |
| 393 × 873 | 4.02%  | iPhone 15/15 Pro / Pixel 7-9 |

The cluster 360 / 375 / 384 / 390 / 393 / 412 / 414 / 430 covers >85% of real iPhone + Android traffic. Adding 320 and 440 catches the floor and ceiling.

## iPhone CSS viewports (current)

| Model | CSS Viewport | DPR |
|-------|--------------|-----|
| iPhone SE 3 (2022) | 375 × 667 | 2 |
| iPhone 12/13/14    | 390 × 844 | 3 |
| iPhone 14/15 Plus  | 428 × 926 | 3 |
| iPhone 15/15 Pro   | 393 × 852 | 3 |
| iPhone 15 Pro Max  | 430 × 932 | 3 |
| iPhone 16          | 393 × 852 | 3 |
| iPhone 16 Pro      | 402 × 874 | 3 |
| iPhone 16 Pro Max  | 440 × 956 | 3 |

## Android flagship CSS widths

| Model | CSS Viewport | DPR |
|-------|--------------|-----|
| Galaxy S24/S25       | 360 × 780 | 3   |
| Galaxy S25 Ultra     | 412 × 891 | 3.5 |
| Pixel 8/9            | 412 × 915 | ~2.6 |
| Pixel 9 Pro XL       | 448 × 998 | 3   |

## Foldables

| Device | Outer | Inner |
|--------|-------|-------|
| Galaxy Z Fold 5 | 320 × 868 | 884 × 829 |
| Galaxy Z Fold 6 | 344 × 800 | 884 × 829 |
| Galaxy Z Fold 7 | 374 × 800 | 984 × 830 |
| Pixel Fold      | 408 × 720 | 838 × 632 |
| Z Flip cover    | ~360 × 360 | main 412 × 919 |

**Critical:** inner-fold widths (838–984 CSS px) hit your `lg` breakpoint and render desktop-style layouts on a sub-7-inch screen. Either rely on container queries OR add a specific test at 884/984 px.

## Tablets

| Device | CSS Viewport | DPR |
|--------|--------------|-----|
| iPad mini (6/7)        | 744 × 1133 | 2 |
| iPad 10/11 gen         | 810 × 1080 | 2 |
| iPad Air 11" (M2/M3)   | 820 × 1180 | 2 |
| iPad Air 13"           | 1024 × 1366 | 2 |
| iPad Pro 11" (M4)      | 834 × 1210 | 2 |
| iPad Pro 13" (M4)      | 1024 × 1366 | 2 |
| Surface Pro 9/10       | 1368 × 912 | 1.5–2 |
| Pixel Tablet           | 1280 × 800 | 2 |
| Galaxy Tab S9/S10      | 800 × 1280 | 2 |

## Desktop common widths

| Width | Use |
|-------|-----|
| 1280  | Smallest common laptop, base testing floor |
| 1366  | Cheap laptop default (~6.6% globally) |
| 1440  | MacBook Pro 13/14" effective @2x |
| 1536  | 1920×1080 @ 125% Windows scaling (very common) |
| 1600  | Older WSXGA laptops |
| 1920  | FHD desktop king (~19% global) |
| 2560  | QHD desktops / MBP 16" @2x |
| 3440  | 21:9 ultrawide |
| 3840  | 4K UHD (typically scaled to ~1920-2560 CSS) |

## What to look for at each width (verification checklist)

For each width in your matrix, examine the screenshot for:

| Class | Specific checks |
|---|---|
| **Layout integrity** | No horizontal scrollbar. Nothing bleeds past viewport. No content cut off behind another element. |
| **Typography** | Body text ≥ 14px effective. Inputs ≥ 16px (iOS zoom). Heading hierarchy visible (h1 visibly larger than h2). |
| **Tap targets** | Buttons/links ≥ 44×44 px on widths ≤ 1024px. Tap targets not packed too tight (≥8px gap). |
| **Content density** | Multi-column layouts have stacked correctly. Sidebars collapsed to drawer ≤ 768px. Tables in scroll wrapper or transformed to cards. |
| **Ultra-wide (≥1920)** | Content not stretched edge-to-edge — `max-width` on main container so it stays readable. No vast empty regions. |
| **320px specifically** | No element has `min-width` exceeding `viewport - 2 × padding`. Hero headings still readable (not gigantic-clamp overshoot). |
| **Interactive state** | If page has modal/menu/drawer, open it at mobile widths and re-screenshot. Verify content reachable. |

## DPR (device pixel ratio) considerations

- **Layout uses only CSS px.** DPR is irrelevant for breakpoint media queries.
- **DPR matters for raster assets** — serve 1x / 2x / 3x via `srcset`. iPhone Pro = DPR 3, so a 100×100 CSS px image must be sourced at 300×300 to stay sharp.
- **DPR matters for `<canvas>`/charts/maps** — scale backing store by `devicePixelRatio` then transform context.
- **Hairline borders** — Windows 125% scaling = DPR 1.5 → `1px` renders unevenly. Use `0.5px` or `outline` workarounds on DPR 2+ targets.

## Cross-platform breakpoint set (recommended, aligned to Material 3)

```
xs:  320px  – ultra-small / foldable cover
sm:  390px  – iPhone baseline (covers iPhone 12-16)
md:  600px  – M3 Compact→Medium boundary (iPad mini portrait, large phone landscape)
lg:  840px  – M3 Medium→Expanded (iPad portrait, foldable inner)
xl:  1200px – M3 Expanded→Large (laptop / large tablet landscape)
2xl: 1600px – M3 Large→Extra-large (desktop)
```

This satisfies:
- HIG compact-vs-regular pivot at 600-768 range
- Material 3 numeric breakpoints (600 / 840 / 1200 / 1600)
- StatCounter dominant device clusters
- Foldable inner display boundary (840-984)

## Sources
- gs.statcounter.com (mobile + desktop resolution share, April 2026)
- yesviz.com/devices.php (CSS viewport + DPR database)
- screensizechecker.com (iPhone + Android viewport tables 2026)
- m3.material.io/foundations/layout/applying-layout/window-size-classes
- developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes
