# 05 — API errors: the grey survival response

Reviewed 2026-08-28. Codes and canonical meaning are [official], live in
`meta-ads/14`. The freeze/replace/rotate mapping here is practitioner judgment
about what an error implies for account survival — no Meta source states it.

Matching rule: branch on `code` + `error_subcode`, never the message string —
`meta-ads/14` owns that rule (field-observed codes 1815857, 3858040, 2446814,
1815045, 3738001 are still safe to match numerically). Log `error_user_msg` as
evidence only.

| Trigger | Grey response |
|---|---|
| Auth 190, subcode 460 (password/security rotation), 463 (expired), 467 (invalid — still emits "user logged out" in the wild) | Mint new token, re-exchange (`meta-ads/14` auth; lifecycle `02`). Regenerate ONCE, exchange to long-lived, stop — every extra regen during a flag pokes the bear (`01`) |
| Subcode 460 specifically, or repeated token deaths in a short window | Persona under security pressure → freeze protocol (`01`): no re-logins, no profile edits, let it settle |
| Access denied (10 / 200) | Not a code bug — check BM asset shares (pixel/pages to the ad account, `03`) and access tier (`02`: your own app on agency accounts sits at Limited). A write-probe (create one PAUSED object) proves write access; GET does not |
| Pixel "no access" (1815045) | Assign via BM Data Sources → Datasets, or ask the agency; ads recover automatically, no rebuild (`03`) |
| "Not delivering", no error | Future start_time (normal), review pending, billing hold, or spend cap — wait/verify before touching |
| Account "Disabled"/restricted | Routine in agency stock. Document (ID, date, spend at death), request replacement, move on — don't appeal fresh stock (`03`) |
| CSV import blocked on fresh accounts (3738001) | Build via API/UI instead |
| Rate limits (BUC/header-driven, detail in `meta-ads/14`) | Back off, don't burn calls — a single buyer never nears the ceiling; don't poll in tight loops, a throttle storm on one persona's IP is a needless signal |
| Rising bot_share / domain-level flags (tracker-ops/03, not an API error) | Rotate the domain before it burns the account — don't wait for the ban |
