# Meta Ads Manager — Interface & Navigation (2025–2026)

Scope: Ads Manager web UI, 2025–2026 — layout, Campaign/Ad set/Ad hierarchy, creation flow, table controls, metrics/columns, breakdowns, date ranges, reporting, automated rules, drafts/publish, billing, spending limit, account quality.

Access: direct `adsmanager.facebook.com`; via Business Suite menu; mobile app exists, not feature-complete vs desktop.

## 1. Overall layout

Outdated-UI warning: any guide/screenshot showing Power Editor or 11 objectives is stale (Power Editor merged 2017–2018; objectives consolidated into ODAX 2021–2022). Editing pane opens via row checkbox + **Edit** [uncertain — exact pane behavior/placement varies by rollout].

---

## 2. The three levels: Campaign / Ad set / Ad

Three-level account structure. Over-segmentation (too many ad sets splitting budget) starves the learning phase — common structural mistake.

### Campaign level
- **Objective** (ODAX, six options — §3)
- **Buying type**: Auction (default) or Reservation (predictable delivery, eligible accounts only)
- **Special Ad Categories**: financial products/services, employment, housing, social issues/elections/politics — targeting/feature restrictions vary by category/country/flow
- **Advantage campaign budget** (formerly CBO) — set at campaign level, auto-distributed across ad sets
- **A/B test** toggle
- Campaign name; Advantage+ vs manual campaign

### Ad set level
- **Performance goal**/conversion event (maximize conversions, link clicks, LPV, reach, impressions — varies by objective)
- **Budget & schedule** (if Advantage campaign budget OFF): daily/lifetime, start/end date. Daily budgets average across a week — Meta may spend up to **~75% more** on high-opportunity days (Shopify; [uncertain], not guaranteed)
- **Audience**: Advantage+ audience (AI-driven, inputs are "suggestions"), Custom, Lookalike (1–10% similarity), detailed targeting (age/gender/location/language/interests/demographics/behaviors). Estimated audience size shown in side column.
- **Placements**: Advantage+ (auto: FB/IG/Messenger/Audience Network/Threads) or Manual
- **Optimization & delivery**: attribution setting (default 7-day click/1-day view), bid/cost controls, ad scheduling (lifetime budgets only)

### Ad level
- **Identity**: FB Page + IG account the ad runs from
- **Format**: single image/video, carousel, collection; flexible format
- **Creative**: media, primary text, headline(s), description, CTA, destination URL + UTM; multiple text/headline options (Meta rotates them)
- **Tracking**: pixel event / URL parameters
- Placement-level preview in sidebar

---

## 3. "+ Create" button and campaign creation flow

Entry: **Ads Manager → Campaigns tab → green "+ Create"** (top-left of table).

Modes:
- **Guided creation** — step-by-step, for new advertisers
- **Quick creation** — shell campaign + bulk ad sets/ads via table, for experienced advertisers

Guided flow:
1. **Choose objective** — six ODAX: **Awareness** (reach/impressions/recall), **Traffic** (clicks/LPV to site/app/Messenger), **Engagement** (reactions/comments/shares/video views/messages), **Leads** (instant forms/website conversions/calls), **App promotion** (installs/in-app events), **Sales** (purchases/conversions, website or catalog). Also: buying type, **Advantage+ campaign** (full automation: audience/placements/budget/creative/destination) — Meta claims ~**20%** better cost per action for Advantage+ sales (Shopify citing Meta, 2026) [uncertain — vendor-reported]. "Single-step Advantage+" automates one component only.
2. **Campaign settings** — fields per §2 Campaign level, + amount if Advantage campaign budget on.
3. **Ad set** — fields per §2 Ad set level, + conversion location and pixel/conversion event.
4. **Ad** — fields per §2 Ad level; live preview per placement.
5. **Review and publish** — final check → **Publish**. Review typically minutes to hours, officially **up to 24 hours** (Shopify, 2026).

Gotchas:
- Objective determines available destinations/goals/events/metrics downstream — verify combinations in the live flow.
- Some edits are "significant" and return an ad set to learning — inspect Delivery status after publishing, don't assume uniform effect.
- Special Ad Category campaigns have restricted targeting/features — verify category, country, live UI.

---

## 4. Campaigns table — key buttons and controls

Toolbar (some buttons need a row checkbox):
- **"+ Create"** — new campaign (§3)
- **On/off toggle** — per-row, pauses/resumes without deleting. Upper-level toggle cascades down (campaign off → ad sets/ads off).
- **Duplicate** — copies campaign/ad set/ad (optionally into another campaign, with/without results). A/B test workflow: Duplicate → "New A/B test" (HubSpot, 2025).
- **Edit** — editing pane, bulk edit across selected rows.
- **Delete** — stops delivery, generally cannot be re-enabled (historical data stays in reports). Turn off instead if you may want it back.
- **A/B Test** button — launches experiment from selected campaign/ad set (also via ⋯ → Duplicate → New A/B test). Managed under **Experiments**; results show statistical confidence + declared winner if conclusive.
- **Rules** — dropdown on selected items → create/manage rules (§9).
- **⋯ (More)** per row — duplicate variants, history/changelog, share link, etc.
- **Delivery column**: Active, In review, Scheduled, Not delivering, Rejected, Completed, Learning, Learning limited, etc. No official universal "50 weekly events" threshold published — legacy heuristic; use live status.

