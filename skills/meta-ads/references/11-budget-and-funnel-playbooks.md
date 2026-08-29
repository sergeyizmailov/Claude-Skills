# Budget and Funnel Playbooks

Last reviewed: 2026-07-22

This reference turns business constraints into an operating plan. It does not define small, medium, or large budgets in currency: the same amount can support a strong test in one market and produce almost no decision-quality data in another.

## Contents

1. Budget tiers by decision capacity
2. Portfolio allocation
3. E-commerce playbook
4. Local lead-generation playbook
5. SaaS and B2B playbook
6. Mobile-app playbook
7. Test backlog and operating cadence
8. Post-mortem template
9. Sources and gaps

## 1. Budget tiers by decision capacity

Start with contribution economics and an account-specific expected CPA/CPL range (conservative + optimistic scenarios). Budget capacity in decision terms = how many results the test buys ÷ results needed per cell.

`results_required_per_cell` is not a universal Meta threshold. Derive it from the baseline rate, minimum effect worth acting on, desired confidence, conversion delay, and acceptable loss. If those inputs are unknown, pilot to estimate them and call the result directional.

| Tier | Operational definition | Appropriate design | Avoid |
|---|---|---|---|
| **Constrained** | The budget cannot support more than one useful decision cell at the target outcome | One consolidated delivery cell; screen materially different creative; validate measurement and funnel | Parallel audience, placement, bid, and creative tests; pretending each under-delivered ad is a completed test |
| **Controlled** | The budget supports a limited holdout or a small number of adequately funded cells | One primary experiment plus business-as-usual delivery; rotate the next question only after the current read | Simultaneously changing offer, page, audience, bid, and creative; scaling from attributed ROAS alone |
| **Portfolio** | The budget supports simultaneous prospecting, lifecycle, and powered experiments without starving the business-as-usual baseline | Separate exploration, validated delivery, and incrementality cells; geo or conversion-lift tests where appropriate | Assuming scale makes platform attribution causal; ignoring marginal CPA and saturation |

The tier can change by country, season, objective, or conversion event without the currency budget changing.

## 2. Portfolio allocation

Allocate by jobs, not by a fixed percentage:

1. **Business-as-usual baseline** — the best current delivery configuration.
2. **Exploration** — concepts, offers, pages, or event-quality improvements whose result can change a decision.
3. **Validation** — randomized A/B, conversion lift, or geo holdout for material claims.
4. **Lifecycle/retention** — only where the message and economics differ from acquisition.
5. **Measurement reserve** — engineering, creative production, CRM feedback, and analysis are part of acquisition cost even though they do not appear as media spend.

Do not hard-code a `70/20/10` or similar split. Fund the baseline to protect current economics, then fund the highest-value uncertainty. A constrained account may have one combined campaign and a sequential creative queue; a portfolio account may maintain several independent test cells.

## 3. E-commerce playbook

### Required inputs

- Net AOV, contribution margin, refunds/returns, discounts, payment and fulfillment cost.
- New versus returning customer value and repeat-purchase observation window.
- Purchase event accuracy, value/currency, order ID, browser/server deduplication.
- Checkout and payment success by device; inventory and geographic availability.

### Launch or repair sequence

1. Calculate break-even and target purchase CPA from contribution, not revenue.
2. Reconcile a sample of order IDs across Meta, analytics, and backend.
3. Use Sales with the closest reliable purchase/value outcome for the actual conversion location.
4. Consolidate redundant prospecting cells; preserve a distinct retention cell only when offer or eligibility requires it.
5. Test concept and offer continuity before targeting micro-segments.
6. Read CPM → link CTR → click-to-LPV → checkout CVR → paid/refunded purchase CPA.
7. Scale on marginal new-customer contribution and inventory capacity; use a lift design when incrementality changes the investment decision.

### Common wrong and better decisions

