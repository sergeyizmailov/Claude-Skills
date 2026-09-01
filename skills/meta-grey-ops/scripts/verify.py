#!/usr/bin/env python3
"""Read every created object back and diff it against the spec that built it.

    python3 verify.py --state .meta-launch/<run_id>.json --spec specs/<spec>.json

A successful mutation is not proof the object holds what you sent: budgets land in
minor units, targeting gets replaced wholesale, and enum defaults fill silently. Run
this before activate.py. Exit 1 on any mismatch or any non-deliverable effective status.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime

import graph
import launch

CAMPAIGN_FIELDS = (
    "id,name,objective,status,effective_status,daily_budget,lifetime_budget,"
    "bid_strategy,buying_type,special_ad_categories,is_adset_budget_sharing_enabled"
)
ADSET_FIELDS = (
    "id,name,status,effective_status,optimization_goal,billing_event,bid_strategy,"
    "daily_budget,start_time,end_time,promoted_object,attribution_spec,"
    "targeting,issues_info"
)
AD_FIELDS = (
    "id,name,status,effective_status,issues_info,"
    "creative{id,object_story_spec,asset_feed_spec,template_url_spec,url_tags}"
)

# effective_status values that mean "activating will not fix this".
BLOCKING = {"DISAPPROVED", "WITH_ISSUES", "DELETED", "ARCHIVED", "ADSET_DELETED",
            "CAMPAIGN_DELETED", "DISABLED"}
# Expected on a freshly built PAUSED tree — reported, never counted as a failure.
EXPECTED = {"PAUSED", "ADSET_PAUSED", "CAMPAIGN_PAUSED", "PENDING_REVIEW", "PREAPPROVED"}


def _as_instant(v):
    """ISO8601 → aware datetime, or None if it is not a timestamp."""
    if not isinstance(v, str):
        return None
    txt = v.strip()
    # Graph returns +0000 / -0700; Python wants +00:00 before 3.11 and accepts both after.
    m = re.match(r"^(.*[+-]\d{2})(\d{2})$", txt)
    if m:
        txt = f"{m.group(1)}:{m.group(2)}"
    try:
        d = datetime.fromisoformat(txt)
    except ValueError:
        return None
    return d if d.tzinfo else None


def _equivalent(expected, actual) -> bool:
    """True when `actual` satisfies everything `expected` asserts."""
    e_dt, a_dt = _as_instant(expected), _as_instant(actual)
    if e_dt and a_dt:
        return e_dt == a_dt
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        # Subset semantics: Graph adds keys of its own; only what the spec set matters.
        return all(_equivalent(v, actual.get(k)) for k, v in expected.items())
    if isinstance(expected, list):
        if not isinstance(actual, list) or len(expected) != len(actual):
            return False
        remaining = list(actual)
        for item in expected:
            match = next((x for x in remaining if _equivalent(item, x)), None)
            if match is None:
                return False
            remaining.remove(match)
        return True
    return str(expected) == str(actual)


class Diff:
    def __init__(self) -> None:
        self.bad = 0

    def check(self, label: str, expected, actual) -> None:
        """Compare semantically, not textually.

        Two things made naive str() comparison produce false MISMATCH on correct builds:
        Graph normalises `start_time` to its own offset (a +03:00 spec comes back as
        +0000 for the same instant), and it returns `targeting` enriched with keys the
        spec never sent. So: timestamps compare as instants, dicts compare only on the
        keys the spec actually asserted, and lists compare order-insensitively."""
        if expected is None:
            return
        ok = _equivalent(expected, actual)
        if not ok:
            self.bad += 1
        mark = "ok  " if ok else "MISMATCH"
        print(f"    {mark}  {label}: expected {expected!r}, got {actual!r}")

    def status(self, label: str, value) -> None:
        """Report an effective_status. Blocking ones fail the run; anything neither
        blocking nor expected-on-a-paused-tree is surfaced for a human to look at."""
        if value in BLOCKING:
            flag, self.bad = "   <-- BLOCKING, activating will not fix it", self.bad + 1
        elif value in EXPECTED:
            flag = ""
        else:
            flag = "   <-- unexpected on a paused build, check it"
        print(f"    ..    {label}: {value}{flag}")

    def note(self, label: str, value) -> None:
        print(f"    ..    {label}: {value}")


def _kind_from_creative(story: dict, feed: dict, creative: dict) -> str:
    """Recover the creative kind from what Graph returned, for spec-less runs."""
    if feed.get("link_urls") or feed.get("asset_customization_rules"):
        return "dlo"
    if creative.get("template_url_spec") or story.get("template_data"):
        return "catalog"
    return "link"


def check_destination(d: Diff, want_c: dict | None, creative: dict) -> None:
    """Diff where the ad actually sends traffic.

    Every creative kind stores the destination somewhere else, and reading the wrong
    place fails a correct build:

      link_image / link_video   object_story_spec.{link_data,video_data}.link
      dlo                       asset_feed_spec.link_urls[].website_url — ONE PER LOCALE,
                                and object_story_spec carries no link at all
      catalog_*                 object_story_spec.template_data.link for the storefront,
                                plus template_url_spec.web.url for the per-card click URL

    `want_c` is None when verify runs without --spec: then this reports, never fails —
    including the kind, which is read off the built creative rather than assumed, or a
    spec-less run flags every DLO ad as broken.

    Nothing here is counted twice: when `d.check` had a spec value to compare against, it
    already recorded the failure, so the explanatory line below it is printed only.
    """
    story = creative.get("object_story_spec") or {}
    feed = creative.get("asset_feed_spec") or {}
    strict = want_c is not None
    want_c = want_c or {}
    kind = want_c.get("kind") or _kind_from_creative(story, feed, creative)

    if kind == "dlo":
        got = [u.get("website_url") for u in (feed.get("link_urls") or [])]
        want = [loc.get("link") for loc in want_c.get("locales") or []] or None
        d.check("        destination (per locale)", want, got)
        if want is None:
            print(f"        destination (per locale) {got or 'NONE'}")
        if not got:
            print("        MISSING  asset_feed_spec carries no link_urls")
            if strict and want is None:
                d.bad += 1
        return

    node = story.get("link_data") or story.get("video_data") or story.get("template_data") or {}
    dest = node.get("link") or ((node.get("call_to_action") or {}).get("value") or {}).get("link")
    want = want_c.get("link")
    d.check("        destination", want, dest)
    if want is None:
        print(f"        destination {dest}")
    if not dest:
        # A missing destination is a defect, not a note: it spends money into nothing.
        print("        MISSING  no destination resolved from the creative")
        if strict and want is None:
            d.bad += 1

    if kind.startswith("catalog"):
        got_t = ((creative.get("template_url_spec") or {}).get("web") or {}).get("url")
        want_t = want_c.get("template_url")
        d.check("        template_url_spec.web.url", want_t, got_t)
        if not got_t and want_t is None:
            print("        WARN  no template_url_spec — catalog card clicks resolve their "
                  "URL from the feed and carry no subids")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--state", required=True)
    ap.add_argument("--spec", help="Diff against the spec that built this run")
    args = ap.parse_args()

    with open(args.state, encoding="utf-8") as fh:
        state = json.load(fh)
    objects = state["objects"]
    spec = launch.load_spec(args.spec) if args.spec else None
    d = Diff()

    campaign_id = objects.get("campaign")
    if not campaign_id:
        sys.exit("state file holds no campaign id — nothing to verify")

    camp = graph.get(campaign_id, params={"fields": CAMPAIGN_FIELDS}, context="verify campaign")
    print(f"campaign {campaign_id}  {camp.get('name')}")
    if spec:
        c = spec["campaign"]
        d.check("objective", c["objective"], camp.get("objective"))
        d.check("daily_budget (minor)", c["daily_budget_minor"], camp.get("daily_budget"))
        d.check("bid_strategy", c.get("bid_strategy", "LOWEST_COST_WITHOUT_CAP"), camp.get("bid_strategy"))
        d.check("special_ad_categories", c["special_ad_categories"], camp.get("special_ad_categories"))
    d.check("status", "PAUSED", camp.get("status"))
    d.status("effective_status", camp.get("effective_status"))

    i = 0
    while f"adset[{i}]" in objects:
        adset_id = objects[f"adset[{i}]"]
        a = graph.get(adset_id, params={"fields": ADSET_FIELDS}, context=f"verify adset {i}")
        print(f"\n  adset[{i}] {adset_id}  {a.get('name')}")
        if spec:
            s = spec["adsets"][i]
            d.check("optimization_goal", s["optimization_goal"], a.get("optimization_goal"))
            d.check("start_time", s["start_time"], a.get("start_time"))
            if s.get("custom_event_type"):
                d.check("promoted_object.custom_event_type",
                        s["custom_event_type"],
                        (a.get("promoted_object") or {}).get("custom_event_type"))
            expected_t = launch.build_targeting(s)
            actual_t = a.get("targeting") or {}
            for key in ("geo_locations", "age_min", "age_max", "targeting_automation"):
                if key in expected_t:
                    d.check(f"targeting.{key}", expected_t[key], actual_t.get(key))
        if a.get("daily_budget"):
            print(f"    MISMATCH  ad set carries its own budget ({a['daily_budget']}) under CBO")
            d.bad += 1
        # Reading this back is not cosmetic: an unknown key inside attribution_spec is
        # ignored by Graph, so a wrong field name looks like a success and leaves the
        # account default in place.
        if spec and s.get("attribution"):
            want = launch.build_attribution(s)
            got = a.get("attribution_spec")
            got_norm = [{"event_type": e.get("event_type"), "window_days": e.get("window_days")}
                        for e in (got or [])]
            d.check("attribution_spec", want, got_norm)
        else:
            d.note("attribution_spec", a.get("attribution_spec"))
        d.status("effective_status", a.get("effective_status"))
        if a.get("issues_info"):
            print(f"    ISSUES  {a['issues_info']}")
            d.bad += 1

        j = 0
        while f"ad[{i}.{j}]" in objects:
            ad_id = objects[f"ad[{i}.{j}]"]
            ad = graph.get(ad_id, params={"fields": AD_FIELDS}, context=f"verify ad {i}.{j}")
            creative = ad.get("creative") or {}
            story = creative.get("object_story_spec") or {}
            print(f"      ad[{i}.{j}] {ad_id}  {ad.get('name')}")
            print(f"        identity page={story.get('page_id')} ig={story.get('instagram_user_id')}")
            if not story.get("instagram_user_id"):
                print("        WARN  no instagram_user_id — any IG placement will fail 1772103")
            # Printing it was not verification. The destination is the one field where a
            # wrong value spends real money into the wrong funnel, so diff it.
            want_c = (spec["adsets"][i]["ads"][j].get("creative") or {}) if spec else None
            check_destination(d, want_c, creative)
            print(f"        url_tags {creative.get('url_tags')}")
            d.status("        effective_status", ad.get("effective_status"))
            if ad.get("issues_info"):
                print(f"        ISSUES  {ad['issues_info']}")
                d.bad += 1
            j += 1
        i += 1

    if d.bad:
        print(f"\n{d.bad} problem(s). Do NOT activate.", file=sys.stderr)
        return 1
    print("\nEverything matches the spec and nothing is blocked. "
          "Preview each placement in Ads Manager, then activate.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
