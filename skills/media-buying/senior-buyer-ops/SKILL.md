---
name: senior-buyer-ops
description: "Operating layer for a senior grey media-buyer / team lead: the team operating-contract to pin on day 1, portfolio budget allocation (test/scale/reserve), kill/watch/scale ladder, creative production cadence, and end-to-end funnel QA. Orchestrates meta-ads (buy), fb-grey-ops (survive/launch), tracker-ops (count)."
---

# Senior Buyer Ops

The layer above the three adapters. They tell you HOW to buy / survive / count;
this tells you WHAT to decide as the person accountable for a portfolio and a
team's numbers. Call the adapters in order; this file owns the decisions between
them.

Route: buy mechanics → `meta-ads` · infra/launch/survival → `fb-grey-ops` ·
trackers/metrics → `tracker-ops` · is-a-result-real / experiment design →
`measurement-experimentation-ops` · portfolio & cadence →
`references/01-portfolio-and-cadence.md` · creative production →
`references/02-creative-ops.md` · funnel QA → `references/03-funnel-ops.md`.

Before you scale or kill on a difference, confirm it's real, not noise
(`measurement-experimentation-ops`): the kill/scale ladder and marginal-scaling
math below assume a MATURED, non-contaminated result.

## Operating contract (pin on day 1, in writing — before any spend)

The single most expensive mistake is optimising against the wrong definition.
Get these from the TL explicitly, don't infer:

1. Payout event — WHICH tracker status/measure pays (lead? reg? FTD? qualified
   FTD? confirmed COD?). Everything downstream is priced on this.
2. Downstream stages + conversion lag — how long until the payout event matures
   (call-center confirm / deposit / KYC). Sets your judging window.
3. Caps — daily/total offer caps; traffic past a cap is unpaid.
4. KPI + targets — target CPA/CPL, and the QUALITY metric the advertiser judges
   later (reg→FTD, confirm %, scrub rate).
5. Timezone — the ad-account tz used for every daily number and the sheet's tz.
6. Naming + mapping — the campaign-name convention and the Meta-macro→tracker-
   param mapping that makes it split (tracker-ops mapping contract).
7. Reporting source of truth — which sheet/dashboard is authoritative and by
   when each day.
8. Responsibility zones + escalation — who owns accounts/creatives/tracker/
   payments; who to ping on a ban wave, a tracking break, a billing hold.

Missing any of 1-8 = you are flying blind; resolve before launch.

## Cadence

- Daily: spend→cost sync (tracker-ops) → per-account CPL vs target → kill/watch/
  scale (01) → update watchlist → report before the deadline.
- Weekly: portfolio review — winner migration, replacement queue, creative
  backlog health, buyer/stock comparison (01).

<!-- Changelog 2026-08-11: New orchestrator skill (per peer-review, gpt) giving
the senior-buyer/TL operating layer that the three adapter skills lacked:
operating-contract intake, cadence, and references for portfolio, creative-ops,
funnel-ops. Dense/LLM-facing; routes to meta-ads/fb-grey-ops/tracker-ops. Review
r3 (gpt): added routing to the new measurement-experimentation-ops sibling
(confirm a result is real before scale/kill). -->
