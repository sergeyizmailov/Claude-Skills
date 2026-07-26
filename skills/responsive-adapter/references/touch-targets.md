# Touch Target Sizes — 2026 Standards

## Material Design 3
- **Minimum: 48 × 48 dp** (~9mm physical)
- Visual icon may be smaller (24 dp) — tap region MUST extend to 48dp via transparent padding
- FAB: 56 dp

## Apple HIG
- **Minimum: 44 × 44 pt** (point ≈ CSS px on web)
- < 44pt → 25%+ mis-tap rate (Apple's research)
- Exception: inline text links

## WCAG 2.2 SC 2.5.8 Target Size (Minimum) — Level AA, MANDATORY in 2.2
- **24 × 24 CSS pixels minimum**
- OR 24 CSS px spacing such that a 24px-diameter circle centered on each target doesn't overlap another target's circle
- OR inline in paragraph (text-link exception)
- OR conformant alternative on same page
- OR UA-controlled (native controls) / essential
- This is a **floor**, not a goal.

## WCAG 2.5.5 Target Size (Enhanced) — Level AAA
- **44 × 44 CSS pixels** (matches HIG)

## Ship-this recommendations (2026)

| Context | Size | Rationale |
|---------|------|-----------|
| Primary CTAs (touch) | 48–56 CSS px | MD3 spec, thumb reach |
| Secondary actions | 44 CSS px | WCAG 2.5.5 / HIG |
| Dense table / icon-only toolbar | 32 CSS px with 24 CSS px gap | meets 2.5.8 via spacing exception |
| Inline text links | natural line-height | exempt from 2.5.8 |
| Form inputs | 44–48 CSS px height + 16px font | combines tap + zoom prevention |

## Spacing (often more important than size)

The 2.5.8 spacing exception lets you ship 24px targets if circles don't overlap. Tighter rule:
```css
/* Minimum */
.toolbar > * + * { margin-inline-start: 8px; }

/* Better */
.toolbar { display: flex; gap: 12px; }
.toolbar button { min-block-size: 44px; min-inline-size: 44px; }
```

Apple HIG: 8pt between targets. MD3: 8 dp.

## Practical baseline (drop-in)

```css
:where(button, a, input, select, [role="button"]) {
  min-block-size: 44px;
  min-inline-size: 44px;
}

/* Tighten on fine-pointer devices */
@media (hover: hover) and (pointer: fine) {
  :where(button, a, input, select, [role="button"]) {
    min-block-size: 32px;
    min-inline-size: 32px;
  }
}
```

`:where()` keeps specificity at zero so it's easy to override.

## Extending hit area without growing visual

```css
.icon-btn { position: relative; }
.icon-btn::before {
  content: "";
  position: absolute;
  inset: -10px;
  /* Now the click area is 20px larger on each side */
}
```

## Sources
- m3.material.io/foundations/designing/structure
- developer.apple.com/design/human-interface-guidelines
- w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- w3.org/WAI/WCAG21/Understanding/target-size.html
