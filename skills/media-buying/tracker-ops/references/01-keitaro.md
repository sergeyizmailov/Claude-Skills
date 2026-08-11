# 01 — Keitaro API

Base `https://TRACKER/admin_api/v1/`. Auth header `Api-Key: <key>` (also accepts
`Authorization: Bearer <key>`). Ref: admin-api.docs.keitaro.io (openapi.json).
Key: Account → API keys → Create (elevated tier; write-once in practice — can't
be edited, only recreated).

## Reports: POST /report/build

Body: `{range:{from,to,timezone | interval}, dimensions:[], measures:[],
filters:[{name,operator,expression?}], sort:[{name,order}]}`. Always pass the
account tz.

- interval (9 tokens): today, yesterday, 7_days_ago, first_day_of_this_week,
  1_month_ago, first_day_of_this_month, 1_year_ago, first_day_of_this_year,
  all_time.
- Corrections that bite:
  - `cpl` metric is present on many installs (version-dependent; not always in
    openapi.json). Production-verified = cost/leads exactly (e.g. 170.95/9 =
    18.9944). Use it when it works; if your tracker errors on it, compute
    CPL = cost / (count of your payout status). `cpa`/`cps` count acquisitions/
    sales, not necessarily your payout event.
  - NO `domain` dimension — use `source`/`referrer`.
  - sub_id range is `sub_id_1..30` (not 15). Also `extra_param_1..10`.
- `ad_campaign_id` = a mappable source parameter ("ID of the advertising
  campaign") that carries whatever token the campaign URL feeds it — a campaign
  id OR a name, depending on your setup; NOT intrinsically utm_campaign. Distinct
  from Keitaro's internal `campaign_id`. `creative_id` = source creative id (may
  be banner/adset id), `external_id` = source click id. So per-account splitting
  by "campaign name" works only if your campaign URL actually maps the FB
  campaign name into this parameter (see the mapping contract, 03).
- Split by status via count metrics leads/sales/rejected (+ revenue variants,
  or flags is_lead/is_sale/is_rejected). `status` itself is a column only in
  conversion-scoped reports.
- If a name errors, the response lists valid columns. Fallback: build in UI →
  DevTools → Network → /report/build → copy payload.

## Cost push: POST /clicks/update_costs

Two accepted shapes — the openapi `ClicksUpdateCostsPayload` lists timezone +
currency as REQUIRED PER ENTRY, and per-entry pushes are production-verified
(returned success, costs landed). Prefer per-entry; top-level also works as a
convenience.
`{campaign_ids:[ID], only_campaign_uniques:0,
costs:[{start_date,end_date,timezone,currency,cost, filters:{ad_campaign_id:"J41-16"}}]}`
- Idempotent (re-push overwrites matched clicks). Push per completed account-tz
  day.
- Filter keys: keyword, external_id, creative_id, ad_campaign_id, source,
  sub_id_1..30 (comma-lists ok) — enables per-campaign-name / per-sub_id splits.
- POST /campaigns/{id}/update_costs exists but docs say "VERY SLOW" — use the
  clicks endpoint.
- /integrations/facebook (native auto cost sync) may be blocked for
  limited-permission users — manual push is the fallback.

## Postback / S2S

`https://TRACKER/{POSTBACK_KEY}/postback?subid={subid}&status={status}&payout={payout}`
- Path segment = a FIXED postback key (Settings → Postback URL), NOT the subid.
  `subid` is a query param (the Keitaro click id). Required: subid + status only.
- Optional: payout, cost, currency, `tid` (records repeat conversions without
  overwriting), sub_id_1..30. Aliases: clickid=subid, type=status, profit=payout.
- Statuses: `lead` (first event/pending → Revenue hold), `sale` (confirmed),
  `rejected`, plus registration/deposit/trash/custom. Network "hold" → send
  `lead` (no native hold). `rebills` is a metric, not a status (repeat via tid).
