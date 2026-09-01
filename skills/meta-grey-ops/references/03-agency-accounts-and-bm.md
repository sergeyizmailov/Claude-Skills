# 03 — Agency accounts, BMs, asset sharing

**New BM = 1 ad account cap** (UI, field-observed 2026-08-30): "maximum number
of ad accounts allowed for a new business portfolio" — more only after "several
weeks of following policies". Second account today = create BM2, create the
account there, then partner-share it to BM1 (BM2 Partners → share ad account →
BM1 ID) and assign your System User on it — existing app/token keeps working.

Agencies issue "setups": FB profile + proxy + BM share + N ad accounts + pages
(sometimes catalog). Billing topped via the agency (crypto). You're a TENANT:
can't make system users / change BM settings / assign some assets. Know your
level (BM → People → your user → assigned assets).

- Bans are routine: disabled → report → replacement → continue. A large share of
  fresh stock can be DOA (zero impressions from birth) — a team/stock-specific
  prior, not a fixed rate; replace, don't "fix". Document every ban (account ID,
  date, spend at death); agencies replace against lists.

**Cross-account creative discipline (practitioner, high-consensus): ONE creative = ONE
account.** Never duplicate the same campaign+creative across accounts: both hit the same users
(two accounts share one auction pool), audience freshness dies, the auction overheats on your
own TA → no leads + spam/reject flags. Per account: its own creative + separated audiences
(exclusions on converted leads, refreshed ~weekly; restart campaigns on refresh). Scale
horizontally by NEW creatives per account, not clones.

## Asset sharing (order of operations)

Pixel/catalog/pages live at BM level; a NEW ad account does NOT inherit them.
Missing-share symptom: ad error "Unassociated pixel" / "account does not have
access to pixel ID" — ad can't deliver. (Code 1815045 is field-observed and absent
from Meta's published reference; it is still a stable numeric code, so branch on it
like any other — `meta-ads/14` owns the rule. Never condition on the message string:
Meta rewrites and localizes those. Log `error_user_msg` as evidence only.)

Fix, in order:
1. Self-serve: business.facebook.com → Settings → Data Sources → Datasets →
   pixel → Assign ad accounts → tick → Save (needs BM role).
2. Agency: send account IDs + pixel ID to the agents chat.
Ads recover automatically after assignment — no rebuild (toggle off/on only if
delivery hasn't resumed within an hour). Same for pages (creative fails without
page access) and catalogs. Launch errors on an asset → check shares first.

## BM-level bans & asset recovery

Distinguish the LEVEL of the hit — recovery differs sharply:

- Single ad account disabled: routine (above); assets under the BM survive →
  replace the account.
- Whole BM restricted/disabled: child ad accounts can all stop at once and assets
  OWNED by that BM may go inaccessible — but scope VARIES by restriction type, and
  a Page/dataset can survive or stay reachable via another role. Check Business
  Support Home / Account Quality per asset before assuming it's lost.
- **Creation-link death chain** (practitioner prior, 2026 storm-era): accounts CREATED
  INSIDE one BM = one death chain — one account flagged → all BM-created accounts died
  (observed 6/6). Accounts created elsewhere and merely SHARED into a BM don't chain:
  observed 1/4 dead over 2 weeks. Shared pixel + catalog + FBP across such accounts was
  NOT the kill factor. Setup implication: create accounts with separate origins, add
  them into a working BM, keep the pixel/catalog/FBP sharing — but assume BM-created
  siblings fall together.
- **Lead-base uploads need a BM-owned account**: personal/legacy accounts can't host
  big uploaded custom-audience databases — keep 1–2 spare BM accounts per setup purely
  as the audience-holding core (exclusions / lookalike seeds), spend elsewhere.

Recovery (do NOT rebuild/farm to evade — that's a ban path, and Meta treats
replacement-to-evade as a violation):

- Own vs shared: an asset owned by a SURVIVING BM (or your own clean BM) can be
  re-shared into fresh accounts; an asset owned by the dead BM is gone. So keep
  the pixel/page on a cleaner, separate owner from the disposable ad-account BM
  where the agency allows it — a page/pixel outliving the ad accounts is the whole
  game.
- New pixel = cold: no event history, re-enters learning, custom audiences rebuild
  from zero — budget for the reset, don't expect the dead pixel's performance.
- Page: if it survives (owned elsewhere), re-share it — a warmed page with history
  is worth more than any single ad account; if it dies with the BM, social proof
  resets too.
