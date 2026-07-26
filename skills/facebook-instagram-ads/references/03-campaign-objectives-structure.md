# Campaign Objectives & Structure for Instagram-Focused Meta Ads (2025–2026)

Scope: the six ODAX objectives, Advantage+ vs manual campaign setup, campaign budgets vs ad-set budgets, special ad categories, naming conventions, and testing-to-scaling account structure. UI details were reviewed 2026-07-22. Treat current Meta documentation or the live account as authoritative; practitioner sources are explicitly labeled as heuristics.

---

## 1. The Six ODAX Objectives

### 1.1 Background: what ODAX changed

- ODAX = "Outcome-Driven Ad Experiences." Announced on the Meta for Developers blog **December 21–22, 2021**; rolled out through 2022; became the **exclusive campaign-creation path in 2023**. (Source: MB Adv ODAX guide, Jun 2026; Meta for Developers via secondary citation.)
- Consolidated **11 legacy objectives** under 3 funnel banners (Awareness / Consideration / Conversion) into **6 flat outcomes**: **Awareness, Traffic, Engagement, Leads, App promotion, Sales**.
- The old three-banner funnel framing no longer exists anywhere in the UI. Any article describing a "consideration campaign" is pre-2023 and outdated.
- Legacy → ODAX mapping (important when reading older tutorials):
  - Brand Awareness, Reach → **Awareness**
  - Traffic → **Traffic** (unchanged)
  - Engagement, Video Views, **Messages** → **Engagement** (this is the big one: Messenger / Instagram Direct / WhatsApp campaigns now live under Engagement)
  - Lead Generation → **Leads**
  - App Installs → **App promotion**
  - Conversions, Catalog Sales → **Sales** (many-to-one; the catalog vs website distinction moved into ad-set conversion-location settings)
  - Store Traffic → **sunset** (new campaigns disabled Jan 2024, delivery halted H2 2024; no ODAX replacement)
- **The objective cannot be edited after launch.** Other settings may be editable, but some edits create a new ad, trigger review, or cause delivery to re-enter preparing/learning. Changing objective requires a new campaign. Treat the objective as a delivery signal, not merely a funnel label.
- Marketing API: legacy objective constants (`BRAND_AWARENESS`, `LINK_CLICKS`, `CONVERSIONS`, `APP_INSTALLS`, etc.) now return 400 errors for new campaigns; use `OUTCOME_AWARENESS`, `OUTCOME_TRAFFIC`, `OUTCOME_ENGAGEMENT`, `OUTCOME_LEADS`, `OUTCOME_APP_PROMOTION`, `OUTCOME_SALES`. Some third-party dashboards still label Sales as "Conversions" — legacy label, same thing. (Source: pipeboard-co/meta-ads-mcp GitHub, 2026.)

### 1.2 Per-objective breakdown

| Objective | Optimizes for | Conversion locations / sub-goals | Best for |
|---|---|---|---|
| **Awareness** | Reach, impressions, ad recall lift, ThruPlay, 2-sec continuous video views | None (visibility only) | Brand launches, video distribution, max reach |
| **Traffic** | Link clicks, landing page views | Website, App, Instagram profile, calls | Sending qualified clicks off-platform; building retargeting pools |
| **Engagement** | Post interactions, messaging conversations, video views, page activity | On-post, Messenger, **Instagram Direct**, WhatsApp, on-video, on-event | DM conversations, social proof, content interaction, page/profile growth |
| **Leads** | Instant Form submits, website lead events, Messenger conversations, calls | Instant Forms, Website, Messenger, Calls, App | Service businesses, B2B, list-building, high-ticket |
| **App promotion** | App installs, in-app events, in-app purchase value | Mobile app only | Any install/in-app goal — closed mandate, no other objective supports installs |
| **Sales** | Purchase, Add to Cart, Initiate Checkout, catalog sales, messaging conversions, value (ROAS) | Website, App, Website+App, Messenger/WhatsApp | E-commerce purchases, subscriptions, bottom-funnel revenue |

Notes per objective:

- **Awareness** — the only objective with no conversion location. Optimization goals (~5): Reach, Impressions, Ad recall lift (users likely to remember the ad within 2 days), ThruPlay (≥15s video views or full video if shorter), 2-second continuous video views (≥50% pixels on screen). Wrong choice whenever any downstream action is the goal. (Source: MB Adv 2026; Get-Ryze 2026.)
- **Traffic** — optimizes for clicks, not what happens after the click. ~5 goals: link clicks, landing page views, Messenger conversations, **Instagram profile visits**, calls. Instagram profile visits as a Traffic conversion location is the closest "official" lever for follower growth (see §1.3). Common failure mode: using Traffic as the permanent campaign type when sales is the goal — Meta finds the cheapest clickers, not buyers.
- **Engagement** — absorbed the legacy Messages objective. This is where **click-to-DM ads (Messenger / Instagram Direct / WhatsApp)** now live. Also the objective for social proof (likes/comments accumulate on the post) and video views.
- **Leads** — Instant Forms are native in-feed forms (no website needed, cheaper CPL, lower lead quality); Website conversion location needs a working Pixel lead event (better data); **Conversion leads** optimization goal requires CRM + Conversions API integration to feed qualified-lead signals back to Meta. Median CPL benchmark: **$23.10** (WordStream 2026 panel; CPC $1.92, CVR 8.25%).
- **App promotion** — closed mandate: ~3 goals (installs, app events, value). If the conversion event is an install, this objective is non-negotiable.
- **Sales** — website-purchase optimization needs a working web event source, while app, shop, catalog, and messaging purchase flows have different event requirements. Optimize for the business outcome whenever it is measurable. Moving temporarily to a higher-frequency event can increase volume but may train delivery toward weaker intent, so test it rather than treating it as the default fix. Catalog ads (formerly "Catalog Sales" / DPA) are configured inside Sales.

### 1.3 Picking an objective for typical Instagram goals

| Goal | Recommended objective | Why / caveats |
|---|---|---|
| **More Instagram followers** | Traffic → conversion location "Instagram profile" (Instagram profile visits), or Engagement | There is no "follows" optimization event. Meta cannot bill/optimize directly on follows; profile visits are the proxy. Expect modest follow-through; creative (why to follow) does the real work. [uncertain: availability of the IG-profile conversion location varies by account/region in 2025–26 rollouts] |
| **DMs (Instagram Direct / Messenger / WhatsApp)** | **Engagement** → messaging conversion location ("Messaging apps") | This is the post-ODAX home of click-to-message ads. Leads objective also supports Messenger/IG Direct as a lead location with automated Q&A flows. Engagement = conversations; Leads = contact capture with qualification questions. |
| **Website sales (e-commerce)** | **Sales** with Purchase event via Pixel + CAPI | Do not substitute Traffic "to be safe" — Meta will find clickers, not buyers. |
| **Lead forms** | **Leads** → Instant Forms (volume) or Website lead event (quality) | Conversion-leads optimization needs CAPI + CRM feedback. |
| **App installs** | **App promotion** | Only objective that supports installs. |

