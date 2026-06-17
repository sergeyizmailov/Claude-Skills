# Agent Skills

[![CI](https://github.com/sergeyizmailov/claude-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/sergeyizmailov/claude-skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skills standard](https://img.shields.io/badge/Agent%20Skills-open%20standard-8A2BE2)](https://agentskills.io)

A growing library of **production-grade skills for AI coding agents** — concrete playbooks that make an agent measurably better at a task, not toy demos. Each skill is a self-contained workflow the agent loads on demand, follows step by step, and verifies its own work against.

Built on the open [Agent Skills standard](https://agentskills.io) (`SKILL.md`), so they work in **Claude Code, Cursor, Gemini CLI, GitHub Copilot, VS Code, Codex, opencode** and other compatible tools — not tied to any single model or vendor.

## Highlights

- **Verification-driven** — skills don't just *do*, they *check*. The responsive skill won't claim done until a real browser confirms every viewport passes.
- **Self-contained** — no dependency on private tooling; portable across agents and stacks.
- **Lazy by design** — only a short `description` stays in context; the full playbook and references load when the skill is actually triggered, so they're cheap to keep installed.
- **CI-enforced quality** — every skill's frontmatter is schema-validated, scripts are shellchecked, Markdown is linted.

## Skills

| Skill | What it does | Triggers on |
|---|---|---|
| [**responsive-adapter**](skills/responsive-adapter) | Makes any existing page fully adaptive from 320px phones to 2560px+ widescreens — without changing the visual design | "make this responsive", "fix mobile layout", "horizontal scroll", "sidebar broken on tablet" |
| [**design-stack-picker**](skills/design-stack-picker) | Picks the right building blocks (icons, fonts, components, color, motion) instead of inventing them — reuse-first | "build a landing page", "restyle this", "make it look better", any frontend visual choice |

More on the way. Each skill's own `SKILL.md` is the full reference.

## Install

Skills live one level deep under your agent's skills directory (`~/.claude/skills/` for Claude Code; see your tool's docs for others). Clone and copy the ones you want:

```bash
git clone https://github.com/sergeyizmailov/claude-skills.git
cp -R claude-skills/skills/responsive-adapter   ~/.claude/skills/
cp -R claude-skills/skills/design-stack-picker  ~/.claude/skills/
```

Your agent auto-discovers them on the next session. To confirm: ask it *"make this page responsive"* or *"pick an icon set for this landing"* and it should reach for the matching skill.

## How a skill is built

Each skill is one directory with a `SKILL.md` entrypoint and optional bundled resources:

```
skills/<name>/
├── SKILL.md        # name + description frontmatter, then the workflow
├── references/     # deep-dive docs, loaded only when the workflow needs them
└── scripts/        # helper scripts the skill calls
```

The `description` is the only part always in context, so it carries the trigger; everything else stays out of the way until needed. See [CONTRIBUTING.md](CONTRIBUTING.md) to add one.

## Contributing

New skills and fixes are welcome — one skill per PR. The bar: it should make an agent measurably better at a real task. See [CONTRIBUTING.md](CONTRIBUTING.md) for the anatomy of a skill and the local checks to run.

## License

[MIT](LICENSE) — use them, fork them, adapt them.
