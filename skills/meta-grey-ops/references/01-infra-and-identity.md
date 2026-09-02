# 01 — Infra & identity: antidetect, proxies, sessions

Reviewed 2026-08-28. **Practitioner doctrine, not Meta documentation** — nothing here
is [official]; validate against your own portfolio. Attribution method → `06`.

Chain Meta reads as one "user": FB profile → antidetect profile → proxy (exit IP) →
agency ad accounts/BM/pages. Inconsistency (two IPs, two devices, odd hours) raises
security score → checkpoint / session kill / restriction / disable.

## IP discipline (core rule)

Operational session hygiene, not a Meta auth requirement — Meta doesn't mandate API
calls share the browser's IP. Matters because a grey persona's trust rests on
looking like one consistent human. Server-side System User token (`02`) is exempt
(no browser session); agency tenants rarely have one, so default to same-IP.

- Persona's entire life from ONE exit IP: browser, API, token gen. Route scripts
  through the same proxy from a secrets file — don't trust a human to VPN.
- Don't rotate casually (new IP = new signal). Change only when burned or unusably
  slow, then change BOTH ends (antidetect + scripts) together.
- Datacenter IPs = cheap/fast/risk; residential/mobile safer for the main persona.
  Agency setups usually ship a proxy — use theirs.

## socks5 vs socks5h (gotcha)

Script through `socks5h://` (proxy resolves DNS). Plain `socks5://` resolves DNS
locally → TLS to graph.facebook.com dies with `SSL: UNEXPECTED_EOF_WHILE_READING`.
Python: `pip install pysocks`, `proxies={"https":"socks5h://user:pass@ip:port"}`.
curl: `-x socks5h://user:pass@ip:port`.

## Sessions ↔ tokens

- API calls are stateless — no sessions, can't "hang." "Leftover API sessions" is a
  myth.
- The session a token was minted from dies on logout / password change / Meta
  security rotation / multi-session flag → token dies with it, even a 60-day one.
- Regenerating a token = a new login. During a flag, every regen pokes the bear:
  regen once, exchange to long-lived immediately, stop.

## Restrictions & checkpoints

- "Can't create multiple sessions" (~1 day): not a documented Meta rule (Meta
  allows concurrent sessions) — anti-abuse response to disparate-geo logins/cookie
  collisions from juggling personas on one device/IP. Freeze, let expire, keep ONE
  session; fix is IP/device discipline, not a setting.
- Checkpoint (long load → logout): identity confirmation. Complete ONCE, calmly,
  from the antidetect profile — repeated failures worsen it.
- Ad account disabled/restricted: background rate. Don't appeal fresh agency
  accounts — request replacement, keep a reserve pipeline.

## Pre-buy / farmed-account QC [practitioner, MagicClick, 2026-08-30]

View-source logged-in Ads Manager HTML for `ADS_TRUST_TIER_`/`ADS_TRUSTED_TIER_` —
farmed-vs-newreg tell, **not** a spend cap (circulating dollar-tier tables are
vendor construction, already rejected in `09`). Empty Off-Facebook activity **or**
"Ads based on custom audiences" **or** no feed ads → likely not farmed. Empty Fan
Page = review flag. Still judge after $30-50 spend (SKILL #5). Chrome-agent driving
Ads Manager inside antidetect on rented seats → selfie/SMS/freeze risk.

## Domain / pixel rotation cadence (rotate before burn)

Signal-driven, not a fixed clock:

- Domain: rotate on signals — rising bot_share/moderation crawlers on the white
  page, spam/reputation flag, SSL/blocklist hit, or LP CTR collapse with normal
  clicks (`tracker-ops/03`). Keep fresh domains pre-provisioned (SSL valid, DNS
  propagated, slightly aged), run each through the pre-flight stack first
  (`google-grey-ops/05`: Safe Browsing/VirusTotal/Wayback/WHOIS). Rotate the
  domain, not the whole funnel, to keep attribution possible.
- Pixel: an asset with history — rotating is costly (new pixel = cold, re-learns,
  audiences reset), so don't rotate reactively. Real lever is pre-segmenting: split
  pixels per domain-cluster/risk tier so a burned funnel doesn't take the shared
  pixel down with it — but only as far as each dataset still gets enough events to
  optimize. By the time a pixel is flagged it's usually too late — decision is
  upstream.
- Never rotate domain + pixel + creative + account together — you lose which one
  burned (`06` balanced designs).

## Where sessions live

Accounts Center → Password and security → Where you're logged in
(`accountscenter.facebook.com/password_and_security`; old
`facebook.com/settings?tab=security` redirects/dies). Non-setup geos = the leak
that flagged the persona.

## Human behavior

- Open FB/developers/business sites for a work persona ONLY inside its antidetect
  profile — never a daily browser.
- No mass actions on a fresh profile: a few logins, some browsing, then work.
  Profile creation → ads on day 0 is a classic ban path.
- One action at a time when unstable. Batch API edits (rename, pause) are fine;
  profile/security edits agitate the system.
