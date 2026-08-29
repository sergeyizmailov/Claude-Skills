# Catalog

All 16 skills, grouped by domain. Every skill folder sits directly under `skills/` —
there are no category subfolders on disk, so a single `cp` installs any of them. The
grouping below is for browsing.

## Media buying — Meta & Google

Layered by concern, not by platform: buy mechanics (`meta-ads`, `google-ads`), survival
infrastructure (`meta-grey-ops`, `google-grey-ops`), the retail data layer
(`google-feed-ops`), counting (`tracker-ops`), experiment validity
(`measurement-experimentation-ops`), and portfolio orchestration (`senior-buyer-ops`)
sitting on top. These eight cross-reference each other by skill name — install the set
together, not a single one in isolation.

| Skill | Adds |
|---|---|
| [**meta-ads**](skills/meta-ads) | Plans, launches, audits, and diagnoses Meta ad accounts — ODAX objectives, budgets/bidding, targeting, pixel/CAPI, policy, and a Marketing API error catalog. |
| [**meta-grey-ops**](skills/meta-grey-ops) | Infrastructure and survival tactics for Meta grey-vertical buying: antidetect/proxy setups, agency accounts, token-death recovery, API mass-launch, cloaking/review-layer filters, verification gates, per-vertical playbooks. |
| [**google-ads**](skills/google-ads) | Plans, launches, audits, and scales a single Google Ads account across Search, PMax, Demand Gen, and Shopping, with AI Max, Smart Bidding, RSA, and OCI tracking. |
| [**google-grey-ops**](skills/google-grey-ops) | Infrastructure and survival tactics for Google Ads grey-vertical buying: MCC account supply, identity/payment infra, AdsBot cloaking, verification gates, geo isolation, per-vertical playbooks. |
| [**google-feed-ops**](skills/google-feed-ops) | Runs the retail data layer for Shopping: feed spec, Merchant API, feed rules, GTIN/`custom_label` schema, and diagnosing Merchant Center suspensions. |
| [**tracker-ops**](skills/tracker-ops) | Operates affiliate trackers (Keitaro, Binom): postback/S2S wiring, payout-vs-all-conversions metric discipline, timezone/CPL math, daily spend-sync, and the gclid-to-offline-conversion chain. |
| [**measurement-experimentation-ops**](skills/measurement-experimentation-ops) | Decides whether a media-buying result is real before scaling it: test-mode selection, validity traps (SRM, peeking, contamination), and the platforms' own measurement tools. |
| [**senior-buyer-ops**](skills/senior-buyer-ops) | Orchestrates a portfolio across Meta and Google: day-1 operating contract, budget allocation, kill/watch/scale rules, creative-intelligence pipeline, funnel QA. |

## Frontend

| Skill | Adds |
|---|---|
| [**responsive-adapter**](skills/responsive-adapter) | Adapts an existing web interface from 320px to 2560px+ without touching the visual design, then verifies across a device matrix. |
| [**design-stack-picker**](skills/design-stack-picker) | Picks compatible fonts, icons, components, imagery, and motion for a UI build with a reuse-first approach. |
| [**normcore-web**](skills/normcore-web) | Builds sites that read as ordinary long-running commercial web instead of freshly art-directed product design, across five genre archetypes. |

## Security

| Skill | Adds |
|---|---|
| [**secure-coding**](skills/secure-coding) | Applies secure defaults across JS/Node/HTML/API/auth/DB/upload code paths and flags AI-generated-code vulnerability patterns. |
| [**js-obfuscation**](skills/js-obfuscation) | Obfuscates JavaScript and adds anti-automation/anti-debugging layers for authorized testing and software protection. |

## Research

| Skill | Adds |
|---|---|
| [**deep-research**](skills/deep-research) | Runs traceable multi-source research with primary-source prioritization, verification, and explicit confidence labels. |
| [**web-scraping**](skills/web-scraping) | Crawls and scrapes at scale past anti-bot defenses (Cloudflare, Akamai, DataDome, PerimeterX) using Crawl4AI and Camoufox. |

## Engineering

| Skill | Adds |
|---|---|
| [**knowledge-delta-skill-architect**](skills/knowledge-delta-skill-architect) | Writes, audits, and compresses agent skills against the baseline-then-cut methodology this collection follows — see [Methodology](docs/METHODOLOGY.md). |
