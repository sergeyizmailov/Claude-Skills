"""Graph API transport: pinned version, forced proxy, rate-limit backoff, typed errors.

Every other script in this directory calls Graph through this module. Nothing here
knows about campaigns — it only makes requests survivable and errors legible.

Credentials come from the environment, never from argv (argv lands in shell history
and process lists):

    META_TOKEN        System User or long-lived user token. Required.
    META_PROXY        socks5h://user:pass@host:port  (see 01 — socks5:// breaks TLS)
    META_API_VERSION  Override the pinned version below.
    META_ALLOW_NO_PROXY=1  Escape hatch for a server-side System User token only.
"""

from __future__ import annotations

import json
import os
import random
import re
import sys
import time
from urllib.parse import quote
from typing import Any

def _requests():
    """Imported lazily so --help works on a box that has not installed it yet."""
    try:
        import requests  # noqa: PLC0415
    except ImportError:  # pragma: no cover
        sys.exit("Missing dependency. Run:  pip install 'requests[socks]'")
    return requests


# Pinned deliberately. An unpinned call silently changes behavior when Meta ships a
# version; re-pin only after re-reading meta-ads/00 §4.1.
API_VERSION = os.environ.get("META_API_VERSION", "v26.0")
BASE = f"https://graph.facebook.com/{API_VERSION}"

# Header budget at which we stop and wait rather than earn a block.
USAGE_PAUSE_PCT = 85.0


class GraphError(Exception):
    """A Graph API error, parsed into the fields worth branching on.

    Branch on (code, subcode) — the stable machine key. `user_msg` is for humans and
    logs only: Meta rewrites and localizes those strings. See meta-ads/14.
    """

    def __init__(self, status: int, payload: dict[str, Any], context: str = ""):
        err = (payload or {}).get("error", {}) or {}
        self.status = status
        self.code = err.get("code")
        self.subcode = err.get("error_subcode")
        self.type = err.get("type")
        self.message = err.get("message", "")
        self.user_title = err.get("error_user_title", "")
        self.user_msg = err.get("error_user_msg", "")
        self.is_transient = bool(err.get("is_transient", False))
        self.trace = err.get("fbtrace_id", "")
        self.blame_field = (err.get("error_data") or {}).get("blame_field_specs")
        self.context = context
        # True when we cannot know whether the server actually applied the request:
        # the transport failed (status 0), or the server answered without a Graph error
        # envelope (an HTML 5xx from a proxy or edge). Graph answering with a real error
        # code IS knowledge — it means the call was rejected and nothing was created.
        self.outcome_unknown = self.status == 0 or (
            self.status >= 500 and self.type is None and self.code in (None, -1)
        )
        super().__init__(str(self))

    def __str__(self) -> str:
        head = f"[{self.context}] " if self.context else ""
        key = f"code={self.code} subcode={self.subcode}"
        detail = self.user_msg or self.message
        blame = f" blame={self.blame_field}" if self.blame_field else ""
        return f"{head}{key}: {detail}{blame} (trace {self.trace})"

    def as_dict(self) -> dict[str, Any]:
        return {
            "context": self.context,
            "status": self.status,
            "code": self.code,
            "subcode": self.subcode,
            "type": self.type,
            "message": self.message,
            "user_title": self.user_title,
            "user_msg": self.user_msg,
            "is_transient": self.is_transient,
            "blame_field_specs": self.blame_field,
            "fbtrace_id": self.trace,
        }


def token() -> str:
    t = os.environ.get("META_TOKEN", "").strip()
    if not t:
        sys.exit("META_TOKEN is not set. Export it; never pass a token on the command line.")
    return t


def redact(text: str) -> str:
    """Strip every credential from anything about to be printed or written to disk.

    Covers the raw token, its URL-encoded form (requests percent-encodes it into the
    exception's request.url), and the proxy's user:pass — which rides in META_PROXY and
    lands in connection-error text."""
    t = os.environ.get("META_TOKEN", "")
    if t:
        text = text.replace(t, "<TOKEN>").replace(quote(t, safe=""), "<TOKEN>")
    proxy = os.environ.get("META_PROXY", "")
    m = re.search(r"://([^/@]+)@", proxy)
    if m:
        creds = m.group(1)
        text = text.replace(creds, "<PROXY_CREDS>")
        user = creds.split(":")[0]
        if len(user) > 2:
            text = text.replace(user, "<PROXY_USER>")
    return text


