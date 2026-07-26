# Practical Meta Ads Case Library

Last reviewed: 2026-07-22

This library adds operational pattern recognition without converting published case-study lifts into benchmarks. Match a case by mechanism, measurement design, business model, conversion lag, and outcome definition—not by headline percentage.

## Contents

1. How to use the cases
2. E-commerce and omnichannel cases
3. Mobile-app cases
4. Local and service lead-generation cases
5. B2B/SaaS cases
6. Cross-case post-mortem patterns
7. Source and evidence limitations

## 1. How to use the cases

For each case:

1. Identify the original constraint and the business outcome.
2. Check whether the reported comparison was causal, directional, or merely attributed.
3. Compare country, funnel, value model, conversion delay, event volume, and sales process with the current account.
4. Reuse the decision rule, not the reported lift.
5. State what would invalidate transfer to the current account.

### Proof grades

| Grade | Meaning |
|---|---|
| **A — causal design reported** | Concurrent randomized, conversion-lift, or geo-holdout design identifies a treatment and counterfactual. Publication may still be an interested-party source without raw data or independent audit. |
| **B — structured comparison** | A comparator exists, but allocation, power, timing, or other material design details are missing. |
| **C — attributed/pre-post case** | No interpretable counterfactual; useful only as a hypothesis or implementation example. |

No case below is an independently audited universal performance claim.

## 2. E-commerce and omnichannel cases

### Case 1 — Mejuri: attributed revenue was not enough; new-customer incrementality became the KPI

- **Context:** US DMA test for a global DTC jewelry brand. Existing Meta activity generated revenue but missed incremental-ROAS goals and concentrated on people already familiar with the brand.
- **Change:** Allocate 25% of Meta budget to upper-funnel acquisition and measure new-customer revenue.
- **Reported result:** Initial 11% incremental-revenue lift; a later read reported 12.9% incremental-sales lift and 57% iROAS improvement.
- **Design:** 70% treatment / 30% geo holdout, three-week treatment plus post-treatment observation.
- **Failure/limitation:** Vendor-authored case, no raw data or confidence interval, and inconsistent description of the post-treatment window.
- **Expert decision:** When platform revenue is concentrated among existing/high-awareness buyers, test incremental new-customer revenue rather than scaling from blended attributed ROAS.
- **Wrong takeaway:** “Move 25% to upper funnel” is not portable; the share was this test's treatment.
- **Proof/source:** **A**, measurement-vendor case: https://www.haus.io/case-studies/how-mejuri-discovered-what-was-really-driving-sales

### Case 2 — HexClad: a short test misread a long-consideration product

- **Context:** US premium cookware sold through Shopify and Amazon; flagship bundle price around $700.
- **Change:** Compare business-as-usual spend, increased spend, and no Meta ads; include both sales channels and observe delayed orders.
- **Reported result:** After three additional observation weeks, measured cost per incremental acquisition was 56% lower in the BAU cell and 67% lower in the increased-spend cell than in the initial two-week read.
- **Design:** Three-cell matched-geo holdout with two-week treatment and three-week post-treatment observation.
- **Failure/limitation:** Spend multiplier, absolute orders/CPIA, matching diagnostics, and confidence were undisclosed.
- **Expert decision:** Derive the test and post-treatment windows from observed purchase lag before declaring high-AOV media inefficient.
- **Wrong takeaway:** The published percentage does not define a universal waiting period or scaling rate.
- **Proof/source:** **A**, measurement-vendor case: https://www.haus.io/customer/hexclad

### Case 3 — DSW: online-only optimization omitted store value

- **Context:** US footwear retailer with meaningful store purchases influenced by Meta.
- **Change:** Join POS/offline events, simplify structure, and compare omnichannel optimization with online-only business-as-usual.
- **Reported result:** One result block reports 23% more omnichannel purchases, 16% revenue lift, and 29% lower incremental CPA; another reports 15% higher ROAS and 18% lower omnichannel CPA.
- **Design:** Agency-reported Meta conversion-lift test with 30% no-ad holdout; exact cell relationship is unclear.
- **Failure/limitation:** Conflicting metric blocks, no dates/spend/confidence, and several interventions bundled together.
- **Expert decision:** When offline sales matter, feed them into measurement and optimization, then separate incremental results from attributed BAU results.
- **Wrong takeaway:** Do not repeat either headline number without resolving its definition.
- **Proof/source:** **A-/B+**, participating-agency case: https://tinuiti.com/work/paid-social-case-study-dsw-meta/

