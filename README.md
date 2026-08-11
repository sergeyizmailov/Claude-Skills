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

### Media buying — Meta (Facebook/Instagram)

A connected set for running Meta ads across clean and grey verticals: three domain
adapters plus one orchestrator that decides between them.

| Skill | Purpose |
|---|---|
| [**meta-ads**](skills/media-buying/meta-ads) | Clean-marketing reference: plan, launch, audit, diagnose, and optimize Meta ads — objectives/ODAX, budgets & bidding, targeting, pixel/CAPI, policy, and a canonical Marketing API error catalog. |
| [**fb-grey-ops**](skills/media-buying/fb-grey-ops) | Infrastructure & survival layer for grey verticals: antidetect/proxy/session discipline, agency accounts, token/session death, API mass-launch, and per-vertical playbooks (nutra, iGaming, crypto, news). |
| [**tracker-ops**](skills/media-buying/tracker-ops) | Affiliate tracker operations: Keitaro & Binom APIs, postback/S2S, metric discipline (payout event, timezones, CPL), the Meta↔tracker mapping contract, and the daily spend-sync. |
| [**senior-buyer-ops**](skills/media-buying/senior-buyer-ops) | Senior-buyer / team-lead operating layer: the day-1 operating contract, portfolio allocation, kill/watch/scale ladder, creative production pipeline, and end-to-end funnel QA — orchestrates the three adapters above. |

### Frontend

| Skill | Purpose |
|---|---|
| [**responsive-adapter**](skills/frontend/responsive-adapter) | Adapts existing web interfaces from 320px phones to 2560px+ displays while preserving the original visual system, then verifies across a device matrix. |
| [**design-stack-picker**](skills/frontend/design-stack-picker) | Selects compatible fonts, icons, components, imagery, motion, and design primitives with a reuse-first approach. |

### Security

| Skill | Purpose |
|---|---|
| [**secure-coding**](skills/security/secure-coding) | Secure defaults and review guidance for JavaScript, Node.js, HTML, CSS, APIs, authentication, databases, uploads, GraphQL, and AI-assisted code. |
| [**js-obfuscation**](skills/security/js-obfuscation) | JavaScript protection, obfuscation, anti-automation, and anti-debugging techniques for authorized testing and software protection. |

### Research

| Skill | Purpose |
|---|---|
| [**deep-research**](skills/research/deep-research) | Traceable multi-source research with primary-source prioritization, verification, confidence labels, and explicit knowledge gaps. |

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
`senior-buyer-ops` routes into `meta-ads` / `fb-grey-ops` / `tracker-ops`).

## Contributing

Improvements and new skills are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
format, quality bar, and local checks.

## License

[MIT](LICENSE)
