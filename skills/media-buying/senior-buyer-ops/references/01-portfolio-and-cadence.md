# 01 — Portfolio & cadence (the TL decisions)

Single-account diagnosis lives in meta-ads; this is the layer above: allocating
a finite pool of accounts + budget + creative across testing and scaling.

## 2026 market facts (perishable — re-verify by 2026-10-01)

- **Auction supply contracted ~12.3% YoY** (45.9B → 40.25B) across 21,425 accounts (Optmyzr, Q1 2025 →
  Q1 2026; their text misstates it as 11%). Flat
  impressions at flat spend is not necessarily degradation. Do not kill on it.
- **Since 2026-08-17, budget-limited tCPA/tROAS campaigns drive toward the literal target**
  (`google-ads/02`). Any account that was quietly overperforming a loose target is now exposed.
  Audit targets before setting scale expectations with a TL.

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
  domain, a billing/asset issue, or the whole bundle. Attribute the cause before
  reacting — hazard-rate forensics in meta-grey-ops/06 (reactions in 01/05).

## Kill / watch / scale ladder

Automating any of the three: `04-automated-rules.md` (thresholds that hold at
small counts, and the platform constraints on expressing them).

- KILL: use the threshold from the operating contract, not a built-in default —
  the "no payout event after ~1.5-2× target CPA" figure is a common starting
  heuristic, but the team's contract sets the real number; plus the account
  verdict (agreed $ with CPA over target, zero delivery in 2-3d, or any disable).
- WATCH: provisional — inside target but thin volume, or a winner whose quality
  metric hasn't matured yet (judge on the click-date cohort, tracker-ops/01).
- SCALE: proven account+creo → vertical (~+20-30%/day is a team heuristic —
  large jumps CAN re-enter learning, but Meta guarantees no universal %,
  meta-grey-ops/04) or horizontal (duplicate the winner to reserve accounts).
  Migrate winners to fresh accounts before the old one fatigues/dies.

## Marginal scaling (never scale on blended CPA)

Blended CPA is an average over already-cheap early spend; it stays green while
the NEXT dollar is already unprofitable. Decide scale on the margin:

- `incremental_CPA = Δspend / Δmature_conversions` between two comparable windows
  (same account, same tz-day basis). Two setup rules or the number is garbage:
  compare a MEANINGFUL step (a tiny day-to-day Δspend is dominated by daily
  variance — use a real budget jump or a multi-day window), and count only MATURE
  conversions (the newest cohort lags, so a raw Δ fakes saturation — nowcast it,
  tracker-ops/03).
- Read the response curve: while incremental_CPA ≤ target, keep ramping; when it
  rises with spend at fixed creative/audience, you've hit saturation — the fix is
  new angle/audience/account (horizontal), not more budget into the same set.
- Rule out FALSE saturation before declaring the account tapped: an OFFER/traffic
  cap (spend past the cap is unpaid → incremental_CPA explodes but it's a payout
  ceiling, not auction fatigue), a learning reset from too big a step, or an
  immature cohort (above).
- Rollback: pre-set the step-down (e.g. revert to the last budget where
  incremental_CPA was in target) and the trigger (N days of mature
  incremental_CPA over target). Log the step so a revert is one action.

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
