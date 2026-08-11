---
name: fb-grey-ops
description: "Grey-vertical Meta (FB/IG) buying: antidetect/proxy/session survival, agency accounts, token/session death, API mass-launch, tracker naming, per-vertical playbooks (nutra, gambling, crypto, news...). The infra+survival layer. Clean marketing = meta-ads; metrics = tracker-ops."
---

# FB Grey Ops

Launch grey verticals at scale without getting accounts/tokens/sessions killed.
Vertical-agnostic infra + survival. Boundary: "buy well" → meta-ads ·
"don't get killed / launch at scale" → here · "count & sync" → tracker-ops ·
"portfolio / TL decisions / creative + funnel ops" → senior-buyer-ops.

Authority (they are NOT one ruleset): this skill governs grey-vertical
execution; meta-ads' clean-marketing guardrails (no cloaking/bypass/account
farming) are authoritative for compliant accounts, not for grey work. Route by
lane; don't merge the two normative stances or treat them as mutually
authoritative.

Stack-agnostic: antidetect (Dolphin/AdsPower/GoLogin/Octo/Multilogin),
proxies, trackers all interchange — the discipline below is what matters, not
the brand.

## Non-negotiables (always apply)

1. One identity = one IP (session hygiene, not a Meta auth requirement). FB
   profile lives in ONE antidetect profile, ONE proxy; every browser/user-token
   touch (API via user token, token gen, developers.facebook.com) exits the SAME
   IP. Bake the proxy into scripts so it can't be forgotten. Exception:
   server-side System User calls don't ride a browser session (01/02) — but
   agency tenants rarely have one, so same-IP is the default.
2. A token rides a login session. Anything that kills the session (logout,
   password change, Meta security rotation, multi-session flag) kills every
   token from it — even 60-day long-lived.
3. During a restriction/checkpoint: FREEZE. No re-logins, token regen, or
   profile edits — each action extends the flag.
4. Never touch a work identity from a personal browser/IP. No exceptions.
5. Fresh agency accounts are fragile. The "~2x CPM / ~half DOA" figures are one
   team's prior on their stock, not a universal property of agency accounts —
   but the DISCIPLINE is general: judge after $30-50 spend (not first hours) and
   keep a replacement reserve.

## Route references

| Need | Reference |
|---|---|
| Antidetect, proxies, IP/session discipline, checkpoints, restrictions, domain/pixel rotation cadence | `references/01-infra-and-identity.md` |
| App setup, Live mode, permissions, token lifecycle, System User, death codes | `references/02-meta-app-and-tokens.md` |
| Agency setups, BMs, asset sharing, BM-ban & asset recovery, billing gotchas & fees, naming, replacements | `references/03-agency-accounts-and-bm.md` |
| API mass launch: structures, params, bid strategies, scheduling, images, spend warm-up | `references/04-mass-launch-api.md` |
| API errors — grey survival response (freeze/replace/rotate); canonical code→fix in meta-ads/14 | `references/05-api-error-catalog.md` |
| Why accounts die, attributed: hazard-rate forensics, balanced infra tests, anomaly pivots, incident fingerprints | `references/06-portfolio-forensics.md` |
| Per-vertical playbooks | `playbooks/` |

Playbooks: news-tg.md is filled (one team); nutra/casino/crypto-trading carry
directional vendor benchmarks (dated/sourced) + event ladders — replace the
numbers with your live data. The shape ports to any vertical (dating, sweeps,
ecom, apps, loans, adult...).

## New-job bootstrap (proven order)

1. Collect access (ad account IDs, BM, pages, pixel, tracker campaign URL,
   proxy) → project notes, verbatim, gitignored.
2. Meta app: Live mode → mint user token in the antidetect profile → exchange
   long-lived → store. All API calls via the setup proxy.
3. Tracker API key → verify a read report.
4. Naming BEFORE first launch: campaign name encodes the ad account — this only
   splits in the tracker because the campaign URL maps it into a tracker param
   (not automatic; tracker-ops mapping contract). Ad name = creative name. Map
   ad → creative.
5. Launch champions structure (04), scheduled 00:00 account tz.
6. Daily sync (Meta spend → tracker cost → report) before the team deadline;
   verify one day manually, then trust it.
7. Kill rules with the TL in writing: spend-without-lead cap, CPL cap, account
   verdict threshold.
