#!/usr/bin/env python3
"""Pre-flight gate. Proves the token can actually WRITE before anything is built.

    export META_TOKEN=...  META_PROXY=socks5h://user:pass@host:port
    python3 probe.py --account act_123 --page 456 [--dataset 789] [--json report.json]

Every check is a separate gate (meta-ads/13 §4): a successful GET proves nothing about
write access, and an asset visible to a human is not an asset assigned to the token.

Every call here retries on a dropped connection, reads and writes alike. This script is
diagnostic: its writes create nothing that a repeat could duplicate (validate_only
mutates nothing, the CAPI probe posts an empty batch, and the PBIA edge is
get-or-create), so a one-shot POST would only let a proxy blip report "no write access"
on an account that has it.
Exit code 1 if any REQUIRED gate fails. Run this before launch.py, every new account.
"""

from __future__ import annotations

import argparse
import json
import sys

import graph

PASS, FAIL, WARN = "PASS", "FAIL", "WARN"

# account_status is undocumented as an enum; these are the widely-observed values.
# Never diagnose from this number alone — confirm in Account Quality (meta-ads/13 §4).
ACCOUNT_STATUS = {
    1: "ACTIVE",
    2: "DISABLED",
    3: "UNSETTLED",
    7: "PENDING_RISK_REVIEW",
    8: "PENDING_SETTLEMENT",
    9: "IN_GRACE_PERIOD",
    100: "PENDING_CLOSURE",
    101: "CLOSED",
    201: "ANY_ACTIVE",
    202: "ANY_CLOSED",
}

REQUIRED_SCOPES = ["ads_management", "ads_read"]


class Report:
    def __init__(self) -> None:
        self.rows: list[dict] = []

    def add(self, gate: str, state: str, detail: str, data=None) -> None:
        self.rows.append({"gate": gate, "state": state, "detail": detail, "data": data})
        mark = {PASS: "ok  ", FAIL: "FAIL", WARN: "warn"}[state]
        print(f"  {mark}  {gate}: {graph.redact(detail)}")

    @property
    def failed(self) -> bool:
        return any(r["state"] == FAIL for r in self.rows)


def gate_identity(r: Report) -> None:
    try:
        me = graph.get("me", params={"fields": "id,name"}, context="identity")
        r.add("token identity", PASS, f"{me.get('name', '?')} ({me['id']})", me)
    except graph.GraphError as e:
        r.add("token identity", FAIL, str(e), e.as_dict())


def gate_scopes(r: Report) -> None:
    try:
        perms = graph.get("me/permissions", context="scopes")["data"]
    except graph.GraphError as e:
        r.add("granted scopes", FAIL, str(e), e.as_dict())
        return
    granted = {p["permission"] for p in perms if p.get("status") == "granted"}
    missing = [s for s in REQUIRED_SCOPES if s not in granted]
    if missing:
        r.add("granted scopes", FAIL, f"missing {missing}; granted={sorted(granted)}", sorted(granted))
    else:
        r.add("granted scopes", PASS, ", ".join(sorted(granted)), sorted(granted))


def gate_account(r: Report, account: str) -> dict | None:
    fields = (
        "id,name,account_status,disable_reason,currency,timezone_name,"
        "timezone_offset_hours_utc,spend_cap,amount_spent,balance,"
        "funding_source_details,business,is_prepay_account,capabilities"
    )
    try:
        acct = graph.get(account, params={"fields": fields}, context="ad account")
    except graph.GraphError as e:
        r.add("ad account read", FAIL, str(e), e.as_dict())
        return None

    status = acct.get("account_status")
    label = ACCOUNT_STATUS.get(status, f"UNKNOWN({status})")
    state = PASS if status == 1 else FAIL
    r.add("ad account status", state, f"{label} disable_reason={acct.get('disable_reason')}", acct)

    r.add(
        "currency / timezone",
        WARN,
        f"{acct.get('currency')} / {acct.get('timezone_name')} — "
        "changing either CLOSES the account and opens a new act id (08). Confirm with the TL.",
    )
    if not acct.get("funding_source_details"):
        r.add("funding source", FAIL, "no payment method on the ad account", None)
    else:
        r.add("funding source", PASS, str(acct["funding_source_details"].get("type_name", "set")))
    return acct


