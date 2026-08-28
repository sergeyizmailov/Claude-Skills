# Campaign Objectives & Structure for Instagram-Focused Meta Ads (2025–2026)

Scope: six ODAX objectives, Advantage+ vs manual setup, campaign vs ad-set budgets, special ad categories, naming conventions, testing-to-scaling structure. UI reviewed 2026-07-22. Treat Meta's current documentation or the live account as authoritative; practitioner sources are labeled as heuristics.

---

## 1. The Six ODAX Objectives

**The objective is a delivery signal, not a funnel label.** Meta optimizes toward the event you name,
so it decides who your ad reaches. Picking "Traffic" when the goal is purchases buys click-prone users
and starves the purchase model — the single most expensive objective error, and it does not surface as
a rejection or a warning, only as bad economics. Choose by the event you want, never by where the
campaign sits in a funnel diagram.

### 1.1 Background: what ODAX changed

- ODAX = "Outcome-Driven Ad Experiences." Announced Meta for Developers blog **Dec 21–22, 2021**; rolled out through 2022; **exclusive campaign-creation path since 2023**. (MB Adv ODAX guide, Jun 2026; Meta for Developers via secondary citation.)
- Consolidated **11 legacy objectives** (3 funnel banners: Awareness/Consideration/Conversion) into **6 flat outcomes**: **Awareness, Traffic, Engagement, Leads, App promotion, Sales**. Banner framing is gone from the UI — any "consideration campaign" article is pre-2023.
- Legacy → ODAX map: Brand Awareness/Reach → **Awareness**. Traffic → **Traffic** (unchanged). Engagement/Video Views/**Messages** → **Engagement** (Messenger/IG Direct/WhatsApp campaigns live here now). Lead Generation → **Leads**. App Installs → **App promotion**. Conversions/Catalog Sales → **Sales** (catalog vs website moved into ad-set conversion-location settings). Store Traffic → **sunset** (new campaigns disabled Jan 2024, delivery halted H2 2024, no replacement).
- **Objective locks after launch** — some edits create a new ad, trigger review, or reset learning; changing it needs a new campaign.
- Marketing API: legacy constants (`BRAND_AWARENESS`, `LINK_CLICKS`, `CONVERSIONS`, `APP_INSTALLS`, etc.) 400-error on new campaigns; use `OUTCOME_AWARENESS/TRAFFIC/ENGAGEMENT/LEADS/APP_PROMOTION/SALES`. Some dashboards still label Sales "Conversions" (legacy, same thing). (pipeboard-co/meta-ads-mcp GitHub, 2026.)

### 1.2 Per-objective breakdown

| Objective | Optimizes for (~goal count) | Conversion locations / sub-goals | Best for | Key trap / requirement |
|---|---|---|---|---|
| **Awareness** | ~5: Reach, Impressions, Ad recall lift (recall within 2 days), ThruPlay (≥15s or full video if shorter), 2-sec continuous views (≥50% pixels onscreen) | None (visibility only) | Brand launches, video distribution, max reach | Only objective with no conversion location; wrong choice if any downstream action is the goal. (MB Adv 2026; Get-Ryze 2026.) |
| **Traffic** | ~5: link clicks, landing page views, Messenger conversations, **Instagram profile visits**, calls | Website, App, Instagram profile, calls | Sending qualified clicks off-platform; building retargeting pools | Optimizes clicks, not the post-click outcome. Profile visits = closest official follower-growth lever (§1.3) |
| **Engagement** | Post interactions, messaging conversations, video views, page activity | On-post, Messenger, **Instagram Direct**, WhatsApp, on-video, on-event | DM conversations, social proof, content interaction, page/profile growth | Absorbed legacy Messages objective; home of **click-to-DM ads**; also covers social proof (post likes/comments) |
| **Leads** | Instant Form submits, website lead events, Messenger conversations, calls | Instant Forms, Website, Messenger, Calls, App | Service businesses, B2B, list-building, high-ticket | Instant Forms = native, cheap, lower quality; Website needs a working Pixel lead event; **Conversion leads** needs CRM + Conversions API feedback. Median CPL **$23.10** (WordStream 2026 panel; CPC $1.92, CVR 8.25%) |
| **App promotion** | ~3: installs, app events, value | Mobile app only | Any install/in-app goal | Closed mandate — non-negotiable if the conversion event is an install |
| **Sales** | Purchase, Add to Cart, Initiate Checkout, catalog sales, messaging conversions, value (ROAS); event requirements differ by app/shop/catalog/messaging flow | Website, App, Website+App, Messenger/WhatsApp | E-commerce purchases, subscriptions, bottom-funnel revenue | A temporary shift to a higher-frequency event can raise volume but train toward weaker intent — test, don't default. Catalog ads (formerly "Catalog Sales"/DPA) configure here |

### 1.3 Picking an objective for typical Instagram goals

| Goal | Recommended objective | Why / caveats |
|---|---|---|
| **More Instagram followers** | Traffic → "Instagram profile" location, or Engagement | No "follows" optimization event exists; profile visits are the proxy, so expect modest follow-through — creative does the real work. [uncertain: IG-profile location availability varies by account/region, 2025–26] |
| **DMs (Instagram Direct / Messenger / WhatsApp)** | **Engagement** → "Messaging apps" location | Post-ODAX home of click-to-message ads; Leads also supports Messenger/IG Direct with automated Q&A (conversations vs qualified contact capture). |
| **Website sales (e-commerce)** | **Sales** with Purchase event via Pixel + CAPI | Don't substitute Traffic "to be safe" — finds clickers, not buyers. |
| **Lead forms** | **Leads** → Instant Forms (volume) or Website lead event (quality) | Conversion-leads optimization needs CAPI + CRM feedback. |
| **App installs** | **App promotion** | Only objective that supports installs. |

Common mistakes (Get-Ryze 2026, MB Adv 2026):
1. Sales for cold zero-pixel audiences → starved learning. Counter-view: even new brands should often start on Sales if tracking is set up — Awareness trains nothing useful (Koro 2026).
2. Traffic when the real goal is leads/sales → window shoppers.
3. Switching objectives mid-flight → learning reset (and it's not even possible — requires a new campaign).
4. Creative misaligned with objective (hard-sell in Awareness campaigns).
5. Underfunding/fragmentation: budget must fit the outcome, conversion delay, and decision size. No universal `50 conversions/week` or `$5–10/day` rule across objectives, markets, economics.

---

## 2. Advantage+ Sales (formerly Advantage+ Shopping) vs Manual Campaigns

### 2.1 The 2025 restructuring — what actually changed

- **ASC is gone.** In 2025 Meta renamed/replaced Advantage+ Shopping Campaigns with **Advantage+ Sales campaigns** inside one streamlined **"Advantage+ campaign setup"** flow (scope in table below). (Jon Loomer, "Advantage+ Campaign Creation: A Complete Guide," Jun 23, 2025; "Advantage+ Sales Replaces Advantage+ Shopping," Mar 6, 2025.)
- Old ASC features did **not** carry over: no targeting inputs, locked placements, single ad set, existing-customer budget cap. Loomer: effectively a manual Sales campaign that never touches the defaults.

| Element | Old (ASC / manual) | New (Advantage+ setup, 2025) |
|---|---|---|
| Creation prompt | Automated-vs-manual choice upfront | Removed — straight into creation |
| Scope | ASC only | **Sales, Leads, App promotion** only; other objectives keep the older tailored flow |
| "Advantage+" toggle basis | N/A | 3 elements: **Budget** (Advantage campaign budget on), **Audience** (Advantage+ audience with suggestions), **Placements** (Advantage+ placements). Untouched defaults = "on"; restrictive edits = "off" + lower **Campaign/Opportunity score** (0–100) |
| Advantage campaign budget default | Off | **On** |
| Ad cap | 150 ads total (ASC) | Max 50/ad set (Meta discourages >~6 active); old total cap gone. [Birch 2026 cites "150 total, 50/set" — total-campaign cap uncertain] |
| API | — | Sept 21, 2025: **unified API structure for Advantage+** across sales/app/leads (PPC Land, 2026) |

### 2.2 Pros / cons

Advantage+ (default/automated) pros:
- Less setup; Meta's aggregate data favors advertisers using defaults. Advantage+ Shopping/Sales surpassed a **$20B annual revenue run rate, ~70% YoY growth (Q3 2024 earnings)** — where Meta invests.
- Best with ~50+/week conversion volume, 5–10+ creative variants, clean Pixel + CAPI.
- Budget flows to what works in real time (with Advantage campaign budget).

Cons / where manual still wins:
- Reduced diagnostic visibility — harder to isolate which audience/placement drove results.
- Broad-by-default can waste spend before the algorithm finds buyers — Fer Rivero (via Birch 2026): minimal-input Advantage+ produced "complete randomness in terms of CPR"; he scales proven winners with automation, not discovers them.
- Creative-testing reads muddy — no equal spend per ad. Special Ad Categories restrict targeting by category/country; verify options in the live flow rather than assuming automation is unavailable.

### 2.3 Current best practice (2025–2026 consensus)

- Mixed manual/Advantage+ preserves controlled testing while automating delivery — not universal; pick the minimum structure that answers the current question without fragmenting data. [practitioner strategy]
- Trust automation for budget scaling; keep human control over creative testing and offer strategy — "creative is the new targeting" inside a broad/Advantage+ structure.
- Consolidate: fewer campaigns, fewer ad sets, more ads per ad set (see §5).

---

## 3. Advantage Campaign Budget (CBO) vs Ad-Set Budgets (ABO)

### 3.1 Naming and mechanics

- **Advantage campaign budget** (formerly CBO; UI also shows "Advantage+ campaign budget"): one campaign-level budget, distributed across ad sets toward best predicted results.
- **Ad set budgets** = ABO; toggle Advantage campaign budget OFF at campaign level. Still labeled "ad set budgets" in the UI.
- Meta's aggregate claim: Advantage campaign budget **decreases CPA ~4.6% on average** vs ad-set budgets (treat directionally). (Capconvert 2026, citing Meta Help Center.)
- Eligibility: every ad set must share the **same budget type** (daily vs lifetime), **same bid strategy**, **standard delivery**. (Capconvert 2026; Jon Loomer "Advantage Campaign Budget Best Practices," Mar 2025.)
- Gotcha (Loomer, Jun 2025): with it on, **Cost Per Result Goal and budget scheduling** move from ad-set to campaign level — confusing for single-ad-set campaigns.
- **Ad set spend limits** (min/max): the max is an **average, not a hard daily cap** — Meta can exceed it on any day if the average holds. Overusing minimums "defeats the whole purpose" (Loomer) — use ad set budgets instead if you don't trust the algorithm to allocate.
- Budget edits reset learning only when Meta deems them significant; 20%/30% thresholds are practitioner heuristics, not published cutoffs — use live delivery status and controlled increments.

### 3.2 When to use which (practitioner framework — Ads Uploader 2026, corroborated by Segwise 2026, Adamigo 2026)

| | ABO (ad set budgets) | CBO (Advantage campaign budget) |
|---|---|---|
| Control | Full manual | Algorithmic |
| Spend distribution | Equal per ad set (forced) | Performance-based; often ~80/20 Pareto split |
| Management load | Daily hands-on | Weekly checks |
| Best for | Tests needing ad-set budget control; operational splits still do not guarantee equal delivery or causal reads | Allocation across ad sets when the performance goal and economics are shared |
| Failure mode | Losses compound if creative hit rate is low | Can starve promising ad sets after a few hours on small budgets; can't fix weak creative |

- **Hybrid trick**: CBO + per-ad-set **minimum daily spend** for ~1 week (forces initial testing fairness), then **remove the minimums** and let CBO optimize. Keeping minimums forever = ABO with extra steps.
- Sizing heuristics: daily budget ~2× target CPA for an ABO test; `(target CPA × 50) ÷ 7` as a legacy volume-planning model. Neither guarantees learning completion — size from acceptable test risk, conversion delay, expected variance, and decisions the test must support.
- Benchmark claim: CBO averages **~27% lower cost per result** than ABO in multi-audience setups (Adamigo, Jul 2026 — directional).

---

## 4. Special Ad Categories

Four categories, **self-declared at campaign level** (dropdown at the top of campaign creation): **Financial Products and Services** (renamed/broadened from "Credit" **Oct 2024**), **Employment**, **Housing**, **Social Issues, Elections, or Politics**. Declaring when applicable is mandatory — failure to declare is itself a policy violation. **EU:** all social-issue/election/political ads blocked since Oct 2025 (TTPA) — `00` §4.

**The full treatment is canonical in `07` §4**: the restriction matrix by category/country, the 15-mile US-only caveat, authorization + "Paid for by" + 7-year Ad Library rules, the 2025-01-13 data-sharing restrictions, and the Special Ad Audiences discontinuation. Route there; do not re-derive the matrix here.

---

## 5. Campaign Naming Conventions (Professional Practice)

Consensus structure (Adamigo naming guide, Jul 2026; AdLibrary naming system, May 2026; DataAlly, Feb 2026):

| Level | Template | Example | Extra tokens |
|---|---|---|---|
| Campaign | `[Brand/Client]_[Objective]_[Theme/Offer]_[Date]` | `Acme_Sales_WinterSale_Dec2025` | Funnel prefix `1_TOF`/`2_MOF`/`3_BOF` (or `1_Awareness`…`3_Conversion`); agency client code `[CLIENT]_[OBJ]_[AUD]_[PLACEMENT]_[PERIOD]`; quarter (`2026Q2`) or month (`MAY26`) tag |
| Ad set | `[Audience]_[Geo]_[Placement]_[Bid strategy]` | `LAL1%_US_Feed_CostCap` | Retargeting window (`RET-WEB-7D` vs `RET-WEB-30D`); budget tier or `_CBO`/`_ABO`; `Adv+` flag for automated variants |
| Ad | `[Hook]_[Format]_[Offer]_[Variant]` | `Testimonial_Video_20%Off_V1` | Format codes V/S/C/Coll (video/static/carousel/collection); ratio `9x16`/`1x1`; duration `15s`; CTA (`ShopNow`); asset IDs for large libraries; temp tags (`_TestA`, `_GreenBG`) removed after winner |

Rules:
- One separator consistently — underscores simplify exports/parsing; spaces need URL encoding. Document abbreviations (`Conv`, `LAL`, `RT`) in a shared schema.
- 5–7 elements max per name. No UTMs in ad names (belongs in URL parameters field). Never change convention mid-campaign — breaks historical reporting.
- Advantage+ Sales (single consolidated structure): move audience info up from ad-set token to campaign token. (AdLibrary, 2026.)
- Names are filterable data columns for pivot/reporting by hook/audience/offer — not just tidiness.

---

## 6. Testing → Scaling Campaign Structure (2025–2026 Best Practice)

### 6.1 The structural shift: consolidation wins

The 2010s playbook (many narrow ad sets, ad-set budgets, manual segmentation) now mechanically hurts delivery (Capconvert, May 2026, with Meta Help Center citations):

- **Learning-volume heuristic**: `50 optimization events in 7 days` is a longstanding planning rule; not a published universal threshold (Meta has tested others). Durable point: splitting limited result volume across redundant ad sets still reduces each set's chance to stabilize.
- **Auction overlap**: overlapping ad sets de-duplicate in auction — only the highest Total Value ad enters; the rest don't bid. Five overlapping ad sets buy one auction entry, not 5× reach.
- **Advantage campaign budget only optimizes the pool it's given** — 2 broad healthy ad sets beat 8 thin overlapping ones.
- Meta removed the counter-levers: ad-set max spend is an average, not a cap; ASC folded into default-on Advantage+ flow.

### 6.2 The standard two-campaign (or few-campaign) structure

Practitioner consensus (Ads Uploader 2026 vertical playbooks; Capconvert 2026; Loomer "Modern Approach," Sep 2025):

1. **Test when separation is useful** — ad-set budgets for operational control, or Meta Experiments for causal comparisons. Size cell count and review window from expected volume, conversion delay, minimum detectable effect, spend risk.
2. **Scale when consolidation is useful** — move or recreate validated concepts into a structure that can allocate sufficient volume. Reusing a post preserves social proof but risks overlap if the original stays active — decide from incremental reach and marginal economics; use bid/cost controls only when the tradeoff fits the constraint.
3. E-commerce multi-SKU variant: dedicated campaign per hero product + one grouped CBO for the long tail + small ABO launches for new SKUs/angles. DTC single-product variant: just the 1-test + 1-scale pair.
4. Prospecting vs retargeting separation is the one other legitimate structural split: pooling lets Meta over-spend on cheap retargeting and under-invest in cold growth. Many 2026 accounts run broad-only (Advantage+ audience) with retargeting inside the same campaign; separating funnel stages remains the defensible default for smaller budgets. [practitioner opinion diverges here]

### 6.3 Operating rules

- Evaluate campaign allocation and ad-set diagnostics together — neither alone is sufficient when campaign budget distributes spend.
- Avoid unnecessary edits during stabilization; only edits Meta treats as significant reset an ad set to learning. Use live Delivery status and conversion lag, not a fixed one-week clock.
- Size creative diversity from available delivery and concept coverage — a fixed 5–10 variants can fragment low-volume ad sets.
- Fixed edit percentages (e.g. 20%, §3.1) aren't guaranteed learning boundaries — monitor marginal economics and Delivery status after a controlled change.
- For consolidation: audit overlap and decision-useful result volume, merge redundant cells, preserve validated creative, choose the appropriate budget level, establish a new baseline. Legacy 50-event/one-week rules are scenario inputs, not migration requirements.

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
