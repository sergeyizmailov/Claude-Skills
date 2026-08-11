---
name: js-obfuscation
description: Use when obfuscating JavaScript, building anti-detection layers, evading Google Safe Browsing, hiding payloads from scanners, adding anti-bot/anti-DevTools protection, or preparing phishing/red-team pages for deployment
---

# JS Obfuscation & Anti-Detection

Professional-grade obfuscation pipeline for offensive JS payloads.

## Architecture: Defense-in-Depth Layers

```
Request arrives
  │
  ├─ L1: Server-side cloaking (IP/ASN/GeoIP) → see anti-bot.md
  │   ├─ L2: CAPTCHA gate (Turnstile) → see anti-bot.md
  │   │   ├─ L3: JS anti-bot (webdriver, fingerprint, behavior) → see anti-bot.md
  │   │   │   ├─ L4: Encrypted payload (AES/XOR/Unicode) → see encryption.md
  │   │   │   │   └─ L5: Obfuscated JS (javascript-obfuscator) → see obfuscator-configs.md
  │   │   │   └─ L6: One-time URLs (single use, then 404)
  │   │   └─ Anti-DevTools → see anti-devtools.md
```

Without L1 everything else just delays detection. With L1, site can live weeks.

## Quick Decision Guide

| Scenario | Layers to apply |
|----------|----------------|
| Quick red team page | L5 (obfuscator balanced) + anti-DevTools |
| Production phishing with longevity | All 6 layers |
| Landing page (BitB popup) | L3 (anti-bot) + L5 (obfuscator) + anti-DevTools |
| Cloudflare Worker | L1 (ASN via CF) + L4 (encrypted payload) + L5 (obfuscator) |
| Email attachment HTML | L4 (AES, key in URL fragment) + L5 (obfuscator max) + anti-DevTools |

## Safe Browsing Evasion Checklist

1. Server-side IP/ASN filter — crawlers never see payload
2. CAPTCHA gate — automated scanners can't solve
3. JS anti-bot — headless/sandbox detected and redirected
4. Encrypted payload — no static malicious HTML in source
5. Obfuscated JS — no signature matches (`password`, `eval(atob(` etc. hidden)
6. One-time URLs — reported link is already dead
7. Domain rotation — flagged → auto-switch to reserve
8. Delayed execution — `setTimeout` 3-5s, scanners have short budgets
9. Interaction-gated — require real click/scroll before payload
10. `domainLock` — code redirects on wrong domain (VirusTotal, sandbox)

Does NOT work: client-side blocking of `safebrowsing.googleapis.com` — checks happen at browser level before page JS.

## VirusTotal / PhishTank Evasion

- No static signatures — all encrypted/dynamic
- CAPTCHA gating — crawlers can't solve
- One-time URLs — reported → 404
- Legit hosting (`.workers.dev`, `.pages.dev`, `.netlify.app`) = high reputation
- Aged domains (.com, 2+ years) flagged slower
- Email whitelist — only serve if email matches target list (Cephas pattern)
- `domainLock` in obfuscator — code breaks on wrong domain

## Cloudflare WAF Compatibility

- No static malicious signatures — all encrypted/dynamic
- Use Turnstile — CF sees "protected site"
- Workers/Pages hosting gets less scrutiny
- Avoid trigger patterns: `eval(atob(`, obvious base64 HTML, known kit signatures
- Use RC4/AES instead of raw base64

## What to Obfuscate vs Not

**Yes:** Tracking scripts, form handlers, exfil logic, CF Worker code, any custom frontend JS.

**No:** Server-side code, Nginx/HAProxy configs, CSS, HTML structure, proxied content, Docker internals.

## One-Time URLs

```python
active = {}

@app.route('/<token>')
def land(token):
    if token in active:
        del active[token]
        return render_page()
    return '', 404
```

## Common Mistakes

1. Using only obfuscation without server-side filtering
2. `base64` instead of RC4/AES — `atob()` is a detection signature
3. Hardcoded URLs in source — construct dynamically or decrypt at runtime
4. No `domainLock` — code runs on VirusTotal → flagged
5. `renameGlobals: true` without testing — breaks external scripts
6. Skipping mouse check — sandboxes bypass webdriver but don't move mouse
7. Static CAPTCHA — if cached forever, scanner reuses session
8. Same code for every visitor — polymorphic mutation prevents signatures

## Reference Files

- `obfuscator-configs.md` — javascript-obfuscator presets (balanced/max/light), CLI commands, options reference
- `anti-bot.md` — anti-bot, anti-sandbox, CDP detection, server-side cloaking, Turnstile gating
- `anti-devtools.md` — 7 anti-DevTools methods, disable-devtool npm
- `encryption.md` — AES-256-GCM, XOR, invisible Unicode, DOM cloaking, polymorphic JS
- `phaas-reference.md` — 11 PhaaS kits (2025-2026), techniques by category, stats
