# 02 — Payments, billing, verification

Reviewed 2026-08-27. **On Google, billing is the trust spine.** This file is mostly official mechanics
because they are what actually govern behavior.

## The mechanics that matter

- **Prepaid cards are explicitly not accepted for automatic payments.** One-time-use and virtual cards
  **are** permitted for **manual** payments.

  > This is the structural reason media buyers run manual/prepay billing with virtual cards rather than
  > automatic billing. It is a documented product constraint, not a workaround.

- **Threshold billing**: the charge fires when account cost reaches the threshold **or** on the 1st of
  the month, whichever comes first. Google's own example: threshold $500 with $1,500 monthly spend →
  three separate $500 charges.

  🔺 **Google does not publish the escalation ladder.** The widely cited $50 → $200 → $350 → $500
  progression is industry lore, unconfirmed against official docs. Do not build a spend plan on it.

- **Monthly invoicing — official eligibility**: registered business **≥1 year** · account in good
  standing **≥6 months** · spend **≥$5,000/month in any 3 of the last 12 months** · MCC link + primary
  billing contact + payments-profile business-name match. Terms net-30; the credit line is the maximum
  balance across all invoiced accounts.

- **PayPal** is "temporarily unavailable for new automatic payment accounts". **Giropay** dead since
  2024-06-28. **Disbursement-only accounts (e.g. Payoneer) are not accepted** as a funding source.

## Suspension triggers — exact official language

> *"If we detect suspicious or unauthorized payment activity on your account, we may restrict how much
> the account can spend or suspend the account."*

The same page separates three distinct causes:

1. **Unpaid balance** — "concerns about your ability to make future payments".
2. **Chargeback** — *"If you instruct your bank or credit card company to reverse a charge that was
   paid against a legitimate Google Ads balance, your account may be suspended."* This officially
   confirms a chargeback is an **account-level** event, not merely a payment-method block. It is one of
   the fastest ways to lose an account permanently.
3. **Promotional code abuse** — multiple codes, reselling codes.

Suspended accounts stay **read-only**: reports and settings viewable, payments and appeals still
possible, ads stopped.

## Decline reasons

Bad card info · expired · insufficient funds · exceeded transaction limits · **bank restrictions on
internet or international transactions**.

That last one is the closest official language to a country/currency mismatch flag — and note it is
framed as an **issuing-bank restriction, not a Google-side geo flag**. 🔺 The official payments-profile
page contains **no** fraud or mismatch language at all, so the widely repeated "billing country must
match card country or Google flags you" claim **remains unconfirmed**. Consistency is still worth
maintaining for the identity-graph reasons in `01`, but do not present it as a documented Google rule.

## Verification

**Triggers**: initial billing setup · changing the primary payment method · one-time payments ·
"unusual activity or transactions" · legal/regulatory compliance.

**Methods**:

1. A temporary charge of **≤$1.95** whose descriptor's last 6 digits are the code.
2. Making a payment.
3. Document upload — government ID plus payment-method image. **Current, legible, in color, all four
   corners visible.** Processing ≤5 business days.

Non-compliance means the account **"may be temporarily paused"** — softer than suspended, and
recoverable.

**Payment-profile verification is separate from advertiser identity verification.** Both can be
required at once, on separate deadlines. Advertiser identity gates *serving*; payment profile gates
*billing*. See `google-ads/09` for the identity side.

## The asymmetry that should drive every decision here

**Failing verification honestly is recoverable — the account pauses.**
**Submitting false information during verification is charged as Circumventing systems — permanent,
propagating to linked accounts, appealable only in "compelling circumstances".**

There is no version of this where fabricating documents is the lower-risk path.

## Virtual card and agency vendors 🔺

Vendor-reported. Counterparty risk, not endorsements.

| Vendor | Terms as reported |
|---|---|
| **Pay2.House** | Unlimited cards, per-card limit to $100,000, Visa/Mastercard, USD/EUR, BINs from multiple countries. $5 issuance, $5/mo per active card, 4% reload, 4% refund, 20% volume discount at 100+ cards. Ships "Decline Analytics"; publishes no decline-rate stats |
| **AdsCard** | Marketed for Google (vendor also names other networks; out of scope). From $1 with a **$500/month ad-spend requirement**. Issuance $2.50–$3.00, standard fee 4%, USDT top-up free. **BINs by geo: USA, EU, Hong Kong.** User reviews report $50k+/month volumes but also a **20-day fund hold with commission charged on failed transactions** and recurring processing delays |
| **PST.NET, XCards (ex-EPN), Mint Card** | General ad-platform virtual cards. **No Google-specific claims surfaced** — treat Google specificity as unverified |
| **YeezyPay** | 2023-dated pricing, likely stale: 10% top-up commission, **30% fee to recover funds from a banned account**, $200 minimum deposit, up to $200,000/month. Live site now shows no public pricing |
| **Mega Digital** | Rents Google/Facebook seats (vendor also lists other networks; out of scope). Product promise is **fund continuity on ban**, not ban prevention |

**Not confirmed by any reachable source**: working BIN ranges, issuer names, crypto-funded-card
acceptance data, or any documented threshold escalation ladder. Anyone quoting specific BINs is
guessing or selling.

## Operational reading

1. **Sequence payment events deliberately.** The single highest-risk moment for an identity
   inconsistency on Google is a billing event, not a login (`01`). Do not add a card, change a method,
   or trigger a threshold charge from an inconsistent context.
2. **Never chargeback.** It is an officially named account-level suspension trigger and it burns the
   payment method's future usability too.
3. **A declined card is not a policy event.** Read the decline reason before escalating — most are
   issuing-bank restrictions on international transactions, fixable at the bank.
4. **Invoiced accounts trade one risk for another.** No decline risk and no chargeback surface, but
   non-payment damages the entire parent relationship rather than one account.
5. **"Temporarily paused" is not "suspended".** Verification pauses are recoverable by completing the
   task. Do not treat one as the other and start a panic migration.
6. **Watch the card networks, not only the platform.** A network-side rule wave kills offer economics
   with clean accounts and no policy event — practitioner case: the Nov 2025 Visa/Mastercard
   sweepstake tightening collapsed multiple teams' funnels at once. A funnel that dies while ad
   accounts are healthy is a payment-network event, not a moderation one. [single source]
