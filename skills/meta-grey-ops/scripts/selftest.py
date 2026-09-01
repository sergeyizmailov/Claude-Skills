#!/usr/bin/env python3
"""Offline regression suite. No network, no token, no account.

    python3 selftest.py

Covers the behaviours that have silently regressed at least once: retry policy on
non-idempotent writes, the unknown-outcome heuristic, credential redaction, per-locale
DLO assembly, the destination diff for every creative kind, and that every shipped spec
in specs/ still builds. Run it after touching graph.py, launch.py or verify.py — a
one-off manual check proved nothing the next edit could not undo.
"""

from __future__ import annotations

import json
import os
import pathlib
import sys

os.environ.setdefault("META_TOKEN", "TESTTOKEN/with+chars")
os.environ.setdefault("META_PROXY", "socks5h://puser:ppass@1.2.3.4:1080")

import graph  # noqa: E402
import launch  # noqa: E402
import verify  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
FAILED: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    print(f"  {'ok  ' if cond else 'FAIL'}  {name}{'' if cond else '  ' + detail}")
    if not cond:
        FAILED.append(name)


class FakeResponse:
    def __init__(self, status: int, body, headers=None):
        self.status_code = status
        self.ok = 200 <= status < 300
        self._body = body
        self.headers = headers or {}
        self.text = body if isinstance(body, str) else json.dumps(body)

    def json(self):
        if isinstance(self._body, str):
            raise ValueError("not json")
        return self._body


class FakeSession:
    """Replays a scripted list of responses/exceptions and counts attempts."""

    def __init__(self, script):
        self.script = list(script)
        self.calls = 0

    def request(self, *_a, **_kw):
        self.calls += 1
        item = self.script[min(self.calls - 1, len(self.script) - 1)]
        if isinstance(item, Exception):
            raise item
        return item


def with_session(script):
    graph._SESSION = FakeSession(script)
    return graph._SESSION


def no_sleep():
    graph.time.sleep = lambda _s: None


# --- transport ------------------------------------------------------------------

def test_transport() -> None:
    print("transport")
    no_sleep()
    boom = ConnectionError("proxy died https://graph.facebook.com/x?access_token=TESTTOKEN%2Fwith%2Bchars")
    ok = FakeResponse(200, {"id": "1"})

    s = with_session([boom] * 9)
    try:
        graph.call("POST", "act_1/campaigns", data={"name": "x"}, retries=4)
        check("create is not retried", False, "no error raised")
    except graph.GraphError as e:
        check("create is not retried", s.calls == 1, f"calls={s.calls}")
        check("create transport error is outcome_unknown", e.outcome_unknown is True)
        check("token redacted in transport error", "TESTTOKEN" not in str(e), str(e))

    s = with_session([boom, boom, ok])
    graph.call("GET", "me", retries=4)
    check("GET retries transport errors", s.calls == 3, f"calls={s.calls}")

    s = with_session([boom, boom, ok])
    graph.call("POST", "1/status", data={"status": "ACTIVE"}, idempotent=True, retries=4)
    check("idempotent write retries", s.calls == 3, f"calls={s.calls}")

    html502 = FakeResponse(502, "<html>Bad Gateway</html>")
    s = with_session([html502, html502, ok])
    graph.call("GET", "me", retries=4)
    check("GET retries a bodyless 5xx", s.calls == 3, f"calls={s.calls}")

    s = with_session([html502] * 9)
    try:
        graph.call("POST", "act_1/campaigns", data={"name": "x"}, retries=2)
        check("create is not retried on a bodyless 5xx", False, "no error raised")
    except graph.GraphError as e:
        check("create is not retried on a bodyless 5xx", s.calls == 1, f"calls={s.calls}")
        check("bodyless 5xx is outcome_unknown", e.outcome_unknown is True)

    rejected = FakeResponse(400, {"error": {"message": "bad", "code": 100,
                                            "error_subcode": 1487390, "type": "OAuthException"}})
    s = with_session([rejected] * 9)
    try:
        graph.call("POST", "act_1/campaigns", data={"name": "x"}, retries=4)
        check("a Graph rejection is not retried", False, "no error raised")
    except graph.GraphError as e:
        check("a Graph rejection is not retried", s.calls == 1, f"calls={s.calls}")
        check("a Graph rejection is a KNOWN outcome", e.outcome_unknown is False)
        check("subcode is parsed", e.subcode == 1487390)


