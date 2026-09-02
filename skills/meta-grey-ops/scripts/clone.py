#!/usr/bin/env python3
"""Duplicate campaigns / ad sets / ads INSIDE an account via the /copies edge.

    python3 clone.py campaign 1234 --times 3 --prefix "S2|" --start 2026-09-04T07:00:00+03:00
    python3 clone.py adset 5678 --into-campaign 9999 --times 2
    python3 clone.py ad 4242 --into-adset 8888 --suffix "-v2"
    python3 clone.py campaign 1234 --dry-run

Cross-account "duplication" is NOT this: hashes, pixels and pages are account-scoped, so a
copy to another account is a rebuild — use bulk.py with the same template. This script is
the autolaunch-SaaS "duplicate ×N" button for the same account.

How it copies (live-verified 2026-09-02, v26.0):
  · `deep_copy=true` is capped — "the total number of ads, ad sets and campaigns copied at
    once must be less than 3" (code 100 / subcode 1885194); on a just-created tree it fails
    with a bare code 1. So a campaign is copied LEVEL BY LEVEL: shallow campaign copy → each
    ad set shallow-copied into it (`campaign_id`) → each ad copied into the new ad set
    (`adset_id`). Same result, no cap.
  · every copy lands PAUSED (status_option=PAUSED) — activation is activate.py's job
  · a copied ad set keeps the source attribution_spec (immutable, 1504040); pass --start to
    refresh start_time on every copied ad set so the clone does not start in dead hours
  · rename via rename_options so the tracker split stays readable (03 → Naming); Meta
    appends " — Копия"/" – Copy" itself when NO_RENAME is used
  · /copies is not retried on transport failure (a copy may have applied); every id is
    printed and written to --json so nothing is lost
  · objects still IN_PROCESS (seconds after create) reject copies — wait for PAUSED
  · response keys seen live 2026-09-02: `copied_campaign_id` (campaign), `copied_adset_id`
    (ad set); the ad-level key `copied_ad_id` and the `ad_object_ids` fallback are from the
    reference, not yet observed (ad copies hit the rate limit that day)
"""

from __future__ import annotations

import argparse
import json
import sys

import graph


def rename_options(args, n: int) -> dict:
    if args.prefix or args.suffix:
        return {"rename_strategy": "ONLY_TOP_LEVEL_RENAME",
                "rename_prefix": (args.prefix or "").replace("{n}", str(n)),
                "rename_suffix": (args.suffix or "").replace("{n}", str(n))}
    return {"rename_strategy": "NO_RENAME"}


def copy_obj(obj_id: str, payload: dict, dry: bool, label: str) -> str | None:
    payload = dict(payload, status_option="PAUSED", deep_copy=False)
    if dry:
        print(f"  would POST /{obj_id}/copies {json.dumps(payload, ensure_ascii=False)}")
        return None
    r = graph.post(f"{obj_id}/copies", payload, context=f"copy {label} {obj_id}")
    new_id = r.get("copied_campaign_id") or r.get("copied_adset_id") or r.get("copied_ad_id")
    if not new_id:
        ids = r.get("ad_object_ids") or []
        new_id = next((x.get("copied_id") for x in ids if x.get("source_id") == obj_id), None)
    if not new_id:
        raise SystemExit(f"copy of {obj_id} returned no id: {json.dumps(r)[:300]}")
    return new_id


def children(edge: str, obj_id: str) -> list[dict]:
    rows, path, params = [], f"{obj_id}/{edge}", {"fields": "id,name,status,effective_status", "limit": 200}
    while True:
        resp = graph.get(path, params=params, context=edge)
        rows.extend(resp.get("data", []))
        nxt = (resp.get("paging") or {}).get("next")
        if not nxt:
            return rows
        path, params = nxt, {}


