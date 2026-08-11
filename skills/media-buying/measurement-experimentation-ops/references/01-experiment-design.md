# 01 — Experiment design (decision rules, not stats theory)

The math (power, p-values, confidence intervals) is assumed known. What follows
is only the media-buying-specific application and the traps that actually bite.

## Size it before launch (or don't call it a test)

- You need three numbers to size: baseline conversion RATE, the minimum
  detectable effect (MDE) you'd actually ACT on, and the tolerable error rates.
  Smaller MDE → quadratically more sample. If the honest MDE needs more
  conversions than the account will produce in the window before it fatigues or
  dies, the causal test is infeasible — screen instead and say so (SKILL gate).
- Convert sample to a spend/time budget: needed conversions ÷ expected daily
  conversions = days; days × daily spend = the test's cost. Decide if the answer
  is worth that before spending it. (An underpowered "no difference" = INCONCLUSIVE,
  not negative — see below.)

## SRM — the first thing to check, before the metric

Cells designed to split evenly should arrive within noise of even. A persistent
skew (e.g. 60/40 on a "50/50") means randomization/logging/delivery is broken →
the comparison is invalid regardless of how good the winner looks. In Meta's A/B
tool, unequal delivery is expected in NON-A/B parallel cells (the algorithm
favors one) — that's exactly why parallel ABO cells are screening, not causal.

## Peeking & stopping

- Fix the window and the decision metric BEFORE launch. Reading daily and
  stopping on the first green crossing manufactures false winners; early leads
  reverse. Meta's "end test early if a winner is found" is automated peeking —
  off by default.
- One primary decision metric tied to the payout event. Secondary metrics are
  context, not tie-breakers you reach for when the primary disappoints.

## Contamination (why two "isolated" cells aren't)

- Audience overlap: same users eligible for both cells → their behavior is shared
  noise. The A/B Test tool enforces non-overlapping groups; manual parallel cells
  do not. Advantage+ broad campaigns are the worst offenders — they expand into
  whatever you thought was a separate manual cell.
- Auction cannibalization: duplicating a winner to "scale the test" makes the
  copies bid against each other; the higher-value one starves the other →
  looks like the loser lost on merit (it lost on overlap). Scale in place or
  differentiate.
- Shared pixel/dataset + retargeting: a retargeting audience feeds on the
  prospecting cell's traffic — the cells aren't independent.

## Conversion lag vs the window

The judging window must be ≥ the click→payout lag (call-center confirm, deposit,
KYC). Judge on the CLICK-DATE cohort so late-maturing conversions land back on
the day/variant that caused them (tracker-ops/03). Deciding on conversion-date
volume mid-lag systematically punishes the newest (still-maturing) variant.

## Invalid vs inconclusive vs negative (don't collapse these)

- INVALID (SRM, tracking break, policy pause mid-test, contamination): throw it
  out and re-run; it's not evidence either way.
- INCONCLUSIVE (ran clean but underpowered / effect smaller than MDE): you
  learned the effect is *at most small*; decide by cost, not by pretending it's a
  tie you can break.
- NEGATIVE (powered, clean, no lift): real information — stop funding the
  variant/channel. Only a powered clean test earns this verdict.

## Cross-refs

Meta tool mechanics & incrementality options → 02. Cohort/nowcast math for the
lag window → tracker-ops/03. Infra-isolation designs → fb-grey-ops/06.
