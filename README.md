# Claude Code Skills

A small collection of production-grade [Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) for [Claude Code](https://claude.com/claude-code) — focused on frontend craft, not toy demos. Each skill is a self-contained playbook: Claude loads it on demand, follows a concrete workflow, and verifies its own work.

| Skill | What it does | Triggers on |
|---|---|---|
| [**responsive-adapter**](#responsive-adapter) | Makes any existing page fully adaptive from 320px phones to 2560px+ widescreens — without touching the visual design | "make this responsive", "fix mobile layout", "horizontal scroll", "sidebar broken on tablet" |
| [**design-stack-picker**](#design-stack-picker) | Picks the right building blocks (icons, fonts, components, color, motion) instead of inventing them — reuse-first | "build a landing page", "restyle this", "make it look better", any frontend visual choice |

---

## responsive-adapter

Take a page someone already designed and built, and make it hold up at **every real viewport width** — without redesigning it. The desktop visual is the source of truth; every other width is a graceful adaptation.

**What makes it different from "just add media queries":**

- **Static anti-pattern scanner** (`scripts/scan.sh`) — greps the codebase for 14+ known responsive killers (missing viewport meta, `user-scalable=no`, fixed `px` widths, `100vh` without `dvh`, sub-16px inputs that trigger iOS zoom, `100vw` overflow, …) and outputs a severity-graded, `file:line` issue list before a single fix.
- **Modern primitives over breakpoint salad** — solves adaptivity with `clamp()`, container queries, `dvh/svh/lvh`, `aspect-ratio`, and `grid auto-fit/minmax` instead of five media queries per component.
- **Stack-aware** — detects vanilla CSS, Tailwind, or CSS-in-JS and follows each one's idioms (12 bundled reference files).
- **Browser-verified** — screenshots an 8-width device matrix (Android baseline → iPhone → iPad → Full HD), checks each for overflow / tap targets / typography, and **won't claim done** until every width passes.
- **Strict scope guard** — colors, fonts, content, and components are *forbidden* to change. A before/after desktop screenshot must be indistinguishable.

**5-phase workflow:** Discover → Static scan → Apply fixes → Browser verification → Report.

```
responsive-adapter/
├── SKILL.md                 # the playbook
├── scripts/scan.sh          # static anti-pattern scanner
└── references/              # 12 deep-dive guides
    ├── anti-patterns.md     # full catalog: detection + fix per pattern
    ├── modern-primitives.md # clamp, container queries, dvh/svh, :has(), subgrid
    ├── fluid-typography.md  # Utopia scale, WCAG-safe clamp formula
    ├── device-matrix.md     # every test width with rationale
    ├── touch-targets.md     # WCAG 2.5.8 vs 2.5.5, MD3 vs HIG
    ├── tailwind.md · vanilla-css.md · css-in-js.md
    ├── admin-patterns.md · menus-drawers.md · design-systems.md
    └── platform-quirks.md   # iOS Safari / Android / foldable gotchas
```

## design-stack-picker

A **selection layer** for frontend work. Instead of hand-crafting every icon, font, and component from scratch — or bolting on a random library — it inspects the current project and picks the smallest building block that fits.

**Decision order it enforces:**

1. Reuse the existing project system if it works.
2. Extend it with the smallest compatible block.
3. Add a new library only when there's a real gap.
4. Hand-craft only for brand assets or when a dependency is heavier than the code.

**What it covers:** icon sets, typography pairings, component/block libraries, accessible primitives, imagery sources, color systems, motion, shadows, spacing, and image optimization — with a **dependency budget** (don't add a library for one icon) and **context routing** (Astro vs React vs admin vs ecommerce vs marketing each get different defaults).

```
design-stack-picker/
├── SKILL.md       # selection rules, defaults, dependency budget, context routing
├── resources.md   # the curated catalog (libraries, fonts, icons, color, motion)
└── patterns.md    # implementation snippets (tokens, reset, icons, cards, motion)
```

---

## Install

Skills live one level deep under `~/.claude/skills/`. Clone the repo and copy the skill(s) you want:

```bash
git clone https://github.com/sergeyizmailov/claude-skills.git
cp -R claude-skills/responsive-adapter   ~/.claude/skills/
cp -R claude-skills/design-stack-picker  ~/.claude/skills/
```

Claude Code auto-discovers them on the next session. Each skill's `description` stays in context (cheap); the full playbook and reference files load only when the skill is triggered.

To verify they're picked up: ask Claude *"make this page responsive"* or *"pick an icon set for this landing"* and it should reach for the matching skill.

## How these are built

Each skill follows the Agent Skills spec: a `SKILL.md` with `name` + `description` frontmatter, a concrete workflow in the body (<500 lines), and bundled resources (`references/`, `scripts/`) that load on demand instead of bloating context. They favor verification over assertion — the page is "responsive" only after the browser says so.

## License

[MIT](LICENSE) — use them, fork them, adapt them.
