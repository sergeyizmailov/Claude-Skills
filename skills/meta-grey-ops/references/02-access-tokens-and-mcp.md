# 02 — Access: app, scopes, tokens, MCP vs API vs CLI

Reviewed 2026-09-02 against developers.facebook.com (permissions, system-users,
ads-ai-connectors), 2026-05-04 access-tier post, claude-code #57191/#62376. API **v26.0**
(2026-07-29); pin `/v26.0/` in every call — unversioned calls rejected, a version lives ~2yr
after its successor ships (v24→2028-02-18, v25→2028-07-29).

Owner of every access fact in paid-media. `meta-ads/13` keeps clean-lane governance, points
here for mechanics.

## 0. Which pipe

| Pipe | What | Use for | Not for |
|---|---|---|---|
| **Marketing API via `metaops`** (internal `scripts/`) | Workspace-bound Graph calls, System User or long-lived user token | **every agent launch and write.** Only surface with confirmed control of `attribution_spec`, `degrees_of_freedom_spec`, `contextual_multi_ads`, `asset_feed_spec`, catalog/template creatives, `validate_only`, batching | direct low-level script writes — internal implementation only |
| **Meta Ads MCP** (`mcp.facebook.com/ads`) | Meta-hosted, 106 tools (live 2026-09-02), bearer System User token w/ `ads_mcp_management` or OAuth; per-account rollout flag | conversational reads: insights, anomaly/benchmarks, entity search, previews, catalog/pixel diagnostics, Ad Library; bounded edits (`ads_update_entity`) | launches: no `contextual_multi_ads` (inherits OPT_IN), defaults push 7d-click/CBO/Advantage+, no `validate_only`, no batch, one account/call, `ads_get_ad_entities` can't read `attribution_spec` back — §6 |
| **Meta Ads CLI** (`pip install meta-ads`, `12`) | click CLI over `facebook-business` SDK, System User token via `ACCESS_TOKEN` | human-operator inspection and diagnosis | **all agent writes** — it has no workspace binding or spend-confirmation gates; also no `validate_only`, multi-account run, resume state, read-back diff, currency guard, or proxy setting; SDK video host deprecated (#701) |
| Third-party Meta MCP servers (pipeboard, hashcott, brijr, ScaleForge…) | community wrappers | nothing here | shared dev apps + raw tokens + unsupervised writes = reported ban mechanism [practitioner-multiple, no Meta statement]; never hand a work token to one |
| CSV bulk import | Ads Manager | human review of thousands of rows | agents: no validate_only; blocked on fresh accounts (3738001) |

Rule: **agent writes → workspace-bound `metaops` API.** The official CLI (`12`) is an
operator reference/diagnostic tool, never an agent write path. MCP is read/analysis only,
parameter coverage unproven; every skill-critical default
(SKILL.md § Launch defaults) enforceable only via `launch.py`. If forced through MCP: build
PAUSED, read every ad set/creative back through API (`verify.py --state` accepts hand-written
state files) before activation.

## 1. Operator handoff checklist (once, BM owner)

Agent needs **one token + ids**; rest is BM owner's setup:

1. **Developer app** (Business type), only golden use cases (extra invite audits): `Create &
   manage ads with Marketing API` · `Measure ad performance data with Marketing API` ·
   `Manage everything on your Page` · `Manage products with Catalog API` · `Create & manage
   ads with ads MCP server` (only if MCP reads wanted). App **Live** (Privacy Policy URL 200)
   — dev mode blocks creative create (1885183).
2. **Admin System User** for agent provisioning — do not choose Employee when the agent must
   create a catalog, dataset/pixel, claim an asset, or assign an asset elsewhere in this Business
   Portfolio. Assign **Full control**: every ad account, Page, IG account, pixel/dataset,
   catalog, and the app. Per-asset — portfolio membership assigns nothing. An Employee System
   User is suitable only for a least-privilege agent operating assets that a BM admin has already
   assigned in the UI; see §2.
3. **Generate token**, expiry Never (60-day option exists; Never is System User default),
   scopes below. Store once, gitignored.
4. **Pixel attached to every ad account** (Datasets → Add assets → ad account). Shared-to-BM
   ≠ attached; fails 1815045 (`probe.py` checks).
5. Page: System User (or app) needs ≥ADVERTISER per Page — PBIA edge needs Page token from
   that role.
6. EU geo: `default_dsa_beneficiary`/`default_dsa_payor` on account, or DSA fields per spec
   (`04`).
7. Recommended: **Require App Secret**, hand agent `META_APP_SECRET` — signs every call with
   `appsecret_proof`, leaked token useless elsewhere.

```
META_TOKEN=<system user token>      META_APP_SECRET=<optional>
ad accounts: act_..., act_...        pages: ...   pixel/dataset: ...   catalog: ...
currency/tz per account: USD / America/Los_Angeles ...
tracker campaign URL + macro mapping: ...
```

Agent's first command is `metaops --workspace . --profile <name> --json doctor --whoami`
(runbook step 1). Nothing else until exit 0.

## 2. System User roles: Admin vs Employee

The token's OAuth scopes and the System User's Business Portfolio role are separate gates. Giving
an Employee token `catalog_management` and `business_management` does **not** turn it into a BM
admin.

| System User role | Can do | Cannot do |
|---|---|---|
| **Employee** | Operate only the ad accounts, existing catalogs, Pages, and other assets explicitly assigned to that System User in Business Settings. It is a valid least-privilege choice for an agent that only launches into preassigned accounts or maintains a preassigned catalog. | Provision or reassign Business-Portfolio-owned assets: creating a catalog or dataset/pixel, claiming assets, or assigning assets to other entities. In particular, `POST /{business_id}/owned_product_catalogs` fails before scopes help. |
| **Admin** | In addition to assigned-asset operations, provision and administer BM-owned catalogs, datasets/pixels, and asset assignments. | It still needs the relevant app scopes, asset access, and API access tier; Admin is not a substitute for those gates. |

**[R, reported 2026-09-03] Catalog-creation trap:** an Employee System User calling
`POST /{business_id}/owned_product_catalogs` can receive `OAuthException` code **10**, subcode
**1690129**, even when `catalog_management` and `business_management` are granted. The reported
English text is equivalent to “You do not have permission to create a catalog because you are not
an admin of this business”; Meta localises error text, so branch on code/subcode rather than that
string. Revalidate this result against the intended BM before relying on it. Use an **Admin System
User** for any agent workflow that must autonomously create or assign BM-level assets. Do not
over-privilege an agent that only operates already assigned assets.

## 3. Scopes

Request only these; verify **granted** via `GET /me/permissions` (use-case bundling grants
extras — `facebook_branded_content_ads_brand`, `threads_business_basic`; requested ≠ granted).

| Scope | Why | Required |
|---|---|---|
| `ads_management` | create/update campaigns/ad sets/ads/creatives | yes |
| `ads_read` | reads + Insights + CAPI send (distinct permission) | yes |
| `business_management` | BM assets, System User mgmt, catalog dependency | recommended |
| `read_insights` | Page/app insights | recommended |
| `pages_manage_ads` | Page-backed ads, click-to-message (PBIA) | recommended |
| `pages_read_engagement`, `pages_show_list` | Page identity reads (dependencies) | recommended |
| `pages_manage_metadata`, `pages_manage_posts` | Page avatar/metadata edits (#283 without), posts | if job edits Pages |
| `instagram_basic` | IG professional identity reads | if real IG account used |
| `catalog_management` | product sets, feed swaps — granted on Business-type Live apps for own-BM catalogs without review (2026-08-30) | catalog launches |
| `leads_retrieval` | lead-form data; needs Full access tier | lead forms only |
| `ads_mcp_management` | MCP server scope | MCP pipe only |

Own-business assets: Limited tier + these scopes suffice. Other businesses' assets: Full tier —
App Review with screencasts. Permission docs redirect to one consolidated
`developers.facebook.com/docs/permissions` page.

## 4. Access tier (renamed 2026-05-04)

"Ads Management Standard Access"→**Marketing API Access Tier**; Standard→**Limited**,
Advanced→**Full**. Full is automatic after **≥500 calls in 15 days, <15% errors over last
500** — but only via App Review upgrade (Marketing API → Ads Management Standard Access);
Business Verification is a prerequisite, app's Privacy Policy URL checked there [doc-confirmed
2026-09-02: marketing-api/overview/rate-limiting, development/release/business-verification].
Tier is a property of the **app**, not the BM — a verified agency BM doesn't lift your app.
Read `ads_api_access_tier` in `X-Business-Use-Case-Usage` header (`meta-ads/14` rate limits).

## 5. Token types and lifecycle

| Token | Lives | Dies when | Proxy rule |
|---|---|---|---|
| **System User** (preferred) | until revoked ("Never") or 60d if chosen | admin revokes, app secret rotated w/ proof enforced, System User removed | use the BM/operator's assigned egress; `META_ALLOW_NO_PROXY=1` only when direct current-IP access is intentional |
| Long-lived user (~60d) | 60 days | **login session dies** — logout, password change, security rotation, multi-session flag; 60-day doesn't save it | must exit antidetect profile's IP (`01`) |
| Short user (Explorer) | ~1–2h | expiry | exchange immediately |
| Page token | derived per call | parent token dies | same as parent |
| Events Manager "Generate access token" | CAPI dataset only | — | **not an ads token; never launch with it**. Reverse works: System User token w/ Full control on dataset POSTs to `/{dataset_id}/events` |

### [W] User token — end-to-end (when System User token unavailable)

Two objects both look like `EAA…` — do not confuse them:

| Source | Lifetime | Exchangeable | appsecret_proof | Use |
|---|---|---|---|---|
| **EAAB… scraped from Ads Manager session** (autolaunch-SaaS style, `13`) | until persona logs out / password change / checkpoint | **no** — app is Meta's own | no | works with every script; treat as persona's session, NOT a 1-2h token |
| **User token from YOUR developer app** (Explorer or FB Login) | short 1–2h → long-lived 60d | yes, with that app's id+secret | yes | preferred user-token path |

Runnable path for row 2, inside persona's antidetect profile (same exit IP as `META_PROXY`):
1. developers.facebook.com → Graph API Explorer → *Meta App* = operator's app (§1's app;
   Explorer's default app can't be exchanged) → *User or Page* = User token → tick
   `ads_management, ads_read, business_management, pages_show_list,
   pages_read_engagement, pages_manage_ads, instagram_basic, catalog_management` (+
   `ads_mcp_management` if MCP reads wanted) → Generate Access Token → persona logs in/approves.
   Missing permission on dialog = app lacks that use case (§1.1).
