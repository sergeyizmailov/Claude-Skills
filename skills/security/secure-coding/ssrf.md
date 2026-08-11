# SSRF & Prototype Pollution

Server-side request forgery prevention (URL parsing, DNS resolution,
private IP blocking, redirect handling) and prototype pollution defense
(safe deep merge, `Object.create(null)`).

Related: `express.md` · `uploads.md`.

## SSRF Prevention

```javascript
const { URL } = require('url');
const dns = require('dns').promises;
const net = require('net');

async function isSafeUrl(urlStr) {
  const url = new URL(urlStr);
  if (!['http:', 'https:'].includes(url.protocol)) return false;
  if (url.hostname === 'localhost' || url.hostname === '127.0.0.1') return false;

  const addresses = await dns.resolve4(url.hostname);
  for (const addr of addresses) {
    if (net.isIP(addr) && isPrivateIP(addr)) return false;
  }
  return true;
}

function isPrivateIP(ip) {
  const parts = ip.split('.').map(Number);
  if (parts[0] === 10) return true;
  if (parts[0] === 172 && parts[1] >= 16 && parts[1] <= 31) return true;
  if (parts[0] === 192 && parts[1] === 168) return true;
  if (parts[0] === 127) return true;
  if (parts[0] === 169 && parts[1] === 254) return true;
  if (parts[0] === 0) return true;
  return false;
}
```

SSRF bypass techniques attackers use:
- `http://0x7f000001` (hex IP) → 127.0.0.1
- `http://0177.0.0.1` (octal) → 127.0.0.1
- `http://2130706433` (decimal) → 127.0.0.1
- `http://localtest.me` → resolves to 127.0.0.1
- `http://[::1]` → IPv6 loopback
- Redirect-based: URL passes check, then 302 redirects to internal IP
- DNS rebinding: first resolve = public IP, second = 127.0.0.1
- `http://evil.com@127.0.0.1` → userinfo bypass

Defense: resolve DNS, check IP, disable redirects, re-check on every socket connect.
For production: use a dedicated egress proxy (Smokescreen, ssrfproxy) that
performs IP validation at connect-time — application-layer checks are racy.

## Prototype Pollution Prevention

```javascript
// VULNERABLE: deep merge without protection
function deepMerge(target, source) {
  for (const key in source) {
    if (typeof source[key] === 'object') {
      target[key] = deepMerge(target[key] || {}, source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}
// Attack: deepMerge({}, JSON.parse('{"__proto__":{"isAdmin":true}}'))

// SAFE: block dangerous keys
function safeDeepMerge(target, source) {
  for (const key of Object.keys(source)) {
    if (key === '__proto__' || key === 'constructor' || key === 'prototype') continue;
    if (typeof source[key] === 'object' && source[key] !== null && !Array.isArray(source[key])) {
      target[key] = safeDeepMerge(target[key] || {}, source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}

// SAFEST: use Object.create(null) for lookup objects
const config = Object.create(null);
```

Prototype pollution → RCE chain (real attacks):
1. Pollute `__proto__.shell` or `__proto__.NODE_OPTIONS`
2. Trigger child_process.spawn/exec/fork
3. Injected property overrides defaults → arbitrary command execution
4. CVE-2026-33660 (n8n): prototype pollution in XML parser → RCE