def test_encoding() -> None:
    print("encoding")
    check("bool → true/false", graph._encode(True) == "true" and graph._encode(False) == "false")
    check("dict → compact json", graph._encode({"a": [1, 2]}) == '{"a":[1,2]}')
    check("str passes through", graph._encode("x") == "x")

    txt = graph.redact("access_token=TESTTOKEN/with+chars enc=TESTTOKEN%2Fwith%2Bchars "
                       "proxy=socks5h://puser:ppass@1.2.3.4")
    check("raw token redacted", "TESTTOKEN/with+chars" not in txt, txt)
    check("url-encoded token redacted", "TESTTOKEN%2F" not in txt, txt)
    check("proxy creds redacted", "ppass" not in txt, txt)


# --- builders -------------------------------------------------------------------

def test_specs() -> None:
    print("specs")
    for path in sorted((HERE / "specs").glob("*.json")):
        try:
            spec = launch.load_spec(str(path))
            for aset in spec["adsets"]:
                launch.build_targeting(aset)
                launch.build_attribution(aset)
                for ad in aset["ads"]:
                    launch.build_creative(spec, ad, "17841400000000000")
            check(f"{path.name} builds", True)
        except SystemExit as e:
            check(f"{path.name} builds", False, str(e))


def test_attribution() -> None:
    print("attribution")
    got = launch.build_attribution({"attribution": {"click_days": 1, "view_days": 1}})
    keys = {k for entry in got for k in entry}
    check("emits window_days, never event_window_days",
          "window_days" in keys and "event_window_days" not in keys, str(got))


def test_dlo() -> None:
    print("dlo")
    spec = launch.load_spec(str(HERE / "specs" / "example-dlo.json"))
    c = spec["adsets"][0]["ads"][0]["creative"]
    feed = launch.build_dlo_feed(c)
    rules = feed["asset_customization_rules"]
    check("at least two rules", len(rules) >= 2)
    check("exactly one default", sum(1 for r in rules if r.get("is_default")) == 1)
    label_key = "image_label" if feed["ad_formats"] == ["SINGLE_IMAGE"] else "video_label"
    check("every rule carries its media label", all(label_key in r for r in rules))
    check("descriptions present for every locale",
          len(feed["descriptions"]) == len(rules) and all(x["text"] for x in feed["descriptions"]))
    check("one link_url per locale", len(feed["link_urls"]) == len(rules))
    check("locale ids are ints",
          all(isinstance(x, int) for r in rules for x in r["customization_spec"]["locales"]))

    try:
        launch.build_dlo_feed({**c, "ad_format": "CAROUSEL"})
        check("CAROUSEL rejected", False, "accepted")
    except SystemExit:
        check("CAROUSEL rejected", True)


def test_catalog_template_url() -> None:
    print("catalog")
    spec = launch.load_spec(str(HERE / "specs" / "example-catalog-collection-tr.json"))
    ad = spec["adsets"][0]["ads"][0]
    payload = launch.build_creative(spec, ad, None)
    want = ad["creative"].get("template_url")
    check("spec ships a template_url", bool(want))
    check("template_url_spec is emitted",
          ((payload.get("template_url_spec") or {}).get("web") or {}).get("url") == want,
          str(payload.get("template_url_spec")))


# --- verify ---------------------------------------------------------------------

