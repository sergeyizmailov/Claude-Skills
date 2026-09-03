# 16 — `metaops`: agent-facing launch interface

`metaops` is the preferred orchestration surface for an agent. It wraps the proven
`probe.py`, `launch.py`, `bulk.py`, `verify.py`, and `activate.py` implementations; it does not
reimplement Graph payloads. Underlying scripts are internal/debugging surfaces; their Graph
writes are rejected unless a workspace-bound `metaops` process launched them.

## Why this exists

- One stable command surface and JSON result schema for agents.
- Absolute paths and a child working directory fixed to the workspace project.
- Immutable input snapshots bound to the saved plan by SHA-256.
- Account/Page/dataset-specific `doctor` receipts bound to each plan.
- A per-state lock that prevents two launcher processes from creating against one state.
- Creation and activation remain separate. `apply` only creates/resumes `PAUSED` objects.
- Existing verification receipts remain the activation authority; the CLI cannot bypass them.

The official `meta-ads` CLI is proprietary and optional. The unrelated open-source
`meta-ads-cli` is also optional. Neither owns launches (`12`).

## Workspace contract

`workspace.json` is the portable, non-secret control plane. A profile binds one ad account to
its BM, app, System User, Page/PBIA, dataset, catalog, product-set aliases, currency, and
timezone. `blocked_accounts` can never be selected. Credentials stay in the environment.
The CLI discovers the nearest `workspace.json` from the current directory upward; explicit
`--workspace` wins, followed by `METAOPS_WORKSPACE`.
Every lifecycle command requires a workspace; workspace-free legacy plans are not executable.
Account-agnostic: `workspace.json` lives in a per-launch project directory outside the skills
directory (one per BM/agency setup — holds `workspace.json`, `.metaops/`, `.notes/` with the
token env file). CLI rejects skill-store workspaces and state directories escaping the project.
Start from `scripts/specs/example-workspace.json`.
`workspace.json.api_version` must exactly equal the launcher's effective `graph.API_VERSION`
(**`v26.0`** in this release without an explicit version override), not merely match the `vNN.N`
shape. `metaops` rejects a mismatch before it makes a Graph call; after a launcher-version
upgrade, update the workspace and re-plan and re-verify its receipts.

```bash
metaops --workspace . --profile <profile> --json workspace validate
metaops --workspace . --profile <profile> --json assets verify --scope core
# Catalog specs require: assets verify --scope all
metaops --workspace . --profile <profile> --json doctor
```

`--scope core` checks BM/app/System User/account/Page/PBIA/dataset; `--scope all` adds catalog +
every declared product set. A successful check writes a workspace-hash, profile, scope,
API-version, and timestamp-bound receipt; catalog specs require `all`, other specs accept `core`
or `all`. `plan` and every later lifecycle command refuse stale or changed receipts. Verification
makes no changes; generated state lives under workspace `.metaops/`.

If a product set is empty, inspect valid catalog IDs without leaving the interface:

```bash
metaops --workspace . --profile <profile> --json assets products --limit 100
metaops --workspace . --profile <profile> --json assets set-products \
  --set <workspace-alias> --retailer-ids <id1>,<id2> --confirm SET
metaops --workspace . --profile <profile> --json assets verify --scope all
```

## Single-account lifecycle

From the package directory, install with `uv tool install .`. Without installation, use
`uv run --project /path/to/meta/meta-grey-ops metaops` before every argument shown below.
Global flags precede the command. Put `--json` before the subcommand when an agent consumes it.
Child diagnostics go to stderr; stdout contains exactly one `metaops.result/v1` object.

```bash
metaops --workspace . --profile <profile> --json doctor
metaops --workspace . --profile <profile> --json media --image creative.jpg --video creative.mp4
metaops --workspace . --profile <profile> --json plan --spec launches/mine.json
metaops --workspace . --profile <profile> --json apply --plan .metaops/plans/<plan>.json
metaops --workspace . --profile <profile> --json verify --plan .metaops/plans/<plan>.json
metaops --workspace . --profile <profile> --json status --plan .metaops/plans/<plan>.json
metaops --workspace . --profile <profile> --json activate --plan .metaops/plans/<plan>.json \
  --confirm-ui REVIEWED --confirm SPEND
```

`doctor` must pass first; its account/Page/dataset-specific receipt is checked by every later command and
expires after 24 hours by default (`METAOPS_DOCTOR_MAX_AGE_SECONDS` overrides the TTL).
Media upload and product-set repair also require that fresh receipt. Product-set repair performs
a live System User/catalog/set ownership check that permits an empty set, then invalidates any
old `all` asset receipt; rerun `assets verify --scope all` after repair.
`plan` snapshots the normalized spec, then runs the existing API `validate_only` path before
writing the artifact. Later source-file edits don't alter the saved plan; run `plan` again to
adopt them. As with `launch.py --dry-run`: campaign and creative payloads reach Meta; ad-set and
ad payloads are local-only until their parent IDs exist during `apply`.

