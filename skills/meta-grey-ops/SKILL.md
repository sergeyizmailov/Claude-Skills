---
name: meta-grey-ops
description: "Launch and run Meta (FB/IG) ads via the Marketing API from a token — access/scopes/System User, MCP vs API, PAUSED bulk launch across ad accounts, catalog/DLO/carousel creatives, catalog as an agent-edited Google Sheet, attribution 1/1/1, Advantage+ and multi-advertiser opt-out, EU DSA, plus grey-market survival: antidetect/proxy/session hygiene, agency accounts, token death, cloaking/review-layer tricks, verification gates, no-path verticals, per-vertical playbooks (casino, nutra, crypto, news-tg). Use for: 'launch FB ads through the API', 'I have a BM access token, set up campaigns', 'bulk launch on N accounts', 'connect Claude to Meta ads / MCP', 'why did the ad set create fail'. Clean marketing theory = meta-ads; tracker metrics = tracker-ops."
---

# Meta Grey Ops

Reviewed 2026-09-02. Launch/operate via API on your own token (= autolaunch SaaS without UI, `13`) + grey survival. "buy well" → `meta-ads` · "count & sync" → `tracker-ops` · "portfolio decisions" → `senior-buyer-ops`.

## Start here

| You are… | Read | Then |
|---|---|---|
| In a directory with `workspace.json` | `references/16-metaops-agent-cli.md` | use `metaops --workspace … --json`; stop reading |
| Handed a token / asked to launch anything via API | `references/00-launch-runbook.md` | create a workspace in a project dir outside the skill (`scripts/specs/example-workspace.json`), validate it, then use `metaops` |
| Setting up access, deciding MCP vs API, minting/handing over a token | `references/02-access-tokens-and-mcp.md` | come back to `00` |
| Hit an error, a gate, a rejection, a dead token | `00` § "When a step fails" | the one file it names |

**Agent writes a JSON spec; `metaops` controls the lifecycle; `launch.py` writes Graph
payloads.** Never hand-assemble a payload or invoke a low-level Graph mutation directly.
New shape → extend `metaops`/the implementation and its tests.

## Launch defaults (what every ad set/ad gets unless the spec says otherwise)

| Setting | Default | Enforced by | Override |
|---|---|---|---|
| Object status at create | `PAUSED`, all levels | internal launcher; spend only via `metaops activate --confirm SPEND` | none |
| Attribution | 1d click / 1d engaged-view / 1d view on conversion goals; **1d click only** on LINK_CLICKS/REACH/etc. (Meta rejects view windows there, 1885501). Set at CREATE (immutable after, 1504040) | `launch.py` `DEFAULT_ATTRIBUTION`; `verify.py` reads it back | `attribution: {...}` or `"account_default"` |
| Advantage+ creative enhancements | every feature `OPT_OUT` incl. `adapt_to_placement`; music via `audios: []` | `launch.py` `DEFAULT_OPT_OUT`; `verify.py` flags any `OPT_IN` | `creative.opt_out_features` |
| Multi-advertiser ads | `contextual_multi_ads: OPT_OUT` on every creative (Meta Ads MCP cannot set it — its creatives inherit OPT_IN) | `launch.py`; readable on link/template creatives, **UI check while PAUSED** on FORMAT_AUTOMATION collections | `creative.multi_advertiser: true` |
| Advantage+ audience | must be explicit `true/false` in `targeting` | spec rejected without it (v23+ Graph rule) | — |
| Placements | Advantage+ (all) | pass `publisher_platforms`/positions to restrict; `["facebook"]` alone is warned (it is the wrong 1772103 fix) | targeting keys |
| Budget mode | CBO (`campaign.daily_budget_minor`) **or** ABO (every `adsets[].daily_budget_minor`) | spec rejected if both/neither; cap strategies need `bid_amount_minor` | — |
| Budget unit | integer minor units; **whole units on no-offset currencies (TWD, JPY, KRW, HUF…)** | `launch.py` prints every budget in major units and fails on `spec.currency` ≠ account currency | put `currency` in the spec |
| `start_time` | conversions 06:00–08:00 geo-time, never 00:00; reach/traffic next 00:00 | spec required; `metaops activate --refresh-start` | — |
| Identity | Page + PBIA (`instagram_user_id: "auto"`) | internal launcher resolves it; `metaops doctor --create-pbia` creates it | explicit id |
| EU/EEA geo | `dsa_beneficiary` + `dsa_payor` required | spec rejected without them | — |
| Tracking | spec-level `url_tags` inherited by every ad; catalog cards need `template_url` | `launch.py`; `verify.py` diffs destination per creative kind | per-creative `url_tags` |
| Special ad categories | must be declared explicitly (`[]` or the real one) | spec rejected if absent | — |

Not in the scripts and therefore on you: account-level "test new optimizations" enrollment
(Advertising Settings, UI only), billing/card binding, appeals, BM and Page creation.

## Non-negotiables (always apply)

1. **One identity = one egress profile.** Browser, API, and token operations use the BM/operator's
   assigned IP or proxy. Token type does not waive this rule. Scripts refuse to run without
   `META_PROXY` unless `META_ALLOW_NO_PROXY=1` deliberately confirms that direct egress from the
   current IP is expected for this BM (`01`, `02`).
2. **A token rides a login session.** Logout / password change / security rotation kills every
   token minted from it, 60-day included. System User tokens are session-independent — prefer
   them when the BM is yours (`02`).
3. **Restriction / checkpoint = FREEZE.** No re-logins, token regen, profile edits (`01`).
4. **Never touch a work identity from a personal browser or IP.**
5. **Judge accounts after $30–50 spend, not the first hours.** Keep a replacement reserve (`03`).
6. **Bulk = one creative per account.** Identical creative across accounts overheats your own
   auction; `bulk.py` warns, you decide (`03`).

