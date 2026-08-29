---
name: senior-buyer-ops
description: "Senior media-buyer / team-lead operating layer (clean and grey portfolios alike): day-1 operating contract, portfolio allocation across accounts (test/scale/reserve), kill/watch/scale + marginal scaling, creative-intelligence pipeline, end-to-end funnel QA, cross-platform (Meta + Google) allocation. Orchestrates meta-ads / meta-grey-ops / google-ads / google-grey-ops / google-feed-ops / tracker-ops / measurement-experimentation-ops."
---

# Senior Buyer Ops

The layer above the four adapters (buy / survive / count / measure): they tell you HOW;
this tells you WHAT to decide as the person accountable for a portfolio and a
team's numbers. Call the adapters in order; this file owns the decisions between
them.

Route by platform, then by layer:

| Layer | Meta | Google |
|---|---|---|
| Buy mechanics | `meta-ads` | `google-ads` |
| Infra / launch / survival | `meta-grey-ops` | `google-grey-ops` |
| Retail data layer | — | `google-feed-ops` |

**Scope: Meta (FB/IG) + Google Ads only** — no Microsoft Ads, TikTok, or other networks.

Platform-agnostic: trackers/metrics → `tracker-ops` · is-a-result-real →
`measurement-experimentation-ops` · portfolio & cadence →
`references/01-portfolio-and-cadence.md` · creative production →
`references/02-creative-ops.md` · funnel QA → `references/03-funnel-ops.md` ·
automated kill/scale rules that survive small samples →
`references/04-automated-rules.md` · which automation pipe (API/MCP/CSV/Sheets)
for agent vs human → `references/05-automation-channels.md`.

**Do not port structure doctrine between platforms.** Google is explicit-search-intent driven (Ani:
"every search query is a person telling you something, not a demographic"), so the split that pays is
by **intent and unit economics**, not by campaign count — merging price tiers and funnel stages the way
Meta rewards is what fails there. Consolidation itself is normal on Google (`google-ads/01`). The
operating discipline below is shared; the mechanics are not.

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
5. Timezone **and currency** of every ad account — the tz used for every daily
   number and the sheet. Google serving-account tz/currency are **permanent**
   (`google-grey-ops/07`). Meta change **closes** the account and opens a new
   act ID (`meta-grey-ops/08`). A mismatch is overhead for the life of the seat.
6. Naming + mapping — the campaign-name convention and the Meta-macro→tracker-
   param mapping that makes it split (tracker-ops mapping contract).
7. Reporting source of truth — which sheet/dashboard is authoritative and by
   when each day.
8. Responsibility zones + escalation — who owns accounts/creatives/tracker/
   payments; who to ping on a ban wave, a tracking break, a billing hold.

Missing any of 1-8 = you are flying blind; resolve before launch.

### Google adds three to the contract

Pin these too when the platform is Google — each one silently redefines a number above:

9. **Which conversion actions are primary and include-in-conversions.** This, not the bid strategy,
   defines what Smart Bidding chases. An analytics-only action left included corrupts every target.
10. **Whether offline conversion import is even available** on this account's developer token — the
    2026-06-15 cutoff blocks new adopters (`tracker-ops/04`). If it is closed, the whole "optimize on
    the payout event" plan needs a different path, and you need to know before quoting a CPA target.
11. **Certification and verification state per target geo**, with expiry dates. Financial services and
    gambling both changed multiple times in 2026; a lapsed certificate stops serving without warning.

### Two 2026 facts that change portfolio decisions

Moved to `references/01-portfolio-and-cadence.md` (§ 2026 market facts) — they are the most
perishable claims in this skill; re-verify there by 2026-10-01 (post-Sept-1 AI Max migration).

## Cadence

- Daily: spend→cost sync (tracker-ops) → per-account CPL vs target → kill/watch/
  scale (01) → update watchlist → report before the deadline.
- Weekly: portfolio review — winner migration, replacement queue, creative
  backlog health, buyer/stock comparison (01).