2. Exchange (from launch box, token never on command line):
   ```bash
   curl -s -G https://graph.facebook.com/v26.0/oauth/access_token \
     --data-urlencode grant_type=fb_exchange_token --data-urlencode client_id=$APP_ID \
     --data-urlencode client_secret=$APP_SECRET --data-urlencode fb_exchange_token=$SHORT
   ```
   400 = wrong app (token minted under another app), or app in dev mode w/ persona not
   tester/admin.
3. Export `META_TOKEN=<long-lived>` and, when required, `META_PROXY=socks5h://…`; then run
   `metaops --workspace . --profile <name> --json doctor --whoami`
   — expects `type=USER`, `expires_at` ~60d out, prints proxy/lifetime verdict.
4. Store token + expiry; re-mint before day 55. 190/460–467 anywhere = dead, no revive.

User token can't do anything a System User can't in the Marketing API — sees whatever the
human sees, incl. client accounts never shared to a BM. Cost: every call is persona's session
(`01` proxy discipline applies to API too); one checkpoint kills automation mid-batch (state
files make resume safe).

**Inspect:** `GET /debug_token?input_token=<token>`, caller = System User token itself (live
2026-09-02): `type: SYSTEM_USER`, `application`, `expires_at: 0`=never, `data_access_expires_at`,
granted scopes. `probe.py` runs this as gate 2.