### Case 4 — The Athlete's Foot: a lift headline used an undefined AddToCart “ROAS”

- **Context:** Sneaker retailer in Mexico/Latin America increasing Advantage+ shopping investment.
- **Change:** Bundle higher automation investment, catalog/product diversity, offer/CTA treatment, and prospecting/retargeting delivery.
- **Reported result:** Case reports 165% incremental “ROAS” on AddToCart, 15% more conversions, 16.2x attributed AddToCart “ROAS,” and 1.79x incremental ROAS.
- **Design:** Claimed Meta Conversion Lift comparison with BAU; allocation, spend equality, window, and confidence are absent.
- **Failure/limitation:** AddToCart value is not realized revenue unless a validated value model is defined; the treatment changed several variables.
- **Expert decision:** Require purchase/revenue outcome, equalized total spend, and a defined value field before using a lift result to scale.
- **Wrong takeaway:** A large platform number does not rescue an undefined business metric.
- **Proof/source:** **B**, Meta-partner agency case: https://www.adsmurai.com/en/case-studies/taf-meta

## 3. Mobile-app cases

### Case 5 — Blibli.com: strong app-install/ROAS claims without a disclosed counterfactual

- **Context:** Indonesian e-commerce app using always-on Advantage+ app acquisition.
- **Change:** Launch automated app campaigns to increase installs and purchases.
- **Reported result:** 34% install lift, 2.4x purchase lift, and 32.4x ROAS.
- **Design:** Not disclosed; the guide does not identify baseline, control, attribution, MMP, duration, or confidence.
- **Failure/limitation:** Absolute platform ROAS appears beside relative lifts, and cohort quality is absent.
- **Expert decision:** Treat the case as a hypothesis; compare against the current setup using the same events/creative/market and graduate on MMP/backend purchase value.
- **Wrong takeaway:** Do not use 32.4x as an app benchmark.
- **Proof/source:** **C**, Meta marketing guide: https://d3m889aznlr23d.cloudfront.net/img/events/458773316/assets/c973d989.maximize-your-customer-engagement--through-apps-with-advantage-app-campaigns--leave-behind_en_us.pdf

### Case 6 — Sephora Singapore: CPI improved, but downstream value was not reported

- **Context:** Singapore beauty-retail app comparing Advantage+ app with manual install ads.
- **Change:** Run automated and manual acquisition approaches alongside each other.
- **Reported result:** 23% higher reach, 45% more installs, and 43% lower CPI for Advantage+.
- **Design:** Comparative test implied; budgets, overlap control, duration, attribution, and confidence undisclosed.
- **Failure/limitation:** Activation, purchases, retention, and LTV were not reported.
- **Expert decision:** Use CPI as a screen, then require D7/D30 activation or value guardrails before shifting material budget.
- **Wrong takeaway:** Cheaper installs are not automatically better users.
- **Proof/source:** **B-/C+**, Meta marketing guide: https://d3m889aznlr23d.cloudfront.net/img/events/458773316/assets/c973d989.maximize-your-customer-engagement--through-apps-with-advantage-app-campaigns--leave-behind_en_us.pdf

### Case 7 — Century Games: downstream value optimization beat an install comparator

- **Context:** Global mobile-game developer seeking purchasers rather than installs.
- **Change:** Compare Advantage+ value optimization with manual app-install acquisition.
- **Reported result:** 70% more purchases, 50% lower cost per purchase, and 65% higher ROAS.
- **Design:** Comparator reported, but no randomization, equal-spend control, title/market, cohort horizon, or MMP detail.
- **Failure/limitation:** Automation and optimization goal changed together, so their effects cannot be separated.
- **Expert decision:** When event volume supports it, test purchase/value optimization while holding market, spend, and creative constant; decide on cohort ROAS.
- **Wrong takeaway:** The case does not prove that every install campaign should switch immediately.
- **Proof/source:** **B-/C+**, Meta marketing guide: https://d3m889aznlr23d.cloudfront.net/img/events/458773316/assets/c973d989.maximize-your-customer-engagement--through-apps-with-advantage-app-campaigns--leave-behind_en_us.pdf

