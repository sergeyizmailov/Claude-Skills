# 02 — Meta app & tokens

API version v26.0 (2026-07-29); pin `/v26.0/` in call paths. Each version has a
~2-year support window then deprecates — check the Graph API changelog for the
exact sunset date rather than assuming.

## App setup (once)

- developers.facebook.com → Create app (use-case flow; exact tile wording is
  volatile/UNVERIFIED — the old "Create & manage ads with Marketing API" label
  may be gone). Working path: Business-type app → add **Marketing API** product.
- Dev mode READS insights + EDITS existing objects but can't create creatives
  (error 1885183). Go Live (Publish) — needs a Privacy Policy URL (App settings
  → Basic) returning HTTP 200.
- Live toggle needs no business verification. Production access is a property of
  the APP, not the BM — a verified agency BM does NOT make your app inherit
  access. See the access matrix below.

## Access matrix (get this right before launch)

"Marketing API Access Tier" (renamed from Ads Management Standard Access;
levels renamed Standard→Limited, Advanced→Full):
- **Limited** = default when you add the Marketing API product. Heavily
  rate-limited per ad account, "for development only". Allows: 1 system user +
  1 admin system user.
- **Full** = via App Review; higher limits, 10 system users + 1 admin. Qualify
  at ~≥500 MAPI calls / 15 days with <15% errors. Requires **Business
  Verification**.

Which you need:
- Managing ad accounts your token user OWNS / has a role on **inside your own
  business** → Limited/default `ads_read`+`ads_management` is enough.
- Managing **other people's** ad accounts (the agency case — accounts belong to
  the agency's/clients' BMs) → **Full Access** (App Review + Business
  Verification). Being a member of the agency's verified BM is a prerequisite,
  not the grant.
- Grey-tenant reality: your OWN app on agency (third-party) accounts hits the
  Limited/dev tier. Practically you operate via the agency's app/tokens, or a
  user token minted with an app that already holds the access — accept the
  Limited rate ceiling otherwise. Confirm access with a write-probe (create one
  PAUSED object): a successful GET does NOT prove write access.

## Permissions

ads_read, ads_management, business_management, pages_read_engagement,
pages_show_list (+public_profile). All current, none renamed in v26.0.
`catalog_management` needs App Review (Advanced Access) — until approved it's
stripped from the token, catalog writes fail; do catalog/product-sets in
Commerce Manager UI.

## User token lifecycle

1. Mint in Graph API Explorer INSIDE the antidetect profile (same IP).
2. Exchange to long-lived (~60d) immediately:
   `GET /v26.0/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=SECRET&fb_exchange_token=SHORT`
3. `GET /debug_token` (access_token = `APP_ID|SECRET`) → check is_valid,
   expires_at, scopes.
4. Store in gitignored secrets; reminder ~55d out.

## System User tokens

Session-independent (survive the death codes below) — the durable choice, but
creating one needs BM admin (agency tenants rarely have it → normally N/A). When
you do: Business settings → System users → add a REGULAR user (not admin) for
API, assign only needed assets, generate token with the scopes above. "Never"
expiry is a Business-Settings option (not dev-doc-guaranteed). Clean view:
meta-ads/13.

## Token death codes (190 subcodes)

- 460 — session invalidated (password change OR Meta security rotation; also
  the old "logged out"). Dead permanently → mint + re-exchange; freeze other
  profile actions.
- 463 — session expired/revoked → mint new.
- 467 — doc-level "invalid access token"; but Meta still emits "session invalid
  because the user logged out" in the wild (seen 2026-08) → mint new.
- "Malformed access token" — copy damage; re-copy, compare length.
Dead token never revives. Repeated deaths = persona under pressure → freeze (01).

## Access denials

Permission/approval denial = code 10 / 200 (missing capability, e.g. catalog
API without catalog_management), NOT code 100 — code 100 is "Invalid parameter".
Ignore the wild "not approved to use this api" string; trust the code (05).

## Ad account timezone

`timezone_name` (e.g. America/Los_Angeles) + `timezone_id` + `timezone_offset_hours_utc`.
Governs reporting day boundaries, scheduling, billing. Agency accounts often
UTC-7. Tracker "day" and Meta "day" only align in account tz.

## Rate limits

Marketing API runs on dynamic BUC limits read from response headers, not a
fixed quota (details/back-off in 05). A single buyer never approaches it — just
don't poll in tight loops.
