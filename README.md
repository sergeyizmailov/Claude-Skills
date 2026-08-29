# knowledge-delta-skills

[![CI](https://github.com/sergeyizmailov/knowledge-delta-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/sergeyizmailov/knowledge-delta-skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skills standard](https://img.shields.io/badge/Agent%20Skills-open%20standard-8A2BE2)](https://agentskills.io)

**Not knowledge for beginners. Missing expertise for already-capable AI.**

Frontier models already know the docs, the frameworks, and the textbook best practice
for most domains. What they don't reliably know is the rest: the platform quirk that
never made it into a changelog, the threshold that only shows up after you've been
burned by it once, the failure mode a postmortem describes and a tutorial never
mentions. That gap — the **knowledge delta** — is what each skill here is built to
close, and only that.

## This is not

- A tutorial, onboarding guide, or "learn X" walkthrough.
- A summary or reformatting of a vendor's official documentation.
- A beginner's guide — every skill assumes a competent model and a competent operator.
- A generic best-practices checklist restated in Markdown.

## Three examples

Quoted verbatim, with the file they live in. None of these are things a competent
outsider — or a general-purpose model with no domain-specific skill loaded — would
reliably know or check for.

> iOS 18 does NOT update `window.innerHeight` when address bar expands; `100vh` always
> equals `lvh` on iOS Safari.

— [`skills/responsive-adapter/references/platform-quirks.md`](skills/responsive-adapter/references/platform-quirks.md)

> Defense: resolve DNS, check IP, disable redirects, re-check on every socket connect.
> Production: dedicated egress proxy (Smokescreen, ssrfproxy) with connect-time IP
> validation — application-layer checks are racy.

— [`skills/secure-coding/ssrf.md`](skills/secure-coding/ssrf.md)

> Daily CPL (for BUYING) = click-date spend (account-tz day) ÷ that same click-date
> cohort's payout count. ... pairing click-date spend with conversion-date conversions
> is the classic apples-to-oranges CPL.

— [`skills/tracker-ops/references/03-metrics-and-math.md`](skills/tracker-ops/references/03-metrics-and-math.md)

## How these are built

Baseline → gap discovery → research → validation → contradiction review → compression
→ skill. In short: run the real tasks with no skill, record what the model gets wrong
or skips, research only the confirmed gaps plus one bounded pass for unknown unknowns,
keep only rules that trace back to a prevented failure, compress hard, then rerun the
same tasks against the draft and cut anything that didn't fix what it was written for.
On broad domains, independent research and a separate contradiction-hunting pass are
used before anything is merged in.

There is no separate "eval" stage — the rerun against the original tasks *is* the
check. **No skill here has a published, measured base-model-vs-base+skill score**;
nothing in this repo should be read as a benchmark result. Full method, what gets cut,
and how volatile facts are dated: [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).

## Catalog

16 skills. Every skill folder sits directly under `skills/` — there are no category
subfolders on disk; the grouping below is this catalog's, for browsing.

### Media buying — Meta & Google

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

### Frontend

| Skill | Adds |
|---|---|
| [**responsive-adapter**](skills/responsive-adapter) | Adapts an existing web interface from 320px to 2560px+ without touching the visual design, then verifies across a device matrix. |
| [**design-stack-picker**](skills/design-stack-picker) | Picks compatible fonts, icons, components, imagery, and motion for a UI build with a reuse-first approach. |
| [**normcore-web**](skills/normcore-web) | Builds sites that read as ordinary long-running commercial web instead of freshly art-directed product design, across five genre archetypes. |

### Security

| Skill | Adds |
|---|---|
| [**secure-coding**](skills/secure-coding) | Applies secure defaults across JS/Node/HTML/API/auth/DB/upload code paths and flags AI-generated-code vulnerability patterns. |
| [**js-obfuscation**](skills/js-obfuscation) | Obfuscates JavaScript and adds anti-automation/anti-debugging layers for authorized testing and software protection. |

### Research

| Skill | Adds |
|---|---|
| [**deep-research**](skills/deep-research) | Runs traceable multi-source research with primary-source prioritization, verification, and explicit confidence labels. |
| [**web-scraping**](skills/web-scraping) | Crawls and scrapes at scale past anti-bot defenses (Cloudflare, Akamai, DataDome, PerimeterX) using Crawl4AI and Camoufox. |

### Engineering

| Skill | Adds |
|---|---|
| [**knowledge-delta-skill-architect**](skills/knowledge-delta-skill-architect) | Writes, audits, and compresses agent skills against the baseline-then-cut methodology this collection follows — see [Methodology](docs/METHODOLOGY.md). |

## Install

Copy the skill directories you want into your runtime's skills folder. There's nothing
else to configure.

```bash
git clone https://github.com/sergeyizmailov/knowledge-delta-skills.git
```

One skill:

```bash
mkdir -p ~/.claude/skills
cp -R knowledge-delta-skills/skills/meta-ads ~/.claude/skills/
```

Everything:

```bash
cp -R knowledge-delta-skills/skills/* ~/.claude/skills/
```

Skills folder by runtime, personal/global scope, verified against each vendor's docs
on 2026-08-29. Most also read a project-local equivalent, and several read each other's
directories for compatibility — check the runtime's own docs for the current list:

| Runtime | Skills directory |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Codex CLI | `~/.agents/skills/` |
| Cursor | `~/.cursor/skills/` (also reads `~/.agents/skills/`) |
| Gemini CLI | `~/.gemini/skills/` (alias `~/.agents/skills/`) |
| opencode | `~/.config/opencode/skills/` (also reads `~/.claude/skills/`) |

The eight media-buying skills reference each other by name; keep them together if you
install any one of them.

## Redundancy and retirement

Base models absorb more of the public internet every release. A skill earns its place
only while there's a real gap between what the model already knows and what a task
needs — once that gap closes, the skill isn't neutral, it's the exact kind of
topically-adjacent-but-useless content that degrades reasoning instead of helping it.

This collection doesn't promise permanence. Volatile-domain skills carry a date; when a
skill is re-baselined and a section turns out to already be handled correctly by a
current model, that section gets cut — the same rule applied at first-write time. Some
skills here will shrink over time, and some are expected to be retired outright once
their delta closes. See [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) for how that
review happens.

## Structure

```text
skills/<name>/
├── SKILL.md        # required — frontmatter (name, description) + the workflow
├── agents/         # optional — agent-facing metadata
├── references/     # optional — on-demand docs, loaded only when needed
└── scripts/        # optional — deterministic helper scripts
```

Only `name` and `description` load for discovery; the body and supporting files load
only once a skill is selected.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the quality bar, the anatomy of a skill, and
the local checks CI runs.

## License

[MIT](LICENSE)
