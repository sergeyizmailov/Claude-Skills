# 09 — Verification gates (Meta)

Researched 2026-08-27. Which wall you hit, when, what clears it. Labels: **[official]** with article ID ·
**[practitioner]** · **[unverified]** · 🔺 = re-verify before acting.

**Meta publishes no SLA for any of these.** Every day-count is a practitioner estimate unless tagged
[official], and the estimates conflict with each other.

## 1. Business Verification — the prerequisite for everything else

Gates higher spend limits, developer/WhatsApp features, Commerce/Shops eligibility, and most category
authorizations. **Not** the paid "Meta Verified" badge. Path: Business Suite → Security Center.
[official 1095661473946872]

| Document | Validates | Note |
|---|---|---|
| Articles/Certificate of Incorporation | Legal name | |
| Business registration / license | Legal name | |
| Government business tax document | Legal name | **Self-filed tax docs rejected** |
| Business bank statement | Legal name + address | |
| Utility bill | Address/phone **only** | Cannot validate legal name |

[official 159334372093366] Must show the **legal entity name as entered in Business Manager** — not a
DBA/trading name — plus registered address or phone. Not expired. Redact unrelated personal IDs.
19 accepted languages; anything else needs a stamped translation.

**Alternate path:** business bank account verification via a third-party vendor — marked deposit,
re-enter the amount, **max 3 attempts** then resubmit bank info. [official 561730264791590]
🔺 The fetched article was a China-locale variant; treat the deposit-match pattern as the shape, not
the universal flow.

**Official rejection reasons** [official 2342133782492969]: false/misleading info · verifying a business
you don't own or represent · circumventing review · **website fails to load, no HTTPS, or broken links**.
That last one is the cheapest to pre-clear and the most often missed.

Resubmission is allowed; Meta publishes **no attempt cap and no cooldown**. A failed *business*
verification blocks the gated feature, it does not auto-suspend the account. But submitting false info
or claiming a business you don't represent → **permanent verification denial or suspension**
[official 1095661473946872].

🔺 [unverified, practitioner, mutually inconsistent]: domain verification 1–2 business days · document
review 3–7 days (up to 10) · ~24h cooldown before resubmitting · throttling after ~4 rejections ·
"file Request Review instead of a 3rd resubmission." None confirmed by Meta.

## 2. Identity and selfie verification — two separate programs

**Do not conflate them.**

**2.1 General "Confirm your identity"** — account recovery and integrity risk. Accepts one government ID
(licence / national ID / passport / birth certificate, showing name+DOB or name+photo) **or two**
non-government documents (student/library/refugee card, employment letter, diploma, loyalty card — one
must carry DOB or photo, names must match). Physical redaction of non-essential numbers is allowed;
**digital alteration is not**. [official 159096464162185]
A **notary form** path exists as a backup when standard ID submission fails [official 346296532662771].
Trigger logic is unpublished — fires on new payment instruments, spend surges, policy flags
[practitioner, unverified]. No fixed recurrence cycle; can re-fire at any time.

**Selfie/liveness video:** short multi-angle face video matched against existing profile photos or the
submitted ID. Meta states it is not used for face recognition and is deleted after "a limited period" —
**no number published**. [unverified retention]

**2.2 SIEP identity confirmation** (§4.1) — separate flow: government photo ID issued by the country you
advertise in, plus a residential address confirmed by a **physical postal code Meta mails you**.
🔺 Country-selector gated; exact per-country text not extractable by automated fetch.

**2.3 Financial-advertiser check** (§4.2) — live selfie or video against the submitted ID, at business
**and/or** individual level at Meta's discretion, "subject to ongoing review." [unverified — no primary
article captured; recurrence claim is directional]

## 3. Beneficial owner — the threshold is ownership, not revenue

**≥10% of total shares** = beneficial owner, and must be documented. [official 193400874040813]
Per owner: government photo ID **front and back** (passport preferred) · a formation document naming the
owner (charter / certificate of incorporation / company registration) · company TIN, plus a possible
extra tax form by country of residence.