def copy_campaign_tree(cid: str, args, n: int, out: dict) -> None:
    new_c = copy_obj(cid, {"rename_options": rename_options(args, n)}, args.dry_run, "campaign")
    out["campaign"] = new_c
    print(f"  + campaign {cid} → {new_c or '<dry>'}")
    for aset in children("adsets", cid):
        payload = {"campaign_id": new_c or "<new-campaign>", "rename_options": {"rename_strategy": "NO_RENAME"}}
        if args.start:
            payload["start_time"] = args.start
        if args.end:
            payload["end_time"] = args.end
        new_a = copy_obj(aset["id"], payload, args.dry_run, "adset")
        out.setdefault("adsets", []).append(new_a)
        print(f"    + adset {aset['id']} {aset.get('name', '')[:40]} → {new_a or '<dry>'}")
        for ad in children("ads", aset["id"]):
            new_ad = copy_obj(ad["id"], {"adset_id": new_a or "<new-adset>",
                                         "rename_options": {"rename_strategy": "NO_RENAME"}},
                              args.dry_run, "ad")
            out.setdefault("ads", []).append(new_ad)
            print(f"      + ad {ad['id']} {ad.get('name', '')[:40]} → {new_ad or '<dry>'}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", choices=["campaign", "adset", "ad"])
    ap.add_argument("id")
    ap.add_argument("--times", type=int, default=1)
    ap.add_argument("--prefix", help="rename prefix on the top object; {n} = copy index")
    ap.add_argument("--suffix", help="rename suffix on the top object; {n} = copy index")
    ap.add_argument("--into-campaign", help="adset copies: target campaign id")
    ap.add_argument("--into-adset", help="ad copies: target ad set id")
    ap.add_argument("--start", help="ISO8601 start_time for copied ad sets (never 00:00 for conversions)")
    ap.add_argument("--end", help="ISO8601 end_time for copied ad sets")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--json", help="write all new ids here")
    args = ap.parse_args()

    if args.kind != "ad" and not args.start and not args.dry_run:
        print("  ! no --start: copies inherit the source start_time, which may be in the past → "
              "they would begin immediately on activation. Pass --start.", file=sys.stderr)

    results = []
    for n in range(1, args.times + 1):
        out: dict = {}
        try:
            if args.kind == "campaign":
                copy_campaign_tree(args.id, args, n, out)
            elif args.kind == "adset":
                payload = {"rename_options": rename_options(args, n)}
                if args.into_campaign:
                    payload["campaign_id"] = args.into_campaign
                if args.start:
                    payload["start_time"] = args.start
                new_a = copy_obj(args.id, payload, args.dry_run, "adset")
                out["adset"] = new_a
                print(f"  + adset {args.id} → {new_a or '<dry>'}")
                for ad in children("ads", args.id):
                    new_ad = copy_obj(ad["id"], {"adset_id": new_a or "<new-adset>",
                                                 "rename_options": {"rename_strategy": "NO_RENAME"}},
                                      args.dry_run, "ad")
                    out.setdefault("ads", []).append(new_ad)
                    print(f"    + ad {ad['id']} → {new_ad or '<dry>'}")
            else:
                payload = {"rename_options": rename_options(args, n)}
                if args.into_adset:
                    payload["adset_id"] = args.into_adset
                out["ad"] = copy_obj(args.id, payload, args.dry_run, "ad")
                print(f"  + ad {args.id} → {out['ad'] or '<dry>'}")
        except graph.GraphError as e:
            print(f"  x copy {n} stopped: {e}", file=sys.stderr)
            if e.code == 1 or e.subcode == 99:
                print("    code 1 / sub 99 here has meant: source still IN_PROCESS (just created) — "
                      "wait a minute and retry", file=sys.stderr)
            results.append(out)
            break
        results.append(out)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            fh.write(graph.redact(json.dumps(results, indent=2)))
    if not args.dry_run:
        print("\nAll copies PAUSED. Copies have no spec, so activate.py (which needs a spec'd verify "
              "receipt) does not apply: check them in Ads Manager, then edit.py --ids <ids> --status "
              "ACTIVE --confirm ACTIVATE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
