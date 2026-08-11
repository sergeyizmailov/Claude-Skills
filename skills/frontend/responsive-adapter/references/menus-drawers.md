# Mobile Menus & Drawers — 2026 Patterns

## Pure-CSS approaches — AVOID in 2026

- **Checkbox hack:** Label not focusable predictably. SR announces "checkbox" instead of "menu button". Use only for ultra-low-JS marketing pages with a11y caveats.
- **`:target`:** Changes URL hash, breaks browser back, conflicts with anchor links.
- **`<details>/<summary>`:** Not announced as expanded on iOS VoiceOver + Safari. NVDA + Chrome inconsistent. No built-in focus-trap or Escape.

**Verdict:** pure-CSS menus are NOT production-grade for accessible navigation in 2026.

---

## Minimal-JS approach (≤15 lines)

```html
<button aria-expanded="false" aria-controls="nav" id="nav-btn">Menu</button>
<nav id="nav" hidden>
  <a href="/">Home</a>
  <a href="/about">About</a>
</nav>
<script>
  const btn = document.getElementById('nav-btn');
  const nav = document.getElementById('nav');
  btn.addEventListener('click', () => {
    const open = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!open));
    nav.hidden = open;
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') {
      btn.setAttribute('aria-expanded', 'false');
      nav.hidden = true;
      btn.focus();
    }
  });
</script>
```

Heydon Pickering's disclosure-widget pattern. Nav links are a list of links, not a `role="menu"` (which is for desktop-app menubars).

---

## Native `<dialog>` drawer (RECOMMENDED 2026)

```html
<button aria-controls="drawer">Menu</button>
<dialog id="drawer" aria-label="Site navigation" class="drawer">
  <button autofocus aria-label="Close" formmethod="dialog">×</button>
  <nav>
    <a href="/">Home</a>
    <a href="/about">About</a>
  </nav>
</dialog>
<script>
  const dlg = document.getElementById('drawer');
  document.querySelector('[aria-controls="drawer"]').onclick = () => dlg.showModal();
  // backdrop click closes
  dlg.addEventListener('click', e => {
    if (e.target === dlg) dlg.close();
  });
</script>
```

```css
.drawer {
  margin: 0 0 0 auto;
  block-size: 100dvh;
  max-inline-size: 20rem;
  inline-size: 85vw;
  border: 0; padding: 1rem;
  padding-block-start: max(1rem, env(safe-area-inset-top));
  padding-inline-end:  max(1rem, env(safe-area-inset-right));
}
.drawer::backdrop { background: rgb(0 0 0 / .5); }
.drawer[open] { animation: slide .2s ease-out; }
@keyframes slide { from { translate: 100% 0; } }
```

`showModal()` provides AUTOMATICALLY:
- Focus management (moves to first focusable / `autofocus`)
- Escape key closes
- Focus trapping (modal mode)
- Top-layer rendering (escapes z-index hell)
- `::backdrop`
- `inert` on rest of page

WCAG 2025 guidance no longer mandates manual focus-trapping inside `<dialog>` — UA handles it.

---

## Bottom-sheet skeleton (mobile-preferred)

```css
.sheet {
  position: fixed;
  inset: auto 0 0 0;
  margin: 0;
  max-block-size: 90dvh;
  border-radius: 1rem 1rem 0 0;
  padding-block-end: max(1rem, env(safe-area-inset-bottom));
}
.sheet::backdrop { background: rgb(0 0 0 / .4); }
.sheet[open] { animation: rise .25s cubic-bezier(.32, .72, 0, 1); }
@keyframes rise { from { translate: 0 100%; } }
```

For drag-to-dismiss: use Vaul (`vaul.emilkowal.ski`) or roll your own with `onDragEnd` velocity threshold ≈500.

---

## View Transitions enhancement (Baseline Oct 2025)

```css
.drawer { view-transition-name: drawer; }
::view-transition-old(drawer) { animation: slide-out .2s ease-in; }
::view-transition-new(drawer) { animation: slide-in  .2s ease-out; }
@keyframes slide-in  { from { translate: 100% 0; } }
@keyframes slide-out { to   { translate: 100% 0; } }

@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(*),
  ::view-transition-new(*) { animation: none; }
}
```

```js
function toggleDrawer() {
  if (!document.startViewTransition) return openDrawer();
  document.startViewTransition(() => openDrawer());
}
```

---

## Accessibility checklist (apply to every drawer)

- Trigger has `aria-expanded`, `aria-controls`, `aria-label` (or visible "Menu" text)
- On open: focus moves to first focusable element (or close button)
- Escape closes (FREE with `<dialog>.showModal()`)
- Focus returns to trigger on close
- Rest of page is `inert` (FREE with `showModal()`; manual otherwise)
- Visible focus styles via `:focus-visible` — never remove without replacing
- 44×44 minimum target on close (×) button
- Don't `aria-label="Hamburger"` — describe purpose (`"Open navigation"`)

---

## UX variants

- **Slide-in** — drawer overlays content; backdrop dims. Use for primary nav.
- **Push-aside** — content shifts. Janky on mobile, AVOID.
- **Fade overlay** — full-screen menu. Marketing sites with large hit targets.
- **Bottom sheet** — slides up from bottom. Mobile-preferred (thumb reach).

---

## When to use which (decision table)

| Context | Pattern | Why |
|---------|---------|-----|
| Marketing landing, ≤7 nav items | Minimal-JS disclosure (`hidden` toggle) | No modal needed |
| Admin app sidebar on mobile | `<dialog>` slide-in drawer | Focus trap + escape + top layer |
| Filter / action sheet on mobile | `<dialog>` bottom-sheet | Thumb reach |
| Settings panel on desktop | Side-sheet (not modal) | Doesn't block context |
| Confirmation prompt | `<dialog>` centered modal | Forces decision |

---

## Sources
- inclusive-components.design/menus-menu-buttons (Heydon Pickering)
- scottohara.me/code (Scott O'Hara accessibility)
- css-tricks.com/there-is-no-need-to-trap-focus-on-a-dialog-element
- schalkneethling.com/posts/html-dialog-native-solution-for-accessible-modal-interactions
- developer.chrome.com/blog/view-transitions-in-2025
- nngroup.com/articles/bottom-sheet
- m3.material.io/components/bottom-sheets/overview
