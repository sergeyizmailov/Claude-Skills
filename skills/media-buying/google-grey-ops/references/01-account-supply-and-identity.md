# 01 — Account supply, identity, session infrastructure

Reviewed 2026-08-27. Prices and vendor terms are volatile and vendor-reported 🔺. Every vendor named
here is a counterparty to evaluate, not an endorsement.

## What the terms mean on Google

Unlike Facebook, Google's grey-market infrastructure is built almost entirely on **Google's own
manager-account and invoicing primitives** rather than on forged business verification.

| Term | What it actually is |
|---|---|
| **Agency account** | A client account created *inside* a Google Ads **Manager Account (MCC)** belonging to a Partner or a reseller adjacent to one. It inherits the MCC's billing relationship, often invoiced. **The MCC hierarchy is a first-party Google feature being rented out** — not an emulation of one, which is the structural difference from Facebook |
| **Invoiced / credit-line account** | Monthly invoicing instead of threshold billing. Google extends credit; no card is charged in real time |
| **MCC** | Google's official multi-account layer. The grey use is renting a seat inside someone else's rather than building your own trust history |
| **Self-farm** | Building your own accounts from scratch. Higher control, higher time cost, **no shared-MCC blast radius** |
| **"Threshold account"** | Not a product. Standard automatic-payments billing where the threshold has already ramped through several clean cycles, sold or rented for the higher ceiling |

## Account types

| Type | Moderation tolerance | Notes |
|---|---|---|
| **Brand-new self-registered** | Lowest — thinnest trust graph, first campaigns get the most scrutiny | Best for self-farm where you control every variable; worst for immediate aggressive scaling |
| **Aged with billing history** | Higher — the threshold ramps with clean payment cycles | **History *is* the credential.** This is the legitimate trust-building mechanic the grey market resells |
| **Partner / Premier Partner MCC** | Highest structural tolerance claimed | The product the agency-account market rents. Partner status requires spend and certification thresholds **on the agency's side** — the client riding inside does not personally qualify |
| **Invoiced / credit-line** | High — no real-time decline risk | Chargebacks are structurally impossible (no per-transaction card charge), but **non-payment on an invoice hits the whole relationship**, far more severely than one declined card |

**Geo:** US/UK/EU/CA/AU/SG have the most mature identity verification and highest scrutiny. OFAC vs
serve-pause vs payment friction are **three different lists** (`07`). Iran is OFAC; Russia is a
serve-to pause; Nigeria/Pakistan/Belarus are **not** on 6163740. 🔺 No official ranked “easiest AIV
geo” list.

## Reseller economics 🔺

All vendor-reported list prices, not market clearing prices.

| Metric | Figure |
|---|---|
| Commission on spend | **3–7%** typical |
| Top-up fee (some resellers, separate from commission) | 5–10% per top-up |
| Flat monthly fee model | Exists; favors advertisers already over ~$10k/mo |
| Cited daily cap, self-serve account | $500–5,000/day initially |
| Cited daily cap, agency account | $5,000+/day; one cited case scaling to $15,000/day in week one |
| Onboarding | 24–72 hours signup to live |
| Fee to recover balance from a banned account | ~30% (one vendor) |

Context for why the market exists: Google's own 2024 Ads Safety Report figures — **12.7 million
advertiser accounts suspended, 5.5 billion ads removed**. Verify against Google's report directly.

### Reading a reseller

Red flags, converged across sources:

- **"Unbannable accounts"** — definitionally false. Every source calls this a red flag.
- **Crypto-only, anonymous, or Telegram-only contact** with no other channel — no recourse if they
  vanish.
- **Vagueness about who owns the MCC.** If they cannot answer this cleanly, you have no idea whose
  compliance history you are inheriting — and MCC-level enforcement cascades (see `04`).
- **No written replacement policy** — a documented timeline and whether unspent balance migrates,
  versus a verbal "we'll take care of you".

**The tell worth reading closely:** one major vendor's explicit product promise is **fund continuity on
ban** — "recover unused balance, transfer funds to another account" — *not* ban prevention. That is the
vendor's own admission of the base rate.

Roundup and comparison articles on this topic are themselves frequently affiliate-monetized, so the
ranking is not independent judgment.

## Signals Google associates accounts by

Converged from official policy language (which names some explicitly) and practitioner consensus
(which fills in the rest). **Google does not publish the full set, by design.** No single factor
triggers linking; the threshold is undisclosed.

- **Payment profile** — card BIN, cardholder name, billing address, bank details. The explicit anchor
  of the suspicious-payment and chargeback enforcement path.
