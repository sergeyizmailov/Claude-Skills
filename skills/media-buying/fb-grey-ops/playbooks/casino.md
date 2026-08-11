# Playbook — iGaming / Casino / Betting

Status: directional vendor benchmarks (dated below) + verified Meta policy.
NOT this team's live data — replace with your own numbers.

Funnel: FB/IG ad → pre-lander (bonus/winner story, app-style) → casino landing
or PWA/WebView app. Common grey bridge: FB → Telegram bot → deposit. Lead =
registration; the paying gate = FTD (first deposit), sometimes qualified FTD.

## Event ladder & KPI

click → LP/bot → **registration** → **FTD** → (qualified FTD / baseline KPI) →
rebills/RevShare. Primary KPI = CPA per FTD (or qualified FTD), not per reg.
Quality delay: FTD can lag registration by hours–days; reg→FTD and CPA mature on
a cohort — judge on click-date cohorts (tracker-ops 01), not same-day.

## Economics (directional priors — NOT individually source-verified)

Cross-vendor bands (2025-26: Partnerkin, BigBetty, OptiKPI, RedClaw, irev).
Rough sanity ranges, not audited — confirm per program/GEO, replace with live
data. THREE DIFFERENT metrics people conflate — keep them apart:

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
once volume builds (fb-grey-ops/04 event-volume lever).

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
  Native app = MMP (AppsFlyer/Adjust) SDK → S2S postbacks to Meta (needs UA+IP
  for CAPI); app-promo campaigns need the app registered + a Meta SDK/certified
  MMP source with events mapped. Pin which event = FTD in the MMP, mirror to the
  tracker/advertiser postback.

## Metrics discipline

- Pin which tracker event = payout (reg? FTD? qualified FTD?) before any CPA
  math (tracker-ops metric rule). FTD lags → cohort by click date.
