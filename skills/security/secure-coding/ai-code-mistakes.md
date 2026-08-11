# AI-Generated Code: Security Mistakes & Patterns

## The Problem (2025-2026 Data)

| Metric | Value | Source |
|--------|-------|--------|
| AI code vulnerability rate vs human | 2.74x higher | Veracode (100+ LLMs) |
| AI samples with OWASP Top 10 vulns | 45% | Veracode |
| XSS defense failure rate | 86% | Veracode |
| Log injection failure rate | 88% | Veracode |
| Privilege escalation paths | 322% more | Apiiro (Fortune 50) |
| Design flaws | 153% more | Apiiro |
| Secrets exposure jump | 40% more | Apiiro |
| AI-assisted commit secret leak rate | 3.2% (vs 1.5% baseline) | GitGuardian 2026 |
| New hardcoded secrets in GitHub (2025) | 28.65 million | GitGuardian |
| CVEs from AI code (Mar 2026) | 35 | Georgia Tech |
| Estimated true AI CVE count | 400-700 | Georgia Tech |
| Vibe-coded apps with critical vulns | 58% | Escape.tech (1,400 apps scanned) |

## Top CWE Patterns AI Gets Wrong

### 1. CWE-79: Cross-Site Scripting (86% failure rate)

AI generates:
```javascript
// AI output — VULNERABLE
app.get('/search', (req, res) => {
  res.send(`<h1>Results for: ${req.query.q}</h1>`);
});

// AI output — VULNERABLE
element.innerHTML = `<div class="user">${userData.name}</div>`;
```

Should be:
```javascript
app.get('/search', (req, res) => {
  const escaped = req.query.q.replace(/[&<>"']/g, c => ({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
  }[c]));
  res.send(`<h1>Results for: ${escaped}</h1>`);
});

element.textContent = userData.name;
```

### 2. CWE-89: SQL Injection

AI generates:
```javascript
// VULNERABLE — string interpolation
const user = await db.query(`SELECT * FROM users WHERE email = '${email}'`);

// VULNERABLE — even with "sanitization"
const safe = email.replace(/'/g, "''");
const user = await db.query(`SELECT * FROM users WHERE email = '${safe}'`);
```

Should be:
```javascript
const user = await db.query('SELECT * FROM users WHERE email = $1', [email]);
```

### 3. CWE-798: Hardcoded Credentials

AI generates:
```javascript
// VULNERABLE — secrets in code
const API_KEY = 'sk-proj-abc123def456';
const DB_URL = 'postgres://admin:password123@db.example.com:5432/prod';
const JWT_SECRET = 'super-secret-key-change-in-production';
```

Should be:
```javascript
const API_KEY = process.env.API_KEY;
const DB_URL = process.env.DATABASE_URL;
const JWT_SECRET = process.env.JWT_SECRET;
```

AI doubles the baseline secret leak rate because:
- Training data is full of example code with placeholder secrets
- LLMs can't distinguish "example" from "production"
- Copilot autocompletes real API keys from context

### 4. CWE-327: Cryptographic Failures

AI generates:
```javascript
// VULNERABLE — MD5 for passwords
const hash = crypto.createHash('md5').update(password).digest('hex');

// VULNERABLE — SHA256 without salt
const hash = crypto.createHash('sha256').update(password).digest('hex');

// VULNERABLE — weak JWT secret
jwt.sign(payload, 'secret', { algorithm: 'HS256' });
```

Should be:
```javascript
const hash = await argon2.hash(password, { type: argon2.argon2id });

const token = await new SignJWT(payload)
  .setProtectedHeader({ alg: 'RS256' })
  .sign(privateKey);
```

### 5. CWE-117: Log Injection (88% failure rate)

AI generates:
```javascript
// VULNERABLE — user data in logs
console.log(`Login attempt for user: ${username}`);
// Attack: username = "admin\nLogin successful for user: admin"
// Log file now shows fake successful login
```

Should be:
```javascript
const safeUsername = username.replace(/[\n\r\t]/g, '_');
logger.info({ event: 'login_attempt', user: safeUsername });
```

### 6. CWE-22: Path Traversal

AI generates:
```javascript
// VULNERABLE — user controls file path
app.get('/files/:name', (req, res) => {
  res.sendFile(path.join(__dirname, 'uploads', req.params.name));
  // Attack: GET /files/../../../etc/passwd
});
```