Before `activate`, complete every UI-only check in `00` §6–8. The command requires
`--confirm-ui REVIEWED`, the spec-bound verification receipt, and literal `--confirm SPEND`.

## Feed (catalog as Google Sheet, `17`)

```bash
metaops --workspace . --profile <p> --json feed sync  --sheet <url> [--gid N] [--update-only] --confirm FEED   # POST /{feed_id}/uploads url=<csv export> → poll end_time
metaops --workspace . --profile <p> --json feed swap  --sheet <url> --file items.json --confirm FEED             # validate prospective rows → upsert → sync → prove no ad re-entered review
```

`feed_id` comes from `profiles.<p>.feed_id`; `--feed-id` is accepted only when the profile has no
declared feed. Sheet CSV export needs a public link; tab
gid resolves via `GSHEETS_JSON_KEY_FILE` or `--gid`. `swap` refuses while any ad on the account is
`PENDING_REVIEW`/`IN_PROCESS`/`PREAPPROVED` (`--force` overrides); exit 1 + phase `re_review`
lists ads whose status flipped into review after the fetch. Result `data.upload`:
`num_persisted_items`, `num_invalid_items`, `error_count`, `errors[]`. `finished=false` = still
running after `--wait` (default 120 s); re-check `GET /{upload_id}`.

## Edit / clone / rules (wrap `edit.py`, `clone.py`, `rules.py`)

```bash
metaops … edit status  (--ids a,b | --state run.json --level adset | --all --level campaign) --status PAUSED|ACTIVE --confirm PAUSE|SPEND
metaops … edit budget  --ids … (--budget-minor N | --budget-pct ±N) [--force-step] [--confirm SPEND]   # ±20%/late-day guard from edit.py
metaops … edit rename  --ids … --prefix P [--suffix S]
metaops … edit ramp    --ids … --step 20 --confirm RAMP                              # exactly one rung; wait 48–72h before the next call
metaops … clone campaign|adset|ad <id> [--times N] [--prefix/--suffix] [--start ISO] [--into-campaign/--into-adset] [--dry-run]   # /copies, level by level, PAUSED; skips deleted/archived children
metaops … rules ladder --target-minor N --event E --level ADSET|AD [--rungs 0-6] [--mode notify|pause] [--ids] [--prefix] [--confirm RULES]
metaops … rules list | history [--since] | execute --rule-id ID --confirm EXECUTE | delete --prefix P --confirm DELETE
```

ACTIVE / budget raise → `--confirm SPEND`; PAUSED → `--confirm PAUSE`; `--mode pause` →
`--confirm RULES`; manual rule execution → `--confirm EXECUTE`. For opaque IDs, the child reads
back `account_id` and refuses an object outside the profile. Children print a final `*.result/v1`
JSON line that lands in `data`.

## Catalog lifecycle (`17`)

```bash
metaops … catalog create --name N [--vertical commerce] --confirm CREATE          # POST /{business}/owned_product_catalogs → put id in workspace.json
metaops … catalog list | access                                                   # owned catalogs; SU assigned_product_catalogs + business match
metaops … catalog feed create --name N --url <csv/sheet export> --schedule hourly|daily|weekly [--hour H] [--update-only] --confirm CREATE
metaops … catalog feed list | uploads [--feed-id]
metaops … catalog set create --name N (--filter f.json | --retailer-ids a,b) --confirm CREATE   # filter sent as dict, encoded once
metaops … catalog set list · products list [--set-id] [--limit]
metaops … catalog products batch --file items.json --method UPDATE|DELETE|CREATE [--wait s] --confirm BATCH   # items_batch item_type=PRODUCT_ITEM → check_batch_request_status
```

`catalog create` requires a token for an **Admin-role System User**. An Employee System User can
maintain a catalog explicitly assigned to it, but cannot create one at the BM edge; see `02` §2.
The `workspace.json` used here must set `api_version` exactly to the effective launcher version
(`v26.0` in this release without an explicit version override).

`schedule` is a JSON string (`interval HOURLY|DAILY|WEEKLY|MONTHLY, hour, minute, day_of_week,
timezone, url`). items_batch takes feed-format `price` "9.99 USD"; `/products` takes integer
minor units — the command passes the file through verbatim. Unverified: `status` strings of
`check_batch_request_status` (polled case-insensitively).

