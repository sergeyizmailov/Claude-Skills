#!/usr/bin/env python3
"""Pull spend and delivery for the daily sync. Account timezone, no eyeballing.

    python3 insights.py --account act_123 --level campaign --since 2026-08-25 --until 2026-08-31
    python3 insights.py --account act_123 --level ad --date-preset yesterday --csv day.csv

Feeds the tracker cost push (tracker-ops/01 update_costs). Two rules it enforces so the
numbers reconcile:

· Every row is in the AD ACCOUNT timezone, which is what Meta reports in and what the
  daily CPL must be computed in — for spend AND for leads. Mixing timezones is the
  quiet way to get a CPL that is wrong by one day's worth of traffic.
· `action_attribution_windows` is stated explicitly. Meta's default is 7-day click, so
  an unstated window silently reports more conversions than a 1-day-click ad set
  actually earned, and the tracker will disagree.

What this does NOT do is decide anything. Meta numbers are one source; the payout
metric lives in the tracker (tracker-ops metric rule) and cohorts mature on click date.
Never conclude from this output alone.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time

import graph

SUMMARY_SCHEMA = "insights.result/v1"

FIELDS = [
    "date_start", "date_stop", "account_currency",
    "campaign_id", "campaign_name", "adset_id", "adset_name", "ad_id", "ad_name",
    "spend", "impressions", "clicks", "inline_link_clicks", "reach", "frequency",
    "cpm", "ctr", "cpc", "actions", "action_values", "cost_per_action_type",
]

# v26.0 removed these; requesting them errors on ANY version. Listed so nobody adds
# them back from an older snippet.
REMOVED_AT_V26 = ("total_video_impressions", "total_video_views_unique")


def flatten_actions(row: dict) -> dict:
    """Actions arrive as a list of {action_type, value}. Flatten the ones worth a column
    and keep the raw list in the JSON output."""
    out = dict(row)
    for key in ("actions", "cost_per_action_type", "action_values"):
        for entry in row.get(key) or []:
            atype = entry.get("action_type", "?")
            out[f"{key}:{atype}"] = entry.get("value")
        out.pop(key, None)
    return out


def fetch(account: str, level: str, params: dict) -> list[dict]:
    """Insights are computed async on large ranges; this follows paging and waits out
    the empty-result window on fresh objects (15-40 min, not a failure)."""
    rows: list[dict] = []
    path = f"{account}/insights"
    query = dict(params, level=level, fields=",".join(FIELDS), limit=500)

    while True:
        resp = graph.get(path, params=query, context=f"insights {level}")
        rows.extend(resp.get("data", []))
        nxt = (resp.get("paging") or {}).get("next")
        if not nxt:
            return rows
        path, query = nxt, {}
        time.sleep(0.3)  # a read is 1 point; do not sprint through paging


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--account", required=True)
    ap.add_argument("--level", default="campaign", choices=["account", "campaign", "adset", "ad"])
    ap.add_argument("--since", help="YYYY-MM-DD, account timezone")
    ap.add_argument("--until", help="YYYY-MM-DD, account timezone")
    ap.add_argument("--date-preset", help="e.g. yesterday, last_7d — used when --since is absent")
    ap.add_argument("--click-window", type=int, default=1, help="attribution click days (default 1)")
    ap.add_argument("--view-window", type=int, default=1, help="attribution view days (default 1)")
    ap.add_argument("--breakdown", help="e.g. country, publisher_platform")
    ap.add_argument("--csv", help="Write a flat CSV here")
    ap.add_argument("--json", help="Write the raw rows here")
    args = ap.parse_args()

    account = graph.normalize_account(args.account)

    acct = graph.get(account, params={"fields": "timezone_name,currency"}, context="account tz")
    print(f"{account}  tz={acct.get('timezone_name')}  currency={acct.get('currency')}")
    print("All dates below are in that timezone. Compute CPL against tracker leads in the "
          "SAME timezone or the number is wrong.\n")

    params: dict = {
        "action_attribution_windows": [
            f"{args.click_window}d_click", f"{args.view_window}d_view"
        ],
    }
    if args.since or args.until:
        if not (args.since and args.until):
            sys.exit("--since and --until must be given together")
        params["time_range"] = {"since": args.since, "until": args.until}
        params["time_increment"] = 1
    else:
        params["date_preset"] = args.date_preset or "yesterday"
        params["time_increment"] = 1
    if args.breakdown:
        params["breakdowns"] = args.breakdown

    rows = fetch(account, args.level, params)
    if not rows:
        print("No rows. On freshly created objects insights stay empty for 15-40 min — "
              "that is propagation, not a delivery failure.")
        print(json.dumps({
            "schema": SUMMARY_SCHEMA, "account": account, "level": args.level, "rows": 0,
            "total_spend": 0.0, "currency": acct.get("currency"), "timezone": acct.get("timezone_name"),
            "csv": args.csv, "json": args.json,
        }, ensure_ascii=False))
        return 0

    flat = [flatten_actions(r) for r in rows]
    total = sum(float(r.get("spend", 0) or 0) for r in rows)
    print(f"{len(rows)} rows, total spend {total:.2f} {acct.get('currency')}")

    if args.csv:
        cols: list[str] = []
        for r in flat:
            for k in r:
                if k not in cols:
                    cols.append(k)
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(flat)
        print(f"csv → {args.csv}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            fh.write(graph.redact(json.dumps(rows, indent=2)))
        print(f"json → {args.json}")

    if not (args.csv or args.json):
        for r in flat[:50]:
            name = r.get("ad_name") or r.get("adset_name") or r.get("campaign_name") or account
            print(f"  {r.get('date_start')}  {name[:44]:<44}  spend {r.get('spend')}")

    print("\nNext: push these as cost into the tracker (tracker-ops/01 update_costs). "
          "No cost push = report cost is 0 = no CPL.")
    print(json.dumps({
        "schema": SUMMARY_SCHEMA, "account": account, "level": args.level, "rows": len(rows),
        "total_spend": round(total, 2), "currency": acct.get("currency"),
        "timezone": acct.get("timezone_name"), "csv": args.csv, "json": args.json,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