**[K] Death codes (190 subcodes):** 460 session invalidated (password/security rotation), 463
expired, 467 invalid ("user logged out" wording still emitted). Dead tokens never revive — mint
- exchange once, then **freeze** if recurring (`01`, `05`). "Malformed access token" = copy
damage.

**[W] Access denials** are code 10/200 (missing capability or asset not assigned), not 100
(100 = invalid parameter). GET succeeding proves nothing about writes — `probe.py` runs a
`validate_only` create.

### Token transport (scripts)

`graph.py` sends token as `Authorization: Bearer <token>`, never `access_token=` in URL
(query strings land in proxy/access logs, exception text). `appsecret_proof` (when
`META_APP_SECRET` set) stays a query param — a hash, not the secret. `graph.redact()` scrubs
token+proxy creds from anything printed/written.

## 6. Meta Ads MCP — live-verified 2026-09-02 (own BM, System User token)

- Endpoint `https://mcp.facebook.com/ads`, Streamable HTTP. `initialize` returns
  `Mcp-Session-Id`, send back every call. Errors: JSON-RPC `result.isError=true` w/
  `error_code`/`error_subcode` (Graph codes); messages **localised to System User's locale**
  (got Polish) — branch on codes (meta-ads/14 rule).
- **Auth:** `Authorization: Bearer <System User token>` w/ `ads_mcp_management` scope.
  Prerequisite: app has use case `Create & manage ads with ads MCP server` — only then does
  token generator offer that scope. Same token/BM without scope → HTTP 401 "restricted to
  certain users" on `initialize`. Claude Code OAuth: `claude mcp add --transport http
  --client-id <META_APP_ID> meta-ads https://mcp.facebook.com/ads` (without `--client-id`:
  "redirect_uris are not registered", #57191). Bearer needs no OAuth.
