# Creative Diagnostics and Account Audits

Last reviewed: 2026-07-22

Use this reference for creative diagnosis, account-audit evidence collection, and Ads Manager CSV analysis. Metric names such as “hook rate” and “hold rate” are practitioner conventions, not standardized Meta performance thresholds.

## Contents

1. Metric contract
2. Creative diagnostic sequence
3. Diagnostic matrix
4. Account audit workflow
5. Ads Manager export schema
6. CSV analyzer
7. Scenario drills
8. Reporting template
9. Sources and gaps

## 1. Metric contract

Define every denominator in the report. Different tools use the same label for different formulas.

| Metric | Formula | What it can indicate | Main caveat |
|---|---|---|---|
| Hook/thumb-stop rate | `3-second video plays / impressions` | Whether the opening earns three seconds of attention | Practitioner metric; autoplay, placement, duration, and impression mix affect it |
| Hold rate | `ThruPlays / 3-second video plays` | Whether hooked viewers reach 15 seconds or completion for shorter videos | Some teams use 15-second views or impressions as denominator; never compare without formula |
| 25/50/75/100% retention | `video plays at depth / video starts or 3-second plays` | Where the narrative loses viewers | Video duration and placement must be comparable |
| Link CTR | `link clicks / impressions` | Ability to produce a link click | Does not prove click quality or landing-page arrival |
| Outbound CTR | `outbound clicks / impressions` | Clicks leaving Meta where the metric is available | Availability and definition vary by destination |
| Click-to-LPV rate | `landing page views / outbound clicks` for an external site; otherwise use the exact matching click type | Redirect, load, browser, and accidental-click loss | LPV measurement itself can be incomplete |
| LPV-to-result ratio | `selected Ads Manager results / landing page views` | A diagnostic handoff ratio | Not necessarily page CVR: results can include view-through or modeled attribution; use click-only or analytics/backend sessions for session CVR |
| CPA/CPL | `spend / business results` | Media cost per selected result | A raw lead or platform purchase may not equal the backend outcome |
| ROAS | `attributed conversion value / spend` | Platform-attributed revenue efficiency | Not contribution profit or incrementality |
| Frequency | `impressions / reach` at the chosen reporting level | Repeated exposure | Reach cannot be summed safely across overlapping rows |

Meta defines a ThruPlay as completion for videos shorter than 15 seconds or at least 15 seconds for longer video. No official universal hook- or hold-rate benchmark was found. Use account-relative cohorts with the same objective, placement, audience state, duration, and time period.

### Account-relative baseline protocol

1. Match objective/performance goal, optimization event, attribution setting, country, placement family, prospecting/retention role, offer/page, and video-duration band.
2. Sum raw numerators and denominators over a window that covers conversion lag and representative business days; never average daily row rates.
3. Compare the candidate with both the pooled baseline and its week/ad distribution so one outlier does not define “normal.”
4. Use attention metrics for screening and the business outcome plus guardrails for promotion.
5. Preserve a control or periodically rerun it so seasonality and auction change are not mistaken for creative lift.

## 2. Creative diagnostic sequence

Read the earliest broken stage:

```text
delivery share
  -> first-frame/3-second capture
  -> retention to message/proof
  -> link intent
  -> landing-page arrival
  -> conversion
  -> qualified/revenue outcome
```

1. Confirm that the ad received enough delivery for the intended decision. Low spend can be an allocation result, not evidence that the concept failed.
2. Check placement rendering, safe zones, sound-off comprehension, destination, and enabled creative enhancements.
3. Compare hook and retention against matched account cohorts, not public bands.
4. Compare link/outbound CTR and comment sentiment to determine whether attention became relevant intent.
5. Inspect click-to-LPV loss before blaming the offer.
6. Inspect page/form/checkout CVR and device errors before changing targeting.
7. Use qualified, paid, retained, or revenue outcomes to validate apparent media winners.

## 3. Diagnostic matrix

