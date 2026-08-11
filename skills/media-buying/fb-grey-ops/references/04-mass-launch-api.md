# 04 — Mass launch via API

Programmatic beats UI after ~2 accounts (identical structure, no misclicks,
naming enforced). All calls via setup proxy (01), long-lived token (02), app
Live (else creative creation fails).

## Structures

- 1-1-3 (1 camp, 1 adset, 3 ads): probe unknown accounts for delivery. Quirk:
  Meta dumps ~90% of adset budget into ONE ad — useless for comparing creatives.
- 1-3-1 (3 adsets, 1 ad each): cleaner SCREENING (each creative gets its own
  adset budget), but NOT a fair/causal test — audiences overlap across adsets and
  auction conditions differ, so read winners as directional. For a causal read use
  the A/B Test tool (measurement-experimentation-ops).
- CBO (daily_budget on campaign) is the common team pattern; 1-3-1+CBO is even
  less balanced (CBO reallocates toward the early leader). ABO splits budget
  evenly but multiplies spend — still not overlap-free.
- Scale: winners → 1-1-3 higher budget, or horizontal (more accounts), +20-30%/day.

## Bid strategies (set explicitly at campaign creation)

New CBO campaigns may default to LOWEST_COST_WITH_BID_CAP → adsets then reject
without bid_amount (error 1815857, field-observed). Enum:
- LOWEST_COST_WITHOUT_CAP — default workhorse.
- COST_CAP + bid_amount (cents) at adset — target cost/result; can choke if
  below market.
- LOWEST_COST_WITH_BID_CAP + bid_amount — auction ceiling, rare for leads.
- LOWEST_COST_WITH_MIN_ROAS + roas_average_floor — value/purchase funnels only.

## Working param set (lead funnels)

- Campaign: objective=OUTCOME_LEADS (ODAX enum: OUTCOME_AWARENESS/TRAFFIC/
  ENGAGEMENT/LEADS/SALES/APP_PROMOTION), buying_type=AUCTION,
  special_ad_categories=[] (=NONE). Restricted verticals MUST declare the real
  category — HOUSING, FINANCIAL_PRODUCTS_SERVICES (replaced CREDIT 2025-01-14),
  EMPLOYMENT, ISSUES_ELECTIONS_POLITICS; a false/empty declaration is a
  violation, not a bypass.
- Adset: billing_event=IMPRESSIONS, optimization_goal=OFFSITE_CONVERSIONS
  (still valid, NOT replaced by CONVERSIONS), promoted_object={pixel_id,
  custom_event_type:"SUBMIT_APPLICATION"}, targeting country/age_min/Advantage+
  broad, start_time. custom_event_type enum incl SUBMIT_APPLICATION, LEAD,
  COMPLETE_REGISTRATION, INITIATED_CHECKOUT, ADD_PAYMENT_INFO, PURCHASE (casino
  FTD/deposit usually → PURCHASE or a custom event; confirm the team's mapping).
- OUTCOME_SALES reportedly blocks Lead/Submit Application events (error 2446814,
  field-observed) → use OUTCOME_LEADS for lead funnels.
- Creative: object_story_spec{page_id, link_data{link, image_hash, caption
  (display domain), message (primary text), call_to_action{type:LEARN_MORE,
  value:{link}}}}. Advantage+ enhancements: the standard_enhancements
  field still exists in the schema, but toggling that bundle on ad create/update
  is gone since v22.0 — control PER-FEATURE via
  degrees_of_freedom_spec.creative_features_spec, each feature with
  enroll_status OPT_IN/OPT_OUT (image_touchups, text_optimizations,
  image_templates, ...). media_type_automation OPT_IN needs a catalog → OPT_OUT
  for plain images (error 3858040, field-observed).
- Catalog/template creatives ({{product.name}}+product_set_id) skip image upload
  but need catalog access + prebuilt product sets (Commerce Manager; catalog_
  management usually unavailable via API).

## Scheduling & images

- Create PAUSED with adset start_time = next midnight account tz
  (2026-08-11T00:00:00-0700), verify, then set ACTIVE — full delivery day, no
  human needed at launch.
- Image hashes come from a per-account endpoint (POST /act_X/adimages,
  multipart) — re-upload per account. Uniquify per account (crop few px +
  re-encode) as a precaution: that identical bytes/hash LINK accounts is an
  UNVERIFIED field hypothesis (no Meta doc supports hash-based cross-account
  association) — do it because it's cheap insurance, not because it's documented.
  Review is async; don't rebuild on first-hour silence.
- CSV bulk import (Ads Manager → More): blocked on fresh accounts (error
  #3738001, field-observed; needs history). Budgets in cents, clear IDs, imports
  PAUSED.

## Spend warm-up (fresh accounts, ~d0-3)

Slamming a fresh/low-history account with a high day-0 budget is a classic review
trigger and often just tanks delivery. Common practice: open conservative and step
up over the first days as the account proves stable, not launch at full target
budget. The exact ramp (start budget, step, days) is account/GEO/vertical-specific
— a practitioner prior to set with the TL, not a rule; don't hardcode a number.
- Step-up signals: stable delivery, no restriction flags, CPL in range on a
  matured/nowcast cohort (tracker-ops/03).
- The tension to balance: too timid a start STARVES the optimization event and
  keeps the ad set learning-limited (unstable CPL) — warm-up caution vs clearing
  the learning-volume floor is the real trade, not "low = safe".

## Metric levers (grey application; theory in meta-ads/06 & 12)

Account selection + creative volume move CPL far more than any budget trick
(see 03 and the playbooks). Beyond those, the API-level levers that stop you
wasting spend:

- Don't nuke learning on mass edits. A SIGNIFICANT edit (bid_strategy,
  optimization_goal, promoted_object event/pixel, targeting, or a large budget
  change) can re-enter the ad set into learning; renames, pause/resume, and small
  budget nudges don't. Meta doesn't publish a universal threshold — the "~20-30%
  budget" line is a practitioner heuristic, not a guaranteed cutoff. Batch the
  harmless edits freely; stage the resetting ones.
- Optimize for an event with enough daily volume to EXIT learning. If the deep
  event (SUBMIT_APPLICATION) is too sparse on a fresh account, optimize a
  higher-funnel event first and switch down once volume builds — a deep event
  starved of conversions keeps the ad set learning-limited = unstable CPL.
- Keep the OPTIMIZATION event aligned with / upstream of the PAYOUT event.
  Optimizing for a signal that doesn't correlate with payout buys cheap junk
  (tracker-ops metric rule).
- Consolidate: a few ad sets each fed enough budget/day to clear the learning
  window beat many starved ad sets spread thin across accounts.
- Cost-cap ramp: start COST_CAP ~15-30% above target CPA, tighten as it
  stabilizes; a cap below market just chokes delivery. All %s are heuristics.

## Verification pass

Re-read campaign (budget, bid_strategy), one adset (start_time, promoted_object,
bid), one ad (renders, right page). Activate only on match. Resume-safe: log
every created object ID to per-account JSON so a failed run continues, not dupes.
