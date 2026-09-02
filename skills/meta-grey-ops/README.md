# Meta Agent Ops

`metaops` is the deterministic execution layer for AI agents operating Meta Ads. It keeps
campaign creation PAUSED, binds plans to immutable specs and verified assets, reads the result
back, and makes activation a separate command.

## Install

```bash
cd meta/meta-grey-ops
uv tool install .
# or, from the same folder:
python3 -m pip install .
```

Credentials remain environment variables. Egress follows the BM/operator network profile; token
type does not decide it. Use `META_PROXY` when that identity is operated through a fixed proxy.
Allow direct egress only when the current IP is deliberately the expected IP for that BM:

```bash
export META_TOKEN='...'
export META_ALLOW_NO_PROXY=1
```

## Agent workflow

Global flags precede the command.
`--workspace` may be omitted when the current directory is inside a workspace; discovery walks
upward to the nearest `workspace.json`. `METAOPS_WORKSPACE` is the environment fallback.
The skill is account-agnostic. `workspace.json` lives in a per-launch project directory outside the skills directory (one directory per BM/agency setup, holding `workspace.json`, `.metaops/`, and `.notes/` with the token env file). The CLI rejects skill-store workspaces and state directories that escape the project. Start from `scripts/specs/example-workspace.json`.

```bash
metaops --workspace . --profile <profile> --json workspace validate
metaops --workspace . --profile <profile> --json assets verify --scope core
# Catalog specs require: assets verify --scope all
metaops --workspace . --profile <profile> --json doctor
metaops --workspace . --profile <profile> --json plan --spec <campaign-spec.json>
metaops --workspace . --profile <profile> --json apply --plan .metaops/plans/<plan>.json
metaops --workspace . --profile <profile> --json verify --plan .metaops/plans/<plan>.json
metaops --workspace . --profile <profile> --json status --plan .metaops/plans/<plan>.json
metaops --workspace . --profile <profile> --json activate --plan .metaops/plans/<plan>.json \
  --confirm-ui REVIEWED --confirm SPEND
```

`workspace.json` owns non-secret asset routing. Generated plans, snapshots, receipts, locks,
and run state live under the workspace's `.metaops/` directory. Lifecycle commands require a
workspace; legacy workspace-free plans and direct low-level Graph writes are rejected.

If `metaops` is not installed, replace it with
`uv run --project /path/to/meta/meta-grey-ops metaops`. Successful asset and doctor checks write fresh,
hash-bound receipts; `plan` refuses a missing, stale, or changed receipt.

Upload media through the same workspace boundary:

```bash
metaops --workspace . --profile <profile> --json media --image creative.jpg --video creative.mp4
```

Low-level scripts are implementation/debugging surfaces. Agents may run their read-only modes,
but all Graph mutations must enter through `metaops`.

The proprietary official `meta-ads` package and unrelated open-source `meta-ads-cli` are not
dependencies. They may be used independently for ad-hoc reads; `metaops` remains the launch
authority.
