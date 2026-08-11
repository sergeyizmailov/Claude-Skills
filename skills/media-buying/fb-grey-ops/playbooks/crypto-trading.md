# Playbook — Crypto / trading / finance

Status: directional vendor benchmarks (dated below) + verified Meta policy.
NOT this team's live data — replace with your own. Heavily overlaps news-tg when
the pre-lander is a fake news article.

Funnel: FB/IG ad → pre-lander (news / review / quiz) → broker/exchange
registration → deposit. Lead = registration; paying gate = FTD (first deposit),
often a qualified/validated deposit.

## Event ladder & KPI

click → LP → **registration/lead** → **FTD** → qualified deposit → RevShare/CRG.
Primary KPI = CPA per FTD (or CRG cost-per-deposit). Quality delay + heavy scrub:
brokers validate deposits and reject low-quality — cohort by click date, reconcile
to the advertiser's validated count (tracker-ops 01).

## Economics (directional priors — NOT individually source-verified)

Cross-vendor bands (2025-26: HotForexLead, Triple Whale/Sovran, Affroom). Rough
sanity ranges, not audited — confirm per broker/GEO, replace with live data.
Keep payout, conversion, and your media cost separate:

Affiliate PAYOUT per FTD (what you EARN):
| offer | payout |
|---|---|
| crypto | $300-800 |
| forex | $150-400 |
| models | CPA / CPL / CRG (cost-per-deposit) |

Conversion rates:
| rate | band |
|---|---|
| lead → FTD | UAE 16-22%, India 12-18%, Nigeria 10-15%, Brazil 9-14%, Vietnam 8-13% |
| click → FTD | 0.5-1% avg; top partners 3-5%; tail <0.1% |

Meta CPM: finance = steepest CPMs on FB (no clean grey number). Your media CPA
per FTD (spend ÷ FTDs) is what you PAY — a separate number from the payout above;
e.g. at a $400 payout and 18% lead→FTD, break-even lead CPL ≈ $72.

## Creative concepts & first tests

News/review/quiz angles; "opportunity" framing (NOT get-rich-quick — policy).
First test 1-3-1 (directional screening, not a causal test — see 04) on
pre-lander angle; optimise to lead where FTD volume thin,
switch down once it builds. Spy: AdSpy / AdHeart.

## Common failure modes

- Broker scrubs hard on quality → optimise to the validated event, not cheap
  regs (click→FTD tail is <0.1% — most regs never deposit).
- Get-rich-quick / guaranteed-returns copy → instant reject/ban (policy).
- Prohibited instrument (binary options / ICO) → no permission path at all.

## Policy (docs-level, verified Aug 2026)

- Crypto = hard gate: exchanges, trading platforms, lending, buy/sell/swap/stake
  wallets, mining need PRIOR WRITTEN PERMISSION + a recognized regulatory
  license via Authorizations & Verifications (Meta Business Suite),
  jurisdiction-gated. Unauthorized crypto isn't runnable clean → rejection/burn.
- Flat-banned finance (no permission path): binary options, ICOs,
  penny/bidding-fee auctions, ≤90-day loans, bail bonds, get-rich-quick,
  recruitment-based returns (MLM). The fastest account-killers.
- Legit finance/trading: identity + regulatory-authorization verification;
  runs under FINANCIAL_PRODUCTS_SERVICES SAC (strips detailed targeting, 18+,
  limits some custom audiences).
- Personal Attributes: copy can't imply the reader's finances ("Drowning in
  debt?", "Turn $250 into $5,000") → product benefit.
- News-styled crypto pre-landers can also trip Social Issues if they debate
  regulation vs promote a product.

## Metrics discipline

- Pin which tracker event = payout (reg? FTD? qualified FTD?) before any CPA
  math (tracker-ops metric rule). Broker traffic is scrubbed on quality —
  optimize to the advertiser's validated event, not cheap regs.
