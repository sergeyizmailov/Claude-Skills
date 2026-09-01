# 04 — Mass launch via API

Programmatic beats UI after ~2 accounts (identical structure, no misclicks,
naming enforced). All calls via setup proxy (01), long-lived token (02), app
Live (else creative creation fails).

**Execute through `../scripts/`, not by hand** — `probe.py`, `media.py`, `launch.py`,
`verify.py`, `activate.py`, `mutate_set.py`; ordered path in `00-launch-runbook.md`.
Everything below is the *why*: the ordering, unit and nesting rules the scripts already
encode, plus the quirks they cannot decide for you. Reach for a hand-written payload only
for a shape the scripts do not cover, and add it there rather than one-off.

## Structures

- 1-1-3 (1 camp, 1 adset, 3 ads): probe unknown accounts for delivery. Quirk:
  Meta dumps ~90% of adset budget into ONE ad — useless for comparing creatives.
- 1-3-1 (3 adsets, 1 ad each): cleaner SCREENING (each creative gets its own
  adset budget), but NOT a fair/causal test — audiences overlap across adsets and
  auction conditions differ, so read winners as directional. For a causal read use
  the A/B Test tool (measurement-experimentation-ops).
  Practitioner claim (YT expert, unverified): Meta itself nudges UNIQUE creatives
  per adset instead of duplicating one creative across adsets; with statics =
  3 unique creatives in 3 adsets (field claim: ~2× cheaper conversions, faster
  exploration). Duplicating the SAME video across 3 adsets is the accepted video
  variant. Use 3–5 adsets (3 is the common pick). Observed rotation: spend hops
  adset-to-adset across days — the winner is often the day-2/3 adset, not day 1,
  so judge on a 3-day window, not first-day CPL.
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
- 🔺 **`is_adset_budget_sharing_enabled` is NOT campaign budget optimization.** It is
  ad-set budget sharing: "advertisers can now share up to 20% of their budget with other
  ad sets in the same campaign" — partial automation, against CBO's 100%. The rule that
  matters: **"required starting v24 if you are not setting budget at the campaign
  level"**, and **"you do not need to pass this field if you are using a campaign
  budget."** [doc-confirmed, adset-budget-sharing guide, verified 2026-08-31] That is why
  the create sequence below needs it: step 1 creates the campaign with NO budget yet, so
  the field is required (4834011 if omitted); step 2 then adds the campaign budget. Send
  budget and bid_strategy in the create call instead and the field is unnecessary — an
  untested simplification of a field-proven sequence, so `launch.py` keeps the 3-step.
- Targeting edits REPLACE the whole object (field-observed): a POST carrying
  one targeting field wipes the rest — always send every field, never one.
- Creative, image: `object_story_spec{page_id, instagram_user_id, link_data{link,
  image_hash, caption (display domain), message (primary text), name (headline),
  description, call_to_action{type, value:{link}}}}`. `image_hash` XOR `picture`, never
  both. `description` is ignored on Instagram. Carousel: `child_attachments` 2–5, and
  `link` + `message` become required.
- 🔺 **Creative, video: `video_data` has NO `link` field.** The destination lives in
  `call_to_action.value.link` — "required to be same as the link url of the creative".
  Fields: `video_id`, `image_hash` (thumbnail) or `image_url`, `title` (headline),
  `message`, `link_description` (needs a CTA to render). [doc-confirmed 2026-08-31]