| Observation | Wrong decision | Better decision |
|---|---|---|
| High attributed ROAS, weak new-customer revenue | Scale because platform ROAS is above target | Separate new/returning customers and test incremental new-customer revenue |
| Strong CTR, weak purchase CVR | Replace audiences | Check message/price continuity, mobile checkout, stock, delivery terms, and event accuracy |
| Cheap AddToCart, weak purchases | Optimize permanently for AddToCart | Repair checkout/measurement and move toward the business outcome when data supports it |
| Good first-week CPA on a high-AOV product | Declare the final economics | Use the observed purchase-lag distribution and mature delayed conversions |

## 4. Local lead-generation playbook

### Required inputs

- Service radius, excluded areas, opening hours, capacity, and response SLA.
- Raw lead, contacted lead, qualified lead, appointment, show, sale, and revenue definitions.
- Close rate by lead source and cohort; no-show, cancellation, spam, and duplicate rates.
- Maximum customer CAC and resulting maximum qualified/raw CPL.

### Launch or repair sequence

1. Enforce serviceability in supported geo controls, creative, form, and downstream address validation.
2. Choose website form, instant form, messaging, or calls based on qualification and follow-up workflow—not CPL alone.
3. Add enough qualification friction to protect sales capacity without suppressing every viable lead.
4. Route leads immediately, record first-contact latency, and deduplicate phone/email.
5. Send qualified and closed stages back through supported CRM/CAPI flows when volume, consent, and data quality allow.
6. Compare campaigns on cost per contacted, qualified, booked, shown, and closed outcome.
7. Diagnose poor quality by geography, creative promise, form answers, time of day, placement, and sales follow-up before narrowing interests.

### Common wrong and better decisions

| Observation | Wrong decision | Better decision |
|---|---|---|
| Instant-form CPL is half the website CPL | Move all budget to instant forms | Compare qualified and closed CAC, response time, spam, and sales capacity |
| Good lead volume, few appointments | Blame targeting | Audit contact latency, routing, scripts, qualification, availability, and duplicate leads |
| Leads outside the service area | Search for the retired residents-only selector | Use supported geo inputs and validate postcode/address in the form or booking flow |
| Cheap calls but low revenue | Optimize for call initiation | Measure connected/qualified calls and downstream sales where supported |

## 5. SaaS and B2B playbook

### Required inputs

- ICP, disqualifiers, contract value, gross margin, sales-cycle length, stage conversion, and pipeline capacity.
- Difference between content leads, product sign-ups, qualified meetings, opportunities, and closed-won revenue.
- CRM identity and stage timestamps; opportunity value and offline/CAPI event plan.

### Launch or repair sequence

1. Define the business event: qualified meeting, activated workspace, sales-qualified opportunity, or another stage with economic meaning.
2. Map lead-to-stage conversion and derive allowable CPL backward from maximum CAC.
3. Match offer to intent: educational asset, diagnostic, demo, trial, or direct sales conversation.
4. Use creative to identify the problem, role, proof, and disqualifier; do not rely on job-title targeting alone.
5. Reconcile cohort pipeline by campaign/ad and sales-stage date; preserve the long conversion lag.
6. Feed qualified stages and values back when event volume and privacy rules permit.
7. Evaluate pipeline/revenue lift before scaling a cheap top-of-funnel lead source.

### Common wrong and better decisions

| Observation | Wrong decision | Better decision |
|---|---|---|
| Low content-download CPL | Treat downloads as pipeline | Track qualified meeting, opportunity, and closed-won rates by cohort |
| Narrow job-title audience has high CPM | Add more adjacent interests | Test broader delivery with ICP-specific creative and form qualification |
| Few closed-won outcomes during the media window | Optimize daily on platform CPA | Use leading stages with known stage-to-revenue value and mature cohorts separately |
| Demo page converts poorly | Increase retargeting frequency | Check offer/ICP fit, proof, scheduling friction, and sales availability |

## 6. Mobile-app playbook

### Required inputs

