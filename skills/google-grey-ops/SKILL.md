---
name: google-grey-ops
description: "Google Ads grey-market buying: agency/MCC account supply, identity/payment infra, AdsBot/cloaking/review-layer filters, RSA/unicode/path tricks, selfie/BOV verification, geo isolation, Demand Gen/App no-cloak surfaces, ban replacement, domains/redirects/trackers, enforcement tracks, failure forensics, per-vertical playbooks (gambling, finance/crypto, nutra, dating, loans, apps). Infra+survival layer. Clean = google-ads; feeds = google-feed-ops; metrics = tracker-ops."
---

# Google Grey Ops

Run aggressive verticals on Google without losing accounts, domains, and payment identities.
Vertical-agnostic infra and survival, plus per-vertical playbooks.

Boundary: **"buy well"** → `google-ads` · **"don't get killed / source accounts / scale"** → here ·
**"feed and Merchant Center"** → `google-feed-ops` · **"count and sync"** → `tracker-ops` ·
**"portfolio and TL decisions"** → `senior-buyer-ops`.

Authority: this skill governs grey-vertical execution. `google-ads`' clean-marketing guardrails are
authoritative for compliant accounts. Route by lane; do not merge the two normative stances.

## The Google model is not the Facebook model

If you carry one thing from `meta-grey-ops`, carry the discipline, not the risk map. They differ:

| | Google | Facebook |
|---|---|---|
| Trust anchors on | **Billing history** — a disclosed, literal threshold ramp | Behavioral/social signals |
| Highest-risk moment | **A payment event** | A login |

Full 7-row comparison (destination review, cascade scope, burn radius, moderation timing, appeal
posture) → `references/04-failure-forensics.md`.

**On Facebook you protect the session. On Google you protect the billing identity and the
destination.** Porting the Facebook playbook wholesale over-invests in session hygiene and
under-invests in payment consistency and landing-page integrity.

## Non-negotiables

1. **Classify the enforcement track before doing anything.** Egregious (no warning, permanent,
   propagates) · non-egregious (mandatory 7-day warning) · Limited Ad Serving (a throttle, not a
   suspension). The correct response differs completely, and the most common expensive error is
   treating a recoverable state as terminal or vice versa. See `04`.
2. **Know which replacement you are doing.** A new Google identity after *your* suspension is a
   separately charged Circumventing-systems violation and it propagates. A reseller swapping the
   *seat* (their MCC, their invoice) is a different product — still cascade-risk if GTM, domain,
   phone, or payment profile overlap. See `05`.
3. **Never submit false information during verification.** Failing honestly pauses the account; lying
   suspends it permanently. There is no version where fabrication is the lower-risk path. Org path
   skips the selfie; grey self-reg does **not** pass BOV — `06`.
4. **Never chargeback.** Officially named as an account-level suspension trigger, and it burns the
   payment method's future usability.
5. **Sequence payment events deliberately.** Do not add a card, change a method, or trigger a threshold
   charge from an inconsistent context.
6. **Rotate on signals, not a timer**, and **change one variable at a time** — otherwise the next burn
   is unattributable and you re-learn the same lesson forever.
7. **Know whose MCC you are in.** A cascade takes every account sharing it. If a reseller cannot answer
   who owns the MCC, you are inheriting an unknown compliance history.

## Route references

| Need | Reference |
|---|---|
| Account supply market, account types, linking signals, antidetect/proxies, compliant alternatives | `references/01-account-supply-and-identity.md` |
| Payment mechanics, threshold billing, invoicing eligibility, verification, virtual-card vendors | `references/02-payments-and-billing.md` |
| AdsBot official behavior, ValueTrack chains, Keitaro/RedTrack measurement config, domains | `references/03-domains-trackers-review.md` |
| Enforcement tracks, death modes, appeals under fire, scaling posture, Google vs Facebook | `references/04-failure-forensics.md` |
| Review-layer filters, cloaking stacks, white pages, RSA/unicode/path tricks, replacement | `references/05-review-layer-and-cloaking.md` |
| Advertiser verification, video selfie, BOV — live vs dead pass paths | `references/06-verification-selfie-bov.md` |
| Geo isolation: OFAC vs RU pause, tz/currency locks, billing vs serve | `references/07-geo-isolation.md` |
| Demand Gen sensitive inventory, App campaigns (no cloak), adult/CBD no-path table | `references/08-surfaces-and-no-path.md` |
| API errors → survival response (freeze/replace/rotate); canonical code→fix in `google-ads/11` | `references/09-api-errors-grey-response.md` |
| Per-vertical playbooks | `playbooks/` |

Policy taxonomy, certifications, and the full appeal process live in `google-ads/09` — read it before
any regulated vertical.

## New-job bootstrap

1. **Collect access** — MCC and account IDs, billing arrangement and who owns it, Merchant Center,
   tracker campaign URL, domains, proxy. Into gitignored project notes, verbatim.
2. **Establish the enforcement baseline** — current policy status, any active strikes, verification
   state, Limited Ad Serving status. You cannot diagnose later changes without a starting point.
3. **Confirm the vertical's certification requirements per target geo** (`google-ads/09`) *before*
   building anything. Gambling and financial services changed multiple times in 2026.
4. **Wire tracking before spend.** Tracking template with `{lpurl}`/`{gclid}`, tracker campaign mapping,
   and — critically — check whether the developer token can still onboard offline conversion import at
   all (the 2026-06-15 cutoff, `google-ads/06`). Do not discover this after launch.
5. **Naming before first launch.** The campaign name must encode whatever the tracker needs to split
   on; the mapping is not automatic (`tracker-ops`).
6. **Launch PAUSED via `validate_only` first** if using the API (`google-ads/10`).
7. **Review layer.** Final URL is the white, same registrable domain, cloak **off** until the ad is
   serving. Do not PMax. Do not cloak App campaigns (`08`). Filter stack in `05`. Confirm tz/currency
   and OFAC vs serve-geo (`07`) before first spend.
8. **Agree kill rules in writing** with the TL: spend-without-conversion cap, CPA cap, account verdict
   threshold, and who decides on a ban wave.

## Diagnose a failure in order

```text
which track (A/B/C) -> account-level or item-level -> payment/verification or policy/content
-> domain-specific or account-wide -> then act
```

Do not skip to remediation. A domain rotation on an account-level signal problem wastes a domain and
teaches you nothing.

## Guardrails

- **Redirects are not the violation.** Content that differs conditioned on who is requesting it is.
  That distinction is Circumventing systems (no warning, permanent, cascade). Filter stacks and
  same-domain whites live in `05` — they do not make the track non-egregious.
- **Compromised site is a disapproval tier. Malicious software is egregious.** Do not treat the first
  as a death sentence.
- **"Temporarily paused" ≠ "suspended".** Verification pauses are recoverable by completing the task.
- Multiple accounts per business are **not** banned. The violation is the evasion pattern, not the count.
- Vendor pricing, spend ceilings, and appeal-success claims in these files are **vendor-reported**.
  Nobody publishes a methodology. Treat every number as a prior, not a fact.
- Where a compliant path reaches the same business goal, say so — `01` maps each grey practice to its
  legitimate alternative. Several are genuinely cheaper long-term because the trust accrues to you and
  cannot be revoked by a third party.

## Output

Lead with the track classification and whether the state is recoverable. Give the exact next action,
the review timeline to expect, what to observe before the next change, and what single variable is
being changed so the result stays attributable.
