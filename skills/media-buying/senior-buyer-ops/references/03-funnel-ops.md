# 03 — Funnel ops (end-to-end QA)

The dead zone between meta-ads (ad) and tracker-ops (numbers): the chain from
click to conversion. When leads vanish but delivery looks fine, it's almost
always here. Cloaking mechanics are assumed known — this is the QA that catches
where the chain silently breaks.

## Click-ID persistence (the #1 silent killer)

- The tracker click id / `subid` must survive EVERY hop: ad → tracker redirect →
  (cloaca white/black) → pre-lander → offer → postback. Each redirect or
  meta-refresh that drops the query string breaks attribution — leads fire but
  can't be matched, so the tracker shows near-zero while the offer records them.
- fbclid → CAPI (more than "pass it through"): capture `fbclid` on entry, but to
  attribute a web conversion back to Meta you format it into the `fbc` value
  (`fb.1.<timestamp>.<fbclid>`), send it with the other matching params (fbp,
  IP, UA, hashed email/phone) in the CAPI event, and set a shared `event_id` on
  BOTH the Pixel and CAPI events so Meta DEDUPLICATES them. Passing fbclid to the
  offer alone doesn't attribute — the fbc/event_id/dedup step is the actual work.
  A prelander that hard-links (new anchor, no params) severs it.
- Test: click a live ad end-to-end, watch the query string at each hop, fire a
  test conversion, confirm it lands on the right subid in the tracker.

## WebView / in-app browser / Telegram / PWA

- Ads open in the platform's IN-APP WebView (FB/IG). **Query string (`fbclid`)
  survives IAB** — Meta appends it; field logs show `FBAN/FBIOS` / `FB_IAB/FB4A`
  with `?fbclid=`. What does **not** survive is the **cookie jar**: WKWebView ≠
  Safari/Chrome. `_fbc` stays in the WebView; “Open in Safari” is a new session.
  Prefer S2S/CAPI (`fbc` from the query string) over a JS pixel that needs cookies.
  iOS Link Tracking Protection (17+) strips `fbclid`/`gclid` in Mail, Messages,
  Safari Private — Apple, not Meta. Do not put `fbclid={fbclid}` in Keitaro URL
  Parameters (placeholder blocks capture).
- PWA is WEB, not a native app: Pixel + CAPI + tracker postbacks + web
  attribution all apply — a PWA "install" is an add-to-home-screen, not a
  store install. Track it like web (carry fbclid/subid through, fire web events).
  An MMP/SDK is needed ONLY for a real native app or an app-store WebView wrapper
  — don't reach for MMP just because it's called a "PWA app" (casino playbook).
- TG bot / Mini App: Pixel inside Telegram WebView is unreliable. CAPI from the
  bot/backend is the path. Short token in `start`/`startapp`, **never raw
  `fbclid`** (64-byte / charset limits). Payload → `tracker-ops/03`.

## Domain / transport health (rotating grey domains)

- Fresh/rotated domains: SSL cert must be provisioned and valid BEFORE traffic
  (cert lag or mismatch → browser block → LP CTR collapses to ~0 with normal
  clicks). DNS fully propagated. Check the cloaca gate returns the black page to
  real users and white to reviewers from the target GEO (not your office IP).
- GEO latency: a slow pre-lander in-GEO tanks LP CTR / CR independent of
  creative — test page speed from the target country (not from your location),
  budget for a CDN or in-region host on T2/T3.

## Forms / checkout / routing

- Validate the form/checkout actually submits in the target GEO on mobile
  (field validation, phone format, COD address fields). A broken field = leads
  that never reach the network.
- Routing/rotation: if a path rotates offers/landers, confirm each branch
  carries the click id and fires the same conversion contract.

## Version → result binding

Tag every funnel version (prelander vN, offer vN, path vN) so a result attaches
to the exact version that produced it — via a sub_id/token or the tracker's
lander/offer id. Without it you can't tell which prelander won and can't roll
back a regression. Bind the version in the mapping contract (tracker-ops/03).
