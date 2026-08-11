# 01 — Portfolio & cadence (the TL decisions)

Single-account diagnosis lives in meta-ads; this is the layer above: allocating
a finite pool of accounts + budget + creative across testing and scaling.

## Budget allocation (test / scale / reserve)

- Split the daily pool into buckets, not one blob: TESTING (new accounts/creos
  hunting for delivery + a winner), SCALING (proven account+creo, ramp), RESERVE
  (unlaunched accounts held against the ban rate). A common starting split is
  ~50/40/10 test/scale/reserve — a lever, not a law; shift toward scaling as
  winners stabilise, toward testing after a ban wave.
- Never launch the whole account stock at once — the ban rate means you'd have
  no replacements. Reserve exists to keep scaling uninterrupted.

## Account prioritisation & replacement queue

- Rank live accounts by CPA vs target AND stability, not by best single day.
  Feed scaling budget to the top; hold mid; queue the bottom for kill.
- Replacement queue: report dead/DOA accounts in batches to the agency; keep the
  reserve topped so a ban never stalls a winner. Track ban rate as a metric — a
  spike has SEVERAL possible causes: infra (IP/persona/device), a bad account
  batch from the agency, a creative/policy pattern tripping review, a burned
  domain, a billing/asset issue, or the whole bundle. Diagnose which before
  reacting (fb-grey-ops/01).

## Kill / watch / scale ladder

- KILL: use the threshold from the operating contract, not a built-in default —
  the "no payout event after ~1.5-2× target CPA" figure is a common starting
  heuristic, but the team's contract sets the real number; plus the account
  verdict (agreed $ with CPA over target, zero delivery in 2-3d, or any disable).
- WATCH: provisional — inside target but thin volume, or a winner whose quality
  metric hasn't matured yet (judge on the click-date cohort, tracker-ops/01).
- SCALE: proven account+creo → vertical (~+20-30%/day is a team heuristic —
  large jumps CAN re-enter learning, but Meta guarantees no universal %,
  fb-grey-ops/04) or horizontal (duplicate the winner to reserve accounts).
  Migrate winners to fresh accounts before the old one fatigues/dies.

## Team stop-loss

Define a portfolio-level daily loss cap with the TL (not just per-account). But
do NOT trigger it on same-day CPA alone: a bad-looking day is usually immature
cohorts (FTD/confirm lag, tracker-ops/01), so first confirm the cohort has
matured AND tracking isn't broken. Only freeze new spend when a MATURED cohort
is genuinely X% over target — otherwise you'll freeze on normal lag.

## Comparing buyers (normalise, don't rank raw)

Buyers get different stock and GEOs — raw CPA isn't comparable. Compare on
CPA-vs-target ratio within the same GEO/offer, and on winner-hit-rate per $
tested. Otherwise you reward the buyer who got the good stock.

## Watchlist / review

- Daily watchlist: accounts near a kill/scale threshold, winners whose quality
  cohort is maturing, anything with a delivery anomaly.
- Weekly review: winner migration plan, replacement queue depth, creative
  backlog vs test throughput (02), buyer comparison, ban-rate trend.

<!-- Changelog 2026-08-11: New — TL portfolio/cadence decision layer (allocation
buckets, prioritisation, kill/watch/scale ladder, team stop-loss, buyer
normalisation, watchlist/review). Ratios are levers, not laws. Peer-review r2
(gpt): kill threshold sourced from operating contract (not a default); scaling %
labelled heuristic; team stop-loss gated on matured cohort + tracking check (not
same-day CPA); ban-rate-spike causes broadened beyond infra. -->

