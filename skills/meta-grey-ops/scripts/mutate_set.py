#!/usr/bin/env python3
"""Swap what a product set contains, and prove it actually changed.

    python3 mutate_set.py --set-id 123 --show
    python3 mutate_set.py --set-id 123 --retailer-ids slot_01,slot_02,slot_03,slot_04
    python3 mutate_set.py --set-id 123 --filter filter.json

Two failure modes this removes, both field-observed (04):

1. `filter` must be JSON-ENCODED EXACTLY ONCE. Meta's own reference calls it "a
   JSON-encoded rule" and passes a string, so a single-encoded string is correct on the
   wire — what breaks is encoding it twice, which happens the moment you hand an
   already-stringified filter to a transport that stringifies for you. The double-encoded
   POST silently no-ops: set id returned, HTTP 200, filter unchanged, no error to notice.
   This script passes a dict and lets graph.py encode it once, then re-reads the set to
   prove the mutation landed.

2. Editing a product in Commerce Manager RECREATES it under a new product_item_id. A
   filter that referenced the old id silently drops it and the set shrinks — ads keep
   delivering on fewer cards. After any manual product fix, re-run with --show.

Set-membership changes do not trigger ad re-review. Format minimums still apply:
COLLECTION needs >=4 items in the set (2490457 at build); regular catalog single-card
and carousel ads have no minimum.
"""

from __future__ import annotations

import argparse
import json
import sys

import graph

SET_FIELDS = "id,name,product_count,filter,product_catalog{id,name}"
COLLECTION_MIN = 4


def show(set_id: str) -> dict:
    s = graph.get(set_id, params={"fields": SET_FIELDS}, context="product set")
    print(f"set {s['id']}  {s.get('name')}")
    print(f"  product_count {s.get('product_count')}")
    print(f"  catalog       {(s.get('product_catalog') or {}).get('name')}")
    print(f"  filter        {json.dumps(s.get('filter'))}")
    if (s.get("product_count") or 0) < COLLECTION_MIN:
        print(f"  WARN  under {COLLECTION_MIN} items — a COLLECTION creative will fail 2490457. "
              "Single-card and carousel catalog ads are unaffected.")
    return s


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--set-id", required=True)
    ap.add_argument("--show", action="store_true", help="Read the set and exit")
    ap.add_argument("--retailer-ids", help="Comma-separated retailer_id values to select")
    ap.add_argument("--filter", help="Path to a JSON file holding the filter object")
    args = ap.parse_args()

    before = show(args.set_id)
    if args.show:
        return 0

    if args.filter:
        with open(args.filter, encoding="utf-8") as fh:
            new_filter = json.load(fh)
        if not isinstance(new_filter, dict):
            sys.exit("--filter must contain a JSON OBJECT, not a string or array")
    elif args.retailer_ids:
        ids = [x.strip() for x in args.retailer_ids.split(",") if x.strip()]
        if not ids:
            sys.exit("--retailer-ids is empty")
        new_filter = {"retailer_id": {"is_any": ids}}
    else:
        sys.exit("pass --show, --retailer-ids, or --filter")

    print(f"\n  applying filter {json.dumps(new_filter)}")
    graph.post(args.set_id, {"filter": new_filter}, context="mutate product set",
               idempotent=True)

    print()
    after = show(args.set_id)

    if json.dumps(after.get("filter"), sort_keys=True) == json.dumps(before.get("filter"), sort_keys=True):
        print("\nFILTER DID NOT CHANGE. The POST returned success and no-opped — this is the "
              "double-encoding trap. Pass an object and let it be encoded once.",
              file=sys.stderr)
        return 1

    print("\nSet mutated. No ad re-review is triggered by a membership change.")
    print("Card renders lag 15-60 min and preview popups cache — verify via API, not previews.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