🔺 **There is no "$50k lifetime Shops revenue" trigger.** Two independent verification passes failed to
find any Meta page stating one. Commerce eligibility gates on Business Verification and account
trustworthiness [official 1627591223954487] — the same ≥10% rule, not a second revenue threshold.
Practitioner-cited triggers are *ad-spend* based (~$5k lifetime), a different metric entirely.
Not completing it leaves Commerce/Shops "Ineligible"; non-Commerce ads keep running.

## 4. Category authorizations

### 4.1 SIEP (social issues, elections, politics)

Self-serve, **not** written permission. Trigger is broader than politics — healthcare, climate and
immigration-adjacent copy get caught. [official 208949576550051]
US proof: government photo ID + residential address confirmed by mailed postal code. Mandatory
"Paid for by" disclaimer whose name must match the entity registered with the campaign-finance
authority. Ads stored in Ad Library **7 years** [official transparency.meta.com SIEP].

**EU: Meta stopped serving political/social-issue/electoral ads entirely from Oct 2025.** Do not build
an EU authorization flow — it is moot. [official, about.fb.com 2025-07]

🔺 Postal mail makes this the **slowest gate** — ~5–10 business days for the code alone, 2–3 weeks total
[practitioner consensus, no SLA]. Start it day 1, in parallel with business verification.
🔺 2026: AI-content disclosure required when a real person/place/event is generated or materially
altered [practitioner-paraphrase, unverified primary wording].
🔺 A "60 days to reconfirm identity / 21 days location" re-verification claim could not be traced to any
primary article. Do not repeat it.

### 4.2 Financial products

Meta's own text: advertisers "may be required to verify business and/or individual identity and
demonstrate authorization by the relevant regulatory authority," and authorization "may be subject to
review by Meta" at any time. In scope: insurance, mortgages, loans, investment products, credit cards.

| Geo | Proof | Note |
|---|---|---|
| UK | FCA firm reference number | Cross-checked against the FCA register via email domain or phone |
| Australia | AFSL number or declared exemption | Plus beneficiary/payer verification 🔺 |
| Taiwan | Beneficiary + payer, **mandatory for all ads targeting TW** once the financial toggle is on | [vendor-sourced] |
| Singapore | Beneficiary/payer verification | [vendor-sourced] |

🔺 **Sources conflict hard on the country count** — one lists 10 (AU, HK, IN, IE, IL, ES, TW, TH, UK, US),
another claims 38. Neither verified against Meta's live list. Never quote a count; check the live list
per target geo. This surface expands by geography over time.

Beneficiary/payer fields are asked **inside Ads Composer at ad-set level** — have the regulator number
in hand before campaign build, not after.

### 4.3 Gambling and games

Policy definition is wide: "any product or service where anything of monetary value is included as part
of a method of entry and prize" — casinos, sportsbooks, poker, bingo, lotteries, fantasy sports,
sweepstakes casinos, skill-based prize contests.

Route: **Authorizations and Verifications tab in Business Suite** — declare operator/aggregator/affiliate
role, target territories, exact destination URLs. Not a free-text email application.
Proof: current regulator licence per targeted territory. **Approvals attach to specific business
portfolios and ad accounts**, not to you as an advertiser — a new account needs a new approval.

**Affiliates get no exemption.** A landing page referencing real-money play, bonuses, promo codes, or
redirecting to an operator is a gambling ad. Meta crawls the redirect path.

Minimum 18+ (or local legal age) targeting, strict geo-fencing.
The **19 unsupported markets** (no gambling ads at any authorization level) are official and current —
named list in `10`. 🔺 [single practitioner source, unverified]: the move to the A&V tab in Jul 2025, and
the 2026-02-23 date for the 19-market list. The list is confirmed; the date is not.

### 4.4 Crypto

**Prior written permission**, via the same Authorizations and Verifications tab.

