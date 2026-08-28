# Meta Business Portfolio (formerly Business Manager) — Setup & Navigation, 2025–2026

Scope: creating/verifying a Business Portfolio, attaching ad accounts/Pages/Instagram, roles, payments, security, restriction diagnosis. UI reviewed **2026-07-24**, varies by rollout; "Business Manager" in older sources = same surface.

---

## 1. Concepts: Business Portfolio vs Personal Account vs Business Suite

### Personal Facebook profile
- Required to create a Portfolio (real login for accountability).
- Creation limit: **2 portfolios per profile** (practitioner-reported). Meta Support confirmed (tested profile): **lifetime quota**, not reset by leaving/deleting. No public limit table found — account-specific, not platform contract. Membership in others' portfolios doesn't count.
- Profile-level Community Standards restriction can block asset creation — check **Facebook Account Status**, not just ad-account status.
- Every profile auto-gets a **personal ad account** (created on first boosted post). Running business ads from it instead of a portfolio-owned account is a classic beginner mistake — assets end up owned by the individual.

### Meta Business Portfolio (formerly Meta Business Manager)
- **Ownership layer**: holds Pages, IG accounts, ad accounts, datasets/Pixels, catalogs, apps, WhatsApp accounts, domains; controls access (people/partners/system users), billing, security.
- **Renamed 2024**. Old `business.facebook.com` links redirect; some help text still says "Business Manager" — synonym.
- **Assets belong to the Portfolio, not a person's profile** — survives staff/agency turnover.
- 2025 rollout: **managed Meta accounts** — company-managed, email-based logins not tied to a personal profile [uncertain: rollout/region vary].

### Meta Business Suite
- Day-to-day workspace: publishing/scheduling, unified inbox (Messenger/IG DMs/WhatsApp/comments), insights, simple ad creation. Has a mobile app; Portfolio doesn't.
- Suite = operating workspace; Portfolio = ownership/access container; increasingly cross-linked.
- Switch: Suite → Help (bottom-left) → "Go to Business Manager" → Portfolio; Portfolio → hamburger (top-left) → "Meta Business Suite" → back.

### Ads Manager
Campaign tool. Ad account can exist without a Portfolio; once claimed by one, access/billing/partner permissions move to Portfolio level.

### When a Business Portfolio is required
Business Suite; business-owned ad accounts; Shops; domain verification; monthly invoicing; social-issues/elections/politics ads (extra verification); agencies/partners; multiple Pages/ad accounts.

---

## 2. Creating a Business Portfolio

Click-path:
1. Log in to personal Facebook profile.
2. `business.facebook.com/overview` → **Create an account**.
3. Enter **Business name**, **your name**, **business email** → **Submit**.
4. **Verify business email** via confirmation email (check spam — unverified email blocks later steps).

Best practices:
- Use the personal-account email or a monitored business inbox (update stale email first).
- Consistent, real naming across Portfolio/Page/IG — mismatches complicate verification/linking.
- Authentic, compliant profile only — fake/disposable = access and enforcement risk.
- Avoid single-person recovery dependency: second trusted, separately-secured full-control owner; everyone else least-privilege (more full-control users = more continuity, more takeover risk).
- Fill **Business Portfolio info** (legal details, primary Page) immediately — incomplete info is a common verification/restriction trigger.

### Creation-limit recovery: access ≠ quota
- `Leave` removes access, not the portfolio; doesn't free quota. Removing a Page/IG asset doesn't affect quota either.
- Tested-profile support reply: leaving **or deleting** does not restore the lifetime quota; can't be increased. No 24/48h reset.
- The live creation error suggested deleting an existing portfolio — conflicts with that reply. Preserve both; escalate manually, don't generalize.
- If limit persists: preserve Page/IG; ask support to delete the inaccessible portfolio or review the profile restriction. If no recovery, an authorized colleague creates the company portfolio (confirm they can accept/use access before migrating assets).
- Deletion can be blocked by System Users, Pixels/datasets, or a problem ad account. Never use bought/shared/fabricated profiles as a workaround.

