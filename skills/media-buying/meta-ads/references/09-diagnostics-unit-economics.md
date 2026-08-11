# Diagnostics, Unit Economics, and Test Design

Last reviewed: 2026-07-22

Use this reference to turn a vague performance problem into a measurable diagnosis. The sequence is: validate measurement, locate the funnel constraint, compare against account-specific economics, then design the smallest useful intervention.

## 1. Minimum intake

Collect what is available before recommending structure, budgets, or kill rules:

| Area | Required context |
|---|---|
| Outcome | Business goal, conversion definition, revenue or qualified-lead outcome |
| Economics | Price/AOV, refunds, discounts, taxes, fulfillment, payment fees, variable cost, gross or contribution margin |
| Funnel | Impression → click → landing-page view → lead/cart → qualified lead/checkout → purchase/closed sale |
| Delivery | Market, objective, performance goal, optimization event, attribution setting, placements, audience controls |
| Measurement | Pixel/dataset, CAPI or CRM ingestion, deduplication, UTMs, analytics, backend source of truth |
| History | Spend, dates, CPM, CTR, CPC, click-to-LPV rate, CVR, CPA/CPL, ROAS, frequency, reach, qualified rate |
| Constraints | Policy category, geography, age, inventory, sales capacity, privacy/consent, creative and landing-page limits |

If inputs are missing, separate facts from assumptions and request only the variables that would change the decision.

## 2. Unit economics

Derive targets from contribution margin (standard break-even math assumed). The non-obvious disciplines:

- Don't treat aspirational LTV as allowable CAC. If you count repeat purchases, state the observation window, retention evidence, discount rate, and cash-flow constraint.
- Lead gen: allowable raw-lead CPL = max CAC × raw→qualified rate × qualified→customer rate; optimize against qualified/closed outcomes when volume and data flow allow, not raw-lead count.

## 3. Metric decomposition

Decompose CPA to locate the constraint (CPM → link CTR → click-to-LPV → CVR), and judge each factor against a comparable account baseline — level AND change, not one blended number.

## 4. Symptom-first diagnostic tree

| Symptom | First checks | Likely constraint classes | Useful next test or action |
|---|---|---|---|
| No or very low spend | Delivery status, schedule, payment, policy, audience size, bid/cost controls, event eligibility | Account/policy issue, overly restrictive controls, bid constraint, fragmented setup | Resolve blocking status; broaden one constraint at a time; verify optimization event |
| CPM increased | Auction seasonality, market, audience saturation, placements, quality ranking, spend change | Auction pressure, constrained audience, creative quality, placement mix | Compare breakdowns and prior periods; test broader eligible delivery or new concepts |
| Low link CTR | Hook, message-market match, visual clarity, offer, placement crop | Creative or offer problem | Test materially different concepts; inspect placement-level delivery and comments |
| High CPC with acceptable CPM | Link CTR and click intent | Creative/offer or unclear CTA | Improve the promise, proof, and CTA; do not start with audience micro-targeting |
| Large click-to-LPV loss | Page speed, redirects, consent layer, broken URL, in-app browser, accidental clicks | Technical funnel or low-intent click problem | Test on real devices/connections; inspect analytics events and redirect chain |
| Low landing-page CVR | Message continuity, load speed, trust, price, form/checkout friction, device errors | Offer, page, or checkout problem | Session/device QA; isolate landing page or offer with a controlled test |
| Cheap leads, poor sales | Lead definition, form friction, incentive, geo, spam, response time, CRM routing | Qualification and sales-process problem | Feed qualified/closed stages back; tighten questions; audit follow-up SLA |
| Meta conversions exceed backend | Attribution windows, view-through credit, duplicate events, refunds, time zones | Definition or attribution mismatch | Reconcile by event ID/order ID and conversion date; audit deduplication |
| Backend exceeds Meta | Consent loss, event failure, missing identifiers, unsupported browser/server flow | Coverage or match problem | Review Diagnostics, event coverage, EMQ inputs, and CAPI delivery |
| Performance fell after edit | Edit log, delivery status, spend allocation, creative distribution, conversion lag | Learning/reallocation, demand change, coincident external factor | Compare pre/post cohorts and breakdowns; revert only when evidence supports causality |

Do not diagnose from one blended metric. Break down by time, placement, geography, device, age where allowed, creative, landing page, and new versus returning customer when the sample is sufficient.

## 5. Measurement validation

Before optimizing media:

1. Confirm the intended event fires once at the correct business moment.
2. Validate `value`, `currency`, item/order identifiers, and event time.
3. Confirm browser/server deduplication with matching `event_name` and `event_id` where both routes are used.
4. Test UTMs and stable entity IDs through redirects into analytics and the backend.
5. Reconcile a sample of event IDs or order IDs across Meta, analytics, CRM, and backend.
6. Record attribution window, time zone, and whether reports use impression time or conversion time.
7. Monitor sudden changes in event coverage, matched events, duplicates, and qualified-outcome imports.

Choose a source of truth per decision. Meta is useful for delivery optimization and platform-attributed outcomes; the backend is authoritative for paid, refunded, qualified, and closed business results.

## 6. Test design

Generic experiment hygiene assumed; the decisions that are Meta/vertical-specific:

- Allocation: randomized Meta Experiments when causal confidence matters; parallel/operational splits are directional SCREENING only (audiences overlap, auction differs) — route causal reads to the measurement layer.
- Window ≥ the conversion lag; judge on the click-date cohort (tracker-ops), not conversion-date volume mid-lag.

## 7. Stop, scale, and rollback logic

- Treat practitioner rules such as fixed days, fixed event counts, “3× CPA,” or fixed budget-edit percentages as optional priors to validate.
- Stop immediately for policy violations, broken tracking, wrong geography, incorrect offer, runaway spend, or a damaged funnel.
- For normal variance, wait for the pre-specified evidence threshold and observed conversion lag.
- Scale while marginal results remain acceptable; blended historical ROAS can hide deteriorating marginal economics.
- Keep an edit log and define a rollback condition before high-impact changes.

## 8. Reporting contract

A useful audit or recommendation should state:

1. Observed facts and date range.
2. Data-quality limitations and attribution settings.
3. Unit-economic target and assumptions.
4. Funnel location of the primary constraint.
5. Ranked hypotheses with evidence labels.
6. Recommended action, expected mechanism, and risk.
7. Test design, success metric, stop condition, and review date.
8. What must be verified in the live account because availability or policy is rollout-dependent.
