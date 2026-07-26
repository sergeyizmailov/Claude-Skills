# Instagram Placements & Ad Creatives (2025–2026)

Knowledge base for Meta Ads Manager as of mid-2026. Covers every Instagram placement, Advantage+ vs manual placement strategy, exact creative specs, Advantage+ creative enhancements, copy rules, Reels hooks, UGC performance data, and creative volume best practices.

**Naming notes (2025–2026):**
- "Automatic placements" → renamed **Advantage+ placements** (ad-set level setting).
- "Automatic advanced matching / dynamic creative enhancements" → **Advantage+ creative** (ad level).
- "Advantage+ shopping campaigns (ASC)" → renamed **Advantage+ sales campaigns** in early 2025.
- ODAX objectives are the only campaign objectives now: **Awareness, Traffic, Engagement, Leads, App promotion, Sales**. Older sources referencing "Conversions", "Reach", "Video views", "Catalog sales" objectives describe the pre-ODAX UI.
- Placement UI groups: **Feeds / Stories and Reels / In-stream ads for videos and Reels / Search results / Messages / Apps and sites** (Jon Loomer, current UI).

---

## 1. Where placements are selected

Click-path: **Ads Manager → Campaigns → + Create → Ad set level → "Placements" section**.

- Default: **Advantage+ placements** (recommended by Meta).
- Switch to **Manual placements** to select platforms (Facebook, Instagram, Audience Network, Messenger) and individual placements via checkboxes.
- Also in the same section: device targeting (All devices / Mobile / Desktop) and "Specific mobile devices & operating systems".
- Meta recommends selecting **6 or more placements** when going manual so delivery isn't starved (Meta guidance, echoed by Topkee, 2025).
- View results per placement: **Ads Manager → Breakdown dropdown → Delivery → Placement**.

**Instagram placements available in Manual placements (2026):**

| UI group | Instagram placements |
|---|---|
| Feeds | Instagram feed, Instagram profile feed, Instagram Explore, Instagram Explore home |
| Stories and Reels | Instagram Stories, Instagram Reels |
| In-stream ads for videos and Reels | Ads on Instagram Reels (overlay format) |
| Search results | Instagram search results |

---

## 2. Instagram placements in detail

### Instagram Feed
- Classic in-feed placement between organic posts; most attention-dense surface on Instagram, also most competitive.
- Supports image, video, carousel, collection. 1:1 and 4:5 dominate; 1.91:1 landscape supported but wastes vertical real estate.
- Per Tinuiti data cited by Shopify (2026): Feed dropped to ~26% of Instagram ad impressions, behind Reels (~33%) and Stories — Feed is no longer the default volume placement.

### Instagram Stories
- Full-screen 9:16 between organic Stories. Ephemeral context = fast consumption; creative must land in the first second.
- Supports image (auto-display ~5–7s), video (Meta auto-segments videos over 60s into multiple Story cards), carousel (native carousel in Stories = 3 cards max per Story unit before expanding), collection.
- Story ads now generate more impressions than Feed (Shopify/Tinuiti, 2026).
- Only placement family (with Reels) where sound is a realistic expectation — design for sound-on AND captions for sound-off.

### Instagram Reels
- Full-screen 9:16 between organic Reels. Fastest-growing placement: ~33% of all Instagram ad impressions, an all-time high (Tinuiti via Shopify, 2026).
- Reels creative should feel native: trending-style audio, fast cuts, UGC look. Polished TV-style spots underperform.
- Restrictions on boosted Reels as ads (Strike Social spec sheet): no Reels published before Oct 15, 2021; no licensed music (use original audio or Meta Sound Collection); no face/camera effects; no GIFs; no product tags.
- Max video duration for the placement: 15 minutes, but performance reality is 5–30s ads.

### "Ads on Instagram Reels" (in-stream/overlay group)
- Distinct from "Instagram Reels". These appear **on top of an existing organic Reel** (banner/post-loop overlay), not as a standalone Reel in the feed (Jon Loomer). Smaller, interruptive format; different creative rules.