- Advantage+ enhancements — **there is no single off switch.** The
  `standard_enhancements` bundle stopped being settable at v22.0; the field still exists
  in the schema, which is why toggling it looks like it worked. Control PER-FEATURE via
  `degrees_of_freedom_spec.creative_features_spec`, each key carrying
  `enroll_status: OPT_IN|OPT_OUT` (only those two values). Traps:
  - **`adapt_to_placement` is OPT-IN BY DEFAULT** — omit it and it stays on.
  - **Music is not opted out through `creative_features_spec`** — the guide's instruction
    is `asset_feed_spec.audios: []`. (A `music_generation` key does appear in the v26.0
    reference READ schema; the guide gives no write recipe for it, so treat `audios: []`
    as the supported control and the key as read-only until proven otherwise.)
  - `media_type_automation` OPT_IN needs a catalog → OPT_OUT for plain images
    (error 3858040, field-observed).
  - Meta's own docs disagree on which keys are writable: the v26.0 reference field table
    and the Advantage+ guide list different sets, and the guide's example writes
    `image_template` (singular) while its table says `image_templates`. `launch.py` ships
    a 19-key default list; `--dry-run` tells you if your account rejects one.
  - Keys set OPT_IN but ineligible are silently removed, and OPT_OUT keys may still
    appear on a GET — harmless as long as they are not OPT_IN. Verify with a read-back.
  - 2026-06-28 out-of-cycle change added `image_animation`, `video_filtering`,
    `video_uncrop`.
  - ABOVE the ad level: accounts are auto-enrolled in new A+ AI feature TESTS
    (practitioner-audited: 14/14 enrolled without opt-in). Kill switch = account-level
    enhancements toggle + "test new optimizations" checkbox in Advertising Settings —
    per-ad OPT_OUT does not cover account test enrollment. Andromeda (Oct 2025 full
    rollout) additionally made detailed-targeting inputs advisory for most performance
    goals, and Jan 2026 removed DT exclusions for most objectives — broad + creative
    volume is the real targeting lever now.
- 🔺 **`advantage_audience` must be explicit on ad-set CREATE.** Since v23.0 it defaults
  to `1` **only** for a default or relaxed targeting setup; any other setup errors unless
  you send `1` or `0`. Updating an existing ad set does not behave this way, on any
  version. Since v26.0, Housing/Employment/Financial ads with relaxable targeting error
  without an explicit value. When enabled: `age_min` is limited to 18–25 and `age_max` is
  forced to 65; location, minimum age, language and custom-audience exclusions are never
  expanded. [doc-confirmed 2026-08-31]
