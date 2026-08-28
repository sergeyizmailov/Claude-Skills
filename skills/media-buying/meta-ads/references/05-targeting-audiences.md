# Audiences & Targeting in Meta Ads Manager (2025–2026)

Scope: audience selection in Ads Manager 2025–2026 — Advantage+ audience vs original audiences, detailed targeting after the 2025 consolidation, custom audiences, lookalikes, retargeting structure, exclusions, sizes, geo/demographic settings. Compiled 2026-07-22.

> Naming note: Meta now calls "Business Manager" a **Business Portfolio**; Sales/Leads/App creation increasingly uses the streamlined **Advantage+ campaign setup** (2025 rollout). "ASC" as a separate campaign type is outdated — folded into Advantage+ campaign setup (Jon Loomer, May 2025).

---

## 1. The Big Picture: Targeting Is Now Mostly "Suggestions"

- **Audience Controls** = hard constraints Meta won't violate (locations, minimum age, excluded custom audiences, language sometimes).
- **Audience suggestions** = soft inputs (custom audiences, lookalikes, age range/max, gender, detailed targeting) — delivery AI can exceed them for more performance-goal actions; applies to Advantage+ audience and, via forced expansion under conversions optimization (§3.3), original audiences too.

Meta's claimed Advantage+ audience benchmarks (vendor-reported, March–June 2023 experiment, still quoted in the UI warning dialog): **33%** lower cost/result; **13%** lower median cost/catalog sale; **7%** lower median cost/website conversion; **28%** lower average cost/click-lead-LPV (Jon Loomer; LaFactory summary of Meta Help Center figures).

---

## 2. Advantage+ Audience (the default)

Launched August 2023; default targeting method when you create an ad set (Jon Loomer).

### 2.1 Audience Controls (hard constraints)

Controls only: **Locations** (§10; old selector gone for new ad sets); **Minimum age** (varies by objective/region/rollout); **Excluded custom audiences**; **Language** (only if uncommon to the location). **No control for max age or gender** — suggestions only.

### 2.2 Audience suggestions

Suggestions: custom audiences, lookalikes, age range, gender, detailed targeting. Meta expands beyond them using account/conversion signals — not a deterministic remarketing-first sequence.

### 2.3 Advantage+ campaign setup (2025 UI change)

Sales/Leads/App: Advantage+ campaign setup merges controls/suggestions into one view, shows a **Campaign Score** rewarding Meta's defaults (budget, audience, placements). "Switch to original audiences" → **"further limit the reach of your ads"** → **"Switch setup"**. Post-switch, "Advantage+ on" badge stays: each input (age range, gender, custom audience, lookalike) is a suggestion by default, becomes a control only by **unchecking its checkbox**. Net effect: no control lost vs old flow, steps just moved (Jon Loomer, "Does Meta's Advantage+ Campaign Setup Impact Targeting Control?", May 2025).

### 2.4 When to use Advantage+ audience (practitioner consensus, Loomer)

- **Use** when broad delivery has a reliable signal, no demographic-control need. A recorded purchase can still be low-quality (refunds, fraud, low margin) — feed the closest reliable value signal.
- **Avoid/switch** for top-of-funnel goals (link clicks, LPV, post engagement, ThruPlay) where low-quality actions mislead delivery, especially with a narrow real customer age/gender; also for lead-quality issues outside target demo.
- Avoid ad sets whose suggestions converge on the same broad pool without a real budget/geo/policy/experimental distinction — one consolidated ad set is often enough, not universal.

### 2.5 Independent test data (treat as directional, single-advertiser tests)

| Source | Metric | Advantage+ | Manual/Original |
|---|---|---|---|
| Thread Transfer, May 2025 (cross-account) | CPM | ~25% lower | baseline |
| | Conversion volume | +20% | baseline |
| | CPA | $34.20 | **$31.85 (won)** |
| | ROAS | 3.2x | **3.4x (won)** |
| | CVR | 2.1% | **2.4% (won)** |
| RKX Advertising, May 2025 (5 ecom campaigns/30d) [uncertain — small test] | CTR | 2.3% | 1.7% |

