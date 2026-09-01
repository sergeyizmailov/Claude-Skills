#!/usr/bin/env python3
"""Build a campaign from a JSON spec. Dry-run first, PAUSED always, resume-safe.

    python3 launch.py --spec specs/example-link-video.json
    python3 launch.py --spec ... --dry-run        # validate_only only, create nothing
    python3 launch.py --spec ...                  # validate, then create PAUSED
    python3 verify.py --state .meta-launch/<run_id>.json
    python3 activate.py --state .meta-launch/<run_id>.json   # separate, human-gated

The LLM writes the spec. This file writes the API calls. That split exists because
every recurring launch bug in this corpus is a payload bug — wrong nesting, wrong
unit, wrong field name, wrong order — and a payload assembled from prose is
re-derived, with fresh odds of being wrong, on every single run.

What this enforces so you cannot forget it:
  · every create is preceded by an `execution_options=['validate_only']` probe on the
    real run. In --dry-run only campaign and creative can be API-validated — ad sets and
    ads reference a parent that does not exist yet, so they are checked locally and
    validated for real at step 5 (that is also where `synchronous_ad_review` runs)
  · every object is created PAUSED; activation lives in activate.py behind a human
  · budgets are read from `*_minor` keys and must be int — no float dollars reach Graph
  · `targeting_automation` is nested inside `targeting`, never top-level  (1870227)
  · campaign create → budget/bid PATCH → budget-less adset, in that order  (4834011 / 1885737)
  · `instagram_user_id: "auto"` resolves the Page's PBIA                   (1772103)
  · `attribution_spec` uses `window_days`, not the non-existent `event_window_days`
  · Advantage+ creative features are opted OUT individually — there is no single switch,
    and `adapt_to_placement` is ON unless you name it
  · every created id is written to the state file before the next call, so a crashed
    run resumes instead of duplicating
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import sys
from typing import Any

import graph

STATE_DIR = ".meta-launch"

class SpecError(SystemExit):
    pass


# --------------------------------------------------------------------------- state


class State:
    """Resume log. Every id lands here before the next call goes out."""

    def __init__(self, path: str):
        self.path = path
        self.data: dict[str, Any] = {"objects": {}, "in_flight": {}, "errors": []}
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                self.data = json.load(fh)

    def get(self, key: str) -> str | None:
        return self.data["objects"].get(key)

    def put(self, key: str, obj_id: str) -> None:
        self.data["objects"][key] = obj_id
        self.data.get("in_flight", {}).pop(key, None)
        self.save()

    def attempt(self, key: str, path: str) -> None:
        """Written before the create POST goes out. If a run dies here, the next run
        sees the marker, refuses to blind-retry, and tells you to reconcile — better a
        stop than a duplicate campaign."""
        pending = self.data.setdefault("in_flight", {})
        if key in pending:
            raise SpecError(
                f"{key} was already attempted and never confirmed (state: {self.path}). "
                f"An object may exist in the account. Check {path} in Ads Manager, then "
                f"either add its id to objects.{key} in the state file or clear "
                f"in_flight.{key} to retry."
            )
        pending[key] = path
        self.save()

    def fail(self, key: str, err: dict, outcome_known: bool = True) -> None:
        """Record a failure. `outcome_known` decides whether the in-flight marker clears.

        Graph answered with a rejection → nothing was created → clear the marker so the
        next run can retry after you fix the spec. The request never reached Graph, or
        the reply was lost → the outcome is genuinely unknown → keep the marker and make
        the next run stop and reconcile. Clearing it in both cases loses the crash guard;
        keeping it in both cases bricks the run on an ordinary validation error."""
        self.data["errors"].append({"key": key, **err})
        if outcome_known:
            self.data.get("in_flight", {}).pop(key, None)
        self.save()

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as fh:
            fh.write(graph.redact(json.dumps(self.data, indent=2, default=str)))


# ---------------------------------------------------------------------- validation


def _int_minor(value: Any, field: str) -> int:
    """Budgets and bids are integer minor units — cents, kuruş, paise.

    A float here is the single most expensive silent bug available: 60.0 dollars
    submitted as `60` is 0.60 in account currency, and the ad set quietly underdelivers
    all day. Reject anything that is not already an int."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise SpecError(
            f"{field} must be an INTEGER in minor units (cents). "
            f"Got {value!r} ({type(value).__name__}). $60.00 → 6000."
        )
    if value <= 0:
        raise SpecError(f"{field} must be > 0, got {value}")
    return value


