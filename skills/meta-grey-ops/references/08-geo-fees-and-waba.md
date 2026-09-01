# 08 — Geo fees, account locks, WABA

Reviewed 2026-08-27. Session/IP → `01`. Agency billing → `03`. CTM/CTWA as LP-skip → `07`.
Google geo/OFAC → `google-grey-ops/07`. Meta-only facts below.

## Location fees (DST pass-through)

Official [facebook.com/business/help/1238737454289085]:

- Fee is on **impressions in the jurisdiction**, **not** business location.
- **Added on top of delivery.** Example: $100 Italy + 3% = **$103**. Not taken from campaign budget.
- Invoice line by country.
- Live rates: **Austria 5% · France 3% · Italy 3% · Spain 3% · Türkiye 5% · United Kingdom 2%.** List can change.
- Agency tenant: the billed party pays. Fold into break-even (`03`); Ads Manager CPL **excludes** this line.

Three different money lines — do not collapse them: **location fee (DST)** · **VAT/tax** (billed-party jurisdiction) · **agency markup** (reseller). Only the first is this Help page.

Secondary (Adsuploader 2026-08 citing Meta FAQ): WhatsApp marketing messages **invoiced with ads** also pick up the fee in those six markets. Re-check the help page before treating WA Cloud API as exempt.

## Timezone / currency / country lock

Official timezone [754049591334898]: changing timezone **closes the existing ad account**; ads stop; **cannot reactivate**; a **new** ad account is created. Default for new accounts: **PST**.

Official currency [291404291014138]: you can change currency **once every 60 days if you don’t have a current balance**. Choosing a new currency/timezone **creates a new ad account**; old one stays visible but **closed**. **Monthly invoicing: cannot change currency** after creation.

Same page: for **Brazil, India, Poland**, business country and currency **must match**. Select a country other than Brazil at create → **cannot change to Brazil later**. Same for BRL.

**RULE — account timezone = target-geo timezone, set at creation, always.** Default for a new account is PST — if you skip the dropdown, your budget day resets at PT midnight = mid-morning in most target geos (TR: 10:00), starving the evening peak and front-loading dead hours. Consequences of a mismatched tz: daily_budget/day-parting/insights date boundaries all follow ACCOUNT tz, not geo — daily-spend reporting doesn't align with local calendar, and delayed-start launches planned by geo hours (04) fire at the wrong time. Tracker joins must match too (timezone discipline, tracker-ops). Field example: tr-1 account created with `timezone_id: 134` (Europe/Istanbul) for TR traffic — verify at setup with `GET /{act_id}?fields=timezone_name,currency`.

Grey: a “settings fix” is a **new act ID**. Pixel/page shares do not follow automatically (`03`).

## Sanctioned targeting (not Google’s OFAC list)

Official location targeting [365561350785642]: **cannot target** Cuba, Iran, North Korea, **Russia (country)**, **Sudan**, Crimea, Donetsk, Luhansk, Sevastopol.

Google’s 6163740 does **not** list Russia or Sudan as OFAC. Meta lists them as untargetable. Do not copy Google’s RU-pause framing onto Meta.

Country-group pages (Europe / CISFTA [1155157871341714]) still **name** Russian Federation. That is group membership, not a serve grant. Worldwide / Europe as a pill does not override the sanctioned-locations note.

## WABA quality ≠ ad-account health

Official [896873687365001] — WhatsApp **Business Platform** (Cloud API), not the consumer WhatsApp app:

- **Two scores:** phone number (7d, Green/Yellow/Red) and **template** (GREEN/YELLOW/RED/UNKNOWN). Template Flagged → 7d to recover or **Disabled**.
- Phone rating from **blocks, reports, mutes** (reasons: no longer needed / didn’t sign up / spam / offensive / no reason). Recency-weighted.
- **Flagged/Restricted phone statuses discontinued 2025-10-07.** Messaging limits are **portfolio-wide** from that date (start 250 unique users outside the 24h window).
- Cloud API **24h customer-service window**: free-form only while open; after close, **templates only** (error 131047). That is **API**, not an ads-review skip.
- WA Commerce Policy bans gambling, dating, adult, drugs, supplements, crypto-as-currency **in the thread**. CTWA dest is still WhatsApp.
- **WABA ban does not officially cascade to the Ads CID** (and reverse). Shared **BM** can still cut `whatsapp_business_management`. Replace the **number**, not the ad account, for a red WABA.

CTWA: **thread-level checkpoint + ad review**. `page_welcome_message` / prefill is a **creative field** (default “Hello! Can I get more info on this?”). A green WABA does not pass a violating greeting.

## Cannabis / CBD (Meta)

Official Transparency Center + Help [5356017181162381]:

- **THC / psychoactive cannabis: no ads.**
- **CBD / similar cannabinoids:** **US only**, 18+, LegitScript + **written authorization**, THC **not >0.3%**, **no disease claims**. Official Standards **do not** split ingestible vs topical (unlike Google). Help still says LegitScript certifies **non-ingestible**. Domain cannot also sell prohibited products.
- **Hemp with no CBD and ≤0.3% THC** (seed, fiber): US, Canada, Mexico; **no** written auth.
- No disease-treatment claims.

THC remains **no path**. Do not copy Google’s topical-only rule onto Meta as official.

## Adult

Ads nudity policy is **stricter than Community Standards** (no overlay-covered nudity). Dating: written permission, 18+; no paid dating, affairs, sexually suggestive emphasis.