### Case 8 — Supersonic from Unity: purchase-biased optimization missed ad-revenue users

- **Context:** Global hybrid-monetized games with both in-app-ad and in-app-purchase revenue.
- **Change:** Feed impression-level ad revenue through AppsFlyer ROI360 and optimize IAA separately from IAP users.
- **Reported result:** One title reported 42% higher D7 ROAS; another reported 4x installs. Within six months the new campaign type reached 53% of Meta spend.
- **Design:** Vendor-reported campaign comparison/portfolio rollout, not a disclosed randomized experiment.
- **Failure/limitation:** Results came from different games; test dates, attribution, control, and cannibalization effect size were absent.
- **Expert decision:** For hybrid apps, send and optimize separate IAA/IAP values, then require fixed-title/market cohort ROAS and non-cannibalization.
- **Wrong takeaway:** Portfolio adoption and total revenue growth do not establish causality.
- **Proof/source:** **C**, AppsFlyer customer case: https://www.appsflyer.com/customers/supersonic-unity/

## 4. Local and service lead-generation cases

### Case 9 — TECOBI/Medved Auto: CRM purchase intent beat raw-lead optimization

- **Context:** Colorado auto-dealer lead ads followed by SMS, sales calls, and CRM purchase-intent/purchase stages.
- **Change:** A/B test lead-volume optimization against conversion-leads optimization using CRM Conversions API feedback.
- **Reported result:** 68% higher conversion rate and 8% lower cost per qualified lead.
- **Design:** Explicit two-cell A/B test; sample, allocation, significance, and the exact “qualified” definition are absent.
- **Failure/limitation:** Previous optimization rewarded form volume rather than likely buyers.
- **Expert decision:** Keep capture/follow-up constant and test the earliest reliable CRM event that separates buyers from form fillers.
- **Wrong takeaway:** The case does not define a universal qualified-lead event or expected lift.
- **Proof/source:** **A**, official Meta CRM guide plus advertiser corroboration: https://digiday.com/wp-content/uploads/2022/03/META_Guide-to-CRM_032222.pdf and https://www.tecobi.com/blog/how-social-media-advertising-can-save-your-dealership-in-the-post-pandemic-auto-market/

### Case 10 — Top Business Class: the sale required a call, so the test added a call path

- **Context:** Premium-flight agency whose negotiated tickets close with a representative.
- **Change:** Test business-as-usual mobile campaign against the same setup plus a call add-on.
- **Reported result:** 22% more qualified leads and 24% lower cost per incremental qualified lead.
- **Design:** Two-week Meta conversion-lift study.
- **Failure/limitation:** No budget, sample, confidence, completed-ticket revenue, or explicit qualification rule; desktop excluded.
- **Expert decision:** When a live conversation is an unavoidable close step, measure connected/qualified calls or bookings—not call-button taps.
- **Wrong takeaway:** The case does not establish that calls beat forms for other sales motions.
- **Proof/source:** **A**, original agency plus Meta lift material: https://www.jumpfly.com/case-studies/top-business-class-2/ and https://about.fb.com/ltam/wp-content/uploads/sites/14/2023/11/LeadGenerationGuide.pdf

### Case 11 — Ortner's Resort: native lead capture worked as part of a nurture system