- **Per-account rollout flag** `is_ads_mcp_enabled`, via `ads_get_ad_accounts` (also
  `is_queryable`, `has_payment_method`, `min_daily_budget_cents`,
  `is_ads_mcp_disabled_reason`). Own account: enabled. Client/agency accounts: `false`,
  "gradually being rolled out" — nothing to click, wait.
- **106 tools** (`tools/list`; Meta's docs show ~29). Groups: ads CRUD+activate, creatives (7
  formats incl. single-video, static carousel, Advantage+ catalog carousel, boost post,
  partnership ads; `ads_creative_upload_media` by URL/device), custom audiences, catalog
  (~40 tools), datasets/pixel event rules, experiments (A/B, lift), insights/anomaly/benchmark,
  Ad Library, help articles, opportunity score.
- **Parameters confirmed present** on write tools: `ads_create_ad_set.attribution_spec` (JSON
  string), `dsa_beneficiary/payor`, `is_dynamic_creative`, `promoted_object`,
  `bid_strategy/bid_amount`, spend caps, budget schedule; `ads_create_creative
  .degrees_of_freedom_spec` (JSON **string**, per-feature OPT_OUT — our 83-key list accepted,
  read back all OPT_OUT), `instagram_user_id`, `product_set_id`, `cards`,
  `placement_videos`; `ads_create_ad.tracking_specs`, `conversion_domain`. Campaign:
  budget/bid/spend_cap/promoted_object.
- **[K] Missing — why MCP is not the launch pipe:** no `contextual_multi_ads` in any of 106
  schemas → creative made through MCP inherits account default **OPT_IN** (multi-advertiser
  ON; reads back `contextual_multi_ads: null`). No `validate_only`, no batch, no proxy, one
  account/call, no read-back diff; `ads_get_ad_entities` can't return `attribution_spec`
  ("Unsupported fields") — verify through Graph instead. Tool prompts steer toward Meta
  defaults: "omit attribution_spec … Default: 7-day click + 1-day view", "ALWAYS use CBO",
  "Advantage+ Audience enabled by default", "suggest opportunity score".
- Verified writes (all PAUSED, then deleted): campaign (CBO, `daily_budget` cents) → ad set
  (explicit `targeting_automation.advantage_audience: 0` kept; `attribution_spec` honoured) →
  creative (all features OPT_OUT) → ad; `ads_update_entity` rename+budget (returns
  `updated_fields`, `active_errors` on draft); `ads_activate_entity` **not** run.
- **[W] Live trap** (Graph rule, surfaced via MCP): `attribution_spec` 1/1/1 on a
  **LINK_CLICKS** ad set → 100/1885501 "supported combination … is (1, 0)": non-conversion
  optimization goals accept 1d click only. `launch.py` sends click-only for those goals when
  spec is silent (`CLICK_ONLY_ATTRIBUTION_GOALS`).
- Governance: Business Settings → Integrations → Ads MCP Server (7 actions, all allowed by
  default; `…/ads_mcp_rules` Graph edge unreachable from our BM).
- **[W] Verified failure via MCP** (#62376): agent set **TWD** budget in "cents" → 100x
  overspend. Direct-API scripts carry the currency guard; MCP has `min_daily_budget_cents` but
  no offset guard.

## 7. Ad account facts scripts read for you

`currency`+`timezone_name` (`probe.py`, `launch.py`) — changing either **closes** account,
opens new act id (`08`). `account_status` 1 active / 2 disabled / 3 unsettled (unpaid, not a
ban) / 7 pending risk review / 9 grace period / 100–101 closing — undocumented enum, never
diagnose from it alone. Rate limits BUC, header-driven (`meta-ads/14`); single buyer never
approaches them — just don't poll in tight loops.