def _session():
    s = _requests().Session()
    proxy = os.environ.get("META_PROXY", "").strip()
    if proxy:
        if proxy.startswith("socks5://"):
            sys.exit(
                "META_PROXY uses socks5:// — DNS then resolves locally and TLS to "
                "graph.facebook.com dies with UNEXPECTED_EOF_WHILE_READING. Use socks5h://."
            )
        s.proxies = {"http": proxy, "https": proxy}
    elif os.environ.get("META_ALLOW_NO_PROXY") != "1":
        sys.exit(
            "META_PROXY is not set. A user-token persona must exit the same IP as its "
            "antidetect profile (01). For a server-side System User token, set "
            "META_ALLOW_NO_PROXY=1 deliberately."
        )
    s.headers["User-Agent"] = "meta-grey-ops/graph.py"
    return s


_SESSION = None


def session():
    global _SESSION
    if _SESSION is None:
        _SESSION = _session()
    return _SESSION


def _worst_usage(headers) -> float:
    """Highest utilisation percentage across every usage header Meta returned."""
    worst = 0.0
    for name in ("x-app-usage", "x-ad-account-usage", "x-business-use-case-usage"):
        raw = headers.get(name)
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except (ValueError, TypeError):
            continue
        buckets = []
        if isinstance(data, dict):
            # x-app-usage is flat; x-business-use-case-usage is keyed by business id.
            for v in data.values():
                if isinstance(v, list):
                    buckets.extend(v)
            if not buckets:
                buckets = [data]
        for b in buckets:
            if not isinstance(b, dict):
                continue
            for k, v in b.items():
                if k.endswith(("_pct", "_util_pct")) or k in (
                    "call_count",
                    "total_cputime",
                    "total_time",
                ):
                    try:
                        worst = max(worst, float(v))
                    except (TypeError, ValueError):
                        pass
    return worst


def _regain_seconds(headers) -> int:
    raw = headers.get("x-business-use-case-usage")
    if not raw:
        return 0
    try:
        data = json.loads(raw)
    except (ValueError, TypeError):
        return 0
    worst = 0
    for buckets in data.values():
        if not isinstance(buckets, list):
            continue
        for b in buckets:
            try:
                worst = max(worst, int(b.get("estimated_time_to_regain_access", 0)))
            except (TypeError, ValueError, AttributeError):
                pass
    return worst * 60


def _encode(v: Any) -> Any:
    """Graph takes complex values as JSON strings — in the QUERY STRING as well as the
    body. `time_range` and `action_attribution_windows` on the Insights edge are query
    params: left as Python objects they arrive as `{'since': ...}` with single quotes and
    are ignored or rejected, so the call silently reports the wrong window.

    Booleans need it too: requests renders a bare Python bool as "True"/"False", which
    Graph does not accept as a boolean. json.dumps gives true/false.
    """
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (dict, list)):
        return json.dumps(v, separators=(",", ":"))
    return v