### Instagram Explore
- Ad appears after a user taps a tile in the Explore grid and starts scrolling the content chain. High-intent discovery context.
- Supports image, video, carousel.

### Instagram Explore home
- Ad appears **directly in the Explore grid** itself (before the tap). Launched October 2022, opened via Marketing API November 2022 (Digiday 2022; Search Engine Journal 2022).
- Distinct placement checkbox from "Instagram Explore" — they cover different surfaces and must both be selected for full Explore coverage.
- Square 1:1 grid context: the creative renders as a tile among organic tiles, so it must read at thumbnail size.

### Instagram profile feed
- Ads inserted into the feed of a **public profile** a non-follower is scrolling. Launched October 2022 (Digiday; SEJ). Lower-intent, more passive context; cheaper impressions.
- Supports wider ratio range than Feed (image 1.91:1–4:5, video 1.91:1–9:16).

### Instagram search results
- Ads appear in the results list when a user taps a search result post and scrolls. Announced 2023; small but growing surface. Still image and carousel supported; no headline field in some configs [uncertain — Meta spec coverage is thin here].

**Behavioral differences to remember (Jon Loomer):** each placement has its own display rules for format, dimensions, and character truncation; costs vary with competition; some placements (esp. Audience Network, rewarded video) are prone to accidental clicks/bots/forced views. Instagram placements themselves are comparatively clean.

---

## 3. Advantage+ placements vs manual placements

### The default: Advantage+ placements
- Meta distributes budget to any eligible placement using historical data and audience behavior, optimizing for the most results within budget.
- **Rule of thumb (Jon Loomer):** if your performance goal is a purchase (or any conversion), leave Advantage+ placements ON. Low-quality clicks from weak placements don't matter because the algorithm adjusts away from placements whose clicks don't convert.
- Removing "low-performing" placements usually just raises costs — cheap placements (e.g., right column) assist conversions even without direct clicks.
- Meta's illustrative math (Meta Help Center example via AdNabu): with $27 and 11 impression opportunities at different costs per result ($3 FB, $5 IG, $1 AN), using all placements yields more total results than cherry-picking the "best" ones.

### When to override to Manual placements
1. **Traffic/link-click or landing-page-view optimization** → inspect Audience Network separately for click quality and downstream behavior. Exclude it only when account data shows low-quality delivery or when brand-safety requirements demand it; do not infer fraud from placement alone.
2. **ThruPlay/video-view optimization** → consider removing **Audience Network rewarded video** (forced/incentivized 15s views inflate metrics).
3. **Reach campaigns with frequency caps** → the algorithm chases cheapest placements; if you need action, force Feeds (costs rise, accept it).
4. **Creative-format constraints** → if you only produced 9:16, limit to Stories/Reels; a landscape video auto-cropped into Stories is a wasted impression. Fix by uploading placement-specific assets via "asset customization" per placement rather than restricting placements.
5. **Placement-level testing** → isolating e.g. Reels-only ad sets gives clean placement data for creative decisions.
6. **Brand-safety/compliance** → regulated verticals sometimes must exclude surfaces like profile feed or search results.
- **Do NOT remove placements just because they show few results** — only remove placements that produce low-quality versions of the exact event you optimize for.

### Gotchas
- Not all objectives support all placements (e.g., Messages placement only appears for sponsored-message campaigns).
- Advantage+ sales campaigns historically locked placement control; 2025 updates restored some controls, but expect fewer manual options inside Advantage+ campaign types.
- Placement selection lives at the **ad set** — you can't vary placements per ad, only per ad set.
- Duplicate-ad-set trap: duplicated ad sets carry old placement choices; verify after duplicating.

---

## 4. Creative specs per placement

Primary references: Meta's official ad spec sheet as mirrored by Strike Social (May 2026) and Sprout Social (Aug 2025). Minor discrepancies between the two are noted.

