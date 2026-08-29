# 07 — Review layer, cloaking, creative-classifier tricks

Reviewed 2026-08-27. Session/IP → `01`. Agency/BM → `03`. API launch / re-moderation
→ `04`. Policy taxonomy (clean lane) → `meta-ads/07`. This file is the grey overlay:
how Meta’s review fetch is filtered, and which creative/format tricks still move
the classifier.

Vendor recipes are **vendor-reported**. Policy facts are official. Live Circumventing
Systems page **redirected to Account Integrity** this pass — cloaking is still named
in Meta’s 2026-02-26 lawsuit.

## What Meta named

Live Standards (fetched 2026-08-27):

- “The products and services promoted in an ad **must match those promoted on the
  landing page**.”
- “Helping anyone **evade or circumvent** our enforcement” is prohibited.
- Restriction grounds include **evading review and enforcement**.

2024 Circumventing Systems page (Jon Loomer quote; URL now redirects): advertisers
can’t run ads that purposely avoid review. Named: **cloaking** (limit Meta’s access
to the destination), **unicode/symbols to obfuscate**, **obscure images**. Evading
Enforcement: don’t recreate similar violating ads across assets; don’t create new
assets after restriction.

2026-02-26 newsroom (live): “a webpage connected to a seemingly legitimate ad
displays one version of its content to our ad review system, but shows different
content to real users.” AI cloaking detection; faster reject of **redirect** chains.

**Display URL** must go to the **same domain as Website URL**.
🔺 The widely-repeated "truncated ~25 chars" figure has **no official source** and is probably a
conflation with **Link Description** (30-char cap, ~27 visible, and only on Marketplace / search
results / Audience Network). Measure in preview; do not design to 25. [unverified]
**March 2026:** single-media and Advantage+ catalog collection ads on Facebook Feed
**no longer display a URL in the ad footer** — display-URL mismatch is less visible
in Feed, not less enforced.

**Domain block (Meta-specific, official):** restricted/suspicious landing-page
domain → **all ads** to that domain rejected (“Ads must not promote restricted
domains”). Block **60 days**, then unblock; **repeats** if linked ad accounts keep
violating. Fix: **change domain**, not appeal the domain. Signals include user
feedback and domains tied to disabled ad accounts / payment risk.

## Meta has no AdsBot

Live crawler page (`developers.facebook.com/docs/sharing/webmasters/crawler/`):

| UA | Official job | Ad review? |
|---|---|---|
| `facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)` | OG link-preview (Sharing Debugger) | **Not stated** |
| `meta-externalads/1.1` | “Improving advertising and other business-related products” | Closest named ads crawler. Not labeled “review” |
| `meta-externalagent/1.1` | AI training / indexing | No |
| `meta-externalfetcher/1.1` | User-requested / agentic; **may bypass robots.txt** | No |
| `meta-webindexer/1.1` | Meta AI search | No |

`facebookexternalhit` mechanics (official): gzip+deflate; OG in first **1 MB**;
`Range: bytes=0-524288`; crawl in a few seconds; may bypass robots.txt for
malware/integrity. Simulate:

```
curl -v --compressed -H "Range: bytes=0-524288" -H "Connection: close" \
  -A "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)" "$URL"
```

IPs: `whois -h whois.radb.net -- '-i origin AS32934'` plus AS63293. IPv6
`2a03:2880::/32`. 2026 logs: **57.141.0.0/24** as facebookexternalhit.

**Not on the 2026-08-27 crawler page:** `Facebot`, `FacebookBot`, Instagram crawler,
`facebookcatalog/1.0`. Treat as retired/unlisted, not current review UAs.

WhatsApp preview UA `WhatsApp/2.x.x.x A|I|N` (Android/iOS/web), OG in first 300 KB
— **link-preview, not ad review**.

JS execution by ad review: **not documented**. `facebookexternalhit` is a static
scrape. Vendors assume a second Chrome-class / residential path. Do not bet on
“review cannot run JS.” Do not bet on JS-only cloaks.

## How review is actually layered

1. **Automated pre-serve** on create/edit. Status In review. Typically **24h**, often
   minutes. Official: an ad **may deliver before all policies are checked**.
2. **Destination fetch** of Website URL (and redirect path). Official: review includes
   landing page. No published fetcher-UA for this step.
3. **Re-review at any time**, including after live.
4. **Edits that may re-review (official):** targeting, creative (images/text/links/
   videos), optimisation, billing event.