- **`url_tags` is not a universal tracker.** The reference scopes it to urls clicked from
  page post ads, the message of the post, and canvas app-install creatives — and it can
  **replace** a colliding query key rather than append. Macros: `{{campaign.id}}`,
  `{{campaign.name}}`, `{{adset.id}}`, `{{adset.name}}`, `{{ad.id}}`, `{{ad.name}}` —
  and name macros resolve from a **snapshot taken at first publish**, not the live name,
  so renaming an object after launch does not change what the tracker receives. Inside
  `asset_feed_spec`, `url_tags` is PER-ASSET (images, videos, bodies, titles,
  descriptions) — the documented way to attribute which variant was clicked. For
  catalog/dynamic cards the click URL comes from the feed; override it with
  `template_url_spec`, not `url_tags` (whether url_tags reaches product links at all is
  [unverified] — the reference's "only" reads as excluding them). This is the mechanism
  behind the missing sub1-4 on catalog cards noted in `playbooks/casino.md`.
- Catalog/template creatives ({{product.name}}+product_set_id) skip image upload
  but need catalog access + prebuilt product sets (Commerce Manager; catalog_
  management usually unavailable via API).
- **IG identity on farmed fan pages — use the PBIA, never drop placements.** A grey
  fan page has no real Instagram account, but every Page can mint a page-backed one, so
  IG placements stay available. Without it, POST /ads fails
  `1772103 "Instagram Account Is Missing"` whenever placements include IG. The tempting
  fix — `targeting.publisher_platforms=["facebook"]` — makes the error vanish while
  silently killing IG + Audience Network + Messenger inventory for that ad set: a large,
  invisible reach cut on the cheapest grey placements. **Fix the identity, not the
  placements.** `probe.py --create-pbia` and `launch.py` (`instagram_user_id: "auto"`)
  do this for you. Mechanics, the PAGE-token requirement, and the dead
  `instagram_actor_id` field: meta-ads/13 §5.

## Scheduling — one rule, keyed on optimization goal

Pick `start_time` from the ad set's optimization goal. Do not mix the two rows; earlier drafts
of this file contradicted themselves here.

| optimization_goal | `start_time` (account tz = geo tz) |
|---|---|
| Conversions (`OFFSITE_CONVERSIONS`, `VALUE`) | **06:00–08:00 geo-time, or 1–2h before the geo's evening window. NEVER 00:00** |
| Reach / impressions / traffic / awareness (`LINK_CLICKS`, `IMPRESSIONS`, `REACH`) | next **00:00** — a full, uniform delivery day |

Always create PAUSED → verify → set ACTIVE. Review runs at submission regardless of
`start_time`, so approval lands before first spend; `start_time` is a supported creation field
with no documented minimum lead time.

Why conversions differ: a cold CBO ad set opening at 00:00 burns its learning-phase impressions
into the 00:00–06:00 dead window. Field corroboration 2026-08-30 — five campaigns launched
~21:30–21:40 TR; by 00:03 three had ZERO delivery. Practitioner rationale, not Meta docs.

Two converting windows per geo day — early morning (~06:00–08:00) and evening (~16:00+). Pick
one and hold it per geo. Both avoid dead hours AND the 12:00–18:00 auction peak, where brand
bid-caps inflate CPM. Corollary: **never judge a campaign on midday numbers** — buyers who cut
at midday "no leads" are discarding their converting hours. [practitioner, 2026 YT team lead]

## DLO / multi-language via API

Whether the language layer still clears review is a `07` question (SPLIT, ~50/50 by seat).
This is only how to build it. [doc-confirmed 2026-08-31]

- Lives in `asset_feed_spec`, not `object_story_spec`. **DLO accepts only
  `SINGLE_IMAGE` or `SINGLE_VIDEO`** — narrower than `asset_feed_spec` generally, which
  also takes CAROUSEL and AUTOMATIC_FORMAT. Also required: `link_urls`, and
  `call_to_action_types` (**exactly one** type when customization rules are present).
- 🔺 **Locales are NUMERIC IDs, not language codes.** The field is
  `asset_customization_rules[].customization_spec.locales: [9, 44]` — ints fetched from
  `GET /search?type=adlocale&q=en` (English US = 6, English UK = 24). There is no
  `language` field here; a string locale code is the classic silent miss.
- Every text asset carries an `adlabels` name; each rule maps labels via `body_label`,
  `title_label`, `description_label`, `link_url_label`, plus **`image_label` (required for
  SINGLE_IMAGE) or `video_label` (required for SINGLE_VIDEO)** — a rule missing its media
  label is rejected. One image/video may omit its label to serve all languages.
  `priority` orders overlapping rules.
- 🔺 **`descriptions` is REQUIRED** — "use an empty string with a single space for blank
  description". An omitted key or an empty list is not the same thing and is rejected.
- **Exactly one rule carries `is_default: true`** — that is the "Default" slot the
  language trick in `07` talks about; the rest are the "Added" locales. It is the fallback
  when a viewer's language matches no rule.
- Conflict in Meta's own docs: the asset-customization-rules page says a feed must have
  **at least two** rules; the autotranslate example ships with one. Assume two.
- The ad set must have `is_dynamic_creative = false` for a rule-based feed — Dynamic
  Creative and customization rules are mutually exclusive.
- Auto-translation instead of hand-written slots: `asset_feed_spec.autotranslate: ["tr_TR"]`
  with `optimization_type: "LANGUAGE"` and one default rule. Your manual edits to a locale
  you also list in `autotranslate` are dropped.
- Limits: ≤49 assets per type, title ≤255, body ≤4096, description ≤10000 chars.
- Objective support is documented against LEGACY objective names only — LINK_CLICKS,
  APP_INSTALLS, CONVERSIONS, REACH, BRAND_AWARENESS, VIDEO_VIEWS — and excludes Messenger
  destinations. [doc-confirmed, Multi-Language Ads page, verified 2026-08-31] Whether the ODAX `OUTCOME_*` equivalents are accepted is [unverified], and
  **a dry run will not tell you** — `validate_only` cannot validate an ad without a real
  parent ad set id, so the rejection lands at `POST /ads` on the real create (`00`, step 5).
  Budget for it: build one DLO ad against a live account before scheduling a launch on it.
  The confirmed hard constraint is unchanged: **Website destination**, no
  Instant Experience, no Messaging Apps (`07`).
- Not the same thing: "Flexible ads" use a top-level `creative_asset_groups_spec` on
  `POST /act_X/ads`, not `asset_feed_spec`, and only under `OUTCOME_SALES` /
  `OUTCOME_APP_PROMOTION`. Placement Asset Customization uses the same rules machinery
  with `optimization_type: "PLACEMENT"` and `customization_spec.publisher_platforms`.

## Media

Run `scripts/media.py` rather than hand-rolling any of this; the notes below are why
it does what it does. [doc-confirmed 2026-08-31 unless marked]

**Images — `POST /act_X/adimages`, multipart.** The multipart FIELD NAME is the
filename, and Meta requires a real extension: `sample.jpg` works, `sample` and
`sample.tmp` are rejected. The response is keyed by that same name:
`{"images": {"<name>": {"hash": ..., "url": ..., "width": ...}}}` — `hash` is nested,
not top-level. The returned `url` is temporary and the reference says **not** to use it
in creative creation. Hashes are account-scoped in practice (the node carries
`account_id`, and `copy_from={source_account_id, hash}` exists precisely to move one
across) — re-upload per account. Uniquify per account (crop a few px + re-encode) as
cheap insurance: that identical bytes/hash LINK accounts is an UNVERIFIED field
hypothesis, no Meta doc supports hash-based cross-account association.

**Videos — `POST /act_X/advideos`.** Small files: `source` (form data) or `file_url`.
Anything real: the chunked session, because it resumes.

- 🔺 **`graph-video.facebook.com` is DEPRECATED — upload to `graph.facebook.com`.**
  Meta's own facebook-python-business-sdk still hardcodes the dead host in
  `video_uploader.py` (issue #701, open since 2025-04) and returns 500s. An agent that
  reaches for the official SDK to upload video fails for a reason no error explains.
- Phases: `upload_phase` = `start` → `transfer` → `finish` (`cancel` to abort), carrying
  `upload_session_id`, `start_offset`, `end_offset`, `video_file_chunk`, `file_size`.
  **The server dictates chunk boundaries** — each `transfer` response returns the NEXT
  offsets; loop until `start_offset == end_offset`. Subcode **1363037** = offsets
  desynced; the error payload carries the correct ones, resync and retry.
- `start` returns `video_id` immediately. That id is NOT usable yet.
- **Readiness gate: `GET /{video_id}?fields=status` → `status.video_status` ∈
  `ready` | `processing` | `error`**, plus `processing_progress` 0-100. Building an ad
  against a processing video fails with "Video not ready for use in an ad"
  (code 100 / subcode 1885252 — community-sourced, [unverified-official]; the message
  is the reliable part). Poll to `ready` first. No official processing-time figure exists.
- Upload errors are documented: 351 video file problem, 352 unsupported format,
  382 file too small, 389 cannot fetch from URL, 6000/6001 upload failure.
- The old narrative chunked-upload guide is gone; Meta now promotes the Resumable
  Upload API (`POST /{app_id}/uploads` → `POST /upload:{session}` →
  `fbuploader_video_file_chunk`). That handle is documented for `/{page_id}/videos`
  and is **not** in the v26 `/act_X/advideos` parameter list — whether ad accounts
  accept it is [unverified]. The `upload_phase` flow above is still in the v26
  endpoint reference; use it.

**Video thumbnails.** `GET /{video_id}/thumbnails` → `data[]` of
`{id, uri, width, height, scale, is_preferred}`. Two paths, and the default matters:

- **Sanctioned:** fetch the preferred `uri`, re-upload it through `/adimages`, put the
  returned hash in `video_data.image_hash`. The AdCreativeVideoData reference explicitly
  says not to feed FB CDN URLs into `image_url`. `media.py` does this automatically.
- **Field workaround:** pass the `uri` directly as `image_url` — then pass it **WHOLE**,
  every query param, ~500 chars. Truncating the signed query string fails creative
  creation (2446603). That the whole-uri requirement is the cause is [unverified] — the
  signed params make it inference, not doc.
- Custom thumbnail: `POST /{video_id}/thumbnails` with `source` + `is_preferred`.
  Max 10 MB, and **only on videos already associated with a Page**.

Review is async; don't rebuild on first-hour silence.

**CSV bulk import** (Ads Manager → More): blocked on fresh accounts (error #3738001,
field-observed; needs history). Budgets in cents, clear IDs, imports PAUSED.

## Spend warm-up (fresh accounts, ~d0-3)

Slamming a fresh/low-history account with a high day-0 budget is a classic review
trigger and often just tanks delivery. Common practice: open conservative and step
up over the first days as the account proves stable, not launch at full target
budget. The exact ramp (start budget, step, days) is account/GEO/vertical-specific
— a practitioner prior to set with the TL, not a rule; don't hardcode a number.
- Organic limit ramp (practitioner, unverified): fresh BM ad accounts often open at a ~$150/day
  spend limit; hitting the cap 1–2 days in a row raises it organically (~$250–300, then ~$600).
  Let it ramp by spending into the cap — don't request increases.
- Billing warm-up (practitioner): before real spend, run $1–3 campaigns until 1–2 SUCCESSFUL
  charges post on the FBP — charged accounts get flagged for payment failure far less. Do it via
  the main BM's payment profile.
- **Budget raises — the step protocol (practitioner consensus; Meta only says "small edits don't
  reset learning, large do", no % in docs):** ≤20% per edit, 48–72h between steps, never near the
  end of the geo-day (a doubled budget at 10pm leaves 2h to spend it — official troubleshoot doc).
  Applies to CBO campaign budget same as adset. FIELD-VERIFIED 2026-08-31: +200% on 5 CBO
  campaigns at once, evening, fresh BM account → account-wide silent delivery freeze for hours
  (all ACTIVE, zero impressions, brand-new probe campaigns frozen too, no API-visible flag).
  Remedy per sources: revert to last good budget, touch NOTHING 48–72h; account-level
  new-account spend throttles are real, undocumented and API-invisible.
- Step-up signals: stable delivery, no restriction flags, CPL in range on a
  matured/nowcast cohort (tracker-ops/03).
- The tension to balance: too timid a start STARVES the optimization event and
  keeps the ad set learning-limited (unstable CPL) — warm-up caution vs clearing
  the learning-volume floor is the real trade, not "low = safe".

## Metric levers (grey application; theory in meta-ads/06 & 12)

Account selection + creative volume move CPL far more than any budget trick
(see 03 and the playbooks). Beyond those, the API-level levers that stop you
wasting spend:

- **Pixel eats only what you feed it (event hygiene).** Send CAPI/pixel ONLY the quality event
  (deposit or CRM-qualified lead — reached/confirmed), never raw leads: the optimizer reproduces
  whatever you feed. Cost: displayed CPL inflates massively (practitioner example: $737/lead
  displayed = $35 real across 21 raw leads; events land with 7–10 day lag) — do CPL math from
  CRM/tracker counts, not from Ads Manager. Tag campaigns by subid so CRM→postback matching is
  1:1 (tracker-ops).
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

## Re-moderation: which edits trigger a new review (field-observed, 2026-08)

Review attaches to the CREATIVE, not the ad set:
- SAFE at ad-set level: geo, devices, age, placements, budget, bid, schedule,
  audience — 45 ad sets edited three times in one day, zero status changes.
- TRIGGERS at ad/creative level: CTA, display link, copy, Multi-advertiser ads,
  swapping the video — each builds a new creative and a new review.
- An ad created PAUSED still goes to review; before first approval, swapping
  the creative restarts first-pass review (safe) — it is not re-moderation.
- A rejected ad cannot be enabled (2490468, meta-ads/14) — create a new ad.
- 🔺 Vendor MagicClick 2026: flipping ad-level **Branding** ON↔OFF requeues Rejected /
  stuck In Review without a new creative (5–20 min claimed). Hidden if all Advantage+
  enhancements are OFF. If enable still fails, create a new ad. Do **not** treat
  schedule-delay as a softer reviewer — field above: schedule edits did not change status.

## Collection/catalog launch quirks (field-observed 2026-08-30, own BM, v26.0)

- **Collection creative that works** (custom video hero + product set): creative = `{product_set_id,
  object_story_spec: {page_id, instagram_user_id (PBIA ok), template_data: {multi_share_end_card,
  link, message, call_to_action}}, asset_feed_spec: {optimization_type: "FORMAT_AUTOMATION",
  ad_formats: ["COLLECTION"], videos: [{video_id}]}, url_tags}`. Omitting instagram_user_id → ad
  create fails 1772103. Retry once before diagnosing: one ad create failed 1772103, succeeded
  unchanged on retry (propagation lag).
- **Dead paths**: `video_data` + product_set_id → 1487832 "invalid repost"; `template_data.retailer_item_ids`
  on a regular catalog → 1443180 (retailer_item_ids = localized catalogs only).
- **Product set minimum = 4 items — COLLECTION format ONLY** (2490457 at build; docs: "at least
  four elements", "four thumbnails are required" — collection-ads doc upd. 2025-12-07). Catalog
  carousel/single-card ads have NO minimum: official single-product template examples exist
  (`force_single_link: true` + `product_set_id`), `format_option` supports
  `carousel_images_single_item`/`show_multiple_images` = one rendered card (verified 2026-08).
  VIDEO card without Collection: attach video to the PRODUCT (feed `video[0].url`, one per
  product; API item `videos` field) + creative `product_set_id` +
  `template_data.format_option:"single_video"` — Dynamic Media path, documented
  (advantage-catalog-ads/dynamic-media, v25). `single_video` == Help Center toggle "Increase
  video priority" (video-first, engagement cost accepted; "single image or video" format only).
  Keep `media_type_automation` OPT_IN (default): it ADDS video alongside images where supported,
  cannot force video-only; OPT_OUT strips video. Items without video still render images.
  `link_data.video_data`+`product_set_id` without
  collection = undocumented → fails (1487832).
  Manual carousels (child_attachments, no set) need 2–5. Drives the
  white→slot swap math: review set 4 white → post-approval mutate 4 slot (or 3 slot + 1 white if
  only 3 arts).
- **Set mutation via API** works on UI-created sets (they are filter-based):
  `POST /{product_set_id}` with `filter`. 🔺 **The rule is ENCODE EXACTLY ONCE — not
  "object, never string".** Meta documents `filter` as "a JSON-encoded rule" and its own PHP
  example passes a string (`'filter' => '{"product_type":...}'`), so a single-encoded string is
  the official form and works. What silently no-ops is **double** encoding: a client that
  JSON-encodes every complex value will encode an already-JSON string a second time, and Meta
  receives escaped quotes instead of a rule — returns the id, filter unchanged, no error. So:
  hand the client a dict and let it encode once, or hand it a string and make sure it does not
  encode again. `scripts/mutate_set.py` passes a dict, then re-reads the set and fails loudly if
  the filter did not change — never trust the 200. A membership change triggers no ad
  re-review.
- **UI product edit recreates the item under a NEW product_item_id** (old id → "does not exist").
  Set filters referencing the old id silently drop it → set shrinks (7 ads kept delivering on 3/4
  cards). After ANY manual product fix in Commerce Manager: re-verify `product_count` and refresh
  filter ids via API.
- **Catalog product create** (`POST /{catalog_id}/products`): `price` = INTEGER minor units (100 =
  TRY 1.00). `image_url` must be a crawler-stable URL — adimages fbcdn signed URLs FAIL ("Image
  fetch failed" → item Not eligible). UI upload is the reliable path (but see recreate-gotcha above).
- **Catalog Management Advanced Access**: 02 said App Review required — field-observed 2026-08-30:
  `catalog_management` GRANTED on a Business-type Live app, Limited tier, own-BM catalog. Try the
  token before assuming it's stripped.
- **OUTCOME_LEADS create sequence** (avoids 3 errors we hit): 1) create campaign with
  `is_adset_budget_sharing_enabled: false` (4834011 if omitted), NO bid_strategy; 2) POST
  `{daily_budget, bid_strategy: LOWEST_COST_WITHOUT_CAP}` to the campaign (bid_strategy without
  budget fails 1885737); 3) adset WITHOUT own budget/bid_strategy.
- **`targeting_automation: {"advantage_audience": 0}` goes INSIDE the `targeting` object**, not a
  top-level adset field. Missing/misplaced → misleading error 1870227 "advantage audience".
- **Multi-advertiser ads are ON by default** for FORMAT_AUTOMATION catalog creatives (UI checkbox
  checked). Creative field-read fails ("nonexisting field") — that does NOT mean off. No API field
  found to disable. Recipe: build PAUSED → bulk-uncheck in Ads Manager UI → then activate.
  Post-approval toggle = re-moderation. 🔺 API clones/recreations inherit ON silently — every
  programmatic (re)launch needs the UI pass; best window is while the review set is still white,
  so the toggle's re-review also passes on white (field-verified 2026-09-01: recreation brought
  the checkbox back after it had been manually unchecked on the originals).
- 🔺 Attribution is IMMUTABLE post-create (1504040, field-observed 2026-09-01: "attribution
  window update no longer supported after ad set creation"). The UI shows THREE rows for
  video-carrying ad sets: Click / Engaged view / View — the middle one is
  `attribution_spec` event_type **`ENGAGED_VIDEO_VIEW`** (not ENGAGED_VIEW) and must be
  included AT CREATE or the ad set is stuck with two windows. 1d-click + 1d-view without
  it ≈ functionally the same for web funnels (engaged-view only fires on ≥10s video
  watches); exact three-row display requires a new ad set.
- **SU token doubles as CAPI dataset token**: with Full access on pixel/dataset, the same System
  User token POSTs to `/{dataset_id}/events`. Clean write probe: POST with `"data": []` →
  "#100 param data must be non-empty" = auth OK without creating events.
- 🔺 **Attribution: the sub-field is `window_days`, NOT `event_window_days`.**
  [doc-confirmed, v26.0 ad set reference, verified 2026-08-31] `attribution_spec` takes
  `{event_type: CLICK_THROUGH|VIEW_THROUGH|ENGAGED_VIDEO_VIEW, window_days: int, weight: float}`.
  An earlier field note in this file used `event_window_days` — **that key does not exist**, and
  Graph ignores unknown keys inside a JSON object parameter instead of rejecting them. So the
  call succeeds, the ad set silently keeps the account default (7-day click), and every CPL
  computed against a believed 1-day window is wrong. If you shipped ad sets with
  `event_window_days`, re-read `attribution_spec` on them before trusting their numbers.
  Correct 1-day/1-day at adset create:
  `attribution_spec=[{"event_type":"CLICK_THROUGH","window_days":1},{"event_type":"VIEW_THROUGH","window_days":1}]`.
  Read the account's real default from `default_unified_attribution_spec` rather than assuming.
  Documented windows: click 1 or 7, view 1, engaged-video-view 1; 7- and 28-day VIEW windows were
  removed from Insights on 2026-01-12. The API lists `attribution_spec` on the update path too, but
  editing live is a significant edit and reporting is not retroactive → set at creation only.
- **Insights on fresh campaigns return empty for 15–40 min** — not a delivery failure.

## Verification pass

Re-read campaign (budget, bid_strategy), one adset (start_time, promoted_object,
bid), one ad (renders, right page). Activate only on match. Resume-safe: log
every created object ID to per-account JSON so a failed run continues, not dupes.