### Aspect-ratio cheat sheet
- **1:1 (square)** — Feed safe default, Explore home grid, carousel cards.
- **4:5 (portrait 1080×1350)** — recommended for Instagram Feed; max vertical space without leaving Feed context.
- **9:16 (full vertical 1080×1920)** — Stories, Reels.
- **1.91:1 (landscape)** — supported in Feed/profile feed but weak; avoid for Instagram-first campaigns.
- Pro strategy: design **4:5 + 9:16** versions of every concept; use per-placement asset customization in Ads Manager instead of relying on auto-crop.

### Image ads

| Placement | Ratio | Min. resolution | Max file | Primary text | Headline |
|---|---|---|---|---|---|
| Instagram Feed | 1:1 (4:5–1.91:1 supported) | 1080×1080 (Sprout: 1440×1440 recommended) | 30 MB | 125 ch | 40 ch |
| Instagram profile feed | 1:1 (1.91:1–4:5) | 1080×1080 | 30 MB | 125 ch | 40 ch |
| Instagram Stories | 9:16 | 1080×1920 (Sprout: 1440×2560) | 30 MB | 125 ch | — |
| Instagram Reels | 9:16 | 1440×2560 rec. | 30 MB | **72 ch** | — |
| Instagram Explore | 9:16 (Strike) / 1:1 (Sprout) [uncertain — sources conflict] | 1080×1080 | 30 MB | 125 ch | — |
| Instagram Explore home | 1:1 | 1080×1080 | 30 MB | 125 ch | 40 ch |
| Instagram search results | matches Explore-style specs [uncertain] | 1080×1080 | 30 MB | 125 ch | — |

- File types: JPG, PNG. Min width 500 px. Aspect-ratio tolerance ~1–3%. Max hashtags: 30.

### Video ads

| Placement | Ratio | Min. resolution | Duration | Max file |
|---|---|---|---|---|
| Instagram Feed | 4:5 | 1080×1080 (Sprout: 1440×1880) | 1s–60 min | 4 GB |
| Instagram profile feed | 4:5 (1.91:1–9:16) | 1080×1080 | 1s–60 min | 4 GB |
| Instagram Stories | 9:16 | 1080×1080 min | 1s–60 min (15s+ gets segmented) | 4 GB |
| Instagram Reels | 9:16 | 500×888 min | up to 15 min (spec) — target 5–30s | 4 GB |
| Instagram Explore | 4:5 | 1080×1080 | 1s–60 min | 4 GB |

- File types: MP4, MOV (GIF accepted in Feed/Stories). Codec stack: H.264, square pixels, fixed frame rate, progressive scan, AAC stereo 128 kbps+.
- Captions and sound are optional but commonly useful on Stories/Reels. Design the message to remain understandable without sound, and test whether audio materially improves the selected outcome.

### Safe zones (critical for Stories & Reels)
- **Stories: keep text/logos/CTA out of the top 14% (~250 px) and bottom 20% (~340 px)** of the 1080×1920 canvas — profile icon, swipe-up CTA, and "Send message" bar render there (Meta guidance via Sprout/Strike).
- **Reels: top ~14% (250 px), bottom up to 35% (~340–670 px depending on UI version), ~6% each side** — username, caption (up to 4 lines), like/comment/share/save buttons, audio attribution all overlay the bottom and right edge (Strike Social; screensnap.pro). Bottom 350 px is the practical floor; captions burned into the bottom third get covered.
- Feed image ads: keep ~13% right / 10% bottom clear (disclaimers, promos) per Strike Social.
- Ads Manager shows a yellow **safe-zone guard overlay** in the ad preview for Stories/Reels — check every placement preview before publishing.

---

## 5. Formats: image vs video vs carousel vs collection

