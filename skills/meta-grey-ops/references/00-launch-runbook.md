# 00 — Launch runbook (start here for any API launch)

The ordered path from "we have an account" to "it is spending", for any vertical. Every
other file in this skill is an exception handler for one of these steps — do not read
them up front. If a step passes, move on.

Reviewed 2026-08-31. Scripts live in `../scripts/`; run them from that directory.
After editing any of them, `python3 selftest.py` — offline, no token, no account, and it
covers the invariants that have regressed before (retry policy, redaction, DLO assembly,
the destination diff).

```
0 gate  →  1 access  →  2 media  →  3 spec  →  4 dry run  →  5 create PAUSED
        →  6 verify  →  7 review layer  →  8 activate
        →  9 first hour  →  9.5 daily sync  →  10 kill rules
```

**Never hand-assemble a Graph payload.** The agent writes the JSON spec; `launch.py`
writes the API calls. Every recurring launch failure in this corpus is a payload bug —
wrong nesting, wrong unit, wrong field name, wrong order — and prose re-derived into a
payload gets a fresh chance to be wrong on every run. The scripts encode the ordering
and unit rules once.

## Vertical parameters

Fill these before writing the spec. Everything else in the runbook is identical across
verticals.

| Vertical | Gate before spend | Typical payout event | First optimization event | Playbook |
|---|---|---|---|---|
| iGaming / casino | A&V gambling authorization + per-territory licence, filed **before any ad exists**; 19 markets take no gambling ads at all | FTD (or qualified FTD) | `COMPLETE_REGISTRATION`, switch to `PURCHASE` at ~20-30 FTD | `playbooks/casino.md` |
| Nutra | Health-claim policy; no prohibited claims | Confirmed COD order | `LEAD` / `PURCHASE` | `playbooks/nutra.md` |
| Crypto / trading | Crypto authorization; the exemption boundary decides if there is a path | Qualified reg / deposit | `COMPLETE_REGISTRATION` | `playbooks/crypto-trading.md` |
| News → Telegram | No formal gate; the funnel is the risk | Subscribe / bot join | `LEAD` | `playbooks/news-tg.md` |
| Anything else | **Check `10` Q1/Q2 first** | — | — | shape ports from any playbook above |

## 0 — Does this vertical have a path at all

`10` Q1 (permission required before spend) and Q2 (no path in any geo). Iterating
creatives against a prohibited vertical burns the account for nothing.

If a gate applies, clear it in `09` **before any ad object exists** — gambling and
crypto authorizations are filed in the Authorizations & Verifications tab, financial
products need the regulator number, SIEP needs a postal code mailed to a residential
address (2–3 weeks). Approvals bind to a **specific portfolio and ad account**: a
replacement account needs a new approval.

## 1 — Access and the write probe

Collect into gitignored notes, verbatim: ad account id, BM, page id, pixel/dataset id,
tracker campaign URL, proxy. Then:

```bash
export META_TOKEN='...'                              # never on the command line
export META_PROXY='socks5h://user:pass@host:port'    # socks5:// breaks TLS (01)
python3 probe.py --account act_123 --page 456 --dataset 789 --create-pbia
```

Exit 0 or you do not launch. The probe proves, as separate gates: token identity,
granted scopes (`/me/permissions` — requested ≠ granted), ad-account status and funding,
a Page access token, the page-backed Instagram identity, CAPI write on the dataset, and
**write access via a `validate_only` campaign create**. A successful `GET` proves none
of these.

Token lifecycle, death codes, access tier → `02`. Asset sharing → `03`.

## 2 — Media

```bash
python3 media.py --account act_123 --video creatives/*.mp4 --image creatives/*.jpg
```

Writes `media.json` with `image_hash`, `video_id`, and a thumbnail `image_hash`. Video
upload is chunked and **asynchronous** — the script polls `status.video_status` to
`ready`, because an ad built against a still-processing video fails. Mechanics and the
`graph-video.facebook.com` deprecation trap → `04` → Media.

## 3 — Write the spec

Copy the nearest example from `scripts/specs/` and fill it:

| `creative.kind` | Shape | Example spec |
|---|---|---|
| `link_image` | single image link ad | adapt `example-link-video.json` |
| `link_video` | single video; destination goes in the CTA, `video_data` has no `link` | `example-link-video.json` |
| `dlo` | language slots via `asset_feed_spec`; `SINGLE_IMAGE`/`SINGLE_VIDEO` only, locale ids NUMERIC, ≥2 rules, exactly one `is_default`, `description` required (single space for blank) | `example-dlo.json` |
| `catalog_collection` | storefront hero + product set; needs **≥4 items** in the set (2490457) | `example-catalog-collection-tr.json` |
| `catalog_single` | one-product set, renders as a single deep-linked card, no minimum | `example-catalog-single.json` |

Catalog kinds: set `creative.template_url` or the cards carry no subids — card clicks
resolve their URL from the product feed and bypass the ad's `url_tags`. `launch.py` emits it
as `template_url_spec` and warns when it is missing.

Two limits of this adapter, before you write anything:

- **CBO only.** The campaign carries the budget; an ad set with its own
  `daily_budget_minor` is rejected. The 1-3-1 ABO screening structure in `04` cannot be
  launched from here — build it by hand or extend `launch.py`.
- **DLO objectives are unverified on ODAX.** Meta documents Multi-Language Ads against
  legacy objective names (LINK_CLICKS, CONVERSIONS, …) only. `example-dlo.json` ships
  `OUTCOME_LEADS`, which may or may not be accepted; the combination fails at the ad create
  in step 5, not in the dry run. Test it on one throwaway ad set before committing a batch.

The three decisions that carry the most cost:

- **Objective.** `OUTCOME_LEADS` for lead/registration funnels. `OUTCOME_SALES` blocks
  Lead/Submit Application events (2446814). Restricted verticals must declare the real
  `special_ad_categories` — a false or empty declaration is a violation, not a bypass.
- **Optimization event.** Aligned with, or upstream of, the payout event. A deep event
  the account cannot feed keeps the ad set learning-limited and the CPL unstable —
  optimize a higher-funnel event first, switch down once volume builds (`04` → Metric
  levers).
- **`start_time`.** Conversion goals: 06:00–08:00 geo-time, or 1–2h before the evening
  window. **Never 00:00.** Reach/traffic goals: next 00:00. Full rule → `04` → Scheduling.

Budgets go in `*_minor` keys as integers — cents, kuruş. `launch.py` rejects a float,
because `60.0` submitted as `60` is 0.60 in account currency and underdelivers all day.

`attribution.click_days` / `view_days` become `window_days` — **not** `event_window_days`,
which does not exist. Graph ignores an unknown key inside a JSON object parameter instead
of rejecting it, so the wrong name reports success and silently leaves the account default
(7-day click) in place. `verify.py` reads it back for exactly that reason.

`launch.py` opts out of 19 Advantage+ creative features by default, including
`adapt_to_placement`, which Meta turns ON unless you name it. Override with
`creative.opt_out_features` when a shape needs one — a catalog creative that wants video
cards must keep `media_type_automation` opted in.

## 4 — Dry run

```bash
python3 launch.py --spec specs/mine.json --dry-run
```

Runs `execution_options: ["validate_only"]` and creates nothing. On failure read
`error_data.blame_field_specs` — it names the exact field path at fault. Support matrix
and limits → `meta-ads/13 §10.0`.

**What a dry run can and cannot prove.** Campaign and creative payloads are validated by
Meta, because neither references an object that does not exist yet. Ad sets and ads are
built and checked locally but their API validation is **deferred to the real run**: they
carry `campaign_id` / `adset_id` / `creative_id`, and in a dry run there is no real parent
id to send — validating with a placeholder would fail on the foreign key and tell you
nothing about your payload. So a clean dry run means "the spec is well-formed and the
campaign and creatives are accepted", not "everything will create". Step 5 still validates
each object immediately before creating it, where the parents do exist.

`synchronous_ad_review` — the Ads Integrity pre-check (message language, image text rule)
— runs on ads, so it lands in step 5, not here.

## 5 — Create, PAUSED

```bash
python3 launch.py --spec specs/mine.json
```