def call(
    method: str,
    path: str,
    params: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    files: dict[str, Any] | None = None,
    token_override: str | None = None,
    context: str = "",
    retries: int = 4,
    idempotent: bool | None = None,
) -> Any:
    """One Graph call with rate-limit backoff. Raises GraphError on a hard failure.

    Nested values in `data` are JSON-encoded, because Graph takes complex fields as
    JSON strings in a form body. The rule is ENCODE EXACTLY ONCE. This encoder already
    satisfies it either way — dicts and lists are stringified once, strings pass through
    untouched — so pass whichever you have. The trap lives one layer up: stringify a
    value yourself and then hand it to something that stringifies everything (the
    business SDK does), and it arrives double-encoded. A double-encoded product-set
    `filter` silently no-ops: HTTP 200, set id returned, filter unchanged (04).
    """
    # A transport failure on a CREATE is not safe to retry: the request may have been
    # applied before the connection dropped, so a retry duplicates the object. Reads and
    # explicit idempotent writes retry freely. Errors Graph *answered* with are always
    # retryable in principle — a rejected call created nothing — so this flag only gates
    # the transport-error path.
    if idempotent is None:
        idempotent = method.upper() == "GET"

    url = path if path.startswith("http") else f"{BASE}/{path.lstrip('/')}"
    params = {k: _encode(v) for k, v in (params or {}).items() if v is not None}
    params["access_token"] = token_override or token()

    body = None
    if data is not None:
        body = {k: _encode(v) for k, v in data.items() if v is not None}

    delay = 2.0
    for attempt in range(retries + 1):
        try:
            resp = session().request(
                method.upper(), url, params=params, data=body, files=files, timeout=180
            )
        except Exception as exc:  # noqa: BLE001 - transport errors embed the tokenised URL
            # requests puts request.url — access_token included — into the exception
            # string, so it is redacted before it can reach stderr or a traceback.
            # A dropped proxy connection or a read timeout is exactly what retries exist
            # for: back off and try again, and only surface it once they are exhausted.
            err = GraphError(
                0, {"error": {"message": redact(str(exc)), "code": -1, "is_transient": True}},
                context,
            )
            if not idempotent:
                # Do not retry. The caller records this as an unknown outcome and stops.
                raise err from None
            if attempt < retries:
                wait = delay + random.uniform(0, 1)
                print(f"  ! transport error — retrying in {wait:.1f}s ({err.message[:120]})",
                      file=sys.stderr)
                time.sleep(wait)
                delay = min(delay * 2, 60)
                continue
            raise err from None

        usage = _worst_usage(resp.headers)
        if usage >= USAGE_PAUSE_PCT:
            wait = 60 * (usage / 100.0)
            print(f"  ! usage at {usage:.0f}% — sleeping {wait:.0f}s", file=sys.stderr)
            time.sleep(wait)

        try:
            payload = resp.json()
        except ValueError:
            payload = {"error": {"message": resp.text[:500], "code": -1}}

        if resp.ok and "error" not in payload:
            return payload

        err = GraphError(resp.status_code, payload, context)

        throttled = err.code in (4, 17, 32, 613) or (
            isinstance(err.code, int) and 80000 <= err.code <= 80999
        )
        if throttled and attempt < retries:
            wait = _regain_seconds(resp.headers) or delay
            print(f"  ! throttled ({err.code}) — sleeping {wait}s", file=sys.stderr)
            time.sleep(wait)
            delay = min(delay * 2, 300)
            continue

        # A 5xx with no Graph error envelope (an HTML page from the proxy or Meta's edge)
        # is the same class of event as a dropped connection: the request may or may not
        # have been applied, and `is_transient` is absent because Meta never answered.
        # Retry it on the same terms as a transport error — idempotent callers only.
        if err.outcome_unknown and idempotent and attempt < retries:
            wait = delay + random.uniform(0, 1)
            print(f"  ! {resp.status_code} with no Graph error body — retrying in {wait:.1f}s",
                  file=sys.stderr)
            time.sleep(wait)
            delay = min(delay * 2, 60)
            continue

        if err.is_transient and attempt < retries:
            wait = delay + random.uniform(0, 1)
            print(f"  ! transient ({err.code}) — retrying in {wait:.1f}s", file=sys.stderr)
            time.sleep(wait)
            delay = min(delay * 2, 60)
            continue

        raise err

    raise GraphError(0, {"error": {"message": "retries exhausted", "code": -1}}, context)


def get(path: str, **kw) -> Any:
    return call("GET", path, params=kw.pop("params", None), context=kw.pop("context", path), **kw)


def post(path: str, data: dict[str, Any], **kw) -> Any:
    """Defaults to NOT retrying on a transport error — a create may already have been
    applied. Pass idempotent=True for writes that are safe to repeat (status flips,
    budget updates, filter swaps)."""
    return call("POST", path, data=data, context=kw.pop("context", path), **kw)


def page_token(page_id: str) -> str:
    """A Page access token. Required for the PBIA edge — a user/SU token returns 190
    'must be called with a Page Access Token', which means wrong token type, not a
    missing PBIA (meta-ads/13 §5).

    Graph does not error when the caller lacks Page admin rights: it returns the node
    WITHOUT the access_token field. Left unhandled that surfaces as a KeyError traceback
    instead of a diagnosable gate failure, so it is converted here."""
    node = get(f"{page_id}", params={"fields": "access_token"}, context="page_token")
    if "access_token" not in node:
        # status 403 deliberately: status 0 is this module's "outcome unknown" sentinel,
        # and a permissions gap is a definite, knowable answer.
        raise GraphError(
            403,
            {"error": {"message": (
                f"Page {page_id} returned no access_token. The token lacks a Page role "
                f"(need >=ADVERTISER, and pages_manage_ads / pages_read_engagement). "
                f"This is a permissions gap, not a missing PBIA."),
                "code": -1, "type": "OAuthException"}},
            "page_token",
        )
    return node["access_token"]
