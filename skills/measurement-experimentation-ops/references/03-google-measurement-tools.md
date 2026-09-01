# 03 — Google measurement tools

Reviewed 2026-08-27. Mode selection and validity traps are in the SKILL.md and `01` and apply
identically. This file covers only the Google-specific instruments and their limits.

## Native Experiments — self-serve, no rep required

Unlike Meta's Conversion Lift, Google's campaign experiments need no account team.

- Built from a **draft**; splits traffic between original and draft over a defined range.
- **Max 25 drafts per account** — a new draft silently fails to publish at the ceiling.
- Supports **geo-based splits** (holdout regions vs test regions) and **budget-level A/B** at campaign
  level.

**PMax experiments** carry an explicit Google warning: **do not run multiple experiments
simultaneously** — they interfere and degrade the read. Run sequentially, and minimize changes to the
campaign under test. Technically you *can* change budgets mid-experiment; doing so undermines the read.

## Conversion Lift

Requires a **Google account team** to request — not self-serve for all account types. More readily
available for Video and Demand Gen than for Search.

- **Minimum 7 days, maximum 56 recommended.** Studies under **14 days** risk up to a **17% drop in
  measured accuracy** for products with long conversion lag.
- **"Study Power"** is Google's own pre-check based on the conversion action, daily budget, expected
  lift size, volume, duration, and holdout %. **It tells you whether a conclusive result is possible
  before you spend anything on it** — run it first, always.
- **Search Lift states a $10,000 minimum spend.** Conversion Lift's threshold is unpublished and varies.

## Brand-search incrementality — the study everyone half-remembers

**eBay** (Blake, Nosko, Tadelis, 2015): pausing branded SEM by DMA produced **ROAS ≈ −63%**. Nearly all
lost paid clicks were recaptured organically.

**But Coviello et al. (2017) replicated the design on Edmunds.com** — a smaller, less organically
dominant brand — **and found materially different, less-negative results.**

> **Brand incrementality is brand-position dependent.** Quoting eBay at a non-dominant brand is a
> serious error, and it is extremely common. Never apply "brand search isn't incremental" without a
> brand-specific test.

The cheap version of that test: a **brand-exclusion holdout in PMax** for ≥4 weeks while keeping a
dedicated brand Search campaign live, comparing **total account** conversions and revenue — not the PMax
line item. Track **organic branded clicks in Search Console** as the secondary signal: real
incrementality loss shows up as organic brand clicks *not* recovering when paid brand spend is cut.

## PMax cannibalization measurement

The specific case where a naive read fails hardest. PMax auto-bids into brand auctions you would win
anyway, so **its reported ROAS is systematically inflated by conversions it did not cause.**

Measure with a holdout on **account totals**, never on the campaign's own metrics. State the trap
explicitly before anyone runs it: **excluding brand makes PMax's own ROAS look worse**, and judged on
that number the correct change gets reverted.

Evidence for how much overlap exists: 67% of PMax campaigns overlap Search on search terms, and Search
wins CVR **84% of the time** on the identical query (Adalysis).

## Meridian — the MMM

`github.com/google/meridian`, PyPI `google-meridian`. Google's current open-source Bayesian MMM,
successor to **LightweightMMM**, which is now effectively legacy.

Advances that matter for this skill: reach-and-frequency modeling · geo-level modeling · Search
query-volume signal · and **experiment calibration** — feeding Conversion Lift or geo-experiment results
in to calibrate channel coefficients. That last one is the bridge between the causal and modeled lanes:
**an MMM calibrated by a real experiment is a different evidence class from one fitted to observational
data alone.**

🔺 **Meridian GeoX** was reported announced May 2026 with testing later in 2026. Single secondary
source, no official page located. Verify before depending on it.

## What you cannot measure

- **AI Overview placement performance.** AIO-placed ads fold into "Top Ads" with **no segmented
  metric**. Any claim about "our AI Overview performance" from standard reporting is unfounded
  (`google-ads/05`).
- **PMax and Demand Gen competitive overlap** — not exposed through Auction Insights the way Search is.
- **Search-term performance below Google's privacy threshold** — a quarter to half of click volume has
  no visible term, and hidden queries skew worse (higher CPC, lower CTR). **The visible report is
  systematically more flattering than reality**, which biases any analysis built on it.
- **Match-type-level attribution under AI Max** — structurally impossible. n-gram and asset-level
  analysis are the only viable lenses.
- **Per-combination RSA performance** — the combinations report exposes impressions only.

Naming an unmeasurable thing as unmeasurable is a result. Do not substitute a proxy and present it as
the answer.

## Feasibility gate — Google edition

The SKILL.md gate applies, with Google-specific reasons causal measurement is often unavailable:

- **Conversion Lift needs a rep** and, for Search Lift, $10k minimum.
- **Low-volume accounts** cannot power a holdout — and below ~30 conversions/month the underlying Smart
  Bidding is itself unstable, so the treatment is not stationary.
- **The 2026-06-15 OCI cutoff** may mean backend truth cannot reach the platform at all on a new token,
  which caps what any in-platform experiment can measure.
- **Certification and geo gating** in regulated verticals can make a clean geo holdout illegal rather
  than merely impractical.

When causal is unavailable, say so and drop to the best affordable proxy — geo holdout, pre/post against
tracker truth, screening — **labeled directional.** The honest weaker method beats a "causal" test that
is silently contaminated.

## Two 2026 confounders that invalidate naive reads on Google

Check both before attributing any Google result to your own change:

1. **Market-level auction supply.** Optmyzr measured eligible auction impressions **−12.3% YoY** across
   21,425 accounts (Q1 2025 → Q1 2026). A pre/post spanning that shift measures the market, not your
   treatment.
2. **The 2026-08-17 budget-limited target enforcement.** Every tCPA/tROAS campaign flagged "Limited by
   budget" changed behavior on that date. A test straddling it has a structural break in the middle.

Neither surfaces as anything but a performance change. See `google-ads/02` and `/08`.
