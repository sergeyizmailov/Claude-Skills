# 00 — Launch runbook (start here for any API launch)

Ordered path "have a token" → "spending". Every other file is an exception handler for one
step below — don't read ahead; if a step passes, move on.

Reviewed 2026-09-02. `metaops` is the only agent-facing Graph write interface. The scripts in
`../scripts/` are implementations/debugging surfaces; direct write calls are rejected.

For agent-driven launches, use the installed `metaops` CLI (`16`). When `workspace.json`
exists, start with:

```bash
metaops --workspace . --profile <name> --json workspace validate
metaops --workspace . --profile <name> --json assets verify --scope core
# Use --scope all when the spec contains catalog_collection or catalog_single.
metaops --workspace . --profile <name> --json doctor
```

It resolves non-secret routing, blocks forbidden accounts and broken asset relationships,
binds inputs to a saved plan, serializes each state, and keeps activation separate.

```
0 gate  →  1 access  →  2 media  →  3 spec  →  4 dry run  →  5 create PAUSED (one or bulk)
        →  6 verify  →  7 review layer  →  8 activate
        →  9 first hour  →  9.5 daily sync  →  10 kill rules
```

**Never hand-assemble a Graph payload.** Agent writes the JSON spec; `launch.py` writes API
calls. Defaults every object gets: `SKILL.md` § Launch defaults.

## Vertical parameters

| Vertical | Gate before spend | Payout event | First optimization event | Playbook |
|---|---|---|---|---|
| iGaming / casino | A&V gambling authorization + per-territory licence, filed **before any ad exists**; 19 markets take no gambling ads | FTD (or qualified FTD) | `COMPLETE_REGISTRATION`, switch to `PURCHASE` at ~20-30 FTD | `playbooks/casino.md` |
| Nutra | Health-claim policy | Confirmed COD order | `LEAD` / `PURCHASE` | `playbooks/nutra.md` |
| Crypto / trading | Crypto authorization; exemption boundary decides if there is a path | Qualified reg / deposit | `COMPLETE_REGISTRATION` | `playbooks/crypto-trading.md` |
| News → Telegram | No formal gate; funnel is the risk | Subscribe / bot join | `LEAD` | `playbooks/news-tg.md` |
| Anything else | **`10` Q1/Q2 first** | — | — | shape ports from any playbook |

## 0 — Path exists?

`10` Q1 (permission required before spend) / Q2 (no path in any geo). Clear gate in `09`
**before any ad object exists**. Approvals bind to a **specific portfolio + ad account** — a
replacement account needs a new approval.

## 1 — Access and write probe

Operator hands you, verbatim into gitignored notes: token, ad account id(s), Page id,
pixel/dataset id, tracker campaign URL, proxy (if user token). Token type decides env (`02`
owns detail):

```bash
export META_TOKEN='...'                               # never on the command line
# user/long-lived token minted in an antidetect profile → same exit IP, always:
export META_PROXY='socks5h://user:pass@host:port'      # when this BM uses a fixed proxy; socks5:// breaks TLS (01)
# Or, only when direct egress from the current IP is intentional for this BM:
export META_ALLOW_NO_PROXY=1
export META_APP_SECRET='...'                          # optional; adds appsecret_proof
metaops --workspace . --json doctor --whoami
metaops --workspace . --profile <name> --json doctor --create-pbia
```

Exit 0 or don't launch. Gates, each separate: token identity · granted scopes
(`ads_management`+`ads_read` required, rest of golden set warned) · account in
`/me/adaccounts` (assigned to token, not merely readable) · account status + funding · Page
token + PBIA · **pixel attached to THIS ad account** (shared to BM ≠ on account, 1815045) ·
CAPI write · `validate_only` write probe. A successful `GET` proves none of these.

Bulk planning validates every selected workspace profile before any PAUSED build.

Token died / access denied → `02`. Asset not visible → `03`.

## 2 — Media

```bash
metaops --workspace . --profile <name> --json media \
  --video creatives/*.mp4 --image creatives/*.jpg
```

Writes `media.json` (`image_hash`, `video_id`, thumbnail `image_hash`). Hashes are
**account-scoped** — upload per account; bulk puts them in the account row's `media` block.
Video async, script polls `video_status=ready`. Mechanics → `04` → Media.

## 3 — Write the spec

