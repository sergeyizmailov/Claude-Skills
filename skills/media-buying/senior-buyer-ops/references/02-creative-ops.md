# 02 — Creative ops (production, not diagnosis)

meta-ads/12 diagnoses a finished ad. This is the pipeline that keeps winners
coming: in broad/Advantage+ delivery the creative is the main lever, so creative
THROUGHPUT — not targeting — is usually the real bottleneck.

## Concept model (keep flat)

Concept = angle (the claim/emotion, e.g. "news exposé", "quiz", "big win") ×
hook (first 1-2s / first line) × format (static, UGC video, screen-record).
Test at the ANGLE level first; hooks/formats are variations under a winning
angle. Don't scatter — a new angle is a new bet, a new hook is an iteration.

## Explore vs exploit (run both, don't collapse into one)

Two modes with different rules — winner-lineage alone converges to a local
maximum, so reserve a fixed EXPLORE quota (e.g. ~20-30% of test budget, a lever):
- EXPLOIT (iterate winners): CONTROL (current best) vs CHALLENGERS descended
  from proven winners — same angle, new hook/format. Change ONE variable per
  variant (hook OR first frame OR CTA OR proof) so a win is attributable and
  iterable. Promote only on the payout metric, not CTR.
- EXPLORE (new concepts): a genuinely new angle changes hook + visual +
  narrative + proof at once — that's expected, don't force one-variable here.
  You're testing the ANGLE bet, not isolating a cause; isolate later if it wins.
- Record winner lineage (which angle-family prints) AND explore results, so
  scaling pulls from exploit while explore keeps refilling the top of the funnel.

## Creative intelligence (tag at the attribute level, not the ad level)

A winner is a BUNDLE of attributes; logging "ad X won" throws away why, and the
ad dies while its winning proof-type or mechanism could live on. Tag every tested
creative on these axes so you're building a combination map, not a leaderboard:

- persona / market-awareness stage / dominant desire · mechanism (the "how it
  works" claim) · proof type (UGC, screenshot, authority, before/after-proxy,
  data) · objection handled · core emotion · angle · hook · format · funnel
  version (which prelander/offer it ran to).

- Score COMBINATIONS, not isolated winners: an angle×proof×emotion (and hook
  family) that prints across multiple unrelated accounts/GEOs is real signal; a
  single-account winner is noise until replicated. Briefs (below) then specify
  the bundle to reproduce, so production compounds on known-transferable parts.
- Decay is per-attribute on different clocks: a HOOK fatigues per audience (rotate
  fast), while an ANGLE/MECHANISM/EMOTION fatigues market-wide — the whole scene
  copies it and CTR decays everywhere at once. Detection cue: the same angle
  suddenly flooding the spy tools (below) is the market-saturation signal to jump
  to a new mechanism, not just a new hook. Track each axis as a time series, not
  one blended fatigue number.

## Multi-stage graduation

Don't jump a new creative straight to a scaling account. Graduate it: cheap
explore test → if it clears the payout bar, promote to challenger vs control →
if it beats control, migrate to a scaling account. Each stage has a bigger
budget and a higher bar; kill early stages fast, protect late-stage winners.

## Fatigue

Leading signals, per ad on the same audience: rising frequency with CTR / CVR
decaying and CPA climbing = fatigue, not auction noise. Rotate to the next
challenger from the backlog BEFORE the winner craters; don't edit the winning
ad (resets learning, fb-grey-ops/04) — launch the successor.

## Backlog & briefs (throughput is the bottleneck)

- Keep a creative backlog sized to your test cadence — if you can test N/day,
  you need ≥N new concepts/iterations queued or scaling stalls waiting on
  creative.
- Brief to the designer/editor = angle + hook + reference (spy link) + must-have
  proof/compliance notes + aspect ratios (4:5, 9:16) + what NOT to show (policy:
  before/after, personal-attribute copy, prohibited claims per the vertical
  playbook). A precise brief is the difference between one usable cut and ten
  rejects.

## Spy / creative intel (current 2026)

- AdSpy — deepest FB/IG DB (comment + affiliate-network filters); best for grey.
- AdHeart — FB/IG, strong in CIS grey scene.
- BigSpy — multi-platform, free tier (budget recon).
- PowerAdSpy — 7+ platforms in one.
- Anstrex — native + push, rips landing/pre-lander pages (nutra pre-landers).
- Meta Ad Library — free, official, but no spend/performance and no cloaked or
  rejected ads → baseline recon only, not competitive truth.
Use spy for angle discovery and prelander teardown; the winning execution is
still yours to test.
