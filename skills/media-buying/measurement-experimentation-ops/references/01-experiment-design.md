# 01 — Experiment design (decision rules, not stats theory)

The math (power, p-values, confidence intervals) is assumed known. What follows
is only the media-buying-specific application and the traps that actually bite.

## Size it before launch (or don't call it a test)

- The non-obvious consequence: if the MDE you'd actually act on needs more
  conversions than the account produces before it fatigues/dies, the causal test
  is INFEASIBLE — screen instead and say so (SKILL gate). Price it in spend/days
  and decide the answer's worth it first.
- An underpowered "no difference" = INCONCLUSIVE, not negative (below).

### Worked sizing (the gate is arithmetic, not vibes)

Two-proportion rule of thumb at α=0.05, power 80%: `clicks/arm ≈ 16 · p(1−p) / δ²`, where p = base
rate and δ = ABSOLUTE MDE.

- **Feasible:** 5,000 clicks/day, payout CVR 2%, you'd act only on +20% relative (δ=0.004):
  16·0.0196/0.000016 ≈ 19,600 clicks/arm ≈ 392 conversions/arm. At 100 payout events/day split
  50/50 → ~8 days per arm, plus the lag window → run it.
- **Infeasible:** same offer at 300 clicks/day (6 events/day, 3/arm): 392/3 ≈ 130 days per arm —
  the account fatigues or dies first → say so, drop to geo holdout or screening, label it
  directional (SKILL gate).
- p is the PAYOUT-event rate, matured — never the front-end lead rate — and the window must still
  cover the lag (tracker-ops/03). Leverage: halving the relative MDE you'd accept quadruples the
  sample; that trade is the whole decision.

## SRM — the first thing to check, before the metric

SRM is about the RANDOMIZED-UNIT counts vs the planned split, nothing else. If a
50/50 assignment arrives materially off (a chi-square on the unit counts flags
it), randomization or logging is broken → the comparison is invalid regardless of
how good the winner looks. Do NOT call downstream divergence (spend, impressions,
conversions between cells) SRM — that's usually a legitimate delivery/auction
effect. In Meta's A/B tool the assignment is randomized (SRM-checkable); in NON-A/B
parallel cells the algorithm allocates unevenly by design — that's not SRM, it's
why parallel ABO cells are screening, not causal.

## Peeking & stopping

- Meta's "end test early if a winner is found" is automated peeking — leave off
  unless Meta's sequential decision rule is verified (unpublished, so don't assume
  it's valid). Pre-set the window and ONE decision metric tied to the payout event
  (secondary metrics are context, not tie-breakers).
- **DIY valid stopping rule (gambler's-ruin sequential test, Evan Miller — source
  verified live 2026-08-27):** size the test as usual to N = TOTAL SUCCESSSES of
  the decision metric across BOTH arms. Track T and C (successes so far per arm).
  Stop and declare a winner the moment `|T − C| ≥ 2.25·√N` (two-sided 5%;
  `2·√N` one-sided). If `T + C` reaches N first → no winner. Valid under constant
  peeking, ignores failure counts entirely (runs on raw tracker postbacks), no
  free parameters. Trade-off: a null test runs LONGER than fixed-sample; real
  wins land 25–50% earlier. Works when `1.5·p + lift < 36%` (p = baseline CVR);
  above that, fixed-sample wins.

## Comparing two assets on small counts (better, not just "bad")

The Poisson ladder (senior-buyer-ops/04) answers "provably bad"; this answers
"challenger vs control — which one wins". Closed form (Evan Miller, source
verified live 2026-08-27), with α = successes+1, β = failures+1 per arm:

`Pr(p_B > p_A) = Σ_{i=0..α_B−1} B(α_A+i, β_B+β_A) / ((β_B+i)·B(1+i,β_B)·B(α_A,β_A))`

No log-beta in the environment? Draw ~10⁵ samples from each Beta(α,β) and count
— same number. Decision use: promote a challenger at `Pr > 0.90–0.95`, chosen by
the cost of a wrong promotion — same decision-parameter logic as the ladder's
confidence level. It changes the STOPPING rule, not the validity requirements:
no contamination, matured cohorts, ONE decision metric — everything above still
applies.

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
- INCONCLUSIVE (underpowered / CI too wide): a non-sig result does NOT mean the
  effect is small — only that you couldn't detect it. Decide by cost/prior; re-run
  powered if it matters.
- NO MEANINGFUL EFFECT: only claimable when the CI sits inside pre-set equivalence
  bounds (TOST) — a non-sig result, even powered, is not proof of no effect. Then
  stop funding it.

## Cross-refs

Meta tool mechanics & incrementality options → 02. Cohort/nowcast math for the
lag window → tracker-ops/03. Infra-isolation designs → meta-grey-ops/06.
