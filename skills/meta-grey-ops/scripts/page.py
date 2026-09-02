#!/usr/bin/env python3
"""Page housekeeping that autolaunch SaaS does from a form: avatar, cover, about, website.

    python3 page.py 456 --show
    python3 page.py 456 --avatar avatar.jpg
    python3 page.py 456 --cover cover.jpg
    python3 page.py 456 --about "Short bio" --website https://example.tld
    python3 page.py 456 --list-pages          # every Page the token can advertise from

All writes go through the PAGE token (graph.page_token) and need pages_manage_metadata /
pages_manage_posts on a Page role — a plain user/System User token gets #283 / 200.

Not here, because the API does not expose them: renaming an established Page (name changes go
through a review flow in the UI), creating a Page (UI), username claim. Do those in the
antidetect profile, one action at a time (01).
"""

from __future__ import annotations

import argparse
import json
import sys

import graph

SUMMARY_SCHEMA = "page.result/v1"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page_id", nargs="?")
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--list-pages", action="store_true")
    ap.add_argument("--avatar", help="image file")
    ap.add_argument("--cover", help="image file")
    ap.add_argument("--about")
    ap.add_argument("--website")
    args = ap.parse_args()

    if args.list_pages:
        rows = graph.get("me/accounts", params={"fields": "id,name,category,tasks,fan_count", "limit": 200},
                         context="pages").get("data", [])
        for p in rows:
            print(f"  {p['id']}  {(p.get('name') or '?')[:40]:<40} {p.get('category')}  tasks={p.get('tasks')}")
        print(json.dumps({"schema": SUMMARY_SCHEMA, "action": "list-pages", "pages": rows},
                         ensure_ascii=False))
        return 0
    if not args.page_id:
        sys.exit("page_id required")
    pid = args.page_id

    if args.show or not any([args.avatar, args.cover, args.about, args.website]):
        p = graph.get(pid, params={"fields": "id,name,username,category,about,website,fan_count,"
                                             "picture{url},cover{source},is_published,verification_status"},
                      context="page")
        print(json.dumps(p, indent=2, ensure_ascii=False))
        print(json.dumps({"schema": SUMMARY_SCHEMA, "action": "show", "page_id": pid, "page": p},
                         ensure_ascii=False))
        return 0

    ptoken = graph.page_token(pid)
    if args.avatar:
        with open(args.avatar, "rb") as fh:
            graph.call("POST", f"{pid}/picture", files={"source": (args.avatar, fh)},
                       token_override=ptoken, context="avatar", idempotent=True)
        print("  ✓ avatar")
    if args.cover:
        with open(args.cover, "rb") as fh:
            photo = graph.call("POST", f"{pid}/photos", data={"published": False},
                               files={"source": (args.cover, fh)}, token_override=ptoken,
                               context="cover upload")
        graph.call("POST", pid, data={"cover": photo["id"]}, token_override=ptoken,
                   context="cover set", idempotent=True)
        print("  ✓ cover")
    fields = {k: v for k, v in (("about", args.about), ("website", args.website)) if v}
    if fields:
        graph.call("POST", pid, data=fields, token_override=ptoken, context="page fields", idempotent=True)
        print(f"  ✓ {', '.join(fields)}")
    back = graph.get(pid, params={"fields": "name,about,website,picture{url}"}, context="readback")
    print(json.dumps(back, indent=2, ensure_ascii=False))
    print(json.dumps({
        "schema": SUMMARY_SCHEMA, "action": "set", "page_id": pid,
        "fields_set": sorted(list(fields) + (["avatar"] if args.avatar else [])
                             + (["cover"] if args.cover else [])),
        "page": back,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
