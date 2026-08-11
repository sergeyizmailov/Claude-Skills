# Budgets, Bidding & Cost Benchmarks — Meta/Instagram Ads 2025–2026

Scope: Ads Manager budget mechanics (daily vs lifetime), minimum budgets, bid strategies, learning phase, cost benchmarks (CPM/CPC/CPL/CPA), cost drivers, and scaling strategy. Naming reflects the 2025–2026 UI (ODAX objectives, Advantage+ suite, "Advantage campaign budget" = former CBO). Where older terminology persists in sources, it is flagged.

---

## 1. Daily vs Lifetime Budgets

Set at the ad set level: **Ads Manager → Ad set → Budget & schedule → Budget → dropdown "Daily budget" / "Lifetime budget"**. With **Advantage campaign budget** (the current name for Campaign Budget Optimization / CBO), the budget moves to the campaign level: **Campaign → Advantage campaign budget toggle → Campaign budget**.

### Daily budget
- An *average* per day, not a hard cap. Meta can spend up to ~75% over the daily amount on high-opportunity days, but will not exceed 7× your daily budget per calendar week (Sun–Sat). (Older documentation said 25% daily overshoot; practitioners now observe the 75% swing — Foxwell Digital via LaFactory, 2026.)
- Best for: always-on campaigns, ongoing lead gen / e-commerce, anything you want to scale up or down day to day, and active reallocation between ad sets.
- Easier to scale: change the number and pacing adjusts immediately. Default recommendation for most advertisers.

### Lifetime budget
- A total amount across a fixed date range (requires an end date). It is a spending **cap over the schedule, not a guarantee of full spend** — Meta paces spend unevenly (some days more, some less) and optimizes for results within the cap; thin auctions, tight cost/bid caps, or narrow targeting can leave it underspent. Back-loaded spending (slow start, rush at the end) is normal, not a bug.
- The only budget type that unlocks **ad scheduling (dayparting)** — running ads only at specific hours/days, e.g. weekdays 9:00–17:00. Option appears under Budget & schedule only when lifetime is selected.
- Best for: fixed-window promotions (holiday sale, event, product drop) and dayparting needs.

### Gotchas (practitioner-observed, Tribe Up Academy / Jason Gan, Sep 2025)
- **Budget type is locked after publishing.** You cannot switch an ad set from daily to lifetime (or back). Fix: duplicate the ad set and set the correct type on the copy.
- **Extending a lifetime campaign often hurts performance.** Rolling a finished lifetime campaign into a new period tends to disrupt delivery learning; the extension frequently underperforms the original run. Recommended: launch the extension as a fresh daily-budget campaign.
- **Mid-flight lifetime increases require manual math** — you must recompute the total yourself (e.g., +20% of remaining days); easy to get slightly wrong.

---

## 2. Minimum Budgets Meta Requires

Meta enforces minimum budgets according to currency, billing event, objective, and account setup. Practitioner sources frequently quote `$1/day` for impression-optimized campaigns and `$5/day` for clicks or lower-frequency events, but current interfaces can accept different amounts. Treat the validation shown in the live budget field as authoritative.

The frequently quoted `daily budget ≥ 5× cost-per-result goal` is a delivery heuristic for constrained bidding, not a universal technical minimum. A tight cost goal with too little budget can suppress delivery, but increasing budget does not guarantee the target CPA.

### Volume-planning heuristic

Older Meta guidance and many practitioner playbooks use this planning model:

> **Illustrative daily budget = (Target CPA × 50) ÷ 7**

- This estimates the spend needed to buy 50 events at the target CPA; it does not prove that 50 events are the current threshold or that the target CPA is achievable.
- Use it as a capacity check, then size the test from available budget, expected CPA range, conversion delay, acceptable loss, and the number of independent cells.
- A common failure is fragmenting a fixed budget across redundant ad sets until none receives enough results to evaluate. Consolidate based on observed delivery, not an arbitrary account-wide ad-set count.

---

## 3. Bid Strategies (current UI naming)