def load_spec(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        spec = json.load(fh)

    for key in ("account_id", "page_id", "campaign", "adsets"):
        if key not in spec:
            raise SpecError(f"spec is missing required key: {key}")

    if not spec["account_id"].startswith("act_"):
        spec["account_id"] = "act_" + str(spec["account_id"])

    camp = spec["campaign"]
    for key in ("name", "objective"):
        if key not in camp:
            raise SpecError(f"campaign is missing required key: {key}")
    _int_minor(camp.get("daily_budget_minor"), "campaign.daily_budget_minor")

    if "special_ad_categories" not in camp:
        raise SpecError(
            "campaign.special_ad_categories must be explicit. Use [] for none, or declare "
            "the real category (HOUSING / FINANCIAL_PRODUCTS_SERVICES / EMPLOYMENT / "
            "ISSUES_ELECTIONS_POLITICS). A false declaration is a violation, not a bypass."
        )

    if not spec["adsets"]:
        raise SpecError("spec has no adsets")
    for i, aset in enumerate(spec["adsets"]):
        for key in ("name", "optimization_goal", "targeting", "start_time"):
            if key not in aset:
                raise SpecError(f"adsets[{i}] is missing required key: {key}")
        if "daily_budget_minor" in aset:
            raise SpecError(
                f"adsets[{i}] carries its own budget while the campaign has one (CBO). "
                "Under CBO the ad set must have neither budget nor bid_strategy."
            )
        if not aset.get("ads"):
            raise SpecError(f"adsets[{i}] has no ads")

    spec.setdefault("run_id", os.path.splitext(os.path.basename(path))[0])
    return spec


# ------------------------------------------------------------------------ builders


def build_targeting(aset: dict) -> dict:
    """Whole targeting object, every time.

    A POST that carries one targeting field REPLACES the object and wipes the rest
    (field-observed, 04). So targeting is only ever assembled here, in full."""
    t = copy.deepcopy(aset["targeting"])

    # advantage_audience is a targeting_automation key nested INSIDE targeting.
    # Top-level it produces the misleading 1870227 "advantage audience" error.
    if "advantage_audience" in t:
        flag = 1 if t.pop("advantage_audience") else 0
        t.setdefault("targeting_automation", {})["advantage_audience"] = flag

    if "geo_locations" not in t:
        raise SpecError("targeting.geo_locations is required")
    return t


def build_attribution(aset: dict) -> list | None:
    """attribution_spec, set at ad-set CREATE.

    The sub-field is `window_days` — **not** `event_window_days`, which does not exist
    in the Marketing API (v26.0 ad set reference, verified 2026-08-31). This matters
    more than a typo: Graph ignores unknown keys inside a JSON object parameter rather
    than rejecting them, so a spec built with `event_window_days` is accepted, reports
    success, and leaves the ad set on the account default — 7-day click. Every CPL
    computed against a believed 1-day window is then wrong. verify.py reads the spec
    back for exactly this reason.

    Meta's product default is 7-day click / 1-day view; read the account's actual
    default from `default_unified_attribution_spec` rather than assuming.
    Editing it on a live ad set is a significant edit and re-enters learning."""
    att = aset.get("attribution")
    if not att:
        return None
    spec = []
    if att.get("click_days"):
        spec.append({"event_type": "CLICK_THROUGH", "window_days": int(att["click_days"])})
    if att.get("view_days"):
        spec.append({"event_type": "VIEW_THROUGH", "window_days": int(att["view_days"])})
    if att.get("engaged_video_view_days"):
        spec.append({"event_type": "ENGAGED_VIDEO_VIEW",
                     "window_days": int(att["engaged_video_view_days"])})
    return spec or None


def resolve_identity(spec: dict, create: bool = True) -> str | None:
    """`instagram_user_id: "auto"` → the Page's page-backed Instagram account.

    Without an IG identity, POST /ads fails 1772103 whenever placements include
    Instagram. The tempting fix — publisher_platforms=['facebook'] — makes the error
    vanish while silently deleting IG + Audience Network + Messenger inventory. Fix the
    identity, never the placements."""
    ig = spec.get("instagram_user_id")
    if ig and ig != "auto":
        return str(ig)
    if ig != "auto":
        return None

    page_id = str(spec["page_id"])
    ptoken = graph.page_token(page_id)
    existing = graph.call(
        "GET", f"{page_id}/page_backed_instagram_accounts",
        token_override=ptoken, context="pbia read",
    ).get("data", [])
    if existing:
        return existing[0]["id"]
    if not create:
        return None
    created = graph.call(
        "POST", f"{page_id}/page_backed_instagram_accounts",
        token_override=ptoken, context="pbia create",
    )
    return created["id"]


# There is NO single switch that disables Advantage+ creative enhancements. The
# `standard_enhancements` bundle stopped being settable at v22.0 (the field still exists
# in the schema, which is why toggling it looks like it worked), so every feature must be
# named individually. Two traps:
#   · `adapt_to_placement` is OPT-IN BY DEFAULT — omit it and it stays on.
#   · Music is not in creative_features_spec at all; opt out with asset_feed_spec.audios=[].
# Meta's own docs disagree about which keys are writable: the v26.0 reference field table
# and the Advantage+ guide list different sets. These are the keys present in the v26.0
# reference plus the three added by the 2026-06-28 out-of-cycle change. If your account
# rejects one, --dry-run catches it before anything is created — drop it from
# `creative.opt_out_features` in the spec.
DEFAULT_OPT_OUT = [
    "adapt_to_placement", "add_text_overlay", "creative_stickers", "description_automation",
    "image_animation", "image_background_gen", "image_templates", "image_touchups",
    "inline_comment", "media_type_automation", "pac_relaxation", "product_extensions",
    "reveal_details_over_time", "standard_enhancements", "text_optimizations",
    "text_translation", "translate_voiceover", "video_filtering", "video_uncrop",
]


def opt_out_enhancements(features: list[str]) -> dict:
    """Per-feature OPT_OUT. The single `enable_standard_enhancements` boolean and the
    `standard_enhancements` bundle stopped being settable at v22.0 — the field still
    exists in the schema, which is why toggling it looks like it worked (14)."""
    return {
        "creative_features_spec": {f: {"enroll_status": "OPT_OUT"} for f in features}
    }


def _prune(obj):
    """Drop None values at every depth.

    graph.call() strips top-level Nones, but object_story_spec is JSON-encoded whole,
    so a null nested inside it reaches Meta verbatim and can fail validation on a field
    you never meant to send."""
    if isinstance(obj, dict):
        return {k: _prune(v) for k, v in obj.items() if v is not None}
    if isinstance(obj, list):
        return [_prune(v) for v in obj]
    return obj


def build_dlo_feed(c: dict) -> dict:
    """asset_feed_spec for language customization.

    Spec shape expected (one entry per locale group):
        "locales": [{"label": "tr", "ids": [59], "is_default": false,
                     "body": "...", "title": "...", "description": "...",
                     "link": "https://..."}]

    Hard rules Meta enforces: exactly ONE ad format per feed; exactly one
    call_to_action_type when customization rules are present; every text asset carries an
    adlabel; exactly one rule is_default. The asset-customization-rules page additionally
    says a feed needs at least two rules — the autotranslate example ships one; assume two.
    The ad set must have is_dynamic_creative=false for a rule-based feed."""
    locales = c.get("locales")
    if not locales:
        raise SpecError("creative.kind=dlo requires a non-empty `locales` list")
    if sum(1 for loc in locales if loc.get("is_default")) != 1:
        raise SpecError("exactly one entry in `locales` must set is_default: true")

    # DLO accepts only these two formats — narrower than asset_feed_spec generally,
    # which also takes CAROUSEL and AUTOMATIC_FORMAT.
    fmt = c.get("ad_format", "SINGLE_IMAGE")
    if fmt not in ("SINGLE_IMAGE", "SINGLE_VIDEO"):
        raise SpecError(
            f"creative.kind=dlo supports ad_format SINGLE_IMAGE or SINGLE_VIDEO only, got {fmt!r}"
        )
    media_key = "image_hash" if fmt == "SINGLE_IMAGE" else "video_id"
    if not c.get(media_key):
        raise SpecError(f"creative.kind=dlo with ad_format={fmt} needs {media_key}")

    feed: dict[str, Any] = {
        "ad_formats": [fmt],
        "call_to_action_types": [c.get("cta", "LEARN_MORE")],
        "bodies": [], "titles": [], "descriptions": [], "link_urls": [],
        "asset_customization_rules": [],
    }
    # One media asset per locale label, so each rule can carry the label the docs
    # require: image_label for SINGLE_IMAGE, video_label for SINGLE_VIDEO. A rule
    # missing its media label is rejected.
    if fmt == "SINGLE_IMAGE":
        feed["images"] = []
    else:
        feed["videos"] = []

    for loc in locales:
        label = loc["label"]
        tag = [{"name": label}]
        feed["bodies"].append({"text": loc["body"], "adlabels": tag})
        feed["titles"].append({"text": loc["title"], "adlabels": tag})
        # `descriptions` is REQUIRED. The docs specify a single space for a blank one —
        # an omitted or empty list is not the same thing and is rejected.
        feed["descriptions"].append({"text": loc.get("description") or " ", "adlabels": tag})
        feed["link_urls"].append({"website_url": loc["link"], "adlabels": tag})

        if fmt == "SINGLE_IMAGE":
            feed["images"].append({"hash": loc.get("image_hash", c["image_hash"]), "adlabels": tag})
        else:
            feed["videos"].append(
                {"video_id": str(loc.get("video_id", c["video_id"])), "adlabels": tag}
            )

        rule: dict[str, Any] = {
            "customization_spec": {"locales": [int(x) for x in loc["ids"]]},
            "body_label": {"name": label},
            "title_label": {"name": label},
            "description_label": {"name": label},
            "link_url_label": {"name": label},
            ("image_label" if fmt == "SINGLE_IMAGE" else "video_label"): {"name": label},
        }
        if loc.get("is_default"):
            rule["is_default"] = True
        feed["asset_customization_rules"].append(rule)

    if len(feed["asset_customization_rules"]) < 2:
        raise SpecError(
            "DLO needs at least two customization rules (the default slot plus at least "
            "one added locale) — Meta's asset-customization-rules page requires it."
        )
    # Music is not opted out through creative_features_spec; an empty audios list is.
    feed.setdefault("audios", [])
    return feed


def _finish(payload: dict, c: dict) -> dict:
    """Apply the enhancement opt-out to every creative shape, then prune nulls.

    Applies to catalog and DLO creatives too — that is the whole point of having one
    exit. `media_type_automation` is the one key worth overriding per shape: OPT_OUT for
    plain images (3858040), but on a catalog creative it is what ADDS video alongside
    images on the Dynamic Media path, so a catalog spec that wants video should pass
    `opt_out_features` without it."""
    features = c.get("opt_out_features")
    if features is None:
        features = DEFAULT_OPT_OUT
    if features:
        payload["degrees_of_freedom_spec"] = opt_out_enhancements(features)
    return _prune(payload)


def build_creative(spec: dict, ad: dict, ig_id: str | None) -> dict:
    """Assemble one adcreative payload. `kind` selects the shape."""
    c = ad.get("creative")
    if not isinstance(c, dict):
        raise SpecError(f"ad {ad.get('name', '?')}: missing a `creative` object")
    kind = c.get("kind", "link_image")

    # Fail on a readable message, not a KeyError traceback — the spec is agent-written.
    required = {
        "link_image": ("link", "image_hash"),
        "link_video": ("link", "video_id"),
        "dlo": ("locales",),
        "catalog_collection": ("link", "product_set_id"),
        "catalog_single": ("link", "product_set_id"),
    }.get(kind)
    if required is None:
        raise SpecError(
            f"ad {ad.get('name', '?')}: unknown creative.kind {kind!r}. "
            "Known: link_image, link_video, dlo, catalog_collection, catalog_single."
        )
    missing = [f for f in required if not c.get(f)]
    if missing:
        raise SpecError(f"ad {ad.get('name', '?')}: creative.kind={kind} is missing {missing}")
    story: dict[str, Any] = {"page_id": str(spec["page_id"])}
    if ig_id:
        story["instagram_user_id"] = ig_id

    payload: dict[str, Any] = {"name": ad["name"]}
    if c.get("url_tags"):
        payload["url_tags"] = c["url_tags"]

    cta = {"type": c.get("cta", "LEARN_MORE"),
           "value": {"link": c["link"]} if c.get("link") else {}}

    if kind == "link_image":
        story["link_data"] = {
            "link": c["link"],
            "message": c.get("message", ""),
            "name": c.get("headline"),
            "description": c.get("description"),
            "caption": c.get("display_link"),
            "image_hash": c["image_hash"],
            "call_to_action": cta,
        }
    elif kind == "link_video":
        story["video_data"] = {
            "video_id": c["video_id"],
            "message": c.get("message", ""),
            "title": c.get("headline"),
            "link_description": c.get("description"),
            "call_to_action": cta,
        }
        # A video ad needs a thumbnail. Prefer image_hash: the AdCreativeVideoData
        # reference says not to feed FB CDN URLs into image_url, and media.py already
        # converts the /thumbnails uri into an owned hash. If you do pass a uri, pass it
        # WHOLE — truncating its signed query string fails creation with 2446603.
        if c.get("image_hash"):
            story["video_data"]["image_hash"] = c["image_hash"]
        elif c.get("thumbnail_url"):
            story["video_data"]["image_url"] = c["thumbnail_url"]
        else:
            raise SpecError(
                f"creative {ad['name']}: a video creative needs a thumbnail. Run media.py "
                "and use its thumbnail_image_hash, or supply thumbnail_url (whole uri)."
            )
    elif kind == "dlo":
        # Multi-language / Dynamic Language Optimization. Locales are NUMERIC ids from
        # GET /search?type=adlocale&q=<lang> — a string locale code is silently wrong.
        # Exactly one rule carries is_default:true; that is the "Default" slot.
        feed = build_dlo_feed(c)
        payload["asset_feed_spec"] = feed
        payload["object_story_spec"] = story
        return _finish(payload, c)

    elif kind in ("catalog_collection", "catalog_single"):
        if not c.get("product_set_id"):
            raise SpecError(f"creative {ad['name']}: {kind} needs product_set_id")
        payload["product_set_id"] = str(c["product_set_id"])
        # Catalog card clicks resolve their URL from the product feed and bypass the
        # ad's url_tags, so subids never arrive. template_url_spec is the documented
        # override; without it a catalog launch is untracked (04 -> url_tags).
        if c.get("template_url"):
            payload["template_url_spec"] = {"web": {"url": c["template_url"]}}
        else:
            print("    ! catalog creative without template_url: card clicks will carry no "
                  "subids. Set creative.template_url, or capture the subid in the landing "
                  "builder.", file=sys.stderr)
        template: dict[str, Any] = {
            "link": c["link"],
            "message": c.get("message", ""),
            "call_to_action": cta,
        }
        if kind == "catalog_collection":
            # COLLECTION needs >=4 items in the set (2490457 at build). The video hero
            # goes through asset_feed_spec, NOT video_data: link_data.video_data with a
            # product_set_id is an undocumented path and fails 1487832 "invalid repost".
            template["multi_share_end_card"] = c.get("multi_share_end_card", False)
            story["template_data"] = template
            payload["object_story_spec"] = story
            feed: dict[str, Any] = {
                "optimization_type": "FORMAT_AUTOMATION",
                "ad_formats": ["COLLECTION"],
            }
            if c.get("video_id"):
                feed["videos"] = [{"video_id": str(c["video_id"])}]
            payload["asset_feed_spec"] = feed
            # Multi-advertiser ads default ON for FORMAT_AUTOMATION catalog creatives and
            # no API field disables them. Build PAUSED, bulk-uncheck in Ads Manager, then
            # activate — toggling it post-approval is re-moderation (04).
            print("    ! catalog_collection: multi-advertiser ads default ON and cannot be "
                  "disabled via API. Uncheck in Ads Manager before activating.")
            if c.get("opt_out_features") is None:
                print("    ! catalog_collection: media_type_automation is being OPT_OUT by "
                      "default, which strips video from Dynamic Media. Pass "
                      "creative.opt_out_features without it if you want video cards.")
        else:
            # One-product set renders as a single deep-linked card, no minimum item count.
            # force_single_link for an image card; format_option single_video for the
            # documented Dynamic Media video path (video attached to the PRODUCT).
            template["force_single_link"] = True
            if c.get("format_option"):
                template["format_option"] = c["format_option"]
            story["template_data"] = template
            payload["object_story_spec"] = story
        return _finish(payload, c)

    else:
        raise SpecError(
            f"unknown creative.kind: {kind}. "
            "Known: link_image, link_video, dlo, catalog_collection, catalog_single."
        )

    payload["object_story_spec"] = story
    return _finish(payload, c)


# -------------------------------------------------------------------------- create


# execution_options support, per the v26.0 reference (verified 2026-08-31):
#   POST /act_X/campaigns    validate_only, include_recommendations
#   POST /act_X/adsets       validate_only, include_recommendations
#   POST /act_X/ads          validate_only, synchronous_ad_review, include_recommendations
#   POST /act_X/adcreatives  validate_only ONLY
#   POST /{adcreative_id}    NOT supported — creatives can only be validated at create time
# `synchronous_ad_review` must be paired with validate_only; it additionally runs Ads
# Integrity checks (message language, image text rule) BEFORE the object exists — the
# cheapest possible read on whether a creative will survive review.
VALIDATE_OPTS = {
    "campaign": ["validate_only"],
    "adset": ["validate_only"],
    "creative": ["validate_only"],
    "ad": ["validate_only", "synchronous_ad_review"],
}


# Objects whose payload references a parent id. In --dry-run the parent was never
# created, so there is no real id to send and `validate_only` would fail on the foreign
# key rather than on your payload — a misleading failure, not a useful gate. These are
# validated locally in dry-run and by the API on the real run, where the parent exists.
PARENT_BOUND = ("adset", "ad")


def _create(node: str, path: str, payload: dict, state: State, dry: bool) -> str | None:
    """validate_only, then (unless --dry-run) the real create. Resumes from state."""
    cached = state.get(node)
    if cached:
        print(f"  = {node}: {cached} (from state, skipped)")
        return cached

    kind = node.split("[")[0]

    if dry and kind in PARENT_BOUND:
        print(f"  - {node}: built OK, API validation deferred (needs a real "
              f"{'campaign' if kind == 'adset' else 'ad set/creative'} id)")
        return None

    probe = dict(payload, execution_options=VALIDATE_OPTS.get(kind, ["validate_only"]))
    try:
        graph.post(path, probe, context=f"validate {node}")
    except graph.GraphError as e:
        state.fail(node, e.as_dict())  # validate_only mutates nothing
        print(f"  x {node}: VALIDATION FAILED\n      {e}", file=sys.stderr)
        if e.blame_field:
            print(f"      offending field path: {e.blame_field}", file=sys.stderr)
        raise SystemExit(1) from e
    print(f"  ✓ {node}: payload valid")

    if dry:
        return None

    # Record the attempt BEFORE issuing it. A kill between a successful POST and the
    # state write would otherwise leave an orphan object that the next run recreates.
    state.attempt(node, path)
    try:
        obj_id = graph.post(path, payload, context=f"create {node}")["id"]
    except graph.GraphError as e:
        # graph.py decides this: a Graph-issued error means the call was rejected and
        # nothing was created; a transport failure or a non-Graph 5xx means the object
        # may or may not exist. A narrower local test missed HTML 502s from an edge.
        outcome_known = not e.outcome_unknown
        state.fail(node, e.as_dict(), outcome_known=outcome_known)
        print(f"  x {node}: CREATE FAILED\n      {e}", file=sys.stderr)
        if not outcome_known:
            print(f"      Outcome UNKNOWN — {node} may exist in the account. The next run "
                  f"will stop and ask you to reconcile.", file=sys.stderr)
        raise SystemExit(1) from e
    state.put(node, obj_id)
    print(f"  + {node}: {obj_id}")
    return obj_id


def run(spec: dict, state: State, dry: bool) -> None:
    account = spec["account_id"]
    camp = spec["campaign"]

    # Resolve in dry-run as well. Validating a creative without the IG identity is a
    # false pass: the real run would then fail 1772103 at POST /ads, which is exactly
    # the failure the dry run exists to catch. In dry-run we only READ the PBIA — we do
    # not create one — so a missing PBIA is reported, not silently fixed.
    ig_id = resolve_identity(spec, create=not dry)
    if ig_id:
        print(f"  identity: instagram_user_id={ig_id}")
    elif spec.get("instagram_user_id") == "auto":
        print("  ! no PBIA on this Page. Any ad set including Instagram placements will "
              "fail 1772103. Run: probe.py --page <id> --create-pbia", file=sys.stderr)

    # Step 1 — campaign WITHOUT budget and WITHOUT bid_strategy.
    # bid_strategy on a campaign that has no budget yet fails 1885737;
    # omitting is_adset_budget_sharing_enabled fails 4834011 on OUTCOME_LEADS.
    campaign_id = _create(
        "campaign",
        f"{account}/campaigns",
        {
            "name": camp["name"],
            "objective": camp["objective"],
            "status": "PAUSED",
            "buying_type": camp.get("buying_type", "AUCTION"),
            "special_ad_categories": camp["special_ad_categories"],
            "is_adset_budget_sharing_enabled": False,
        },
        state, dry,
    )
    if not campaign_id:
        campaign_id = "<dry-run>"

    # Step 2 — budget and bid strategy onto the existing campaign.
    # No in-flight marker here, deliberately: re-POSTing the same daily_budget and
    # bid_strategy is idempotent, so a crash mid-PATCH costs a harmless repeat on the
    # next run. A marker would only turn that into a false "reconcile by hand" stop.
    # It DOES need the same error handling and dry-run probe as every other write —
    # without them a failure here surfaced as a bare traceback, and --dry-run never
    # checked the budget or bid strategy at all.
    if not state.get("campaign_budget"):
        budget_payload = {
            "daily_budget": _int_minor(camp["daily_budget_minor"], "campaign.daily_budget_minor"),
            "bid_strategy": camp.get("bid_strategy", "LOWEST_COST_WITHOUT_CAP"),
        }
        if camp.get("bid_amount_minor"):
            budget_payload["bid_amount"] = _int_minor(camp["bid_amount_minor"], "campaign.bid_amount_minor")

        # POST /{campaign_id} does accept validate_only, but in a dry run the campaign
        # does not exist, so the call could only fail on the missing object — which says
        # nothing about the budget or bid strategy. Report the values and validate them
        # on the real run, where the campaign is there.
        if dry:
            print(f"  - campaign budget: {budget_payload['daily_budget']} minor units, "
                  f"{budget_payload['bid_strategy']} (validated on the real run — the "
                  f"campaign does not exist yet)")
        else:
            try:
                graph.post(
                    campaign_id,
                    dict(budget_payload, execution_options=["validate_only"]),
                    context="validate campaign budget",
                )
                graph.post(campaign_id, budget_payload, context="campaign budget",
                           idempotent=True)
            except graph.GraphError as e:
                state.fail("campaign_budget", e.as_dict(), outcome_known=not e.outcome_unknown)
                print(f"  x campaign budget: FAILED\n      {e}", file=sys.stderr)
                print(f"      The campaign exists ({campaign_id}) but carries no budget, so "
                      f"its ad sets cannot be created. Fix and re-run — this step is "
                      f"idempotent.", file=sys.stderr)
                raise SystemExit(1) from e
            state.put("campaign_budget", campaign_id)
            print(f"  + campaign budget: {budget_payload['daily_budget']} minor units, "
                  f"{budget_payload['bid_strategy']}")

    for i, aset in enumerate(spec["adsets"]):
        # Step 3 — ad set with NO budget and NO bid_strategy (the campaign owns both).
        payload: dict[str, Any] = {
            "name": aset["name"],
            "campaign_id": campaign_id,
            "status": "PAUSED",
            "billing_event": aset.get("billing_event", "IMPRESSIONS"),
            "optimization_goal": aset["optimization_goal"],
            "targeting": build_targeting(aset),
            "start_time": aset["start_time"],
        }
        if aset.get("end_time"):
            payload["end_time"] = aset["end_time"]
        if spec.get("pixel_id") and aset.get("custom_event_type"):
            payload["promoted_object"] = {
                "pixel_id": str(spec["pixel_id"]),
                "custom_event_type": aset["custom_event_type"],
            }
        att = build_attribution(aset)
        if att:
            payload["attribution_spec"] = att

        adset_id = _create(f"adset[{i}]", f"{account}/adsets", payload, state, dry) or "<dry-run>"

        for j, ad in enumerate(aset["ads"]):
            creative_payload = build_creative(spec, ad, ig_id)
            creative_id = _create(
                f"creative[{i}.{j}]", f"{account}/adcreatives", creative_payload, state, dry
            ) or "<dry-run>"
            _create(
                f"ad[{i}.{j}]",
                f"{account}/ads",
                {
                    "name": ad["name"],
                    "adset_id": adset_id,
                    "creative": {"creative_id": creative_id},
                    "status": "PAUSED",
                },
                state, dry,
            )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--dry-run", action="store_true", help="validate_only; create nothing")
    ap.add_argument("--state", help=f"default {STATE_DIR}/<run_id>.json")
    args = ap.parse_args()

    spec = load_spec(args.spec)
    state_path = args.state or os.path.join(STATE_DIR, f"{spec['run_id']}.json")
    state = State(state_path)

    mode = "DRY RUN (validate_only)" if args.dry_run else "CREATE (all objects PAUSED)"
    print(f"Graph {graph.API_VERSION} · {spec['account_id']} · {mode}")
    print(f"state → {state_path}\n")

    run(spec, state, args.dry_run)

    if args.dry_run:
        print("\nSpec validates. Re-run without --dry-run to create.")
    else:
        print(f"\nCreated PAUSED. Next: python3 verify.py --state {state_path}")
        print("Nothing spends until activate.py, which needs explicit human approval.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
