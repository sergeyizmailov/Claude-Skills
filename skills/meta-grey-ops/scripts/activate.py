#!/usr/bin/env python3
"""Internal activation implementation for workspace-bound metaops.

Activation is a spend-producing action and needs the operator's explicit approval of the
final budget, schedule, destination and creative set. "Do everything" authorises the
build, not the spend. Run verify.py first — this script refuses to guess.

Order matters: ads and ad sets first, campaign last. Flipping the campaign on while a
child is still misconfigured is how a bad ad set gets a live hour.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

import graph


def receipt_path(state_path: str) -> str:
    return state_path + ".verified.json"


def file_sha(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:16]


def check_receipt(state_path: str, state: dict | None = None) -> str | None:
    """None when verify.py passed on exactly this state file, else the reason it did not.

    verify.py writes `<state>.verified.json` {state_sha, ok, ts} only on exit 0. If the
    state file changed since (a resume added objects), the hash differs and the receipt is
    void — verify again. An operator's word that verify passed is not a receipt."""
    rp = receipt_path(state_path)
    if not os.path.exists(rp):
        return f"no verification receipt ({rp}). Run metaops verify for the bound plan first"
    try:
        with open(rp, encoding="utf-8") as fh:
            r = json.load(fh)
    except ValueError:
        return f"unreadable receipt {rp}"
    if not r.get("ok"):
        return "receipt records a failed verification"
    if r.get("state_sha") != file_sha(state_path):
        return "state file changed after verification — run verify.py again"
    if state is None:
        with open(state_path, encoding="utf-8") as fh:
            state = json.load(fh)
    # A spec-less verify only checks statuses and destinations. Activation needs the full
    # diff, so the receipt must carry the spec hash and it must be the spec that built the tree.
    if not r.get("spec_sha"):
        return ("receipt came from a spec-less verification — re-run metaops verify for the "
                "bound plan")
    if not state.get("spec_sha"):
        return ("state file carries no spec_sha (legacy or hand-written); it cannot be activated "
                "through the agent interface — create a new workspace-bound plan")
    if r["spec_sha"] != state["spec_sha"]:
        return "receipt was made against a different spec than the one that built this state"
    return None


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
            "destination URL, creative set. verify.py must have exited 0 on this exact state file "
            "(it leaves a receipt next to it; this script checks it)."
        )

    with open(args.state, encoding="utf-8") as fh:
        state = json.load(fh)
    graph.require_write_authority(
        "POST", f"{graph.normalize_account(state.get('spec_account', ''))}/campaigns"
    )
    why = check_receipt(args.state, state)
    if why:
        sys.exit(f"Refusing to activate: {why}.")
    objects = state["objects"]
    if state.get("in_flight"):
        sys.exit(f"Refusing to activate: unresolved in-flight creates {sorted(state['in_flight'])} — "
                 "the tree is incomplete or has an unreconciled object.")
    if not any(k.startswith("ad[") for k in objects):
        sys.exit("Refusing to activate: state holds no ads — nothing would deliver, and an ad set "
                 "activated without ads is a half-built tree.")

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
