---
name: tracker-ops
description: "Tracker ops for affiliate/media buying: Keitaro + Binom APIs (keys, reports, cost push), postback/S2S, metric discipline (payout event vs all-conversions, timezones, CPL math), daily spend-sync. Principles port to other trackers. Pairs with fb-grey-ops + meta-ads."
---

# Tracker Ops

Count money correctly and automate tracker work. Keitaro + Binom specifics
below; the metric rules and daily sync port to any tracker.

## Metric rule (NEVER violate)

1. "conversions" (Keitaro) can exceed your payout-lead count, but that is
   INTEGRATION-SPECIFIC, not an inherent 3.5-4x: the same subid+status
   OVERWRITES; extra records come only from distinct `tid`s or a genuine
   multi-step funnel. Never do CPL math on "conversions" — the payout metric is
   ONE event/status; get it from the TL in writing. (Any "3.5-4x" is one
   setup's ratio, not a law.)
2. Metric names aren't portable: Keitaro "leads" = status Lead (first event);
   Binom "leads" ≈ all conversions. Verify semantics per tracker per setup.
3. Cross-check: pixel lead count ≈ tracker lead count. A big divergence = wrong
   metric or broken tracking; stop and reconcile before reporting. The "±20%"
   tolerance is an account-specific baseline you set from a reconciled day, not
   a universal constant.
4. Compute daily CPL in the AD ACCOUNT timezone for both spend and leads.
5. Rows with unsubstituted `{{...}}` macros: exclude from performance analysis,
   then classify the cause — bots/crawlers, yes, but also a broken URL template,
   an unsupported/misspelled macro, or manual/direct traffic. Fix the template
   if it's yours before blaming traffic.

## Route references

| Need | Reference |
|---|---|
| Keitaro: key, report/build, measures, update_costs, postback/S2S, gotchas | `references/01-keitaro.md` |
| Binom: legacy URL-param + v2 REST, reports, cost, postback/S2S | `references/02-binom.md` |
| CPL math, funnel + anti-fraud metrics, cohort nowcasting, backend optimization contract (status→CAPI event), mapping, daily routine | `references/03-metrics-and-math.md` |

## Non-negotiables

- Work only on YOUR campaign IDs; every call carries a campaign filter. Other
  buyers' campaigns are read-never-touch.
- No cost push = no CPL/ROI (report cost is 0). Overwriting a period is safe
  (idempotent).
- API keys are write-once; store verbatim in gitignored notes.

<!-- Changelog 2026-08-11: Route table reflects postback/S2S, Binom's two API
surfaces, and anti-fraud metrics; softened Binom "leads" to ≈all. Compressed.
Peer-review (gpt): metric rule #1 reframed — "conversions inflation" is
integration-specific (overwrite-by-default; extra records only via distinct
tid), not an inherent 3.5-4x. Rule #3 ±20% labelled account-specific; rule #5
"unsubstituted macros" now = exclude-then-classify (not automatically bots). -->