---

## 3. Business Verification

### What it is
Confirms real legal entity behind the portfolio. **Not mandatory for basic advertising**, but required/recommended for: WhatsApp Business API (approval, higher limits); certain API/app features; stronger ownership evidence in support/review; some advanced features (sharing/partner, politics/social-issues ads).
- Gotcha: **"Start verification" in Security Center is often greyed out** until a verification-requiring feature is attempted (e.g. adding an app/WhatsApp number) — trigger the feature first [uncertain: exact trigger list].

### Click-path
`Business Settings → Security Center → Business Verification → Start verification → Get started` → country where business is headquartered → legal business details → select/confirm business (Meta matches public records) → upload documents if unmatched → confirm phone/email via code.

### Documents
- Must show **legal business name + address and/or phone**, match portfolio info **exactly**, supported language; utility-bill-type docs generally **≤~1 year old**.
- Accepted: certificate of formation/incorporation, articles of incorporation, business license/permits, tax registration, business bank statements, utility bills, business credit reports, shop establishment certificates, country-specific registrations (Udyam/India, PAN card).
- **Not accepted**: invoices, purchase orders, self-filed tax returns, personal bank statements, website printouts, self-created marketing docs (letterheads, flyers).
- Phone number can be verified via a second document if the main one lacks it.

### Timeline and status
**~48 hours** (Superchat, 2026) up to **30 days** (Klaviyo, 2026), queue/quality-dependent. Status in **Security Center**: *In review* / *Verified* / rejected-with-reason.
Common rejections: name/address mismatch, expired/self-created docs, unsupported language, blurry scans.

---

## 4. Ad Accounts: Adding, Creating, and Limits

### Click-path
`business.facebook.com/settings → Accounts → Ad accounts → + Add`:
- **Add an ad account** (claim one you own/admin)
- **Request access to an ad account** (client accounts — correct agency workflow)
- **Create a new ad account** → name, time zone, currency → assign people

