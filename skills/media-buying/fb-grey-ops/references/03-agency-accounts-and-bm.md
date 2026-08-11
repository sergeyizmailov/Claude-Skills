# 03 — Agency accounts, BMs, asset sharing

Agencies issue "setups": FB profile + proxy + BM share + N ad accounts + pages
(sometimes catalog). Billing topped via the agency (crypto). You're a TENANT:
can't make system users / change BM settings / assign some assets. Know your
level (BM → People → your user → assigned assets).

- Bans are routine: disabled → report → replacement → continue. A large share of
  fresh stock can be DOA (zero impressions from birth) — a team/stock-specific
  prior, not a fixed rate; replace, don't "fix". Document every ban (account ID,
  date, spend at death); agencies replace against lists.

## Asset sharing (order of operations)

Pixel/catalog/pages live at BM level; a NEW ad account does NOT inherit them.
Missing-share symptom: ad error "Unassociated pixel" / "account does not have
access to pixel ID" — ad can't deliver. (Code #1815045 is field-observed, not
in Meta's published reference — match the message.)

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
- Whole BM restricted/disabled: every child ad account stops at once, and the
  pixel/page/catalog OWNED by that BM go inaccessible with it. The expensive one.

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
- Freeze during an active BM review (SKILL non-negotiable #3): appeals/edits mid-
  restriction extend it.

## Billing gotchas that affect launches

- A "dead" account may just be an UNPAID BALANCE, not a ban: a failed payment
  pauses delivery and restricts the account. On agency crypto-topup setups,
  confirm the balance before requesting a replacement for a "banned" account.
- Account Spending Limit (ASL) is a LIFETIME cap across the whole account that
  pauses EVERY ad when hit — a silent full-stop that's easy to forget (distinct
  from ad-set budget and the billing threshold).
- Fees sit ON TOP of spend, so real CPL > what Ads Manager shows — fold into
  break-even: Meta "location fees" (a % keyed to the audience's jurisdiction,
  rolling out ~2026-07, separate invoice line) + VAT. Rates/countries change —
  read them off Billing, don't hardcode.

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