## References

| Need | Reference |
|---|---|
| **Ordered launch path — START HERE** | `references/00-launch-runbook.md` |
| Antidetect, proxies, IP/session discipline, checkpoints, domain/pixel rotation | `references/01-infra-and-identity.md` |
| **Access: app use cases, scopes, System User vs user token, token death, MCP vs API vs CLI, operator handoff checklist** | `references/02-access-tokens-and-mcp.md` |
| Agency setups, BMs, asset sharing, BM-ban recovery, billing gotchas, naming, replacements | `references/03-agency-accounts-and-bm.md` |
| Why the scripts do what they do: structures, params, bid strategies, scheduling, DLO, catalog quirks, media, warm-up, re-moderation | `references/04-mass-launch-api.md` |
| API errors — grey survival response (freeze/replace/rotate); canonical code→fix is `meta-ads/14` | `references/05-api-error-catalog.md` |
| Why accounts die, attributed: hazard-rate forensics, balanced infra tests | `references/06-portfolio-forensics.md` |
| Review-layer filters, cloaking, DLO/catalog/unicode/CTM tricks, BM verification | `references/07-review-layer-and-cloaking.md` |
| Location fees, tz/currency 60d lock, sanctioned targeting, WABA | `references/08-geo-fees-and-waba.md` |
| Verification gates: business / beneficial-owner / identity, gambling+crypto+financial authorization, order | `references/09-verification-gates.md` |
| **Does this vertical have a path at all** — permission-before-spend and no-path lists | `references/10-no-path-and-permissions.md` |
| PWA funnel builders: join macros, postbacks, CAPI, QA gates | `references/11-pwa-funnel-builders.md` |
| **Meta Ads CLI** (`pip install meta-ads`): what it can do, flags, traps — read before reaching for it | `references/12-meta-ads-cli.md` |
| **Autolaunch parity**: what Dolphin Cloud / FBTool / cabinet.partners do, how (EAAB tokens), feature → our script or UI-only | `references/13-autolaunch-parity.md` |
| Meta Ads MCP live tool inventory (106 tools, params) | `references/15-mcp-tools-live.md` |
| **Agent launcher**: plan/apply/verify/activate contract, JSON output, locks | `references/16-metaops-agent-cli.md` |
| **Catalog as one Google Sheet** — service-account setup, Commerce Manager scheduled feed, columns, `sheetfeed` | `references/17-catalog-via-google-sheets.md` |
| Per-vertical playbooks (casino, nutra, crypto-trading, news-tg) | `playbooks/` — numbers are dated vendor/team priors, replace with live data |

Declared gaps: no dating or loans playbook; `APP_PROMOTION` only directional in `playbooks/casino.md`.

## Scripts

`metaops` is the agent write boundary: rejects workspaces inside the skills directory; generated
files belong in the project workspace. Low-level scripts: read-only inspection only — POST/DELETE
enabled only inside a validated workspace-bound `metaops` process. Run `16`'s isolated checks after
any edit.

| Script | Does | Spends? |
|---|---|---|
| `metaops.py` | agent interface: workspace/assets/doctor/media/feed/catalog/business, hash-bound plan → apply PAUSED → verify → explicit single/bulk activate, then edit/clone/rules/review/monitor/comments/page/insights | activate, `edit … --confirm SPEND` |
| `probe.py` | internal doctor implementation: identity/scopes/account/PBIA/dataset/write gates | no spend |
| `media.py` | internal `metaops media` implementation | no spend |
| `launch.py` | spec → `validate_only` → create PAUSED; resume-safe state | no |
| `bulk.py` | internal bulk-plan/apply implementation | no |
| `verify.py` | read-back diff of every spec field; exit 0 writes `<state>.verified.json` | no |
| `activate.py` | internal single/bulk activation implementation; receipt required | **yes** |
| `cmd_edit.py` · `cmd_catalog.py` · `cmd_business.py` · `cmd_operate.py` | `metaops` command groups: edit/clone/rules · catalog/feed/set/products · BM accounts/pixel/CAPI/users/partners · review/monitor/comments/page/insights (`16`) | edit ACTIVE/budget only with `--confirm SPEND` |
| `edit.py` · `clone.py` · `rules.py` | internal implementations behind `metaops edit/clone/rules` | mutating |
| `monitor.py` | N-account status/spend sweep → verdicts incl. `STALL` (ad set ≥40 impr, 0 clicks), JSONL | no |
| `insights.py` | spend/delivery, explicit attribution window, CSV for tracker | no |
| `comments.py` | internal `metaops comments list/hide/delete` (Page token) | no spend |
| `mcp.py` | official Meta Ads MCP: tools, rollout diagnostics, allowlisted reads only; mutating tools are rejected in code | no |
| `mutate_set.py` | internal `metaops assets set-products` implementation | no spend |
| `sheetfeed.py` | edit/validate the Google-Sheet catalog via service account (`17`); Meta pulls it as a scheduled feed | no spend |
| `uniquify.py` · `page.py` | local creative variants (`--no-crop` keeps exact pixels for text/border banners) · internal `metaops page` | no spend |
| `feed_upload.py` | internal `metaops feed sync/swap`: `POST /{feed_id}/uploads` + poll | no spend |

Env: `META_TOKEN` (required), `GSHEETS_JSON_KEY_FILE` (sheetfeed only), `TG_BOT_TOKEN`+`TG_CHAT_ID` (`monitor --telegram`), `META_PROXY` or `META_ALLOW_NO_PROXY=1`, optional `META_APP_SECRET`
(adds `appsecret_proof`), `META_API_VERSION` (pinned `v26.0`). Never pass a token on argv.
