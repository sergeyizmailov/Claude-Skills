"""Read-only verification of the asset graph declared in workspace.json."""

from __future__ import annotations

from typing import Any

import graph
from meta_workspace import Workspace


def _ids(rows: list[dict[str, Any]]) -> set[str]:
    return {str(row.get("id")) for row in rows}


def _edge(
    path: str,
    fields: str = "id,name",
    max_rows: int | None = None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    after: str | None = None
    while True:
        page_limit = min(200, max_rows - len(rows)) if max_rows is not None else 200
        params = {"fields": fields, "limit": page_limit}
        if after:
            params["after"] = after
        payload = graph.get(path, params=params, context=path)
        rows.extend(payload.get("data", []))
        if max_rows is not None and len(rows) >= max_rows:
            return rows[:max_rows]
        after = ((payload.get("paging") or {}).get("cursors") or {}).get("after")
        if not after or not (payload.get("paging") or {}).get("next"):
            return rows


def verify_assets(
    workspace: Workspace,
    requested_profile: str | None = None,
    scope: str = "all",
) -> dict[str, Any]:
    if scope not in {"core", "all"}:
        raise ValueError("asset scope must be 'core' or 'all'")
    name, profile = workspace.profile(requested_profile)
    checks: list[dict[str, Any]] = []

    def check(key: str, ok: bool, detail: str) -> None:
        checks.append({"check": key, "ok": bool(ok), "detail": detail})

    business_id = str(profile.get("business_id") or "")
    app_id = str(profile.get("app_id") or "")
    system_user_id = str(profile.get("system_user_id") or "")
    account_id = graph.normalize_account(profile["ad_account_id"])
    page_id = str(profile.get("page_id") or "")
    dataset_id = str(profile.get("dataset_id") or "")
    catalog_id = str(profile.get("catalog_id") or "")

    business = graph.get(business_id, params={"fields": "id,name,verification_status"},
                         context="workspace business")
    check("business", business.get("id") == business_id,
          f"{business.get('name')} verification={business.get('verification_status')}")

    if app_id:
        apps = _edge(f"{business_id}/owned_apps")
        check("app_owned", app_id in _ids(apps), f"app {app_id} owned by business")
    if system_user_id:
        users = _edge(f"{business_id}/system_users")
        check("system_user_assigned", system_user_id in _ids(users),
              f"system user {system_user_id} assigned to business")
        assigned_accounts = _edge(f"{system_user_id}/assigned_ad_accounts", "id,name,tasks")
        check("account_assigned", account_id in _ids(assigned_accounts),
              f"{account_id} assigned to system user")

    account = graph.get(
        account_id,
        params={"fields": "id,name,account_status,disable_reason,currency,timezone_name,"
                          "funding_source_details,business{id,name}"},
        context="workspace ad account",
    )
    account_business = str((account.get("business") or {}).get("id") or "")
    check("account_active", account.get("account_status") == 1,
          f"{account.get('name')} status={account.get('account_status')} "
          f"disable_reason={account.get('disable_reason')}")
    is_assigned = account_id in _ids(assigned_accounts) if system_user_id else False
    check("account_owned", account_business == business_id or is_assigned,
          f"account business={account_business or 'agency_assigned'}")
    check("funding", bool(account.get("funding_source_details")), "funding source is set")
    expected_currency = profile.get("currency")
    check("currency", not expected_currency or account.get("currency") == expected_currency,
          f"live={account.get('currency')} expected={expected_currency}")
    expected_timezone = profile.get("timezone")
    check("timezone", not expected_timezone or account.get("timezone_name") == expected_timezone,
          f"live={account.get('timezone_name')} expected={expected_timezone}")

    if page_id:
        assigned_pages = _edge(f"{system_user_id}/assigned_pages", "id,name,tasks")
        check("page_assigned", page_id in _ids(assigned_pages),
              f"page {page_id} assigned to system user")
        page_access_token = graph.page_token(page_id)
        pbias = graph.get(
            f"{page_id}/page_backed_instagram_accounts",
            params={"fields": "id,username", "limit": 20},
            token_override=page_access_token,
            context="workspace PBIA",
        ).get("data", [])
        check("pbia", bool(pbias), f"{len(pbias)} Page-backed Instagram account(s)")

    if dataset_id:
        pixels = _edge(f"{account_id}/adspixels")
        check("dataset_attached", dataset_id in _ids(pixels),
              f"dataset {dataset_id} attached to {account_id}")
        dataset = graph.get(dataset_id, params={"fields": "id,name"}, context="workspace dataset")
        check("dataset_read", dataset.get("id") == dataset_id, str(dataset.get("name")))

    product_sets: list[dict[str, Any]] = []
    if scope == "all" and catalog_id:
        catalogs = _edge(f"{system_user_id}/assigned_product_catalogs")
        check("catalog_assigned", catalog_id in _ids(catalogs),
              f"catalog {catalog_id} assigned to system user")
        catalog = graph.get(
            catalog_id,
            params={"fields": "id,name,vertical,product_count,business{id,name}"},
            context="workspace catalog",
        )
        catalog_business = str((catalog.get("business") or {}).get("id") or "")
        check("catalog_owned", catalog_business == business_id,
              f"catalog business={catalog_business}")
        check("catalog_products", int(catalog.get("product_count") or 0) > 0,
              f"catalog product_count={catalog.get('product_count')}")
        for alias, set_id in (profile.get("product_sets") or {}).items():
            product_set = graph.get(
                str(set_id),
                params={"fields": "id,name,product_count,filter,product_catalog{id,name}"},
                context=f"workspace product set {alias}",
            )
            set_catalog = str((product_set.get("product_catalog") or {}).get("id") or "")
            count = int(product_set.get("product_count") or 0)
            ok = set_catalog == catalog_id and count > 0
            product_sets.append({
                "alias": alias,
                "id": str(set_id),
                "name": product_set.get("name"),
                "catalog_id": set_catalog,
                "product_count": count,
                "ready": ok,
            })
            check(f"product_set:{alias}", ok,
                  f"catalog={set_catalog} product_count={count}")

    failed = [row for row in checks if not row["ok"]]
    return {
        "workspace": str(workspace.path),
        "profile": name,
        "scope": scope,
        "account_id": account_id,
        "checks": checks,
        "product_sets": product_sets,
        "ready": not failed,
        "failed_checks": [row["check"] for row in failed],
    }


def list_catalog_products(
    workspace: Workspace,
    requested_profile: str | None = None,
    limit: int = 100,
) -> dict[str, Any]:
    name, profile = workspace.profile(requested_profile)
    catalog_id = str(profile.get("catalog_id") or "")
    if not catalog_id:
        raise ValueError(f"profile {name} has no catalog_id")
    rows = _edge(f"{catalog_id}/products", "id,retailer_id,name", max_rows=limit)
    return {
        "workspace": str(workspace.path),
        "profile": name,
        "catalog_id": catalog_id,
        "count": len(rows),
        "products": rows,
    }


def verify_product_set_binding(
    workspace: Workspace,
    requested_profile: str | None,
    alias: str,
) -> dict[str, Any]:
    """Verify catalog/set ownership for repair without requiring the set to be non-empty."""
    name, profile = workspace.profile(requested_profile)
    catalog_id = str(profile.get("catalog_id") or "")
    set_id = str((profile.get("product_sets") or {}).get(alias) or "")
    if not catalog_id or not set_id:
        raise ValueError(f"profile {name} has no declared product set {alias!r}")
    assigned = _edge(f"{profile['system_user_id']}/assigned_product_catalogs")
    catalog = graph.get(
        catalog_id,
        params={"fields": "id,business{id}"},
        context="repair catalog ownership",
    )
    product_set = graph.get(
        set_id,
        params={"fields": "id,product_catalog{id}"},
        context="repair product-set ownership",
    )
    actual_catalog = str((product_set.get("product_catalog") or {}).get("id") or "")
    actual_business = str((catalog.get("business") or {}).get("id") or "")
    checks = {
        "catalog_assigned": catalog_id in _ids(assigned),
        "catalog_owned": actual_business == str(profile["business_id"]),
        "product_set_catalog": actual_catalog == catalog_id,
    }
    return {
        "profile": name,
        "catalog_id": catalog_id,
        "product_set_id": set_id,
        "checks": checks,
        "ready": all(checks.values()),
    }
