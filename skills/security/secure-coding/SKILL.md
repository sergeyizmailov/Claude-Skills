---
name: secure-coding
description: Use when writing JavaScript, Node.js, HTML, CSS code for websites, landing pages, admin panels, APIs. Reduces common vulnerability classes (XSS, injection, SSRF, etc.) via secure libraries, proper headers, and safe patterns. Includes AI code vulnerability patterns.
---

# Secure Coding (JS / Node.js / HTML / CSS)

Apply automatically when writing any web code. Every output should be hardened
by default — this skill reduces common vulnerability classes (OWASP Top 10,
CWE-79/89/918/22/502 etc.) but does not guarantee absence of bugs. Validate
deployment topology (reverse proxy, TLS termination, CDN) before applying
defaults like `trust proxy`, HSTS `preload`, or cross-origin isolation headers.

## Why This Matters (2025-2026 Reality)

- AI-generated code has **2.74x more vulnerabilities** than human-written (Veracode, 100+ LLMs tested)
- **45%** of AI code samples introduce OWASP Top 10 vulnerabilities
- **86%** fail XSS defense, **88%** vulnerable to log injection
- **35 new CVEs** from AI-generated code in March 2026 alone
- Hardcoded secrets in AI-assisted commits: **3.2%** rate (vs 1.5% baseline — 2x higher)
- CVE-2025-55182 (React2Shell): CVSS 10.0 RCE via single HTTP request, near-100% exploit reliability

## Workflow

### When writing new code

1. Start with secure defaults: helmet, cors (explicit origins), rate-limit, body size limit
2. For each endpoint: auth middleware → input validation (zod) → parameterized queries → generic error responses
3. Before finishing: scan output against the "Never Do" table below — if any anti-pattern slipped in, fix it
4. Check dependencies before adding (prefer `context7` MCP when available;
   fall back to npm registry / GitHub / GHSA when not):
   - Verify latest stable version (never use known-outdated)
   - Check for open critical/high CVEs and GHSA advisories
   - Confirm maintainer is active (responds to issues, security patches land
     within reasonable time) — raw commit cadence is a poor signal; mature
     crypto/security libs like `argon2`, `helmet`, `jose` can sit quiet for
     months and still be canonical. Disqualify only on: deprecated, archived,
     unanswered CVE > 90 days, ownership transferred to unknown party
   - Apps: rely on `package-lock.json` + `npm ci`. Libraries: use semver
     ranges in `package.json`; run audit in CI
   - Prefer packages from Safe Library Stack below

### When auditing existing code

1. Scan project structure: find entry point, routes, middleware chain, static file serving
2. Check dependencies: `npm audit`, pinned versions, known compromised packages
3. Check configs: NODE_ENV, exposed files (.env, .git, source maps), debug endpoints
4. Walk each route: auth → validation → data handling → error responses
5. Check infrastructure: headers, CSP, CORS, cookies, open ports
6. Output findings using the format below

### Audit output format

```
### [CRITICAL/HIGH/MEDIUM/LOW] Finding title
- **Location**: file:line
- **Vulnerability**: CWE-XXX (name)
- **Impact**: what an attacker can do
- **Fix**: specific code change or recommendation
```

## OWASP Top 10:2025 Quick Map

| # | Risk | How It's Exploited | Your Defense |
|---|------|--------------------|--------------|
| A01 | Broken Access Control | IDOR: change `/api/user/123` to `/api/user/124` | Auth check on EVERY endpoint, return 404 not 403 |
| A02 | Security Misconfiguration | Default creds, debug mode, verbose errors, exposed files | Helmet, CSP, no defaults, generic errors, block dotfiles |
| A03 | Supply Chain | Compromised npm packages (Shai-Hulud: 500+ packages) | Pin versions, `npm ci --ignore-scripts`, audit |
| A04 | Cryptographic Failures | Weak hashing, plaintext storage, broken TLS | Argon2id, AES-256-GCM, TLS 1.2+ only |
| A05 | Injection | SQLi, XSS, SSTI, prototype pollution, prompt injection | Parameterized queries, DOMPurify, no `eval()` |
| A06 | Insecure Design | No rate limit on login, no anti-automation | Rate limit, CAPTCHA, account lockout |
| A07 | Auth Failures | JWT `alg:none`, weak secrets, no session rotation | `jose` + RS256, strong secrets, regenerate on login |
| A08 | Integrity Failures | Tampered CDN scripts, unsigned updates | SRI hashes, verify signatures |
| A09 | Logging Failures | No auth logging, secrets in logs | Log auth events, NEVER log tokens/passwords |
| A10 | Exception Mishandling | Stack traces + DB errors leaked to client | Generic 500, detailed to server logs only |

## Never Do (hacker's wishlist)