Gotchas:
- **Currency and time zone are permanent** — mistake = new ad account.
- Ad account belongs to **one** Portfolio only. "Add" fails if another portfolio owns it → use "Request access."
- Closing/deactivating stops ads/publishing, distinct from policy-disabled. Voluntarily closed accounts normally reactivate via Ads Manager once billing is resolved — check account state before creating a replacement. (Official: https://www.facebook.com/help/messenger-app/331993756945799/)

### Ad Account Creation Limit
- New portfolios start at **1 ad account**; grows with spend history, on-time payments, policy compliance (Jon Loomer; reconfirmed Graphed 2025).
- Check: `Business Settings → Business portfolio info` → **Ad account creation limit** [uncertain: label may sit under Business info].
- Raise faster: build spend/payment history or work with a Meta account rep.

---

## 5. Connecting Facebook Pages and Instagram Professional Accounts

### Prerequisites for Instagram
- Use an Instagram **professional account** (Business or Creator — commerce/partner/messaging/publishing features vary by type/region). Prefer Business for companies, or if an integration excludes Creator.
- IG should be **linked to the Facebook Page** (Page → Settings → Linked accounts → Instagram, or **Accounts Center**) — powers cross-posting, unified inbox, IG placement identity in ads.

### Add a Facebook Page
`Business Settings → Accounts → Pages → + Add → Add a Page` → search by name/URL → appears instantly if you have required access.
- Only **full control / ownership-level** Page access can add it; if claimed by another Portfolio, "Add" fails — **request access** or have it transferred.
- Page access splits into **Facebook access** (full control or partial: content/messages/ads/insights) and **task access** (granular) — task-access-only people may not be able to move a Page into a portfolio.
- Alternative: `+ Add → Request access to a Page` (agency) → **Partial access** or **Full control** → Page admin approves.
- Set **Primary Page** in Business portfolio info — used for business identity across Meta.

### Add an Instagram account
`Business Settings → Accounts → Instagram accounts → + Add` → log in with IG professional-account credentials → grant permissions.
- IG must not already be connected to a *different* Portfolio — disconnect there first.
- **Assign people** to the IG asset after adding — adding someone to the portfolio does NOT auto-grant asset access (most common setup mistake).
- Verify FB↔IG link in **Accounts Center → Sharing & logging in**; if Page isn't listed, connection is incomplete and IG won't appear as an identity option in Ads Manager.
- Troubleshoot in order: professional-account status → Business vs Creator eligibility → Page/portfolio ownership → operator permissions → existing connections → stale login sessions. Creator status alone is rarely the cause.

---

## 6. People, Roles, and Partners

### People (Users → People)
- Add by the **email tied to their Facebook profile**; they appear "Pending" until accepted; invites expire and may need resending.
- Roles (2024+ naming):
  - **Full control** (was "admin access") — manage settings/people/tools/all assets; can delete the portfolio. Max 2–3 trusted owners.
  - **Partial access** (was "employee access") — assigned assets/tools only.
  - **Advanced**: **Finance** permissions (billing/invoices/credit lines without full control); **temporary access** (time-limited, auto-revoked).
- Two-layered access: **portfolio-level** (settings/people) + **asset-level** (per Page/ad account/dataset, task toggles like "create ads", "view performance"). Adding a person ≠ assigning assets.
- Page-level roles via portfolio: Page advertiser/analyst/editor; ad-account-level: admin/advertiser/analyst. Grant minimum needed (advertiser+analyst covers most agency work).

### Partners (Users → Partners)
- Correct agency model: client **keeps ownership**; agency gets access via its own Portfolio.
- `Business Settings → Users → Partners → Add → Give a partner access to your assets` → paste agency's **Business ID** (from their own Business portfolio info) → select assets/permission levels → confirm.
- Reverse: `Ask a partner to share their assets` → receive their assets.
- If agency does initial setup, document ownership/recovery/transfer explicitly.
- Remove: `Users → Partners → select → Remove` — instant, no data loss, assets stay with owner.

### System users (Users → System users)
- Server-to-server identities for API/tokens (not people); relevant for Conversions API, app integrations.
- Assign the app and each required ad account/Page/IG/dataset/catalog to the System User before generating its token. Token scopes and business-asset tasks are separate layers.
- A successful asset-list `GET` doesn't prove campaign-write/advertising identity access. Run a zero-spend `PAUSED` write + Page/IG creative probe before full campaign build. See `13-api-access-billing-launch-operations.md`.

---

## 7. Payment Methods and Spending Limits

### Adding a payment method
- Portfolio level: `Business Settings → Billing & payments` — balances, activity, credit lines, all connected accounts' payment status.
- Ad account level: `Ads Manager → ☰ All tools → Billing & payments → Payment settings → Add payment method`.
- Varies by country: cards most common; PayPal/direct debit in some markets; **manual payments** (prepay) in certain countries; **monthly invoicing/credit lines** only via application for qualifying spenders.
- Automatic payments charge at a billing threshold and bill date. Failures can stop delivery or trigger verification; no universal rule flags every prepaid/virtual card.
- Keep a **backup payment method** — one declined charge can pause delivery and flag the account.
- Diagnose separately: failed transaction, amount due, verified/default card, payment-method eligibility, account restriction. Zero balance + verified card alone doesn't restore an account.
- Card entry, hold codes, 3DS, verification: only in Meta's trusted UI — never transmit card data/verification codes via chat or API tooling.

### Spending limits (distinct concepts)
- **Account spending limit**: hard cap on lifetime ad-account spend. At cap, **all campaigns stop delivering but still show active** (Jon Loomer) — classic "ads stopped" mystery. Manage: `Ads Manager → Billing & payments → Payment settings → Account spending limit` (Set/Change/Remove/Reset via `…`). Reset continues spend under same cap.
- **Daily spending limit**: Meta-imposed, dynamic, grows with history — not manually settable.
- **Campaign spending limit**: optional per-campaign cap.
- Instagram-side: same account limits apply; "Instagram ad spending limit" in the IG promotion flow = same account spending limit.

---

## 8. Two-Factor Authentication and Security Settings

### 2FA requirement (portfolio-wide)
- `Meta Business Suite → Settings → Business portfolio info → Business options → Two-factor authentication` → **Admins only** / **Everyone** / **No one**. Only **full control** can change this.
- Meta allows new portfolios to require 2FA, and requires it for **certain** portfolios older than **90 days** (not documented as universal) — require it for everyone with asset access regardless. (Mirror of Meta Help article: https://support.chatarchitect.com/books/meta-business-portfolio-setup/page/turn-on-the-two-factor-authentication-requirement-in-your-business-portfolio)
- Side effects: people without personal 2FA lose access until enabled; cookie-clearing browsers demand a code every login; third-party tools require a login code next sign-in.
- Individuals enable via Facebook `Accounts Center → Password and security → Two-factor authentication` (authenticator app preferred over SMS).

### Other security surfaces
- **Security Center**: verification status, 2FA requirement, alerts, recent activity.
- **Account quality**: restriction status for portfolio, ad accounts, linked profiles; appeal entry (`View details` → request review).
- Hygiene: remove ex-employees/agencies immediately; audit `Users → People`/`Partners` quarterly; never share logins; watch for phishing impersonating "Meta Business Support" (leading cause of portfolio takeover → ad-account bans).

---

## 9. Business Settings Panel Structure (what lives where)

Entry: `business.facebook.com/settings` (Business Suite → Settings redirects here). Left panel (ordering/labels vary by rollout):

- **Users**: People · Partners · System users.
- **Accounts**: Pages · Ad accounts · Business asset groups · Apps · Instagram accounts · WhatsApp accounts · Commerce accounts.
- **Data sources**: Catalogs · Datasets · Meta Pixels · Custom conversions · Audiences. Dataset groups events across website/app/offline; Pixel remains the web source, may share its ID with the dataset. (Official: https://www.facebook.com/help/messenger-app/952192354843755)
- **Brand safety and suitability**: Domains (verification) · Block lists.
- **Security center**: verification, 2FA requirement, alerts.
- **Business portfolio info**: business details, primary Page, **ad account creation limit**, business options (2FA), **permanently delete business**.
- **Billing & payments**: balances, payment methods, invoices, credit lines, connected accounts.
- **Account quality / Business Support Home**: restrictions/appeals (`business.facebook.com/business-support-home`).
- Suite's settings gear redirects here — no separate "Suite settings."

Legacy mapping: "Business Manager" = Business Portfolio; "Admin access" = Full control; "Employee access" = Partial access; "Business Settings → Business Info" = Business portfolio info. Do NOT map "Pixels" directly to "Datasets" — Pixel is a web data source; datasets can group its events.

---

## 10. Setup failures and restriction diagnosis

### Restrictions: levels and mechanics
- Can affect a person, Page, ad account, portfolio, payment method, or single ad. Check the exact affected asset/reason, don't assume portfolio-wide ban.
- First stop: **Account quality / Business Support Home** + Delivery/status details in Ads Manager. Provide only the evidence requested for that case.

### Common setup and access failures
1. **Inauthentic/shared profiles** — violate identity rules, unreliable recovery.
2. **Missing requested verification or 2FA** blocks workflows requiring them — not a universal restriction cause absent the displayed reason.
3. **Payment problems**: declines, insufficient funds, unsupported methods, inconsistent billing, unpaid balances. Resolve the exact message; don't blanket-reject prepaid/virtual cards.
4. **Compromised credentials/unusual access** trigger security checks — respond to the actual checkpoint, no generic "warm-up."
5. **Asset ownership disputes**: Page/data source owned by ex-employee/agency, claimed by another portfolio, duplicate setups. Verify recovery window before deleting anything.
6. **Shared logins / broad full control** — one compromised admin takes down the whole portfolio; use partner/partial access instead.
7. **Wrong IG linkage/permissions**: connected elsewhere, insufficient access, unsupported account type.
8. **Incomplete business contact details** can block verification/recovery comms — no evidence of a hidden "trust score" penalty.
9. **Unmanaged account spending limit** — mimics a restriction: ads stop at cap while showing "active."
10. **Running ads before the foundation is clean** (unclaimed Page, personal ad account, no Pixel/dataset ownership) — complicates migration, can strand data with the asset owner.

### Structural practices for continuity
- One portfolio per legal entity; business owns all assets; agencies get **partner** access only.
- 2+ full-control admins, everyone else partial/temporary; quarterly access audits.
- Verification + 2FA from day one; real, matching business details everywhere.
- Keep payment methods healthy + backup where supported. Budgets from economics/risk, not account-aging ritual.

---

## Sources

1. https://www.leadsie.com/blog/meta-business-manager-vs-meta-business-suite-differences — Business Suite vs Business Portfolio roles, 2024 rename, access model, managed Meta accounts (practitioner; accessed 2026-07-22)
2. https://badrhinoinc.com/blog/meta-business-suite-vs-business-portfolio/ — Portfolio vs Suite framing, common ownership mistakes (practitioner; accessed 2026-07-22)
3. https://graphed.com/blog/how-many-meta-business-accounts-can-i-have — 2 portfolios per profile, ad account limit growth, Business Info → Ad Account Creation Limit, delete business path (practitioner, 2025-12; accessed 2026-07-22)
4. https://www.jonloomer.com/glossary/ad-account-creation-limit/ — ad account creation limit starts at 1, grows with spend/payment history (practitioner, 2023 — older date, terminology still current; accessed 2026-07-22)
5. https://www.jonloomer.com/campaign-spending-limits-account-spending-limits-daily-spending-limits/ — account vs campaign vs daily spending limits; ads stop but show active at cap (practitioner, 2023 — mechanics unchanged in 2025 sources; accessed 2026-07-22)
6. https://help.klaviyo.com/hc/en-us/articles/40116148219163 — business verification click-path (Security Center → Start verification), accepted/rejected documents, up to 30 days (official-adjacent partner doc, 2026-03; accessed 2026-07-22)
7. https://help.superchat.com/en/articles/14982-how-to-submit-a-meta-business-account-verification — verification documents must show name/address/phone, ≤1 year old, ~48h review (partner doc, 2026-07; accessed 2026-07-22)
8. https://support.chatarchitect.com/books/meta-business-portfolio-setup/page/turn-on-the-two-factor-authentication-requirement-in-your-business-portfolio — partner reproduction of 2FA settings and Meta language applying a requirement to certain portfolios older than 90 days; not evidence that all such portfolios share one mandate (accessed 2026-07-22)
9. https://support.properti.ai/how-to-create-a-facebook-business-page-instagram-business-account-connect-them-to-your-meta-business-portfolio — exact steps for adding Pages and IG accounts in Business Settings, ownership rules, IG Business-account requirement, Accounts Center verification, troubleshooting (practitioner; accessed 2026-07-22). References official Meta help URLs: facebook.com/business/help/1710077379203657 (create portfolio), /898752960195806 (connect IG), /104002523024878 (create Page), /187316341316631 (Page roles), help.instagram.com/502981923235522 (professional account) — (official, cited but not directly fetchable)
10. https://tj21.com/how-to-share-partner-access-with-an-agency-in-metas-business-portfolio-without-losing-control-of-your-assets/ — partner access via Business ID, asset-level permission guidance, removal flow, ownership-transfer risks (practitioner, 2025-12; accessed 2026-07-22)
11. https://socialschool4edu.com/a-comprehensive-guide-to-meta-business-portfolio/ — real-world setup walkthrough: checking existing portfolio ownership via Page Roles/Business ID, two-admin rule, People/Pages verification, Meta support recovery process with notarized letter (practitioner, 2025-01; accessed 2026-07-22)
12. https://www.superads.ai/blog/fix-facebook-ads-account-restricted — restriction levels (personal/portfolio/ad account), causes (policy, suspicious activity, authenticity), Account Quality / Business Support Home appeal path (practitioner, 2025-09; accessed 2026-07-22)
13. https://favfly.com/post/meta-ads-account-disabled — appeal evidence and prevention: clean payment methods, no budget spikes, no random-device logins (practitioner, 2025-04; accessed 2026-07-22)
16. https://graphed.com/blog/how-to-change-facebook-ad-billing-threshold — billing threshold management path: Ads Manager → All tools → Billing (practitioner, 2025-12; accessed 2026-07-22)
17. https://www.leadsie.com/blog/request-access-to-facebook-page — request Page access flow with Partial access vs Full control (practitioner, 2026-06; accessed 2026-07-22)
18. https://www.facebookblueprint.com/student/path/219702-business-portfolio-course — Meta Blueprint "Setting up a business portfolio" course, confirms current official terminology (official; accessed 2026-07-22)
19. Live Meta Business Suite / Business Settings observation — leaving a third-party portfolio and an owned portfolio removed access, but a subsequent creation submission still returned the portfolio-limit error; deletion was blocked by System Users, Pixel/dataset, and an ad account with issues (official live product, account-specific; observed 2026-07-24)
20. https://www.facebook.com/help/messenger-app/195296697183682/ — Meta warns against sharing Facebook accounts or creating inauthentic profiles; use assigned access instead (official; accessed 2026-07-24)
21. Meta Support response for the tested profile — reported an active Community Standards restriction; stated a lifetime two-created-portfolio quota, no reset after leaving/deletion, no support increase, and recommended creation by a trusted colleague (official account-specific; received 2026-07-24; not a public universal policy)
22. https://www.facebook.com/help/1392616391875085/ — Account Status shows profile/Page restrictions and unavailable features (official; accessed 2026-07-24)
23. https://www.facebook.com/business/ads/review-policy-guidelines — restrictions can affect user, Page, ad account, or business; Business Support Home is the review surface (official; accessed 2026-07-24)

## Gaps

- **Official Meta Help Center pages could not be fetched directly** (facebook.com/business/help returns errors to non-authenticated fetches). Official click-paths above are corroborated by partner docs that reproduce Meta's help text (e.g., chatarchitect for 2FA) and by multiple practitioner sources, but label wording should be re-verified in a live UI.
- **Ad account creation limit scale**: sources agree it starts at 1 and grows, but Meta publishes no fixed tier table; exact increments unverified.
- **Billing threshold starting amounts and increments** by country/currency: not verifiable from public sources; marked [uncertain].
- **Business Portfolio creation limit and reset timing**: a profile-specific
  limit is confirmed by the live Meta creation error. Support stated that this
  profile has a lifetime two-created-portfolio maximum that leaving/deletion
  cannot reset. No matching public Meta policy page was found, and the creation
  UI itself suggested deletion, so preserve this as account-specific official
  guidance rather than a universal contract.
- **Managed Meta accounts rollout**: announced/rolling out per practitioner sources; availability, eligibility, and setup flow for 2026 not verified from official docs.
- **"Start verification" greyed-out behavior**: widely reported (button activates only when a feature requires verification) but not documented officially; trigger list unverified.
- **Business Settings left-panel exact menu ordering/labels in mid-2026**: reconstructed from multiple sources; Meta A/B-tests this UI, so section ordering and minor labels vary.
- **Documents age limit (~1 year)** for verification: from partner docs; Meta's official wording on document recency not directly verified.
