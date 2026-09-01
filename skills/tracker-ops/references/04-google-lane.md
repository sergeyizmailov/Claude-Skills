# 04 — Google lane

Reviewed 2026-08-27. The Meta lane is the rest of this skill; the metric discipline in the SKILL.md
applies identically. This file covers only what differs when the traffic source is Google Ads.

## The chain

```
click -> Google appends gclid -> tracking template ({lpurl} + {gclid}) -> tracker stores gclid
-> offer/LP -> conversion -> network S2S postback -> tracker -> upload back to Google (OCI)
```

Google Ads mechanics for the last hop → `google-ads/06`. Redirect and review-layer constraints →
`google-grey-ops/03`.

## Check this before building anything

**From 2026-06-15, `UploadClickConversion` fails unless the developer token has previously sent an
offline-conversion or enhanced-conversions-for-leads request.** A fresh developer token **cannot
onboard classic gclid-based OCI at all.**

Existing integrations keep working. New ones must go through the **Data Manager API** or enhanced
conversions for leads. Verify live status before committing engineering effort — this is a hard
blocker, not a deprecation warning. Implementation of the Data Manager hop is below; do not let a
gclid-only Worker become the whole lane.

## Post-cutoff path: Data Manager API [practitioner, MagicClick 2026-08]

Classic `UploadClickConversion` stays for tokens that already onboarded. New tokens:
`POST https://datamanager.googleapis.com/v1/events:ingest`.

- Conversion action: Tools → Conversions → Import → **Clicks** → Website (Import from clicks).
  Address-bar `ctId=` = `conversion_action_id` / `productDestinationId`.
- GCP: enable **Data Manager API**; service-account JSON; invite `client_email` as **Standard**
  user on the CID (hyphens stripped). JWT-bearer scope
  `https://www.googleapis.com/auth/datamanager`. This SA path is **Data Manager only** —
  Google Ads API still has no SA auth (`google-ads/10`).
- `{gclid}` expands **only** in the Final URL Google Ads actually stores. A cloak/intermediary
  must **forward the already-substituted value**. Putting `{gclid}` in the cloak's own redirect
  sends the literal 7 characters.
- Capture **gbraid/wbraid too** — a gclid-only Worker silently drops iOS. Windows / dedup /
  `partial_failure` still apply; Data Manager does not waive them.
- Send **Approved/payout** events only. 🔺 Vendor: 14-day trial before the action feeds bidding
  (visible in reports immediately) — verify in-product.

## Click IDs — three, not one

| ID | When |
|---|---|
| `gclid` | Any web click, including mobile web |
| `gbraid` | Web click → iOS **app** conversion, ATT consent granted |
| `wbraid` | iOS app click → **web** conversion, without full ATT. Aggregated, non-user-identifying |

**Capture all three plus `gad_source` and `gad_campaignid` on every landing page. Store all, submit
whichever is populated.** A tracker capturing only `gclid` silently loses iOS traffic entirely.

## ValueTrack — the escaping ladder

Google explicitly designs ValueTrack around multi-hop tracker redirects. This is the supported path,
not a workaround.

| Token | Behavior |
|---|---|
| `{lpurl}` | Final URL. **Escaped unless placed at the very start of the template** |
| `{lpurl+2}` / `{lpurl+3}` | Double / triple-escaped for 2- or 3-hop chains |
| `{unescapedlpurl}` / `{escapedlpurl}` | Never escaped / escapes `: / ? = %` |
| `{ignore}` | Drops tracking elements from the final URL to cut crawl load. Final-URL only |
| `{campaignid}` `{adgroupid}` `{creative}` `{matchtype}` `{device}` `{keyword}` `{targetid}` | Mapping and segmentation |

**Syntax:** `{lpurl}` at template start uses a literal `?`; anywhere else it must be `%3F`
(double-escaped `%253F`, triple `%25253F`).

**Tracking-template changes take 24–48h to propagate to serving.** Do not judge a broken chain sooner —
you will chase a phantom and change two variables at once.

**Parallel tracking** sends the user straight to the Final URL while the template fires in the
background — no added latency. RedTrack explicitly **discourages** it unless Google has approved it for
your setup.

