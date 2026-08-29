# Agent Skills

[![CI](https://github.com/sergeyizmailov/Claude-Skills/actions/workflows/ci.yml/badge.svg)](https://github.com/sergeyizmailov/Claude-Skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skills standard](https://img.shields.io/badge/Agent%20Skills-open%20standard-8A2BE2)](https://agentskills.io)

Reusable, verification-oriented skills for AI agents. Each skill is a focused, dense
workflow — written for the model, not as a tutorial — and can bundle references,
decision guides, or deterministic helper scripts.

They follow the open [`SKILL.md`](https://agentskills.io) format and work with Claude Code,
Codex, Cursor, Gemini CLI, GitHub Copilot, VS Code, opencode, and other compatible agents.

Skills are grouped into categories under [`skills/`](skills/). Add a new one in the fitting
category (or a new category); the tooling discovers any `skills/**/SKILL.md`.

## Catalog

### Skill router

[**skill-router**](skills/skill-router) is the entry point for this collection. It lives
directly under `skills/`, one level shallower than every other skill here, each of which is
nested inside a category folder. A runtime that doesn't discover skills two levels deep will
still find `skill-router` — read it first: it indexes the categories below and routes a task
to the right skill by name, without needing to be kept in sync with each skill's own detail.

### Media buying — Meta & Google

Eight skills covering Meta and Google ads together, layered by concern rather than by
platform: buy mechanics (`meta-ads`, `google-ads`), survival infrastructure (`meta-grey-ops`,
`google-grey-ops`), the retail data layer (`google-feed-ops`), counting (`tracker-ops`),
experiment validity (`measurement-experimentation-ops`), and portfolio orchestration
(`senior-buyer-ops`) sitting on top of all of them. The set cross-references itself by skill
name, so install it together — a single skill installed alone will point at files you don't
have.

| Skill | Purpose |
|---|---|
| [**meta-ads**](skills/media-buying/meta-ads) | Clean-marketing reference: plan, launch, audit, diagnose, and optimize Meta ads — objectives/ODAX, budgets & bidding, targeting, pixel/CAPI, policy, and a canonical Marketing API error catalog. |
| [**meta-grey-ops**](skills/media-buying/meta-grey-ops) | Infrastructure & survival layer for Meta grey verticals: antidetect/proxy/session survival, agency accounts, token death, API mass-launch, cloaking/review-layer filters, DLO/catalog/CTM/unicode tricks, verification gates (business/beneficial-owner/identity), and per-vertical playbooks (nutra, gambling, crypto, news). |
| [**google-ads**](skills/media-buying/google-ads) | Senior single-account layer for Google Ads: plan, launch, audit, diagnose, and scale across Search, PMax, Demand Gen, and Shopping, with AI Max, Smart Bidding, RSA, tCPA/tROAS, and OCI tracking wired in. |
| [**google-grey-ops**](skills/media-buying/google-grey-ops) | Infrastructure & survival layer for Google Ads grey verticals: agency/MCC account supply, identity/payment infra, AdsBot cloaking and review-layer filters, RSA/unicode/path tricks, selfie/BOV verification, geo isolation, enforcement tracks, and per-vertical playbooks (gambling, finance/crypto, nutra, dating, loans, apps). |
| [**google-feed-ops**](skills/media-buying/google-feed-ops) | The retail data layer: feed spec and attributes, the Merchant API, feed rules and supplemental feeds, title optimization, GTIN/`custom_label` schema, and diagnosing Merchant Center suspensions and free-listings eligibility. |
| [**tracker-ops**](skills/media-buying/tracker-ops) | Affiliate tracker operations across Keitaro and Binom APIs: postback/S2S wiring, payout-event-vs-all-conversions metric discipline, timezone and CPL math, the daily spend-sync, and Google's gclid → offline conversion import chain. |
| [**measurement-experimentation-ops**](skills/media-buying/measurement-experimentation-ops) | Decide whether a result is real before scaling it: testing-mode selection (causal / screening / infrastructure), validity traps (SRM, peeking, contamination, lag, multiple testing), and platform tools — Meta's A/B Test, `ad_study` API, Conversion Lift, GeoLift, Robyn, and Google's Experiments, Conversion Lift, and Meridian MMM. |
| [**senior-buyer-ops**](skills/media-buying/senior-buyer-ops) | Portfolio-orchestration layer for senior buyers and team leads across Meta and Google: the day-1 operating contract, cross-platform allocation (test/scale/reserve), kill/watch/scale plus marginal scaling, the creative-intelligence pipeline, and end-to-end funnel QA — routes into the seven skills above by name. |

### Frontend

| Skill | Purpose |
|---|---|
| [**responsive-adapter**](skills/frontend/responsive-adapter) | Adapts existing web interfaces from 320px phones to 2560px+ displays while preserving the original visual system, then verifies across a device matrix. |
| [**design-stack-picker**](skills/frontend/design-stack-picker) | Selects compatible fonts, icons, components, imagery, motion, and design primitives with a reuse-first approach. |
| [**normcore-web**](skills/frontend/normcore-web) | Builds sites that read as ordinary, long-running commercial web rather than freshly art-directed product design, across five genre archetypes with measured tokens and a runnable audit. |

### Security

| Skill | Purpose |
|---|---|
| [**secure-coding**](skills/security/secure-coding) | Secure defaults and review guidance for JavaScript, Node.js, HTML, CSS, APIs, authentication, databases, uploads, GraphQL, and AI-assisted code. |
| [**js-obfuscation**](skills/security/js-obfuscation) | JavaScript protection, obfuscation, anti-automation, and anti-debugging techniques for authorized testing and software protection. |

### Engineering

| Skill | Purpose |
|---|---|
| [**knowledge-delta-skill-architect**](skills/engineering/knowledge-delta-skill-architect) | Writes, audits, and compresses agent skills so they earn their tokens: baseline what the model already does, keep only the delta, and package it for progressive disclosure. |

### Research

| Skill | Purpose |
|---|---|
| [**deep-research**](skills/research/deep-research) | Traceable multi-source research with primary-source prioritization, verification, confidence labels, and explicit knowledge gaps. |
| [**web-scraping**](skills/research/web-scraping) | Mass crawling and scraping past anti-bot defenses (Cloudflare, Akamai, DataDome, PerimeterX): Crawl4AI for scale (`arun_many`, dispatchers, deep crawl, LLM-ready markdown) and Camoufox for fingerprint evasion. |

## Install

Clone the collection:

```bash
git clone https://github.com/sergeyizmailov/Claude-Skills.git
```

Install one skill (copy the skill directory itself, not its category):

```bash
mkdir -p ~/.claude/skills
cp -R Claude-Skills/skills/media-buying/meta-ads ~/.claude/skills/
cp -R Claude-Skills/skills/security/secure-coding ~/.claude/skills/
```

Or keep the categories and install everything:

```bash
cp -R Claude-Skills/skills/* ~/.claude/skills/
```

Agents discover skills recursively, so category subfolders are fine. For Codex, copy into
`~/.codex/skills/` instead; other agents may use a different skills directory.

## Structure

```text
skills/<category>/<name>/
├── SKILL.md        # required — frontmatter (name, description) + the workflow
├── agents/         # optional — agent-facing metadata
├── references/     # optional — on-demand docs, loaded only when needed
└── scripts/        # optional — deterministic helpers
```

Only `name` and `description` load for discovery; the body and supporting files load when the
skill is selected. The media-buying skills also cross-reference each other by name (e.g.
`senior-buyer-ops` routes into `meta-ads` / `meta-grey-ops` / `google-ads` / `google-grey-ops` /
`google-feed-ops` / `tracker-ops` / `measurement-experimentation-ops`).

## Contributing

Improvements and new skills are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
format, quality bar, and local checks.

## License

[MIT](LICENSE)