- **Phone number** — creation and verification challenges.
- **Recovery email and the underlying Google account.** The circumventing-systems policy explicitly
  targets "creating new accounts to re-enter the system", which only functions as a deterrent if Google
  ties the *person*, not just the account.
- **Browser/device fingerprint** — canvas, WebGL, fonts, timezone/locale consistency.
- **IP/ASN** — exit IP type and consistency across sessions for one identity.
- **GTM container / Google Tag / Analytics property IDs** — shared tagging infrastructure across
  "different" accounts is a strong cross-link. Frequently overlooked.
- **Merchant Center** — business name, address, domain tie into MC's own verification.
- **Domain WHOIS registrant** reused across otherwise-unrelated properties.
- **Search Console property ownership** — verifying multiple domains under one identity ties them.
- **Business name and address** reused across Merchant Center, invoicing, WHOIS, and the landing page's
  own About-us content.

**Consistency is required *within* one persona; separation is required *between* personas.** Both
halves matter.

### Where Google differs from Facebook

The full comparison table and the practical translation — protect the **billing identity and the
destination**, not the session — are canonical in `04`. The one operating consequence for this file:
a payment event, not a login, is the highest-risk identity-mismatch moment, so sequence a persona's
activity around its payment events (see `02`).

## Antidetect and proxies 🔺

**No rigorous, methodology-backed comparison of antidetect vendors' Google-specific detection
resistance exists in reachable public material.** This is a genuine gap, not an omission. What was
found is vendor marketing and competitor-authored reviews, which are structurally unreliable.

- **Dolphin{anty}** — heavily positioned for Facebook/TikTok; Google support present but described by
  users as technically demanding. Free plan cut from 10 to **5 profiles in Sept 2025**. Flagged as
  *detected* in one third-party fingerprint check — **but that review was competitor-authored**, so
  treat it as marketing.
- **GoLogin, AdsPower, Octo Browser, Multilogin, Undetectable** — all market Google multi-accounting.
  None of their own Google-specific configuration docs were retrievable this pass.
- **Linken Sphere** — one review cites affiliates running **15–20 Google Ads accounts**. The only
  concrete N-accounts figure surfaced for Google specifically.

**Proxies:**

- **Static residential is the reported norm** for an account-holding persona — an exit IP that behaves
  like a real home connection, held stable for the persona's life.
- **Datacenter** is cheap and fast but flagged by IP-reputation systems as non-residential, raising
  baseline suspicion before any behavioral signal is evaluated.
- **Mobile** offers carrier-grade reputation at higher cost, but shared/rotating CGNAT ranges can cause
  **cross-persona collisions** if reused without control.
- **Rotating residential is the wrong choice for the account-holding persona** — it breaks IP
  consistency and resets the model on every rotation. Appropriate only for scraping tasks unrelated to
  the persona's own session.

Vendor product docs for Bright Data, IPRoyal, Proxy-Seller, and 922proxy could not be retrieved for
Google-specific guidance.

## The compliant path for each grey practice

| Grey practice | Compliant alternative reaching a similar goal |
|---|---|
| Renting a seat in an unknown reseller's MCC for spend headroom | Apply for **Google Partner** status directly, or qualify for **direct monthly invoicing** — same billing flexibility, no shared-fate MCC risk |
| Buying aged "threshold accounts" to skip the trust ramp | Run a real account through Google's own threshold progression with compliant spend. Slower, but the trust is **yours and not revocable by a third party** |
| Cloaking | Build one page that is simultaneously compliant and converting — solve the actual policy friction (missing product or company info, absent disclosures) rather than hiding it from the crawler |
| Domain-hopping to dodge a disapproval | Fix the specific policy trigger named in the notice and use the real appeal path. Domain cycling to evade detection is named in policy as **Evasive ad content** |
| Payment-identity fragmentation | Consolidate onto one verified invoiced business relationship where scrutiny is expected and accounted for |
| Antidetect session separation to hide multi-account operation | Use the **MCC hierarchy** — a first-party feature designed for exactly this, with none of the fingerprint-evasion risk |
| Buying stolen or synthetic-identity accounts | Register a real entity and complete Advertiser Identity Verification **proactively** — this removes the entire "account collapses when verification catches up" failure class |

**Google does not ban multiple accounts per business.** Agencies and multi-brand companies run many
under one MCC routinely. What crosses into Circumventing systems is creating an account **to re-enter
after a suspension**, or spreading the same violating content across accounts to evade detection.
**The violation is the evasion pattern, not the account count.**