---

## 3. Original (Manual) Audiences

### 3.1 How to switch

Ad set → Audience → link at bottom of Advantage+ box ("Switch to original audience options" / "further limit the reach of your ads" → "Switch setup"). Meta warns citing its 33% stat; confirm to proceed.

### 3.2 What you get back

May expose tighter age/gender/language/custom-audience/location controls, depending on objective, performance goal, region, special category, rollout — verify live. Custom-audience inputs remain suggestions under standard Advantage+ flow; isolation needs a setup exposing the hard control.

### 3.3 Expansion products inside original audiences (critical)

| Expansion product | Applies to | Can it be turned off? |
|---|---|---|
| **Advantage custom audience** | Custom audience inputs | Suggestion by default; isolation controls depend on the current setup |
| **Advantage lookalike** | Lookalike inputs | Forced ON when optimizing for conversions; toggle available for other performance goals (link clicks, LPV, ThruPlay…) |
| **Advantage detailed targeting** | Interest/behavior inputs | Forced ON for conversions; Meta announced forced-on for link clicks and landing page views too (not yet rolled out to all accounts per Loomer) |

So "original audiences" ≠ deterministic: under a conversions goal, lookalike/detailed-targeting inputs auto-expand, no opt-out. Illusion-of-control trap: advertisers think they're targeting a 1% lookalike while Meta delivers well beyond it.

### 3.4 When original audiences are the right choice (Loomer)

1. Top-of-funnel optimization needing demographic guardrails.
2. **True remarketing** — message only for an eligible custom audience (e.g. existing-customer offer). Use a setup exposing the restriction, verify reach. If not exclusive, compare suggestion-based vs a separated cell using account data.

---

## 4. Detailed Targeting (Demographics / Interests / Behaviors) After the 2025 Consolidation

### 4.1 What changed in 2025 (AdAmigo/Conversios reporting on Meta's updates)