5. **Field 2026-08 (`04`):** review attaches to the **creative**. Ad-set geo / devices /
   age / placements / budget / bid / schedule did **not** change status in a 45-ad-set
   test. Treat official as what *can* re-trigger; field as what *usually* does.
6. **Click-to-Messenger** has a **thread-level checkpoint on top of ad review**. If
   destination is Messenger/IG/WA, there is no web LP for the primary destination —
   welcome message is reviewed instead. Second gate, not a skip.
7. **Instant Experience** is a Meta-hosted destination. Buttons still have URLs
   (those can be crawled). June 2025: IX **no longer counts as a landing-page view**.
8. **Ads Library** `ad_snapshot_url` is a Meta-hosted **archived creative**, not the
   money page. CTA click from Library is a **normal browser** to advertised URL.

Humans exist (train systems; sometimes review ads). **No official human UA/IP.**
Account-restriction review typically 48h — expectation, not SLA.

## Filter stack for Facebook (layers, in order)

Google’s gclid-always-on does **not** port. FB’s cheap gate is **unsubstituted
macros / missing url_tags**. Build AND. Architecture first: **zero-redirect PHP
white**. JS-only / Tilda-Shopify / IP-only die.

0. **Same-host PHP reverse / local file.** Adspect: safe page **must be displayed
   without redirect** — mandatory for Facebook PHP. 302-the-white is the leak.
1. **Named crawler identity** — UA ∈ facebookexternalhit / meta-externalads /
   (hist.) Facebot **and** IP ∈ AS32934 / AS63293 / 57.141. Serve white **200**.
   Never 403 these.
2. **IPv6 reject** — Keitaro: FB owns huge v6 and uses it for bots. Optional,
   leftover; real users also use v6.
3. **Unsubstituted macros / missing url_tags / missing fbclid** — money AND:
   `{{ad.name}}` (or a dedicated utm) **is not @empty**. Review hits **Website URL**;
   users get the **URL parameters** field + auto `fbclid`. Official conflict:
   macros “replaced when the ad is rendered.” The trick only works if review
   fetches the **declared Website URL** without `url_tags`. Vendor (Binom 2025-05,
   CPA.RIP) still documents it. If Meta fetches the expanded href, this gate dies.
4. **Referrer contains facebook** — Binom money path requires it. Review/share
   crawls often have none.
5. **Language + geo match campaign targeting.** Review language empty/unknown is
   a common white.
6. **First-N clicks white** — Binom `FIRST`. Adspect On Review + “blacklist all
   IPs in Review.” Do **not** click your own On-Review link.
7. **JS / TLS fingerprint** — second stage only. Binom TLS/TCP/VPN **die behind
   Cloudflare**. Adspect **requires** Cloudflare. Pick: CF + PHP, or Binom TLS
   without CF — not both.
8. **Pixel on money:** do **not** fire standard FB JS pixel (Referer leaks money
   URL). Adspect: `<meta name="referrer" content="no-referrer">` or noscript /
   `fetch` with `referrerPolicy: "no-referrer"`.

**Do not enable the cloak on day 0.** Watch the click log (bot flag, geo, UA,
macros present?), then turn filters on.

### Binom UTM split (vendor blog 2025-05, still published)

Website URL = bare tracker: `https://domain.com/click?key=…`

URL parameters field = `ad_id={{ad.id}}&…&utm_code=310306` (Binom recipe 2025-05).
**Keitaro:** do **not** put `fbclid={fbclid}` in URL Parameters — Meta **auto-appends** `fbclid`; a source placeholder **blocks** capture (`docs.keitaro.io` Facebook Conversions, 2026-07).

Stated logic: `utm_code` is attached **after** moderation on the user-visible ad.
Reviewers hit the original URL without tags → white. Money rule requires the UTM.

### Binom Protect Facebook recipe (official)

Default path = white. Money path AND:

1. Referrer **facebook**
2. Language EN (or IS NOT Empty/Unknown)
3. Is **not** Bot (`FB` method = HTTP headers + IP — “recommended by default if
   working with Facebook”)
4. Country = buy geo

Expected: tracker clicks **~2×** FB clicks (FB bots). Offer discrepancy 3–5%.

## Keitaro — Facebook recipe

```text
Forced: Bots IS  → CURL / Show HTML = WHITE (200, same host)
Regular: Country IS {buy geo} AND Bots IS NOT
         AND Parameter {{ad.name}} (or utm) IS NOT @empty
         → money / prelander
Default: WHITE
```