Common mistakes (consensus across Get-Ryze 2026, MB Adv 2026):
1. Choosing Sales for cold audiences with zero pixel history → starved learning phase. Counter-view from practitioners: even new brands should often start on Sales if tracking is set up, because Awareness trains nothing useful (Koro 2026 guide).
2. Using Traffic when the real goal is leads/sales → window shoppers.
3. Switching objectives mid-flight → learning reset (and it's not even possible — requires a new campaign).
4. Creative misaligned with objective (hard-sell creative in Awareness campaigns).
5. Underfunding or fragmentation: budget must support the outcome, conversion delay, and decision being made. No universal `50 conversions/week` or `$5–10/day` rule applies across objectives, markets, and account economics.

---

## 2. Advantage+ Sales (formerly Advantage+ Shopping) vs Manual Campaigns

### 2.1 The 2025 restructuring — what actually changed

- **Advantage+ Shopping Campaigns (ASC) are gone.** In 2025 Meta renamed/replaced them with **Advantage+ Sales campaigns**, and folded Sales, Leads, and App promotion objectives into a single streamlined **"Advantage+ campaign setup"** flow. (Source: Jon Loomer, "Advantage+ Campaign Creation: A Complete Guide," Jun 23, 2025; "Advantage+ Sales Replaces Advantage+ Shopping," Mar 6, 2025.)
- The old ASC distinguishing features did **not** carry over: no targeting inputs, locked placements, single ad set, up to 150 ads, existing-customer budget cap. Loomer's summary: an Advantage+ Sales campaign is best described as "a manual Sales campaign using the prior approach, but without making any significant edits to defaults."
- New flow specifics (Loomer, Jun 2025):
  - The initial "automated vs manual" prompt at campaign creation is **removed**; you go straight into creation.
  - Advantage+ applies to **Sales, Leads, App promotion** objectives only; other objectives keep the older tailored flow.
  - Whether a campaign counts as "Advantage+" is determined by three elements: **Budget** (Advantage campaign budget on), **Audience** (Advantage+ audience with suggestions), **Placements** (Advantage+ placements). Leave defaults untouched → Advantage+ stays "on." Restrictive edits turn it "off," which also lowers the in-UI **Campaign Score / Opportunity score** (0–100).
  - **Advantage campaign budget is now ON by default** in the streamlined flow (it was off by default in the old manual flow).
  - Ad limits: max 50 ads per ad set (Meta discourages more than ~6 actively); the old ASC 150-ad cap no longer applies. [Birch 2026 guide cites "max 150 ads total, 50 per ad set" — treat total-campaign cap as uncertain.]
  - Sept 21, 2025: Meta launched a **unified API structure for Advantage+ campaigns** across sales, app, and leads objectives (PPC Land, 2026 timeline).

### 2.2 Pros / cons

Advantage+ (default/automated) pros:
- Less setup; Meta's aggregate data shows advertisers using defaults get better results on average. Meta reports Advantage+ Shopping/Sales surpassed a **$20B annual revenue run rate, ~70% YoY growth (Q3 2024 earnings)** — that's where Meta invests.
- Best with sufficient conversion volume (~50+/week), diverse creative (5–10+ variants), clean Pixel + CAPI tracking.
- Budget flows to what works in real time (combined with Advantage campaign budget).

Cons / where manual still wins:
- Reduced diagnostic visibility: harder to tell which audience/placement drove results.
- Broad-by-default can waste spend before the algorithm finds buyers — practitioner Fer Rivero (via Birch 2026): running Advantage+ with minimal input produced "complete randomness in terms of CPR"; he uses automation to scale proven winners, not to discover them.
- Creative testing reads are muddy — Advantage+ doesn't give equal spend per ad.
- Special Ad Categories restrict specific targeting controls by category and country. Do not assume that all Advantage+ automation is unavailable; verify the options exposed in the actual campaign flow.

### 2.3 Current best practice (2025–2026 consensus)

- A mixed manual/Advantage+ structure can preserve controlled testing while using automation for delivery, but it is not universally required. Choose the minimum structure that answers the current test or scaling question without fragmenting data. [practitioner strategy]
- Trust automation for budget scaling on winners; keep human control over creative testing and offer strategy. "Creative is the new targeting" — inside a broad/Advantage+ structure, creative variation is what segments the audience.
- Consolidate: fewer campaigns, fewer ad sets, more ads per ad set (see §5).

---

## 3. Advantage Campaign Budget (CBO) vs Ad-Set Budgets (ABO)

### 3.1 Naming and mechanics

- **Advantage campaign budget** (formerly Campaign Budget Optimization / CBO; Meta UI also shows "Advantage+ campaign budget"): one budget at campaign level; Meta distributes it across ad sets in real time toward best predicted results.
- **Ad set budgets** = ABO ("Ad Set Budget Optimization"); toggle Advantage campaign budget OFF at campaign level. ABO is still called ad set budgets in the UI.
- Meta's own aggregate claim: Advantage campaign budget can **decrease CPA by ~4.6% on average** vs ad-set budgets (Meta marketing figure, treat directionally). (Source: Capconvert 2026, citing Meta Help Center.)
- Eligibility requirements: every ad set in the campaign must share the **same budget type** (daily vs lifetime), **same bid strategy**, and **standard delivery**. (Source: Capconvert 2026, citing Meta Help Center; Jon Loomer "Advantage Campaign Budget Best Practices," Mar 2025.)
- Gotcha from the new default-on flow (Loomer, Jun 2025): with Advantage campaign budget on, some ad-set-level options disappear — e.g., **Cost Per Result Goal and budget scheduling move to campaign level**. Confusing if you only wanted one ad set.
- **Ad set spend limits** (min/max) under Advantage campaign budget: the max is an **average limit, not a hard daily cap** — Meta can exceed it on any given day as long as the average holds. Overusing minimums "defeats the whole purpose" (Loomer): if you don't trust the algorithm to allocate, use ad set budgets instead.
- Budget edits can change delivery or re-enter learning when Meta treats them as significant. Fixed 20% or 30% thresholds are practitioner heuristics, not published universal cutoffs; use the live delivery status and controlled increments.

### 3.2 When to use which (practitioner framework — Ads Uploader 2026, corroborated by Segwise 2026, Adamigo 2026)

| | ABO (ad set budgets) | CBO (Advantage campaign budget) |
|---|---|---|
| Control | Full manual | Algorithmic |
| Spend distribution | Equal per ad set (forced) | Performance-based; often ~80/20 Pareto split |
| Management load | Daily hands-on | Weekly checks |
| Best for | Tests needing ad-set budget control; operational splits still do not guarantee equal delivery or causal reads | Allocation across ad sets when the performance goal and economics are shared |
| Failure mode | Losses compound if creative hit rate is low | Can starve promising ad sets after a few hours on small budgets; can't fix weak creative |

- **Hybrid trick**: CBO + per-ad-set **minimum daily spend** for ~1 week (forces initial testing fairness), then **remove the minimums** and let CBO optimize. Keeping minimums forever = ABO with extra steps.
- Practitioner sizing heuristics include daily budget near 2× target CPA for an ABO test and `(target CPA × 50) ÷ 7` as a legacy volume-planning model. Neither guarantees learning completion. Size the structure from acceptable test risk, conversion delay, expected variance, and the number of decisions the test must support.
- Benchmark claim: CBO campaigns average **~27% lower cost per result** than ABO in multi-audience setups (Adamigo research summary, Jul 2026 — third-party figure, treat as directional).

---

## 4. Special Ad Categories

### 4.1 The categories (current, 2025–2026)

Declared at **campaign level** in Ads Manager (a "Special Ad Category" dropdown/checkbox at the top of campaign creation). Failing to declare when applicable is itself a policy violation → ad rejections, and on repeat, account restrictions.

1. **Financial products and services** — renamed from "Credit" and expanded in **October 2024** (US advertisers or ads targeting US audiences). Now covers credit cards, loans, financing, plus banking, insurance, investment products, payment platforms.
2. **Employment** — job listings, internships, professional certification programs, job fairs, employment agencies.
3. **Housing** — sale/rental listings, real estate services, homeowners insurance, mortgage, housing repair. (General home goods — furniture, decor — excluded.)
4. **Social issues, elections or politics** — ads by/about candidates, parties, elections, or advocacy on debated social issues. Requires ad authorization (ID verification) and "Paid for by" disclaimers. **EU: Meta blocked all social issue/election/political ads from October 2025** under the EU TTPA regulation (PPC Land, Oct 8, 2025) — political ads are simply unavailable in the EU now.

Background: categories introduced 2019 after US civil-rights settlements; expanded 2022 under the HUD settlement. (Source: Pix-Vu, Apr 2026; WordJack, Nov 2024; Faraday, Dec 2024.)

### 4.2 Targeting restrictions once a category is declared

The restriction matrix depends on category, advertiser/target country, and current Meta implementation. Affected housing, employment, and financial-product flows can limit age, gender, postcode/radius, location exclusions, detailed targeting, lookalikes, saved audiences, or form questions. The 15-mile radius rule is specific to documented US anti-discrimination implementations and must not be generalized worldwide.

**Special Ad Audiences are not a replacement:** Meta sunset them in 2022 and confirmed discontinuation in 2023. Custom audiences and other controls may remain available subject to anti-discrimination rules, but inspect the declared campaign rather than assuming a universal feature set. (Official: https://about.fb.com/news/2022/06/expanding-our-work-on-ads-fairness/ and https://about.fb.com/news/2023/01/an-update-on-our-ads-fairness-efforts/)

Sensitive-data-source classifications can also affect event sharing or optimization availability. Verify the live Events Manager and campaign flow before naming a restricted event. Additional authorization, Page, identity, or 2FA requirements are feature- and country-dependent. Failure to declare an applicable category can cause rejection or enforcement.

---

## 5. Campaign Naming Conventions (Professional Practice)

Consensus structure (Adamigo naming guide, Jul 2026; AdLibrary naming system, May 2026; DataAlly, Feb 2026):

- **Campaign**: `[Brand/Client]_[Objective]_[Theme/Offer]_[Date]` → `Acme_Sales_WinterSale_Dec2025`. Funnel prefixes for sorting: `1_TOF`, `2_MOF`, `3_BOF` (or `1_Awareness`…`3_Conversion`). Agencies prepend a 3–4 char client code: `[CLIENT]_[OBJ]_[AUD]_[PLACEMENT]_[PERIOD]`. Quarter-tag (`2026Q2`) or month (`MAY26`) for time-series filtering.
- **Ad set**: `[Audience]_[Geo]_[Placement]_[Bid strategy]` → `LAL1%_US_Feed_CostCap`; encode retargeting windows in the token (`RET-WEB-7D` vs `RET-WEB-30D`), budget tier or `_CBO`/`_ABO` flag, `Adv+` flag for automated variants.
- **Ad**: `[Hook]_[Format]_[Offer]_[Variant]` → `Testimonial_Video_20%Off_V1`. Format codes: V/S/C/Coll (video/static/carousel/collection); aspect ratio `9x16`, `1x1`; duration `15s`; CTA (`ShopNow`); asset IDs for large libraries; temporary test tags (`_TestA`, `_GreenBG`) removed after winner selection.

Rules:
- Use one separator consistently. Underscores simplify exports and parsing; spaces are valid but require correct URL encoding and can make downstream parsing less convenient. Document standardized abbreviations (`Conv`, `LAL`, `RT`) in a shared schema.
- 5–7 elements max per name; more is noise.
- No UTMs in ad names (they belong in the URL parameters field).
- Never change the convention mid-campaign — breaks historical reporting.
- For Advantage+ Sales campaigns (single consolidated structure), move audience info up from ad-set token to campaign token. (AdLibrary, 2026.)
- Purpose: names act as filterable data columns for pivot/reporting by hook, audience, offer — not just tidiness.

---

## 6. Testing → Scaling Campaign Structure (2025–2026 Best Practice)

### 6.1 The structural shift: consolidation wins

The 2010s playbook (many narrow ad sets, ad-set budgets, manual segmentation) now mechanically hurts delivery (Capconvert, May 2026, with Meta Help Center citations):

- **Learning-volume heuristic**: `50 optimization events in 7 days` is a longstanding planning rule, but current official delivery guidance does not publish that number as a universal threshold and Meta has tested other thresholds. The durable point is that splitting limited result volume across redundant ad sets reduces each set's opportunity to stabilize.
- **Auction overlap**: overlapping ad sets de-duplicate in auction — only the highest Total Value ad enters; the rest don't bid. Five overlapping ad sets buy one auction entry, not five× reach.
- **Advantage campaign budget only optimizes the pool it's given** — 2 broad healthy ad sets > 8 thin overlapping ones.
- Meta removed the counter-levers: ad-set max spend is an average, not a cap; ASC folded into default-on Advantage+ flow.

### 6.2 The standard two-campaign (or few-campaign) structure

Practitioner consensus (Ads Uploader 2026 vertical playbooks; Capconvert 2026; Loomer "Modern Approach," Sep 2025):

1. **Testing campaign when separation is useful** — use ad-set budgets for operational control or Meta Experiments for causal comparisons. Choose the number of cells and review window from expected volume, conversion delay, minimum detectable effect, and spend risk.
2. **Scaling campaign when consolidation is useful** — move or recreate validated concepts in a structure that can allocate sufficient volume. Reusing an existing post can preserve social proof, but leaving the original active can create overlap; decide from incremental reach and marginal economics. Use bid/cost controls only when their delivery tradeoff matches the business constraint.
3. E-commerce multi-SKU variant: dedicated campaign per hero product + one grouped CBO for the long tail + small ABO launches for new SKUs/angles. DTC single-product variant: exactly the 1-test + 1-scale pair above.
4. Prospecting vs retargeting separation is the one legitimate structural split beyond test/scale: pooling them lets Meta over-spend on cheap retargeting conversions and under-invest in cold growth. Many 2026 accounts run broad-only (Advantage+ audience) and let creative do the segmentation, with retargeting handled inside the same campaign — both patterns are in current use; separating funnel stages is still the defensible default for smaller budgets. [practitioner opinion diverges here]

### 6.3 Operating rules

- Evaluate campaign-level allocation and ad-set-level diagnostics together when campaign budget distributes spend; neither level is universally sufficient by itself.
- Avoid unnecessary edits while delivery is stabilizing, but only edits Meta treats as significant can return an ad set to learning. Use the live Delivery status and conversion lag rather than a fixed one-week clock.
- Size creative diversity from available delivery and concept coverage; a fixed 5–10 variants can fragment low-volume ad sets.
- Fixed edit percentages such as 20% are practitioner heuristics, not guaranteed learning boundaries. Monitor marginal economics and Delivery status after a controlled change.
- For consolidation, audit overlap and decision-useful result volume, merge redundant cells, preserve validated creative, choose the appropriate budget level, then establish a new baseline. The legacy 50-event and one-week rules can be scenario inputs but are not migration requirements.

---

## Sources

1. https://www.mbadv.agency/meta-ads/meta-ads-campaign-objectives — Meta Ads Campaign Objectives: 6 ODAX Guide 2026 (practitioner; cites Meta for Developers Dec 2021, Meta Help Center; accessed 2026-07-22)
2. https://www.get-ryze.ai/blog/meta-ads-campaign-objectives-explained — Meta Ads Campaign Objectives Explained 2026 (practitioner; accessed 2026-07-22)
3. https://www.jonloomer.com/advantage-plus-campaign/ — Advantage+ Campaign Creation: A Complete Guide, Jun 23 2025 (practitioner, Jon Loomer; accessed 2026-07-22)
4. https://www.jonloomer.com/qvt/advantage-sales-replaces-advantage-shopping/ — Advantage+ Sales Replaces Advantage+ Shopping, Mar 6 2025 (practitioner; seen in search results 2026-07-22)
5. https://www.jonloomer.com/advantage-plus-sales-app-leads-campaigns/ — Advantage+ Sales, App, and Leads Campaigns Are Coming, Feb 10 2025 (practitioner; seen in search results 2026-07-22)
6. https://www.jonloomer.com/advantage-campaign-budget-best-practices/ — Advantage Campaign Budget Best Practices, Mar 2025 (practitioner; seen in search results 2026-07-22)
7. https://www.jonloomer.com/meta-advertising-strategy/ — The Modern Approach to Meta Advertising Strategy, Sep 2 2025 (practitioner; fetch blocked 403, snippet only; accessed 2026-07-22)
8. https://bir.ch/blog/advantage-plus-sales-campaigns-guide — Understanding Meta's Advantage+ Sales Campaigns [2026 Guide] (practitioner, Birch; accessed 2026-07-22)
9. https://www.capconvert.com/learn/blog/meta-ads-account-structure-2026 — Meta Ads Account Structure in 2026 (practitioner; cites Meta Help Center pages on Advantage campaign budget, auction overlap, spend limits; accessed 2026-07-22)
10. https://adsuploader.com/blog/abo-vs-cbo — ABO vs CBO: Which Budget Strategy Actually Works in 2026 (practitioner; quotes Levi Steede, Depesh Mandalia, Barry Hott, Marin Istvanic, Andrew Foxwell team, Jon Loomer; accessed 2026-07-22)
11. https://www.adamigo.ai/blog/campaign-vs-ad-set-budgets-key-differences — Campaign vs. Ad Set Budgets (practitioner/benchmark claim of 27% lower CPR with CBO; seen in search results 2026-07-22)
12. https://segwise.ai/blog/abo-cbo-meta-ads-budget-strategies — ABO vs CBO in 2026 (practitioner; seen in search results 2026-07-22)
13. https://linkrunner.io/blog/meta-advantage-shopping-vs-manual-campaigns-for-app-growth-when-to-use-each — Advantage+ vs Manual Campaigns for Apps, Apr 2026 (practitioner; seen in search results 2026-07-22)
14. https://www.adamigo.ai/blog/meta-ad-naming-conventions-guide — Ultimate Guide to Meta Ad Naming Conventions 2025 (practitioner; accessed 2026-07-22)
15. https://adlibrary.com/posts/meta-ads-campaign-naming-conventions — Meta Ads Campaign Naming Conventions: The Complete System, May 2026 (practitioner; seen in search results 2026-07-22)
16. https://www.dataally.ai/blog/facebook-ad-naming-conventions-guide — Facebook Ad Naming Conventions Guide, Feb 2026 (practitioner; seen in search results 2026-07-22)
17. https://well-oiledmarketing.com/resources/social-media-advertising/metas-special-ad-categories/ — Navigating Meta's Special Ad Categories, Oct 2025 (practitioner; accessed 2026-07-22)
18. https://about.fb.com/news/2022/06/expanding-our-work-on-ads-fairness/ — official Special Ad Audience sunset announcement, reviewed 2026-07-22
19. https://wordjack.com/blog/a-quick-look-at-facebooks-special-ad-categories/ — A Quick Look at Facebook's Special Ad Categories, Nov 2024 (practitioner; seen in search results 2026-07-22)
20. https://faraday.ai/blog/facebook-special-audiences — Facebook special ad category overview, Dec 2024 (practitioner; seen in search results 2026-07-22)
21. https://lafactory.online/meta-ad-policies-account-bans/ — Meta Ad Policies and Account Bans, Jun 2026 (practitioner; seen in search results 2026-07-22)
22. https://www.adamigo.ai/blog/meta-ad-targeting-after-third-party-data-restrictions — Meta Ad Targeting After Third-Party Data Restrictions, Jun 2026 (practitioner; seen in search results 2026-07-22)
23. https://ppc.land/meta-blocks-political-ads-in-eu-as-ttpa-regulation-takes-effect/ — Meta blocks political ads in EU as TTPA takes effect, Oct 8 2025 (trade press; seen in search results 2026-07-22)
24. https://ppc.land/metas-value-rules-might-actually-cost-more-than-theyre-worth/ — PPC Land Meta timeline (incl. Sept 21 2025 unified Advantage+ API, value rules dates), Jan 2026 (trade press; seen in search results 2026-07-22)
25. https://www.geear.io/blog/how-credit-unions-can-still-see-results-with-social-media-advertising-in-2025 — Credit unions & first-party data under special ad restrictions, Jun 2025 (practitioner; seen in search results 2026-07-22)
26. https://github.com/pipeboard-co/meta-ads-mcp — Meta Ads MCP server docs, legacy→ODAX objective constant mapping, 2026 (technical/practitioner; seen in search results 2026-07-22)
27. https://getkoro.app/blog/campaign-objective-for-instagram-ads — Instagram Campaign Objectives: The ODAX Strategy, Jan 2026 (practitioner; seen in search results 2026-07-22)
28. https://lobehub.com/zh/skills/giacomoarienti-meta-ads-skill — meta-ads-expert skill notes (Advantage+ ~22% higher ROAS claim, Andromeda, CAPI/EMQ figures), Jul 2026 (practitioner, unverified claims flagged; seen in search results 2026-07-22)
29. https://blackpropeller.com/blog/meta-ads-manager-complete-guide/ — Meta Ads Manager in 2026: The Complete Guide, Jul 2026 (practitioner; seen in search results 2026-07-22)
30. https://www.digitaltwentyfour.com/learn/special-ads-categories/ — Special ads categories, Aug 2025 (practitioner; seen in search results 2026-07-22)

## Gaps

- **Official Meta Help Center pages could not be fetched directly** (facebook.com/business/help and developers.facebook.com return 400/403 to automated fetches). All UI mechanics (objective picker, Advantage+ flow, Advantage campaign budget eligibility, special ad category restrictions) are corroborated across 2+ independent 2025–2026 practitioner sources that cite the Help Center, but exact current label wording should be spot-checked in a live Ads Manager account.
- The "~4.6% CPA decrease" for Advantage campaign budget and "$20B run rate / 70% YoY" for Advantage+ Sales are **Meta's own aggregate marketing figures** (via secondary citations), not independent benchmarks.
- The "**~22% higher ROAS with Advantage+**" and "CAPI recovers 20–30% of lost conversions / EMQ >8.0" figures come from a third-party skill listing (source 28) — plausible but unverified against a primary study.
- The "27% lower cost per result with CBO" figure (source 11) is a vendor blog research summary without a visible methodology.
- Exact 2026 restriction matrices still vary by category, country, and campaign flow. Special Ad Audiences themselves are confirmed discontinued; verify the remaining controls in the live account.
- Availability of the **"Instagram profile" conversion location** under Traffic for follower-growth campaigns appears to vary by account/rollout — needs live-account verification.
- Exact per-objective optimization-goal **counts** (~3–6 per objective) are practitioner-compiled; Meta publishes no canonical list and options shift with rollouts.
- Benchmarks (CPL $23.10, median CPM $13.48, CTR 2.19%, CPC Traffic $0.70 / Leads $1.92) are 2026 third-party panels (WordStream, Digital Applied, Visible Factors) with differing compositions — directional only.