Location: **Ad set → Optimization & delivery → Bid strategy** (with Advantage campaign budget ON, the strategy is set once at campaign level and applies to all ad sets). Older sources say "Optimization & Delivery → Cost Control / Bid Control" — same section, older labels.

| Current UI label | Old name | What it does | When to use |
|---|---|---|---|
| **Highest volume** (default) | Lowest cost | Spends your full budget getting the maximum number of results; no cost constraint | Default for ~most advertisers, most of the time. Prospecting, testing, any time you lack a proven CPA benchmark |
| **Cost per result goal** | Cost cap | You set a target average cost per result (e.g., $10/purchase); Meta aims to keep the *average* at/under it. Individual results can cost more or less. It is a goal, not a guarantee | When you know your break-even CPA and want stability while scaling. Set it realistically (near recent actual CPA) — too low and delivery chokes, learning phase drags, budget stops spending |
| **Bid cap** | Bid cap | Ceiling on Meta's auction bid, not a CPA ceiling | Advanced teams with a bidding model that connects impression value, estimated action rate, and allowable acquisition cost. `AOV ÷ target ROAS` estimates allowable purchase CPA, not the correct auction bid cap. An aggressive cap can suppress delivery |
| **Highest value** | (Value optimization) | With "Maximize value of conversions" performance goal: prioritizes high-value purchases over volume. Requires pixel/CAPI purchase events with value | E-commerce with variable basket sizes and enough value-event volume |
| **ROAS goal** | Minimum ROAS | With value optimization: Meta spends toward a target return (e.g., entering 1.100 = 110% ROAS target). Full budget delivery is **not** guaranteed | Mature purchase campaigns where profitability floor matters more than volume. Set a realistic goal or spend stalls |

Key behavior notes (Jon Loomer, Meta Help Center via LaFactory 2026):
- Goals are **averages over time**, not per-result caps; expect swings.
- All constrained strategies (cost per result goal, bid cap, ROAS goal) **slow or block delivery** if set aggressively, and make the learning phase harder to exit.
- "Don't get cute": setting caps unrealistically low doesn't trick the auction — you simply get no distribution.
- Not every strategy is available for every optimization event. Cost-per-result goal works for conversions, leads, link clicks, landing page views, app installs, engagement, video views, etc. Bid cap is available for most optimizations. ROAS goal requires value optimization.
- **2026 consensus default:** leave Highest volume + broad/Advantage+ audience; add cost controls only when scaling demands cost discipline (Andromeda-era practice — see §7).

---

## 4. Learning Phase

- Meta documents that ad sets enter learning, that performance is less stable during it, and that insufficient results can produce `Learning limited`. Current official delivery-status guidance does not publish `50 events in 7 days` or a universal `20–40%` CPA penalty.
- **Delivery column states:** "Learning" → "Learning limited" (not getting enough events) → active. Hover the Delivery column in Ads Manager for the exact status.
- `50/7` remains a useful legacy capacity heuristic. Meta has tested other thresholds, including a practitioner-observed `10 events in up to 3 days`; use the live Delivery status rather than asserting either threshold as current for every account.
- Meta says significant edits can return delivery to preparing or learning. Targeting, optimization, creative, bid, schedule, and budget changes can qualify, but Meta does not publish a universal 20% or 30% budget threshold. Check the live status after editing.
- **How to exit faster:**
  - Ensure the ad set has enough budget and time to generate a decision-useful number of results; use the legacy formula only as a scenario, not a requirement.
  - **Consolidate:** fewer ad sets, more events each (account consolidation is the core 2025–2026 structural advice).
  - If purchases are too rare, consider a higher-frequency event only when it remains meaningfully connected to business value; test against purchase optimization because cheaper proxy events can reduce buyer quality.
  - Minimize nonessential edits and observe at least one representative conversion-delay window. Seven days is a common starting window, not a universal waiting period.
  - Use Advantage+ / Advantage campaign budget to let Meta pool learning across audiences.

---

## 5. Cost Benchmarks (with sources & dates)