def test_destination() -> None:
    print("verify.destination")

    d = verify.Diff()
    verify.check_destination(
        d,
        {"kind": "link_video", "link": "https://a.tld/"},
        {"object_story_spec": {"video_data": {"link": "https://a.tld/"}}},
    )
    check("link_video match passes", d.bad == 0, f"bad={d.bad}")

    d = verify.Diff()
    verify.check_destination(
        d,
        {"kind": "link_video", "link": "https://a.tld/"},
        {"object_story_spec": {"video_data": {"link": "https://WRONG.tld/"}}},
    )
    check("wrong destination fails", d.bad == 1, f"bad={d.bad}")

    d = verify.Diff()
    locales = [{"link": "https://white.tld/"}, {"link": "https://money.tld/"}]
    verify.check_destination(
        d,
        {"kind": "dlo", "locales": locales},
        {"object_story_spec": {},
         "asset_feed_spec": {"link_urls": [{"website_url": "https://white.tld/"},
                                           {"website_url": "https://money.tld/"}]}},
    )
    check("dlo with matching link_urls passes", d.bad == 0, f"bad={d.bad}")

    d = verify.Diff()
    verify.check_destination(
        d,
        {"kind": "dlo", "locales": locales},
        {"object_story_spec": {}, "asset_feed_spec": {"link_urls": [
            {"website_url": "https://white.tld/"}, {"website_url": "https://TYPO.tld/"}]}},
    )
    check("dlo with a wrong locale link fails", d.bad == 1, f"bad={d.bad}")

    d = verify.Diff()
    verify.check_destination(d, {"kind": "dlo", "locales": locales},
                             {"object_story_spec": {}, "asset_feed_spec": {}})
    check("dlo with no link_urls fails exactly once", d.bad == 1, f"bad={d.bad}")

    d = verify.Diff()
    verify.check_destination(d, {"kind": "dlo"},
                             {"object_story_spec": {}, "asset_feed_spec": {}})
    check("dlo with neither spec locales nor link_urls fails once", d.bad == 1, f"bad={d.bad}")

    # Spec-less run: the kind is recovered from the built creative, so a DLO ad is not
    # mistaken for a link ad with a missing destination.
    d = verify.Diff()
    verify.check_destination(
        d, None,
        {"object_story_spec": {},
         "asset_feed_spec": {"link_urls": [{"website_url": "https://white.tld/"}]}},
    )
    check("no --spec: dlo is recognised and not failed", d.bad == 0, f"bad={d.bad}")

    d = verify.Diff()
    verify.check_destination(d, None, {"object_story_spec": {}, "asset_feed_spec": {}})
    check("no --spec: nothing is ever failed", d.bad == 0, f"bad={d.bad}")

    d = verify.Diff()
    verify.check_destination(
        d, {"kind": "link_video", "link": "https://a.tld/"},
        {"object_story_spec": {"video_data": {}}},
    )
    check("spec'd link with no destination fails exactly once", d.bad == 1, f"bad={d.bad}")

    d = verify.Diff()
    verify.check_destination(
        d,
        {"kind": "catalog_collection", "link": "https://shop.tld/",
         "template_url": "https://go.tld/?sub={{product.retailer_id}}"},
        {"object_story_spec": {"template_data": {"link": "https://shop.tld/"}},
         "template_url_spec": {"web": {"url": "https://go.tld/?sub={{product.retailer_id}}"}}},
    )
    check("catalog match passes", d.bad == 0, f"bad={d.bad}")

    d = verify.Diff()
    verify.check_destination(
        d,
        {"kind": "catalog_collection", "link": "https://shop.tld/",
         "template_url": "https://go.tld/?sub=X"},
        {"object_story_spec": {"template_data": {"link": "https://shop.tld/"}}},
    )
    check("dropped template_url_spec fails", d.bad == 1, f"bad={d.bad}")


def test_probe_is_retryable() -> None:
    """probe.py is diagnostic: none of its writes create anything a repeat could
    duplicate, so every one of them must survive a dropped connection. A one-shot POST
    here reports 'no write access' on an account that has it — the single most expensive
    false negative in the runbook, because it stops a launch at step 1."""
    print("probe")
    import ast

    src = (HERE / "probe.py").read_text(encoding="utf-8")
    bad = []
    for node in ast.walk(ast.parse(src)):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        if not (isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name)
                and fn.value.id == "graph" and fn.attr in ("post", "call")):
            continue
        args = {kw.arg for kw in node.keywords}
        method = next((a.value for a in node.args if isinstance(a, ast.Constant)), None)
        if fn.attr == "call" and method == "GET":
            continue
        if "idempotent" not in args:
            bad.append(node.lineno)
    check("every probe.py write is marked idempotent", not bad, f"lines {bad}")


def test_equivalence() -> None:
    print("verify.equivalence")
    d = verify.Diff()
    d.check("tz", "2026-09-02T07:00:00+03:00", "2026-09-02T04:00:00+0000")
    check("same instant, different offset → match", d.bad == 0, f"bad={d.bad}")

    d = verify.Diff()
    d.check("subset", {"countries": ["TR"]}, {"countries": ["TR"], "location_types": ["home"]})
    check("Graph-enriched dict → match", d.bad == 0, f"bad={d.bad}")

    d = verify.Diff()
    d.check("order", ["a", "b"], ["b", "a"])
    check("list order ignored", d.bad == 0, f"bad={d.bad}")

    d = verify.Diff()
    d.check("real diff", {"countries": ["TR"]}, {"countries": ["DE"]})
    check("a real difference still fails", d.bad == 1, f"bad={d.bad}")


def main() -> int:
    for fn in (test_transport, test_encoding, test_specs, test_attribution, test_dlo,
               test_catalog_template_url, test_destination, test_probe_is_retryable,
               test_equivalence):
        fn()
    print()
    if FAILED:
        print(f"{len(FAILED)} failure(s): {FAILED}", file=sys.stderr)
        return 1
    print("all green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
