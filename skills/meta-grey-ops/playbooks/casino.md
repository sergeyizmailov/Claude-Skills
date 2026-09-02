# Playbook — iGaming / Casino / Betting

Reviewed 2026-08-28. Vendor benchmarks below are directional priors, not this team's live data — replace once you have your own. Execution mechanics → `00`; casino-specific parameters (gate, event ladder, optimization event, kill numbers) here.

**Gate:** A&V authorization + per-jurisdiction licence, filed before any ad exists, intent declared per new territory. 19 no-gambling markets, social-casino carve-out → `10`. Approvals bind to portfolio+account — replacement account needs new approval (`09`).

**Objective/event:** OUTCOME_LEADS → optimize CompleteRegistration first (FTD too sparse on small budgets); switch to Purchase (FTD) at ~20–30 FTD via a NEW campaign. Primary KPI = CPA per FTD, not per reg — judge on click-date cohorts, FTD lags reg by hours–days.

**Funnel/tracking:** FB/IG ad → pre-lander → casino LP or PWA/WebView, or FB→Telegram bot→deposit.
- PWA/H5/web-checkout: WEB tracking (tracker postback + Pixel/CAPI, carry fbclid through smart-link) — no app-store gate.
- FB→TG bot: no Pixel; CAPI from bot with a short token, not raw fbclid (tracker-ops/03).
- Native app: MMP (AppsFlyer/Adjust) SDK → S2S to Meta (needs UA+IP); pin which MMP event = FTD, mirror to tracker.
- Messenger/ManyChat: still CTM greeting+thread gate (`07`) — not a review skip.

**Creative constraints:** Slots gameplay / big-win reactions / bonus offers; app-style for PWA/WebView. 2–3 angles 1-3-1 screening (directional, not causal — `04`).

**Review traps:**
- Catalog camouflage (TR field-tested 2026-08-30): ≥4-product-set limit is Collection-format-only (error 2490457); submit with all-white cards, slot arts pre-uploaded but out-of-set, swap via API filter post-approval — no re-review. Never let set drop below 4. Alt: 1-product set renders as single deep-linked card, no minimum; `force_single_link: true` or catalog-item video + `format_option:"single_video"`.
- Catalog-card clicks bypass ad url_tags (no sub1-4) — subid capture must live in the landing builder. Set/catalog changes propagate to render with 15–60 min lag; preview popups cache — verify via API, not previews.
- APP_PROMOTION/rented WebView [MagicClick 2026]: store-shell, not web cloak — do not port PHP-white here. Apps last ~1 week then Play-dead → re-share a new app into the **live** campaign, don't rebuild. Optimize in-app Purchases (FTD), not install. Audience Network = junk. OS 10+ for payer quality, 7+ only for reach. Deep link/campaign naming is the offer router (AppsFlyer OneLink or bot) — wrong name → recreate, it caches.

**What kills the account:**
- Running gambling without A&V authorization → burn, not rejection; plan replacement pipeline.
- Optimizing to cheap regs that don't deposit — advertiser scrubs non-FTD traffic.
- Payment method reused >10× → flagged "Risks" [vendor] — card vendors → `03`.
- Broken app-event mapping → FTDs invisible, looks dead, gets killed as non-performing.

**Kill numbers** (ladder in `04`, target CPL_reg $12 example, 2026-08-30 field test): spend $36/0 regs kill, $57/≤1, $76/≤2; FTD verdict only on matured click-date cohorts (reg→FTD 15–25% band); spend-without-FTD stop at ~2× target CPA_FTD on matured data.

**Economics (vendor bands, 2025-10/2026 sources — replace with live data):**
| Metric | Band |
|---|---|
| reg→FTD (FB traffic) | 15–25% after ~4wk warmup; FB/ASO 30–50% |
| reg→FTD (overall) | 20–50% by GEO; EU 47–50%, CIS/EE 17–19% |
| FTD as % of clicks | ~5–15% |
| Payout/FTD T1 EU | $250–500 (via FB ~$90–100, up to $500–700 high-intent) |
| Payout/FTD NA/LATAM/SEA | NA $300–500; LATAM $50–200 (low <$35); SEA $60–150 |
| RevShare alt model | 25–50% (top 55–60%) |
| Named programs (Partnerkin 2025-10, low weight) | 1Win $200–400+RS40%, Welcome.Partners $150–320, Pin-Up $100–280, Leadshub $180–350, Pelican $120–250 (no-KYC crypto) |

**GEO notes:** DE+AT first (shared EUR/PPP), CH later (higher CPM, CHF, iOS-heavier). Kill one GEO without stopping campaign: Page → Followers → Country Restrictions "Show only to…".

**Funnel builders:** pwa.bot join key `{user_id}` only (no `{subid}`), usd-only postback value, CAPI dataset+token via ЛК→Аналитика, pixel off by default (inject via `fbp=<dataset_id>`). Other vendors + universal QA gates → `11-pwa-funnel-builders.md`.

**Metrics discipline:** pin which tracker event = payout (reg? FTD? qualified FTD?) before any CPA math; cohort by click date.
