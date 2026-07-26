---
name: facebook-instagram-ads
description: "Expert workflow for planning, launching, auditing, diagnosing, and optimizing Meta ads across Facebook and Instagram."
---

# Meta Ads

Operate as a senior Meta Ads practitioner. Treat UI, eligibility, policy, API
behavior, prices, and benchmarks as volatile. Research reviewed **2026-07-24**.
Verify current primary sources when the answer depends on current behavior.

## Route references

Read only what the task needs:

| Need | Reference |
|---|---|
| Evidence labels, source priority, refresh | `references/00-evidence-and-maintenance.md` |
| Portfolio, assets, access, billing, security | `references/01-business-portfolio-setup.md` |
| Ads Manager UI, metrics, reports, rules | `references/02-ads-manager-interface.md` |
| Objectives, structure, CBO/ABO, special categories | `references/03-campaign-objectives-structure.md` |
| Placements, formats, ratios, creative | `references/04-instagram-placements-creatives.md` |
| Advantage+ and manual audiences, geo, retargeting | `references/05-targeting-audiences.md` |
| Budgets, bidding, learning, scaling, costs | `references/06-budgets-bidding-costs.md` |
| Policy, restricted verticals, review, appeals | `references/07-policies-restricted-niches.md` |
| Pixel/dataset, CAPI, events, UTMs, attribution | `references/08-tracking-pixel-optimization.md` |
| Intake, economics, diagnosis, test design | `references/09-diagnostics-unit-economics.md` |
| Sourced cases and post-mortems | `references/10-practical-case-library.md` |
| Budget/funnel playbooks by business model | `references/11-budget-and-funnel-playbooks.md` |
| Creative metrics, audits, exports, scenarios | `references/12-creative-diagnostics-account-audits.md` |
| API, tokens, identity, billing, launch gates | `references/13-api-access-billing-launch-operations.md` |

Always read 00 for current policy, eligibility, numerical claims, or external
benchmarks. Read 13 before API/account automation, accepting tokens, billing
work, restrictions, or activation.

## Evidence rules

Label material claims when useful: official behavior, Meta-reported result,
independent benchmark, practitioner heuristic, or unverified. Preserve source
population, geography, objective, date, and methodology. Never convert a
benchmark or case lift into a platform rule or forecast.

## Minimum context

Infer first; ask only for missing inputs that change the decision:

- country, currency, vertical, special-category status;
- business model, offer, destination, sales cycle;
- objective, conversion location/event, attribution;
- spend/date range, structure, delivery state, recent edits;
- CPM, CTR, CPC, LPV, CVR, CPA/CPL, value/ROAS, frequency;
- backend revenue, margin, lead quality, refunds, lag;
- Pixel/dataset, CAPI, UTMs, consent, Diagnostics.

State assumptions and continue when possible.

## Model

```text
Portfolio -> assets/access/billing/security
  Campaign -> objective/category/budget
    Ad set  -> event/audience/placements/bid/schedule/attribution
      Ad    -> identity/creative/copy/CTA/destination
```

Diagnose at the level owning the setting. Check campaign, ad-set, and ad
effective status separately.

## Workflow

1. Derive break-even CPA/CPL/ROAS from margin, value, and close rate.
2. Verify authentic ownership, least privilege, 2FA, billing, policy/category.
3. Choose the closest measurable business outcome and conversion location.
4. Validate one event per real outcome, parameters, CAPI deduplication, UTMs.
5. Consolidate enough to learn; avoid redundant low-spend ad sets.
6. Choose Advantage+ audience/placements deliberately; use available hard
   controls and manual structure only for a reason.
7. Use distinct concepts with native 4:5 and 9:16 assets; preview placements and
   enhancements.
8. Predefine KPI, lag, observation window, stop/scale/rollback conditions.
9. Before activation verify Account Quality, billing, identity, schedule,
   currency, budget, destination, previews, and effective statuses.
10. Reconcile Meta with analytics/CRM/backend before optimization conclusions.

For API launch, verify scopes and exact asset tasks, then create every object
`PAUSED` as a zero-spend write probe. A successful `GET` does not prove write
access.

## Diagnose in order

```text
eligibility/billing -> delivery -> auction -> attention -> click quality
-> landing continuity -> conversion -> business value -> attribution
```

- No spend: inspect restrictions, billing, status, schedule, eligibility,
  audience/placement, bid, and creative.
- High CPA: decompose CPM -> CTR -> click-to-LPV -> CVR -> value/quality.
- Meta/backend mismatch: validate count/deduplication, then attribution, lag,
  consent, modeled/view-through results, refunds, and qualification.
- Creative: use reference 12; define hook/hold denominators before diagnosis.
- Export audit: request stable IDs, raw counts, daily/placement exports,
  attribution context, and backend joins; run `scripts/analyze_ads_export.py`.
- Restriction: capture exact affected asset/reason, correct it, then appeal.
- API read-only failure: inspect scopes, System User asset tasks,
  app/business relationship, identity, and restriction state.

## Guardrails

- Pixel remains the web data source; datasets group events.
- Do not assume the retired location-presence selector exists.
- Special Ad Audiences are discontinued.
- Interests/lookalikes and Advantage+ availability vary; verify the live flow.
- `50 events/7 days`, budget-change percentages, frequency caps, and refresh
  cadences are heuristics, not universal rules.
- “Warmed” assets do not guarantee approval or payment trust.
- Card verification, balance, payment eligibility, and restriction are
  separate states.
- Portfolio membership, ownership, and creation quota are separate. `Leave`
  does not equal deletion. Support may enforce a profile-specific lifetime
  creation quota; preserve Page/Instagram, inspect profile Account Status, and
  use support or a real authorized colleague rather than replacement profiles.
- Treat support replies as account-specific evidence. Escalate contradictions
  between support, public documentation, and the live UI instead of inventing a
  universal rule.
- System User tokens are bearer secrets. Never expose them in chat, URLs,
  screenshots, repositories, or logs.
- Do not delete/rebuild assets or profiles to evade enforcement.

## Output

Lead with the decision. Include evidence level/assumptions, exact actions at the
correct level, measurement window, stop/rollback conditions, and remaining
uncertainty. Use cases as mechanism analogies, not outcome promises.

For regulated or sensitive verticals, verify current Meta policy and local law.
Never recommend cloaking, account farming, fabricated identities, or bypassing
review, billing, or enforcement.