### 5.1 Platform-wide US benchmarks — WordStream/LocaliQ 2025 study
Sample: 1,000+ US campaigns (554 traffic, 726 leads), data window **April 1, 2024 – June 30, 2025**. Published 2025; figures are medians.

| Metric | Traffic campaigns | Leads campaigns |
|---|---|---|
| CTR | 1.71% (up from 1.57% YoY) | 2.59% |
| CPC | **$0.70** (down from $0.77) | **$1.92** (up from $1.88) |
| Conversion rate | — | 7.72% (down from 8.67%) |
| Cost per lead | — | **$27.66** (up 20.9% from $22.87) |

Industry extremes (same study): CPL from **$3.16** (Restaurants & Food) to **$76.71** (Dentists & Dental Services) — a 24× spread, so "average cost" without an industry qualifier is meaningless. Traffic CPC from **$0.34** (Shopping/Collectibles/Gifts) to **$1.22** (Finance & Insurance).
Do not conclude that Meta is categorically cheaper than Google from cross-platform averages: channel intent, attribution, industries, lead definitions, and sample populations differ. Use the figures only for their stated US campaign sample.

### 5.2 Instagram-specific 2026 directional ranges

Source: adlibrary.com, April 2026, aggregating other publications without a disclosed raw panel. Use these only as **low-confidence orientation**, never as a forecast or target.
| Metric | Low | Median | High |
|---|---|---|---|
| CPM | $3.50 | $7.80 | $16.00 |
| CPC (all clicks) | $0.20 | $0.85 | $2.40 |
| CPC (link clicks) | $0.40 | $1.20 | $3.50 |
| CPA (purchase) | $12 | $34 | $90+ (finance/B2B SaaS $80–120) |
| CPL | $4 | $10.50 | $28 |
| CPI (app install) | $0.80 | $2.20 | $6.00 |

### 5.3 By placement (vendor-aggregated, directional)
| Placement | Avg CPM | Avg CPC | Notes |
|---|---|---|---|
| Reels | $4–8 | $0.25–0.80 | Cheapest reach, discovery-mode users, highest relative CPA for conversions |
| Stories | $6–10 | $0.40–1.10 | Mid-intent; tolerates higher frequency before fatigue; good retargeting surface |
| Feed | $10–16 | $0.70–2.00 | Highest CPM but highest purchase intent; often best CPA |
| Advantage+ placements blend | ~$7–11 CPM | — | Meta shifts budget to cheapest-result placement |

A second vendor dataset (AdAmigo, 2026, methodology undisclosed) reports substantially different placement costs. Other publications range from roughly `$7` to `$15+` Instagram CPM. This disagreement is evidence that objective, geography, date, optimization, and placement mix dominate any platform-wide average; do not select or remove a placement from these values alone.

### 5.4 E-commerce / global panels
- Triple Whale (~35,000 brands, 2025 data, via AdMake AI, June 2026): global median **CPM $13.48–14.19 (+20% YoY)**; e-commerce **CPA (purchase) $38.17 (+1% YoY)**.
- US CPM estimates $20–23 (Madgicx/SuperAds 2025–2026 via AdMake AI).

### 5.5 By geography (AdAmigo, July 2026 — vendor-compiled "projections for 2026 based on late-2025 industry data"; methodology not disclosed, treat as directional [uncertain])
| Market tier | Country | Avg CPM | Avg CPC |
|---|---|---|---|
| Tier 1 | United States | $23.00 | $2.69 |
| Tier 1 | Australia | $18.50 | $2.10 |
| Tier 1 | Canada | $13.40 | $1.75 |
| Tier 1 | United Kingdom | $10.31 | $1.95 |
| Tier 1 | Germany | $10.05 | $1.45 |
| Tier 2 | France | $8.05 | $1.15 |
| Tier 2 | Spain | $5.80 | $0.85 |
| Tier 2 | Poland | $5.50 | $0.75 |
| Tier 2 | UAE | $6.50 | $1.40 |
| Tier 3 | Brazil | $4.20 | $0.35 |
| Tier 3 | Mexico | $4.50 | $0.45 |
| Tier 3 | India | $2.60 | $0.20 |
| Tier 3 | Indonesia | $2.80 | $0.18 |
| Tier 3 | Nigeria | $1.50 | $0.12 |

