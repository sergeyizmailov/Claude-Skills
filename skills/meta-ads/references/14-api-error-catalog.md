# 14 — Marketing API error catalog (canonical)

Code → cause → fix for the Marketing API (v26.0, 2026-08). This is the canonical
reference; for the grey-ops RESPONSE to these errors (when a code means freeze
the profile / replace the account / rotate the domain) see `meta-grey-ops/05`.

**Matching rule (this file owns it; every other file defers here).** Branch on
`error.code` + `error.error_subcode` — the numeric pair is the stable machine key. Read
`error_user_msg` / `error_user_title` for the human diagnosis and log it, but never branch on
it: Meta rewrites those strings without notice, and they are localized. `is_transient:true` =
retry with backoff; `false` = fix the input, retrying is wasted.

A code being **field-observed** (absent from Meta's published error references) does not make
its number unstable — Meta does not renumber codes. It only means you cannot look it up in a
doc, so the entry below is your reference. Match the number; keep the string as evidence.

Two tiers:
- **doc-confirmed** — in a Meta published reference (see which page per code).
- **field-observed** — recurs in practice, absent from every published reference. Still
  branch on the number per the rule above; just don't cite it to anyone as documented,
  and confirm the pair against a live error on your own account before relying on it.

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
- 2446603: creative `image_url` rejected. If the uri came from
  `GET /{video_id}/thumbnails`, pass it WHOLE (all signed query params, ~500 chars) —
  truncating it fails ad creation. Better: don't pass an fbcdn uri at all. The
  AdCreativeVideoData reference says not to use FB CDN URLs in `image_url`; re-upload
  the thumbnail through `/adimages` and use `image_hash` (meta-grey-ops/04 → Media,
  automated in `meta-grey-ops/scripts/media.py`).
- "Video not ready for use in an ad" on adcreative/ad create: the video is still
  transcoding. Poll `GET /{video_id}?fields=status` until `status.video_status ==
  "ready"` — a video_id returned by the upload is not yet a usable video. Reported as
  code 100 / subcode 1885252 [unverified-official — not in Meta's error reference].
  Confirm that pair against a live error on your own account before hardcoding it; the
  matching rule at the top of this file still applies once you have.
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

- 100 / subcode **3858504** (live, validate_only, v26.0, 2026-09-02): `standard_enhancements` key
  present in `degrees_of_freedom_spec.creative_features_spec` → "standard enhancements field no
  longer supported, set individual features instead". Remove the key; opt out every other feature
  by name (`meta-grey-ops/scripts/launch.py DEFAULT_OPT_OUT`, 83 live keys).

- **HTTP 503 with no Graph error body** (live 2026-09-02 on `POST /act_X/adcreatives`): Meta's
  edge answered, the API did not. The outcome is unknown — nothing existed afterwards in this
  case, but nothing proves that in general. `graph.py` does not retry a non-idempotent create
  on it; `launch.py` keeps the `in_flight` marker; `verify.py`/`activate.py` refuse until the
  operator reconciles (check Ads Manager, then clear `in_flight` or record the id).

- 100 / subcode **1885501** (live 2026-09-02, ad set create): "supported combination of click and
  view windows for your objective/optimization goal is (1, 0)" — any VIEW_THROUGH or
  ENGAGED_VIDEO_VIEW window on a non-conversion optimization goal (LINK_CLICKS verified; REACH,
  LANDING_PAGE_VIEWS, THRUPLAY… same family). Send 1d click only (`launch.py
  CLICK_ONLY_ATTRIBUTION_GOALS`). Message arrives localised — match the number.

- 100 / subcode **1885194** (live 2026-09-02) on `POST /{campaign_id}/copies` with `deep_copy=true`:
  "total number of ads, ad sets and campaigns copied at once must be less than 3". Copy level by
  level instead (`meta-grey-ops/scripts/clone.py`). A bare code 1 (ad set: code 1 / sub 99) on
  `/copies` seconds after the source was created = source still IN_PROCESS; wait.

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

## Rate limits (doc-confirmed — **Marketing API** rate-limiting page, verified 2026-08-31)

Source: `developers.facebook.com/docs/marketing-api/overview/rate-limiting` — **not** the
Graph API rate-limiting page. The point scoring, the 100 QPS mutation cap and subcode
5044001 appear only on the Marketing API page; a reviewer checking the Graph page will
wrongly conclude they are invented.

Marketing API = Business Use Case (BUC) limits, **scored at the AD ACCOUNT level**,
header-driven, not a fixed quota. A read costs 1 point, a **write costs 3**.

**The header that matters** is `X-Business-Use-Case-Usage`, keyed by business id:
```json
{"<business-id>": [{"type": "ads_management", "call_count": 95, "total_cputime": 20,
  "total_time": 20, "estimated_time_to_regain_access": 19,
  "ads_api_access_tier": "standard_access"}]}
```
`type` ∈ ads_insights | ads_management | custom_audience | instagram | leadgen |
messenger | pages. The three usage numbers are percentages, throttling at 100.
`estimated_time_to_regain_access` is **minutes**. `ads_api_access_tier` tells you
which quota you are actually on: `development_access` (Limited) vs `standard_access` (Full).

Other headers: `X-App-Usage` (app/user platform limits, rolling 1 h);
`X-FB-Ads-Insights-Throttle` (Insights only); and **`X-Ad-Account-Usage`
(`acc_id_util_pct`, `reset_time_duration`, `ads_api_access_tier`) — read it, it is
current.** Two Meta pages disagree about it and you will meet both:

- **Marketing API → Handle Throttling Errors → Initial Assessment** names the header, uses
  it in its own worked flow, and does not mark it legacy.
- **Graph API → Rate Limiting → Platform headers** scopes `X-Ad-Account-Usage` to "v3.3 and
  older Ads API calls", which reads as retired.

Same split as the `17` / `2446079` row below, and resolve it the same way: **follow the
Marketing API page** — it is the one Meta maintains for this surface — but never make the
header load-bearing. `X-Business-Use-Case-Usage` is the one to gate on; treat
`X-Ad-Account-Usage` as corroboration and tolerate its absence. (An earlier revision of
this file said "legacy, do not build on it" as settled fact — that overstated the Graph
page.)

| Code | Marketing API? | Meaning |
|---|---|---|
| **80004** (sub 2446079) | **yes — the main one** | ads_management BUC limit reached |
| 80000 (sub 2446079) | yes | ads_insights BUC limit |
| 80003 | yes | custom_audience BUC limit |
| **613** | yes | account-level / QPS. Subcode **5044001** = the 100 req/s cap on mutation endpoints; 1996 = inconsistent request volume |
| **17** (sub 2446079) | yes — **hit live 2026-09-02 after ~150 calls/40 min on one Limited-tier account; cleared in minutes** | "User request limit reached" — the **ad-account score cap** was hit (Ad Account Level API-Level Limits): 60 on development access, 9000 on full. Not a Limited-tier-only error; the tier only decides which cap and which block duration applies. ⚠ The two Meta pages disagree: the Graph BUC table scopes this subcode to "V3.3 and Older Ads API excluding Ads Insights", the Marketing API page presents it as current. Follow the Marketing API page and treat the Graph scoping as stale. Slow down; raising the tier needs business verification (13) |
| 4 | indirectly | app-level platform limit (app access token) |
| 32 | **no** | Pages API — not a Marketing API throttle |

Hourly BUC quotas scale with account size: ads_management =
`(100 000 Full | 300 Dev) + 40 × active ads`; ads_insights =
`(190 000 Full | 600 Dev) + 400 × active ads − 0.001 × user errors`. Full/standard
access is granted after 500 Marketing API calls in 15 days with <15 % error rate.

Back off by reading headers: pause near 100; on an 80000-family error honor
`estimated_time_to_regain_access` (× 60 for seconds). Batch reads, cache, no tight polling.

## Batching (doc-confirmed, verified 2026-08-31)

- **50 requests max per batch**; for ad creation Meta advises **≤10 ads per batch**.
- **Batching does not save quota.** "Each call within the batch is counted separately" —
  a batch of 10 costs 10 calls. It saves round-trips and HTTP overhead, nothing else.
  Third-party claims that a batch counts as one request are wrong.
- Errors are per-entry: the outer HTTP response is 200, each array element carries its
  own `code`/`headers`/`body`, and the other entries still succeed.
- Dependent chaining works — `{result=create-campaign:$.id}` JSONPath references;
  independent ops run in parallel, dependent ones sequentially. Set
  `omit_response_on_success: false` on a parent to keep its id in the response.
- **Never mix `validate_only` with chained creation in one batch**: a validate-only op
  returns `{"success": true}` with no `id`, so every JSONPath child reference breaks.
  Whether `execution_options` is honored inside a batch entry at all is [unverified].