---

## 5. Columns and metrics

### Customizing columns
**Columns dropdown → Customize Columns** — search/add, drag to reorder, **save as preset**. Built-in presets: Performance, Performance and clicks, Delivery, Engagement, Video engagement, App engagement, + others (varies by rollout).

### Metric gotchas
- **Results**: DIFFERENT event per campaign (purchase/lead/link click/ThruPlay by objective) — check what "result" means per row.
- **Frequency**: fatigue above ~5–8 (AdManage: risk above 8–9; "optimal" 3–7, campaign-length dependent).
- **CPM**: driven by targeting breadth/competition/seasonality (Q4 spikes **50–100%** commonly reported).
- **"CPC (all)"/"CTR (all)"**: include reaction/comment clicks, look deceptively cheap — use LINK-click variants for creative evaluation. Placement CTR (AdManage 2025-11): FB Feed ~0.9%, IG Feed ~0.5%, Stories ~0.3%.
- **ROAS**: needs supported conversion-value measurement per conversion location (web = Pixel/CAPI; app/shop differ); "Purchase ROAS" ≠ "Website purchase ROAS".
- **LPV < link clicks**: large click→LPV drop = slow landing page, not creative.
- **Quality/Engagement/Conversion-rate rankings**: per-ad vs competitors for same audience (Above/Average/Below).

### Benchmarks (WordStream/LocaliQ 2025 study; US, Apr 2024–Jun 2025; medians)
- Traffic (n=554): CTR 1.71%, CPC $0.70
- Leads (n=726): CTR 2.59%, CPC $1.92, conversion rate 7.72%, cost/lead $27.66
- Industry spread (traffic): Shopping/Collectibles & Gifts CTR 4.13%/CPC $0.34 (best); Travel CTR 2.76%/CPC $0.51; Finance & Insurance CTR 0.98%/CPC ~$1.22 (expensive)
- Alternative averages (Birch via Shopify, 2026): CPM $13.86, CPC $0.74, CPE $0.07, CPL $13.39, CPI $2.30 — rough cross-source reference, methodology differs
- Never compare traffic-objective CPC to leads-objective CPL.

Starter column set: Results, Cost per result, Amount spent, CTR (link), CPC (link), CPM, Frequency, Reach, Impressions, + ROAS/Cost per purchase for sales campaigns.

---

## 6. Breakdowns and filters

### Breakdown dropdown (next to Columns)
Seven categories (Jon Loomer, 2025-12):
- **Time**: Day, Week, 2 Weeks, Month
- **Demographics**: Age, Gender, Age and Gender, Audience segments (Engaged/Existing customers/New audience — Sales campaigns only, requires defined segments)
- **Geography**: Country, Region, ...
- **Delivery**: Placement, Placement and device, Platform, Device platform, Time of day...
- **Action**: Conversion device, Destination, Carousel card, Post reaction type, Video view type, Video sound, Brand, Category, Messaging purchase source, Messaging outcome destination
- **Dynamic creative element**: Image/video/slideshow, Text, Headline
- **Creative**
- Bonus: Value rules (bid-adjustment), Attribution (breakdown by attribution setting; First conversions vs All other conversions)

High-value uses (Loomer):
- Placement breakdown exposes junk distribution: Audience Network inflating cheap link clicks; Audience Network Rewarded Video inflating ThruPlays (results > reach = tell); "Ads on Facebook Reels" soaking Awareness-reach budgets.
- Age/Gender exposes over-spend on cheap-action demographics for non-purchase goals (example: 70% of budget on 55+ for registration optimization; value rules cut it to 17%).
- Country breakdown: Meta allocates multi-country budget by cheapest results, not evenly.

Limits: only one breakdown at a time in main table (Ads Reporting allows cross-segmentation, e.g. Age × Gender); breakdowns don't backfill cleanly across all metrics [uncertain].

### Filters
Name/ID search, delivery status, objective, metric thresholds ("Selection" filter, e.g. Cost per result > X). Saved filters available; filtering only hides rows, doesn't alter data.

---

## 7. Date presets and charts

Preset list UI-trivial (rollout-dependent); **Compare** toggle shows % change per metric. Gotcha: default Last 7 days view is a classic misread — judge on **≥2 weeks** before decisions (Shopify, 2026).

---

