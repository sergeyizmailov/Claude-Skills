# Evidence and Maintenance Guide

Last reviewed: 2026-07-24

This file defines how the Meta Ads references should be interpreted, cited, and maintained. Meta changes product names, UI paths, defaults, eligibility, and regional availability continuously. A dated screenshot or practitioner workflow is evidence of one account state, not a universal product contract.

## 1. Evidence labels

Use one of these labels when a claim can materially change a recommendation:

| Label | Meaning | Appropriate use |
|---|---|---|
| **Official behavior** | Current Meta policy, Help Center, developer documentation, or in-product state | Product rules, availability, policy, required setup |
| **Meta-reported** | Result or benchmark published by Meta, often from selected studies | Directional context with the study scope stated |
| **Independent benchmark** | Aggregated data with disclosed sample, period, geography, objective, and methodology | Planning ranges for a comparable account |
| **Practitioner heuristic** | Operational rule derived from experience or a vendor article | A starting hypothesis to validate against account data |
| **Unverified** | Single-source, stale, inaccessible, conflicting, or rollout-dependent claim | Explicit uncertainty only; never present as a requirement |

For case studies, add a proof grade separately from source ownership: causal design reported, structured comparison, or attributed/pre-post case. Meta, an agency, or a measurement vendor can describe a real experiment while still being an interested-party publisher. Never turn a positive case-study lift into an expected result for another account.

Do not convert vendor language such as “best practice,” “optimal,” “must,” or “Meta recommends” into official guidance unless the primary Meta source supports it.

## 2. Source priority

1. Live in-product state for the exact account, country, objective, placement, and data source.
2. Current Meta Advertising Standards, Help Center, Business Help Center, and developer documentation.
3. Meta newsroom or product announcement with publication date and rollout scope.
4. Independent benchmark with visible methodology.
5. Practitioner or vendor source with date and account context.
6. Undated summaries, search snippets, and copied screenshots only as discovery leads.

When sources conflict, state the conflict, prefer the higher-priority and newer evidence, and advise checking the live account. Never infer universal availability from one UI screenshot.

An agent/support reply is **official account-specific evidence**, not a public
platform contract. Preserve the case text and affected asset IDs. If it
conflicts with the live UI or public documentation, operate conservatively for
that account and request human/manual escalation.

## 3. Verification protocol

Before asserting a changing fact:

1. Identify the claim type: policy, product behavior, UI path, benchmark, or heuristic.
2. Record the relevant market, objective, optimization event, placement, and account type.
3. Check an official source and its publication/update date.
4. Check the live account when access exists; account state overrides generic navigation instructions.
5. Use an independent source only when official documentation is unavailable or ambiguous.
6. Label the confidence and give the user a concrete verification step for unresolved rollout variance.

For high-impact recommendations, include the evidence label inline. Exact prices, thresholds, reporting delays, learning requirements, and feature defaults are presumed volatile unless verified.

## 4. Confirmed corrections and retired concepts

| Topic | Current interpretation | Evidence |
|---|---|---|
| Location presence selector | Meta removed the old “living in or recently in” choice for new ad sets in 2023. Current location behavior and exceptions must be checked in-product. | Independent product reporting: https://searchengineland.com/new-update-to-meta-ads-location-targeting-404124 |
| Special Ad Audiences | Meta stopped making Special Ad Audiences available for housing, employment, and credit in 2022. Do not recommend them as a current substitute for lookalikes. | Official: https://about.fb.com/news/2022/06/expanding-our-work-on-ads-fairness/ |
| Pixel and dataset | Meta Pixel remains a browser-side web data source; a dataset can group events from multiple sources. The terms are related but not interchangeable. | Official: https://www.facebook.com/help/messenger-app/952192354843755 |
| Closed ad account | A closed ad account can be reactivated; closure is not inherently irreversible. Restrictions and disabled accounts are separate states. | Official: https://www.facebook.com/help/messenger-app/331993756945799/ |
| Two-factor authentication | Meta may require 2FA for certain portfolios and workflows. Recommending it for every privileged user is a security practice, not proof that every portfolio has the same product requirement. | Meta help should be checked in-product; secondary setup context: https://support.chatarchitect.com/books/meta-business-portfolio-setup/page/turn-on-the-two-factor-authentication-requirement-in-your-business-portfolio |
| Offline event ingestion | References to the separate Offline Conversions API can be stale. Current offline/CRM event ingestion should be designed around supported Conversions API routes and verified against current developer documentation. | Official CAPI overview: https://www.facebook.com/business/help/AboutConversionsAPI |
| Meta-enabled CAPI | Meta announced a no-code Meta-enabled Conversions API option in April 2026. Availability and supported data sources remain account-dependent. | Official: https://about.fb.com/ltam/news/2026/04/eliminar-barreras-tecnicas-para-ayudar-a-empresas-de-todos-los-tamanos-a-aprovechar-mas-sus-anuncios/amp/ |
| Detailed targeting exclusions | Availability has changed and can depend on campaign state and account rollout. Do not build a strategy that assumes the legacy control exists. | Official: https://www.facebook.com/help/messenger-app/717368264947302/ |
| EU political, electoral, and social-issue ads | Meta announced that these ads would no longer be delivered in the EU from October 2025. Confirm scope and current policy before planning. | Official: https://about.fb.com/news/2025/07/ending-political-electoral-and-social-issue-advertising-in-the-eu/ |