Bot DB is generic, not FB-specific. Update Maintenance → Geo-DBs / Bots. IPv6
reject is the vendor leftover. Watch Click Log before enabling.

## Adspect — Facebook SOP

[docs.adspect.ai, 2026-07]:

1. Use-case = Facebook.
2. Safe page **without redirect** (local file / reverse PHP / No Action).
3. Submit **On Review** + Blacklist All IPs in Review. Not Filtering.
4. After approval → Filtering.
5. Cloudflare yellow-cloud. `.com/.net/.org`. No stop-words in domain.
6. Self-hosted white. Shopify / Wix / Tilda: vendor says networks **pre-ban**
   constructors.
7. White: terms/privacy/cookies, unique, mobile, not a redirect to google.com,
   not a direct affiliate link.
8. Do not alter a live white.
9. One stream per campaign.
10. JS integration = constructor fallback (visitor starts on white; ajax.php
    decides). Weaker. JS-capable reviewer sees money if money is JS-swapped.

## White page Meta actually checks

Official bar is **thin**: ad↔LP product match, working destination, **not a
restricted domain**. No AdsBot-style published checklist.

Vendor FB white = Google-like **real site**: unique, mobile, legal pages,
self-hosted, no constructors, 200, same URL, no redirect. Empty HTML whites pass
`facebookexternalhit` OG and fail a human re-review.

**news-tg display-a-news-domain** conflicts with official same-domain Display URL (tricks table below; Mar 2026 feed-footer removal hides it from users, not from review).

## What actually dies

1. **Content substitution** — Meta’s own 2026 lawsuit definition. Account /
   BM / domain cascade.
2. **JS-primary / Tilda-Shopify white** — constructor pre-ban (Adspect); JS
   reviewer sees money.
3. **IP-only** — misses new ranges (57.141) + any residential reviewer.
4. **302-the-white** — Adspect mandatory no-redirect on FB PHP.
5. **Standard FB pixel on money** — Referer leak.
6. **Restricted domain** — 60-day, all ads, don’t appeal the domain.
7. **Recreating similar violating ads across Pages/BMs** — Evading Enforcement
   (2024 named; live heading gone, enforcement not).
8. **CTM / IX as a cloak** — second gate exists, not a skip (see layered review above)

## Failure signatures

| Signature | What it is | Move |
|---|---|---|
| Ad rejected, account live | Creative / destination | Edit creative, new ad (`04`). Rejected ad cannot enable (2490468) |
| Approved → later reject | Official re-review | Isolate: creative vs domain vs account |
| Ad account restricted | Asset-level | Fresh agency: **replace**, don’t appeal (`01`) |
| User restricted from advertising | Other admins may still run | Freeze the persona |
| BM / portfolio restriction | “Connected abusive assets” | Isolate. Don’t attach clean Pages |
| **Domain restricted 60 days** | Meta-specific | Rotate domain. Do not reuse on next seat |
| Pixel/event domain blocked | Events Manager, separate | New dataset; don’t share across risk tiers (`01`) |
| Page unpublished | Community Standards + ads | New Page, uniquify |
| Tracker clicks ≈ 2× FB clicks | Binom: FB bots on white | Normal. Watch for domain/account wave |
| Instant copy reject | Classifier, not cloak | Image-baked text / new copy. Unicode tricks → this file § below |
| Circumventing / evading | 2024 named; 2026 page moved | Freeze. Replacement is `03`, not a new self-farmed BM |

## Creative-classifier tricks (catalog, language, unicode)

Named Circumventing (live ads-violations UI 2026-08-27; dedicated Transparency
URL 302s to Account Integrity): cloaking · **unicode/symbols to obfuscate** ·
**obscure images** (blur/pixelate/objects) · **emoji as numbers/prices**.
Evading Enforcement: clone violating ads across assets; **new assets after
restriction**.

