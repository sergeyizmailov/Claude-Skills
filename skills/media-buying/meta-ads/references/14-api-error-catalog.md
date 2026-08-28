# 14 — Marketing API error catalog (canonical)

Code → cause → fix for the Marketing API (v26.0, 2026-08). This is the canonical
reference; for the grey-ops RESPONSE to these errors (when a code means freeze
the profile / replace the account / rotate the domain) see `meta-grey-ops/05`.

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
- 2703 / subcode 2490336: a cost or ratio condition (`cpa`, `cost_per_*`,
  `website_purchase_roas`) on an AD-SET- or AD-scoped automated rule → rejected
  at rule creation, for every action except CHANGE_BUDGET / CHANGE_BID —
  NOTIFICATION is rejected too. Campaign scope accepts them. The message
  ("Rules that turn off ads can't have cost conditions") names the wrong cause:
  it is scope, not action. Fix: express the condition as spend + count
  (`spent > X AND <conversion count> < k+1`); the threshold ladder lives in
  senior-buyer-ops/04.
- 2446603: creative `image_url` rejected — take the uri WHOLE from
  `GET /{video_id}/thumbnails` (all query params, ~500 chars); truncating it
  fails ad creation.
- 2490468 HARD_ERROR: a REJECTED ad cannot be enabled at all — editing does not
  help; the fix is a brand-new ad (grey-ops practice: don't fight rejects,
  leave them off — meta-grey-ops/05).
- 100 / subcode **1772103** "Instagram Account Is Missing" on POST `/ads`: the
  ad set's placements include Instagram and the CREATIVE carries no IG identity.
  It is a creative-identity error, never "this account/Page can't run Instagram"
  and never a targeting error. Note it fires at AD creation — the adcreative
  POST succeeds without an identity, so the creative existing proves nothing.
  Fix: put the Page's PBIA in `object_story_spec.instagram_user_id` (13 §5).
  Do NOT "fix" it with `targeting.publisher_platforms=["facebook"]` — that
  silently drops Instagram + Audience Network + Messenger delivery for the whole
  ad set, converting an identity bug into a permanent reach cut.
- 100 "Param instagram_user_id / instagram_actor_id must be a valid Instagram
  account id": with a PBIA id this almost always means the request used the
  retired `instagram_actor_id` (dead since v22.0 — 13 §5). Same id under
  `instagram_user_id` is accepted. Check the field name before concluding the
  identity is invalid.

## Creative enhancements note (v22.0+ change)

`enable_standard_enhancements` (top-level boolean) is obsolete, and since v22.0
(2025-01-21) you can no longer create/update ads by toggling the
`standard_enhancements` bundle. The field still exists in the schema, but the
supported control is PER-FEATURE: `degrees_of_freedom_spec.creative_features_spec`
with each feature (image_touchups, text_optimizations, image_templates, …)
carrying `enroll_status: OPT_IN|OPT_OUT`. Opt out feature-by-feature.

## Import & delivery

- 3738001 (field-observed) on CSV import: account too fresh → API/UI meanwhile.
- 1487828 (field-observed): `spend_cap` not writable by the buyer on agency
  accounts — the agency owns it; ask them, don't retry.
- "Not delivering", no error: future start_time (normal), review pending,
  billing hold, or spend caps.
- Disabled/restricted account: check Account Quality for the asset + reason,
  fix, appeal in-product. Do not rebuild assets to evade enforcement.

## Rate limits (doc-confirmed — Rate Limiting guide, not the error catalogs)

Marketing API = Business Use Case (BUC) limits, header-driven, not a fixed quota.
- Platform: `X-App-Usage` {call_count/total_cputime/total_time, 0-100%}. Errors
  4 (app), 17 (user), 32 (Pages). On bulk work, 17 / subcode 2446079
  (field-observed) = the app's Marketing API access tier is Limited → sleep
  ≥0.5 s between calls; raising the tier needs business verification (13).
- BUC (Marketing API): `X-Business-Use-Case-Usage` (per business/account, `type`
  = ads_insights/ads_management/..., + `estimated_time_to_regain_access` min).
  Errors 80000-family.
Back off by reading headers: pause near 100; on 80000 honor
estimated_time_to_regain_access. Batch reads, cache, no tight polling.
