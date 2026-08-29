# Skills

Every skill is a directory here — flat, no category folders. That is deliberate: agent
runtimes discover skills one level deep, so a nested layout silently loads nothing. The
grouping below is for reading, not for the filesystem.

Install one, or all of them:

```bash
cp -R knowledge-delta-skills/skills/meta-ads ~/.claude/skills/   # one
cp -R knowledge-delta-skills/skills/* ~/.claude/skills/          # everything
```

Other runtimes use their own directory — see the table in the [root README](../README.md#install).

## Media buying — Meta & Google

Layered by concern, not by platform. These eight reference each other by skill name, so
install the set together.

| Skill | Layer |
|---|---|
| [meta-ads](meta-ads) · [google-ads](google-ads) | Buy mechanics — objectives, budgets, bidding, targeting, tracking |
| [meta-grey-ops](meta-grey-ops) · [google-grey-ops](google-grey-ops) | Account infrastructure and survival in grey verticals |
| [google-feed-ops](google-feed-ops) | The retail data layer — feed spec, Merchant API, suspensions |
| [tracker-ops](tracker-ops) | Counting — Keitaro/Binom, postbacks, timezone and CPL math |
| [measurement-experimentation-ops](measurement-experimentation-ops) | Whether a result is real before it gets scaled |
| [senior-buyer-ops](senior-buyer-ops) | Portfolio orchestration on top of the seven above |

## Frontend

| Skill | Purpose |
|---|---|
| [responsive-adapter](responsive-adapter) | Adapt an existing interface 320px→2560px+ without touching the design |
| [design-stack-picker](design-stack-picker) | Pick fonts, icons, components, imagery and motion that fit together |
| [normcore-web](normcore-web) | Build sites that read as ordinary commercial web, not art-directed product design |

## Security

| Skill | Purpose |
|---|---|
| [secure-coding](secure-coding) | Secure defaults across JS/Node/HTML/API/auth/DB/upload paths, plus AI-generated-code patterns |
| [js-obfuscation](js-obfuscation) | JavaScript protection, anti-automation and anti-debugging for authorized testing |

## Research

| Skill | Purpose |
|---|---|
| [deep-research](deep-research) | Traceable multi-source research with primary sources and confidence labels |
| [web-scraping](web-scraping) | Crawling and scraping past Cloudflare, Akamai, DataDome and PerimeterX |

## Skill authoring

| Skill | Purpose |
|---|---|
| [knowledge-delta-skill-architect](knowledge-delta-skill-architect) | Write, audit and compress skills against the method this collection follows |