- **Single image** — fastest to produce; strong for retargeting and offers. Works everywhere.
- **Single video** — best for Reels/Stories and prospecting; hook discipline required (§7).
- **Carousel** — 2–10 cards, 1:1 (4:5 in Feed per Sprout), image 30 MB / video 4 GB per card; Stories carousel video limited to 15s per card (Strike). Each card gets its own headline (40 ch) and link. Best for multi-product, feature breakdowns, sequenced storytelling.
- **Collection** — cover image/video + product catalog grid opening into an Instant Experience (required). Cover ratio 1.91:1–1:1 (Feed/Stories), 9:16 cover with 1:1 product images for Reels. Commerce/catalog accounts only.
- **Flexible ads** (replaced much of Dynamic Creative in 2024–2025): upload up to 10 images/videos in one ad; Meta assembles variations per user. Use for variation testing without DCO overhead.

---

## 6. Advantage+ creative enhancements — the toggles

Location commonly appears at **Ad level → "Advantage+ creative" → Edit** or in an "Optimize media" panel. Defaults and account-level controls vary by feature and rollout. Inspect the state on every ad and preview every eligible placement; do not assume a universal account-wide switch exists or that every enhancement is enabled.

### AI-labeled (generative — highest brand risk)
| Toggle | What it does | Verdict for brand control |
|---|---|---|
| **Text improvements / text generation** | Rewrites/reorders primary text, headline, description; swaps positions per placement | Disable when exact wording, disclosures, or isolated creative testing matter; otherwise test against a fixed control |
| **Expand image** | Generative fill extends image edges to fit 9:16 etc. | Test; warps hands/logos/edges — preview every variant. Alternative: upload true 9:16 assets |
| **Generate background** (catalog) | AI lifestyle backgrounds behind product shots | Test per product; avoid for premium brands |
| **Image animation / 3D animation** | Ken Burns zoom / parallax on static images | Disable on composed product photography (edge crop as zoom progresses) |
| **Enhance CTA** | Highlights phrases from copy onto CTA | Test |
| **Add overlays** | Auto text overlays from headline onto image | Usually ugly (Jon Loomer: "looks pretty awful") — test rarely |

### Standard (rule-based)
| Toggle | What it does | Verdict |
|---|---|---|
| **Visual touch-ups / adjust brightness & contrast** | Subtle color/contrast lift | Low risk; disable only with strict color governance |
| **Music** | Adds Meta library track to Stories/Reels videos lacking audio | Preview every placement; disable for regulated or tightly governed creative, or provide approved audio |
| **Relevant comments** | Shows top comment under ad as social proof | Enable; monitor comment quality |
| **Adapt to placement / Dynamic media / Dynamic description** (catalog) | Fit, pick best asset, pull catalog copy | Enable for catalogs |
| **Site links** | Adds up to 4 extra links under CTA | Use when additional destinations support the journey; disable when they distract from a single conversion path. Validate with a controlled test |
| **Dynamic overlays / Info labels** (catalog) | Price/discount badges | Enable only when pricing data is accurate |

- Bulk editing: multi-select ads → Edit → Advantage+ creative (not every toggle exposed in bulk).
- API: Marketing API v22.0 (Jan 2025) **deprecated the single `enable_standard_enhancements` field** — per-feature flags now required (`text_optimization_enable`, `enhance_cta_enable`, etc.) via `creative_features_spec`.
- Meta claims ~4% lower cost per result on average from enhancements [Meta-reported; treat as directional].
- Failure case (2025): True Classic ran unintended AI enhancements; Meta generated images of a grandma holding a product the brand doesn't sell (Ads Uploader).
- **Testing hygiene:** enhancements modify creative mid-flight, so you can't isolate variant performance while they're on. Standardize enhancement state across test/control.

---

## 7. Copy: primary text, headline, description

