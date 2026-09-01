# Playbook — iGaming / Casino / Betting

Status (reviewed 2026-08-28): directional vendor benchmarks (dated below) + verified Meta policy.
NOT this team's live data — replace with your own numbers.

Execution order for an API launch is `references/00-launch-runbook.md`; this file supplies
the casino-specific parameters it asks for (gate, event ladder, optimization event, kill
numbers). Read it alongside, not instead.

**Gate before anything here:** A&V authorization + per-jurisdiction licence, filed **before any ad
exists**, with intent declared per new territory. **19 markets take no gambling ads at any authorization
level** — named list and the social-casino carve-out in `references/10-no-path-and-permissions.md`.
Approvals bind to a specific portfolio and ad account, so a replacement account needs a new one (`09`).

Funnel: FB/IG ad → pre-lander (bonus/winner story, app-style) → casino landing
or PWA/WebView app. Common grey bridge: FB → Telegram bot → deposit. Lead =
registration; the paying gate = FTD (first deposit), sometimes qualified FTD.

## Event ladder & KPI

click → LP/bot → **registration** → **FTD** → (qualified FTD / baseline KPI) →
rebills/RevShare. Primary KPI = CPA per FTD (or qualified FTD), not per reg.
Quality delay: FTD can lag registration by hours–days; reg→FTD and CPA mature on
a cohort — judge on click-date cohorts (tracker-ops 01), not same-day.

## Economics

Vendor-band numbers are directional priors — replace with your live data (SKILL.md).
THREE DIFFERENT metrics people conflate — keep them apart:

Conversion rates:
| rate | band |
|---|---|
| reg → FTD (FB traffic) | 15-25% after ~4wk warmup; FB/ASO 30-50% |
| reg → FTD (overall) | 20-50% GEO/source; strongest EU 47-50%; CIS/EE 17-19% |
| FTD as % of clicks | ~5-15% |
| FB→TG bot funnel | LP→bot join 25-35%; bot→deposit 8-12% |

Affiliate PAYOUT per FTD (what you EARN from the program):
| tier | payout |
|---|---|
| T1 EU | $250-500 (€400-650); via FB ~$90-100, up to $500-700 high-intent |
| NA / LATAM / SEA | NA $300-500; LATAM $50-200 (low <$35); SEA $60-150 |
| Asia / Africa | East Asia $100-250; South Asia $30-90; Africa $5-15 |
| RevShare (alt model) | 25-50% (top 55-60%) |

Player VALUE & your media cost (NOT the payout, NOT each other):
| metric | band |
|---|---|
| FTD deposit value (player) | T1 $180-350; T2/T3 $50-80 |
| your CPC (what you pay Meta) | FB T1 $0.60-1.20; CIS $0.10-0.30 |
| your CPI | PWA $0.50-1.80; WebView $0.80-2.50 |

Your media CPA per FTD (spend ÷ FTDs) is what you PAY and must sit below the
payout above — it's a fourth number, measured from your own spend, not quoted here.

Named programs (single-source case, Partnerkin Oct 2025 — weight low): 1Win
$200-400+RS40%, Welcome.Partners $150-320, Pin-Up $100-280, Leadshub $180-350,
Pelican $120-250 (no-KYC crypto).

## Creative concepts & first tests

Slots gameplay / big-win reactions / bonus offers. App-style creatives for
PWA/WebView funnels. First test: 2-3 angles 1-3-1 (directional screening, not a
causal test — see 04); optimise to reg where FTD
volume is too thin to optimise on directly, then switch to the deposit event
once volume builds (meta-grey-ops/04 event-volume lever).

## Common failure modes

- Optimising to cheap regs that don't deposit — advertisers scrub non-FTD
  traffic; a low-CPA-reg GEO with poor reg→FTD loses money.
- FTD event too sparse to exit learning on fresh accounts → optimise reg first.
- App funnel tracking broken (MMP event not mapped) → FTDs invisible, looks dead.

## Policy + tracking (docs-level, verified Aug 2026)

- Real-money gambling allowed ONLY with prior WRITTEN PERMISSION: advertiser
  applies via Authorizations & Verifications tab (Meta Business Suite) + proves
  a regulator license per target territory (territory-scoped, 18+). Without it
  only offline gambling promo. Grey teams run unauthorized → pay in account
  burn; plan the replacement pipeline.
- Tracking: PWA/H5/web-checkout = WEB (tracker postback + Pixel/CAPI; carry
  fbclid through the smart-link) — the common grey path, no app-store gate.
  FB → Telegram Mini App / bot: no Pixel; CAPI from the bot with a **short
  token**, not raw fbclid (`tracker-ops/03`).
  Native app = MMP (AppsFlyer/Adjust) SDK → S2S postbacks to Meta (needs UA+IP
  for CAPI); app-promo campaigns need the app registered + a Meta SDK/certified
  MMP source with events mapped. Pin which event = FTD in the MMP, mirror to the
  tracker/advertiser postback.
  Messenger/ManyChat JSON flows: still the CTM greeting+thread gate (`07`) — no
  web LP, not a skip past thread review.