Should be:
```javascript
app.get('/files/:name', (req, res) => {
  const safeName = path.basename(req.params.name);
  const fullPath = path.join(__dirname, 'uploads', safeName);
  if (!fullPath.startsWith(path.join(__dirname, 'uploads'))) {
    return res.status(400).json({ error: 'Invalid path' });
  }
  res.sendFile(fullPath);
});
```

### 7. CWE-862: Missing Authorization

AI generates:
```javascript
// VULNERABLE — no auth check
app.delete('/api/users/:id', async (req, res) => {
  await db.query('DELETE FROM users WHERE id = $1', [req.params.id]);
  res.json({ ok: true });
});
```

Should be:
```javascript
app.delete('/api/users/:id', requireAuth, requireRole('admin'), async (req, res) => {
  await db.query('DELETE FROM users WHERE id = $1', [req.params.id]);
  res.json({ ok: true });
});
```

## Patterns AI Consistently Gets Wrong

### Missing Input Validation
AI rarely adds validation middleware. It trusts `req.body` and passes it directly to database operations. Always add Zod/Joi validation.

### Missing Rate Limiting
AI never adds rate limiting to auth endpoints. Login, register, password reset — all need strict limits (5 attempts / 15 min).

### Missing Error Handling
AI code uses `try/catch` but sends raw errors to client:
```javascript
// AI pattern — leaks info
catch (err) { res.status(500).json({ error: err.message }); }
// Attacker sees: "relation 'users' does not exist" → knows DB is Postgres
```

### Insecure Defaults
- `cors()` with no options = allow all origins
- `express.json()` with no `limit` = DoS via large payload
- `app.set('trust proxy', true)` = trusts all proxies (IP spoofing)
- Session cookies without `secure: true` and `httpOnly: true`

### Outdated Libraries
AI suggests old or deprecated packages:
- `request` (deprecated 2020) instead of `node-fetch` or `undici`
- `jsonwebtoken` instead of `jose`
- `bcryptjs` instead of `argon2`
- `body-parser` instead of `express.json()` (built-in since Express 4.16)
- `csurf` (deprecated) instead of `csrf-csrf`
- `express-validator` v4 instead of v7 or `zod`

## AI Code Review Checklist

Before accepting ANY AI-generated code, verify:

- [ ] No hardcoded secrets, API keys, tokens, passwords
- [ ] No `eval()`, `new Function()`, `setTimeout(string)`
- [ ] No `innerHTML` with user data (use `textContent` or DOMPurify)
- [ ] No string concatenation in SQL/DB queries
- [ ] No `res.send(error.message)` or `res.send(error.stack)`
- [ ] All endpoints have auth middleware
- [ ] All user input validated (Zod/Joi, not manual checks)
- [ ] Rate limiting on auth endpoints
- [ ] `express.json({ limit: '10kb' })`
- [ ] `cors()` has explicit `origin` list
- [ ] Cookies have `httpOnly`, `secure`, `sameSite`
- [ ] JWT verification specifies `algorithms` array
- [ ] File paths use `path.basename()` or validated against root
- [ ] URLs validated before `fetch()` (no SSRF)
- [ ] Dependencies pinned to exact versions
- [ ] No deprecated packages

## OpenSSF Guidance (Sep 2025)

Key recommendations from OpenSSF Security-Focused Guide for AI Code Assistants:

1. **Write security requirements in prompts** — "use parameterized queries", "validate all input", "no hardcoded secrets"
2. **Don't tell AI it's a security expert** — this causes overconfidence and skipping basics
3. **Use Recursive Criticism and Improvement (RCI)** — ask AI to review its own code for security issues, repeat
4. **Never trust AI output blindly** — treat as untrusted junior developer code
5. **Run automated scanning** — `npm audit`, SAST tools (Semgrep, CodeQL), before merging
6. **Pin dependencies explicitly** — AI suggests `^` versions by default

## Real Incidents (2025-2026)

**Moltbook breach**: Entirely AI-generated app. Within 3 days, researchers found exposed production database with 1.5M API tokens, 35K email addresses, and private messages.

**Copilot prompt injection** (CVE-2025-53773, CVSS 9.6): Hidden prompt in PR description → Copilot executes arbitrary code during review.

**CamoLeak** (CVE-2025-59145, CVSS 9.6): Prompt injection extracts API keys and private source code from Copilot context.

**35+ CVEs in March 2026**: Direct result of AI-generated code deployed to production without review.
