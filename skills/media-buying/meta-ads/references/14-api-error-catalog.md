# 14 — Marketing API error catalog (canonical)

Code → cause → fix for the Marketing API (v26.0, 2026-08). This is the canonical
reference; for the grey-ops RESPONSE to these errors (when a code means freeze
the profile / replace the account / rotate the domain) see `fb-grey-ops/05`.

Read `error_user_msg` first; `is_transient:true` = retry with backoff, `false` =
fix input. Match on numeric code + subcode, not the human string (Meta edits
strings). Two tiers:
- **doc-confirmed** — in a Meta published reference (see which page per code).
- **field-observed** — recurs in practice, absent from every published
  reference; match the message, don't cite the number as documented.

## Auth 190 (doc-confirmed — Graph API "Handle Errors" page, not the Marketing API error reference)

Subcodes: 458/459, 460 (password changed OR security rotation; also the "user
logged out" wording seen in the wild, production 2026-08), 463 (expired), 464,
467 (invalid access token). Any of them: token dead → mint fresh + re-exchange
long-lived; never wait for "revive". "Malformed access token" = copy damage.
Prevention: System User tokens for durable integrations (13), exchange to
long-lived immediately, store in a secrets manager.

## App mode & permissions (doc-confirmed — Marketing API error reference)

- 1885183: app in dev mode can't create creatives → go Live (Privacy Policy URL
  must return 200).
- Permission/approval denial = code 10 ("Application does not have permission")
  or 200 (permission error) — missing capability (e.g. catalog API without
  catalog_management, or managing others' accounts without Full/Advanced
  Access). NOT code 100 — code 100 = "Invalid parameter" (many subcodes, e.g.
  33 = missing/inaccessible object). Request access or use UI.
- Asset access denied = asset not shared to the token user/SU or ad account →
  check BM assignments before debugging code.

## Object creation (field-observed — in neither published error reference)

- 1815857 "Bid Amount Required": CBO defaulted to LOWEST_COST_WITH_BID_CAP →
  set bid_strategy explicitly.
- 3858040 "No catalog… media type": a creative-enhancement/media feature needs
  a catalog → OPT_OUT the feature or attach one (enhancements are controlled
  per-feature under `degrees_of_freedom_spec.creative_features_spec`, see below).
- 2446814: Lead/Submit Application blocked under Sales objective → use
  OUTCOME_LEADS.
- 1815045 "no access to pixel": assign pixel to the ad account (BM → Data
  Sources → Datasets → Assign). Ads recover automatically; no rebuild.

## Creative enhancements note (v22.0+ change)

`enable_standard_enhancements` (top-level boolean) is obsolete, and since v22.0
(2025-01-21) you can no longer create/update ads by toggling the
`standard_enhancements` bundle. The field still exists in the schema, but the
supported control is PER-FEATURE: `degrees_of_freedom_spec.creative_features_spec`
with each feature (image_touchups, text_optimizations, image_templates, …)
carrying `enroll_status: OPT_IN|OPT_OUT`. Opt out feature-by-feature.

## Import & delivery

- 3738001 (field-observed) on CSV import: account too fresh → API/UI meanwhile.
- "Not delivering", no error: future start_time (normal), review pending,
  billing hold, or spend caps.
- Disabled/restricted account: check Account Quality for the asset + reason,
  fix, appeal in-product. Do not rebuild assets to evade enforcement.

## Rate limits (doc-confirmed — Rate Limiting guide, not the error catalogs)

Marketing API = Business Use Case (BUC) limits, header-driven, not a fixed quota.
- Platform: `X-App-Usage` {call_count/total_cputime/total_time, 0-100%}. Errors
  4 (app), 17 (user), 32 (Pages).
- BUC (Marketing API): `X-Business-Use-Case-Usage` (per business/account, `type`
  = ads_insights/ads_management/..., + `estimated_time_to_regain_access` min).
  Errors 80000-family.
Back off by reading headers: pause near 100; on 80000 honor
estimated_time_to_regain_access. Batch reads, cache, no tight polling.