The table's claimed global average CPM is `$6.59`, but its methodology is undisclosed. Do not extrapolate that Kazakhstan, Uzbekistan, Ukraine, or another market behaves like a generic tier. No reliable CIS-specific panel was found. Meta suspended ads in Russia and ads targeting Russia in March 2022, so current Russia-market buying benchmarks are not comparable.

---

## 6. What Affects Costs

1. **The auction itself.** Meta describes delivery in terms of bid, estimated action rate, and ad quality ("total value"). The highest bid does not necessarily win. Creative affects predicted response and quality, but no universal CPM multiplier applies to a weak hook.
2. **Campaign objective.** Reach/awareness = cheapest CPM (US ~$10–15); traffic mid; leads/sales highest (US lead gen $25–40 CPM, sales $20–30) because Meta targets a smaller, higher-value pool. Choosing the wrong objective is a structural cost mistake.
3. **Seasonality.** Q4 (Oct–Dec) CPMs rise **40–80%** (adlibrary) / 60%+ (AdAmigo) as retail floods the auction; January resets lower (global median CPM $25.22 Nov 2025 → $15.74 Jan 2026 per AdAmigo). US election years add political spend shocks (2024: $3B+ digital political ads, half in the final 30 days). Counter-move: start holiday campaigns before Black Friday peak pricing. Note BFCM itself can paradoxically show cheaper CPMs on some datasets (Gupta Media observed 12–27% cheaper Instagram CPMs during BFCM 2024) — the *weeks around* it are the expensive part.
4. **Placement.** Reels often buys cheaper impressions than Feed in third-party datasets, but the gap and downstream CPA vary by account. Judge placement on the optimized event and quality, not CPM alone.
5. **Creative quality & fatigue.** Monitor hook/hold metrics, CTR, conversion efficiency, frequency, and control-vs-challenger performance. No single frequency or monthly creative count defines fatigue for every account.
6. **Audience breadth.** Narrow audiences can cost more and redundant ad sets can reduce learning opportunities, but the effect depends on auction, relevance, geography, and objective. Test broad delivery against coherent audience hypotheses rather than assuming one universal size threshold.
7. **Competition & industry.** Finance/insurance, dental, B2B SaaS auctions are inherently expensive (see CPL spread §5.1).
8. **Tracking quality.** iOS/SKAdNetwork gaps undercount conversions → the algorithm under-optimizes → phantom CPA inflation. Mitigation: Conversions API (CAPI). Broken pixel/CAPI data raises effective CPM.
9. **Geo quality.** Low-cost traffic can differ materially in fraud, intent, language, payment access, and serviceability. Validate downstream outcomes and fraud signals per market; do not assign a universal bot-rate premium to a geographic tier.

---

## 7. Scaling Strategies

### Vertical scaling (raise budget on winners)
- Practitioner playbooks commonly use 10–30% increments separated by several days. Meta does not document a universal safe percentage; treat this as a controlled-change heuristic.
- Scale only after performance covers a representative conversion-delay and business cycle, tracking is trustworthy, and marginal CPA/ROAS remains acceptable.
- Example paths such as `$100 → $130 → $170` illustrate gradual changes, not an endorsed schedule.
- Duplicating at a higher budget preserves the original configuration but starts a new delivery instance and can create overlap. It does not preserve learning or guarantee the winner's performance.

### Horizontal scaling (add new surfaces)
- Duplicate winners to **new audiences/geos**, new placements (Reels, Stories), new creator/UGC variants, new offers — not stacked narrow interests.
- 2025–2026 framing: horizontal = new *creative angles* and *markets*, since audiences are mostly broad/Advantage+ now. "Signals over segments."