| Field | Recommended visible | Hard limit |
|---|---|---|
| Primary text | 50–125 characters | ~2,200 (truncated behind "… more" after ~125 on most placements; **72 ch on Reels**) |
| Headline | 27–40 characters | 40 (UI practical) / 255 technical [sources conflict; plan for 40] |
| Description | 20–30 characters | 30 practical / 125 technical [sources conflict; plan for 30] |
| Hashtags | — | 30 max |
| Carousel card headline | — | 40 ch per card |

Best practices:
- Front-load value in the first 125 characters (first ~2 lines) — everything else sits behind "See more".
- On Reels only ~72 characters of primary text display — write Reels-specific short copy.
- Don't repeat the headline in the description; description only shows on some placements, so never put critical info there.
- Text-improvements enhancement can reorder your copy (§6) — disable if message order matters.
- The old 20%-text-on-image rule is dead; low text still correlates with cheaper delivery.
- Q4 note (WordStream 2025): explicit problem-solution copy structure beat product-description copy by 28% CTR in December campaigns [seasonal benchmark].

---

## 8. Reels hooks — first 3 seconds

Meta's own guidance (Meta Marketing blog, Dec 2025, via Social Media Today):
- "Great Reels nail the hook within the first few seconds… younger audiences consume content at 3x the speed of older."
- Three hook archetypes: **value promise** (benefit up front), **statement of intent** (say exactly what viewer will learn), **question/invitation** (curiosity, self-reflection).
- A/B test hooks; iterate fast — small hook changes yield outsized improvements.
- **Audio:** campaigns with music or voiceover in Reels deliver up to **13% higher incremental conversions** (Meta).
- Creative-volume context: Meta's retrieval system **Andromeda** scans tens of millions of ads and rewards genuinely differentiated creative; advertisers using Meta's image generation see **+11% CTR, +7.6% CVR**; text generation **+3% CTR** (Meta, Dec 2025).
- Corroborating data: ads with strong first-3-second hooks see up to 89% higher engagement per Meta's 2025 Creative Best Practices report (cited by adlibrary.com) [uncertain — secondary citation]; 63% of top-watched videos deliver the key message in the first 3 seconds (Lebesgue via Billo, 2026).
- Practitioner hook-rate metric: track 3-second video plays ÷ impressions ("hook rate"); healthy creative testing accounts watch ThruPlay + 3s views as leading indicators (Metalla, 2025).

---

## 9. UGC-style creative performance data

- Creator-led or phone-shot Reels can outperform studio creative when the format improves message fit and attention, but vendor CTR claims are not portable benchmarks. Compare concepts under the same objective, market, and attribution setup.
- Widely repeated UGC lift figures often trace to vendor summaries or older studies. Preserve sample, period, comparison creative, and methodology before citing them.
- Self-published UGC studies are directional. Prefer the account's controlled test over a universal conversion-rate or CPA uplift.
- Placement impression share shift (Tinuiti via Shopify, 2026): Reels 33% of IG ad impressions (all-time high), Feed 26%, Stories above Feed — budget weight should follow toward vertical video.
- AppsFlyer 2025: 70–80% of Meta ad performance variance stems from creative strength, not budget/targeting (via Billo).
- Practical format: "Performance UGC" — briefed, scripted creator content mimicking organic behavior; iterate primarily on the hook (first 3s); run via Partnership Ads (formerly whitelisting/branded content ads) through the creator's handle for extra lift (Koro, 2026).

---

## 10. How many creatives per ad set