## APP_PROMOTION / rented WebView [practitioner, MagicClick, fetched 2026-08-30]

Store-shell, not web cloak. Do not port PHP-white onto this lane.

- Objective `APP_PROMOTION`. Review sees the Play listing / in-app placeholder; user
  hits the offer in the WebView.
- Apps last ~**1 week** then Play-dead — **re-share a new app into the live campaign**,
  don't rebuild.
- Optimize in-app **Purchases** for FTD (not install). Audience Network = junk quality.
  OS **10+** for payer quality; 7+ only for reach.
- Deep link / campaign naming is the offer router (AppsFlyer OneLink or network bot).
  Wrong name → recreate; it caches.
- Payment method reused **>10× → Risks** (vendor). Card vendors → `03`.
- DE+AT first (same EUR/PPP); CH later (higher CPM, CHF, iOS-heavier). Kill one GEO
  without stopping the campaign: Page → Followers → Country Restrictions "Show only
  to…". [MagicClick 2026]

## TR PWA catalog-camouflage launch (field-tested 2026-08-30, own BM+app, single acct)

End-to-end validated: build → review pass on white → API set-swap → delivery on slots.

- **Catalog**: the **≥4 products in set** limit is Collection-format-only (storefront hero + cards;
  error 2490457). At submission the
  advertised set = all-white cards (electronics); slot arts pre-uploaded in catalog (Eligible
  independently) but OUT of the set. Post-approval: swap set to slot arts via API filter — no ad
  re-review (04). Never let set drop below 4. Alternative shape: regular catalog ad with a
  **1-product set** — renders as one deep-linked card, no minimum (04); image card via
  `force_single_link: true`, or VIDEO card via catalog-item video + `format_option:"single_video"`
  (Dynamic Media, 04). Looks like a plain ad instead of a storefront.
- **Campaign**: OUTCOME_LEADS → optimize CompleteRegistration (reg volume; FTD too sparse on small
  budgets), switch to Purchase at ~20-30 FTD via NEW campaign. Lowest cost, CBO per concept
  ($60-90 each), 1 adset/ad per campaign. TR broad 21+, all placements, Advantage+ creative OFF,
  multi-advertiser OFF pre-activation (04). Attribution 1-day click/view at create (default 7d
  inflates CPL numbers).
- **Kill numbers** (ladder 04, target CPL_reg $12 example): ad spend $36/0 regs kill, $57/≤1,
  $76/≤2; FTD verdict only on matured click-date cohorts (reg→FTD 15-25% band); spend-without-FTD
  stop at ~2× target CPA_FTD on matured data.
- **Tracking holes**: catalog-card clicks bypass ad url_tags (no sub1-4) unless deep-link override
  — subid capture must live in the landing builder, not the ad link. Set/catalog changes propagate
  to ad render with 15-60 min lag; preview popups cache — verify via API, not previews.

## pwa.bot funnel builder (vendor, docs.pwa.bot 2026-08-30)

PWA landing builder: built-in tracker, geo-cloak, CAPI. TR casino teams run FB Ads → PWA → offer.

- Offer link macros: `{user_id}` = visitor id, the ONLY join key (**no `{subid}` macro** — wrong
  macro = postbacks never match = zero CAPI events, funnel looks dead). Incoming ad params
  addressable by key: `&sub1={sub1}`.
- Postbacks (paste into ПП S2S): `api.pwa.bot/postback/?user_id={visit_id}&event=reg` /
  `...event=dep&value={profit}&currency=usd` (usd only). Exact URLs incl. pwaId from ЛК → Аналитика.
- CAPI: dataset id + token in ЛК → Аналитика (System User token works — 02). Default map: install→
  Lead, reg→CompleteRegistration, dep→Purchase. Pixel NOT injected into PWA by default (CAPI-only)
  — inject via `fbp=<dataset_id>` URL param or ЛК toggle if browser events wanted.
- Test server events: Events Manager test_event_code → ЛК → Аналитика → «Пульс» → Test Events.
- Geo-cloak: non-target-geo IPs (office, US crawlers) get whitepage → remote curl QA always shows
  white; user-branch test only via target-geo proxy. Real-geo postback loop test: fire manual
  postback with a live visit_id, watch Events Manager.
- Other builders (Monster PWA, PWA.Group, APEX, Comsign) + universal QA gates → `11-pwa-funnel-builders.md`.

## Metrics discipline

- Pin which tracker event = payout (reg? FTD? qualified FTD?) before any CPA
  math (tracker-ops metric rule). FTD lags → cohort by click date.