### Current best practice with Advantage+ (2025–2026 consensus)
- **Consolidate.** Use the fewest campaigns and ad sets needed for distinct objectives, geographies, policy requirements, budgets, or experiments. Published percentage splits and "three campaigns max" are practitioner templates, not universal architecture.
- Meta-reported or vendor-reported Advantage+ improvements apply to specific test populations. Compare automation with an appropriate account-level baseline rather than assuming a fixed 10–20% CPA benefit or a minimum conversion threshold.
- Advantage campaign budget (CBO) by default; let Meta allocate between ad sets instead of micro-managing ABO budgets — unless you need fixed per-set spend for clean tests.
- Keep a **10–20% "R&D" carve-out** for creative testing (Tailored Edge Marketing, 2025): Explore (small ABO tests, judge hooks/CTR/ATC) → Prove (Meta Experiments A/B across one purchase cycle) → Scale (move winners into broad/Advantage+).
- Hybrid model is the norm: gradual vertical ramp + controlled horizontal expansion + automated rules.
- Value rules (launched June 2025) let you adjust bids by age/gender/geo/placement segments *without* fragmenting into separate ad sets — the modern replacement for manual geo-split scaling. Note they raise CPM on up-weighted segments by design.

---

## 8. How Much Budget to Start Testing

Derive test budget from business economics and uncertainty rather than a global monthly minimum:

1. Compute break-even CPA/CPL and the target range from margin, refunds, close rate, repeat value, and operating constraints.
2. Estimate a plausible CPA range from the account's own history or a closely matched benchmark.
3. Choose how many independent cells the test truly needs.
4. Fund enough expected outcomes to distinguish a useful signal while capping acceptable loss.
5. Observe at least the conversion delay plus enough weekday/weekend or purchase-cycle coverage for the business.

`$1,000–3,000/month`, `(target CPA × 50) ÷ 7`, seven days, and `3× target CPA with zero results` are common practitioner scenarios. They are not universal minimums or automatic kill rules. When the budget cannot support the desired outcome, first simplify the test, improve measurement/offer/landing page, or accept wider uncertainty; changing to a proxy event can change lead or buyer quality.

---

## Gotchas & Common Mistakes (quick list)

- Budget type (daily/lifetime) and optimization event are **locked after publish** — duplicate to change.
- Lifetime budget can back-load spend; extending one often kills performance.
- Cost per result goal / ROAS goal set too tight → delivery stops. It's an average goal, not a guarantee.
- Significant edits can return delivery to preparing or learning; there is no guaranteed seven-day clock for every ad set.
- Learning-phase CPA is often less stable, but no universal 20–40% inflation factor is established.
- Too many ad sets on a small budget → everything stuck in Learning Limited.
- Large budget changes can alter delivery; use controlled increments and watch marginal economics rather than relying on a universal 30% cutoff.
- Comparing your blended CPM to benchmarks without matching objective + placement + geo mix (Reels-heavy accounts look "cheap"; Feed-heavy US lead gen looks "expensive" — both can be healthy).
- Optimizing for link clicks in Tier-3 geos → bot traffic.
- Assuming a $50/day CPA holds at $500/day — warm audiences exhaust first; scale gradually.
- UI naming drift: "Lowest cost"/"Cost cap"/"Minimum ROAS" in pre-2024 sources = "Highest volume"/"Cost per result goal"/"ROAS goal" now; "CBO" = "Advantage campaign budget"; "Advantage+ shopping" = former ASC.

## Sources