- Meta has historically recommended limiting active ads in an ad set so delivery can allocate enough impressions to each, while newer automated formats can support more asset combinations. Treat `≤6` and the practitioner `3–5` range as starting heuristics, not hard limits.
- Learning status is evaluated at the **ad-set level**, not separately for every ad. Do not multiply the legacy `50 events` heuristic by the number of ads or use the former `ads ≤ weekly budget ÷ (CPA × 50) × 7` formula; it is dimensionally incorrect.
- Select creative count from budget, audience size, concept diversity, and the question the test must answer. Reduce variants when most receive too little delivery to evaluate.
- Testing frameworks: 3-2-2 method (3 audiences × 2 creatives × 2 copy = 12 variations) only with budget to match; Meta's built-in **Creative testing / A/B test** tool forces even budget splits for clean reads.
- **Creative diversification > superficial volume:** Meta's retrieval and delivery systems can select among many assets, but near-duplicates provide little new information or audience relevance. Vary angle, persona, offer, and format rather than only captions. Do not claim a specific algorithmic penalty unless Meta documents one.
- In Advantage+ sales campaigns and Flexible ads, higher variation counts are fine — the system assembles combinations internally without the same per-ad learning penalty.
- Refresh when account-relative evidence shows fatigue: declining attention or conversion efficiency at comparable delivery, rising frequency, and a control-vs-challenger comparison. Calendar cadence and frequency thresholds are practitioner heuristics, not universal limits.

---

## 11. Common mistakes checklist

1. Running one 1:1 asset across all placements and letting Meta auto-crop/letterbox into Reels — white bars flag repurposed creative instantly; upload native 9:16.
2. Burned-in captions in the bottom 350 px of Reels — hidden behind UI chrome.
3. Leaving **Music** enhancement on — random library tracks on brand creative.
4. Leaving **Text improvements** on during creative tests — invalidates attribution of what worked.
5. Removing placements because "they don't convert" while optimizing for traffic — you probably wanted to remove Audience Network only, and only for traffic objectives.
6. Restricting placements without a format, policy, quality, or experimental reason and thereby reducing auction opportunities.
7. Treating "Instagram Explore" and "Instagram Explore home" as one placement — they're separate checkboxes covering different surfaces.
8. Ignoring per-placement previews — the yellow safe-zone overlay in Ads Manager preview exists precisely to catch §2/§4 problems.
9. Assuming Ads Manager > Preview shows what users saw — preview shows the unenhanced original; use Inspect per placement for enhancement-applied previews.
10. Counting on >125 characters of primary text being read — write for the truncation.

---

## Sources