- Dedup model: same subid+status → OVERWRITES the existing conversion (identical
  params → processed, no duplicate, no re-send). A unique `tid` creates a
  SEPARATE record (upsells/rebills). So multiple conversions per click are
  intentional (distinct tid), not accidental inflation — this is why "conversions"
  is not a CPL denominator (SKILL metric rule).
- Click-id flow: source id → Keitaro → offer via `{external_id}`; network
  returns it as `subid`. sub_id_1..30 = extra markup pass-through.

## Postback drill (verify before trusting any conversion number)

Before scaling a new funnel/offer/tracker link, fire a REAL test conversion
end-to-end and confirm it lands right — don't assume the postback works because
the URL looks correct.

- Fire it: trigger the offer's conversion (or ask the network for a test fire),
  OR hit the postback URL manually with a real click's `subid` + the agreed
  `status` (+`payout`, +`tid`).
- Confirm on the tracker: conversion appears on the RIGHT click (subid), with the
  status mapped to YOUR payout metric, correct payout, correct campaign/sub_id
  split. Read the incoming-postback log to see exactly what arrived vs expected.
- Catches: subid dropped/renamed in the chain (lands on no click → invisible
  conversions), status-string mismatch (network `deposit` vs your scheme), missing
  or zero payout, missing `tid` (rebills overwrite instead of stacking).
- Re-drill after ANY change to the redirect chain, offer link, status scheme, or
  tracker. Tracker-side complement to the funnel click-through test
  (senior-buyer-ops/03).

## Conversion lifecycle (what breaks daily numbers)

- Report date mode: CHECK THE INSTANCE SETTING FIRST — `Settings → System →
  Report display conversion date` toggles the whole reporting basis between
  `By Click Date` and `By Conversion Date`, and recalculates existing stats. So a
  `/report/build` call returns click- OR conversion-date numbers depending on this
  global setting; there's no per-request param that overrides it. Automation must
  read the setting (or pin it) before trusting which basis a pull is on. The raw
  per-conversion rows (regardless of the toggle) come from `POST /conversions/log`
  (body: range, columns[],
  filters[], sort[], limit/offset). Columns you need (exact names from the
  instance openapi.json — confirm on your version): `click_datetime` (click
  time), `postback_datetime` (conversion registration time), `sale_datetime`,
  `status`/`previous_status`/`original_status`, `conversion_id`, `tid`, `sub_id_N`,
  revenue. There is NO built-in lag measure — derive lag = postback_datetime −
  click_datetime per row. (`sale_period` gives a coarse bucket.)
- For MEDIA optimization use click-date (a conversion attaches to the click's
  timestamp, so a lead posting back today lands on YESTERDAY's row → yesterday's
  CPL keeps moving; re-pull a trailing 3-7d window each run, don't freeze a day
  after one pull). For FINANCIAL/payout reporting, conversion-date
  (`postback_datetime`) can be the right basis — just don't mix the two in one
  CPL number. Know which mode/endpoint your pull used.
- Delayed status changes: lead→sale/deposit can flip days later (same subid,
  status update). Approve/reject lifecycle means "today's" quality is provisional
  — report leads now, quality on a lag, and re-pull the cohort when it matures.
- Offer caps: once the advertiser's daily cap is hit, further conversions may be
  rejected/unpaid though the tracker still logs clicks — watch cap state before
  scaling spend into a capped offer.
- Failed postbacks: if the network's postback didn't reach the tracker, the
  conversion is simply missing (not delayed). Keitaro logs incoming postbacks;
  check the log and have the network re-fire (or import via subid,payout,tid,status)
  before concluding a funnel is dead.
- Reconcile against the advertiser/backend periodically — tracker leads are your
  count, the advertiser's approved count is what pays; a widening gap = scrub or
  a tracking break.

## Gotchas

- Bot clicks inflate `clicks` (not `campaign_unique_clicks`); cost spreads over
  all matching clicks → CPC looks diluted on bot days, but daily CPL vs your
  payout-status count stays correct.
