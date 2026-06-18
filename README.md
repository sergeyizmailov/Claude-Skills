# Agent Skills

[![CI](https://github.com/sergeyizmailov/Claude-Skills/actions/workflows/ci.yml/badge.svg)](https://github.com/sergeyizmailov/Claude-Skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skills standard](https://img.shields.io/badge/Agent%20Skills-open%20standard-8A2BE2)](https://agentskills.io)

**Heavyweight, hand-crafted skills for AI coding agents.** Not thin prompt wrappers or a list of tips — each one is a deeply engineered, multi-phase playbook the agent loads on demand, executes step by step, and **verifies its own work against** before claiming done.

Every skill here is built the hard way: from **multi-source deep research with adversarial fact-verification and current 2026 data**, then pressure-tested on real tasks and gated by CI. The goal is one quality bar — a skill should make an agent *measurably* better at a task, or it doesn't ship.

Built on the open [Agent Skills standard](https://agentskills.io) (`SKILL.md`), so they run in **Claude Code, Cursor, Gemini CLI, GitHub Copilot, VS Code, Codex, opencode** and other compatible tools — not tied to any single model or vendor.

## What makes these different

Most public skills are lightweight: a short description and a few hints. These are the opposite — they trade weight for reliability.

- **Research-backed, not vibes** — each skill's guidance comes from a fan-out research pass across primary sources (official docs, standards bodies, real top repos), with claims adversarially verified and refuted myths thrown out. Current as of 2026, not stale training memory.
- **Verification-driven** — the skill doesn't just *act*, it *proves the result*. `responsive-adapter` won't report success until a real browser confirms every viewport in an 8-width device matrix passes — no "looks right in the diff" hand-waving.
- **Deep, layered, and bundled** — multi-phase workflows, bundled scanners/scripts that do the deterministic work, and a dozen on-demand reference files per skill. This is engineering, not a paragraph.
- **Scope-disciplined** — explicit "may / may not change" rules so the agent fixes the real problem and nothing else. No scope creep, no surprise rewrites.
- **Cheap to keep installed** — only a short `description` stays in context; the heavy playbook and references load *only* when the skill actually triggers. All that depth costs you nothing until it's needed.
- **CI-enforced** — every skill's frontmatter is schema-validated, scripts are shellchecked, Markdown is linted on every push. Quality is gated, not promised.

## Skills

| Skill | What it does | Triggers on |
|---|---|---|
| [**responsive-adapter**](skills/responsive-adapter) | Makes any existing page fully adaptive from 320px phones to 2560px+ widescreens — without changing the visual design. Static anti-pattern scanner → modern-CSS fixes → browser-verified device matrix → report. | "make this responsive", "fix mobile layout", "horizontal scroll", "sidebar broken on tablet" |
| [**design-stack-picker**](skills/design-stack-picker) | A reuse-first selection layer for frontend building blocks — icons, fonts, components, color, motion — that inspects the project and picks the smallest thing that fits instead of inventing or over-installing. | "build a landing page", "restyle this", "make it look better", any frontend visual choice |

More on the way — same bar. Each skill's own `SKILL.md` is the full reference.

## Install

Skills live one level deep under your agent's skills directory (`~/.claude/skills/` for Claude Code; see your tool's docs for others). Clone and copy the ones you want:

```bash
git clone https://github.com/sergeyizmailov/Claude-Skills.git
cp -R Claude-Skills/skills/responsive-adapter   ~/.claude/skills/
cp -R Claude-Skills/skills/design-stack-picker  ~/.claude/skills/
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

The `description` is the only part always in context, so it carries the trigger; everything else stays out of the way until needed. See [CONTRIBUTING.md](CONTRIBUTING.md) for the full anatomy and the quality bar.

## Contributing

New skills and fixes are welcome — one skill per PR, held to the same bar: research-backed, verification-driven, and it must make an agent measurably better at a real task. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) — use them, fork them, adapt them.
