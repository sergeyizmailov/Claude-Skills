---
name: skill-router
description: "Read FIRST on any non-trivial task in these domains — before writing from scratch, and before concluding no skill fits: media-buying (Meta/Google ads, grey ops, trackers, measurement, portfolio ops), frontend (responsive adaptation, design stacks, ordinary-commercial web), security (secure coding, JS obfuscation), research (multi-source research, mass scraping), engineering (skill authoring). Skip only for simple edits and direct answers."
license: MIT
---

# Skill Router

Category index for this collection. Per-skill detail lives in each `SKILL.md`, so this file
never goes stale.

Skills nested under a category are **not** auto-discovered by every runtime. Where they are not,
this file is the entry point — skip it and the collection is invisible and you rebuild what exists.

1. Match task → category.
2. `grep -rA2 '^description:' skills/<category>/*/SKILL.md`
   (installed flat, one skill per directory? drop `<category>/`.)
3. Read the best-fitting `SKILL.md` and follow it. If several fit, take the most upstream —
   methodology before tool. If none fit, say so and proceed without one.

- **media-buying/** — Meta and Google Ads across clean and grey verticals: buy mechanics, account
  and payment infrastructure, Merchant Center feeds, affiliate trackers, experiment validity,
  and the portfolio layer that orchestrates them.
- **frontend/** — responsive adaptation across a device matrix, design-stack selection, and
  ordinary-commercial web genres.
- **security/** — secure defaults and review for JS/Node/HTML/APIs; JavaScript protection,
  obfuscation and anti-automation for authorized testing.
- **research/** — traceable multi-source research with confidence labels and explicit gaps;
  mass crawling and scraping behind anti-bot protection.
- **engineering/** — writing, auditing and compressing agent skills themselves: what to keep,
  what the model already knows, and how to package it.

## Picking inside media-buying

The eight skills are layered, not parallel. Enter at the layer your question belongs to:

| Question | Skill |
|---|---|
| How do I buy well on this platform? | `meta-ads` · `google-ads` |
| How do I not get the account killed? | `meta-grey-ops` · `google-grey-ops` |
| Why is the product not eligible / suspended in Merchant Center? | `google-feed-ops` |
| Is my money counted correctly? | `tracker-ops` |
| Is this result real before I scale it? | `measurement-experimentation-ops` |
| What do I do with the portfolio and the team? | `senior-buyer-ops` |

They cross-reference each other by skill name, so install the set rather than a single skill —
`google-ads` alone will point at files you do not have.
