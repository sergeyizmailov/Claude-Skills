# 16 — `metaops`: agent-facing launch interface

`metaops` is the preferred orchestration surface for an agent. It wraps the proven
`probe.py`, `launch.py`, `bulk.py`, `verify.py`, and `activate.py` implementations; it does not
reimplement Graph payloads. Underlying scripts are internal/debugging surfaces; their Graph
writes are rejected unless a workspace-bound `metaops` process launched them.

## Why this exists

- One stable command surface and JSON result schema for agents.
- Absolute paths and a fixed child working directory.
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
Every lifecycle command requires a workspace. Workspace-free legacy plans are not executable.
The skill is account-agnostic. `workspace.json` lives in a per-launch project directory outside the skills directory (one directory per BM/agency setup, holding `workspace.json`, `.metaops/`, and `.notes/` with the token env file). The CLI rejects skill-store workspaces and state directories that escape the project. Start from `scripts/specs/example-workspace.json`.

```bash
metaops --workspace . --profile <profile> --json workspace validate
metaops --workspace . --profile <profile> --json assets verify --scope core
# Catalog specs require: assets verify --scope all
metaops --workspace . --profile <profile> --json doctor
```

`--scope core` checks BM/app/System User/account/Page/PBIA/dataset. `--scope all` additionally
checks the catalog and every declared product set. A successful check writes a workspace-hash,
profile, scope, API-version, and timestamp-bound receipt; catalog specs require `all`, other
specs accept `core` or `all`. `plan` and every later lifecycle command refuse stale or changed
receipts. Verification makes no changes. Generated state lives under workspace `.metaops/`.

If a product set is empty, inspect valid catalog IDs without leaving the interface:

```bash
metaops --workspace . --profile <profile> --json assets products --limit 100
metaops --workspace . --profile <profile> --json assets set-products \
  --set <workspace-alias> --retailer-ids <id1>,<id2>
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
writing the artifact. Later source-file edits do not alter the saved plan; run `plan` again to
adopt them. As with
`launch.py --dry-run`, campaign and creative payloads reach Meta; ad-set and ad payloads are
local-only until their parent IDs exist during `apply`.

Before `activate`, complete every UI-only check in `00` §6–8. The command requires
`--confirm-ui REVIEWED`, the spec-bound verification receipt, and literal `--confirm SPEND`.

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
