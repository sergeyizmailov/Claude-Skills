# Meta Business Portfolio (formerly Business Manager) — Setup & Navigation, 2025–2026

Scope: what the Business Portfolio is, how to create and verify it, how to attach ad accounts / Pages / Instagram accounts, people & partner roles, payments, security, and how accounts get restricted at this stage. UI labels were reviewed **2026-07-24** and vary by account rollout; older sources that say "Business Manager" usually refer to the same ownership surface.

---

## 1. Concepts: Business Portfolio vs Personal Account vs Business Suite

### Personal Facebook profile
- The top-level login for everything Meta. A personal profile is **required** to create a Business Portfolio — Meta requires a real personal login to establish ownership and accountability.
- A profile-specific Business Portfolio creation limit exists. A maximum of
  **2 created portfolios** is consistently practitioner-reported. For the
  tested profile, Meta Support stated this is a lifetime quota that does not
  reset after leaving or deletion. No universal public Meta limit table was
  found, so preserve this as official account-specific guidance rather than a
  platform contract. Membership in portfolios created by others is separate.
- A profile-level Community Standards restriction can remove specific Facebook
  features and may block creation of business assets. Check **Facebook Account
  Status** as well as Business Support Home; ad-account status alone is not
  enough.
- Every personal profile also has its own **personal ad account** (created automatically when you first boost a post). Running business ads from a personal ad account instead of a portfolio-owned one is a classic beginner mistake — assets end up owned by the individual, not the business.

### Meta Business Portfolio (formerly Meta Business Manager)
- The **organizational container / ownership layer**: it holds the business's assets (Facebook Pages, Instagram accounts, ad accounts, datasets/Pixels, catalogs, apps, WhatsApp accounts, domains) and controls **who has access** (people, partners, system users) plus billing and security settings.
- **Renamed 2024**: Meta Business Manager → Meta Business Portfolio. Old `business.facebook.com` / Business Manager links redirect to the new interface, but some buttons and Meta help articles still say "Business Manager" (e.g., the "Go to Business Manager" link inside Business Suite). Treat the terms as synonyms.
- Key principle: **assets should be owned by the Business Portfolio, not by a person's profile**. This is what makes employee/agency changes survivable.
- New in 2025 rollout: **managed Meta accounts** — company-managed work identities (email-based logins not tied to a personal Facebook profile) that Meta is gradually introducing for larger organizations [uncertain: rollout status and availability vary by region/account].

### Meta Business Suite
- The **day-to-day workspace**: publishing/scheduling posts, stories, reels; unified inbox (Messenger, Instagram DMs, WhatsApp, comments); insights; simple ad creation/boosting. It has a mobile app; Business Portfolio does not (Portfolio settings are reachable through the Suite app).
- Relationship: Business Portfolio is the ownership/access container; Business Suite is the operating workspace for content, messages, insights, and lightweight ads. Meta increasingly surfaces portfolio settings from Business Suite, but account history and rollout can make the boundary look different.
- Switching between them (current UI quirk): Business Suite → "Help" (bottom-left) → "Go to Business Manager" (label not yet updated) takes you to the Portfolio; from Portfolio, hamburger menu (top-left) → "Meta Business Suite" takes you back.

### Ads Manager
- The campaign tool. An ad account can exist without a Business Portfolio, but once an ad account is created in or claimed by a Portfolio, its access, billing, and partner permissions are managed at the Portfolio level.

### When a Business Portfolio is required (per practitioner sources, 2024–2026)
- Use Meta Business Suite; run ads with business-owned ad accounts; create/manage Shops; verify a domain; enroll in monthly invoicing; run social-issues/elections/politics ads (requires extra verification); work with agencies/partners; manage multiple Pages/ad accounts.

---

## 2. Creating a Business Portfolio

Click-path (desktop):
1. Log in to your **personal Facebook profile**.
2. Go to `business.facebook.com/overview` (or `business.facebook.com`) → **Create an account**.
3. Enter **Business name**, **your name**, **business email** → **Submit**.
4. **Verify the business email** via the confirmation email Meta sends (check spam — an unverified email blocks later steps like adding some assets).

