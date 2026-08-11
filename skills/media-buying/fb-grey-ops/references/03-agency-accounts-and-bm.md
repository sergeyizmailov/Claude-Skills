# 03 — Agency accounts, BMs, asset sharing

Agencies issue "setups": FB profile + proxy + BM share + N ad accounts + pages
(sometimes catalog). Billing topped via the agency (crypto). You're a TENANT:
can't make system users / change BM settings / assign some assets. Know your
level (BM → People → your user → assigned assets).

- Bans are routine: disabled → report → replacement → continue. ~Half of stock
  is DOA (zero impressions from birth) — replace, don't "fix". Document every
  ban (account ID, date, spend at death); agencies replace against lists.

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