| Pattern | Likely hypotheses | First useful test | Do not conclude |
|---|---|---|---|
| Low hook, acceptable CPM | Opening frame, visual clarity, immediate relevance, placement crop | New first frame/hook on the same body and offer | The audience is wrong |
| High hook, low hold | Hook-body mismatch, slow proof, confusing story, duration | Shorter bridge to mechanism/proof; compare matched duration | The hook is the winner overall |
| High hold, low link CTR | Entertaining but weak product relevance, offer, CTA, or destination intent | Stronger product/offer connection and CTA | More watch time guarantees sales |
| High link CTR, low click-to-LPV | Slow page, redirects, consent layer, broken deep link, accidental clicks | Device/network QA and redirect/event audit | The creative is successful |
| Good LPV rate, low CVR | Message mismatch, price/offer, trust, form/checkout friction, availability | Page/offer test with stable traffic source | Meta targeting caused the entire loss |
| Good platform CPA, poor backend quality | Proxy optimization, spam, misleading promise, sales follow-up | Qualified/closed event feedback and creative/form qualification | Cheaper leads are better leads |
| Strong ad-level ROAS, weak incrementality | Existing-customer concentration, view-through credit, branded demand | New-customer split and lift/geo holdout | Attribution equals causal lift |
| Rising frequency and falling outcome | Creative fatigue, audience saturation, demand/seasonality, spend shift | Compare creative-level and audience-wide decline; introduce a materially new concept | A generic frequency threshold was crossed |

## 4. Account audit workflow

### A. Freeze the question

- Business goal and target economics.
- Date range and comparison range.
- Attribution setting, account time zone, and conversion delay.
- Selected reporting level: campaign, ad set, ad, or time series.
- Change log: budget, bid, event, audience, placement, creative, landing page, offer, tracking.

### B. Validate account state

- Delivery status at campaign, ad set, and ad.
- Billing, schedule, account limits, review/restriction, and disapprovals.
- Objective, conversion location, performance goal, event, bid strategy, and budget level.
- Special category, geography, age, placements, and rollout-dependent controls.

### C. Validate measurement

- Test event timing, value/currency, order or lead ID, and browser/server deduplication.
- UTMs with stable campaign/ad set/ad IDs.
- Meta versus analytics/CRM/backend reconciliation by event/order ID.
- Raw → contacted → qualified → booked/opportunity → paid/closed stages.
- Refund, cancellation, retention, IAP/IAA, or new-customer adjustments.

### D. Review history and decompose performance

Review Ads Manager Activity history so an edit is not mistaken for market or creative change. Analyze totals and distributions by campaign, ad set, ad, placement, country/region, device, age where permitted, day/week, and new versus returning customer. Require sufficient sample before interpreting a narrow breakdown.

### E. Rank hypotheses

For each hypothesis, record evidence, disconfirming evidence, expected mechanism, action, risk, success metric, stop condition, and review date. Separate a fact from a practitioner prior.

## 5. Ads Manager export schema

Export a stable English-language custom column view when possible. Do not mix campaign rows whose `Results` represent different actions. Preserve raw counts and recompute weighted rates; never average row-level CTR, CPA, ROAS, CVR, or frequency.

Create separate fact files when the audit needs time and placement analysis:

1. an unbroken totals export for reconciliation;
2. a daily breakdown for trend/edit/fatigue analysis;
3. a publisher-platform and placement breakdown for delivery-quality analysis.

Do not join breakdown files in a way that multiplies spend or actions, and do not sum reach across rows.

### Identity and configuration

- Reporting starts/ends
- Campaign name and ID
- Ad set name and ID
- Ad name and ID
- Objective, buying type, attribution setting where exportable
- Delivery status and bid strategy where exportable

### Delivery and cost

- Amount spent and account currency
- Impressions, reach, frequency
- CPM
- Link clicks, outbound clicks, landing page views
- Link/outbound CTR and CPC

### Video creative

- 3-second video plays
- ThruPlays
- Video plays at 25%, 50%, 75%, and 100%
- Average video play time where available

### Business outcomes

- One explicitly named result column, not an unexplained mixed `Results`
- Cost per selected result
- Conversion value and ROAS when valid
- Backend-qualified/paid/closed result joined by stable IDs outside Ads Manager

### Context joins

- Creative concept, angle, hook, format, duration, creator, offer, and landing-page version
- Campaign/ad set/ad IDs in analytics and CRM
- New/returning customer and gross/contribution margin where available
- Edit log and experiment cell

## 6. CSV analyzer

The skill includes `scripts/analyze_ads_export.py`. It uses the Python standard library and applies no benchmark thresholds.

```bash
python3 scripts/analyze_ads_export.py export.csv \
  --result-column "Purchases" \
  --value-column "Purchase conversion value" \
  --top 20 > audit-summary.md
```

For lead generation, pass a joined column such as `Qualified leads` or `Closed won` after enriching the export with CRM outcomes. Use `--name-column` when the desired entity is not auto-detected.

The analyzer calculates weighted totals and top-spend rows for CPM, outbound/link CTR, CPC, click-to-LPV, LPV-to-selected-result ratio, CPA, ROAS, hook rate, and hold rate. It intentionally:

- requires an explicit business-result column for CPA/CVR;
- does not sum reach or infer cross-row frequency;
- does not label a metric good or bad;
- does not claim causal significance;
- warns when key columns are absent.

For a true landing-page CVR, use click-only conversion data or join analytics/backend converted sessions. Do not interpret an Ads Manager purchase-to-LPV ratio as session CVR when view-through or modeled results are included.

## 7. Scenario drills

### 1. Cheap CTR, expensive purchase

**Data:** CPM and CTR improved; click-to-LPV stable; LPV CVR fell; refunds rose.
**Diagnosis:** creative expanded click volume by changing the promise or buyer mix, while the page/product economics worsened.
**Action:** compare promise/offer, device, new-customer share, paid orders, and refunds. Do not call the creative a winner from CPC.

### 2. Video “winner” receives most spend

**Data:** one ad has best CPA and most spend; challengers have little delivery.
**Diagnosis:** allocation and selection are confounded.
**Action:** treat the result as an operational winner; use an overlap-free experiment if the causal creative difference matters.

### 3. Strong hook, weak body

**Data:** hook rate above the matched cohort; hold rate and link CTR below it.
**Diagnosis:** pattern interrupt works, but message/proof does not earn continued attention or intent.
**Action:** keep the opening treatment, replace the bridge/mechanism, and test against the same offer and duration.

### 4. Weak hook, strong conversion among clickers

**Data:** low hook and CTR; click-to-LPV and page CVR strong.
**Diagnosis:** downstream offer works for a small self-selected group; reach/attention is the constraint.
**Action:** create clearer variants of the same proposition before changing the page.

### 5. Instant-form CPL falls, sales do not rise

**Data:** raw CPL halves; contact and qualified rates fall; closed CAC rises.
**Diagnosis:** the campaign optimized form completion, while form friction or promise quality changed buyer intent.
**Action:** restore qualification, audit response time, and feed qualified/closed events where appropriate.

### 6. Meta ROAS rises after CAPI launch

**Data:** Meta-attributed purchases rise; backend orders are flat; browser/server duplicates appear.
**Diagnosis:** measurement coverage or duplication changed, not necessarily demand.
**Action:** reconcile event/order IDs and deduplication before claiming performance lift.

### 7. App CPI falls, D7 value falls faster

**Data:** install volume rises and CPI falls; activation, retention, and D7 ROAS decline.
**Diagnosis:** optimization found cheaper installers rather than valuable users.
**Action:** test a downstream activation/value event and keep cohort payback as the guardrail.

### 8. High-AOV campaign looks inefficient after one week

**Data:** spend matures faster than purchases; assisted and delayed orders appear later.
**Diagnosis:** evaluation window is shorter than the purchase-lag distribution.
**Action:** define the post-treatment window from observed lag and use a lift/geo design when the investment decision is material.

## 8. Reporting template

```text
Business question and target economics:
Date range, comparison range, attribution, time zone:
Data sources and known gaps:
Earliest broken funnel stage:
Creative-level observation:
Backend/CRM/app-cohort observation:
Ranked hypotheses with evidence labels:
Recommended action and mechanism:
Test design and primary metric:
Guardrails and stop/rollback condition:
Decision date after conversion lag:
What requires live-account or country-policy verification:
```

## 9. Sources and gaps

- Official Meta creative overview: https://www.facebook.com/business/ads/ad-creative
- Official Meta Reels creative page, including split-test scope: https://www.facebook.com/business/ads/facebook-instagram-reels-ads
- Official Meta awareness/video-view definitions: https://www.facebook.com/business/ads/ad-objectives/awareness
- Official Meta traffic objective and LPV context: https://www.facebook.com/business/ads/ad-objectives/traffic
- Official Meta delivery-status guidance: https://www.facebook.com/help/messenger-app/650774041651557/
- Official Meta Ads Manager levels and rollout caveats: https://www.facebook.com/help/messenger-app/621956575422138/
- Official Meta Activity history: https://www.facebook.com/help/messenger-app/289211751238030
- Practitioner formula reference for hook/hold definitions: https://win.varos.com/en/articles/8055146-how-video-facebook-ads-benchmark-metrics-are-calculated

Gaps: Meta does not publish universal hook/hold benchmarks. Export labels vary by locale, objective, account rollout, and reporting level. Public exports do not contain all configuration history or backend outcome quality; join those separately and preserve privacy controls.
