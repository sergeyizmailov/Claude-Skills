# Meta Marketing API, Billing, and Launch Operations

Last reviewed: 2026-07-28

Use this reference for Marketing API and Ads MCP automation, System User tokens,
Page/Instagram advertising identity, payment readiness, restrictions, and final
activation. Meta UI labels, Graph versions, permissions, app-mode rules, and
support availability change; verify the live account and current official
developer documentation before an irreversible or spend-producing action.

## Contents

1. Ownership model
2. System User and token setup
3. Token security
4. Readiness tests
5. Page and Instagram identity
6. App state and access levels
7. Ads MCP governance
8. Billing and payment diagnosis
9. Restriction and support flow
10. Safe automation launch sequence
11. Failure map
12. Observed post-mortem
13. Sources and uncertainty

## 1. Ownership model

Keep these layers distinct:

```text
Personal or managed login
  Business Portfolio
    Ad account
    Facebook Page
    Instagram professional account
    Dataset / Pixel
    Developer app
    System User -> token -> assigned assets
```

- The portfolio owns or receives partner access to assets. A person or System
  User then receives tasks on each asset.
- Adding a person, partner, or System User to a portfolio does not automatically
  assign the ad account, Page, Instagram account, dataset, or app.
- Prefer business ownership and partner access over shared personal credentials.
- An established or “warmed” portfolio is not a documented guarantee of faster
  moderation, lower restriction risk, or transferable trust.
- Before spend, audit `People`, `Partners`, and `System Users`. An unknown
  full-control identity can manage people, settings, and assets and may be able
  to delete the portfolio. Confirm recovery/ownership before removing an
  unfamiliar owner; secure legitimate admins with 2FA first.

## 2. System User and token setup

Use a System User token for durable server-to-server work on the business's own
assets. Do not call it an “API key” when precision matters: it is a bearer
access token tied to an app, System User, scopes, business, and asset tasks.

Recommended UI sequence:

1. Create or connect a **Business** developer app to the owning portfolio.
2. Add the Marketing API product if the app dashboard requires it.
3. In `Business Settings -> Users -> System users`, create/select a System User.
4. Assign the app and every required business asset before generating the token:
   - ad account: create/manage campaigns and view performance;
   - Page: advertise and read the Page information required by the flow;
   - Instagram professional account: advertise;
   - dataset/Pixel or catalog only when the campaign or measurement needs it.
5. Generate the token for that app and request only required scopes.
6. Inspect the token and run both read and zero-spend write tests.

Common scopes:

| Need | Typical scope |
|---|---|
| Create/update campaigns, ad sets, ads | `ads_management` |
| Read ad objects and reporting | `ads_read` |
| Read/manage business asset relationships | `business_management` |
| Create Page-backed ads | `pages_manage_ads` |
| Read Page engagement/identity data | `pages_read_engagement` |
| List accessible Pages when required | `pages_show_list` |
| Read connected Instagram professional identity | `instagram_basic` |
| Catalog commerce work | `catalog_management`, only when needed |

Permission names and combinations are product- and version-dependent. Do not
request every available permission “just in case.” For an app managing only its
own business's ad accounts, Meta's official Marketing API collection states
that Standard Access with `ads_read` and `ads_management` can be sufficient.
Managing assets owned by other businesses may require Advanced Access, App
Review, partner/Business On Behalf Of design, or another supported relationship.

System User setup via API is possible, but the UI is usually safer for the first
installation. API creation has additional admin-token, app/business ownership,
and app-secret-proof requirements. Do not disable App Secret Proof merely to
make token automation easier.

## 3. Token security

- Never paste a live token into chat, a prompt, source code, shell history,
  screenshots, issue trackers, URLs, or query strings.
- Store it in an OS keychain, encrypted secret manager, or protected runtime
  variable. Prefer `Authorization: Bearer ...` over `access_token=` in a URL.
- Do not print tokens, request headers, environment dumps, paging URLs, or full
  API responses that may echo credentials.
- Generate separate tokens per integration when practical so one can be rotated
  without breaking everything.
- Use the shortest workable lifetime. A non-expiring token needs an owner,
  inventory, access review, rotation procedure, and incident response.
- If a token was exposed, revoke/rotate it before spend. Check dependencies
  first: `Revoke tokens` can affect more than the token currently visible.