## 5. Claims that always need context

- Cost benchmarks: currency, country, period, objective, optimization event, attribution setting, placement mix, and sample size.
- Learning: current Delivery status, result volume, conversion delay, event quality, and fragmentation; avoid a universal event-count formula.
- Budget changes: marginal economics and observed delivery response; percentage limits are heuristics.
- Frequency and fatigue: objective, evaluation window, audience size, reach, creative distribution, and outcome trend.
- Event Match Quality: diagnostic signal, not a universal launch or optimization gate.
- Attribution gaps: identity, consent, click/view windows, time zones, reporting timestamps, deduplication, refunds, and backend definitions.
- Feature paths and defaults: account rollout, objective, country, placement, and interface version.

## 6. Maintenance checklist

Review at least quarterly and immediately after a major Meta announcement:

1. Recheck official policy and product links.
2. Search for removed product names, retired APIs, legacy objectives, and hard-coded years.
3. Reclassify every new benchmark and record its scope and methodology.
4. Replace dead sources; do not silently preserve a claim whose evidence disappeared.
5. Re-run contradiction searches for universal language: `must`, `always`, `never`, exact learning counts, fixed edit percentages, fixed reporting delays, and fixed frequency limits.
6. Compare the canonical research directory with the skill reference copies using the sync tool.
7. Update the review date only after the facts, links, and known gaps have actually been checked.

## 7. Official knowledge map

Do not copy Meta's whole help corpus into this skill. Route the question to the
current primary surface:

| Question | Check first |
|---|---|
| Exact account/asset restriction | Live error, [Account Status](https://www.facebook.com/help/1392616391875085/), [Business Support Home](https://business.facebook.com/business-support-home/), Support Inbox |
| Ad rejection or prohibited content | [Advertising Standards](https://transparency.meta.com/policies/ad-standards/), [ad-review guide](https://www.facebook.com/business/ads/review-policy-guidelines) |
| Profile/Page conduct | [Community Standards](https://transparency.meta.com/policies/community-standards/) and Account Status |
| Portfolio, Page, Instagram, billing UI | [Business Help Center](https://www.facebook.com/business/help), live Business Settings/Billing |
| Campaign operation and official training | [Meta Blueprint](https://www.facebookblueprint.com/student/catalog/list), [Ads Manager learning](https://www.facebookblueprint.com/student/collection/507792-meta-ads-manager-learning) |
| Creative format/placement availability | [Ads Guide](https://www.facebook.com/business/ads-guide), live placement preview |
| Competitor/market creative discovery | [Meta Ad Library](https://www.facebook.com/ads/library/) |
| Marketing API objects and permissions | [Marketing API docs](https://developers.facebook.com/docs/marketing-apis/), [official Postman collection](https://www.postman.com/meta/facebook-marketing-api/collection/0zr4mes/facebook-marketing-api-mapi) |
| Breaking API changes | [Graph API versioning](https://developers.facebook.com/docs/graph-api/guides/versioning/), [changelog](https://developers.facebook.com/docs/graph-api/changelog/) |
| SDK implementation | [official Business SDK repositories](https://github.com/facebook/facebook-python-business-sdk) |
| Pixel/CAPI/data duties | [CAPI overview](https://www.facebook.com/business/help/AboutConversionsAPI), [Business Tools Terms](https://www.facebook.com/legal/terms/businesstools) |
| Contract, billing, delivery obligations | [Commercial Terms](https://www.facebook.com/legal/commercial_terms), [Self-Serve Ad Terms](https://www.facebook.com/legal/self_service_ads_terms) |
| Suspected platform outage | [Meta Status](https://metastatus.com/) before rebuilding or changing campaigns |
| Announced rollout | [Meta newsroom](https://about.fb.com/news/); verify availability in the exact account |

Search snippets are discovery aids only. Logged-in Help Center pages, live UI,
country eligibility, and current API version can differ from indexed copies.
