# knowledge-delta-skills

[![CI](https://github.com/sergeyizmailov/knowledge-delta-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/sergeyizmailov/knowledge-delta-skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skills standard](https://img.shields.io/badge/Agent%20Skills-open%20standard-8A2BE2)](https://agentskills.io)

**Not knowledge for beginners. Missing expertise for already-capable AI.**

```text
baseline what the model already does  →  research only the gaps  →  distil  →  ship the delta
```

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

Full method, what gets cut, and how volatile facts are dated:
[`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).

## Catalog

### Featured

| Skill | Adds |
|---|---|
| [**knowledge-delta-skill-architect**](skills/knowledge-delta-skill-architect) | Writes, audits, and compresses agent skills against the baseline-then-cut method this collection follows. |
| [**meta-ads**](skills/meta-ads) | Plans, launches, audits, and diagnoses Meta ad accounts — ODAX objectives, budgets/bidding, pixel/CAPI, policy, and a Marketing API error catalog. |
| [**deep-research**](skills/deep-research) | Runs traceable multi-source research with primary-source prioritization, verification, and explicit confidence labels. |
| [**secure-coding**](skills/secure-coding) | Applies secure defaults across JS/Node/HTML/API/auth/DB/upload code paths and flags AI-generated-code vulnerability patterns. |
| [**web-scraping**](skills/web-scraping) | Crawls and scrapes at scale past anti-bot defenses (Cloudflare, Akamai, DataDome, PerimeterX) using Crawl4AI and Camoufox. |
| [**responsive-adapter**](skills/responsive-adapter) | Adapts an existing web interface from 320px to 2560px+ without touching the visual design, then verifies across a device matrix. |

All 16 skills, grouped by domain — media buying, frontend, security, research,
engineering: [`CATALOG.md`](CATALOG.md).

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
