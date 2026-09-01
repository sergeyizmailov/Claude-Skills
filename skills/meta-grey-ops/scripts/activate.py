#!/usr/bin/env python3
"""The only script here that can cause spend. Deliberately separate, deliberately noisy.

    python3 activate.py --state .meta-launch/<run_id>.json --confirm SPEND

Activation is a spend-producing action and needs the operator's explicit approval of the
final budget, schedule, destination and creative set. "Do everything" authorises the
build, not the spend. Run verify.py first — this script refuses to guess.

Order matters: ads and ad sets first, campaign last. Flipping the campaign on while a
child is still misconfigured is how a bad ad set gets a live hour.
"""

from __future__ import annotations

import argparse
import json
import sys

import graph


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--state", required=True)
    ap.add_argument("--confirm", help="Must be the literal string SPEND")
    ap.add_argument("--refresh-start", help="ISO8601 start_time to set before activating")
    args = ap.parse_args()

    if args.confirm != "SPEND":
        sys.exit(
            "Refusing to activate without --confirm SPEND.\n"
            "Before you pass it, confirm with the operator: daily budget, schedule, "
            "destination URL, creative set, and that verify.py exited 0."
        )

    with open(args.state, encoding="utf-8") as fh:
        objects = json.load(fh)["objects"]

    campaign_id = objects.get("campaign")
    if not campaign_id:
        sys.exit("no campaign in state file")

    camp = graph.get(
        campaign_id,
        params={"fields": "name,daily_budget,objective,effective_status"},
        context="pre-activation read",
    )
    print(f"About to activate: {camp.get('name')}")
    print(f"  objective     {camp.get('objective')}")
    print(f"  daily_budget  {camp.get('daily_budget')} (minor units, account currency)")
    print(f"  status now    {camp.get('effective_status')}\n")

    # A paused build can outlive its own start_time while access or billing is sorted.
    # A start_time in the past does not error — it just starts immediately, which is
    # exactly the dead-hours launch the scheduling rule exists to prevent.
    if args.refresh_start:
        i = 0
        while f"adset[{i}]" in objects:
            graph.post(objects[f"adset[{i}]"], {"start_time": args.refresh_start},
                       context=f"refresh start adset[{i}]", idempotent=True)
            print(f"  start_time → {args.refresh_start} on adset[{i}]")
            i += 1

    order = (
        [k for k in objects if k.startswith("ad[")]
        + [k for k in objects if k.startswith("adset[")]
        + ["campaign"]
    )
    # Children first, campaign last — and STOP on a child failure. Flipping the campaign
    # on while an ad or ad set is broken buys delivery for a tree you did not verify.
    for key in order:
        obj_id = objects[key]
        try:
            graph.post(obj_id, {"status": "ACTIVE"}, context=f"activate {key}", idempotent=True)
            print(f"  ACTIVE  {key} {obj_id}")
        except graph.GraphError as e:
            print(f"  FAILED  {key} {obj_id}: {e}", file=sys.stderr)
            # 2490468: a REJECTED ad cannot be enabled at all. Editing does not help;
            # the fix is a brand-new ad. Do not retry, do not fight the reject.
            if e.subcode == 2490468 or "2490468" in str(e):
                print("          rejected ad — build a NEW ad, editing will not clear it",
                      file=sys.stderr)
            if key == "campaign":
                done = order[:order.index(key)]
                print(f"\nThe campaign was NOT activated, so nothing is spending. "
                      f"{len(done)} child object(s) are ACTIVE and idle beneath it: {done}.",
                      file=sys.stderr)
                return 1
            done = order[:order.index(key)]
            print(f"\nSTOPPED. The campaign was NOT activated, so nothing is spending — "
                  f"but {len(done)} child object(s) were already set ACTIVE before this "
                  f"failure: {done}. They deliver nothing while the campaign is paused. "
                  f"Fix this object and re-run: re-activating the others is a no-op.",
                  file=sys.stderr)
            return 1

    print("\nActivated. A successful mutation does not mean spend started.")
    print("Read delivery back within the hour: effective_status, spend, and the tracker.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
