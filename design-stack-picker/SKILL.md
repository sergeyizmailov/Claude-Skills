---
name: design-stack-picker
description: >-
  Build or restyle frontend UI by selecting proven building blocks: icon sets, fonts,
  component/block libraries, accessible primitives, imagery sources, color systems,
  motion, shadows, spacing, and image optimization patterns. Use for landing pages,
  ecommerce, dashboards, web apps, emails, single components, and any task involving
  visual assets or frontend design choices. Prefer existing project systems first;
  add libraries only when they solve a real gap. See resources.md for the catalog and
  patterns.md for implementation snippets.
---

# design-stack-picker

Use this skill to improve frontend quality without inventing every asset from scratch.
It is a **selection layer**, not a mandate to replace a project's current design system.

## Core Rule

Inspect the current project before adding anything:

- framework and rendering model
- existing icons, fonts, tokens, components, image pipeline, and breakpoints
- current dependencies and visual style

Decision order:

1. Reuse the existing project system if it works.
2. Extend it with the smallest compatible building block.
3. Add a new library only when the project has no good local solution.
4. Hand-craft locally only for brand assets, tiny static pieces, or cases where a dependency is heavier than the implementation.

## Resource Loading

- Read `resources.md` only when choosing a library, font, icon set, imagery source, component set, motion tool, or color system.
- For vague "make it look better" tasks, read `resources.md` §12 first to pick concrete references/patterns before changing UI.
- Read `patterns.md` only when implementing tokens, reset, icons, fonts, cards, image markup, motion, or CSS snippets.
- Do not load both by default if the task only needs one.

## Defaults

Use these as starting points, not fixed requirements:

| Axis | Default |
|---|---|
| Icons | Iconify + Solar; Simple Icons for brand marks |
| Fonts | Unbounded display + Onest body via Fontsource |
| Components | Existing project components first; HyperUI/Preline for static sections; shadcn/Radix for React primitives |
| Color | Semantic CSS variables; one dominant brand color + one accent |
| Motion | CSS-first restrained reveal; Motion for React; GSAP only for complex timelines |
| Imagery | Real product/user/stock/CMS assets; optimized AVIF/WebP where practical |

## Dependency Budget

Do not add a dependency for:

- one icon when an icon system already exists
- one static section that existing layout primitives can handle
- a basic disclosure/dropdown in Astro/plain HTML when scoped JS is smaller and verifiable
- a visual effect achievable with existing CSS
- a library that duplicates current project dependencies

Add a dependency when it prevents real implementation risk: complex accessible widgets,
large consistent icon coverage, image optimization at scale, or multi-screen design systems.

## Context Routing

| Project context | Bias |
|---|---|
| Existing Astro/static site | Local `.astro` components, scoped CSS, progressive JS, `astro:assets`; avoid React-only primitives unless already used |
| React/Next app | Current UI layer first; shadcn/Radix for missing complex primitives |
| Admin/dashboard | Dense, scannable forms/tables/filters; minimal decoration |
| Ecommerce/catalog | Real product imagery, stable cards, search, category navigation, price/stock hierarchy, mobile filters |
| Marketing page | Stronger typography, imagery/video, section blocks, restrained motion |
| Prototype | Smallest working choice; avoid a full design system unless it will continue |

## Hard Rules

- Do not hand-draw generic SVG icons; use one coherent icon set unless it is a supplied brand logo.
- Do not accidentally ship default fonts for brand-facing UI; choose and load intentional type.
- Do not scatter magic colors/spacing/shadows inline; use tokens.
- Use accessible primitives for complex widgets: dialogs, comboboxes, tabs, menus, tooltips, switches.
- Use one family per axis: one icon style, one illustration style, one color system, one type pairing.
- Respect `prefers-reduced-motion`, visible focus, and AA contrast.
- Optimize important images; set dimensions; eager-load only the LCP image.

If a hard rule conflicts with a mature existing project convention, preserve the convention and improve incrementally.

## Workflow

1. Establish direction: ecommerce, admin, SaaS, editorial, product, campaign, etc.
2. Audit existing project foundation before changing it.
3. Choose the smallest building block that fits the project.
4. Implement with existing tokens/components where possible.
5. Use real assets; avoid decorative filler where product/content clarity matters.
6. Verify in a browser.

## Ecommerce Notes

For product/catalog UI:

- Prefer real product photos; keep placeholders neutral.
- Use stable card dimensions and `object-fit: contain` for product grids.
- Test long names, missing images, different prices, sale/stock states, and uneven item counts.
- Make category navigation, search/autocomplete, and mobile filters easy to reach and dismiss.
- Prioritize price, stock, main spec, and action hierarchy over decorative labels.

## Done Checklist

- Icons are from one set and sized consistently.
- Fonts are intentional and loaded once.
- Tokens cover colors, spacing, radii, shadows, type, and states.
- Complex widgets have keyboard/focus behavior.
- Images are real, optimized where practical, and have stable dimensions.
- Motion is restrained and respects reduced motion.
- Responsive behavior is checked from phone to wide desktop.
- Browser verification confirms no horizontal overflow and key images load with natural dimensions.
