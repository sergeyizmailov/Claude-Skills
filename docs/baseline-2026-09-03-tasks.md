# Baseline tasks (answer each as an expert operator would, today is 2026-09-03)

T1. Meta: a conversions ad set (OFFSITE_CONVERSIONS, pixel Lead) doubled CPA over 5 days, spend flat, CTR flat, CPM +40%. Give the diagnostic order and the first three concrete actions. Name which Ads Manager columns/breakdowns you would read.

T2. Meta Marketing API v26: you must create an ad set via POST /act_X/adsets with 1-day-click / 1-day-view attribution and Advantage+ audience OFF. Write the exact JSON fields for attribution_spec and the targeting flag. Can attribution be changed after creation?

T3. Meta: creative via POST /act_X/adcreatives for a single image link ad. Which fields switch off every Advantage+ creative enhancement and multi-advertiser ads? Give field names and values.

T4. Meta: Graph error 1885501 on ad set create, and separately error 1487832 on a catalog video creative. What do they mean and what is the fix for each?

T5. Google Ads: it is 2026-09-03. A client runs Search campaigns with campaign-level broad match and legacy Automatically Created Assets. What is happening to those campaigns this month, is there an opt-out, and what survives?

T6. Google Ads: PMax is taking brand queries from an exact-match brand Search campaign. Which two settings stop it, and what is the only guaranteed rule about Search vs PMax query arbitration?

T7. Google Ads API (latest version): create a Search campaign via MutateOperations in one request with a budget and a campaign in the same call. How do you reference the not-yet-created budget from the campaign, how do you validate without creating, and what status should the campaign be created in? Which field declares EU political advertising?

T8. Google Merchant Center: new account, products uploaded, all show "pending" for 5 days, then account gets "Misrepresentation" suspension. What is being reviewed (feed or site), what site elements are checked, and what should NOT be done (name the policy that a second account triggers)?

T9. Merchant Center ↔ Google Ads: link a Merchant Center account to an Ads account via API only. Name the services/resources on both sides.

T10. Tracker: Keitaro campaign gets Facebook traffic; leads arrive via S2S postback, CRM approves sales 3–7 days later. How do you compute CPL/CPA per day so it reconciles with Ads Manager and the CRM? Which date is the cohort key and which attribution window must you pin on the Meta side?

T11. Meta: bulk-launching the same campaign template across 6 ad accounts under one BM with a System User token. Name three things that must differ per account and two things that are account-scoped in the API (cannot be reused across accounts).

T12. Google Ads grey: an account is suspended for "Circumventing systems" after a cloaked landing page. Client wants to open a new account under the same payment profile. Advise, naming the cascade mechanics.