- Never place real tokens, app secrets, card data, or personal identifiers in
  this skill or its examples.

## 4. Readiness tests

Treat each of these as a separate gate:

1. **Token identity** — inspect the token with Meta's token debugger or supported
   debug endpoint; verify app, type, expiry, data-access expiry, and user.
2. **Granted scopes** — query `/me/permissions`; requested scopes are not proof
   that they were granted.
3. **Readable assets** — list the expected ad account, Page, Instagram account,
   and data source by stable ID.
4. **System User tasks** — inspect the System User's assigned assets in Business
   Settings. Seeing an asset in one list does not prove every required task.
5. **Zero-spend write probe** — create the smallest disposable campaign or
   creative as `PAUSED`; then read it back. Do this before uploading the full
   creative set or building the complete campaign.
6. **Identity probe** — create a paused creative using the intended Page and
   Instagram identity. A generic campaign write does not validate identity.
7. **Delivery gate** — inspect Account Quality, Billing, effective status, and
   the live UI. API object creation does not prove the account can deliver.

Never activate a probe. Delete it only after validating that no useful audit
evidence or dependency remains; otherwise keep it paused with a clear test name.

If a read succeeds but a write fails, do not regenerate tokens blindly. Check:

- `ads_management` is granted, not merely requested;
- the System User has write tasks on the exact ad account;
- the app belongs to/has the supported relationship with the business;
- the token belongs to the same app and System User expected;
- Page and Instagram assets are assigned where the creative requires them;
- the ad account, business, user, Page, and payment method are unrestricted;
- the API version and requested fields are current.

Do not infer meanings from an undocumented numeric `account_status` alone.
Combine the API response with effective statuses, Account Quality, Billing, and
the live product message.

## 5. Page and Instagram identity

For Instagram ads, verify all of the following:

- the Instagram account is professional and linked to the intended Page;
- the portfolio owns it or has valid partner access;
- the operator/System User has advertising access to the Page and Instagram;
- the ad account is allowed to use those identities;
- the intended identity appears in the live ad creation flow;
- a paused creative using both identities succeeds.

An Instagram account appearing in `/instagram_accounts` does not prove that it
is valid as `instagram_actor_id`. The creative is the authoritative probe.
`Param instagram_actor_id must be a valid Instagram account id` usually points
to linkage, asset assignment, ID type, token/app relationship, or unsupported
creative configuration—not audience targeting.

For Page-backed Instagram creative, current official Meta Postman examples use
`object_story_spec.page_id` plus `instagram_actor_id`. Destination-specific
flows such as Instagram Direct can additionally require the matching promoted
object, destination, CTA, and messaging eligibility. Verify against the current
Marketing API version.

In the EU, account-level choices about personalized or less-personalized ads can
affect creation eligibility. This is the user's privacy choice: explain the
effect and open the exact Accounts Center screen, but do not choose on the
user's behalf. Re-test the paused creative after the user completes the choice.

## 6. App state and access levels

- Complete required app basics: contact email, category, privacy-policy URL,
  data-deletion instructions/URL, and app icon when the dashboard requests them.
- Own-asset use and third-party use have different access requirements.
  Standard Access may be enough for the business's own ad account; third-party
  assets commonly require Advanced Access and App Review.
- Development/Live mode behavior is use-case- and rollout-dependent. If the API
  explicitly requires Live mode for the attempted write, complete the displayed
  requirements and verify the exact app/use-case relationship. Do not publish
  an app solely because a generic tutorial says it is always required.
- A successful token generation does not prove app review, access level, asset
  tasks, creative identity, or delivery eligibility.

## 7. Ads MCP governance

Ads MCP availability and controls are account/rollout-dependent. Distinguish
Meta's connector shown in Business Suite from a third-party MCP server and from
direct Marketing API access; they have different operators, credentials, and
trust boundaries.

A secondary report dated 2026-07-27 shows
`Business Suite -> Integrations -> Ads MCP Server` controls for:

- read-only versus actions in the ad account;
- budget editing with limits;
- creating campaigns, ad sets, and ads initially off;
- audience, creative, and delivery-status changes.

It also reports that these controls may be enabled by default. Treat the path,
defaults, and availability as **unverified** until confirmed in the exact
portfolio. When present:

1. Start read-only; verify the connected portfolio and ad accounts.
2. Enable only the required write categories. Keep budget, creative, audience,
   status, and activation writes off for analysis-only agents.
3. Set the smallest workable budget ceiling. A daily budget is not itself an
   agent permission boundary.
4. Require new objects to remain off/paused and review stable IDs, identity,
   targeting, placements, destination, schedule, and budget before activation.
5. Keep activation and budget increases human-approved; recheck the live
   integration controls before each spend-producing session.
6. Review agent actions and revoke the integration if the operator, server, or
   requested permissions are unclear.

Never send a Marketing API token to an unknown MCP provider. Prefer Meta-hosted
authorization when independently verified; otherwise inspect the server,
credential storage, logging, deletion, and revocation model first.

## 8. Billing and payment diagnosis

The Marketing API does not replace the trusted Meta UI for entering card
details, 3DS, temporary-hold codes, or payment-method verification. The user
must perform those steps; never ask them to share full card data in chat.

Keep these states separate:

| State | Meaning | Action |
|---|---|---|
| Failed transaction | One charge/top-up attempt failed | Inspect that transaction and card response |
| Current amount due | Meta shows an actual payable balance | Pay through the displayed billing flow |
| Card verified/default | The card passed one verification and is selected | Continue checking account eligibility |
| Payment method ineligible | Meta will not accept that method for the shown verification/flow | Use the supported alternative or support path |
| Ad account restricted | Delivery/write access is blocked at account level | Resolve in Business Support Home/Account Quality |

`Current balance = 0` or `No payment due` can coexist with a failed transaction
and an account restriction. Do not pay an arbitrary amount or add funds just to
“unlock” the account when no real amount is due.

Virtual, prepaid, and crypto-linked cards are not subject to a documented
universal ban, but they may receive more issuer, verification, or risk failures
in practice. Treat “not eligible for self-verification” as account-specific.
For the cleanest path, prefer a conventional bank-issued, verifiable
credit/debit card whose legal name, billing country/address, currency, and
available funds are consistent. Avoid rapid card swaps and repeated retries.

A default or verified replacement card does not automatically clear a
restriction caused by an earlier failed payment. Confirm restoration separately
in Account Quality and by a paused write probe.

## 9. Restriction and support flow

1. For a personal-profile or Page feature restriction, inspect Facebook
   **Account Status**. For advertising/business assets, open Business Support
   Home / Account Quality. Check Meta Status first when multiple unrelated
   accounts or surfaces fail at once.
2. Select the exact affected person, portfolio, ad account, Page, or payment
   asset.
3. Save the displayed reason, transaction/payment ID, policy/error code,
   timestamps, and screenshots. Record only the card's last four digits.
4. Correct the underlying issue before requesting review.
5. Use the review/contact path shown for that asset. Avoid duplicate requests.
6. If support calls the decision final, preserve the case and do not bypass it
   with replacement accounts, identities, cloaking, or asset hopping.

Treat support replies as official for the named account, not as universal
product documentation. Automated or first-line replies can conflict with the
live UI. Preserve the transcript and case ID; ask for manual escalation and the
exact affected asset, rule, date, duration, and review path when the answer is
ambiguous or contradictory.

Concise billing appeal template:

> Please review ad account [AD_ACCOUNT_ID]. It was restricted after failed
> transaction [PAYMENT_ID] on the previous card ending [LAST4]. A verifiable
> replacement card ending [LAST4] is now default, and Billing shows
> [BALANCE/NO PAYMENT DUE]. Please restore access or provide the exact remaining
> remediation and affected asset.

Do not include a token, app secret, full card number, CVV, verification code, or
identity document in the message unless the official secure upload flow
explicitly requests the relevant document.

## 10. Safe automation launch sequence

Build for reversibility:

1. Confirm ownership, privileged users, 2FA, Account Quality, Billing, currency,
   time zone, payment type, spending limits, and Page/Instagram linkage.
2. Validate measurement/destination and applicable policy/special category.
3. Run token, asset, write, and identity probes.
4. Create campaign, ad set, creatives, and ads with every level `PAUSED`.
5. Read back stable IDs and all critical fields. Check budget units, bid
   strategy, objective, promoted object, optimization event, geo, age, schedule,
   attribution, placements, Page/Instagram identity, CTA, destination, URLs,
   UTMs, and creative enhancements.