Setup best practices:
- Use the same email as your personal Facebook account or a monitored business inbox; update a stale email in Facebook settings first.
- Use consistent, real business naming across the Portfolio, Page, and IG account — mismatches complicate verification and asset linking later.
- Create the portfolio from an authentic profile that complies with Meta's identity rules. A fake or disposable profile introduces avoidable access and enforcement risk.
- Avoid a single-person recovery dependency. For an established organization, give full control to a second trusted, separately secured owner and keep everyone else on least-privilege access. More full-control users improve continuity but also increase takeover risk.
- Fill in **Business Portfolio info** (legal business details, primary Page) right away; incomplete business info is a common verification and restriction trigger.

### Creation-limit recovery: do not confuse access with quota

- `Leave` removes access; it does not delete the portfolio. Removing a Page or
  Instagram asset does not affect creation quota.
- For the tested profile, support said leaving **or deleting** does not restore
  the lifetime creation quota and the quota cannot be increased. Treat that as
  the operative account decision; do not promise a 24/48-hour reset.
- The live creation error also suggested deleting an existing portfolio, which
  conflicts with the support reply. Preserve both, ask for manual escalation
  or clarification, and do not generalize either message to all users.
- If the limit remains, preserve Page and Instagram. Ask support to delete the
  inaccessible portfolio or identify/review the profile restriction. If support
  confirms no recovery, a real authorized colleague may create the company
  portfolio and grant appropriate access. Verify that the restricted user can
  accept and use that access before migrating assets.
- Deletion may be blocked by System Users, Pixels/datasets, or an ad account
  with issues. Do not use bought, shared, or fabricated profiles as a workaround.

---

## 3. Business Verification

### What it is and why it matters
- Business verification confirms to Meta that the portfolio belongs to a real legal entity. It is **not mandatory for basic advertising**, but it:
  - is required or strongly recommended for **WhatsApp Business API** (approval, higher messaging limits),
  - is required for **certain API/app features** and developer access,
  - can provide stronger ownership evidence during support or review flows,
  - is needed for some advanced features (e.g., certain sharing/partner features, politics/social-issues ads).
- Gotcha: the **"Start verification" button in Security Center is often greyed out** until you attempt a feature that requires verification (e.g., adding an app or WhatsApp number). This is normal; trigger the feature first, then the button activates [uncertain: exact trigger list changes over time].

### Click-path
`Business Settings → Security Center → Business Verification → Start verification → Get started` → choose the **country where the business is headquartered** → enter legal business details → select/confirm the business (Meta matches your details against public records) → upload documents if the business isn't matched → confirm phone/email via code.

### Documents
- Must show the **legal business name** plus **address and/or phone number**, match the details entered in the portfolio **exactly**, be in a supported language, and (per partner docs) generally be **no more than ~1 year old** for utility-bill-type documents.
- Accepted: certificate of formation/incorporation, articles of incorporation, business license/permits, business tax registration, business bank account statements, utility bills, business credit reports, shop establishment certificates, country-specific registrations (e.g., Udyam in India, PAN card).
- **Not accepted**: invoices, purchase orders, self-filed tax returns, personal bank statements, website printouts, self-created marketing docs (letterheads, flyers).
- If the main document lacks a phone number, a second document can verify the phone number.

### Timeline and status
- Practitioner/partner sources cite **~48 hours** (Superchat, 2026) up to **30 days** (Klaviyo, 2026) depending on queue and document quality. Status shows in **Security Center** as *In review* / *Verified* / rejected-with-reason.
- Common rejection causes: name/address mismatch between document and portfolio info, expired or self-created documents, unsupported language, blurry scans.

---

## 4. Ad Accounts: Adding, Creating, and Limits

### Click-path to create/add
`business.facebook.com/settings → Accounts → Ad accounts → + Add` → three options:
- **Add an ad account** (claim an existing account you own/admin),
- **Request access to an ad account** (for client accounts — correct agency workflow),
- **Create a new ad account** → set ad account name, time zone, currency → assign to people.