| Trick | What it actually is | 2026 status |
|---|---|---|
| **DLO Default exotic + Added GEO language** | Default = VI/AZ/KY + Amazon/white URL; Added = ES/PT/ID + grey creative + money URL. Claim: bot scores Default first; users follow UI language | **LIVE, primary format trick** (CPA.RIP 2025-04 → AffTrends 2026-07). Official: DLO **unavailable** for Instant Experience and Messaging Apps — needs **Website** dest. Failure: EN copy in exotic slot; target language common in GEO so white spends |
| Soft-language copy, other GEO, no DLO | PT/ES/ID/TH/RU/AR vs US/EU, hope EN classifier misses | **Degraded.** OCR is multilingual. Official wants creative to match |
| RTL / U+202E bidi override | Reverse displayed text | **Unknown** on Meta ads 2025–26. Treat as named unicode obfuscation |
| Homoglyphs / ZWSP / ZWNJ / BOM | Cyrillic а, Greek ο, U+200B/C/D, U+FEFF | **LIVE vs keyword filters** (Gen Digital Mar 2026 at scale). **DEAD vs CV/OCR** (AffTrends Jul 2026). Named Circumventing |
| Emoji as the claim (💰💊🎰 / 9️⃣9️⃣9️⃣) | Replace prices/banned words | **Named trip**, not a bypass |
| Image-baked headline + **empty** ad-level text | news-tg live Aug 2026 | **LIVE as copy-field skip.** **DEAD as OCR skip** if the baked string is the violating claim. Official: blank text **may be pulled from Website URL**. Advantage+ can **rewrite text baked into the image** (Loomer 2026-07) — OPT_OUT |
| Blur / pixelate / object-cover | Hide slot UI / body | **DEAD** for gambling/nutra icons (AffTrends). Superpower Daily Aug 2026: scenic **video covers** for porn = Meta called **adversarial** |
| **Collection / Advantage+ catalog** | Innocent cover + grey product set; product click → feed `link` unless **Override catalog deep links** | **LIVE as structure.** Cover is **not** the only review object — Commerce Manager rejects products; image fetch = `Meta-ExternalAds`; `link` crawled. Cover-only review is **false** |
| Catalog feed-swap after review | Change images/text/links post-approval | **Circumventing** if destination disguises. High ban on re-crawl |
| Instant Experience as first hop | White IE canvas, CTA to money | **LIVE format.** Button URLs crawled. DLO off. Jun 2025: IE ≠ LPV |
| **Mar 2026 Feed footer URL gone** | Single-media + A+ catalog collection on FB Feed no longer show URL | Display-URL “cnn.com” trust cue **dies on those units**. Dest mismatch less user-visible, still enforced |
| Display URL ≠ Website URL | news-tg: news domain vs tracker | **Official: same domain.** Gen Digital Mar 2026: URL masking **still at scale**. 60-day domain block if it trips |
| CT-Messenger / WhatsApp / IG Direct | No web LP | **LIVE LP-skip.** Greeting + creative still reviewed. DLO off. Partnerkin: language trick **requires Website** dest |
| Instant Forms | No offer LP; privacy-policy URL required (not PDF) | **LIVE LP-skip.** 2026 Leads default = **Website and Instant Forms** — buried Single; accidental website dest turns LP review back on |
| Carousel: grey card 1 + white 2–n | Disable card optimization | **LIVE** (AffTrends / vc.ru). Per-card review |
| Placement mix: grey Feed/IG, white Messenger/Search | Dilute | **Dying** — Aug 2026 placement-control removal (Loomer) |
| Split claim across headline + description | Neither string trips | **Degraded.** Advantage+ can swap headline ↔ primary. Description not shown on most Feed/IG |
| Video: no captions / first 3s clean / white thumbnail | Skip ASR / OCR | **No-captions ≠ no ASR** (review includes **audio**). First-3s is a **view metric**, not a review window. White thumbnail **LIVE/degraded** |
| SAC undeclared | Avoid Financial targeting tax | **KILL.** Official: ads may be rejected if category not chosen (US Financial 2025-01-14). Practitioner *workaround* is **declare Financial**, not hide it |
| Dark posts / multi-Page clone | Hide from Ad Library / reset | Dark posts **still in Ad Library** when active. Multi-Page clone = **named Evading** |
| PostID reuse of an approved post | Port a cleared creative | **Evading** if the post is the same violation |
| Advantage+ gen-bg / expand / text gen | Camouflage | **Trip, not camouflage.** Crop disclaimers, invent claims. Grey default = OPT_OUT (`04`) |
| Page name / IG bio as the pitch | Ad is clean | **Unknown / weak.** No 2025–26 sourced playbook |

**Replacement stack if unicode/blur died:** UGC lifestyle (no slot UI, no
before/after) + DLO language layers + empty ad-level copy + image-baked
*non-keyword* headline + CTWA/forms if the funnel allows + Collection/IE as first hop. SAC: declare if
finance-shaped. Cloak stack (PHP white) is still required for a grey web dest —
format tricks are the **classifier** layer, not a substitute.

### Catalog-camouflage ops (vendor-reported, Rentacc 2025-05)