- Agency tenants can rarely appeal a BM ban or move assets themselves → request a
  fresh setup (new BM + accounts + re-shared page/pixel), give the agency the dead
  BM ID + asset IDs.
- Freeze during an active BM review (SKILL non-negotiable #3): repeated
  appeals/edits mid-restriction are widely held to extend it — field prior, not
  documented.

## Ban detection loop (own detection, not just response)

Bans and silent stops are found by polling, not by noticing zero spend a day
late. Two sweeps, both cron-able:

- STATUS sweep (daily, per account): `GET /act_<id>?fields=account_status,
  disable_reason` — 1=active, 2=disabled, 3=unsettled (= unpaid balance, see
  billing above — a topup fixes it, not a replacement). Log every change with
  date + spend at death into the survival log (06) — that log is what makes the
  forensics and the agency replacement lists possible. Per-ad rejects:
  `effective_status=DISAPPROVED` on the ads edge.
- SPEND sweep (daily): yesterday's spend ≈ 0 on an account that was live =
  silent stop — ASL hit, unpaid balance, or a restriction that hasn't surfaced
  as a status yet. All child accounts stopping at once is also the earliest
- **Opportunity Score (Ads Manager overview, 0–100) is ADVISORY — not a signal.**
  Aggregates setup recommendations (A+, CAPI, creative count); restricted/grey
  verticals floor it to 0 because the recommendations are unappliable. Meta
  officially: "does not reflect actual or future performance". Not exposed via
  Graph API. The real signals are account_status/disable_reason, per-ad
  DISAPPROVED, and delivery-vs-budget gaps — not this score.
  BM-level signal (BM restriction, above).

This is the front of the chain: detection (here) → attribution (06) → response
(05). It feeds the daily kill/watch/scale watchlist in senior-buyer-ops/01.

## Billing gotchas that affect launches

- A "dead" account may just be an UNPAID BALANCE, not a ban: a failed payment
  pauses delivery and restricts the account. On agency crypto-topup setups,
  confirm the balance before requesting a replacement for a "banned" account.
- Account Spending Limit (ASL) is a LIFETIME cap across the whole account that
  pauses EVERY ad when hit — a silent full-stop that's easy to forget (distinct
  from ad-set budget and the billing threshold).
- Meta location fees (DST) sit ON TOP of spend, on impressions — full table →
  `08`. Read the invoice line, don't hardcode.

## Card / topup vendors (Meta) 🔺

Agency crypto-topup is the default, but for own-BM setups the card market looks
like this — directory pricing, vendor-reported (Partnerkin tools index, fetched
2026-08-27), counterparty risk, not endorsements:

| Vendor | As listed |
|---|---|
| Pay2.House | multi-currency, from $5 |
| AdsCard | Classic $2.5 / VIP $1 per card |
| Combo Cards | from $1/card |
| flexcard | from $2, "ADS BINs" |
| Capitalist | from $2.95 |
| 4×4.io | $2/issue + 5% on charges |
| Getsby | €3.99 + 3% + €0.99/mo — marketed for FB |
| PST.NET / XCards (ex-EPN) | from $10/card |
| ADVcash / Wallester / Soldo | wallet or licensed-issuer routes, from €0 |
| Linkpay / Adpos | on request, 2%+ |

"Ad-friendly BIN" claims come with no methodology — judge vendors on
replacement/refund terms and fund recovery (same test as Google-side resellers:
what happens on ban), not on BIN marketing. The card stays a linking signal to
the ad account (`07`).

## Naming (decide before first launch, never change mid-flight)

The tracker splits by campaign name ONLY because the campaign URL maps the FB
campaign-name macro into a tracker param (ad_campaign_id) — it is not automatic
(tracker-ops mapping contract, 03). Ad-level splits likewise need ad macros
mapped. Given that mapping:
- Campaign name = the ad account (e.g. J41-16), one campaign/account/test wave.
- Ad set = structure+creative (S1-creoName). Ad = creative name.
Gives exact per-account tracker CPL, readable Ads Manager, unambiguous kills.
Rename legacy campaigns before scaling — renames are safe, don't reset learning.

## Replacement pipeline

- Hold unused accounts in reserve; don't launch on all at once.
- Verdict (with TL): trash after ~$50 with CPL over target, or zero delivery in
  2-3 days, or any disable. Report in batches.
- On new accounts: check asset shares (pixel!), timezone, currency BEFORE building.