1. https://tribeupacademy.com/meta-ads-budget-daily-vs-lifetime/ (practitioner, Jason Gan, Sep 2025) — daily vs lifetime behavior, dayparting, lock-in, extension problem. Accessed 2026-07-22.
2. https://www.stackmatix.com/blog/facebook-ads-minimum-budget-requirements (practitioner, 2026) — $1/$5 floors, 5× CPR rule, practical minimums, (CPA×50)/7 formula, scaling steps. Accessed 2026-07-22.
3. https://www.tryvizup.com/blog/meta-ads-minimum-budget-requirements-2026 (practitioner, May 2026) — cost per result goal 5× budget rule (search snippet). Accessed 2026-07-22.
4. https://coinis.com/how-to/best-way-to-minimum-budget-for-facebook-ads (practitioner) — $1–5/day floors citing Meta Help Center; practical-minimum formula (search snippet). Accessed 2026-07-22.
5. https://www.jonloomer.com/facebook-ads-bid-strategies/ (practitioner, Jon Loomer, updated Mar 2025; older UI labels "Lowest cost/Cost cap/Bid cap/Minimum ROAS") — mechanics, when-to-use, availability by optimization. Accessed 2026-07-22.
6. https://www.jonloomer.com/glossary/bid-strategy/ (practitioner, 2023) — current labels: Highest volume, Cost per result goal, Highest value, ROAS goal, Bid cap (search snippet). Accessed 2026-07-22.
7. https://lafactory.com/meta-bid-strategies/ (practitioner, June 2026) — synthesis citing Meta Business Help Center bid-strategy and auction docs, Foxwell Digital cost-controls analysis, 75% daily spend swing, current UI labels (search snippet). Accessed 2026-07-22.
8. https://www.jonloomer.com/qvt/is-the-learning-phase-changing/ (practitioner, Jon Loomer, May 2024) — 50 events/7 days standard; observed test of 10 events/3 days. Accessed 2026-07-22.
9. https://adlibrary.com/posts/meta-ads-learning-phase-50-events-guide (practitioner, May 2026) — 50 optimization events/week per ad set incl. pixel + CAPI events (search snippet). Accessed 2026-07-22.
10. https://www.wordstream.com/blog/ws/facebook-advertising-benchmarks (benchmark, WordStream/LocaliQ) — benchmark context; confirm edition, sample, market, and objective before use. Accessed 2026-07-22.
11. https://hawky.ai/blog/facebook-ads-cost (benchmark/practitioner, June 2026) — WordStream 2025 figures, CPL spread $3.16–$76.71, auction total-value formula, budget math table. Accessed 2026-07-22.
12. https://sepia-lab.com/en/blog/video-ad-benchmarks-by-industry (benchmark, June 2026) — WordStream 2025 sample sizes (554 traffic / 726 leads campaigns, Apr 2024–Jun 2025) and YoY deltas (search snippet). Accessed 2026-07-22.
13. https://www.mbadv.agency/meta-ads/meta-ads-cost-budgeting-and-bidding (benchmark/practitioner, June 2026) — CPL $22.87→$27.66 (+20.94%), CPC $1.88→$1.92, Google CPL comparison (search snippet). Accessed 2026-07-22.
14. https://adlibrary.com/posts/instagram-advertising-costs (benchmark/practitioner, April 2026) — Instagram 2026 CPM/CPC/CPA/CPL medians, placement-level costs, creative-fit discount, ASC 10–20% CPA reduction, $1–2K/mo testing floor, Q4 +40–80%. Accessed 2026-07-22.
15. https://www.adamigo.ai/blog/meta-ads-cpm-cpc-benchmarks-by-country-2026 (benchmark, vendor projections, July 2026 [uncertain methodology]) — geo CPM/CPC table, global $6.59 avg CPM, objective-level US CPMs, Q4 +60%, Nov→Jan CPM swing, bot-traffic note. Accessed 2026-07-22.
16. https://admakeai.com/blog/how-much-do-facebook-ads-cost (benchmark aggregator, June 2026) — Triple Whale ~35k-brand panel: CPM $13.48–14.19 (+20% YoY), ecom CPA $38.17; US CPM $20–23 (search snippet). Accessed 2026-07-22.
17. https://madgicx.com/blog/facebook-ads-cost (practitioner, Aug 2025) — 2025 averages $0.70 CPC / $12.74 CPM (search snippet). Accessed 2026-07-22.
18. https://www.guptamedia.com/social-media-ads-cost (benchmark, agency first-party data, Oct 2024) — Instagram avg CPM $7.43 (Fridays), BFCM CPMs 12–27% cheaper (search snippet). Accessed 2026-07-22.
19. https://admanage.ai/blog/how-much-do-instagram-ads-cost (practitioner, April 2026) — 2025 Instagram averages $1.31 CPC / $15.26 CPM in some datasets (search snippet). Accessed 2026-07-22.
20. https://deepsolv.ai/blog/budget-scaling-for-meta-instagram-ads-in-2025 (practitioner, 2025) — vertical scaling 20–30%/3–5 days, no scaling during learning, hybrid model (search snippet). Accessed 2026-07-22.
21. https://dancingchicken.com/post/scaling-meta-ads-in-2025-vertical-strategies-explained (practitioner, 2025) — vertical scaling preconditions: 50+ weekly conversions, 20% every 3–5 days (search snippet). Accessed 2026-07-22.
22. https://tailorededgemarketing.com/scaling-facebook-ads-without-losing-roi-a-practical-playbook-for-2025/ (practitioner, Aug 2025) — Explore/Prove/Scale framework, 10–20% R&D carve-out, 20–30% ramps, horizontal = geos/placements/creators (search snippet). Accessed 2026-07-22.
23. https://getadplus.com/tools/ad-budget-calculator/meta-ads-for-ecommerce (practitioner, 2025) — 60–70% ASC / 15–20% testing / 10–15% retargeting split, 15–30 creatives/month (search snippet). Accessed 2026-07-22.
24. https://viralbrandworks.com/blogs/news/meta-s-andromeda-update-2025 (practitioner, Oct 2025) — Andromeda-era structure: one CBO campaign per objective, broad/Advantage+ defaults, no caps unless strict logic, creative stacking (search snippet). Accessed 2026-07-22.
25. https://theoptimizer.io/blog/meta-ads-value-rules-how-they-work-when-they-help-and-when-theyll-drain-your-budget (practitioner, June 2026) — value rules launch June 2025, segment-level bid adjustments (search snippet). Accessed 2026-07-22.
26. https://www.facebook.com/business/help/190490051321426?id=629338044106215 (official, Meta Business Help Center — campaign budget article; URL seen in search results, page itself not fetchable from this environment — HTTP 400). Accessed 2026-07-22.
27. https://www.wordstream.com/blog/ws/facebook-advertising-benchmarks (benchmark, WordStream legacy 2017 study: avg CPC $1.72, CPA $18.68, CVR 9.21% across 18 industries) — included only as historical baseline; superseded by source 10. Accessed 2026-07-22.