Every object is created `PAUSED`. The state file `.meta-launch/<run_id>.json` records each
create as in-flight **before** the POST and stores the id on success. A create is never
retried on a dropped connection — the request may already have been applied — so a run
killed mid-call stops on the next attempt and tells you to reconcile rather than silently
creating a duplicate. A create that Graph *rejected* clears its marker and is retryable. There is deliberately no `--rollback`: paused objects cost nothing, and
deleting assets to tidy up is how you lose the one that actually succeeded. Reconcile by
hand from the state file. The script enforces the ordering that three separate errors
punish: campaign without budget or bid strategy (4834011) → budget + `bid_strategy`
POSTed onto the campaign (1885737) → ad set with neither.

## 6 — Verify before you trust it

```bash
python3 verify.py --state .meta-launch/<run_id>.json --spec specs/mine.json
```

Reads every object back and diffs it against the spec: budget in minor units, bid strategy,
optimization goal, promoted object, targeting, attribution, destination URL, and every
`effective_status`; identity and `url_tags` are printed for eyeballing. Timestamps compare as
instants and targeting as a subset, so a correct build does not trip on Graph's own
normalisation. A successful mutation is not
proof the object holds what you sent.

The destination diff is creative-kind aware, because each kind stores it elsewhere:
`link_data`/`video_data` for link ads, **`asset_feed_spec.link_urls` one per locale** for
DLO, and `template_data` plus `template_url_spec.web.url` for catalog. A missing
destination is a failure, not a warning.

Then preview each placement in Ads Manager. 4:5 for feeds, 9:16 for Stories/Reels.

## 7 — Review layer (only if the funnel needs one)

`07` — filter stack, white-page requirements, what is LIVE vs DEAD vs SPLIT. Cloak stays
**off** until the ad is serving. Catalog camouflage and the post-approval set swap:
`04` → Collection/catalog quirks, executed with `mutate_set.py`.

PWA funnel builders, join macros, postback contracts, QA gates → `11`.

## 8 — Activate

```bash
python3 activate.py --state .meta-launch/<run_id>.json --confirm SPEND \
                    --refresh-start 2026-09-02T07:00:00+03:00
```

Spend-producing, so it is a separate script behind an explicit flag. Refresh
`start_time` first: a paused build can outlive its own start while billing or access is
sorted, and a past `start_time` does not error — it just starts immediately, which is
the dead-hours launch step 3 exists to prevent. Ads and ad sets flip first, campaign
last.

Confirm with the operator before passing `--confirm SPEND`: final budget, schedule,
destination, creative set, and that `verify.py` exited 0.

## 9 — First hour

- Insights on fresh campaigns return empty for 15–40 min. That is not a delivery failure.
- Check `effective_status`, spend, destination, tracker receipt, billing.
- No spend and no error: future `start_time` (normal), review pending, billing hold, or
  a spend cap. Wait and verify before touching anything (`05`).
- A rejected ad cannot be enabled — build a new one, do not fight it (2490468).
- Pause on any identity, destination, measurement, or budget mismatch.

## 9.5 — Daily sync

```bash
python3 insights.py --account act_123 --level ad --date-preset yesterday --csv day.csv
```

Rows come back in the **ad account timezone** with the attribution window stated
explicitly (default here is 1d click / 1d view — Meta's own default is 7-day click,
which silently reports more conversions than a 1-day ad set earned). Push the spend as
cost into the tracker; no cost push means report cost is 0 and there is no CPL
(`tracker-ops/01` `update_costs`). Verify one day by hand, then trust it.

## 10 — Kill rules, agreed in writing

Spend-without-lead cap, CPL cap, account verdict threshold — with the TL, before launch,
not after. Ladder and the small-sample math → `senior-buyer-ops/04`. Judge accounts after
$30–50 spend, not first hours (SKILL #5). Judge cohorts on click date, never same-day
(`tracker-ops/03`).

## When a step fails

| Symptom | Go to |
|---|---|
| Any API error code | `meta-ads/14` for cause+fix, then `05` for the survival response |
| Token died / 190 | `02`, then `05` freeze protocol |
| Asset not visible to the token | `03` |
| Account restricted, checkpoint, session killed | `01` freeze protocol |
| Rejected creative, review not passing | `07` |
| Vertical seems to have no path | `10` |
| Verification / authorization demanded | `09` |
| Numbers disagree with the tracker | `tracker-ops` metric rule |
| Is this difference even real | `measurement-experimentation-ops` |