Copy nearest example from `scripts/specs/`, fill it. Put `"currency": "USD"` (account's) in
spec — stops a cents-template landing on a TWD/JPY account at 100x.

| `creative.kind` | Shape | Example |
|---|---|---|
| `link_image` | single image link ad | adapt `example-link-video.json` |
| `link_video` | single video; destination in CTA, `video_data` has no `link` | `example-link-video.json` |
| `link_carousel` | 2–10 `cards`, each `image_hash` XOR `video_id`; cards inherit `link` | `example-abo-1-3-1.json` |
| `dlo` | language slots via `asset_feed_spec`; SINGLE_IMAGE/SINGLE_VIDEO only, locale ids NUMERIC, ≥2 rules, one `is_default`, `description`=" " for blank | `example-dlo.json` |
| `catalog_collection` | storefront hero + product set, **≥4 items** (2490457) | `example-catalog-collection-tr.json` |
| `catalog_single` | one-product set → one deep-linked card, no minimum | `example-catalog-single.json` |

Catalog kinds: fastest source is one Google Sheet edited via service account and pulled by Commerce
Manager as a scheduled feed — `17` (`sheetfeed`). Swap links/images in the sheet, not via batch API.

Structure is a spec choice, not a script limit:
- **CBO** — `campaign.daily_budget_minor`, ad sets budget-less.
- **ABO** — no campaign budget, every ad set carries `daily_budget_minor` (+ `bid_strategy`,
  `bid_amount_minor` for COST_CAP/BID_CAP). 1-3-1 shape: `example-abo-1-3-1.json`. Mixed or
  absent → spec rejected.
- **EU/EEA** — `dsa_beneficiary` + `dsa_payor` on ad set (`example-eu-dsa.json`).

Costliest decisions:
- **Objective.** `OUTCOME_LEADS` for lead/registration funnels. `OUTCOME_SALES` blocks
  Lead/Submit Application events (2446814). Restricted verticals declare real
  `special_ad_categories` — false/empty is a violation, not a bypass.
- **Optimization event.** Aligned with or upstream of payout event; a deep event the account
  can't feed keeps the ad set learning-limited. `OFFSITE_CONVERSIONS` +
  `promoted_object{pixel_id, custom_event_type}` for site events; `LEAD_GENERATION` is the
  lead-FORMS goal, not a website goal (`04`).
- **`start_time`.** Conversions: 06:00–08:00 geo-time or 1–2h before evening window, **never
  00:00**. Reach/traffic: next 00:00 (`04` → Scheduling).

Attribution: omit key → 1d click/1d engaged-view/1d view. Set only to deviate;
`"account_default"` sends nothing. **Immutable after create** (1504040) — wrong window = new
ad set. Enhancements + multi-advertiser OFF by default; catalog creative wanting video cards
must opt `media_type_automation` back in via `creative.opt_out_features`.

Two adapter gaps: DLO objectives documented against legacy names only — `OUTCOME_*`
acceptance unverified, a dry run can't catch it (ad create can). Test one DLO ad before a
batch.

## 4 — Dry run

```bash
metaops --workspace . --profile <name> --json plan --spec specs/mine.json
metaops --workspace . --json bulk-plan \
  --template specs/mine.json --accounts accounts.json --run <wave>
```

`bulk-plan` deliberately has no `--profile`: each row in `accounts.json` selects its bound
workspace profile. An absent or mismatched binding fails; do not add a catch-all profile flag.

`execution_options: ["validate_only"]` — Meta validates, nothing created. On failure read
`error_data.blame_field_specs` (names the field path at fault). Campaign+creative payloads
validated by Meta now; ad sets/ads reference parents that don't exist yet, so checked locally
now and by Meta immediately before each real create in step 5 (`synchronous_ad_review` also
runs there). `bulk.py` refuses a real run until whole batch has a clean dry-run marker
The saved plan hashes every input; editing a bound input requires a new plan.

## 5 — Create, PAUSED

```bash
metaops --workspace . --profile <name> --json apply --plan .metaops/plans/<plan>.json
metaops --workspace . --json bulk-apply \
  --plan .metaops/plans/<bulk-plan>.json --verify [--dlo-tested]
```

DLO/catalog template on >1 account: use `metaops apply` to build ONE account PAUSED, verify it,
then pass `--dlo-tested` to `bulk-apply` — a dry run cannot prove the
objective/creative combination is accepted (`04` → DLO).

Every object created `PAUSED`. Workspace state `.metaops/<run_id>.json` records each create
in-flight **before** the POST, id on success; a create is never retried on dropped connection
(may have applied) — killed run stops next time, asks to reconcile instead of duplicating. A
Graph *rejection* clears the marker and is retryable. No `--rollback`: paused objects cost
nothing; deleting to tidy up is how you lose the one that succeeded.

Bulk: substitutes account/page/pixel/IG per row, expands `{tag}` in every name (campaign name
= account code is the tracker mapping contract, `03`), deep-merges `overrides`, applies
per-account `media`, writes resolved specs below `.metaops/bulk/<run>/`, runs each
account with its own state. One account failing doesn't stop the rest; summary names what to
reconcile. Same template + same account again → resumes, never duplicates.

## 6 — Verify before you trust it

```bash
metaops --workspace . --profile <name> --json verify --plan .metaops/plans/<plan>.json
```

`verify.py` fails (no receipt) on **incomplete** state: any `in_flight` key (create whose
outcome is unknown — live 2026-09-02 a creative POST got a bare 503; object didn't exist, but
only Ads Manager can tell you that) or any spec ad set/ad missing from `objects`. Reconcile,
then re-run `metaops apply --plan …` — it resumes from state and creates only what's missing.

Reads every object back, diffs: budget (campaign under CBO, ad set under ABO) in minor units,
bid strategy, optimization goal, promoted object, targeting, **attribution_spec**, **DSA
fields**, destination per creative kind, `template_url_spec`, **`contextual_multi_ads` =
OPT_OUT**, **no Advantage+ feature left OPT_IN**, every `effective_status`. A successful
mutation isn't proof the object holds what you sent — Graph ignores unknown keys inside JSON
parameters and fills enum defaults silently.

Where API can't prove it, UI must, **while PAUSED**: Multi-advertiser checkbox on
FORMAT_AUTOMATION collection creatives (field not readable there), placement previews (4:5
feeds, 9:16 Stories/Reels).

## 7 — Review layer (only if funnel needs one)

`07` — filter stack, white-page requirements, LIVE/DEAD/SPLIT status. Cloak stays **off**
until ad is serving. Catalog product-set repair: `04` → Collection/catalog quirks, executed
through `metaops assets set-products`. PWA builders → `11`.

## 8 — Activate

```bash
metaops --workspace . --profile <name> --json activate \
  --plan .metaops/plans/<plan>.json --confirm-ui REVIEWED --confirm SPEND \
  --refresh-start 2026-09-03T07:00:00+03:00

# For a bulk plan, activate exactly one reviewed account per command:
metaops --workspace . --profile <name> --json bulk-activate \
  --plan .metaops/plans/<bulk-plan>.json --account act_123 \
  --confirm-ui REVIEWED --confirm SPEND \
  --refresh-start 2026-09-03T07:00:00+03:00
```

Spend-producing, separate command behind explicit flags. There is no activate-all command.
Refresh `start_time` first — a past
`start_time` doesn't error, it starts immediately in dead hours. Ads/ad sets first, campaign
last; stops on first failure. Before `--confirm SPEND`, confirm with operator: budget in
**major units and currency**, schedule, destination, creative set, `metaops verify` exit 0
on this exact state file (writes `<state>.verified.json` with state hash + spec hash;
the internal activator refuses if state changed since, receipt made without `--spec`, or against a
different spec), UI multi-advertiser check done.

## 9 — First hour

- Insights on fresh campaigns empty 15–40 min. Not a delivery failure.
- Check `effective_status`, spend, destination, tracker receipt, billing.
- No spend, no error: future `start_time`, review pending, billing hold, spend cap. Wait,
  verify before touching anything (`05`).
- Rejected ad cannot be enabled (2490468) — build a new one.
- **Any budget/billing anomaly: pause first, diagnose second.** Verified 2026 incident: agent
  debated currency units while a 100x budget kept spending.

## 9.1 — Operate

```bash
metaops … review --state .metaops/run.json            # ad_review_feedback / issues_info; exit 1 on rejects
metaops … monitor --accounts accounts.json --telegram   # status + spend sweep, STALL (≥40 impr, 0 clicks), survival log, TG alerts
metaops … rules ladder --target-minor 1200 --event … --level ADSET --mode pause --confirm RULES
metaops … edit budget --ids … --budget-pct +20 --confirm SPEND · edit status --ids … --status PAUSED --confirm PAUSE · clone campaign <id> --times 2
metaops … comments hide --all --matching "scam|fake" --confirm HIDE
metaops … insights pull --level ad --date-preset yesterday --csv day.csv · insights leaderboard --accounts accounts.json
```

All operate mutations are workspace-bound `metaops` commands (`16`); do not bypass the
transport guard. Still UI-only: appeals, billing, BM/Page creation. Ladder math/traps →
`senior-buyer-ops/04`.

## 9.5 — Daily sync

```bash
metaops --workspace . --profile <name> --json insights pull \
  --level ad --date-preset yesterday --csv .metaops/day.csv
```

Rows in ad account timezone, attribution window stated explicitly (1d/1d here; Meta's own
default is 7d click). Push spend as cost into tracker (`tracker-ops/01` `update_costs`); no
cost push = no CPL. Verify one day by hand, then trust it.

## 10 — Kill rules, agreed in writing

Spend-without-lead cap, CPL cap, account verdict threshold — with TL, before launch. Ladder/
small-sample math → `senior-buyer-ops/04`. Use the workspace-bound `metaops rules` commands in
§9.1. Judge accounts after $30–50, cohorts on click date
(`tracker-ops/03`).

## When a step fails

| Symptom | Go to |
|---|---|
| Any API error code | `meta-ads/14` for cause+fix, then `05` for survival response |
| Token died / 190, scopes missing, "not visible to token" | `02` |
| Asset shared to BM but absent on account | `03` (pixel/page assignment) |
| Account restricted, checkpoint, session killed | `01` freeze protocol |
| Rejected creative, review not passing | `07` |
| Vertical seems to have no path | `10` |
| Verification/authorization demanded | `09` |
| Spec rejected locally (budget mode, advantage_audience, DSA, currency) | message names the fix; shapes in `scripts/specs/` |
| Numbers disagree with tracker | `tracker-ops` metric rule |
| Is this difference even real | `measurement-experimentation-ops` |
