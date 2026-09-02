#!/usr/bin/env python3
"""Status + spend sweep across accounts. The detection half of the ban loop (03).

    python3 monitor.py --accounts accounts.json                 # today + yesterday
    python3 monitor.py --accounts act_1,act_2 --log survival.jsonl
    python3 monitor.py --accounts accounts.json --json out.json --quiet

Per account, in one pass:
  · account_status / disable_reason / balance / spend_cap / amount_spent
  · yesterday's and today's spend (account level, account timezone)
  · counts of ads by effective_status — DISAPPROVED / WITH_ISSUES / ACTIVE / PAUSED
  · ad sets with issues_info

Verdicts it prints (never acts on):
  DISABLED         account_status != 1 → document (id, date, spend at death) and replace (03)
  UNSETTLED        status 3 = unpaid balance, a topup fixes it — NOT a ban
  SILENT_STOP      was spending yesterday, ~0 today past mid-day → ASL cap, billing hold,
                   throttle or a restriction not yet surfaced as status
  REJECTS          DISAPPROVED ads present → new ads, do not fight (2490468)
  OK

Every row is appended to --log as JSONL with a UTC timestamp: that log is what makes the
forensics in 06 and the agency replacement lists possible. Autolaunch SaaS shows this on a
dashboard; here it is a cron line.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys

import graph

ACCOUNT_FIELDS = ("id,name,account_status,disable_reason,currency,timezone_name,"
                  "timezone_offset_hours_utc,balance,spend_cap,amount_spent")
STATUS = {1: "ACTIVE", 2: "DISABLED", 3: "UNSETTLED", 7: "PENDING_RISK_REVIEW",
          8: "PENDING_SETTLEMENT", 9: "IN_GRACE_PERIOD", 100: "PENDING_CLOSURE", 101: "CLOSED"}


def load_accounts(arg: str) -> list[str]:
    if arg.endswith(".json"):
        with open(arg, encoding="utf-8") as fh:
            rows = json.load(fh)
        ids = [r["account_id"] if isinstance(r, dict) else r for r in rows]
    else:
        ids = arg.split(",")
    return [graph.normalize_account(i) for i in ids if str(i).strip()]


def spend(account: str, preset: str) -> float:
    rows = graph.get(f"{account}/insights",
                     params={"fields": "spend", "date_preset": preset, "level": "account"},
                     context=f"spend {preset}").get("data", [])
    return float(rows[0]["spend"]) if rows else 0.0


def ad_status_counts(account: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    path, params = f"{account}/ads", {"fields": "effective_status", "limit": 500,
                                       "effective_status": json.dumps(
                                           ["ACTIVE", "PAUSED", "DISAPPROVED", "WITH_ISSUES",
                                            "PENDING_REVIEW", "ADSET_PAUSED", "CAMPAIGN_PAUSED"])}
    while True:
        resp = graph.get(path, params=params, context="ads status")
        for ad in resp.get("data", []):
            counts[ad.get("effective_status", "?")] = counts.get(ad.get("effective_status", "?"), 0) + 1
        nxt = (resp.get("paging") or {}).get("next")
        if not nxt:
            return counts
        path, params = nxt, {}


def adset_issues(account: str) -> list[dict]:
    rows = graph.get(f"{account}/adsets",
                     params={"fields": "id,name,effective_status,issues_info", "limit": 200},
                     context="adset issues").get("data", [])
    return [{"id": a["id"], "name": a.get("name"), "issues": a["issues_info"]}
            for a in rows if a.get("issues_info")]


def local_hour(offset_hours: float | None) -> int | None:
    if offset_hours is None:
        return None
    return (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=float(offset_hours))).hour


def sweep(account: str) -> dict:
    row: dict = {"account": account, "ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    try:
        acct = graph.get(account, params={"fields": ACCOUNT_FIELDS}, context="account")
    except graph.GraphError as e:
        row.update({"verdict": "UNREACHABLE", "error": str(e), "code": e.code, "subcode": e.subcode})
        return row
    st = acct.get("account_status")
    row.update({
        "name": acct.get("name"), "status": st, "status_label": STATUS.get(st, f"UNKNOWN({st})"),
        "disable_reason": acct.get("disable_reason"), "currency": acct.get("currency"),
        "tz": acct.get("timezone_name"), "balance": acct.get("balance"),
        "spend_cap": acct.get("spend_cap"), "amount_spent": acct.get("amount_spent"),
    })
    try:
        row["spend_yesterday"] = spend(account, "yesterday")
        row["spend_today"] = spend(account, "today")
        row["ads"] = ad_status_counts(account)
        row["adset_issues"] = adset_issues(account)
    except graph.GraphError as e:
        row["error"] = str(e)

    hour = local_hour(acct.get("timezone_offset_hours_utc"))
    verdicts = []
    if st == 3:
        verdicts.append("UNSETTLED")
    elif st != 1:
        verdicts.append("DISABLED")
    if row.get("ads", {}).get("DISAPPROVED"):
        verdicts.append("REJECTS")
    if row.get("ads", {}).get("WITH_ISSUES") or row.get("adset_issues"):
        verdicts.append("ISSUES")
    y, t = row.get("spend_yesterday", 0.0), row.get("spend_today", 0.0)
    # Only a verdict when something is supposed to be delivering: all-paused accounts
    # legitimately spend 0 (false positive seen 2026-09-02 on a paused account).
    active_ads = row.get("ads", {}).get("ACTIVE", 0)
    if st == 1 and active_ads and y > 0 and hour is not None and hour >= 12 and t < 0.05 * y:
        verdicts.append("SILENT_STOP")
    cap = acct.get("spend_cap")
    try:
        if cap and int(cap) > 0 and int(acct.get("amount_spent", 0)) >= int(cap):
            verdicts.append("ASL_HIT")
    except (TypeError, ValueError):
        pass
    row["verdict"] = ",".join(verdicts) or "OK"
    return row


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--accounts", required=True, help="accounts.json (bulk.py format) or act_1,act_2")
    ap.add_argument("--log", default="survival.jsonl", help="append-only JSONL survival log")
    ap.add_argument("--json", help="write this sweep's rows here")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    rows = []
    for acct in load_accounts(args.accounts):
        row = sweep(acct)
        rows.append(row)
        if not args.quiet:
            ads = row.get("ads", {})
            print(f"{acct:<20} {row.get('status_label', '?'):<18} y={row.get('spend_yesterday', '-'):<9} "
                  f"t={row.get('spend_today', '-'):<9} rej={ads.get('DISAPPROVED', 0)} "
                  f"issues={ads.get('WITH_ISSUES', 0)}  → {row['verdict']}")
    with open(args.log, "a", encoding="utf-8") as fh:
        for row in rows:
            fh.write(graph.redact(json.dumps(row, default=str)) + "\n")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            fh.write(graph.redact(json.dumps(rows, indent=2, default=str)))
    bad = [r for r in rows if r["verdict"] != "OK"]
    print(f"\n{len(rows)} account(s), {len(bad)} need attention. Log → {args.log}")
    if bad:
        print("DISABLED → document + replace (03). UNSETTLED → topup. SILENT_STOP → check ASL, "
              "billing, review; touch nothing else. REJECTS → new ads, never re-enable.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
