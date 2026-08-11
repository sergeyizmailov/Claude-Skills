# 01 — Infra & identity: antidetect, proxies, sessions

Chain Meta reads as one "user": FB profile → antidetect profile → proxy (exit
IP) → agency ad accounts/BM/pages. Inconsistency (two IPs, two devices, odd
hours) raises security score → checkpoint / session kill / restriction / disable.

## IP discipline (core rule)

This is operational session HYGIENE for a browser/user-token persona, not a Meta
authentication requirement — Meta does not mandate that API calls share the
browser's IP. It matters because a grey persona's whole trust rests on looking
like one consistent human; a server-side System User token (02) is exempt (no
browser session), but agency tenants rarely have one, so treat same-IP as the
default rule.

- Persona's entire life from ONE exit IP (the antidetect proxy): browser, API,
  token gen. Route scripts through the same proxy — read it from a secrets file,
  don't trust a human to VPN.
- Don't rotate casually (new IP = new signal). Change only when burned or
  unusably slow, then change BOTH ends (antidetect + scripts) together, keep it
  stable.
- Datacenter IPs = cheap, fast, risk factor; residential/mobile safer for the
  main persona. Agency setups usually ship a proxy — use theirs.

## socks5 vs socks5h (gotcha)

Script through `socks5h://` (DNS resolved BY the proxy). Plain `socks5://`
resolves DNS locally → TLS to graph.facebook.com dies with
`SSL: UNEXPECTED_EOF_WHILE_READING` (some sites load, TLS to big hosts fails).
Python: `pip install pysocks`, `proxies={"https":"socks5h://user:pass@ip:port"}`.
curl: `-x socks5h://user:pass@ip:port`.

## Sessions ↔ tokens

- API calls are stateless — they do NOT create sessions and can't "hang" as
  open sessions. "Leftover API sessions" is a myth.
- But the session a token was minted from dies on logout / password change /
  Meta security rotation / multi-session flag → the token dies with it, even a
  60-day one.
- Regenerating a token = a new login. During a flag every regen pokes the bear:
  regen once, exchange to long-lived immediately, stop.

## Restrictions & checkpoints (field guide)

- "You can't create multiple sessions" (~1 day): NOT a documented Meta rule
  (Meta allows concurrent sessions, no cap). It's an anti-abuse response to
  disparate-geo logins / cookie-token collisions from juggling personas on one
  device/IP. Freeze, let it expire, keep exactly ONE session. Fix is IP/device
  discipline, not a setting.
- Checkpoint (long load → logout): identity confirmation. Complete ONCE, calmly,
  from the antidetect profile. Repeated failures worsen it.
- Ad account disabled/restricted: normal background rate. Don't appeal fresh
  agency accounts — request replacement, keep a reserve pipeline.

## Domain / pixel rotation cadence (rotate before burn, not after)

Cadence is signal-driven, not a fixed clock:

- Domain: rotate on the SIGNALS, not a timer — rising bot_share / moderation
  crawlers on the white page, a spam/reputation flag, SSL or blocklist hit, or LP
  CTR collapse with normal clicks (tracker-ops/03). Keep fresh domains
  pre-provisioned (valid SSL, DNS propagated, slightly aged) so rotation is
  instant; a same-day scramble bleeds spend. Rotate the domain, not the whole
  funnel, so you can attribute the burn.
- Pixel: it's an asset WITH history — rotating it is costly (new pixel = cold,
  re-learns, custom audiences reset), so don't rotate reactively. The real lever
  is PRE-SEGMENTING to contain blast radius: separate pixels per domain-cluster /
  risk tier instead of one pixel across everything, so a burned funnel doesn't
  take the shared pixel (and its learning) down with it. By the time a pixel is
  flagged it's usually too late to save — the decision is upstream.
- Never rotate domain + pixel + creative + account together — you lose which one
  actually burned (fb-grey-ops/06 balanced designs).

## Where sessions live (current UI)

Accounts Center → Password and security → Where you're logged in
(https://accountscenter.facebook.com/password_and_security; old
facebook.com/settings?tab=security redirects/dies). Non-setup geos = the leak
that flagged the persona.

## Human behavior

- Open FB/developers/business sites for a work persona ONLY inside its
  antidetect profile — never a daily browser, not "for a second".
- No mass actions on a fresh profile: a few logins, some browsing, then work.
  Profile creation → ads on day 0 is a classic ban path.
- One action at a time when unstable. Batch API edits (rename, pause) are fine;
  profile/security edits agitate the system.
