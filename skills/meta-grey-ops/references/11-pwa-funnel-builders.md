# 11 — PWA funnel builders (casino/iGaming)

Builders = PWA "install-page" landing + tracker + geo-cloak + CAPI forwarder, one per domain.
The contract is IDENTICAL across vendors; only macro spelling, postback host and test tooling
differ. Facts: vendor docs/bundles fetched 2026-08-30 (SPA sites — facts extracted from JS
bundles) + practitioner sources per line. Sources are mostly vendor blogs — practitioner-
documented, not neutral measurement.

## The universal contract — verify all five per vendor before spend

1. **Join key**: builder assigns a click id at entry and exposes it as an offer-URL macro. Spelling
   varies per vendor (see table). Wrong macro = literal in offer URL = postbacks never match =
   zero CAPI events, funnel looks dead. Test: substituted value visible in the offer URL.
2. **Postbacks IN** from the network: reg + dep; dep carries value + currency (rules differ:
   pwa.bot usd-only, MonsterPWA `{currency}`).
3. **CAPI forwarder**: dataset id + token; canonical map install→Lead, reg→CompleteRegistration,
   dep→Purchase. Require shared `event_id` pixel↔CAPI or deposits double-count.
4. **Cloak**: non-target geo / crawler UA / datacenter IPs → whitepage. Remote curl QA always
   shows white — user-branch test only from target geo (proxy/SIM).
5. **Test tooling**: test-event feature or manual postback fire; check Events Manager Test Events.

## Vendor table (fetched 2026-08-30)

| builder | join macro | postback IN | FB events | cloak | notes |
|---|---|---|---|---|---|
| **pwa.bot** | `{user_id}` (only join macro; `{subid}` does NOT exist) | `api.pwa.bot/postback/?user_id={...}&event=reg\|dep&value={profit}&currency=usd` (usd only) | install→Lead, reg→CompleteRegistration, dep→Purchase | geo whitepage ("Stope page") | test: «Пульс» + test_event_code; pixel off PWA unless `fbp=<dataset_id>` param; full block → playbooks/casino.md |
| **Monster PWA** (monsterpwa.com) | `{external_id}` + `{subId}` (case-insensitive) | `pwac.world/postback?external_id={external_id}&event=reg\|dep&value=&currency=` | install→Lead, open→ViewContent, reg→CompleteRegistration, dep→Purchase; CAPI delivery logs; event_id dedup undocumented | built-in cloaca + Adspect; device rules; per-country PWA mapping; white from Play/AI | only vendor publishing the full inbound postback contract |
| **PWA.Group** | per-network click_id (templates); outgoing as `{get_PARAM}` | template postbacks, reg/dep separate | install→Lead auto; "no duplicate events" toggle = dedup | "non-target GEO" whitepage + filter module | macro list via support TG; pixel+token CAPI |
| **APEX** (app.apex-pwa.com) | clickid persisted across install; macro unpublished | Keitaro/Binom/RedTrack/Voluum S2S guides; reg/dep/qualified | event_id dedup documented; pixel per domain (survives rotation) | cloaca + antibot: geo, ASN/datacenter, VPN, UA, JS-challenge; `?nc=1` bypass | EMQ/Test Events guide; HTTPS auto |
| **Comsign** (comsign.io) | docs in-app only | — | pixel insertable on safe page | modes Strict/Money/Flexible/Manual; AI whites; 48-lang; HTML randomization | moderation-protection positioning |

Dead / no public docs 2026-08-30 (don't waste time): AFFPRO, app-pwa.com, ipwa.io, pwabudget.com,
pwawave.com, pwa2win.com, appsb.io (dead/parked); EpicPWA, PWA.Market (live, doc-opaque).

## Failure modes (each documented in the wild, 2026 sources)

- Click-id stripped by any redirect/builder hop → "once gone, no postback reconstructs it"
- Postback status macros mismatched to pixel events → FB optimizes the wrong target
- reg+dep+rebill flattened into one generic Purchase → optimization poisoned toward non-payers
- pixel+CAPI without shared event_id → deposits double-counted; event_ids generated independently
  per side = the common bug
- EMQ: capture fbc/fbp/external_id at click; fbc expires after 7 days; pixel-only EMQ 3–5 vs 6–8
  with postbacks; 20–30% of purchases lost to browser prevention recoverable via CAPI
- `test_event_code` left live routes real events to the test panel
- Expired System User token silently cuts the CAPI feed
- Network batching postbacks past the attribution window
- `{{placement}}`/`{{site_source_name}}` macros return empty in some ASC/catalog configs
- iOS Link Tracking Protection strips fbclid in Mail/Messages/Safari-private

## QA gates before scaling

1. Walk click→deposit end-to-end in the tracker's live UI; substituted join-key visible at every hop
2. Test events: event_name/value/event_id correct; pixel+CAPI share the same event_id; EMQ ≥6
3. Postback delivery logs clean (no 404/timeout); weekly health audit after
4. Target-geo SIM, mid-range Android: PWA loads <2s on 3G; per-OS install instructions (separate
   iOS/Safari page)
5. Events Manager diagnostics 2–3 days live → then remove test_event_code; keep a 5–10 domain pool
   with rotation plan (Meta flags domains system-wide — a URL seen in a banned ad underperforms
   even from new accounts)
6. reg→FTD split diagnostic: installs high/regs low = onboarding problem; regs high/FTD low =
   payments or traffic quality

## Numbers (practitioner/self-reported bands — no independent audit)

click→install 18–35% PWA (vs 8–14% mobile landing) · install→reg 40–60% · reg→FTD 10–20% ·
click→FTD 3–7% solid · case: Meta installs $1.2–1.5, FTD ~$30 · deep links +20–40% FTD CR · local
payments +25–40% deposit CR · push campaigns +20–30% FTD lift. Sources: affhub.media 2026-01-09,
affstudio.org 2026-03/05, partnerkin 2026-06.

**Moderation reality**: NordVPN (2026-07-30) logged a 400+ domain network serving fake Play-style
"clean" pages to automated review (3,100+ instances) vs 7,200 casino-page instances — proof Meta
adversarially re-crawls at scale. Treat the funnel as a window, not immunity: rotate domains/
accounts, expect re-crawl, keep the white set intact until every first review is done.