- **March 31, 2025**: Meta began removing **detailed targeting exclusions** (completed by June 2025) — no more ad-set-level interest/behavior/demographic exclusions. Rationale: 22.6% lower median cost per conversion without exclusions.
- **June 10, 2025**: wave 1 — niche sub-interests merged into broad groupings (e.g., "CrossFit"/"powerlifting"/"bodybuilding" → "Fitness & Exercise").
- **June 23, 2025**: wave 2 — Interests, Behaviors, Demographics.
- **January 15, 2026**: campaigns still using removed interests stop delivering (per Meta's timeline, AdAmigo/Conversios).
- Drivers: privacy signal loss; Meta's AI performs better unconstrained (~5% more ad conversions on Instagram, ~3% on Facebook, Q2 2025, per Meta internal figures cited by AdAmigo). [uncertain — Meta-reported numbers relayed by a vendor blog] The "~50% ATT opt-in" figure is **AppsFlyer's**, not Meta's, and is one of two defensible vendor readings — canonical statement and the geo spread that matters more: `tracker-ops/03`.

### 4.2 What remains in the interface

Ads Manager → ad set → Audience → **Detailed targeting** → **Browse**, three tabs:

- **Demographics**: age, gender, location, language, education, relationship status, life events (birthday, new job, recently moved, newly engaged), work (job titles, industries, employers), financial (limited), parents (by child age).
- **Interests**: broad groupings only — Business & Industry; Entertainment; Family & Relationships; Fitness & Wellness; Food & Drink; Hobbies & Activities; Home & Garden; News & Politics; Shopping & Fashion; Sports & Outdoors; Technology. Sub-interests fewer/broader, shift quarterly — verify live.
- **Behaviors**: purchase behavior (engaged shoppers, category buyers), device usage (OS, device model), travel (frequent/international travelers, commuters), digital activities (Page admins, event creators), anniversaries, charitable giving. Third-party behaviors reduced; Meta leans on first-party on-platform signals.

### 4.3 When interest targeting still matters

- Some original-audience/goal combos still expose detailed-targeting or expansion controls — verify live, don't assume forced expansion.
- Useful starting signal: new accounts, niche products, B2B, low-volume objectives; pair with a sufficiently broad audience.
- Avoid uninterpretable large stacks — test few coherent hypotheses, judge downstream value not just CPM/CTR.

### 4.4 Exclusions after March 2025 — what still works

- **Custom audience exclusions** at ad-set level — now primary mechanism (exclude purchasers, unqualified leads, employees).
- Account-level controls, placement exclusions (e.g. Audience Network).
- Creative-based filtering (copy that repels wrong segment).
- Clean seed/exclusion lists at CRM level pre-upload — no interest-exclusion patch left in Ads Manager (Madgicx).

---

## 5. Custom Audiences

**Ads Manager → Audiences (left nav; under "Assets" in All Tools) → Create Audience → Custom Audience** → pick source. Five types: Website, Customer list, App activity, Engagement, Offline activity.

### 5.1 Website (Meta Pixel)

- Rules: all visitors; specific-page visitors (URL contains); time-spent visitors; pixel events (Purchase, AddToCart, Lead, etc.).
- Retention: default 30d; up to **180d** standard events; purchase events to **730d** (Jon Loomer, May 2026 QVT — raised from old 180d max).
- Prereq: Pixel installed/firing (Meta Pixel Helper); CAPI recommended post-ATT.
- Example (Chipper 2025): `Purchase`, 180d window → "Website Purchasers 180d" — retargeting + exclusions.

### 5.2 Customer list

- CSV/TXT; 15 identifier types: email, phone, fn, ln, ct, st, zip, country, dob, birth year, gen, mobile advertiser ID, FB app user ID, FB Page user ID, external ID.
- Hashing: **UI — do NOT pre-hash** (Meta hashes client-side); **Marketing API — MUST pre-hash** (normalize, SHA-256 hex). Headers must match Meta's template exactly.
- **30–60% match rate**; improve with multiple identifiers/row, fresh (<12mo) data.
- Min **100 matched**; aim 1,000+.
- Requires Meta's **Custom Audience Terms** per ad account (lawful basis + consent; no sensitive/brokered/scraped data).
- Static — re-upload monthly or sync via CRM (Klaviyo/HubSpot/Zapier) or CAPI.

### 5.3 App activity

Meta SDK (iOS/Android) or App Events API; standard/custom in-app events (app open, purchase, level complete, content view, add to cart…). Retention up to 180d.

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

- IG engagement (coinis, citing Loomer): "everyone who engaged with your professional account" (broadest); liked/saved/shared/commented/carousel swipes/CTA taps/link clicks; message senders (may be unavailable in some EU markets); ad interactions.
- Video: 25% = broad pool, 95% = hottest; can scope to specific videos.
- Populate at creation; some sources may backfill historically — verify per source [uncertain].

### 5.5 Offline activity

In-store/phone/CRM events via standard Conversions API or a supported partner integration. Separate Offline Conversions API discontinued May 2025 — migrate to datasets.

### 5.6 Sizing and hygiene

- Size: **1,000–50,000** (AdAmigo) — below ~1,000 struggles, above ~50k decays.
- Naming: `[Brand]_[Source/Event]_[Window]`, e.g. `Chipper25_Purchase_180d`. Never sensitive traits ("Diabetes_Patients") — policy violation.
- Refresh CRM monthly; audit pixel firing; use **Audience Overlap** tool.
- Privacy: GDPR consent pre-use; CCPA/CPRA opt-outs (Limit Data Use); Special Ad Categories (housing, employment, credit, social/political) restrict features.

---

## 6. Lookalike Audiences

### 6.1 Status in 2025–2026

Still available, widely used (unlike Google Similar Audiences, phased out by 2025) — but now **raw material for Meta's AI, not a hard boundary**: suggestions inside Advantage+ audience; inside original audiences with conversion optimization, Advantage lookalike auto-expands beyond the chosen percentage.

Performance (vendor/agency via Madgicx, directional): Advantage+ audience ~18% lower CPA than classic lookalikes; lookalikes (1–3%) ~32% better CPA than interest targeting; Advantage+ Shopping ~17% lower CPA / +16% ROAS vs manual. [uncertain — secondary agency stats, not Meta-published]

### 6.2 Creation

**Ads Manager → Audiences → Create Audience → Lookalike Audience** (or from an existing custom audience → "Create Lookalike"):

1. Choose source custom audience (value-based preferred, e.g. purchase event with value); if value-based, select the value event (Purchase default/strongest).
2. Set location (≥1 country).
3. Choose count (up to 6 at once) and **percentage 1–10%** (1% = smallest/most similar; start 1–3%, expand to 3–5% when scaling exhausts pool).
4. Create; population takes hours to ~1 day.

Requirements: source ≥100 people from a single country (Meta minimum); 1,000+ for stability (practitioner consensus).

### 6.3 Seed quality hierarchy (Balistro 2026 guide)

1. Customer purchase lists (repeat/high-value buyers; 50–70% match rate) — gold standard.
2. Pixel purchase events (ideally 1,000+ purchases/90 days; self-updating).
3. Value-based customer lists (LTV-weighted).
Weaker: website visitors, engagers. Best practice: seed from **top 10–20% by LTV** or 3+ repeat purchasers, refresh monthly — stale seeds cause "audience decay."

### 6.4 Lookalikes vs Advantage+ — do they still matter?

- Yes for: niche verticals, B2B, low-budget/new accounts lacking conversion data, high-quality Advantage+ suggestions.
- 2026 consensus: hybrid — broad/Advantage+ for scale fed strong seeds, manual 1–3% lookalikes where control matters.
- **Overlap trap**: nested 1/3/5% lookalikes can overlap in parallel — no universal CPM penalty, don't fix by multiplying campaigns. Test whether tiers answer a real question; else consolidate, evaluate after conversion delay + required sample.

---

## 7. Retargeting Structure: Warm/Hot Setup

Standard 2025 structure (Chipper 2025; AdAmigo):

**Warm (engaged/non-buyers) — build all four:** website visitors, last 90 days (pixel); catalog/product viewers, last 90 days; Instagram engagers, last 90 days (or up to 730d); email-list non-buyers (CRM upload).

**Existing customers (exclusion + upsell):** website purchasers, 180 days (pixel Purchase event); customer file purchasers (CSV, refreshed monthly); Instagram Shop purchasers (if IG Shop connected).

**Hot subsets for conversion campaigns:** cart/checkout abandoners 7–14 days, pricing-page visitors, 95% video viewers, lead-form openers who didn't submit (90-day cap).

Rules of thumb:
- Match retention window to purchase cycle — subscription/replenishable → 28–30 days, not 180.
- Warm audiences usually 90 days.
- Exclude recent purchasers only when offer is one-time or replenishment timing makes another purchase undesirable — no universal 180-day exclusion for subscriptions, consumables, cross-sell, upsell, short replenishment, or acquisition campaigns permitting existing customers.
- Optimizing for purchases often needs no separate remarketing ad set: Advantage+ audience already prioritizes converters/engagers before going broad — isolate "true" remarketing only when the message must be exclusive to that group (Loomer).

---

## 8. Recommended Audience Sizes

- 2–10M is Meta's general-guidance broad range for prospecting; not a universal limit — depends on geography, objective, budget, conversion rate, service area.
- Don't diagnose too-small/too-broad from population alone — check reach, frequency, delivery status, auction cost, conversion volume, and control-vs-suggestion status.
- Custom audiences: min 100 (Meta hard minimum), effective min ~1,000, sweet spot 1,000–50,000.
- Lookalike seeds: ≥100/country required; 1,000+ matched recommended (upload 2,000+ raw contacts if match rate ~50%).
- No universal `50 conversions/week` or `$50/day` boundary makes manual targeting categorically better than automation — choose from signal quality, expected result volume, test purpose, live Delivery status.

---

## 9. Location, Language, Age, Gender Settings

### 9.1 Location options and the classic geo mistake

Meta removed the former location-presence dropdown (residents/recent visitors/travelers) for new ad sets. Delivery generally uses people **living in or recently in** the selected location; legacy ad sets/isolated surfaces may still show older wording. Don't switch to `People living in this location` unless the live account exposes that control. (Observed rollout: https://www.jonloomer.com/big-change-to-meta-ads-location-targeting/ and https://searchengineland.com/new-update-to-meta-ads-location-targeting-404124)

Local serviceability: use smallest supported cities/postcodes/radii; exclude unsupported locations; state service area in creative/landing page; validate postcode/address in form/checkout. Tourism campaigns qualify travel intent via message/destination — old travelers-only selector is generally unavailable.

Other geo gotchas:
- Radius targeting around a pin (min ~1 mi/1 km [uncertain on exact current minimum]) preferable to city polygons for hyper-local.
- Exclude specific locations (e.g., target a state, exclude a city) via location "Exclude".
- Location is an **Audience Control** — one of the few hard constraints left; Advantage+ won't override it.
- Multi-country e-commerce: split high-spend countries into separate ad sets/campaigns rather than lumping disparate economies, so CPMs/learning don't blend.

### 9.2 Language

Only a control when the language isn't common to the selected location. Don't select a geo-dominant language (restricts nothing, just noise) — do select for expat/minority-language targeting.

### 9.3 Age and gender

- Advantage+ audience: min age only (§2.1); original audiences / "further limit the reach" exposes full age range + gender as controls (uncheck the suggestion checkbox). Available controls vary by campaign setup, region, special category.
- Platform minimums/teen-targeting restrictions vary by country/product — don't assume every ad starts at 18+. Alcohol, gambling, financial products, other regulated offers can require higher legal ages. Special Ad Categories can remove age/gender controls in affected countries.
- Common mistake: tight age/gender "for brand fit" while optimizing for purchases — unnecessary, the algorithm finds buyers. Reserve demographic controls for top-of-funnel goals where engagement quality suffers.

---

## 10. Gotchas & Common Mistakes ( consolidated )

1. Treating Advantage+ suggestions as constraints — check "Audience definition" estimates but know delivery will exceed them.
2. Multiple ad sets with non-distinct suggestions fragment delivery — consolidate redundant cells, keep separate ones only for a necessary test/operational constraint.
3. Assuming every original-audience input is a fixed constraint — expansion and controls depend on the selected setup, inspect live UI.
4. Trying to exclude by interest — removed March–June 2025; use custom-audience exclusions instead.
5. Campaigns referencing removed interest categories stopped delivering after **Jan 15, 2026** — audit old ad sets.
6. Assuming the removed residents-only location selector still exists — qualify local serviceability through supported geo inputs and conversion flow.
7. Universal purchaser exclusion without considering replenishment, upsell, or acquisition strategy.
8. Retention windows mismatched to purchase cycle (180d for a 30-day replenishment product).
9. Pre-hashing customer lists before a **UI** upload (breaks matching — UI hashes for you); wrong CSV headers. **Marketing API** uploads require the opposite: pre-hash SHA-256.
10. Parallel 1%/3%/5% lookalike ad sets in one campaign → self-competition, CPM inflation.
11. Sensitive-trait audience names → policy risk.
12. Comparing audience approaches before sufficient delivery/conversion lag accumulate — define required sample and review window from the account, not a universal 7–14 days.

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
