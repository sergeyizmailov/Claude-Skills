# Agent Skills

[![CI](https://github.com/sergeyizmailov/Claude-Skills/actions/workflows/ci.yml/badge.svg)](https://github.com/sergeyizmailov/Claude-Skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skills standard](https://img.shields.io/badge/Agent%20Skills-open%20standard-8A2BE2)](https://agentskills.io)

Reusable, verification-oriented skills for AI coding agents. Each skill provides a focused
workflow and can include references, decision guides, or deterministic helper scripts.

The collection follows the open [`SKILL.md`](https://agentskills.io) format and works with
Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, VS Code, opencode, and other compatible
agents.

## Skills

### Development

| Skill | Purpose |
|---|---|
| [**responsive-adapter**](skills/responsive-adapter) | Adapts existing web interfaces from 320px phones to 2560px+ displays while preserving the original visual system, then verifies the result across a device matrix. |
| [**design-stack-picker**](skills/design-stack-picker) | Selects compatible fonts, icons, components, imagery, motion, and design primitives with a reuse-first approach. |
| [**secure-coding**](skills/secure-coding) | Applies secure defaults and review guidance for JavaScript, Node.js, HTML, CSS, APIs, authentication, databases, uploads, GraphQL, and AI-assisted code. |

### Research and operations

| Skill | Purpose |
|---|---|
| [**deep-research**](skills/deep-research) | Runs traceable multi-source research with primary-source prioritization, verification, confidence labels, and explicit knowledge gaps. |
| [**facebook-instagram-ads**](skills/facebook-instagram-ads) | Plans, launches, audits, and optimizes Meta advertising across Facebook and Instagram using current evidence and operational playbooks. |

### Security research

| Skill | Purpose |
|---|---|
| [**js-obfuscation**](skills/js-obfuscation) | Provides JavaScript protection, obfuscation, anti-automation, and anti-debugging techniques for authorized testing and software protection. |

## Install

Clone the collection:

```bash
git clone https://github.com/sergeyizmailov/Claude-Skills.git
```

Install every skill for Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -R Claude-Skills/skills/* ~/.claude/skills/
```

Or install only the skills you need:

```bash
cp -R Claude-Skills/skills/deep-research ~/.claude/skills/
cp -R Claude-Skills/skills/secure-coding ~/.claude/skills/
```

For Codex, copy the same folders to `~/.codex/skills/`. Other compatible agents may use a
different skills directory.

## Structure

```text
skills/<name>/
├── SKILL.md
├── agents/       # optional agent-facing metadata
├── references/   # optional on-demand documentation
└── scripts/      # optional deterministic helpers
```

Only the `name` and `description` frontmatter is needed for discovery. Detailed workflows
and supporting files load when a skill is selected.

## Contributing

Improvements and new skills are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) for the
format, quality requirements, and local checks.

## License

[MIT](LICENSE)
