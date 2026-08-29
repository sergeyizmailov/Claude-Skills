---
name: google-feed-ops
description: "Merchant Center, product feeds, and Shopping eligibility: feed spec and attributes, Merchant API, feed rules and supplemental feeds, title optimization, custom_label schema, GTIN, Merchant Center suspensions, free listings, CSS. The retail data layer. Campaign types and PMax bidding live in google-ads."
---

# Google Feed Ops

The retail data layer. Google Ads buys the traffic; **the feed decides what is eligible, what it
costs, and what gets suspended.** No Facebook analogue exists at this depth — this is where US
e-commerce accounts are won or lost.

Route: buy mechanics → `google-ads` · infra/survival/agency accounts → `google-grey-ops` · counting →
`tracker-ops` · portfolio decisions → `senior-buyer-ops`.

## Check first

| Need | Reference |
|---|---|
| Attributes, limits, submission methods, Merchant API, titles, custom labels | `references/01-feed-spec-and-submission.md` |
| Suspensions, the gates that block review, required website elements, ratings | `references/02-merchant-center-suspensions.md` |
| Standard Shopping priority ladder, PMax retail structure, product-level reporting, CSS | `references/03-shopping-pmax-retail.md` |

## Three things that break accounts

1. **The five review gates.** Shipping settings · a data source for the target country · website URL
   claimed and verified · business address verified · US tax settings. **Missing any one blocks review
   entirely.** This is the real cause of most "products not showing" tickets — check before diagnosing
   anything else.
2. **Feed vs live page mismatch on price and availability.** Google's automated crawl fires
   preemptive item disapproval. It is automated, so **the fix is a sync fix, never an
   appeal-and-argue.** Compare against the **checkout total**, not just the product page.
3. **Promotional text in titles or descriptions.** A policy trigger, not a soft ranking issue.

## Migration status 🔺

- **Content API for Shopping sunset 2026-08-18.** Only API integrations broke — manual upload,
  scheduled fetch, Sheets, and platform connectors were unaffected.
- **Merchant API v1beta discontinued 2026-02-28**, earlier than the Content API sunset.
- Current: `merchantapi.googleapis.com`, stable **v1**.
- **UCP** (in-Google checkout via `native_commerce(checkout_eligibility)`) is **early access, select
  merchants, US/CA/AU only**. It did **not** replace Buy on Google, which shut down 2023-09-26.

## Model

```text
Merchant Center account -> verification gates -> data source(s)
  primary feed (structured) -> feed rules / supplemental feeds (overlay)
    product -> id / title / price / availability / GTIN / custom_label_0-4
      listing group filter -> asset group (PMax) or product group (Shopping)
        -> bid strategy per segment
```

**The throughline: label schema → listing-group filter → divergent bid strategy per filter.** That is
how per-segment economics happen without per-SKU bidding.

## Workflow

1. Clear the five review gates before anything else.
2. Establish **one primary submission method per data source**. Mixing methods causes silent
   last-write-wins conflicts.
3. Fix required attributes and GTIN coverage. A missing real GTIN costs visibility and disables price
   benchmarking.
4. Build the `custom_label` schema deliberately — margin tier, price band, bestseller rank,
   seasonality, stock lifecycle (`01`). Do it before campaign structure, because structure depends on
   it. This table is canonical; do not invent a second schema in a playbook.
5. Optimize titles for the **~70-character cliff**, specs before adjectives, decision-driving
   attributes first.
6. Confirm destinations and listing-group **keys** are valid. PMax/Shopping campaign structure, feed-only
   vs assets, brand exclusions, and product-level reporting live in `google-ads` (`01`, `07`).

## Guardrails

- **`id` is the join key. Never reuse or recycle it.**
- Never fake a `gtin` or `mpn` with an internal SKU — set `identifier_exists=no`.
- Never submit a `sale_price` without the real non-sale `price`. That is a misrepresentation trigger.
- `shipping_label` and `custom_label_0-4` are unrelated. Conflating them is a common integration bug.
- Use the **test/preview mode** on attribute rules. It prevents catalog-wide breakage.
- Campaign priority does nothing unless two campaigns share the **same products in the same country and
  language** — and an under-budgeted high-priority campaign silently falls back to the low-priority one.
- **AI title generation belongs in a testing sandbox, not in production.** Codify winning patterns into
  templates with fallback chains.
- **CSS is EEA/Switzerland/UK only. The ~20% figure has zero US applicability** — never cite it to a US
  advertiser.
- Merchant Center suspensions and Google Ads suspensions are **separate systems** with separate
  appeals. Do not conflate them.

## Output

Lead with which layer the problem sits in — gates, feed data, policy, or campaign structure. Most
"campaign" problems in retail are feed problems. Give the exact attribute or setting, the expected
review timeline (3–5 business days initial, up to 7 for account suspension, 24–48h for a re-crawl), and
what to verify after the next refresh.
