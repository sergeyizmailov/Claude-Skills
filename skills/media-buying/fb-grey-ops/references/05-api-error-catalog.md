# 05 — API errors: the grey survival response

Canonical code → cause → fix lives in `meta-ads/14` (the API-owner skill). This
file is the grey-ops RESPONSE layer: what an error MEANS for account/profile
survival and what to do — freeze, replace, or rotate. Don't duplicate the code
table; look codes up in 14, act here.

General rule: match on `error_user_msg`, not the number — several codes buyers
rely on (1815857, 3858040, 2446814, 1815045, 3738001) are field-observed and not
in Meta's published references, so the string is more stable than the digits.

## Auth 190 → freeze protocol

Any token-death subcode (460 password/security rotation, 463 expired, 467
invalid — 467 still emits the "user logged out" string in the wild) = mint a new
token and re-exchange (see 14/02). Grey response:
- Regenerate ONCE, exchange to long-lived, stop. Every extra regen during a flag
  pokes the bear (01).
- Subcode 460 specifically (security rotation) or repeated deaths in a short
  window = the persona is under security pressure → switch to freeze protocol
  (01): no re-logins, no profile edits, let it settle.

## Access denied (10 / 200) → check shares, not code

Missing capability or asset not shared — not a bug to debug in code. Check BM
assignments (pixel/pages to the ad account, 03) and your access tier (02: your
own app on agency accounts sits at the Limited tier). A write-probe (create one
PAUSED object) proves write access; GET does not.

## Delivery / account-state → replace, don't fight

- Pixel "no access" (msg like #1815045): assign via BM Data Sources → Datasets,
  or ask the agency; ads recover automatically, no rebuild (03).
- "Not delivering", no error: future start_time (normal), review pending,
  billing hold, or spend cap — wait/verify before touching.
- Account "Disabled"/restricted: routine in agency stock. Document (ID, date,
  spend at death), request replacement, move on — don't appeal fresh stock (03).
- CSV import blocked on fresh accounts (msg like #3738001): build via API/UI.

## Rate limits → back off, don't burn calls

BUC / header-driven (canonical detail in 14). A single buyer never approaches
the ceiling; the only grey rule is don't poll in tight loops — a throttle storm
on one persona's IP is a needless signal.

## When bot/fraud signals spike (not an API error)

Rising bot_share / domain-level flags (from the tracker, tracker-ops/03) → this
is the grey ACTION for that signal: rotate the domain before it burns the
account; don't wait for the ban.

<!-- Changelog 2026-08-11: Peer-review (gpt) boundary fix — restructured from a
duplicate code catalog into the grey survival RESPONSE layer (freeze/replace/
rotate); canonical code→fix now owned by meta-ads/14 (pointer reversed). Kept
the death-code freeze protocol, replace-don't-fight account handling, and the
domain-rotation action for tracker bot signals. -->
