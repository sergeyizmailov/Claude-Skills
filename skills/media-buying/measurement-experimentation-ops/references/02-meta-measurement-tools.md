# 02 — Meta measurement tools (verified 2026-08-11)

Which native tool gives which grade of evidence, with current names/params and
the caveats that matter. Version-sensitive — re-pin the API version and re-check
enums per release.

## Native A/B Test (Ads Manager → Experiments)

- Forces **random, non-overlapping** audience cells — its whole value over
  parallel ABO. Use for offer / LP / funnel / big-bet comparisons. [OFFICIAL:
  facebook.com/business/measurement/ab-testing — "random, non-overlapping"]
- Confidence: the results view shows a "% confidence this will be a winner." The
  widely repeated "~90% default" is likely the LIFT-test threshold; Meta's A/B
  framework appears to flag a "winner" at a LOWER bar (~65%+ cited), so an A/B
  "winner" is directional, not long-run-grade — don't treat it as a lift result.
  [PRACTITIONER; official help page geo-blocked at check — verify in-product.]
- "End test early if a winner is found" = automated peeking → leave OFF.
- Metric selection skews to "Cost per …"; conversion rate isn't native (build a
  custom metric). Clunky for high-volume creative iteration (one test per setup).
- UI mechanics (paths, metric limits, ABO-vs-Advantage+ screening) are documented
  once in meta-ads/08 §7 — this file owns only the evidence-grade framing.

## Marketing API — `AdStudy` node (programmatic tests)

- Node `ad_study`; docs at **v25.0** as of check — pin your version. [OFFICIAL:
  developers.facebook.com/docs/marketing-api/reference/ad-study]
- Study `type` enum includes: `SPLIT_TEST`, `LIFT`, `CONTINUOUS_LIFT_CONFIG`,
  `GEO_LIFT`, `BACKEND_AB_TESTING`, `PORTFOLIO_OPTIMIZER`, `VERSION_CONTROL`,
  `CREATIVE_SPEND_ENFORCEMENT`. Objective `type` includes `CONVERSIONS`,
  `BRANDLIFT`, `SALES`, `NONSALES`, `MPC_CONVERSION`. [OFFICIAL]
- Cells: name + `treatment_percentage` (float, ≤2 decimals) + ≥1 object
  (account/campaign/ad set IDs). Documented constraints: each cell's
  `treatment_percentage` **should be ≥ 10**, and the **sum across all cells ≤ 100**.
  [OFFICIAL: developers.facebook.com/docs/marketing-api/reference/ad-study/]
- Use for scripted split tests at scale and to launch lift/geo studies without
  the UI. Enums shift by version — the safe move is GET the node schema for your
  pinned version before building.

## Conversion Lift (incrementality — the real thing)

- Ghost-ads / intent-to-treat holdout: randomize into exposed vs holdout, log the
  counterfactual "would-have-seen" users, delta = TRUE incremental conversions
  (vs no-ads-at-all, unlike A/B which compares variant-vs-variant). [PRACTITIONER;
  method well-established]
- Now largely **self-serve in Experiments** (was rep-gated). BUT the clean
  "sandbox" holdout that excludes ALL your other campaigns still needs a Meta
  account team — **without a rep, expect holdout contamination from your other
  active campaigns**, which understates true lift. [PRACTITIONER — the material
  gotcha: a self-serve lift on a busy account is not a clean holdout.]
- Eligibility ≈ good standing + healthy Pixel/CAPI signal + enough expected
  conversions to hit sample in-window. No published hard $/conversion minimum —
  the tool shows a feasibility/power estimate and greys out if volume is too low;
  verify live in Experiments. [PRACTITIONER/UNVERIFIED threshold]

## Brand Lift

- Survey-based: incremental brand perception (recall/awareness) via poll to
  holdout vs exposed — a DIFFERENT objective from Conversion Lift, not a sales
  measure. ~$30k US self-serve minimum commonly cited (market-dependent).
  [PRACTITIONER — verify at facebook.com/business/help/417527072254206]
- Rarely relevant to direct-response grey buying; know it exists so you don't
  confuse it with Conversion Lift.

## GeoLift (when the pixel can't be trusted — the grey-relevant one)

- Meta OSS R package **`facebookincubator/GeoLift`**: geo holdout via **Synthetic
  Control** — quasi-experimental, NOT randomized. Data-driven MARKET SELECTION
  picks test/holdout regions (via the bundled power calculators), then builds a
  synthetic counterfactual from the untreated regions. Ships power calc + market
  selection + inference. R ≥ 4.0.0. [OFFICIAL: GitHub]
- Also expressible natively as `GEO_LIFT` in the `ad_study` node.
- Why it matters for grey: geo lift needs NO user-level pixel signal — it works
  on aggregate regional outcomes (even tracker/backend revenue by GEO). When
  ATT/consent/cloaking make user-level attribution unreliable, geo holdout is the
  most credible incrementality proxy you can actually run. Needs enough
  comparable geo units and stable spend.

## Robyn / calibrated MMM

- Meta OSS R package **`facebookexperimental/Robyn`** (MMM: ridge + evolutionary
  optimization, saturation/diminishing-returns curves, budget allocator). CRAN
  **v3.12.1 (2025-07)**, actively maintained, MIT. Python port `robynpy` is still
  **Beta** — R is the production path. [OFFICIAL]
- **Meridian is GOOGLE's MMM — do not conflate with Robyn.**
- "Calibrated MMM" = anchor the model's channel effects to experiment ground
  truth (Conversion Lift / GeoLift) so it reflects causal lift, not correlation.
  The pattern: run lift/geo tests → feed as calibration priors into Robyn. MMM is
  the top-down cross-channel view for when per-event attribution is degraded;
  calibration is what keeps it honest.

## Andromeda (why test design is shifting to creative/offer)

- Meta's next-gen ads **retrieval** engine (eng blog 2024-12-02): a deep net at
  the retrieval stage narrowing tens of millions of ads to a few thousand;
  reported ~10,000× retrieval-model complexity, +6% recall, +8% ad quality on
  segments. [OFFICIAL claims; buyer implication is interpretation]
- Implication: the machine does the user×ad×creative matching. Manual audience
  micro-slicing loses to broad + high creative volume + machine-selected
  combinations. So your testable surface is increasingly CREATIVE and OFFER, not
  audiences — design experiments accordingly (senior-buyer-ops/02 is the creative
  engine that feeds this).