def gate_page_and_pbia(r: Report, page_id: str, create: bool) -> str | None:
    try:
        ptoken = graph.page_token(page_id)
        r.add("page access token", PASS, f"page {page_id}")
    except graph.GraphError as e:
        r.add("page access token", FAIL, f"{e} — needs >=ADVERTISER role on the Page", e.as_dict())
        return None

    try:
        existing = graph.call(
            "GET",
            f"{page_id}/page_backed_instagram_accounts",
            token_override=ptoken,
            context="pbia read",
        ).get("data", [])
    except graph.GraphError as e:
        r.add("PBIA", FAIL, str(e), e.as_dict())
        return None

    if existing:
        pbia = existing[0]["id"]
        r.add("PBIA", PASS, f"instagram_user_id={pbia}", pbia)
        return pbia

    if not create:
        r.add(
            "PBIA",
            FAIL,
            "none exists. Ads with Instagram placements will fail 1772103 at POST /ads. "
            "Re-run with --create-pbia. Do NOT 'fix' it with publisher_platforms=['facebook'].",
        )
        return None

    try:
        pbia = graph.call(
            "POST",
            f"{page_id}/page_backed_instagram_accounts",
            token_override=ptoken,
            context="pbia create",
            idempotent=True,
        )["id"]
        r.add("PBIA", PASS, f"created instagram_user_id={pbia}", pbia)
        return pbia
    except graph.GraphError as e:
        r.add("PBIA", FAIL, str(e), e.as_dict())
        return None


def gate_dataset(r: Report, dataset_id: str) -> None:
    """Zero-event CAPI write probe: an empty data array proves auth without writing.

    Meta answers a well-authorised empty POST with 'param data must be non-empty'.
    That error IS the pass condition."""
    try:
        graph.post(dataset_id + "/events", {"data": []}, context="capi probe",
                   idempotent=True)
        r.add("dataset CAPI write", WARN, "empty POST accepted — unexpected, verify manually")
    except graph.GraphError as e:
        text = (e.user_msg or e.message).lower()
        if "non-empty" in text or "must be non-empty" in text:
            r.add("dataset CAPI write", PASS, "auth confirmed, no events written")
        else:
            r.add("dataset CAPI write", FAIL, str(e), e.as_dict())


def gate_write(r: Report, account: str) -> None:
    """validate_only campaign create. Runs Meta's own field validation and mutates nothing.

    This is the guardrail that catches a malformed payload without creating an object,
    without spend, and without touching the account's risk surface."""
    try:
        graph.post(
            f"{account}/campaigns",
            {
                "name": "probe-validate-only",
                "objective": "OUTCOME_LEADS",
                "status": "PAUSED",
                "special_ad_categories": [],
                # Required from v24 when the campaign carries no budget, which a probe
                # never does. Omitting it fails 4834011 and looks like a permissions
                # problem. It is NOT campaign budget optimization — it is up-to-20%
                # budget sharing between sibling ad sets.
                "is_adset_budget_sharing_enabled": False,
                "execution_options": ["validate_only"],
            },
            context="write probe",
            idempotent=True,
        )
        r.add("write access (validate_only)", PASS, "campaign payload validated, nothing created")
    except graph.GraphError as e:
        r.add(
            "write access (validate_only)",
            FAIL,
            f"{e} — check ads_management granted, System User write task on THIS "
            "account, app-business relationship, and account restriction state (13 §4).",
            e.as_dict(),
        )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--account", required=True, help="act_<id>")
    ap.add_argument("--page", help="Page id used as the ad identity")
    ap.add_argument("--dataset", help="Pixel/dataset id for the CAPI write probe")
    ap.add_argument("--create-pbia", action="store_true", help="Create the PBIA if absent")
    ap.add_argument("--json", help="Write the full report here")
    args = ap.parse_args()

    account = args.account if args.account.startswith("act_") else f"act_{args.account}"

    print(f"Graph {graph.API_VERSION} · {account}")
    r = Report()
    gate_identity(r)
    gate_scopes(r)
    gate_account(r, account)
    if args.page:
        gate_page_and_pbia(r, args.page, args.create_pbia)
    if args.dataset:
        gate_dataset(r, args.dataset)
    gate_write(r, account)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            fh.write(graph.redact(json.dumps(r.rows, indent=2, default=str)))
        print(f"\nreport → {args.json}")

    if r.failed:
        print("\nBLOCKED — fix the FAIL gates before launching.", file=sys.stderr)
        return 1
    print("\nAll required gates passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
