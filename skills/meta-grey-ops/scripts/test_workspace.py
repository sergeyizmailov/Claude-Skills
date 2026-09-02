#!/usr/bin/env python3
"""Offline tests for the workspace and asset-graph contracts."""

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import asset_graph
import jsonschema
import meta_workspace
import metaops

HERE = pathlib.Path(__file__).resolve().parent
SCHEMA_DIR = HERE.parent / "schemas"


def valid_workspace() -> dict:
    return {
        "schema": meta_workspace.WORKSPACE_SCHEMA,
        "name": "test-workspace",
        "api_version": metaops.graph.API_VERSION,
        "blocked_accounts": ["act_99"],
        "profiles": {
            "test": {
                "business_id": "10",
                "app_id": "11",
                "system_user_id": "12",
                "ad_account_id": "act_13",
                "page_id": "14",
                "instagram_user_id": "auto",
                "dataset_id": "15",
                "catalog_id": "16",
                "product_sets": {"main": "17"},
                "currency": "USD",
                "timezone": "Europe/Warsaw",
            }
        },
        "defaults": {
            "profile": "test",
            "token_env": "TEST_META_TOKEN",
            "allow_no_proxy": True,
            "state_dir": ".metaops",
        },
    }


class WorkspaceTests(unittest.TestCase):
    def write_workspace(self, root: pathlib.Path, data: dict | None = None) -> pathlib.Path:
        path = root / "workspace.json"
        path.write_text(json.dumps(data or valid_workspace()), encoding="utf-8")
        return path

    def test_loads_directory_and_resolves_state_root(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.write_workspace(root)
            workspace = meta_workspace.load_workspace(str(root))
            self.assertEqual(workspace.path, (root / "workspace.json").resolve())
            self.assertEqual(workspace.state_root, (root / ".metaops").resolve())
            self.assertEqual(workspace.profile_name(), "test")

    def test_rejects_workspace_inside_a_skill_store(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td) / ".claude" / "skills" / "campaign-project"
            root.mkdir(parents=True)
            self.write_workspace(root)
            with self.assertRaisesRegex(meta_workspace.WorkspaceError, "outside skill stores"):
                meta_workspace.load_workspace(str(root))

    def test_rejects_state_directory_outside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td) / "campaign-project"
            root.mkdir()
            data = valid_workspace()
            data["defaults"]["state_dir"] = "../shared-state"
            self.write_workspace(root, data)
            with self.assertRaisesRegex(meta_workspace.WorkspaceError, "stay inside the workspace"):
                meta_workspace.load_workspace(str(root))

    def test_discovers_workspace_from_nested_directory(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            nested = root / "one" / "two"
            nested.mkdir(parents=True)
            workspace_path = self.write_workspace(root).resolve()
            self.assertEqual(meta_workspace.discover_workspace(nested), workspace_path)

    def test_rejects_blocked_or_duplicate_account(self) -> None:
        blocked = valid_workspace()
        blocked["profiles"]["test"]["ad_account_id"] = "act_99"
        with self.assertRaisesRegex(meta_workspace.WorkspaceError, "blocked account"):
            meta_workspace.validate_workspace(blocked)

        duplicate = valid_workspace()
        duplicate["profiles"]["second"] = dict(duplicate["profiles"]["test"])
        with self.assertRaisesRegex(meta_workspace.WorkspaceError, "duplicate ad account"):
            meta_workspace.validate_workspace(duplicate)

    def test_runtime_validation_matches_published_shape(self) -> None:
        malformed = valid_workspace()
        malformed["blocked_accounts"] = "act_99"
        with self.assertRaisesRegex(meta_workspace.WorkspaceError, "must be an array"):
            meta_workspace.validate_workspace(malformed)
        unknown = valid_workspace()
        unknown["defaults"]["profil"] = "test"
        with self.assertRaisesRegex(meta_workspace.WorkspaceError, "unsupported keys"):
            meta_workspace.validate_workspace(unknown)
        wrong_type = valid_workspace()
        wrong_type["profiles"]["test"]["product_sets"]["main"] = 17
        with self.assertRaisesRegex(meta_workspace.WorkspaceError, "must be a string"):
            meta_workspace.validate_workspace(wrong_type)

    def test_published_workspace_schema_accepts_runtime_fixture(self) -> None:
        schema = json.loads((SCHEMA_DIR / "workspace.v1.json").read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema).validate(valid_workspace())

        malformed = valid_workspace()
        malformed["profiles"]["test"]["unexpected"] = "drift"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(schema).validate(malformed)

    def test_resolve_spec_injects_routing_and_product_set(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.write_workspace(root)
            workspace = meta_workspace.load_workspace(str(root))
            profile, spec = meta_workspace.resolve_spec(
                {
                    "run_id": "run-1",
                    "adsets": [{"ads": [{"creative": {"product_set": "main"}}]}],
                },
                workspace,
            )
            self.assertEqual(profile, "test")
            self.assertEqual(spec["account_id"], "act_13")
            self.assertEqual(spec["page_id"], "14")
            self.assertEqual(spec["pixel_id"], "15")
            creative = spec["adsets"][0]["ads"][0]["creative"]
            self.assertNotIn("product_set", creative)
            self.assertEqual(creative["product_set_id"], "17")

    def test_resolve_spec_rejects_cross_profile_routing(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.write_workspace(root)
            workspace = meta_workspace.load_workspace(str(root))
            with self.assertRaisesRegex(meta_workspace.WorkspaceError, "conflicts with profile"):
                meta_workspace.resolve_spec({"account_id": "act_999"}, workspace)

    def test_resolve_spec_rejects_undeclared_nested_assets(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.write_workspace(root)
            workspace = meta_workspace.load_workspace(str(root))
            raw = {
                "adsets": [{
                    "promoted_object": {"pixel_id": "999"},
                    "ads": [{"creative": {"product_set_id": "888"}}],
                }]
            }
            with self.assertRaisesRegex(meta_workspace.WorkspaceError, "promoted_object.pixel_id"):
                meta_workspace.resolve_spec(raw, workspace)

    def test_workspace_bulk_rejects_unprofiled_account(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.write_workspace(root)
            workspace = meta_workspace.load_workspace(str(root))
            with self.assertRaisesRegex(metaops.MetaOpsError, "not an allowed workspace profile"):
                metaops.workspace_bulk_rows(workspace, [{"account_id": "act_99"}])

    def test_bulk_catalog_override_requires_all_scope(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.write_workspace(root)
            workspace = meta_workspace.load_workspace(str(root))
            template = {"adsets": [{"ads": [{"creative": {"kind": "link_image"}}]}]}
            rows = [{
                "account_id": "act_13",
                "workspace_profile": "test",
                "overrides": {
                    "adsets": [{"ads": [{"creative": {
                        "kind": "catalog_single",
                        "product_set_id": "17",
                    }}]}]
                },
            }]
            with mock.patch.object(
                metaops,
                "require_assets",
                return_value=(root / "assets.json", "sha"),
            ) as require:
                bindings = metaops.bind_bulk_assets(workspace, template, rows)
            require.assert_called_once_with(workspace, "test", True)
            self.assertTrue(bindings[0]["catalog_required"])

    def test_workspace_validate_is_one_json_result(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.write_workspace(root)
            proc = subprocess.run(
                [
                    sys.executable,
                    str(HERE / "metaops.py"),
                    "--workspace",
                    str(root),
                    "--json",
                    "workspace",
                    "validate",
                ],
                cwd=HERE,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            rows = proc.stdout.splitlines()
            self.assertEqual(len(rows), 1)
            self.assertEqual(json.loads(rows[0])["phase"], "valid")

    def test_workspace_can_map_a_custom_token_environment_variable(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.write_workspace(root)
            with mock.patch.dict(os.environ, {"TEST_META_TOKEN": "TOKEN"}, clear=True):
                metaops.configure_workspace(str(root))
                self.assertEqual(os.environ["META_TOKEN"], "TOKEN")
                self.assertEqual(metaops.graph._WRITE_ACCOUNTS, {"act_13"})

    def test_workspace_doctor_rejects_explicit_routing_override(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.write_workspace(root)
            workspace = meta_workspace.load_workspace(str(root))
            args = type("Args", (), {
                "workspace_obj": workspace,
                "profile": "test",
                "account": "act_999",
                "page": None,
                "dataset": None,
                "business": None,
                "whoami": False,
                "create_pbia": False,
                "attach_pixel": False,
                "timeout": 10,
            })()
            with self.assertRaisesRegex(metaops.MetaOpsError, "conflicts with workspace profile"):
                metaops.command_doctor(args)

    def test_workspace_whoami_does_not_inject_profile_routing(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.write_workspace(root)
            workspace = meta_workspace.load_workspace(str(root))
            args = type("Args", (), {
                "workspace_obj": workspace,
                "profile": "test",
                "account": None,
                "page": None,
                "dataset": None,
                "business": None,
                "whoami": True,
                "create_pbia": False,
                "attach_pixel": False,
                "timeout": 10,
            })()
            child = metaops.ChildResult(["probe.py"], 0, "", "")
            with mock.patch.object(metaops, "run_child", return_value=child) as run:
                code, payload = metaops.command_doctor(args)
            self.assertEqual(code, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["artifacts"], {})
            run.assert_called_once_with("probe.py", ["--whoami"], 10)


class AssetGraphTests(unittest.TestCase):
    def test_edge_limit_stops_pagination(self) -> None:
        page = {
            "data": [{"id": "1"}],
            "paging": {"cursors": {"after": "cursor"}, "next": "https://next"},
        }
        with mock.patch.object(asset_graph.graph, "get", return_value=page) as get:
            rows = asset_graph._edge("catalog/products", max_rows=1)
        self.assertEqual(rows, [{"id": "1"}])
        get.assert_called_once()

    def test_empty_declared_product_set_blocks_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self_path = root / "workspace.json"
            self_path.write_text(json.dumps(valid_workspace()), encoding="utf-8")
            workspace = meta_workspace.load_workspace(str(root))

            objects = {
                "10": {"id": "10", "name": "BM", "verification_status": "verified"},
                "act_13": {
                    "id": "act_13",
                    "name": "Account",
                    "account_status": 1,
                    "disable_reason": 0,
                    "currency": "USD",
                    "timezone_name": "Europe/Warsaw",
                    "funding_source_details": {"id": "funding"},
                    "business": {"id": "10"},
                },
                "15": {"id": "15", "name": "Dataset"},
                "16": {
                    "id": "16",
                    "name": "Catalog",
                    "product_count": 21,
                    "business": {"id": "10"},
                },
                "17": {
                    "id": "17",
                    "name": "Main",
                    "product_count": 0,
                    "product_catalog": {"id": "16"},
                },
                "14/page_backed_instagram_accounts": {"data": [{"id": "18"}]},
            }
            edges = {
                "10/owned_apps": [{"id": "11"}],
                "10/system_users": [{"id": "12"}],
                "12/assigned_ad_accounts": [{"id": "act_13"}],
                "12/assigned_pages": [{"id": "14"}],
                "act_13/adspixels": [{"id": "15"}],
                "12/assigned_product_catalogs": [{"id": "16"}],
            }

            def fake_get(path: str, **kwargs: object) -> dict:
                del kwargs
                if path in edges:
                    return {"data": edges[path]}
                return objects[path]

            with (
                mock.patch.object(asset_graph.graph, "get", side_effect=fake_get),
                mock.patch.object(asset_graph.graph, "page_token", return_value="PAGE_TOKEN"),
            ):
                report = asset_graph.verify_assets(workspace)
                core_report = asset_graph.verify_assets(workspace, scope="core")
            self.assertFalse(report["ready"])
            self.assertEqual(report["failed_checks"], ["product_set:main"])
            self.assertTrue(core_report["ready"])
            self.assertEqual(core_report["scope"], "core")

    def test_catalog_plan_requires_all_scope_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            workspace_path = root / "workspace.json"
            workspace_path.write_text(json.dumps(valid_workspace()), encoding="utf-8")
            workspace = meta_workspace.load_workspace(str(root))
            with mock.patch.object(metaops, "PLAN_DIR", root / ".metaops" / "plans"):
                core_path = metaops.asset_receipt_path("test", "core")
                metaops.atomic_json(core_path, {
                    "schema": metaops.ASSET_RECEIPT_SCHEMA,
                    "checked_at": metaops.now_utc(),
                    "api_version": metaops.graph.API_VERSION,
                    "workspace_sha": metaops.file_sha(workspace.path),
                    "profile": "test",
                    "scope": "core",
                })
                self.assertEqual(metaops.require_assets(workspace, "test", False)[0], core_path)
                with self.assertRaisesRegex(metaops.MetaOpsError, "assets verify --scope all"):
                    metaops.require_assets(workspace, "test", True)


if __name__ == "__main__":
    unittest.main()
