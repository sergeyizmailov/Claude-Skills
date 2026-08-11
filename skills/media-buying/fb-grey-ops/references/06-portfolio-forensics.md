# 06 — Portfolio forensics (why accounts die, attributed)

senior-buyer-ops/01 says "diagnose which cause" for a ban-rate spike. This is the
HOW: turn a pile of dead accounts into an attributed hazard so you fix the real
driver instead of superstitiously changing everything at once.

## Log the survival dimensions (or you can't attribute anything)

For every account log, from birth: supplier/batch (which agency shipment),
account age at first spend and at death, antidetect profile + proxy cluster
(subnet/ASN, not just the single IP), domain(s) used, creative family (the
attribute bundle from senior-buyer-ops/02), launch method (API vs manual,
schedule, day-0 spend jump), spend-at-death, and the death signal (checkpoint /
disable / restriction / soft throttle). Death without these fields = an anecdote.

## Failure rate, not raw count (and know which rate)

Rank each dimension by a RATE, not raw deaths — the most-used domain/proxy/creative
shows the most deaths simply because it ran most. Two rates, don't conflate them:
- `deaths ÷ accounts exposed` = cumulative failure rate (share dead so far).
  Fine for a quick pass, but it ignores how long each account survived and
  censors nothing.
- Exposure-adjusted rate = deaths ÷ account-days AT RISK, censoring accounts still
  alive. (The true hazard is time-dependent and conditional on survival; this is
  the practical incidence-rate estimator of it.) For the shape over account age,
  use Kaplan–Meier (survival curve — the hazard is derived from it) or a
  discrete-time hazard model.
  Reach for this once you have enough history — it separates "dies fast" from
  "dies eventually" that the cumulative rate blurs.
Set a minimum-exposure floor before trusting either: 3 accounts at 100% death
outranks a 200-account batch at 30% but is noise — need enough accounts (and
account-days) on a dimension before its rate means anything. Survival TIME is the
same signal directionally: died at $5 pre-spend = DOA supply problem; died at $400
after 10 days = scaling/creative-heat problem — opposite fixes.

## Confounding is the whole trap → balanced designs

New domain + new creative + new account batch launched together → a ban wave
can't be pinned on any one. To keep attribution possible, vary ONE infra axis at
a time across an otherwise-balanced set:

- Infrastructure test mode: run the SAME proven creative across accounts that
  differ only in the axis under test (domain A vs B; proxy cluster A vs B; supplier
  batch A vs B), balanced counts. Divergent death/CPM/delivery then isolates that
  axis. This is the infra-fixed inversion of a creative test — the third testing
  mode (measurement-experimentation-ops). Never move both axes at once when
  something is dying.
- When you must change several things (new vertical launch), at least stagger
  them so the timeline separates the effects.

## Cross-account anomaly detection

Bans cluster by shared cause. When several accounts fail close together, pivot on
the shared attribute: same subnet/ASN (proxy cluster burned), same domain (domain
flagged → rotate, tracker-ops/03 signal), same supplier batch (bad shipment →
stop launching it, claim replacements), same creative family (policy pattern
tripping review → pull it everywhere, not just the banned account), same launch
script/timing (automation fingerprint). One account dying is background rate;
three sharing an attribute makes that attribute the PRIME SUSPECT — a hypothesis
to confirm with a balanced/controlled check (above), not a proven cause (it can
be a confounder, and clustered deaths can be coincidence at low counts).

## Incident fingerprints (match new deaths to a known pattern)

Keep a short library of past incidents as {symptom + timing + shared attribute →
confirmed cause → fix}. A new wave usually rhymes with an old one; matching the
fingerprint skips the re-diagnosis. Examples of distinct fingerprints: instant
day-0 disable across a batch (supply/verification), gradual CPM climb then death
(creative heat / policy drift), simultaneous checkpoint across one subnet (proxy
cluster / geo-mismatch), single-domain collapse to ~0 LP CTR (domain/SSL/cloaca,
not a ban — funnel fault, senior-buyer-ops/03).

## Boundary

This is diagnosis/attribution METHOD. The reactions (freeze, rotate domain,
replace batch, kill creative) live in 01/05 and tracker-ops; the portfolio-level
decision (shift budget to testing after a wave) is senior-buyer-ops/01.
