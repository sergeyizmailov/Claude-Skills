# Contributing

Thanks for wanting to add to the library. The bar is simple: a skill should make an agent **measurably better** at a task than it is with no skill — a concrete workflow, not a vibe.

## Anatomy of a skill

Each skill is one directory under a category in [`skills/`](skills/) (e.g.
`skills/frontend/`, `skills/security/`, `skills/media-buying/`, `skills/research/`).
Add to the fitting category, or create a new one:

```
skills/<category>/<name>/
├── SKILL.md        # required — the playbook
├── references/     # optional — deep-dive docs loaded on demand
└── scripts/        # optional — helper scripts the skill calls
```

`SKILL.md` starts with YAML frontmatter:

```yaml
---
name: my-skill              # lowercase-hyphenated, matches the directory
description: >-             # what it does AND when to use it (stays in context)
  One or two sentences, specific and trigger-rich, so an agent reaches
  for it at the right moment.
---
```

Then the body: a concrete workflow the agent follows. Keep it under ~500 lines and push detail into `references/` that loads only when needed.

## Guidelines

- **One skill per PR.** Easier to review, easier to revert.
- **Specific over generic.** "Make a page responsive across the device matrix" beats "help with CSS".
- **Self-contained.** Don't depend on private tooling; name portable alternatives (e.g. "Playwright or an equivalent browser tool").
- **Verify, don't assert.** If a skill produces output, it should check that output.
- **English only** in all files.

## Before opening a PR

CI runs frontmatter schema validation, Markdown lint, and shellcheck. Run them locally:

```bash
npx markdownlint-cli2 "**/*.md"
shellcheck skills/**/scripts/*.sh   # if your skill ships scripts
```

Then update the catalog table in the [README](README.md) if you added or renamed a skill.