1. https://www.jonloomer.com/a-guide-to-meta-ads-placements/ — placement inventory, Advantage+ vs manual decision rules (practitioner). Accessed 2026-07-22.
2. https://sproutsocial.com/insights/instagram-ad-sizes/ — per-placement specs, safe zones, character limits, updated Aug 22 2025 (practitioner). Accessed 2026-07-22.
3. https://strikesocial.com/blog/instagram-ad-specs/ — full spec sheet incl. Explore home, profile feed, Reels restrictions, safe zones, updated May 2026 (practitioner). Accessed 2026-07-22.
4. https://www.socialmediatoday.com/news/meta-shares-tips-on-reels-hooks-creative-diversification-in-ads-and-threa/808182/ — Meta's Reels hook types, +13% incremental conversions from audio, Andromeda/creative diversification stats (practitioner, reports official Meta marketing blog). Accessed 2026-07-22.
5. https://adsuploader.com/blog/advantage-plus-creative-enhancements — full Advantage+ creative enhancement matrix, AI vs standard tiers, API v22.0 deprecation, True Classic case, site-links CVR issue, June 2026 (practitioner). Accessed 2026-07-22.
6. https://www.hyperfx.ai/blog/meta-advantage-creative-enhancements-issues — per-toggle disable paths, account/ad-set/ad override levels, May 2026 (practitioner). Accessed 2026-07-22.
7. https://withblip.com/blog/how-many-ads-to-run-meta-campaign/ — Meta's ≤6 ads per ad set rule, learning-phase budget math, budget tiers, April 2026 (practitioner). Accessed 2026-07-22.
8. https://blog.adnabu.com/facebook/meta-advantage-placements/ — Meta's budget-efficiency example for Advantage+ placements, July 2025 (practitioner, cites Meta Help Center). Accessed 2026-07-22.
9. https://www.shopify.com/blog/instagram-ads — placement impression shares (Reels 33%, Feed 26%) via Tinuiti, Stories > Feed; Story ad segmentation, July 2026 (benchmark). Accessed 2026-07-22.
10. https://digiday.com/marketing/the-rundown-meta-to-put-new-ads-all-over-facebook-and-instagram-including-on-user-profiles/ — Explore home + profile feed ad launch, Oct 2022 (practitioner/news). Accessed 2026-07-22.
11. https://www.searchenginejournal.com/meta-announces-instagram-explore-home-ads-placement-via-marketing-api/471006/ — Explore home via Marketing API, Nov 2022 (practitioner/news). Accessed 2026-07-22.
12. https://billo.app/blog/what-is-a-good-ctr/ — creator Reels 38% CTR (Zebracat 2025), UGC 2× CTR, Lebesgue 63% first-3s stat, 2026 (benchmark). Accessed 2026-07-22.
13. https://billo.app/blog/meta-ads-best-practices/ — AppsFlyer 70–80% creative-share-of-performance, 2026 (benchmark). Accessed 2026-07-22.
14. https://paceads.com/research/meta-ads-statistics-2026 — WordStream/LocaliQ 2025 medians: 1.71% CTR / $0.70 CPC traffic, 2.59% CTR / $1.92 CPC / 7.72% CVR / $27.66 CPL leads; $14.19 ecommerce CPM (benchmark aggregator). Accessed 2026-07-22.
15. https://digitalmarketinginstitute.com/blog/how-to-use-user-generated-content-ugc-with-4-great-examples — UGC 4× CTR aggregate stat, Dec 2025 (practitioner). Accessed 2026-07-22.
16. https://ugcera.com/wp-content/uploads/2025/08/ugcera_whitepaper.pdf — 84-campaign UGC study: +21% CVR, −17% CPA, Aug 2025 (benchmark, vendor self-published). Accessed 2026-07-22.
17. https://getkoro.app/blog/how-to-use-ugc-for-facebook-ads — Performance UGC methodology, hook iteration, Partnership Ads naming, Feb 2026 (practitioner). Accessed 2026-07-22.
18. https://www.screensnap.pro/blog/instagram-reels-size-guide — Reels safe zone detail (top 250 px, bottom 350 px), April 2026 (practitioner). Accessed 2026-07-22.
19. https://metalla.digital/facebook-ad-creative-testing-2025/ — creative testing phases, CTR 0.90–1.60% healthy range, July 2025 (practitioner). Accessed 2026-07-22.
20. https://admakeai.com/blog/what-is-facebook-ads-manager — Advantage+ naming confusion, ASC→Advantage+ sales rename Q1 2025 (practitioner). Accessed 2026-07-22.

## Gaps

- **Meta's official Ads Guide (facebook.com/business/ads-guide) could not be fetched** (HTTP 400/JS-gated). All specs above come from Strike Social and Sprout Social, which mirror the official spec sheets; minor conflicts between them are flagged inline ([uncertain] tags, e.g. Explore image ratio 9:16 vs 1:1).
- **Instagram search results placement specs** are thin in all secondary sources; ratio/field support marked [uncertain]. The official Meta help article on ads in Instagram search results (March 2023 announcement) was not directly retrieved.
- The "89% higher engagement from first-3-second hooks" figure is a secondary citation of Meta's 2025 Creative Best Practices report (adlibrary.com); the primary Meta report was not retrieved.
- Whether a global account-level off-switch for Advantage+ creative enhancements exists: sources conflict (HyperFX says Business Settings > Advertising settings sets defaults; mbadv.agency says no campaign/account-level disable, per-ad only). Verify in a live account.
- Safe-zone pixel values (250/340 vs 250/350) vary slightly by source and UI version; Meta publishes percentages, not hard pixels.
- UGC performance statistics (4× CTR, 50% lower CPC) trace to pre-2024 aggregate studies recirculated by vendors; no rigorous 2025–2026 Meta-published UGC benchmark was found.
