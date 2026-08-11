---
name: measurement-experimentation-ops
description: "Decide whether a media-buying result is REAL before acting on it: pick the testing mode (causal / screening / infrastructure), size it, and dodge the validity traps (SRM, peeking, Advantage+ contamination, conversion lag, multiple testing). Covers Meta's tools — A/B Test, ad_study API, Conversion Lift, GeoLift, Robyn/MMM — and the grey reality where clean holdouts aren't available. Pairs with meta-ads, tracker-ops, senior-buyer-ops, fb-grey-ops."
---

# Measurement & Experimentation Ops

The layer that answers the ONE question the other skills assume before they act:
*is this difference real, or am I about to scale noise?*

## Pick the testing mode by the decision at stake

Three modes, different evidence bars — match the mode to what a wrong answer
costs, don't default to whatever's easy:

1. **Causal** (randomized): the ONLY mode that proves incrementality. One
   treatment vs a non-overlapping control/holdout, pre-sized sample. Use for
   expensive, hard-to-reverse bets: offer, funnel, landing page, "does this
   channel even lift sales." Cost: volume + discipline + often a Meta rep.
2. **Screening** (directional): many concepts in one ad set / parallel ABO cells;
   delivery is UNEQUAL by design, so a "winner" is a hypothesis, not a proof.
   Use for high-throughput creative hunting where being fast beats being certain.
   Never present a screen result as validated.
3. **Infrastructure** (isolate infra variance): hold the CREATIVE fixed, vary one
   infra axis (domain / proxy cluster / account batch) across a balanced set to
   attribute delivery/ban/CPM differences to infra, not creative. The grey
   inversion of a normal test — see fb-grey-ops/06.

## Feasibility gate (grey reality — check BEFORE promising a clean test)

Causal measurement often isn't available on grey/small-account buys: too little
volume to power a holdout, accounts die mid-test, no clean pixel signal, no rep
for a sandboxed Conversion Lift. When you can't run causal, SAY SO and drop to
the best affordable proxy (geo holdout, pre/post with tracker truth, screening)
— label it directional, don't dress a screen up as a lift study. Choosing the
honest weaker method beats a "causal" test that's silently contaminated.

## Validity traps (each one silently flips a conclusion)

- **SRM (sample ratio mismatch):** cells that should split 50/50 arrive lopsided
  → the randomization or logging is broken; the result is invalid, not "a win."
  Check cell sizes before reading the metric.
- **Peeking:** stopping the moment it looks significant inflates false positives.
  Meta's A/B "end test early if a winner is found" IS peeking — leave it off, run
  the pre-set window (02).
- **Contamination:** overlapping audiences between cells (esp. Advantage+ broad
  campaigns bleeding into manual cells; duplicated winners cannibalizing in the
  auction) means you're not comparing clean groups. Use the A/B Test tool's
  non-overlapping split, or geo separation.
- **Conversion lag:** judging before the payout event matures counts spend
  against unripe conversions → every fresh cohort looks like a loser. Window ≥
  the lag; nowcast if you must decide early (tracker-ops/03).
- **Multiple testing:** many variants tested at once produce chance "winners."
  Screening tolerates this (you re-test winners anyway); a causal decision needs
  the significance bar corrected for the number of comparisons.
- **Underpowered:** too few conversions to detect the effect you care about →
  "no significant difference" means *couldn't tell*, not *no difference*. Size
  first (01).

## Route references

| Need | Reference |
|---|---|
| Sizing (MDE/power as decision rules), SRM, peeking, contamination, lag, inconclusive handling | `references/01-experiment-design.md` |
| Meta tools: A/B Test, `ad_study` API, Conversion Lift, Brand Lift, GeoLift, Robyn/MMM, Andromeda implication | `references/02-meta-measurement-tools.md` |

Buy mechanics → meta-ads (its /09 owns single-account diagnosis & test-design
intake; this skill owns the validity/incrementality layer above it). Counting &
cohort truth → tracker-ops. Portfolio decisions on the result → senior-buyer-ops.

<!-- Changelog 2026-08-11: New skill (review r3, gpt) — the measurement/validity
layer for the media-buying set: three testing modes + grey feasibility gate,
validity traps (SRM/peeking/contamination/lag/multiple-testing/power), and Meta
tool routing. Tool facts verified 2026-08-11 (ad_study v25.0, GeoLift, Robyn).
Dense/LLM-facing; defers stats basics an LLM already knows. -->