## The mapping contract

Same rule as the Meta lane: **the split is not automatic.** The campaign name must encode whatever the
tracker needs, and the tracking template must carry it into a tracker parameter.

Google-specific: **`{campaignid}` is the reliable key**, not the campaign name string. Names change;
IDs do not. Map ID → account/campaign in the tracker rather than parsing names.

## Tracker configuration

### Keitaro

- Maintenance → Integrations → Google Ads → OAuth → **Customer ID without hyphens** → select campaigns.
- **`{campaignid}` must be in the tracking template** or cost never attributes correctly.
- **Conversions post back only when `gclid` is present. No gclid → no postback, silently.** This is the
  single most common "why are conversions missing" cause on Google traffic.
- Cost sync every **12h**; conversion postback every **6h**. Plan the daily routine around these, not
  around Meta's cadence.
- **MCC/manager accounts are explicitly unsupported.**
- Vendor guidance: disable cookie tracking to reduce moderation risk.

### RedTrack

- Requires a **custom tracking domain via CNAME + SSL** — not raw redtrack.io.
- Protected macro roles: `{creative}`→Aid, `{adgroupid}`→Gid, `{campaignid}`→Cid.
- **PMax puts parameters in the Final URL suffix field, not the Tracking template.** All other types use
  the tracking template. **YouTube is ad-level only.**
- **Google's "count one conversion per click" setting breaks GBRAID/WBRAID upload.**
- Retries upload every 4h for up to 36h. Latency ~24h standard, **~48h for iOS conversions with no
  clickid** — do not judge iOS cohorts on day-one numbers.
- **Connected account must be the account running the campaigns — MCC-to-subaccount does not work.**

🔺 **Voluum** markets an API S2S postback plus Automizer cost sync; technical docs unreachable.
**Binom** has no located Google-specific traffic-source doc. Verify against current vendor docs before
writing operational steps for either.

## Timezone — the failure mode

`conversion_date_time` must be `yyyy-mm-dd HH:mm:ss+|-HH:mm` — **a space, not `T`, and the offset is
mandatory.**

**Normalize every tracker and network timestamp to one explicit offset before building the payload.**
Mixing local-server time with offer-network time produces `CONVERSION_PRECEDES_CLICK` and
`EXPIRED_CLICK` partial failures, especially when tracker and network sit in different zones.

Reporting tz: same rule as the Meta lane — daily CPL/CPA in the **ad-account timezone** for both
spend and conversions. Google's account timezone is permanent (SKILL rule 4), so if it disagrees
with the tracker, reconcile in the tracker, never by eyeballing.

## Backdate windows

| Path | Max |
|---|---|
| Standard gclid OCI | **90 days** after the click — beyond this the row is **silently dropped** |
| Enhanced conversions for leads | **63 days** |
| Conversion adjustments | **54 days** from first recording (55 is **Hotel Ads only**) |

**Any funnel with a payout event maturing beyond ~2–3 months cannot feed the terminal event back
directly.** Upload an in-window proxy milestone, then true up value with adjustments.

## Dedup

**The key is `gclid` + conversion action + conversion date/time.** Re-uploading the identical triple is
a no-op.

> **`order_id` is NOT a dedup key for standard gclid imports.** Dedup on it in your own system before
> sending. This differs from what most tracker documentation implies.

## Non-negotiables for this lane

- **Always set `partial_failure = True`**, iterate `partial_failure_error`, and reconcile accepted vs
  rejected counts against the tracker export nightly. Rows past the window drop silently — a pipeline
  that never checks looks healthy while delivering nothing.
- **Optimize on the payout event, not the front-end lead.** Front-end leads are frequently 30–70% junk;
  bidding on them teaches Smart Bidding to find more junk. Set the front-end action to secondary and
  create a primary **Import**-category action fed from the tracker (`google-ads/06`).
- **Cross-check tracker conversion count against Google's reported conversions** for the same window in
  the same timezone. Divergence means wrong metric or broken chain — stop and reconcile before
  reporting, exactly as in the Meta lane.
- A 20–30% variance between Google Ads and GA4 is **expected** and is not evidence of breakage
  (`google-ads/06` enumerates all nine causes).