6. Preview each placement. Match 4:5 to feeds and 9:16 to Stories/Reels; verify
   safe zones and no unintended cropping.
7. Refresh start/end times immediately before activation. A paused build can
   become invalid or shorten its intended lifetime while access/billing issues
   are resolved.
8. Recheck effective statuses and account restrictions after publication/review.
9. Activate deliberately, respecting object dependencies, and immediately read
   back delivery. Never assume a successful mutation means spend started.
10. Monitor the first hour/day for rejection, delivery, spend, destination,
    tracking, messaging/lead receipt, and billing anomalies. Pause on any
    identity, destination, measurement, or budget mismatch.

Activation is spend-producing and must follow the user's explicit approval of
the final budget, schedule, destination, and creative set. “Do everything”
authorizes setup within scope, not hidden changes to privacy choices, card
details, legal declarations, or unrestricted spend.

## 11. Failure map

| Symptom | First checks |
|---|---|
| Token works for `GET`, fails on `POST` | Granted scopes, System User write tasks, exact account restriction |
| Asset visible to person, absent to token | Assign it to the System User and app; inspect business relationship |
| Instagram visible but creative fails | Page link, actor ID type, Page/IG assignments, paused identity probe |
| Token generation fails | Same-business app/System User, admin rights, app installation, app-secret proof |
| App asks to go Live | Exact API error, use case, own vs third-party asset, dashboard requirements |
| Card verified but account restricted | Failed transaction vs amount due vs payment eligibility vs account review |
| Campaign created but no delivery | Effective statuses, review, billing, schedule, bid, audience, identity, creative |
| Old paused campaign cannot start | Refresh dates, budget period, policy/review state, creative availability |

## 12. Observed post-mortem

**Evidence: account-specific operational observation, not a universal Meta rule.**

- A new owned portfolio connected a Page, Instagram professional account,
  dataset, app, System User, and token. Paused campaign objects could be partly
  prepared.
- A card/top-up attempt failed. A later replacement card was verified and made
  default, while Billing showed zero balance/no payment due.
- The ad account remained restricted, API writes still failed, and support
  reported that the payment method was not eligible for self-verification.
- Repeated token regeneration did not solve the asset/account restriction.

Transferable lessons:

1. Verify payment-method eligibility and Account Quality before building the
   full campaign.
2. Run a minimal paused write and Instagram-identity probe early.
3. Separate a failed transaction, payable balance, card verification, and
   account restoration.
4. Preserve paused drafts while resolving access; refresh schedules afterward.
5. Do not keep swapping cards or rebuilding portfolios to bypass enforcement.

## 13. Sources and uncertainty

Official/current sources to verify:

- Marketing API overview: https://developers.facebook.com/docs/marketing-apis/
- Meta Marketing API official Postman collection:
  https://www.postman.com/meta/facebook-marketing-api/documentation/0zr4mes/facebook-marketing-api-mapi
- Meta Business SDKs and App Secret Proof guidance:
  https://github.com/facebook/facebook-python-business-sdk
- Meta Advertising Standards:
  https://transparency.meta.com/policies/ad-standards/
- Facebook Account Status:
  https://www.facebook.com/help/1392616391875085/
- Meta ad-review, restriction, and support guide:
  https://www.facebook.com/business/ads/review-policy-guidelines
- Business Support Home: https://business.facebook.com/business-support-home/
- Meta Status: https://metastatus.com/
- Ads MCP controls report (secondary; verify in live Business Suite):
  https://fbki.la/v-business-suite-upravljat-servera-ads-mcp

The official Postman collection documents bearer authorization, System User
token options, Standard versus Advanced Access for own versus third-party ad
accounts, and paused ad creation with Page/Instagram identity. Business Help
Center pages often require a live login, so exact billing and support click
paths must be verified in-product. Error subcodes, app-mode requirements,
permission combinations, and Accounts Center privacy prompts are
rollout/account-specific unless a current primary source states otherwise.
No public primary Meta documentation confirming the reported Ads MCP control
path and defaults was located during the 2026-07-28 review; keep those details
unverified until the live portfolio or an official Meta source confirms them.
