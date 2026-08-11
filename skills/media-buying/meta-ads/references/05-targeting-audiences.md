# Audiences & Targeting in Meta Ads Manager (2025–2026)

Scope: how audience selection works in Ads Manager as of 2025–2026 — Advantage+ audience vs original audiences, detailed targeting after the 2025 consolidation, custom audiences, lookalikes, retargeting structure, exclusions, sizes, and geo/demographic settings. Compiled 2026-07-22.

> Naming note: Meta now calls the old "Business Manager" a **Business Portfolio**; campaign creation for Sales/Leads/App objectives increasingly uses the streamlined **Advantage+ campaign setup** (2025 rollout). Older articles describing "Advantage+ Shopping Campaign (ASC)" as a separate campaign type are outdated — ASC is being phased into the Advantage+ campaign setup (Jon Loomer, May 2025).

---

## 1. The Big Picture: Targeting Is Now Mostly "Suggestions"

The single most important mental model for 2025–2026:

- **Audience Controls** = hard constraints Meta will not violate (locations, minimum age, excluded custom audiences, language in some cases).
- **Audience suggestions** = soft inputs (custom audiences, lookalikes, age range/max, gender, detailed targeting). Meta's delivery AI may go beyond any of them if it predicts more of your performance-goal actions.

This applies at both the default Advantage+ audience level and, increasingly, inside "original" audiences via forced expansion products (Advantage detailed targeting / Advantage lookalike) when optimizing for conversions.

Meta's claimed benchmarks for Advantage+ audience (vendor-reported, experiment run March–June 2023, still quoted in the UI warning dialog): 33% lower cost per result; Meta documentation also cites 13% lower median cost per catalog sale, 7% lower median cost per website conversion, 28% lower average cost per click/lead/landing page view (Jon Loomer best-practices guide; LaFactory summary of Meta Help Center figures).

---

## 2. Advantage+ Audience (the default)

Launched August 2023; it is the default targeting method when you create an ad set (Jon Loomer).

### 2.1 Audience Controls (hard constraints)

Only these exist as controls:

- **Locations** (current presence behavior and exceptions are described in §10; the old selector is not available for new ad sets)
- **Minimum age** (the available range can depend on objective, region, and account rollout)
- **Excluded custom audiences**
- **Language** (only when the language isn't common to the selected location)

There is **no control for maximum age or gender** under Advantage+ audience. Both are suggestions only.

### 2.2 Audience suggestions

Optional inputs can include custom audiences, lookalikes, age range, gender, and detailed targeting. Meta can use account and conversion signals to find likely responders and expand beyond suggestions. Do not describe that delivery as a deterministic remarketing-first sequence, and do not treat a suggestion as a hard restriction.

### 2.3 Advantage+ campaign setup (2025 UI change)

For Sales/Leads/App objectives, the streamlined Advantage+ campaign setup merges controls and suggestions into one view and shows a **Campaign Score** that rewards accepting Meta's defaults (budget, audience, placements). "Switch to original audiences" was replaced by a link labeled **"further limit the reach of your ads"** → **"Switch setup"**. After switching, an "Advantage+ on" badge remains: each input (age range, gender, custom audience, lookalike) is still a *suggestion by default* and only becomes a control when you **uncheck the suggestion checkbox** next to it. Net effect per Loomer's item-by-item comparison: no control is actually lost vs the old original-audiences flow — the steps just moved (Jon Loomer, "Does Meta's Advantage+ Campaign Setup Impact Targeting Control?", May 2025).

### 2.4 When to use Advantage+ audience (practitioner consensus, Loomer)

- **Use it** when broad delivery has a reliable optimization signal and no business or compliance need for tighter demographic control. A recorded purchase can still be low quality because of refunds, fraud, low margin, or poor downstream value; feed the system the closest reliable value signal available.
- **Avoid/switch** for top-of-funnel performance goals (link clicks, landing page views, post engagement, ThruPlay) where low-quality actions mislead delivery — especially when your real customer is a narrow age/gender group. Also consider switching for lead quality problems falling outside your target demo.
- Campaign construction consequence: avoid multiple ad sets whose suggestions converge on the same broad pool unless each represents a necessary budget, conversion-location, geography, policy, or experimental distinction. One consolidated ad set is often enough, but it is not a universal campaign rule.

### 2.5 Independent test data (treat as directional, single-advertiser tests)

- Thread Transfer (May 2025), cross-account tests: Advantage+ audience had ~25% lower CPM and +20% conversion volume, but manual targeting won on CPA ($31.85 vs $34.20), ROAS (3.4x vs 3.2x), and CVR (2.4% vs 2.1%).
- RKX Advertising (May 2025), 5 ecommerce campaigns / 30 days: Advantage+ CTR 2.3% vs 1.7% original. [uncertain — small internal test]

---

## 3. Original (Manual) Audiences

### 3.1 How to switch

Ad set → Audience section → link at the bottom of the Advantage+ audience box ("Switch to original audience options", or "further limit the reach of your ads" → "Switch setup" in the new UI). Meta shows a discouraging warning dialog citing its 33% stat; confirm to proceed.

### 3.2 What you get back

- Original-audience setup may expose tighter age, gender, language, custom-audience, or location controls. Availability depends on objective, performance goal, region, special category, and rollout; verify each field in the live account.
- Custom-audience inputs are suggestions in the standard Advantage+ audience flow. Isolation requires a setup that exposes the relevant hard audience control; verify availability for the objective, account, region, and special category.

### 3.3 Expansion products inside original audiences (critical)

| Expansion product | Applies to | Can it be turned off? |
|---|---|---|
| **Advantage custom audience** | Custom audience inputs | Suggestion by default; isolation controls depend on the current setup |
| **Advantage lookalike** | Lookalike inputs | Forced ON when optimizing for conversions; toggle available for other performance goals (link clicks, LPV, ThruPlay…) |
| **Advantage detailed targeting** | Interest/behavior inputs | Forced ON for conversions; Meta announced forced-on for link clicks and landing page views too (not yet rolled out to all accounts per Loomer) |

So "original audiences" no longer means deterministic targeting: with a conversions performance goal, your lookalike and detailed-targeting inputs are expanded automatically with no opt-out. The illusion-of-control trap: advertisers think they're targeting a 1% lookalike while Meta delivers well beyond it.

### 3.4 When original audiences are the right choice (Loomer)

1. Top-of-funnel optimization where you need demographic guardrails.
2. **True remarketing** — a message that must be seen only by an eligible custom audience (for example, an existing-customer offer). Use a setup that exposes the necessary restriction and verify actual reach. If the message is not audience-exclusive, compare a suggestion-based approach with a separated cell using account data.

---

## 4. Detailed Targeting (Demographics / Interests / Behaviors) After the 2025 Consolidation

### 4.1 What changed in 2025 (AdAmigo/Conversios reporting on Meta's updates)

- **March 31, 2025**: Meta began removing **detailed targeting exclusions**; removal completed by June 2025. You can no longer exclude by interest/behavior/demographic attribute at the ad set level. Meta's stated rationale: 22.6% lower median cost per conversion in tests without exclusions.
- **June 10, 2025**: first consolidation wave — niche sub-interests merged into broad groupings (e.g., "CrossFit", "powerlifting", "bodybuilding" → "Fitness & Exercise").
- **June 23, 2025**: second wave across Interests, Behaviors, and Demographics.
- **January 15, 2026**: final deadline — campaigns still using removed interests stop delivering after this date (per Meta's update timeline as reported by AdAmigo/Conversios).
- Drivers: privacy signal loss (iOS ATT ~50% opt-in by April 2025) and Meta's AI model performance (~5% more ad conversions on Instagram, ~3% on Facebook in Q2 2025 when allowed to optimize beyond manual interests, per Meta internal figures cited by AdAmigo). [uncertain — Meta-reported numbers relayed by a vendor blog]

### 4.2 What remains in the interface

Ads Manager → ad set → Audience → **Detailed targeting** → **Browse** opens three tabs:

- **Demographics**: age, gender, location, language, education, relationship status, life events (birthday, new job, recently moved, newly engaged), work (job titles, industries, employers), financial (limited), parents (by child age).
- **Interests**: now broad top-level groupings — Business & Industry; Entertainment; Family & Relationships; Fitness & Wellness; Food & Drink; Hobbies & Activities; Home & Garden; News & Politics; Shopping & Fashion; Sports & Outdoors; Technology. Sub-interests still exist under each but are fewer and broader, and the list shifts quarterly — always verify in the interface.
- **Behaviors**: purchase behavior (engaged shoppers, category buyers), device usage (OS, device model), travel (frequent/international travelers, commuters), digital activities (Page admins, event creators), anniversaries, charitable giving. Third-party-data-based behaviors were reduced; Meta leans on first-party on-platform signals.

### 4.3 When interest targeting still matters

- Under Advantage+ audience, detailed-targeting inputs are suggestions and do not define a hard delivery boundary.
- Some original-audience and performance-goal combinations still expose detailed targeting or expansion controls; verify the live setup instead of assuming expansion is always forced.
- Interests can provide a useful starting signal for new accounts, niche products, B2B, or low-volume objectives. Meta's current targeting guidance still describes interest targeting and recommends using it only with a sufficiently broad audience.
- Avoid large stacks that cannot be interpreted. Test a small number of coherent hypotheses against broad delivery and judge downstream value, not only CPM or CTR.

### 4.4 Exclusions after March 2025 — what still works

- **Custom audience exclusions** at the ad set level — now the primary exclusion mechanism (exclude purchasers, unqualified leads, employees).
- Account-level controls and placement exclusions (e.g., Audience Network).
- Creative-based filtering (copy that repels the wrong segment).
- Fix hygiene upstream: clean seed/exclusion lists at the CRM level before upload, since you can't patch with interest exclusions inside Ads Manager anymore (Madgicx).

---

## 5. Custom Audiences

Creation path: **Ads Manager → Audiences (left nav; under "Assets" in All Tools) → Create Audience → Custom Audience** → pick source. Five source types: Website, Customer list, App activity, Engagement, Offline activity.

### 5.1 Website (Meta Pixel)

- Rules: all visitors; visitors of specific pages (URL contains); visitors by time spent; specific pixel events (Purchase, AddToCart, Lead, etc.).
- Retention: default 30 days; up to **180 days** for standard events; purchase-event audiences extended to **730 days** (Jon Loomer, May 2026 QVT article, notes this was raised from the old 180-day max).
- Prereq: Pixel installed and firing (verify with Meta Pixel Helper); Conversions API strongly recommended post-ATT.
- Example (Chipper 2025 guide): `Purchase` event, 180-day window → "Website Purchasers 180d" audience used both for retargeting and for exclusions.

### 5.2 Customer list

- Upload CSV/TXT; 15 identifier types supported: email, phone, fn, ln, ct, st, zip, country, dob, birth year, gen, mobile advertiser ID, FB app user ID, FB Page user ID, external ID.
- Hashing depends on the path: **UI (Ads Manager) upload — do NOT pre-hash**, Meta normalizes and hashes client-side before sending. **Marketing API upload — you MUST pre-hash**: normalize, then SHA-256 (hex) each identifier yourself. Column headers must match Meta's template exactly.
- Expect **30–60% match rate**; improve with multiple identifiers per row and fresh (<12-month) data.
- Minimum **100 matched people** to use; aim for 1,000+.
- Requires accepting Meta's **Custom Audience Terms** per ad account (lawful basis + consent; no sensitive-category data, no brokered/scraped data).
- Static — does not auto-refresh; re-upload monthly or sync via CRM integration (Klaviyo/HubSpot/Zapier) or Conversions API.

### 5.3 App activity

- Requires Meta SDK (iOS/Android) or App Events API. Build from standard/custom in-app events (app open, purchase, level complete, content view, add to cart…). Retention up to 180 days.

### 5.4 Engagement (on-platform)

Subtypes and max retention windows (AdAmigo, 2026):

| Engagement source | What it captures | Max retention |
|---|---|---|
| Video | Watched 25% / 50% / 75% / 95%+ of selected or any videos | 365 days |
| Lead form | Opened (not submitted) or submitted | 90 days |
| Instant Experience | Opened or clicked | 365 days |
| Shopping | Viewed products / added to cart / purchased in shop | 365 days |
| Instagram account | Profile visit, engaged with post/ad, saved, shared, messaged | 730 days |
| Facebook Page | Page visit, post/ad engagement, CTA click, message | 730 days |
| Events | Responded Interested/Going | 365 days |
| On-Facebook listings | Marketplace viewers/messagers | 365 days |

- Instagram engagement options (coinis, citing Loomer): "everyone who engaged with your professional account" (broadest); specific actions — liked, saved, shared, commented, carousel swipes, CTA taps, link clicks; people who sent a message (may be unavailable in some European markets); ad interactions.
- Video viewers: pick watch threshold per intent — 25% = broad pool, 95% = hottest. Can scope to specific videos.
- Note: these audiences start populating when created (some engagement sources backfill historically; verify per source — [uncertain]).

### 5.5 Offline activity

- Send in-store, phone, and CRM events through the standard Conversions API or a supported partner integration. The separate Offline Conversions API was discontinued in May 2025; migrate integrations to datasets.

### 5.6 Sizing and hygiene

- Practical working size for a custom audience: **1,000–50,000** (AdAmigo). Below ~1,000 delivery struggles; above ~50k relevance decays.
- Naming convention: `[Brand]_[Source/Event]_[Window]` e.g. `Chipper25_Purchase_180d`. Never name audiences with sensitive traits ("Diabetes_Patients") — policy violation.
- Refresh CRM lists monthly; audit pixel firing; use the **Audience Overlap** tool to detect audiences that make your ad sets bid against each other.
- Privacy: GDPR consent before pixel/list use; CCPA/CPRA "Do Not Sell or Share" + honor opt-outs (Meta's Limit Data Use feature); Special Ad Categories (housing, employment, credit, social issues/politics) restrict some audience features.

---

## 6. Lookalike Audiences

### 6.1 Status in 2025–2026

Still available and still widely used (unlike Google Similar Audiences, fully phased out by 2025). But their role changed: they are now **raw material for Meta's AI rather than a hard boundary**. Inside Advantage+ audience they are suggestions; inside original audiences with conversion optimization, Advantage lookalike expands beyond your chosen percentage automatically.

Reported performance comparisons (vendor/agency figures via Madgicx, treat as directional): Advantage+ audience ~18% lower CPA than classic lookalikes; lookalikes (1–3%) ~32% better CPA than interest targeting; Advantage+ Shopping ~17% lower CPA / +16% ROAS vs manually managed campaigns. [uncertain — secondary citations of agency stats, not Meta-published]

### 6.2 Creation

**Ads Manager → Audiences → Create Audience → Lookalike Audience** (or from an existing custom audience → "Create Lookalike"):

1. Choose the source custom audience (value-based sources preferred — e.g., purchase event with value).
2. If value-based, select the value event (Purchase is default/strongest).
3. Set location (≥1 country).
4. Choose number of audiences (up to 6 at once) and **percentage 1–10%** (1% = most similar/smallest; start 1–3%, expand to 3–5% when scaling exhausts the pool).
5. Create; population takes hours to ~1 day.

Requirements: source needs ≥100 people from a single country (Meta minimum); 1,000+ for stability (practitioner consensus).

### 6.3 Seed quality hierarchy (Balistro 2026 guide)

1. Customer purchase lists (esp. repeat/high-value buyers; 50–70% typical match rate) — gold standard.
2. Pixel purchase events (ideally 1,000+ purchases in 90 days; self-updating).
3. Value-based customer lists (LTV-weighted).
Then weaker: website visitors, engagers. Best practice: seed from **top 10–20% of customers by LTV** or 3+ repeat purchasers, refresh monthly — stale seeds cause "audience decay."

### 6.4 Lookalikes vs Advantage+ — do they still matter?

- Yes for: niche verticals, B2B, low-budget/new accounts without enough conversion data for the algorithm, and as high-quality suggestions inside Advantage+ audience.
- Hybrid is the 2026 consensus: run broad/Advantage+ for scale, feed it strong seeds; keep manual 1–3% lookalikes where control matters.
- **Overlap trap**: nested 1%, 3%, and 5% lookalikes can overlap when run in parallel. Do not assume a universal CPM penalty or solve overlap by multiplying campaigns. Test whether separate tiers answer a real question; otherwise consolidate and evaluate after the account's conversion delay and required sample.

---

## 7. Retargeting Structure: Warm/Hot Setup

Standard 2025 practitioner structure (Chipper 2025 guide; AdAmigo):

**Engaged / non-buyers (warm) — build all four:**
1. Website visitors, last 90 days (pixel).
2. Catalog/product viewers, last 90 days.
3. Instagram engagers, last 90 days (or longer, up to 730d).
4. Email-list non-buyers (CRM upload).

**Existing customers (for exclusion + upsell):**
1. Website purchasers, 180 days (pixel Purchase event).
2. Customer file purchasers (CSV, refreshed monthly).
3. Instagram Shop purchasers (if IG Shop connected).

**Hot subsets for conversion campaigns:** cart/checkout abandoners 7–14 days, pricing-page visitors, 95% video viewers, lead-form openers who didn't submit (90-day cap).

Rules of thumb:
- Match the retention window to the purchase cycle — subscription/replenishable product → 28–30 day windows, not 180.
- Warm audiences usually 90 days: "recent enough to stay warm, not so old it's a cold list."
- Exclude recent purchasers when the offer is one-time or replenishment timing makes another purchase undesirable. Do not apply a universal 180-day exclusion to subscriptions, consumables, cross-sell, upsell, short replenishment cycles, or acquisition campaigns that deliberately permit existing customers.
- If optimizing for purchases, you often don't need a separate remarketing ad set at all: Advantage+ audience already prioritizes your converters/engagers before going broad; run "true" isolated remarketing only when the message must be seen exclusively by that group (Loomer).

---

## 8. Recommended Audience Sizes

- Practitioner guides often propose multi-million-person prospecting audiences, and Meta's current general guidance describes 2–10M as a useful broad range. These are not universal limits: viable size depends on geography, objective, budget, conversion rate, and service area.
- Do not diagnose an audience as too small or too broad from population alone. Check reach, frequency, delivery status, auction cost, conversion volume, and whether the audience is a hard boundary or only a suggestion.
- Custom audiences: min 100 (Meta hard minimum for lists), effective min ~1,000, sweet spot 1,000–50,000.
- Lookalike seeds: ≥100 per country required; 1,000+ matched recommended (upload 2,000+ raw contacts if match rate is ~50%).
- Learning context: automation benefits from accurate outcome signals and sufficient delivery, but no universal `50 conversions/week` or `$50/day` boundary makes manual targeting categorically better. Choose the setup from signal quality, expected result volume, test purpose, and live Delivery status.

---

## 9. Location, Language, Age, Gender Settings

### 9.1 Location options and the classic geo mistake

For new ad sets, Meta removed the former location-presence dropdown that separated residents, recent visitors, and travelers. Current delivery generally uses people **living in or recently in** the selected location; legacy ad sets or isolated account surfaces may still show older wording. Do not instruct users to switch to `People living in this location` unless the live account actually exposes that control. (Observed rollout: https://www.jonloomer.com/big-change-to-meta-ads-location-targeting/ and https://searchengineland.com/new-update-to-meta-ads-location-targeting-404124)

For local serviceability, use the smallest supported cities, postcodes, or radii; exclude unsupported locations where available; state the service area in the creative and landing page; and validate postcode/address in the form or checkout. Tourism campaigns must qualify travel intent through message and destination because the old travelers-only selector is generally unavailable.

Other geo gotchas:
- Radius targeting around a pin (min radius ~1 mi / 1 km [uncertain on exact current minimum]) is preferable to city polygons for hyper-local.
- Exclude specific locations (e.g., target a state, exclude a city) via the location "Exclude" option.
- Location is an **Audience Control** — one of the few hard constraints left; Advantage+ won't override it.
- Country-level targeting for multi-country e-commerce: split high-spend countries into separate ad sets/campaigns rather than lumping disparate economies, so CPMs and learning don't blend.

### 9.2 Language

Only available as a control when the language isn't common to the selected location. Don't select a language that is dominant in the geo (it restricts nothing and is just noise); do select it for expat/minority-language targeting.

### 9.3 Age and gender

- Advantage+ audience: minimum age is a documented control; maximum age and gender are generally suggestions. Available controls vary by campaign setup, region, and special category.
- Original audiences / "further limit the reach": full age range and gender as controls (uncheck the suggestion checkbox in the new Advantage+ campaign setup UI).
- Platform minimums and teen-targeting restrictions vary by country and product; do not assume every ad starts at 18+. Alcohol, gambling, financial products, and other regulated offers can require higher legal ages. Special Ad Categories can remove age/gender controls in affected countries.
- Common mistake: setting a tight age/gender "for brand fit" while optimizing for purchases — unnecessary; the algorithm finds buyers. Reserve demographic controls for top-of-funnel goals where engagement quality suffers.

---

## 10. Gotchas & Common Mistakes ( consolidated )

1. Treating Advantage+ suggestions as constraints — check "Audience definition" estimates but know delivery will exceed them.
2. Creating multiple ad sets whose suggestions do not represent distinct hypotheses can fragment delivery. Consolidate redundant cells; retain separate cells when they answer a necessary test or operational constraint.
3. Assuming every original-audience input is a fixed constraint. Expansion and available controls depend on the selected setup; inspect the live UI.
4. Still trying to exclude by interest — removed March–June 2025. Use custom-audience exclusions instead.
5. Campaigns still referencing removed interest categories stopped delivering after **Jan 15, 2026** — audit old ad sets.
6. Assuming the removed residents-only location selector is still available; qualify local serviceability through supported geo inputs and the conversion flow.
7. Applying a universal purchaser exclusion without considering replenishment, upsell, or acquisition strategy.
8. Retention windows mismatched to purchase cycle (180d for a 30-day replenishment product).
9. Pre-hashing customer lists before a **UI** upload (breaks matching — the UI hashes for you); wrong CSV headers. (For **Marketing API** uploads the opposite holds: you must pre-hash SHA-256.)
10. Parallel 1%/3%/5% lookalike ad sets in one campaign → self-competition, CPM inflation.
11. Sensitive-trait audience names → policy risk.
12. Comparing audience approaches before sufficient delivery and conversion lag have accumulated. Define the required sample and review window from the account rather than imposing 7–14 days universally.

---

## Sources

1. https://www.jonloomer.com/advantage-plus-audience-best-practices-guide/ — (practitioner) Advantage+ audience mechanics, controls vs suggestions, Meta's claimed benchmarks, when to use/switch. Accessed 2026-07-22.
2. https://www.jonloomer.com/advantage-plus-campaign-setup-targeting/ — (practitioner) 2025 Advantage+ campaign setup UI, "further limit the reach of your ads" / "Switch setup", per-input suggestion checkboxes. Accessed 2026-07-22.
3. https://www.jonloomer.com/advantage-audience-vs-original-audiences/ — (practitioner) Advantage custom audience / lookalike / detailed targeting expansion rules by performance goal. Accessed 2026-07-22.
4. https://www.jonloomer.com/qvt/how-to-define-audience-segments/ — (practitioner) Purchase-event custom audience retention extended to 730 days. Accessed 2026-07-22.
5. https://www.adamigo.ai/blog/7-tips-for-interest-based-targeting-on-meta-ads — (practitioner) June 2025 interest consolidation timeline, exclusions removal (Mar 31, 2025), remaining Demographics/Interests/Behaviors, setup walkthrough, 1–4M audience sizing. Accessed 2026-07-22.
6. https://www.conversios.io/blog/meta-advantage-audience-vs-detailed-targeting-2026-guide/ — (practitioner) June 23, 2025 consolidation date; Advantage+ vs detailed targeting FAQ; Pixel+CAPI prerequisite. Accessed 2026-07-22.
7. https://www.adamigo.ai/blog/how-to-create-custom-audiences-in-meta-ads — (practitioner) All five custom audience sources, step-by-step, retention window table, match rates, min sizes, compliance. Accessed 2026-07-22.
9. https://madgicx.com/blog/why-facebook-lookalike-audiences-are-worth-your-ad-spend — (practitioner) Lookalike creation steps, seed LTV segmentation, lookalikes-as-suggestions, overlap/CPM-inflation fix, CPA comparison stats. Accessed 2026-07-22.
10. https://www.balistro.com/facebook-ads-lookalike-audiences-guide/ — (practitioner) Seed source quality hierarchy, 50–70% match rate, 1,000+ purchase events. Accessed 2026-07-22.
11. https://ivanmana.com/what-is-a-lookalike-audience/ — (practitioner) Lookalike availability across platforms 2025; Google Similar Audiences phased out. Accessed 2026-07-22.
12. https://getkoro.app/blog/lookalike-audiences-on-instagram-ads — (practitioner) 1% starting percentage, seed refresh monthly, match-rate sizing math. Accessed 2026-07-22.
13. https://thread-transfer.com/blog/2025-05-09-advantage-plus-audience/ — (practitioner/benchmark) Advantage+ vs manual CPA/ROAS/CPM test results, May 2025. Accessed 2026-07-22.
14. https://rkxadvertising.com/advantage-audience-vs-original-audience/ — (practitioner) Advantage detailed targeting vs Advantage+ audience distinction; small internal CTR test. Accessed 2026-07-22.
15. https://www.adenslab.com/blog/geo-targeting-improve-meta-ad-performance-local-national-brands — (practitioner) Three/four location status options, "living in" vs "recently in" guidance. Accessed 2026-07-22.
16. https://coinis.com/how-to/best-way-to-target-country-on-facebook-ads — (practitioner) Location targeting options, default "living in or recently in". Accessed 2026-07-22.
17. https://coinis.com/how-to/engagement-instagram-custom-audience — (practitioner) Instagram engagement custom audience subtypes incl. message senders, EU availability caveat. Accessed 2026-07-22.
18. https://lafactory.com/meta-advantage-plus-audience/ — (practitioner) Summary citing Meta Help Center ("About Advantage+ audience"; "About Audience controls and Audience suggestions") and Meta benchmark figures. Accessed 2026-07-22.
19. https://www.mbadv.agency/meta-ads/meta-ads-audience-targeting — (practitioner) Controls-vs-suggestions UI confirmation; ~50 conversions/week, $50/day heuristics. Accessed 2026-07-22.
20. https://adsuploader.com/blog/meta-audience-targeting — (practitioner) Four audience types; 2–10M recommended size. Accessed 2026-07-22.
21. https://audiencelab.ai/blog/lookalike-audiences-guide — (practitioner) Lookalike seed quality, testing guidance 2025. Accessed 2026-07-22.
22. https://leadsbridge.com/blog/a-step-by-step-guide-to-facebook-custom-audiences/ — (practitioner) Custom audience creation steps. Accessed 2026-07-22.

## Gaps

- **Official Meta Business Help Center pages could not be fetched** (facebook.com/business/help blocks automated fetches — HTTP 400). UI labels and flows here come from practitioner walkthroughs with screenshots (chiefly Jon Loomer), not from the primary Meta docs. Titles confirmed via secondary citation: "About Advantage+ audience", "About Audience controls and Audience suggestions". Recommend manual capture of those help-center URLs.
- Exact current minimum radius and available location controls vary by country, objective, special category, and account rollout; verify them in the live ad set.
- Whether engagement custom audiences backfill historical engagement at creation (vs only accumulating forward) varies by source and was not verified per subtype.
- The reported "Jan 15, 2026 stop-delivery deadline" for removed interests and the June 2025 consolidation waves rest on two vendor blogs (AdAmigo, Conversios) citing Meta update notices; not cross-confirmed against the official Meta announcement.
- Meta's Advantage+ performance stats (33% / 28% / 13% / 7%) are vendor-reported from a 2023 experiment; no newer official benchmark verified.
- CPA/ROAS comparison numbers in §6.1 are agency stats relayed by Madgicx, not primary sources.
- Special Ad Category targeting restrictions (housing/employment/credit/social issues) mentioned but full 2025–2026 restriction matrix not detailed here.
