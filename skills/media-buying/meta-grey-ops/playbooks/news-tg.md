# Playbook — News funnels: FB ads → news pre-lander → Telegram subscription

Status (reviewed 2026-08-28): FILLED FROM LIVE WORK (Aug 2026). Benchmarks are one team's, re-verify
per team. Vertical: "news-style" crypto/finance persona funnels to a TG channel.

## Funnel anatomy

FB/IG ad (news-style image, no ad-level texts per moderation rules) → Keitaro
campaign URL (cloaca: bots/reviewers to a white page, real users to the black
news pre-lander) → pre-lander (fake news article, persona story) → CTA to a
Telegram channel. Lead = TG subscription, tracked by postback into the
tracker. Deeper funnel (registrations, deposits, revenue) happens behind the
channel and is judged by the TL — cheap low-quality subs are a trap.

## Economics and benchmarks (one team, US GEO)

- Target CPL (subscriber): $10. Team working range $9-11 on seasoned accounts.
- Healthy account: CTR 5-7%, CPM $16-32, CPC $0.28-0.50.
- Fresh agency accounts: CPM $44-68 (2x premium), normalizes over days.
- Per-account variance with identical funnel: $5 to $25 CPL — account quality
  is the decisive variable. "Find converting accounts" is the game.
- Click→sub conversion on a healthy funnel: ~5-6% of Meta link clicks.
- Payout models seen: % of spend on a CPL sliding scale (e.g. $8→12%,
  $10→10%, $12→8%).

## Launch rules (proven)

- Objective: Leads (NOT Sales — Sales blocks Lead/Submit Application events).
  Conversion event: Submit Application on the shared team pixel.
- Targeting: USA 20+, Advantage+ broad, auto placements; kill placements with
  suspiciously cheap CPM and zero leads.
- Structure: probe 1-1-3 to find delivering accounts; screen creatives with
  1-3-1 (directional, not a causal test — see 04 / measurement-experimentation-ops);
  scale winners 1-1-3 + budget steps or horizontal (more accounts).
- Creatives: news-photo style with baked-in headline text; no ad-level
  primary text/headline (moderation rule); display link a big news domain
  (real destination stays the tracker link); CTA Learn more; all enhancements
  off except Hide price; multi-advertiser off.
- Uniquify creatives per account before upload.
- Scheduled start 00:00 account time for a full first day.

## Kill and verdict rules (agreed pattern)

- Creative: no lead after ~$20 (1.5-2x target CPL), or CTR <2% → off.
- Adset: CPL stable above $12-15 after 2-3 leads → off.
- Account: verdict after ~$50 or 3 days — CPL persistently >$15-25 → replace.
- Zero impressions in 2-3 days with live campaign → replace (normal for
  agency stock, don't fix).
- Automated rule per account: Spend > $20 lifetime AND Results < 1 → turn
  off ad sets, run continuously.

## Metrics discipline

- TG subscription = tracker "leads" (Keitaro). "conversions" counts the whole
  funnel's postbacks — this team observed ~3.5-4x their lead count, but that
  ratio is setup-specific (tracker-ops metric rule), never a CPL denominator.
  Cross-check: Meta pixel Lead ≈ tracker leads.
- Day = ad account timezone day for both spend and leads.
- Bot share spikes in tracker = cloaca filtering hard; watch for domain or
  account ban after.

## Policy note (docs-level, verify in practice)

- A "news-style" persona does not by itself trigger a Special Ad Category —
  the trigger is CONTENT: an ad advocating/debating a topic of public
  importance (economy, health, crypto regulation, etc.) can fall under Social
  Issues, Elections or Politics. Neutral product promotion does not. Keep the
  creative on the product/offer, not on a debated issue.
- The financial/crypto angle common to these funnels can pull the ad into the
  FINANCIAL_PRODUCTS_SERVICES category or the crypto/financial authorization
  gate — see the crypto-trading playbook and meta-ads policy
  reference before running a finance-flavored news funnel.

## Ban patterns observed

- Ad accounts die in batches early (fresh stock, first spend) — expected,
  replace; no appeal.
- No creative-level reject flags even when accounts die — account quality,
  not creative content, is usually the trigger.
- FB profile restrictions (multiple sessions) come from IP/device
  inconsistency, not from ads — see 01-infra-and-identity.md.
