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

## Hazard, not raw count

Rank each dimension by FAILURE RATE (deaths ÷ accounts exposed), not raw deaths —
the most-used domain/proxy/creative shows the most deaths simply because it ran
most. Set a minimum-exposure floor before trusting a rate: a batch of 3 accounts
at 100% death outranks a 200-account batch at 30% but is noise — need enough
accounts on a dimension before its rate means anything. Also weight by survival
TIME (an account that died at $5 pre-spend is a DOA supply problem; one that died
at $400 after 10 days is a scaling/creative-heat problem — opposite fixes).

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
three sharing an attribute is that attribute.

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

<!-- Changelog 2026-08-11: New (review r3, gpt) — portfolio forensics: log
survival dimensions, hazard-rate (not raw count) + survival-time weighting,
balanced infra-test designs to beat confounding (the third testing mode from
measurement-experimentation-ops), cross-account anomaly pivots, incident
fingerprint library. Method only; reactions stay in 01/05/tracker-ops. -->