- OS and country mix; Meta SDK/CAPI or MMP configuration; ATT, SKAN/AEM, and attribution settings.
- Install, activation, retention, subscription/purchase, ad-revenue, refund, and cohort-LTV definitions.
- IAP versus IAA monetization; payback horizon and fraud filtering.

### Launch or repair sequence

1. Validate event names, value, currency, deduplication, and MMP/backend reconciliation.
2. Establish install-to-activation and activation-to-value funnels by OS, country, and cohort.
3. Optimize toward the deepest reliable event that represents the business model; retain downstream guardrails if an upstream proxy is necessary.
4. For hybrid apps, keep IAA and IAP value definitions explicit and test whether one optimization path cannibalizes the other.
5. Test creative concepts using both media outcomes and D1/D7/D30 quality.
6. Compare automated and manual approaches with fixed market, creative, event, total spend, and cohort window where possible.
7. Scale on cohort contribution/payback, not CPI alone.

### Common wrong and better decisions

| Observation | Wrong decision | Better decision |
|---|---|---|
| CPI falls sharply | Scale immediately | Check activation, retention, payer/ad-revenue value, fraud, and cohort payback |
| Purchase count rises | Assume total app value rose | Check purchase value, IAA value, retention, and cannibalization |
| Meta and MMP differ | Pick the larger number | Reconcile attribution rules, event time, consent, deduplication, and SKAN/AEM coverage |
| Creative wins on install CTR | Promote it as the control | Require a downstream quality guardrail for the same install cohort |

## 7. Test backlog and operating cadence

Maintain a ranked backlog with these fields:

| Field | Meaning |
|---|---|
| Decision | What changes if the result is positive, negative, or inconclusive |
| Constraint | Current earliest broken funnel stage |
| Hypothesis | Mechanism that should move the outcome |
| Treatment | One material variable or a clearly defined package |
| Primary metric | Business-aligned decision metric |
| Guardrails | Quality, policy, spend, refund, retention, or sales-capacity limits |
| Evidence requirement | Directional screen, randomized A/B, conversion lift, or geo holdout |
| Minimum data | Baseline, MDE, confidence, lag, and acceptable loss assumptions |
| Owner and date | Who acts and when the result matures |

Do not use a calendar cadence such as “three new creatives every week” without reference to spend and delivery. The operating cadence should keep the next useful candidate ready before the current control deteriorates while avoiding a queue too large to receive meaningful delivery.

## 8. Post-mortem template

```text
Decision being tested:
Business and account context:
Economics and target:
Treatment and counterfactual:
Dates, attribution, and conversion-lag window:
Primary metric and guardrails:
Observed funnel movement:
Backend/CRM outcome:
What changed besides the intended variable:
Result: positive / negative / inconclusive / invalid
Mechanism supported or rejected:
What would reproduce or falsify the conclusion:
Next action and rollback condition:
Transfer limits: country, objective, placement, audience, season, scale
```

An invalid or inconclusive test is not a losing ad. Record why the design could not answer the question—tracking failure, overlap, unequal spend, offer change, insufficient sample, conversion lag, or external demand shock—so the same mistake is not repeated.

## 9. Sources and gaps

- Official Meta budget guidance: https://www.facebook.com/business/ads/pricing
- Official Meta auction overview: https://www.facebook.com/business/ads/ad-auction
- Official Meta campaign-level structure: https://www.facebook.com/help/messenger-app/621956575422138/
- Official Meta Conversions API overview: https://www.facebook.com/business/help/AboutConversionsAPI
- Official Meta Advantage+ leads guidance and CRM quality-loop aggregates: https://www.facebook.com/business/ads/meta-advantage-plus/leads
- Official Meta Advantage+ app overview: https://www.facebook.com/business/ads/meta-advantage-plus/app-campaigns

Gaps: public sources do not provide a universal sample-size rule, currency budget tier, or result volume that guarantees a stable decision. Power calculations require account-specific baselines. Country-level prices, sales processes, app attribution, and regulated-category controls remain volatile.
