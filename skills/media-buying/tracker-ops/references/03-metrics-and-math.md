# 03 — Metrics, math, markup, routine

Principles below port to any tracker (Voluum, RedTrack, BeMob, PeerClick...);
only the API surface differs (01/02).

## CPL that doesn't lie

Daily CPL = Meta spend (account-tz day) / tracker payout-metric count (same day).
- Spend truth: ad platform API per account/day. Gotcha: `/me/adaccounts` returns
  only LIVE accounts — disabled ones vanish and their spend silently drops from
  totals. Keep your own spend log (or agency billing) for history with dead
  accounts.
- Lead truth: tracker, the AGREED payout measure only (not "conversions" =
  all postback records; how much that exceeds your leads is integration-specific,
  not a fixed multiple — SKILL metric rule).
- Cross-check: pixel leads ≈ tracker leads. The ±20% tolerance is an
  account-specific rule of thumb, not a Meta/tracker constant — set your own
  from a reconciled baseline. A bigger gap = wrong metric or broken tracking →
  stop and reconcile before reporting.

## Reconciliation tree (when Meta ≠ tracker)

Branch on DIRECTION — the causes are different:

Meta pixel leads > tracker leads (Meta sees more):
- tracking loss before the tracker: click-ID/subid dropped in the redirect chain
  or prelander (senior-buyer-ops/03), postback not firing/failed
  (tracker-ops 01 replay), or pixel double-counting (dedup/event_id).
- wrong tracker metric picked (counting a deeper status than the pixel event).

Tracker leads > Meta pixel (tracker sees more):
- pixel under-fires: WebView/in-app browser strips it, consent/ATT blocks it,
  CAPI not sending → prefer S2S truth, fix the pixel.
- attribution-window / timezone mismatch (Meta modeled/attributed vs tracker raw).
- bots/duplicate postbacks inflating tracker (check tid/overwrite, 01).

Either way: reconcile ONE clean day end-to-end first (fire a test conversion,
follow it both sides), set your own tolerance from that baseline, then trust the
delta — don't chase noise day to day.

## Funnel metrics (what each says)

- CTR(link): creative. CPM: account/auction quality (fresh ~2x premium).
  LP CTR: pre-lander. click→lead CR: whole funnel (judge on 100+ clicks).
  reg→deposit / lead→sale: lead QUALITY (what the advertiser judges; cheap
  low-quality leads lose deals).

## Anti-fraud / cloaking signals (read as a set)

- raw clicks >> unique: bot refresh / source re-fire — judge cost on payout
  count, not raw clicks.
- rising bot_share / proxies: moderation crawlers on the white page; some is
  normal on a cloaked funnel, a rising trend precedes domain/account bans. This
  is the SIGNAL; the response (domain rotation) is a grey-ops action — see
  fb-grey-ops/05.
- near-zero LP CTR w/ normal clicks: cloaca over-filtering real users (or black
  page broken) — a tracking fault, not bad traffic; fix the filter, don't kill.
- empty_referrers spike: stripped/direct traffic — correlate with bot_share.
- unsubstituted `{{...}}` rows: exclude from analysis, then classify — bots, or
  a broken template / unsupported macro / manual traffic (fix your template
  first if it's yours).

## Markup & the mapping contract

There is no automatic split — the tracker only knows what your campaign URL
maps into its parameters. Nail down this contract before analysis (it's the
single thing that makes per-account/per-ad numbers real):

| Meta side (macro) | → tracker param | carries |
|---|---|---|
| `{{campaign.name}}` | ad_campaign_id (or a sub_id) | your campaign-name convention (= ad account) |
| `{{adset.id}}` / `{{ad.id}}` | sub_id_N | per-adset / per-ad split (only if mapped) |
| FB click id (fbclid / macro) | external_id / subid | click identity for the return postback |
| offer event (reg/FTD/sale) | postback `status` | which status = your PAYOUT metric |

- FB substitutes macros at click time; the tracker splits by `ad_campaign_id`
  ONLY because your URL feeds the campaign name into it — it is not intrinsic
  (01). Per-ad splits need `{{ad.id}}`→sub_id_N mapped; confirm before assuming
  per-ad analysis.
- FB naming discipline IS the tracking plan (fb-grey-ops/03): campaign name =
  ad account, ad name = creative — so the contract above resolves cleanly.
- Pin the payout `status` in the contract too — optimization event, tracker
  status, and payout event must line up or CPL/ROI is measuring the wrong thing.

## Daily routine (automate)

For YESTERDAY (account tz): pull Meta spend/impr/clicks per live account → push
total spend to tracker cost (idempotent) → pull tracker payout count → fill the
team report (raw columns, formulas compute) → read per-account CPL vs target →
kill/watch/scale → log snapshot. Missed days: re-run per date (scripts take a
date arg).

## Reporting upward

Use the team's lead definition + their timezone (ask which the sheet uses).
Never report a metric not reconciled once against a second source. Keep a dated
stats log; correct by appending, not rewriting.

<!-- Changelog 2026-08-11: Added anti-fraud/cloaking signal reading + "ports to
other trackers" note. CPL is computed in account tz here; a Keitaro `cpl` metric
also exists on many installs (see 01). Compressed to dense form. Peer-review
(gpt): labelled ±20% and the inflation ratio as account-specific; moved the
domain-rotation ACTION to fb-grey-ops (signal stays here); added the Meta↔tracker
mapping contract (params, statuses, payout event). Peer-review r2 (gpt): added a
directional reconciliation tree (Meta>tracker vs tracker>Meta). -->

