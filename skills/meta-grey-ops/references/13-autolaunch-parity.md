# 13 — Autolaunch SaaS parity: what they do, how, and where it lives here

Reviewed 2026-09-02. Sources: vendor sites (cloud.dolphin.tech, cabinet.partners, fbtool.pro),
RU review aggregators (cpa.rip, traffnews, greyhunter, partnerkin, cpa.club), one working
practitioner script (dvygolov gists / YWB.FBLogin). No vendor publishes mechanics; "how" below
is reconstructed and labelled.

## Mechanism

Dolphin Cloud, FBTool, Nooklz, Saint.tools, cabinet.partners are **Graph API wrappers with a
dashboard**. "Autolaunch" = (1) a **user token scraped from the Ads Manager browser session**
(`EAAB…`, regex on `accessToken="` in adsmanager HTML, or minted from `c_user`/`xs` cookies) —
no developer app or BM admin needed — plus (2) a form UI looping the same create calls over N
accounts. Everything marketed as a feature is a documented endpoint already in `scripts/`,
minus a few UI-only actions (end of feature map). [practitioner + source-code:
dvygolov/YWB.FBLogin, cpa.rip token guide, fbtool.pro FAQ "import cookies/access_token";
inferred for cabinet.partners, which discloses nothing]

Why we differ: System User token from your own BM is session-independent, scoped, revocable,
survives persona logout (`02`). Scraped EAAB token is the persona's session — every death code
in `02` §4 applies, carries every permission the human has, un-scopeable. Ban correlation by
pipe mechanism: **unquantified anywhere** [not found]; practitioner consensus blames account
quality/spend velocity, not the pipe.

## Feature map

| SaaS feature (Dolphin / FBTool / cabinet.partners) | Ours | API |
|---|---|---|
| Import accounts by cookies / token | operator hands System User token + ids (`02` §1) | — |
| Template → N accounts | `metaops bulk-plan` → `bulk-apply` (template × accounts, bound inputs, PAUSED) | `POST /act_X/campaigns\|adsets\|adcreatives\|ads` |
| Creative "uniquification" | `uniquify.py` (`--no-crop` for text-heavy banners) locally, then workspace-bound `metaops media` per account | client-side; `POST /adimages`, `/advideos` |
| Catalog/feed/product-set create, batch upsert/delete, instant fetch | `metaops catalog create\|feed create\|set create\|products batch`, `metaops feed sync\|swap` (`16`, `17`) | `POST /{business}/owned_product_catalogs`, `/{catalog}/product_feeds`, `/{catalog}/product_sets`, `/{catalog}/items_batch`, `/{feed}/uploads` |
| Distribution "All→All" / "1→1" | spec shape: ads per ad set in template; per-account `media` block | — |
| Duplicate campaign/ad set ×N | `metaops clone campaign\|adset\|ad <id> --times N` (level by level, PAUSED; `deep_copy` capped at <3 objects) | `POST /{id}/copies` |
| Scheduled launch / dead-hours avoidance | spec `start_time`; `metaops activate --refresh-start`; `04` → Scheduling | `start_time` |
| Autorules (kill/scale/notify) | `metaops rules ladder/list/history/execute/delete` (Poisson ladder, `--confirm RULES` for pause mode) | `POST /act_X/adrules_library`, `/{rule}/execute`, `/adrules_history` |
| Budget ramp / mass status | `metaops edit status/budget/rename/ramp` (±20% + late-day guard, `--confirm SPEND`) | `POST /{id}` |
| Comment auto-hide by trigger words | `metaops comments hide\|delete --matching REGEX --confirm HIDE\|DELETE` (Page token) | `GET /{post}/comments`, `POST /{comment}?is_hidden=true` |
| Spend/status/ban dashboard, Telegram alerts | `metaops monitor --telegram` (verdicts incl. STALL, JSONL, Bot API via `TG_BOT_TOKEN`/`TG_CHAT_ID`) | `GET /act_X?fields=account_status…`, `/insights`, `/ads?fields=effective_status` |
| Rejected-ad review + appeal | `metaops review [--previews]` (ad_review_feedback, issues_info); **appeal is UI-only** | `issues_info` read only |
| Pixel attach to account | `metaops business pixel create/share/shared`, `metaops doctor --attach-pixel`; `business capi test` proves the dataset receives events | `POST /act_X/adspixels`, `POST /{pixel}/shared_accounts` |
| Page avatar/cover/about writes | `metaops page set --avatar/--cover/--about/--website --confirm PAGE`. **Create+rename: UI-only** | `POST /{page}/picture`, `/{page}` |
| Card binding, auto-topup, balance payment | **UI-only** — no billing writes in Marketing API. Agency crypto topup or persona's browser (`03`) | — |
| BM creation, new ad account under BM | BM: UI-only. Ad account: `metaops business adaccount create` (new-BM cap = 1 account, `03`); users/partners: `business user invite\|assign`, `partner share` | partial |
| Tracker cost push (Keitaro/Binom) | `insights.py --csv` → `tracker-ops/01 update_costs` | `/insights` |
| Per-creative stats every 15 min, cross-account | `metaops insights leaderboard --accounts …` (join on `ad_name` = creative name, `03`); `insights pull --csv` → tracker | `/insights` |
| Team seats/roles | `metaops business user invite --role EMPLOYEE\|ADMIN` | — |
| "AI assistant over your data" (cabinet.partners) | this skill + `insights.py` output | — |
| 2FA/checkpoint handling, warm-up | not an API concept — `01` freeze protocol, antidetect profile | — |

## Their defaults vs ours

No vendor documents attribution/Advantage+/multi-advertiser defaults [not found]; payloads
omit the fields, so Meta's defaults apply: **7d click, every enhancement ON, multi-advertiser
ON**. Quiet reason "same creative performs differently from the tool" — ours pins 1/1/1, all
OPT_OUT (`SKILL.md` § Launch defaults).

## Volume/hygiene practices (practitioner, cpa.rip/partnerkin)

- Caps: ~200 launches/creatives per day per tool tier; >50 launches/day called unmanageable
  even automated. `bulk.py` has no cap — TL sets one.
- One proxy per account from antidetect layer; no vendor publishes inter-call delays [not
  found]. `graph.py` backs off on BUC headers; don't sprint `bulk.py` with hundreds of accounts
  on one persona IP — split by persona.
- Warm-up (browsing, small spend before real budgets) is RPA/antidetect territory, not the
  launcher's; `04` → Spend warm-up.

## Open items

- IG comment moderation (`/{ig_media_id}/comments`, `is_hidden`) — add to `comments.py` when a
  funnel needs it.
- Appeal submission, card binding, BM/Page creation stay in the antidetect profile.
- Whether any vendor uses its own developer app rather than scraped tokens: unknown for all.