## 8. Custom reports (Ads Reporting)

Path: **All tools → Ads Reporting** (also via Reports control in table).
- Pick metrics, add breakdowns, choose visualization (table/bar/line/pie) or pivot layout.
- Save/reload reports; share via link (recipients need ad account access).
- **Export** as CSV/Excel; charts as images.
- **Schedule email delivery** of saved reports, recurring (AdManage, 2025-11).
- Supports combining two breakdowns (cross-segmentation), unlike main table.

---

## 9. Automated rules

Paths: **Ads Manager → All tools → Automated Rules** (direct: `facebook.com/ads/manager/rules`, Cropink 2026); or table: select → **Rules** → Create a new rule.

Structure: rule = **Apply to** (scope) + **Action** + **Condition(s)** + **Schedule** + **Notification subscriber**.

Scope: All active campaigns/ad sets/ads, or selected items. One level per rule — campaigns OR ad sets OR ads; mixing levels needs separate rules (Netpeak, 2025-03).

Actions (Netpeak, 2025-03):
- Campaign: turn off, turn on, notify only
- Ad set: turn off, turn on, notify only, increase/decrease daily budget (%), increase/decrease lifetime budget, increase/decrease bid, scale bid by target field, scale daily budget by target field

Conditions: any metric threshold — Cost per result, Results, CPC, CPM, CTR, Frequency, ROAS, spend, impressions, pixel-event costs (cost per add-to-cart/initiate-checkout/purchase/lead/registration/add-payment-info), plus time-based ("Current time between…" for dayparting). ANDed; for OR logic use separate rules.

Schedule: Continuous (~every 30 min [uncertain]), Daily, or Custom.

Limits & gotchas:
- **Max 250 rules per ad account**, including inactive (Netpeak). Consolidated limits table: `00` §4.2.
- Not available for social issues/elections/politics ads.
- Uncapped budget-increase rules can spiral — set max-budget ceilings; add minimum impressions/spend conditions to avoid noise-triggering (e.g. Frequency > 2 AND CTR < x AND Impressions > 8,000).
- Rules log actions — check rule history before blaming Meta for budget changes.
- API-side: cost/ratio conditions (`cpa`, `cost_per_*`, `website_purchase_roas`) are rejected on ADSET/AD-scoped rules for every action except CHANGE_BUDGET/CHANGE_BID — even NOTIFICATION (error 2703/subcode 2490336, field-observed 2026-08 on v26.0); campaign scope accepts them (why the UI can offer cost conditions at all). Ad-set-level "cost per result > X → pause" must be built as `spent > price x k AND <conversion count> < k+1`. Threshold choice for small samples + API field/unit gotchas: `senior-buyer-ops/references/04-automated-rules.md`.

---

## 10. Drafts and review/publish flow

- Unpublished work held as a **draft** (badge on review control). Bulk uploads/imports also land as paused drafts (Ads Uploader, 2026).
- Path: edit → **Review and publish** (pending-change count) → itemized change list → **Publish**. **Discard** reverts unpublished changes.
- Nothing goes live until Publish — safe to build in drafts. [uncertain — auto-save/review behavior shifted 2024–2025; some accounts see minor edits auto-applied without a drafts step]
- After Publish: review typically minutes to hours, officially **up to 24 hours**. Status "In review" → "Active"/"Rejected" (policy reason; appeal from the ad or Account Quality).
- **Creative Hub** — separate tool for sharing ad preview links, client approval pre-launch (Jon Loomer, updated 2025-03).

---

## 11. Billing, account spending limit, account quality

### Billing
Path: **Ads Manager → All tools → Billing → Payment settings** (also `business.facebook.com/billing_hub`). Contains payment methods, activity/charges, billing thresholds, account spending limit.

### Account spending limit
Path: **Billing → Payment settings → Account spending limit → ⋯ → Set limit**/manage (Graphed, 2025-12).
- **Lifetime cap** on total ad-account spend — not monthly, not per campaign (Meta Help Center, cited by Agrowth, 2026-01).
- At limit: ads pause but stay listed Active (editable/resumable); progress bar shows spend toward cap.
- Not available for manual-payment (prepaid) accounts.
- Distinct from campaign budgets, ad-set daily/lifetime budgets, Meta billing thresholds (auto-charge points), and Meta's risk-based new-account caps (lift with billing history, typically months).
- Gotcha: exhausted $0-limit accounts look "banned" — check here before assuming restriction (ADS Infra, 2026).

### Account quality / status
Path: `business.facebook.com/accountquality` (also via Business Support Home). Shows status of ad accounts, Pages, portfolio, user account: active restrictions, rejected ads, reasons, **Request review** buttons. "My accounts" view for per-asset status (Dolphin Anty, 2025-02).
- If ads won't run with no visible ban — check here first.
- Common triggers (practitioner consensus): repeated policy-violating rejections, payment/risk flags (payment method country mismatch, suspicious activity), sudden activity spikes on new accounts, ads from restricted Pages.

