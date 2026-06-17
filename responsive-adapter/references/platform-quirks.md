# iOS Safari + Android Chrome — Platform Quirks (2026)

## iOS Safari (iOS 17 / 18 / 26)

### Input zoom (16px)
Still triggers on iOS 18 / iPhone 16. Apple hasn't changed since iOS 5.
**Fix:** input/textarea/select `font-size: 16px`. See anti-patterns A4. NEVER fix with `maximum-scale=1` — accessibility violation.

### `100vh` vs `100dvh`
iOS 18 does NOT update `window.innerHeight` when address bar expands. `100vh` always equals `lvh` on iOS Safari.
**Fix:** `dvh`/`svh`/`lvh` (Baseline June 2025). Don't animate `dvh`.

### Safe-area insets
```css
.app {
  padding-block-start: env(safe-area-inset-top);
  padding-block-end:   env(safe-area-inset-bottom);
  padding-inline-start: env(safe-area-inset-left);
  padding-inline-end:   env(safe-area-inset-right);
}
/* iOS 16.4+ static maximum: */
.fixed-overlay {
  padding-block-end: max(12px, env(safe-area-max-inset-bottom));
}
```

**REQUIRES** `viewport-fit=cover` in viewport meta. Without it env values are 0 and Safari letterboxes landscape with black bars.

iOS landscape has unreported ~20px touch dead-zone along the top.

### Sticky + overflow bugs
`position: sticky` inside `overflow: auto` or inside a transformed ancestor BREAKS on iOS Safari. Bug persists through iOS 18.
**Fix:** Move sticky element out of the scroll container, or use `overflow: clip` + fixed positioning.

### Bounce / rubberband
```css
html, body { overscroll-behavior: none; }
/* Or contain for nested scrollers: */
.scroller { overscroll-behavior: contain; }
```

### `-webkit-text-size-adjust`
iOS portrait→landscape silently inflates fonts.
```css
html { -webkit-text-size-adjust: 100%; text-size-adjust: 100%; }
```
Use `100%`, NOT `none` (blocks user text-size preferences = a11y violation).

### Date inputs
iOS 17 `<input type="date">` with `display: inline-flex` ignores `width: 100%`. iOS 18 fixed but `display: inline-block` adds random bottom padding.

### PWA standalone
- Detect: `window.matchMedia('(display-mode: standalone)').matches` or `navigator.standalone` (iOS-specific).
- Different safe-area behavior — Dynamic Island can hide top UI; always pad with `env(safe-area-inset-top)`.
- iOS 17+ rotation animation ~500ms — debounce dimension reads.

---

## Android Chrome

### Soft keyboard (Chrome 108+)
Chrome 108+ changed default: keyboard resizes only the **visual** viewport, NOT layout viewport. Old `100vh` elements no longer collapse when keyboard appears (good).

Opt back into legacy resize for chat apps that need it:
```html
<meta name="viewport"
      content="width=device-width, initial-scale=1, interactive-widget=resizes-content">
```
Values: `resizes-visual` (default), `resizes-content` (legacy), `overlays-content`.

VisualViewport API for fine control:
```js
window.visualViewport.addEventListener('resize', () => {
  document.documentElement.style.setProperty(
    '--kb',
    (innerHeight - visualViewport.height) + 'px'
  );
});
```

VirtualKeyboard API (Chromium-only):
```js
if ('virtualKeyboard' in navigator) {
  navigator.virtualKeyboard.overlaysContent = true;
}
```
Then CSS `env(keyboard-inset-height)` reachable.

### Pull-to-refresh
```css
html, body { overscroll-behavior-y: contain; } /* preserves nested scrolls */
/* Or none to fully kill PTR + bounce */
```

### Address bar
More predictable than iOS but still varies. Same `dvh`/`svh`/`lvh` solution applies.

### Display cutout
Same `env(safe-area-inset-*)` (with `viewport-fit=cover`).

### Foldables (Galaxy Z Fold/Flip, Surface Duo)
```css
@media (horizontal-viewport-segments: 2) {
  .layout {
    grid-template-columns: env(viewport-segment-right 0 0) 1fr;
  }
}
@media (device-posture: folded) { /* book/laptop posture */ }
```
Viewport Segments API + Device Posture API — Chrome 125 (origin trial → stable). Use `vertical-viewport-segments` for Flip-style hinges. Guard with `@supports`.

---

## Safe-area drop-in recipe (works iOS + Android)

```css
:root {
  --safe-t: env(safe-area-inset-top);
  --safe-r: env(safe-area-inset-right);
  --safe-b: env(safe-area-inset-bottom);
  --safe-l: env(safe-area-inset-left);
}

.app-shell {
  padding-block-start: var(--safe-t);
  padding-block-end:   var(--safe-b);
  padding-inline-start: var(--safe-l);
  padding-inline-end:   var(--safe-r);
}

.bottom-nav {
  position: fixed;
  inset: auto 0 0 0;
  padding-block-end: max(0.75rem, var(--safe-b));
  padding-inline:    max(1rem,    var(--safe-l));
  /* extend bg into inset */
  background: #fff;
}
```

## Sources
- developer.chrome.com/blog/viewport-resize-behavior (Chrome 108 keyboard)
- developer.mozilla.org VirtualKeyboard API, env()
- polypane.app/blog/using-safe-area-inset-to-build-mobile-safe-layouts
- muffinman.io/blog/ios-safari-scroll-position-fixed (iOS sticky bugs)
- kilianvalkhof.com/2022/css-html/your-css-reset-needs-text-size-adjust-probably
- developer.chrome.com/blog/foldable-apis-ot
- savvy.co.il, aravishack.medium (dvh/svh/lvh)