## Gaps

- Some Meta Business Help pages remain login- or JavaScript-gated. Current official public pages confirm that daily budgets are averages, Meta can spend above them on individual days, campaigns should receive sufficient budget over at least seven days, and significant edits can affect learning. Exact `$1/$5`, `5× CPR`, `50/7`, and budget-edit percentage claims were not confirmed as universal current rules and remain practitioner/legacy guidance.
- **Exact current daily-budget floor for conversion campaigns**: sources conflict ($1 vs $5/day). The $5 figure is the widely cited rule of thumb; the 2026 UI may accept $1.
- **Learning phase threshold**: whether the 10-events/3-days variant Loomer observed in 2024 has rolled out broadly by 2026 is unconfirmed; Meta documentation reportedly still said 50/7.
- **CIS-region benchmarks**: no credible public CPM/CPC dataset for Ukraine/Kazakhstan/Uzbekistan etc. found. Russia is excluded from Meta advertising since March 2022.
- **AdAmigo geo table (source 15)** is vendor-compiled "projections for 2026" with undisclosed methodology — directional only; US $23 CPM sits at the high end of other estimates ($13–23).
- **WordStream 2025 Instagram-vs-Facebook split**: the LocaliQ 2025 study covers Facebook placements; Instagram-only medians by industry from a comparably large panel were not found (Instagram figures rely on adlibrary/AdAmigo aggregates).
- **"75% daily overspend" rule** rests on practitioner reporting (Foxwell via LaFactory); Meta's current official daily-spend flexibility wording not directly verified.