---

## Sources

1. https://admanage.ai/blog/facebook-ads-dashboard — Complete Guide to Facebook Ads Dashboard (2025-11-10) (practitioner; fetched 2026-07-22)
2. https://www.shopify.com/blog/facebook-ads-manager — How To Use Meta (Facebook) Ads Manager in 2026 (2026-03-22) (practitioner; fetched 2026-07-22)
3. https://www.jonloomer.com/essential-breakdowns-meta-ads-manager/ — 8 Essential Breakdowns to Use in Meta Ads Manager (2025-12-01) (practitioner; fetched 2026-07-22)
4. https://netpeak.us/blog/how-to-set-up-automated-rules-in-meta-ads/ — How to Set Up Automated Rules in Meta Ads (2025-03-14) (practitioner; fetched 2026-07-22)
5. https://hawky.ai/blog/facebook-ads-benchmarks — Facebook Ads Benchmarks by Industry, citing WordStream/LocaliQ 2025 study (2026-07) (benchmark; search result 2026-07-22)
6. https://sepia-lab.com/en/blog/video-ad-benchmarks-by-industry — WordStream 2025 dataset details: n=554 traffic / n=726 leads, Apr 2024–Jun 2025, medians (benchmark; search result 2026-07-22)
7. https://www.mbadv.agency/meta-ads/meta-ads-cost-budgeting-and-bidding — WordStream 2025 industry tables (benchmark; search result 2026-07-22)
8. https://www.mbadv.agency/meta-ads/meta-ads-account-structure — Meta Ads Account Structure Guide 2026 (practitioner; search result 2026-07-22)
9. https://www.graphed.com/blog/how-to-reset-facebook-ad-spending-limit — Spending limit click-path: All tools → Billing → Payment settings (2025-12-21) (practitioner; search result 2026-07-22)
10. https://agrowth.io/blogs/facebook-ads/facebook-ad-account-spending-limit — ASL definition quoting Meta Business Help Center (2026-01-11) (practitioner; search result 2026-07-22)
13. https://cropink.com/meta-automated-rules — Direct URL facebook.com/ads/manager/rules; All Tools path (2026-06-02) (practitioner; search result 2026-07-22)
14. https://blog.hubspot.com/blog/tabid/6307/bid/30893/how-to-split-test-your-facebook-ads-to-maximize-conversions.aspx — A/B test via Duplicate → New A/B test (2025-07-10) (practitioner; search result 2026-07-22)
15. https://www.get-ryze.ai/blog/meta-ads-ab-testing-basics-beginners-guide — A/B Test toolbar button + three-dot duplicate (2026-05-07) (practitioner; search result 2026-07-22)
16. https://www.jonloomer.com/new-facebook-ads-manager/ — Jon Loomer's "New Ads Manager" post — actually from ~2015; cited ONLY as an example of outdated UI (Power Editor, old objectives) (practitioner, outdated; fetched 2026-07-22)
17. https://adsuploader.com/blog/facebook-ads-bulk-uploads — Bulk uploads land as drafts; review & publish step (2026-05-25) (practitioner; search result 2026-07-22)
18. https://blackpropeller.com/blog/meta-ads-manager-complete-guide/ — Meta Ads Manager in 2026: six ODAX objectives (2026-07-16) (practitioner; search result only — fetch returned 403, 2026-07-22)
19. https://lobehub.com/zh/skills/giacomoarienti-meta-ads-skill — Practitioner skill notes: CAPI recovers 20–30% of conversion data; Advantage+ ~22% higher ROAS claim (2026-07-03) (practitioner; search result 2026-07-22)

## Gaps

- **Official Meta Business Help Center articles could not be fetched directly** (help-center URLs are hard to verify without hitting login walls; site: searches returned nothing usable). All click-paths above come from practitioner sources quoting Meta docs; treat exact menu labels as 2025–2026 snapshots that may drift by rollout.
- **Editing pane** (right-side vs full-screen) and current auto-save/drafts behavior could not be verified against an official source — marked [uncertain] in §1 and §10.
- **Exact daily-budget overspend allowance** (Shopify cites up to 75% over daily budget; Meta's own current wording not verified).
- **Continuous rules check interval** (~30 min) not verified.
- **Exact date-preset list and column-preset list** vary by account rollout; not exhaustively confirmed.
- **A/B test statistical methodology details** (confidence thresholds, minimum runtime) not covered by fetched sources.
- **WordStream 2025 report** itself (wordstream.com) was not fetched directly; numbers come via three independent secondary sources that agree (hawky.ai, sepia-lab.com, mbadv.agency).
- Advantage+ campaign performance claims (20–22% improvement) are Meta/vendor-reported, not independently verified.