- **Context:** German hospitality advertiser moving native form leads through email nurture to inquiry and booking.
- **Change:** Native lead form with a voucher plus automated pre-/post-booking nurture versus website-directed ads; multiple creative cells also reported.
- **Reported result:** 3.7x qualified leads, 62% lower CPL, 206% more booking inquiries, and 50% more final bookings.
- **Design:** Meta-published comparison, but destination randomization, allocation, dates, and booking attribution are unclear.
- **Failure/limitation:** Offer, friction, creative, and nurture changed together; no booking value or incrementality.
- **Expert decision:** Judge native forms as a capture-and-nurture system reaching bookings, not as a CPL tactic.
- **Wrong takeaway:** The form surface alone cannot be credited with the reported outcome.
- **Proof/source:** **A-**, advertiser/Meta case: https://www.additive.eu/en/articles/meta-facebook-co-pulished-success-story-with-additive-successful-lead-generation-in-the-hotel-industry

### Case 12 — SumUp: one eligibility question corrected high-volume, low-fit leads

- **Context:** European payment provider receiving many lead-form submissions from people who were not business owners.
- **Change:** A/B test a lead-filtering question: “Are you a business owner?”
- **Reported result:** 4x lower CPL after qualification/filtering.
- **Design:** Meta-reported A/B test; sample, allocation, significance, eligible-lead count, and downstream revenue absent.
- **Failure/limitation:** Published outcome remains CPL; “quality” is only the binary eligibility gate.
- **Expert decision:** Test one high-information disqualifier before adding a long questionnaire; compare cost per eligible lead and downstream CAC.
- **Wrong takeaway:** More form friction is not always better.
- **Proof/source:** **A-**, official Meta lead guide: https://about.fb.com/ltam/wp-content/uploads/sites/14/2023/11/LeadGenerationGuide.pdf

### Case 13 — Mira Clinic: CRM conversion-lead optimization improved a local-service lead metric

- **Context:** Turkish cosmetic dentistry/plastic-surgery clinic using testimonial video, instant form, and CRM stages.
- **Change:** A/B test standard lead optimization against conversion-leads optimization connected through CRM CAPI.
- **Reported result:** 48% more “quality leads” and 36% lower cost per lead.
- **Design:** Meta-reported A/B test; budget, event volume, confidence, and exact CRM event not public.
- **Failure/limitation:** “Quality lead” is undefined; a clinic could mean booked, attended, or paid consultation.
- **Expert decision:** Name the downstream event before launch and report booked, attended, and paid stages separately.
- **Wrong takeaway:** Do not copy the result without knowing which CRM action trained delivery.
- **Proof/source:** **C+**, Meta case reproduced by implementation partner: https://www.facebook.com/business/success/mira-clinic and https://www.privyr.com/blog/facebook-lead-generation-case-study-best-practices/amp/

### Case 14 — AdEspresso: a transparent form-vs-page test was still confounded

- **Context:** B2B software retargeting warm visitors to six ebook offers; $2,000 total spend.
- **Change:** Sequentially compare landing-page forms with native lead forms.
- **Reported result:** Landing page: 1,077 leads, 50% visit-to-lead rate, $0.93 CPL. Native form: 1,057 leads, 67% form conversion, $0.95 CPL. Later free-trial conversion was described as almost identical without counts.
- **Design:** Original advertiser experiment with public front-end results, but campaigns were sequential rather than randomized/concurrent.
- **Failure/limitation:** Different fields, placements, reach, and timing; one weak ebook and later high frequency materially affected results.
- **Expert decision:** Compare destination through the next business stage and inspect offer-level variation before declaring the surface responsible.
- **Wrong takeaway:** Near-equal CPL does not prove native forms and landing pages are equivalent.
- **Proof/source:** **B+**, transparent but confounded original case: https://adespresso.com/blog/facebook-landing-pages-vs-facebook-lead-ads-which-is-better/

## 5. B2B/SaaS cases

### Case 15 — Podium: cold-start B2B optimized to booked demos before sparse pipeline stages

- **Context:** US B2B AI-agent software launching Meta from zero.
- **Change:** Consolidated CBO creative screening, micro-persona creative, known-lead exclusion, booked-demo optimization, and plans to move deeper when qualified-stage volume accumulated.
- **Reported result:** Six figures of ACV in month one and 3.98x pipeline ROI during the first 60 days.
- **Design:** Named-client agency/CRM report, no causal counterfactual.
- **Failure/limitation:** Spend, demo/SQL counts, qualification, attribution window, and closed-won revenue absent; pipeline is not cash ROAS.
- **Expert decision:** For sparse B2B outcomes, start with the closest event proven to predict pipeline and shift deeper only after reliable volume; keep pipeline and closed-won CAC separate.
- **Wrong takeaway:** The agency's proposed event-count trigger is not a universal Meta threshold.
- **Proof/source:** **B**, named agency case: https://www.flighted.co/case-studies/from-zero-to-6-figure-meta-ads-acv-for-podium