Gotchas:
- **Currency and time zone are permanent** once the ad account is created — you cannot change them later; a mistake means creating a new ad account.
- An ad account can only belong to **one** Business Portfolio. "Add" fails if another portfolio already owns it — use "Request access" instead.
- Closing/deactivating an ad account stops ads and publishing but is distinct from a policy-disabled account. A voluntarily closed account can normally be reactivated through Ads Manager after billing issues are resolved. Do not create a replacement account before checking the account state and supported reactivation flow. (Official Meta Help Center: https://www.facebook.com/help/messenger-app/331993756945799/)

### Ad Account Creation Limit
- New portfolios typically start with a limit of **1 ad account**. The limit grows with history: consistent spend, on-time payments, policy compliance (Jon Loomer; reconfirmed by Graphed 2025).
- Check your limit: `Business Settings → Business portfolio info` → **Ad account creation limit** [uncertain: Meta has moved this label; it may also appear under Business info].
- To raise it faster: build spend/payment history or work with a Meta account rep.

---

## 5. Connecting Facebook Pages and Instagram Professional Accounts

### Prerequisites for Instagram
- Use an Instagram **professional account**. Business and Creator accounts can both participate in many Meta business workflows, but commerce, partner, messaging, or publishing features may differ by account type and region. Prefer Business when the account represents a company and a required integration explicitly excludes Creator accounts.
- The IG account should be **linked to the Facebook Page** (Page → Settings → Linked accounts → Instagram, or via **Accounts Center**). This linkage powers cross-posting, unified inbox, and IG placement identity in ads.

### Add a Facebook Page to the portfolio
`Business Settings → Accounts → Pages → + Add → Add a Page` → search by Page name or paste Page URL → it appears instantly if you have the required access.
- Only someone with **full control / ownership-level access** on the Page can add it; if the Page is already claimed by another Business Portfolio, "Add" fails — you must **request access** from that portfolio or have the Page transferred.
- New Pages experience note: Page access is split between **Facebook access** (full control or partial: content, messages, ads, insights) and **task access** (granular permissions) — people with only "task access" may not be able to move a Page into a portfolio.
- Alternative: `+ Add → Request access to a Page` (agency scenario) — choose **Partial access** (specific tasks) or **Full control** → Confirm; Page admin approves.
- Set the **Primary Page** in Business portfolio info — used for business identity across Meta.

### Add an Instagram account to the portfolio
`Business Settings → Accounts → Instagram accounts → + Add` → log in with the Instagram professional-account credentials in the popup → grant requested permissions.
- The IG account must not be connected to a *different* Business Portfolio already — disconnect there first.
- After adding, **assign people** to the IG asset or they can't use it (adding a person to the portfolio does NOT automatically grant asset access — most common setup mistake).
- Verify the FB↔IG link in **Accounts Center → Sharing & logging in**; if the Page isn't listed, the connection is incomplete and IG may not appear as an identity option in Ads Manager.
- Troubleshooting: verify professional-account status, feature eligibility for Business versus Creator, Page/portfolio ownership, the operator's permissions, existing portfolio connections, and stale login sessions. Do not assume that Creator status alone is the cause.

---

## 6. People, Roles, and Partners

### People (Users → People)
- Add people by the **email tied to their Facebook profile**; they receive an email invite and appear as "Pending" until accepted. Invites expire and may need resending.
- Current role naming (2024+):
  - **Full control** (formerly "admin access") — manage settings, people, tools, all assets; can delete the portfolio. Give to max 2–3 trusted owners.
  - **Partial access** (formerly "employee access") — work only on assigned assets/tools.
  - **Advanced options**: **Finance** permissions (view/manage billing, invoices, credit lines without full control) and **temporary access** (time-limited, auto-revoked).
- Access is two-layered: **portfolio-level** (settings/people) and **asset-level** (per Page/ad account/dataset, with task toggles like "create ads", "view performance", "manage creative"). Adding a person ≠ assigning assets — always assign assets after adding.
- Page-level roles surfaced via portfolio: Page advertiser / Page analyst / Page editor; ad-account-level: ad account admin / advertiser / analyst. Grant the minimum needed (advertiser + analyst covers most agency work; admin not required).

### Partners (Users → Partners)
- The correct agency model: the client **keeps ownership**; the agency gets access through its own Business Portfolio.
- Steps: `Business Settings → Users → Partners → Add → Give a partner access to your assets` → paste the agency's **Business ID** (they find it in their own `Business Settings → Business portfolio info`) → select assets and permission levels → confirm.
- Reverse flow: `Ask a partner to share their assets` → you receive their assets into your portfolio (agency initiating).
- Prefer client ownership of client assets and grant the agency partner access. If an agency performs initial setup, document ownership, recovery, and transfer explicitly rather than leaving business-critical assets dependent on the agency.
- Removing a partner: `Users → Partners → select → Remove` — instant, no data loss, all assets stay with the owner. Review partners when contracts end.

### System users (Users → System users)
- Server-to-server identities for API/token use (not people); relevant for Conversions API and app integrations.
- Assign the app and each required ad account, Page, Instagram account, dataset,
  or catalog to the System User before generating its token. Token scopes and
  business-asset tasks are separate permission layers.
- A successful asset-list `GET` does not prove campaign-write or advertising
  identity access. Run a zero-spend `PAUSED` write and Page/Instagram creative
  probe before building the full campaign. See
  `13-api-access-billing-launch-operations.md`.

---

## 7. Payment Methods and Spending Limits

### Adding a payment method
- Portfolio level: `Business Settings → Billing & payments` — view balances, payment activity, credit lines, and all connected ad accounts' payment status in one place.
- Ad account level: `Ads Manager → ☰ All tools → Billing & payments → Payment settings → Add payment method`.
- Methods vary by country: credit/debit cards most common; PayPal and direct debit in supported markets; **manual payments** (prepay funds) in certain countries; **monthly invoicing / credit lines** only for qualifying established spenders via application.
- Billing can use automatic payments, available funds/manual payments, invoicing, or other account-specific arrangements. With automatic payments, Meta can charge at a billing threshold and on the bill date. Payment failures can stop delivery or trigger verification; no universal public rule makes every prepaid or virtual card a restriction trigger.
- Keep at least one **backup payment method**; a single declined charge can pause delivery and flag the account.
- Diagnose a failed transaction, current amount due, verified/default card,
  payment-method eligibility, and ad-account restriction separately. A zero
  balance and verified replacement card do not by themselves restore an account.
- Card entry, temporary-hold codes, 3DS, and verification belong in Meta's
  trusted UI. Never transmit full card data or verification codes through chat
  or API tooling.

### Spending limits (distinct concepts — don't confuse)
- **Account spending limit**: a hard cap on total lifetime spend for the ad account. When reached, **all campaigns stop delivering but still show as active** (Jon Loomer) — a classic "my ads stopped" mystery. Manage at `Ads Manager → Billing & payments → Payment settings → Account spending limit` (Set / Change / Remove / Reset via the `…` menu). Resetting lets spend continue under the same cap.
- **Daily spending limit**: Meta-imposed caps on new accounts (dynamic, grows with good history) — cannot be set manually.
- **Campaign spending limit**: optional per-campaign cap set at campaign level.
- Instagram-side: ads run through the linked ad account obey the same limits; the "Instagram ad spending limit" some guides mention is the same account spending limit surfaced in the IG promotion flow.

---

## 8. Two-Factor Authentication and Security Settings

### 2FA requirement (portfolio-wide)
- Click-path (current): `Meta Business Suite → Settings → Business portfolio info → Business options → Two-factor authentication` → choose **Admins only** / **Everyone** / **No one**.
- Only people with **full control** can change this.
- Meta allows new portfolios to require 2FA and requires it for **certain** portfolios older than 90 days; the rule is not documented as universal for every portfolio. Regardless of enforcement state, require 2FA for everyone with asset access as operational security. (Meta Help article mirror preserving the original source URL: https://support.chatarchitect.com/books/meta-business-portfolio-setup/page/turn-on-the-two-factor-authentication-requirement-in-your-business-portfolio)
- Side effects: people without 2FA on their personal accounts lose portfolio access until they enable it; browsers that clear cookies/private-mode will demand a code every login; third-party tools will require a login code on next sign-in.
- Individuals enable 2FA in their own Facebook `Accounts Center → Password and security → Two-factor authentication` (authenticator app preferred over SMS).

### Other security surfaces
- **Security Center** (Business Settings): business verification status, 2FA requirement, security alerts, recent activity.
- **Account quality** (Business Support Home / `Business Settings → Account quality` in some UIs): restriction status for the portfolio, ad accounts, and linked personal profiles; the starting point for appeals (`View details` → request review).
- Operational hygiene: remove ex-employees/ex-agencies immediately; audit `Users → People` and `Users → Partners` quarterly; never share personal logins; be wary of phishing emails impersonating "Meta Business Support" (a leading cause of portfolio takeover, which then leads to ad-account bans for fraudulent spend).

---

## 9. Business Settings Panel Structure (what lives where)

Entry: `business.facebook.com/settings` (or Business Suite → Settings, which redirects here). Left-hand panel, current naming (ordering and a few labels vary by rollout):

- **Users**: People · Partners · System users — who can access the portfolio and at what level.
- **Accounts**: Pages · Ad accounts · Business asset groups · Apps · Instagram accounts · WhatsApp accounts · Commerce accounts — the owned/claimed assets.
- **Data sources**: Catalogs · Datasets · Meta Pixels · Custom conversions · Audiences. A dataset groups events from website, app, offline, and other sources; the Meta Pixel remains the web data source and may share the same ID as its dataset. (Official: https://www.facebook.com/help/messenger-app/952192354843755)
- **Brand safety and suitability**: Domains (domain verification) · Block lists.
- **Security center**: business verification, 2FA requirement, alerts.
- **Business portfolio info**: business details, primary Page, **ad account creation limit**, business options (incl. 2FA), **permanently delete business**.
- **Billing & payments**: balances, payment methods, invoices, credit lines, connected accounts.
- **Account quality / Business Support Home**: restrictions and appeals (sometimes accessed via `business.facebook.com/business-support-home`).
- **Settings gear in Business Suite** redirects into this panel — there is no separate "Suite settings."

Legacy mapping for older tutorials: "Business Manager" ≈ Business Portfolio; "Admin access" ≈ Full control; "Employee access" ≈ Partial access; "Business Settings → Business Info" ≈ Business portfolio info. Do not map "Pixels" directly to "Datasets": the Pixel remains a web data source whose events can be grouped in a dataset.

---

## 10. Setup failures and restriction diagnosis

### Restrictions: levels and mechanics
- Enforcement or access problems can affect a person, Page, ad account, business portfolio, payment method, or individual ad. Inspect the exact affected asset and reason instead of assuming a portfolio-wide ban.
- First stop for diagnosis: **Account quality / Business Support Home** and the Delivery/status details in Ads Manager. Follow the available review path and provide only the identity, business, billing, or compliance evidence requested for that case.

### Common setup and access failures
1. **Inauthentic or shared profiles** violate identity rules and make ownership recovery unreliable.
2. **Incomplete requested verification or missing 2FA** blocks workflows that explicitly require them. Neither condition should be presented as a universal cause of ad-account restriction without the displayed reason.
3. **Payment problems** include declines, insufficient funds, unsupported methods, inconsistent billing details, and unpaid balances. Resolve the exact billing message rather than categorically rejecting all prepaid or virtual cards.
4. **Unexpected access patterns or compromised credentials** can trigger security checks. Do not prescribe a generic account “warm-up”; maintain consistent authorized access and respond to the actual checkpoint.
5. **Asset ownership problems**: a Page or data source owned by an ex-employee or previous agency, assets claimed by another portfolio, or duplicate setups with unclear ownership. Verify the consequences and recovery window before deleting any business or asset.
6. **Sharing logins or granting full control broadly** — a compromised admin account takes the whole portfolio down; use partner access and partial access instead.
7. **Wrong Instagram linkage or permissions**: the account is connected elsewhere, the user lacks the required access, or the selected feature does not support the account type.
8. **Incomplete business contact details** can prevent verification or recovery communications; no public evidence establishes a universal hidden “trust score” penalty.
9. **Unmanaged account spending limit** — not a restriction, but mimics one: ads silently stop at the cap while still showing "active."
10. **Running ads before the foundation is clean** (unclaimed Page, personal ad account, no Pixel/dataset ownership) — makes later migrations painful and can strand historical data with whoever owns the asset.

### Structural practices that improve continuity
- One portfolio per legal entity; business owns all assets; agencies get **partner** access only.
- 2+ full-control admins, everyone else partial/temporary access; quarterly access audits.
- Business verification + 2FA requirement enabled from day one; real, matching business details everywhere.
- Keep authorized payment methods healthy and add a backup where supported. Set budgets from economics and risk tolerance, not an account-aging ritual.

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
