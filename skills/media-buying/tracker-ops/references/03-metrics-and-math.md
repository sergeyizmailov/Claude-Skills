# 03 — Metrics, math, markup, routine

Principles below port to any tracker (Voluum, RedTrack, BeMob, PeerClick...);
only the API surface differs (01/02).

## CPL that doesn't lie

Daily CPL (for BUYING) = click-date spend (account-tz day) ÷ that same click-date
cohort's payout count. "Same day" only holds once the cohort has matured; while
it's still lagging, use the matured or nowcast cohort count (cohort nowcasting
below), NOT today's raw postback count — pairing click-date spend with
conversion-date conversions is the classic apples-to-oranges CPL. Conversion-date
basis (postback day) is for FINANCE/cashflow, not for buying decisions.
- Spend truth: ad platform API per account/day. Field-observed gotcha (not a
  documented Graph contract): a plain `/me/adaccounts` pull can omit disabled
  accounts, so their spend silently drops from totals — verify what your
  edge+fields actually return, and keep your own spend log (or agency billing)
  for history with dead accounts.
- Lead truth: tracker, the AGREED payout measure only (not "conversions" =
  all postback records; how much that exceeds your leads is integration-specific,
  not a fixed multiple — SKILL metric rule).
- Cross-check: pixel leads ≈ tracker leads (±tolerance is account-specific, set
  from a reconciled baseline — SKILL rule #3). A bigger gap = wrong metric or
  broken tracking → stop and reconcile before reporting.

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

### iOS ATT & the Meta↔tracker gap (segment, don't assume direction)

iOS ATT degrades USER-LEVEL signal: no consent → no IDFA, and app conversions
lean on SKAdNetwork/AAK (aggregated, delayed, capped). But this does NOT mean
Meta always shows fewer — Meta backfills with modeling + view-through, so its
number can land EITHER side of tracker/backend (same as meta-ads/08: "either side
can be higher"). What's real: iOS user-level attribution is noisier, and the gap
is OS/GEO-dependent — larger on iOS-heavy T1 (US/UK/AU), smaller on Android-heavy
T2/T3. Global ATT opt-in ≈ 35–38% (2025→2026, moving — verify). Implications:
- Segment Meta-vs-tracker deltas by OS/GEO before reconciling — an iOS-heavy
  campaign's gap is expected noise, but don't presume its DIRECTION.
- On iOS-heavy traffic treat S2S/postback as the more stable money-truth and
  Meta's iOS figure as modeled — reconcile, don't blindly trust either side.
- PWA/web funnels don't use SKAN (they're web, senior-buyer-ops/03) — this mainly
  bites real native-app / store flows.

## Multi-tracker sync & the conversion ledger

Two trackers in the chain (your Keitaro + the network's tracker, or a redirect
tracker + an analytics one) will NOT agree by default — different click-id keys,
timezones, dedup, bot filters. Pick ONE as source of truth for money (usually the
one that holds the payout postback); treat the other as cross-check, never a
second total to add.

- Join key: they reconcile only if a shared click id crosses both — carry your
  subid/external_id into the network as its sub param and back on the postback, so
  each conversion matches 1:1 across both. No shared key → you can only compare
  aggregates, not rows.
- Align timezone/window to the ad-account tz before comparing a day; a "gap" is
  often just a boundary/lag mismatch (reconciliation tree above).

Conversion ledger (raw, append-only): log every INCOMING postback verbatim —
timestamp, subid, status, payout, tid, raw query — separate from the tracker's
own mutable state. Why it's worth the trouble:

- Rebuild/replay: if the tracker breaks or a status scheme changes, re-import
  conversions (Keitaro imports via subid+status+payout+tid; the postback log is
  the source) instead of losing the period.
- Scrub disputes: you can prove exactly what the network sent, postback by
  postback, when they later "adjust" approvals.
- Dedup audit: distinct-tid vs overwrite behaviour is verifiable against the raw
  stream. Append, never rewrite; key each row by an idempotency id (subid+tid+
  status) so a replay can't double-count, and REDACT tokens/PII from the stored
  query — don't keep secrets raw.

## Funnel metrics (what each says)

- CTR(link): creative. CPM: account/auction quality (fresh ~2x premium).
  LP CTR: pre-lander. click→lead CR: whole funnel (judge on 100+ clicks).
  reg→deposit / lead→sale: lead QUALITY (what the advertiser judges; cheap
  low-quality leads lose deals).

## Cohort nowcasting (decide before the cohort matures)

Today's CPA looks terrible because today's conversions haven't posted back yet
(confirm/deposit/KYC lag). Don't wait blind and don't judge raw — project the
mature number:

1. Build the completion curve from history: take matured click-date cohorts,
   bucket each conversion by lag = conversion_time − click_time (Keitaro
   `/conversions/log`: `postback_datetime` − `click_datetime`; Binom: the
   built-in `Time since click` column, 02). p(d) = cumulative fraction of a
   cohort's eventual conversions that have arrived by age d days.
2. Nowcast a fresh cohort: `predicted_mature ≈ observed_to_date ÷ p(age_so_far)`;
   `predicted_CPA = spend ÷ predicted_mature`. Decide kill/scale on the NOWCAST,
   not the raw immature count (feeds senior-buyer-ops marginal scaling + team
   stop-loss — both require MATURE numbers).
3. Keep the two bases separate: click-date cohorts drive MEDIA decisions (a
   conversion belongs to the click that caused it); conversion-date drives
   FINANCE/cashflow (when money actually lands). Never mix them in one figure.

Caveats: the curve DRIFTS — a new offer/GEO/season changes the lag, so refit on
recent cohorts, don't reuse a stale curve. Low-volume cohorts give a noisy
nowcast (wide error) — treat as directional. And a never-arriving conversion
isn't lag: a broken/failed postback looks identical to a slow one early on, so
rule out a tracking break (01) before trusting the projection.

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
- unsubstituted `{{...}}` rows: exclude-then-classify (SKILL rule #5) — read
  alongside the signals above, not automatically as bots.

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

## Backend optimization contract (which status → which CAPI event)

Three events that people conflate but are usually DIFFERENT — pin each
separately, because optimizing the wrong one is the most expensive silent error:

- REPORTING event — what you show the team / call a "lead".
- PAYOUT event — the tracker status you actually get paid on (senior-buyer-ops
  operating-contract #1).
- OPTIMIZATION event — the CAPI/Pixel event the ad set bids toward. This is the
  one Meta's delivery learns from; it drives who you get shown to.

Wiring: tracker/CRM status → CAPI event back to Meta. The separate Offline
Conversions API was discontinued (~May 2025, widely reported — confirm the
dataset migration in Events Manager) — all CRM/backend stages now flow through
standard CAPI into the dataset. Set `action_source` to where the conversion
ACTUALLY happened, from the enum (`website`, `app`, `phone_call`, `chat`, `email`,
`physical_store`, `business_messaging`, `system_generated`, `other`) — NOT
`system_generated` for every server postback. `system_generated` is only for
conversions that occur automatically with no customer interaction (e.g. a
subscription auto-renewal). Set `action_source` PER EVENT by where THAT stage
actually happened — don't auto-inherit it from the original lead's source. CAPI
mechanics live in meta-ads/08; this is which status maps to what.

Choosing the optimization event = reliability × volume × correlation-with-payout:
- Deeper event (FTD / confirmed sale) is best aligned with revenue but LOW volume
  → an ad set may never clear the learning-phase volume floor (Meta's ~50
  optimization events/ad set/7d — a documented heuristic, verify live), so Meta
  optimizes badly. Shallower event (reg / lead) is high-volume and easy to
  optimize but weakly correlated with payout → cheap junk that never converts
  downstream.
- Rule: optimize for the DEEPEST event that still clears the learning-volume bar.
  If the payout event is too rare, optimize a reliable UPSTREAM proxy that
  correlates with payout, and monitor that correlation (reg→FTD rate) so you're
  not scaling volume that dies downstream.
- Value optimization (VBO) needs `value`+`currency` and clears a volume gate thin
  grey funnels often can't meet → optimize on conversion COUNT and control quality
  via which status you send back, not VBO. (Exact VBO + Conversion-Leads
  eligibility numbers live in meta-ads/08 — single source.)
- Native lead forms: Meta's Conversion Leads goal (Lead Ads / Instant Forms) takes
  CRM stage events via CAPI to optimize a down-funnel stage instead of raw form
  fills — eligibility gates in meta-ads/08.
- Only send events you can stand behind (deduped via event_id, real): the
  optimization signal also feeds Meta's quality modeling — noisy/fake events
  degrade delivery, not just reporting.

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