## 6. Cross-case post-mortem patterns

### A. The optimizer was rewarded for a proxy

- **Symptoms:** CPI, raw CPL, AddToCart, or purchase count improves while retained value, qualified rate, new-customer contribution, or total cohort revenue does not.
- **Cases:** Mejuri, Century Games, Supersonic, TECOBI, SumUp.
- **Action:** Map the P&L outcome to the deepest timely event with reliable volume; keep downstream quality as a guardrail when using a proxy.

### B. The measurement boundary excluded where or when value appeared

- **Symptoms:** Media looks inefficient online or immediately after treatment, while store, marketplace, phone, or delayed outcomes appear later.
- **Cases:** DSW, HexClad, Top Business Class.
- **Action:** Pre-register sales surfaces and conversion/post-treatment windows from backend behavior.

### C. Two campaigns ran, but no causal test existed

- **Symptoms:** Large lift claim without allocation, equal spend, overlap control, confidence, or backend reconciliation.
- **Cases:** Blibli, Sephora, Century Games, Supersonic, Podium, parts of Ortner's/TAF.
- **Action:** Call it directional and rerun a material decision through Experiments, Conversion Lift, or a powered geo holdout.

### D. Form friction changed lead volume and quality together

- **Symptoms:** Raw CPL and form CVR move, but qualification or revenue moves differently.
- **Cases:** SumUp, AdEspresso, Ortner's.
- **Action:** Test the smallest useful qualifier and compare cost at every CRM stage.

### E. The treatment was a package, not one variable

- **Symptoms:** Automation, budget, creative, offer, audience, page, and nurture changed together.
- **Cases:** DSW, TAF, Ortner's, Podium.
- **Action:** Describe the conclusion at package level. Do not credit a component that was not isolated.

### F. Attractive platform economics were not contribution or incrementality

- **Symptoms:** ROAS, pipeline ROI, or platform CPA looks strong without refunds, margin, new-customer split, cash revenue, or holdout evidence.
- **Cases:** Mejuri, TAF, Blibli, Podium.
- **Action:** Reconcile backend contribution and use lift measurement when causality changes the investment.

### G. Technical readiness was inferred from partial success

- **Symptoms:** Assets are visible and a token can read the account, but creative
  creation, delivery, or billing still fails.
- **Observed mechanism:** Token scopes, System User asset tasks, Page/Instagram
  identity, app state, payment-method eligibility, and account restriction are
  independent gates. A verified/default replacement card can coexist with zero
  balance, a failed historical transaction, and an active restriction.
- **Action:** Run a minimal `PAUSED` write and identity probe before the full
  build; inspect Billing and Account Quality separately; never use token
  regeneration, card swapping, or replacement assets as an enforcement bypass.
- **Evidence:** Account-specific operational post-mortem, 2026-07-24. Use as a
  diagnostic pattern, not a platform-wide causal claim. Full workflow:
  `13-api-access-billing-launch-operations.md`.

## 7. Source and evidence limitations

- Public case studies select positive results and are commonly published by Meta, an agency, or a measurement/implementation vendor involved in the work.
- None of the 15 cases exposes an independently audited raw dataset.
- Absolute spend is missing from most cases; sample sizes, MDEs, confidence intervals, and attribution settings are rarely disclosed.
- “Qualified lead” is usually undefined. Require the actual CRM field/rule before transferring a lead case.
- App cases commonly omit ATT/SKAN/AEM state, OS mix, fraud controls, retention, payback, and cohort LTV.
- Country, objective, product naming, feature availability, and platform measurement are volatile. Recheck source date and live account before implementation.
- A reported case lift is evidence that a treatment is worth testing under similar conditions, not a forecast for another advertiser.