Needs permission: trading/exchange platforms (spot, margin, futures) · lending/borrowing · enhanced
wallets that buy/sell/swap/stake · mining **software** · solicitation to invest, **including affiliate
sites**.
Exempt: tax services for crypto firms · educational/news content · NFTs and non-currency blockchain
products · storage-only wallets · mining **hardware**. 🔺 This exemption boundary was flagged uncertain
even within the sourced material — check live.

Meta recognizes 25+ jurisdictional licences (FCA, MAS, NY BitLicense, AUSTRAC/ASIC, FINTRAC, FinCEN,
FSA…) [practitioner, no primary Meta list captured].

**Permission does not immunize a creative.** Every ad is still reviewed independently against
Advertising Standards, landing page included.

## 5. Payment method verification

| Method | Mechanism | Failure |
|---|---|---|
| Card | Temporary authorization hold, auto-reversed. 🔺 The "$1–3 + descriptor code" figure is **[unverified]** — Meta's article is login-gated, secondary sources say "$1.01" or "4-digit code" and disagree | Hold expires; not itself a disablement |
| Bank via online-banking login | Instant [official 260929950658464] | — |
| Bank manual deposit | Meta deposits **$0.01–$0.99**, re-enter the exact amount. Completes within **3 business days**, **max 3 attempts** [official 260929950658464] | Resubmit bank details from scratch |

Statement descriptors seen: `METAPAY` · `META PAY` · `METAADS` · `FACEBKADS` · `FACEBK MENLO PARK` ·
`FBMARKETPLACE` · `FACEBOOK PAYMENT` · `FACEBK*`+10 chars. [practitioner, cosmetic, changes] 🔺

**A billing "disabled" is not a policy "disabled"** — the notification should name billing specifically.
Repeated failed charges lead to suspension after a retry cycle (🔺 24–72h, [unverified]).
Card/account **name mismatch** is a documented risk trigger. Chargebacks freeze billing and trigger
review; permanent ban is possible but not automatic.

🔺 The circulating "7-day disablement → guaranteed learning-phase reset" tier table with its dollar-cost
model is **one vendor blog's construction**, not measured and not Meta-sourced. Illustrative only.
Same for "invoice billing needs 3 months of $10k+/month" [unverified].

## 6. Pre-clear order for a restricted vertical

Operational inference, not a Meta-published sequence.

1. **Business Verification** — everything else assumes it. Pre-clear the website first: loads, HTTPS,
   no broken links (an official rejection reason and the cheapest to fix).
2. **Beneficial owner docs** — same round-trip if a ≥10% owner exists and Commerce is in scope.
3. **Payment method** — before heavy spend, so a billing suspension never compounds a policy hold.
4. **Identity/selfie** — fires opportunistically, not schedulable. Front-load if the vertical is financial.
5. **Category authorization** — **parallelize with 1, don't sequence after it.** Gambling/crypto file in
   A&V before any ad exists; financial needs the regulator number sourced externally (usually the
   blocking dependency); SIEP starts day 1 because postal mail is the long pole.
6. **Ad-level review** — independent of every gate above. Authorization never immunizes a creative.

## Gaps — do not fill with plausible guesses

1. No primary SLA for business-verification review; practitioner estimates conflict (2–5 / 3–7 / ≤10 days).
2. No published attempt cap before permanent denial.
3. No published selfie/ID video retention period or re-verification cadence.
4. No Commerce-specific beneficial-owner threshold found separate from the ≥10% rule.
5. Financial-products country list: 10 vs 38, unresolved.
6. Australia AFSL beneficiary/payer rollout — "early February" of an ambiguous year.
7. Jul 2025 gambling move to the A&V tab — single practitioner source.
8. Current crypto exemption boundary — uncertain in the source material itself.
9. These pages are JS-rendered or login-gated and could not be fully extracted; re-fetch live before
   quoting exact wording: `transparency.meta.com/policies/ad-standards/restricted-goods-services/financial-services/`,
   `facebook.com/business/help/208949576550051`, `facebook.com/business/help/2992964394067299`.