## Business Manager setup (no billing surface exists)

```bash
metaops … business assets                                                          # owned/client accounts, pages, pixels, catalogs, system users
metaops … business adaccount create --name N --currency USD --timezone-id 1 [--end-advertiser B] --confirm CREATE   # new-BM cap = 1 (`03`)
metaops … business pixel create --name N [--is-crm] --confirm CREATE · pixel share --account act_X --confirm SHARE · pixel shared
metaops … business capi test --event Lead --test-code TESTxxxx [--url …]           # /{dataset}/events, hashed dummy user_data → Events Manager "Test events"
metaops … business user invite --email E --role EMPLOYEE|ADMIN --confirm SHARE
metaops … business user assign --user-id U --asset adaccount|page|pixel --tasks … --confirm SHARE   # /assigned_users {user,tasks}; pixel: ADVERTISE,ANALYZE,EDIT,UPLOAD
metaops … business partner share --partner-business B --asset adaccount|page|pixel --tasks … --confirm SHARE       # /agencies {business,permitted_tasks}
```

## Operate

```bash
metaops … review [--state run.json | --ids a,b | --all] [--previews --format DESKTOP_FEED_STANDARD,MOBILE_FEED_STANDARD]   # ad_review_feedback, issues_info; exit 1 on DISAPPROVED/WITH_ISSUES
metaops … monitor --accounts accounts.json [--stall-impressions 40] [--telegram] [--log] [--out-json rows.json]   # global `--json` remains before `monitor`; TG_BOT_TOKEN + TG_CHAT_ID env only
metaops … comments list [--ads a,b | --all]                                               # Page token, read-only
metaops … comments hide --ads a,b|--all (--matching REGEX | --all-comments) --confirm HIDE
metaops … comments delete --ads a,b|--all --matching REGEX --confirm DELETE
metaops … page show | set --avatar f --cover f --about "…" --website URL --confirm PAGE | list-pages
metaops … insights pull --level ad (--date-preset yesterday | --since --until) [--csv]
metaops … insights leaderboard --accounts accounts.json [--date-preset] [--top N] [--csv]            # joins on ad_name only when all rows have one currency
```

## Bulk lifecycle

```bash
metaops --workspace . --profile <profile> --json bulk-plan \
  --template specs/mine.json --accounts accounts.json --run wave-1
metaops --workspace . --profile <profile> --json bulk-apply --plan .metaops/plans/<bulk-plan>.json --verify
metaops --workspace . --profile <profile> --json status --plan .metaops/plans/<bulk-plan>.json
```

For a multi-account DLO/catalog template, prove one real tree first, then pass `--dlo-tested`
to `bulk-apply`. Activate one reviewed account at a time; there is deliberately no activate-all
command:

```bash
metaops --workspace . --profile <profile> --json bulk-activate \
  --plan .metaops/plans/<bulk-plan>.json --account act_123 \
  --confirm-ui REVIEWED --confirm SPEND
```

`bulk-activate` revalidates fresh doctor and asset receipts for the selected account only;
an unrelated sibling's expired receipt does not block it. The complete batch input, workspace,
item identities, and state bindings remain hash-validated.

## Failure contract

- Non-zero child exit: `ok=false`, child exit code preserved, redacted diagnostics on stderr.
- Timeout or unknown POST outcome: inspect the state `in_flight` entry and reconcile before a
  retry. Do not remove the lock or marker merely to force progress.
- A saved snapshot or bound doctor receipt changed after `plan`: command refuses; create a new
  doctor receipt and plan. Editing the original source does not mutate an existing plan.
- Existing `.metaops.lock`: another process owns that state. Inspect its PID/timestamp; only
  remove a stale lock after confirming no launcher process is running.
- API version changed: old plan is refused; create a new plan under the pinned version.

Offline checks:

```bash
SKILL_ROOT=/path/to/meta/meta-grey-ops
PYTHONDONTWRITEBYTECODE=1 uv run --isolated --project "$SKILL_ROOT" python "$SKILL_ROOT/scripts/test_metaops.py"
PYTHONDONTWRITEBYTECODE=1 uv run --isolated --project "$SKILL_ROOT" python "$SKILL_ROOT/scripts/test_workspace.py"
PYTHONDONTWRITEBYTECODE=1 uv run --isolated --project "$SKILL_ROOT" python "$SKILL_ROOT/scripts/selftest.py"
uv run --isolated --project "$SKILL_ROOT" ruff check --no-cache "$SKILL_ROOT/scripts"
uv lock --check --offline --project "$SKILL_ROOT"
```