Why catalogs work as camouflage: budget spread across many product cards "blurs"
the arbitrage footprint vs a mono-creative with one landing link. Mechanics:
update the feed daily and cut stale cards · segment offers via product sets ·
track per-card ROAS through `content_id` and kill losers individually · Events
catalogs carry sweepstake-style offers. Constraint from the tricks table above
stands: Commerce Manager rejects products independently — cover-pass ≠ feed-pass,
and post-approval feed swaps that disguise the destination are Circumventing.

## Delivery-cloaking: steering Andromeda (not the review)

Different goal from everything above: bot-differentiated content to manipulate
**targeting**, not to pass review. The product still matches — this is not the
named substitution pattern — but it IS bot-vs-user differentiation; treat as
risk-bearing. [practitioner case, n=1, Partnerkin 2026-01, white e-com US, +30%
ROI — mechanism unverified]:

- Serve Meta's crawler/indexer UAs (§ "Meta has no AdsBot") content structured
  for a different audience/expansion signal than users see → delivery explores
  audiences the user lander never attracted. Readout is **frequency at scale**,
  not CTR.
- Adjacent levers from the same case: lander rotation via external tracker +
  CAPI loop (7 variants as an audience-expansion lever, orders passed API→shop);
  sweeps-style native post without the CTA button, link in the first pinned
  comment (~10× organic reach claim); seeded comment threads →
  `senior-buyer-ops/02`.
- Discipline: attribute with `06`'s balanced designs — one axis at a time, or
  the read is fiction.

## Identity / selfie / BM verification (Meta)

Three+ **separate** gates. Buying “verified” clears one of them.

| Gate | What it is | Grey note |
|---|---|---|
| Business Suite verification | Legal entity. 5 docs: COI; registration/license; **gov-issued** tax (self-filed refused); bank statement; utility **only for address/phone — cannot prove legal name**. Up to 14 business days. HTTPS site | Monthly invoicing: Meta may not need docs for this flow |
| Ads-transparency advertiser/payer (Mar 2026: “advertiser” replaces “beneficiary”) | Org: registry match or upload. Person: **gov ID**. Advertiser and payer **can differ** | Grant the person access or they verify from an account they already have |
| Payment-method hold | Card: temporary authorization, 🔺 exact amount **[unverified]**. Bank: Meta deposits **$0.01–$0.99**, re-enter exactly, **max 3 attempts** [official 260929950658464]. Full table → `09` | Not last-4 of PAN. Separate from ID |
| Commerce Manager KYC | Checkout shops. Address last 12 months, **no P.O. box**. Beneficial owner = **≥10% of shares** [official 193400874040813] — there is **no** "$50k lifetime Shops revenue" trigger; two verification passes found no Meta page stating one. Docs per owner → `09` | Extra vs catalog-ads-only (domain + Commerce catalog still required) |
| Facebook Verified (Jul 2026) | Free selfie vs **profile photos**. Dating/Marketplace/Groups badge | **Not** an ads gate |

**Market (2026, vendor prices, volatile):** verified BM ~$50–$350; aged profiles
sold with “matching identity documents.” What still links after you buy: **user
ID / cookies-tokens, phone/2FA, the verification ID, the card.** A verified BM
does not clear personal ID, 2FA, or payment.

**Liveness:** presentation attacks (print, screen replay, 2D mask) are **mostly
dead** against certified PAD. Injection (virtual camera / Android camera hook)
is the live industry class — **no 2025–26 source shows a confirmed Meta ads
selfie pass via deepfake/injection.** Grey inventory is **already-verified
assets**, not a liveness exploit.

Same nominee on Google + Meta + bank: **intra-platform** cascade is real.
Cross-platform sharing of the selfie video is **undocumented**. Shared phone /
legal name / address / card is the practical radius.

## Gaps

- No official UA for **ad review** as distinct from sharing / ads-product crawl.
- No official JS-execution or residential-reviewer spec.
- Live Circumventing Systems text not retrievable (redirect).
- Macro/`url_tags` split: vendor yes (2025-05); official “when rendered” argues
  against. Unverified 2026.
- HideClick / Cloaking Master: no public FB field-level SOP.
- BHW / afflift: HTTP 403 this pass.
- Whether DLO Default is what the pre-moderation bot actually scores first: universal
  practitioner claim, no Meta confirmation.
- Catalog ads-only (no Shop): exact HTML policy crawl of every `link` vs cover —
  image crawler confirmed; full page crawl not in one Help sentence.
- Page name / IG bio as sole pitch: no sourced 2025–26 playbook.
- RTL/U+202E on Meta ads: not found.