| Bad Code | Attack | Impact |
|----------|--------|--------|
| `eval(userInput)` | Code injection | RCE |
| `innerHTML = userInput` | XSS | Session theft, keylogging |
| `db.query(\`...${id}\`)` | SQL injection | Full DB dump |
| `res.send(error.stack)` | Info leak | DB creds, paths, versions |
| `jwt.verify(token, key)` without `algorithms` | `alg:none` bypass | Auth bypass, admin access |
| `require(userInput)` | Path traversal | RCE, file read |
| `fetch(userUrl)` without validation | SSRF | Internal network scan, cloud metadata |
| `JSON.parse` + deep merge without check | Prototype pollution | RCE via gadget chain |
| `password = md5(input)` | Hashcat: 100B/sec on GPU | Full account takeover |
| `cors({ origin: '*' })` | Cross-origin access | Data theft from any domain |
| `cookie: { sameSite: 'none' }` without reason | CSRF | Unauthorized actions |
| `npm install` in CI | Supply chain | Malicious postinstall scripts |
| `/^(.+)+$/.test(userInput)` | ReDoS | Event loop freeze, full DoS |
| WebSocket without origin check | CSWSH | Session hijacking via any website |
| `SELECT ... WHERE` then `UPDATE` without lock | Race condition | Double-spend, duplicate actions |

## Safe Library Stack (2025-2026)

| Purpose | Use | Avoid | Why |
|---------|-----|-------|-----|
| Password hash | `argon2` / `@node-rs/argon2` | md5, sha256 | GPU-resistant, OWASP standard |
| JWT | `jose` (v6+) | `jsonwebtoken` | Maintained, universal runtime, no `alg:none` |
| HTML sanitize | `DOMPurify` (v3+) | regex sanitizers | 55% of sanitizers vulnerable to DOM clobbering |
| HTTP security | `helmet` (v8+) | manual headers | Sets 11 headers correctly by default |
| Rate limit | `express-rate-limit` + Redis | nothing | Login brute-force takes minutes without it |
| Validation | `zod` / `joi` | manual `if` checks | Type-safe, strips unknown fields |
| ORM | `drizzle-orm` / `prisma` | string concatenation | Parameterized by design |
| Session | `express-session` + Redis | cookie-only | Server-side storage, revocable |
| Template | Handlebars / Nunjucks (`autoescape:true`) | EJS `<%-` | Auto-escape prevents XSS |
| Regex | `re2` | nested quantifiers | Linear time, no catastrophic backtracking |

## Critical CVEs (2025-2026)

| CVE | Target | CVSS | Impact |
|-----|--------|------|--------|
| CVE-2025-55182 | React Server Components / Next.js | 10.0 | Pre-auth RCE via single HTTP request |
| CVE-2025-59465 | Node.js HTTP/2 | 7.5 | Server crash via malformed HEADERS |
| CVE-2026-33660 | n8n (AlaSQL + prototype pollution) | 9.4 | RCE via workflow nodes |
| CVE-2025-53773 | GitHub Copilot | 9.6 | RCE via prompt injection in source files |
| CVE-2026-3125 | OpenNext Cloudflare | High | SSRF via path normalization bypass |
| CVE-2025-59145 | GitHub Copilot (CamoLeak) | 9.6 | Secret exfiltration via prompt injection |
| Shai-Hulud | npm ecosystem | Critical | Self-propagating worm, 500+ packages |
| Axios compromise | axios 1.14.1 / 0.30.4 | Critical | RAT in 3-hour window (DPRK attributed) |

## Decision: When to Read Reference Files

Load only the files that match the concern at hand — each is focused.

| Concern | File |
|---------|------|
| Express baseline, rate limit, Zod validation, error handler, prod misconfigs | `express.md` |
| Password (Argon2id), JWT (`jose`), sessions, RBAC/ownership, timing-safe, JWT attacks | `auth.md` |
| Parameterized SQL, race conditions / TOCTOU, row locking, distributed locks | `db.md` |
| File upload (multer, MIME, magic bytes), path traversal | `uploads.md` |
| SSRF (DNS resolve, private-IP block, redirect handling), prototype pollution | `ssrf.md` |
| ReDoS (event-loop blocking regex), WebSocket / Socket.IO hardening, CSWSH | `dos.md` |
| GraphQL: introspection, depth/complexity, batching, field-level auth | `graphql.md` |
| Prompt injection / LLM apps: input filter, delimited prompts, output validation, tool least-privilege | `llm.md` |
| HTML/CSS/frontend: XSS, DOM clobbering, template injection, postMessage, iframe sandbox | `frontend-security.md` |
| HTTP security headers, CSP nonces, cookie flags, CORS | `headers-and-csp.md` |
| Dependencies, lockfiles, SRI, npm supply-chain attacks, emergency response | `supply-chain.md` |
| Reviewing AI-generated code, CWE statistics, OpenSSF guidance | `ai-code-mistakes.md` |
