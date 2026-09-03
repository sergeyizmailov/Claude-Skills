#!/usr/bin/env python3
"""Offline contract tests for metaops.py. No network or real credentials."""

from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import feed_upload
import jsonschema
import mcp
import metaops
import monitor
import probe
import verify

os.environ.setdefault("META_TOKEN", "TEST_TOKEN")


HERE = pathlib.Path(__file__).resolve().parent
SCHEMA_DIR = HERE.parent / "schemas"


def valid_spec(run_id: str = "contract-test") -> dict:
    return {
        "run_id": run_id,
        "account_id": "act_1",
        "page_id": "2",
        "pixel_id": "3",
        "currency": "USD",
        "campaign": {
            "name": "Campaign",
            "objective": "OUTCOME_LEADS",
            "special_ad_categories": [],
            "daily_budget_minor": 1000,
        },
        "adsets": [
            {
                "name": "Ad set",
                "optimization_goal": "OFFSITE_CONVERSIONS",
                "start_time": "2030-01-01T08:00:00+00:00",
                "targeting": {
                    "geo_locations": {"countries": ["TR"]},
                    "advantage_audience": False,
                },
                "ads": [
                    {
                        "name": "Ad",
                        "creative": {
                            "kind": "link_image",
                            "image_hash": "test_hash",
                            "link": "https://example.com/",
                        },
                    }
                ],
            }
        ],
    }


class MetaOpsContractTests(unittest.TestCase):
    def write_json(self, root: pathlib.Path, name: str, value: object) -> pathlib.Path:
        path = root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def write_doctor(self, root: pathlib.Path, account: str = "act_1") -> pathlib.Path:
        return self.write_json(
            root,
            "doctor.json",
            {
                "schema": metaops.DOCTOR_SCHEMA,
                "checked_at": metaops.now_utc(),
                "api_version": metaops.graph.API_VERSION,
                "account_id": account,
                "page_id": "2",
                "dataset_id": "3",
                "business_id": "10",
            },
        )

    def workspace(self, root: pathlib.Path) -> metaops.meta_workspace.Workspace:
        path = self.write_json(
            root,
            "workspace.json",
            {
                "schema": metaops.meta_workspace.WORKSPACE_SCHEMA,
                "name": "contract",
                "api_version": metaops.graph.API_VERSION,
                "blocked_accounts": ["act_99"],
                "profiles": {
                    "test": {
                        "business_id": "10",
                        "app_id": "11",
                        "system_user_id": "12",
                        "ad_account_id": "act_1",
                        "page_id": "2",
                        "dataset_id": "3",
                        "currency": "USD",
                        "timezone": "Europe/Warsaw",
                    }
                },
                "defaults": {"profile": "test", "state_dir": ".metaops"},
            },
        )
        return metaops.meta_workspace.load_workspace(str(path))

    def bind_single_plan(
        self,
        root: pathlib.Path,
        plan: dict,
        workspace: metaops.meta_workspace.Workspace,
    ) -> None:
        doctor = self.write_doctor(root)
        asset = self.write_json(
            root,
            "assets.json",
            {
                "schema": metaops.ASSET_RECEIPT_SCHEMA,
                "checked_at": metaops.now_utc(),
                "api_version": metaops.graph.API_VERSION,
                "workspace_sha": metaops.file_sha(workspace.path),
                "profile": "test",
                "scope": "core",
            },
        )
        plan.update(
            {
                "workspace_path": str(workspace.path),
                "workspace_sha": metaops.file_sha(workspace.path),
                "profile": "test",
                "doctor_receipt": str(doctor.resolve()),
                "doctor_sha": metaops.file_sha(doctor),
                "asset_receipt": str(asset.resolve()),
                "asset_sha": metaops.file_sha(asset),
            }
        )

    def test_single_plan_is_absolute_and_hash_bound(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            spec_path = self.write_json(root, "spec.json", valid_spec())
            plan = metaops.build_single_plan(spec_path)
            self.assertEqual(plan["schema"], metaops.SINGLE_PLAN_SCHEMA)
            self.assertTrue(pathlib.Path(plan["state_path"]).is_absolute())
            self.assertTrue(pathlib.Path(plan["dry_state_path"]).is_absolute())
            self.assertEqual(len(plan["spec_sha"]), 16)

    def test_saved_spec_isolated_from_source_change_and_tamper_evident(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            spec_path = self.write_json(root, "spec.json", valid_spec())
            plan = metaops.build_single_plan(spec_path)
            plan["spec_path"] = str(root / "snapshot.json")
            snapshot = pathlib.Path(plan["spec_path"])
            metaops.atomic_json(snapshot, metaops.load_launch_spec(spec_path))
            workspace = self.workspace(root)
            self.bind_single_plan(root, plan, workspace)
            changed = valid_spec()
            changed["campaign"]["daily_budget_minor"] = 2000
            self.write_json(root, "spec.json", changed)
            resolved, _ = metaops.validate_single_plan(plan, workspace, "test")
            self.assertEqual(resolved, snapshot.resolve())
            snapshot_data = json.loads(snapshot.read_text(encoding="utf-8"))
            snapshot_data["campaign"]["daily_budget_minor"] = 3000
            metaops.atomic_json(snapshot, snapshot_data)
            with self.assertRaisesRegex(metaops.MetaOpsError, "spec changed after plan"):
                metaops.validate_single_plan(plan, workspace, "test")

    def test_invalid_spec_becomes_launcher_error_in_json_mode(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            bad = self.write_json(root, "bad.json", {"account_id": "act_1"})
            proc = subprocess.run(
                [sys.executable, str(HERE / "metaops.py"), "--json", "plan", "--spec", str(bad)],
                cwd=HERE,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 2)
            rows = proc.stdout.splitlines()
            self.assertEqual(len(rows), 1)
            payload = json.loads(rows[0])
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["error"]["kind"], "precondition")

    def test_dlo_requires_an_explicit_static_adset(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            spec = valid_spec()
            spec["adsets"][0]["ads"][0]["creative"]["kind"] = "dlo"
            path = self.write_json(root, "dlo.json", spec)
            with self.assertRaisesRegex(metaops.launch.SpecError, "is_dynamic_creative: false"):
                metaops.launch.load_spec(str(path))
            spec["adsets"][0]["is_dynamic_creative"] = False
            self.write_json(root, "dlo.json", spec)
            self.assertEqual(metaops.launch.load_spec(str(path))["adsets"][0]["is_dynamic_creative"], False)

    def test_verify_receipt_expires_before_activation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            spec = {"adsets": [{"ads": [{}]}]}
            state = {"objects": {"campaign": "1", "adset[0]": "2", "ad[0.0]": "3"},
                     "spec_sha": metaops.launch.spec_hash(spec)}
            state_path = self.write_json(root, "state.json", state)
            verify.write_receipt(str(state_path), "spec.json", spec)
            receipt_path = pathlib.Path(str(state_path) + ".verified.json")
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt["ts"] = "2000-01-01T00:00:00+00:00"
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
            self.assertIn("maximum", metaops.activate.check_receipt(str(state_path), state) or "")

    def test_verify_receipt_ttl_is_configurable_without_import_time_failure(self) -> None:
        checked_at = dt.datetime(2030, 1, 1, tzinfo=dt.timezone.utc)
        with mock.patch.dict(os.environ, {"METAOPS_VERIFY_MAX_AGE_SECONDS": "1"}, clear=False):
            why = metaops.activate.receipt_timestamp_error(
                checked_at.isoformat(), now=checked_at + dt.timedelta(seconds=2)
            )
        self.assertIn("maximum 1s", why or "")
        with mock.patch.dict(os.environ, {"METAOPS_VERIFY_MAX_AGE_SECONDS": "bad"}, clear=False):
            why = metaops.activate.receipt_timestamp_error(checked_at.isoformat(), now=checked_at)
        self.assertIn("must be a positive integer", why or "")

    def test_lock_excludes_concurrent_writer_and_is_removed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            state = pathlib.Path(td) / "state.json"
            lock = pathlib.Path(str(state) + ".metaops.lock")
            with metaops.state_lock(state):
                self.assertTrue(lock.exists())
                with (
                    self.assertRaisesRegex(metaops.MetaOpsError, "locked by another launcher"),
                    metaops.state_lock(state),
                ):
                    pass
            self.assertFalse(lock.exists())

    def test_missing_state_is_not_activation_ready(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            summary = metaops.state_summary(pathlib.Path(td) / "missing.json")
            self.assertEqual(summary["phase"], "planned")
            self.assertFalse(summary["activation_ready"])

    def test_bulk_input_change_invalidates_plan(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            template = valid_spec("template")
            accounts = [{"account_id": "act_1", "page_id": "2", "pixel_id": "3"}]
            template_path = self.write_json(root, "template.json", template)
            accounts_path = self.write_json(root, "accounts.json", accounts)
            workspace = self.workspace(root)
            plan = metaops.build_bulk_plan(
                template_path, accounts_path, "batch", None, workspace
            )
            plan["template_path"] = str(root / "template.snapshot.json")
            plan["accounts_path"] = str(root / "accounts.snapshot.json")
            metaops.atomic_json(pathlib.Path(plan["template_path"]), template)
            metaops.atomic_json(
                pathlib.Path(plan["accounts_path"]),
                metaops.workspace_bulk_rows(
                    workspace, metaops.validated_bulk_rows(accounts, None, "batch")
                ),
            )
            doctor = self.write_doctor(root)
            plan["doctor_receipts"] = [
                {"account_id": "act_1", "path": str(doctor.resolve()),
                 "sha": metaops.file_sha(doctor)}
            ]
            asset = self.write_json(
                root,
                "assets.json",
                {
                    "schema": metaops.ASSET_RECEIPT_SCHEMA,
                    "checked_at": metaops.now_utc(),
                    "api_version": metaops.graph.API_VERSION,
                    "workspace_sha": metaops.file_sha(workspace.path),
                    "profile": "test",
                    "scope": "core",
                },
            )
            plan["asset_receipts"] = [
                {"profile": "test", "path": str(asset.resolve()),
                 "sha": metaops.file_sha(asset), "catalog_required": False}
            ]
            accounts[0]["page_id"] = "4"
            self.write_json(root, "accounts.json", accounts)
            metaops.validate_bulk_plan(plan, workspace)
            snapshot_rows = json.loads(pathlib.Path(plan["accounts_path"]).read_text(encoding="utf-8"))
            snapshot_rows[0]["page_id"] = "5"
            metaops.atomic_json(pathlib.Path(plan["accounts_path"]), snapshot_rows)
            with self.assertRaisesRegex(metaops.MetaOpsError, "changed after plan"):
                metaops.validate_bulk_plan(plan, workspace)

    def test_bulk_rejects_path_tags_and_routing_overrides(self) -> None:
        with self.assertRaises(metaops.MetaOpsError):
            metaops.validated_bulk_rows(
                [{"account_id": "act_1", "tag": "../escape"}], None, "batch"
            )
        with self.assertRaisesRegex(metaops.MetaOpsError, "routing keys"):
            metaops.validated_bulk_rows(
                [{"account_id": "act_1", "overrides": {"account_id": "act_2"}}],
                None,
                "batch",
            )

    def test_state_must_match_plan_before_activation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            state_path = self.write_json(
                root,
                "state.json",
                {"spec_sha": "other", "spec_account": "act_2", "objects": {}},
            )
            plan = {"spec_sha": "expected", "account_id": "act_1"}
            with self.assertRaisesRegex(metaops.MetaOpsError, "different spec"):
                metaops.require_state_binding(plan, state_path)

    def test_mismatched_in_flight_state_is_rejected_before_apply(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            source = self.write_json(root, "source.json", valid_spec())
            state_path = self.write_json(
                root,
                "state.json",
                {"spec_sha": "other", "spec_account": "act_2", "objects": {},
                 "in_flight": {"campaign": {"path": "act_2/campaigns"}}},
            )
            plan = metaops.build_single_plan(source, str(state_path))
            snapshot = root / "snapshot.json"
            plan["spec_path"] = str(snapshot.resolve())
            metaops.atomic_json(snapshot, metaops.load_launch_spec(source))
            workspace = self.workspace(root)
            self.bind_single_plan(root, plan, workspace)
            plan_path = root / "plan.json"
            metaops.atomic_json(plan_path, plan)
            args = type("Args", (), {
                "plan": str(plan_path), "timeout": 10,
                "workspace_obj": workspace, "profile": "test",
            })()
            with (
                mock.patch.object(metaops, "run_child") as child,
                self.assertRaisesRegex(metaops.MetaOpsError, "different spec"),
            ):
                metaops.command_apply(args)
            child.assert_not_called()

    def test_apply_invokes_launch_with_saved_snapshot_and_paused_state(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            source = self.write_json(root, "source.json", valid_spec())
            plan = metaops.build_single_plan(source, str(root / "state.json"))
            snapshot = root / "snapshot.json"
            plan["spec_path"] = str(snapshot.resolve())
            normalized = metaops.load_launch_spec(source)
            metaops.atomic_json(snapshot, normalized)
            workspace = self.workspace(root)
            self.bind_single_plan(root, plan, workspace)
            plan_path = root / "plan.json"
            metaops.atomic_json(plan_path, plan)

            def fake_child(script: str, argv: list[str], _timeout: int) -> metaops.ChildResult:
                self.assertEqual(script, "launch.py")
                self.assertEqual(argv[argv.index("--spec") + 1], str(snapshot.resolve()))
                self.assertNotIn("activate.py", argv)
                self.write_json(
                    root,
                    "state.json",
                    {
                        "spec_sha": plan["spec_sha"],
                        "spec_account": "act_1",
                        "objects": {"campaign": "1", "adset[0]": "2", "ad[0.0]": "3"},
                    },
                )
                return metaops.ChildResult([script, *argv], 0, "", "")

            args = type("Args", (), {
                "plan": str(plan_path), "timeout": 10,
                "workspace_obj": workspace, "profile": "test",
            })()
            with mock.patch.object(metaops, "run_child", side_effect=fake_child):
                code, payload = metaops.command_apply(args)
            self.assertEqual(code, 0)
            self.assertEqual(payload["phase"], "built_paused")

    def test_json_usage_error_is_one_object(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(HERE / "metaops.py"), "--json", "apply"],
            cwd=HERE,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(len(proc.stdout.splitlines()), 1)
        self.assertEqual(json.loads(proc.stdout)["error"]["kind"], "usage")

    def test_refresh_start_requires_offset_and_future_time(self) -> None:
        with self.assertRaises(metaops.MetaOpsError):
            metaops.validate_future_start("2020-01-01T08:00:00")
        with self.assertRaises(metaops.MetaOpsError):
            metaops.validate_future_start("2020-01-01T08:00:00+00:00")

    def test_run_name_rejects_paths(self) -> None:
        with self.assertRaises(metaops.MetaOpsError):
            metaops.safe_name("../escape", "run_id")

    def test_workspace_free_plan_is_rejected_before_side_effects(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            spec = self.write_json(root, "spec.json", valid_spec())
            proc = subprocess.run(
                [sys.executable, str(HERE / "metaops.py"), "--json", "plan", "--spec", str(spec)],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
                env={key: value for key, value in os.environ.items()
                     if key != "METAOPS_WORKSPACE"},
            )
            self.assertEqual(proc.returncode, 2)
            payload = json.loads(proc.stdout)
            self.assertIn("requires a workspace", payload["error"]["message"])
            self.assertFalse((root / ".metaops").exists())

    def test_invalid_timeout_environment_still_returns_one_json_envelope(self) -> None:
        env = dict(os.environ, METAOPS_TIMEOUT_SECONDS="not-an-integer")
        proc = subprocess.run(
            [sys.executable, str(HERE / "metaops.py"), "--json", "doctor", "--whoami"],
            cwd=HERE,
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )
        self.assertEqual(proc.returncode, 2)
        payload = json.loads(proc.stdout)
        self.assertFalse(payload["ok"])
        self.assertIn("METAOPS_TIMEOUT_SECONDS", payload["error"]["message"])

    def test_low_level_graph_write_requires_metaops_authority(self) -> None:
        with (
            mock.patch.dict(os.environ, {"META_TOKEN": "TEST_TOKEN"}, clear=True),
            mock.patch.object(metaops.graph, "_WRITE_ACCOUNTS", None),
            mock.patch.object(metaops.graph, "_WRITE_CAPABILITY_LOADED", True),
            mock.patch.object(metaops.graph, "session") as session,
            self.assertRaisesRegex(SystemExit, "direct Graph POST is disabled"),
        ):
            metaops.graph.post("act_1/campaigns", {"name": "blocked"})
        session.assert_not_called()

    def test_low_level_graph_write_rejects_an_empty_workspace_capability(self) -> None:
        with (
            mock.patch.dict(os.environ, {"META_TOKEN": "TEST_TOKEN"}, clear=True),
            mock.patch.object(metaops.graph, "_WRITE_ACCOUNTS", set()),
            mock.patch.object(metaops.graph, "_WRITE_CAPABILITY_LOADED", True),
            mock.patch.object(metaops.graph, "session") as session,
            self.assertRaisesRegex(SystemExit, "direct Graph POST is disabled"),
        ):
            metaops.graph.post("123/anything", {"name": "blocked"})
        session.assert_not_called()

    def test_low_level_graph_write_rejects_account_outside_workspace(self) -> None:
        with (
            mock.patch.dict(os.environ, {"META_TOKEN": "TEST_TOKEN"}, clear=True),
            mock.patch.object(metaops.graph, "_WRITE_ACCOUNTS", {"act_1"}),
            mock.patch.object(metaops.graph, "_WRITE_CAPABILITY_LOADED", True),
            mock.patch.object(metaops.graph, "session") as session,
            self.assertRaisesRegex(SystemExit, "does not authorize.*act_99"),
        ):
            metaops.graph.post("act_99/campaigns", {"name": "blocked"})
        session.assert_not_called()

    def test_absolute_graph_url_cannot_bypass_account_or_host_gate(self) -> None:
        with (
            mock.patch.object(metaops.graph, "_WRITE_ACCOUNTS", {"act_1"}),
            mock.patch.object(metaops.graph, "_WRITE_CAPABILITY_LOADED", True),
            mock.patch.object(metaops.graph, "session") as session,
            self.assertRaisesRegex(SystemExit, "does not authorize.*act_99"),
        ):
            metaops.graph.post(
                "https://graph.facebook.com/v26.0/act_99/campaigns", {"name": "blocked"}
            )
        session.assert_not_called()

        with (
            mock.patch.object(metaops.graph, "session") as session,
            self.assertRaisesRegex(SystemExit, "outside https://graph.facebook.com"),
        ):
            metaops.graph.get("https://example.com/collect")
        session.assert_not_called()

    def test_provisioning_admin_binds_the_token_to_workspace_role(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            workspace = self.workspace(pathlib.Path(td))

            def fake_get(path, params=None, context=""):
                if path == "me":
                    self.assertEqual(params, {"fields": "id,name"})
                    return {"id": "12", "name": "Launcher"}
                self.assertEqual(path, "10/system_users")
                self.assertEqual(params, {"fields": "id,name,role", "limit": 500})
                return {"data": [{"id": "12", "name": "Launcher", "role": "ADMIN"}]}

            with mock.patch.object(metaops.graph, "get", side_effect=fake_get) as get:
                result = metaops.require_provisioning_admin(workspace, "test")
            self.assertEqual(result["role"], "ADMIN")
            self.assertEqual(result["system_user_id"], "12")
            self.assertEqual(get.call_count, 2)

    def test_provisioning_rejects_employee_system_user(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            workspace = self.workspace(pathlib.Path(td))
            responses = [
                {"id": "12", "name": "Launcher"},
                {"data": [{"id": "12", "name": "Launcher", "role": "EMPLOYEE"}]},
            ]
            with mock.patch.object(metaops.graph, "get", side_effect=responses):
                with self.assertRaisesRegex(metaops.MetaOpsError, "requires an ADMIN"):
                    metaops.require_provisioning_admin(workspace, "test")

    def test_provisioning_rejects_a_token_other_than_workspace_system_user(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            workspace = self.workspace(pathlib.Path(td))
            with mock.patch.object(metaops.graph, "get", return_value={"id": "99", "name": "Other"}) as get:
                with self.assertRaisesRegex(metaops.MetaOpsError, "workspace System User token"):
                    metaops.require_provisioning_admin(workspace, "test")
            get.assert_called_once()

    def test_only_whoami_doctor_is_workspace_free(self) -> None:
        blocked = type("Args", (), {
            "command": "doctor", "whoami": False, "workspace_obj": None,
        })()
        with self.assertRaisesRegex(metaops.MetaOpsError, "account-targeted doctor"):
            metaops.require_command_workspace(blocked)
        allowed = type("Args", (), {
            "command": "doctor", "whoami": True, "workspace_obj": None,
        })()
        metaops.require_command_workspace(allowed)
        provisioning = type("Args", (), {
            "command": "doctor", "whoami": True, "workspace_obj": None, "scope": "provisioning",
        })()
        with self.assertRaisesRegex(metaops.MetaOpsError, "scope provisioning requires a workspace"):
            metaops.require_command_workspace(provisioning)

    def test_state_summary_does_not_claim_past_spec_ready_for_activation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            spec = valid_spec()
            spec["adsets"][0]["start_time"] = "2000-01-01T08:00:00+00:00"
            spec_path = self.write_json(root, "spec.json", spec)
            state_path = self.write_json(root, "state.json", {
                "objects": {"campaign": "1", "adset[0]": "2", "ad[0.0]": "3"},
                "in_flight": {}, "errors": [],
            })
            with mock.patch.object(metaops.activate, "check_receipt", return_value=None):
                summary = metaops.state_summary(state_path, spec_path)
            self.assertFalse(summary["activation_ready"])
            self.assertIn("start_time is past", summary["activation_blocker"])

    def test_plan_cannot_move_to_another_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_workspace = self.workspace(pathlib.Path(first))
            second_workspace = self.workspace(pathlib.Path(second))
            plan = {
                "workspace_path": str(first_workspace.path),
                "workspace_sha": metaops.file_sha(first_workspace.path),
                "profile": "test",
            }
            with self.assertRaisesRegex(metaops.MetaOpsError, "does not match"):
                metaops.require_plan_workspace(plan, second_workspace, "test")

    def test_mcp_blocks_every_mutating_tool_before_network(self) -> None:
        for name in (
            "ads_activate_entity",
            "ads_create_campaign",
            "ads_catalog_update_product_set",
            "ads_pixel_event_delete",
        ):
            with self.assertRaisesRegex(SystemExit, "read-only allowlist"):
                mcp.require_read_only_tool(name)
        mcp.require_read_only_tool("ads_get_ad_entities")
        mcp.require_read_only_tool("ads_catalog_list_products")

    def test_doctor_receipt_is_bound_to_business(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            receipt = self.write_doctor(root)
            with self.assertRaisesRegex(metaops.MetaOpsError, "business_id mismatch"):
                metaops.require_doctor(valid_spec(), str(receipt), "999")

    def test_dry_run_refuses_missing_pbia_for_instagram_placements(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            raw = valid_spec()
            raw["instagram_user_id"] = "auto"
            spec = metaops.load_launch_spec(self.write_json(root, "spec.json", raw))
            state = metaops.launch.State(str(root / "dry.json"))
            with (
                mock.patch.object(metaops.launch, "account_currency", return_value="USD"),
                mock.patch.object(metaops.launch, "resolve_identity", return_value=None),
                self.assertRaisesRegex(metaops.launch.SpecError, "no PBIA"),
            ):
                metaops.launch.run(spec, state, True)

    def test_media_routes_upload_to_workspace_profile(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            workspace = self.workspace(root)
            image = root / "creative.jpg"
            image.write_bytes(b"image")
            manifest = root / "output" / "media.json"
            args = type("Args", (), {
                "workspace_obj": workspace,
                "profile": "test",
                "image": [str(image)],
                "video": [],
                "manifest": str(manifest),
                "timeout": 10,
            })()

            def fake_child(script: str, argv: list[str], _timeout: int) -> metaops.ChildResult:
                self.assertEqual(script, "media.py")
                self.assertEqual(argv[argv.index("--account") + 1], "act_1")
                metaops.atomic_json(manifest, {"account_id": "act_1"})
                return metaops.ChildResult([script, *argv], 0, "", "")

            with (
                mock.patch.object(metaops, "require_assets", return_value=(root, "sha")),
                mock.patch.object(metaops, "require_doctor", return_value=(root, "sha")),
                mock.patch.object(metaops, "run_child", side_effect=fake_child),
            ):
                code, payload = metaops.command_media(args)
            self.assertEqual(code, 0)
            self.assertEqual(payload["artifacts"]["manifest"], str(manifest.resolve()))

    def test_product_set_mutation_rejects_wrong_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            data = json.loads(self.workspace(root).path.read_text(encoding="utf-8"))
            data["profiles"]["test"]["catalog_id"] = "16"
            data["profiles"]["test"]["product_sets"] = {"main": "17"}
            workspace = metaops.meta_workspace.load_workspace(
                str(self.write_json(root, "workspace.json", data))
            )
            args = type("Args", (), {
                "workspace_obj": workspace,
                "profile": "test",
                "set": "main",
                "retailer_ids": "sku-1",
                "confirm": "SET",
                "timeout": 10,
            })()
            with (
                mock.patch.object(metaops, "require_assets", return_value=(root, "sha")),
                mock.patch.object(metaops, "require_doctor", return_value=(root, "sha")),
                mock.patch.object(
                    metaops.asset_graph,
                    "verify_product_set_binding",
                    return_value={
                        "ready": False,
                        "checks": {"product_set_catalog": False},
                    },
                ),
                mock.patch.object(metaops, "run_child") as child,
                self.assertRaisesRegex(metaops.MetaOpsError, "repair binding failed"),
            ):
                metaops.command_assets_set_products(args)
            child.assert_not_called()

    def test_bulk_activate_targets_one_bound_account(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            workspace = self.workspace(root)
            spec_path = self.write_json(root, "item.json", valid_spec("bulk-one"))
            spec = metaops.load_launch_spec(spec_path)
            state_path = self.write_json(
                root,
                "state.json",
                {
                    "spec_sha": metaops.launch.spec_hash(spec),
                    "spec_account": "act_1",
                    "objects": {"campaign": "1", "adset[0]": "2", "ad[0.0]": "3"},
                },
            )
            item = {
                "account_id": "act_1",
                "run_id": "bulk-one",
                "spec_path": str(spec_path.resolve()),
                "spec_sha": metaops.launch.spec_hash(spec),
                "state_path": str(state_path.resolve()),
            }
            plan_path = self.write_json(
                root,
                "bulk-plan.json",
                {
                    "schema": metaops.BULK_PLAN_SCHEMA,
                    "api_version": metaops.graph.API_VERSION,
                    "items": [item],
                },
            )
            args = type("Args", (), {
                "plan": str(plan_path),
                "account": "1",
                "confirm": "SPEND",
                "confirm_ui": "REVIEWED",
                "refresh_start": None,
                "timeout": 10,
                "workspace_obj": workspace,
            })()
            child = metaops.ChildResult(["activate.py"], 0, "", "")
            with (
                mock.patch.object(metaops, "validate_bulk_plan") as validate_plan,
                mock.patch.object(metaops, "validate_bulk_items", return_value=[item]),
                mock.patch.object(metaops, "run_child", return_value=child) as run,
            ):
                code, payload = metaops.command_bulk_activate(args)
            self.assertEqual(code, 0)
            self.assertEqual(payload["data"]["account_id"], "act_1")
            run.assert_called_once_with(
                "activate.py", ["--state", str(state_path.resolve()), "--confirm", "SPEND"], 10
            )
            self.assertEqual(validate_plan.call_count, 2)
            for call in validate_plan.call_args_list:
                self.assertEqual(call.args[2], {"act_1"})

    def test_result_envelope_matches_published_schema(self) -> None:
        schema = json.loads((SCHEMA_DIR / "result.v1.json").read_text(encoding="utf-8"))
        payload = metaops.result_envelope("test", True, "valid")
        jsonschema.Draft202012Validator(schema).validate(payload)

    def test_graph_session_rebuilds_when_proxy_configuration_changes(self) -> None:
        old_session = object()
        new_session = object()
        with (
            mock.patch.object(metaops.graph, "_SESSION", old_session),
            mock.patch.object(metaops.graph, "_SESSION_CONFIG", ("socks5h://old", "")),
            mock.patch.dict(
                os.environ,
                {"META_PROXY": "socks5h://new", "META_ALLOW_NO_PROXY": ""},
                clear=False,
            ),
            mock.patch.object(metaops.graph, "_session", return_value=new_session) as rebuild,
        ):
            self.assertIs(metaops.graph.session(), new_session)
        rebuild.assert_called_once_with()

    def test_json_parse_error_names_a_new_command(self) -> None:
        with mock.patch.object(sys, "argv", ["metaops", "--json", "monitor"]):
            with self.assertRaises(SystemExit) as exit_info, mock.patch("builtins.print") as printed:
                metaops.parser().error("the following arguments are required: --accounts")
        self.assertEqual(exit_info.exception.code, 2)
        payload = json.loads(printed.call_args.args[0])
        self.assertEqual(payload["command"], "monitor")

    def test_global_json_survives_monitor_subparser(self) -> None:
        parsed = metaops.parser().parse_args(["--json", "monitor", "--accounts", "act_1"])
        self.assertTrue(parsed.json)
        self.assertIsNone(parsed.out_json)




class FeedAndMonitorTests(unittest.TestCase):
    def test_feed_upload_polls_until_end_time(self) -> None:
        states = [{"id": "u1"}, {"id": "u1", "end_time": "t", "num_persisted_items": 3, "error_count": 0}]
        with (
            mock.patch.object(feed_upload.graph, "get", side_effect=lambda *a, **k: states.pop(0)),
            mock.patch.object(feed_upload.time, "sleep"),
        ):
            u = feed_upload.poll("u1", wait_s=60)
        self.assertTrue(feed_upload.finished(u))
        self.assertEqual(u["num_persisted_items"], 3)

    def test_feed_upload_start_posts_url(self) -> None:
        with mock.patch.object(feed_upload.graph, "post", return_value={"id": "u9"}) as post:
            self.assertEqual(feed_upload.start("77", "https://x/export?format=csv&gid=0", True), "u9")
        self.assertEqual(post.call_args.args[0], "77/uploads")
        self.assertEqual(post.call_args.args[1], {"url": "https://x/export?format=csv&gid=0", "update_only": True})

    def test_monitor_stall_heuristic(self) -> None:
        rows = [{"id": "1", "impressions": 45, "clicks": 0}, {"id": "2", "impressions": 45, "clicks": 1},
                {"id": "3", "impressions": 10, "clicks": 0}]
        self.assertEqual([r["id"] for r in monitor.stalled(rows)], ["1"])
        self.assertEqual(monitor.stalled(rows, 5), [rows[0], rows[2]])

    def test_feed_swap_gate_blocks_ads_in_review(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            ws = MetaOpsContractTests().workspace(root)
            items = MetaOpsContractTests().write_json(root, "items.json", [{"id": "SKU1", "link": "https://a/"}])
            args = type("Args", (), {"workspace_obj": ws, "profile": "test", "feed_id": "5", "sheet": "abc",
                                     "tab": "products", "gid": 0, "url": None, "update_only": False,
                                     "wait": 1, "timeout": 5, "file": str(items), "force": False,
                                     "confirm": "FEED"})()
            with mock.patch.object(metaops, "ad_statuses", return_value={"a1": "PENDING_REVIEW"}):
                with self.assertRaisesRegex(metaops.MetaOpsError, "swap gate"):
                    metaops.command_feed_swap(args)

    def test_feed_swap_validates_prospective_rows_before_sheet_write(self) -> None:
        import sheetfeed
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            ws = MetaOpsContractTests().workspace(root)
            args = type("Args", (), {"workspace_obj": ws, "profile": "test", "feed_id": "5", "sheet": "abc",
                                     "tab": "products", "gid": 0, "url": None, "update_only": False,
                                     "wait": 1, "timeout": 5, "file": str(root / "items.json"), "force": False,
                                     "confirm": "FEED"})()
            sheet = mock.Mock()
            sheet.read.return_value = (["id"], [])  # Missing required feed columns.
            with (
                mock.patch.object(sheetfeed, "load_items", return_value=[{"id": "SKU1"}]),
                mock.patch.object(sheetfeed, "Sheet", return_value=sheet),
                mock.patch.object(metaops, "ad_statuses", return_value={}),
                mock.patch.object(metaops, "run_feed_upload") as upload,
            ):
                code, payload = metaops.command_feed_swap(args)
            self.assertEqual(code, 1)
            self.assertEqual(payload["phase"], "sheet_invalid")
            sheet.upsert.assert_not_called()
            upload.assert_not_called()

    def test_feed_binding_requires_feed_id(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws = MetaOpsContractTests().workspace(pathlib.Path(td))
            args = type("Args", (), {"workspace_obj": ws, "profile": "test", "feed_id": None})()
            with self.assertRaisesRegex(metaops.MetaOpsError, "no feed id"):
                metaops.feed_binding(args)
            args.feed_id = "42"
            self.assertEqual(metaops.feed_binding(args)[2], "42")

    def test_whoami_returns_nonzero_when_a_required_gate_fails(self) -> None:
        def fail_gate(report):
            report.add("token", probe.FAIL, "expired")

        with (
            mock.patch.object(probe.sys, "argv", ["probe.py", "--whoami"]),
            mock.patch.object(probe, "gate_identity", side_effect=fail_gate),
            mock.patch.object(probe, "gate_token_debug"),
            mock.patch.object(probe, "gate_scopes"),
            mock.patch.object(probe, "gate_visible_accounts"),
            mock.patch.object(probe, "whoami_verdict"),
        ):
            self.assertEqual(probe.main(), 1)

    def test_pixel_gate_follows_pagination_before_declaring_missing(self) -> None:
        report = probe.Report()
        first = {"data": [{"id": "first"}], "paging": {"cursors": {"after": "cursor-2"}, "next": "yes"}}
        second = {"data": [{"id": "wanted"}]}
        with mock.patch.object(probe.graph, "get", side_effect=[first, second]) as get:
            probe.gate_pixel_attached(report, "act_1", "wanted", None, False)
        self.assertEqual(get.call_count, 2)
        self.assertEqual(report.rows[-1]["state"], probe.PASS)

    def test_monitor_adset_queries_follow_pagination(self) -> None:
        pages = [
            {"data": [{"id": "a1", "issues_info": {"error_code": 1}}], "paging": {"cursors": {"after": "cursor"}, "next": "next"}},
            {"data": [{"id": "a2", "issues_info": {"error_code": 2}}]},
        ]
        with mock.patch.object(monitor.graph, "get", side_effect=lambda *a, **k: pages.pop(0)) as get:
            issues = monitor.adset_issues("act_1")
        self.assertEqual([issue["id"] for issue in issues], ["a1", "a2"])
        self.assertEqual(get.call_count, 2)

    def test_workspace_schema_accepts_feed_id(self) -> None:
        schema = json.loads((SCHEMA_DIR / "workspace.v1.json").read_text(encoding="utf-8"))
        doc = json.loads((HERE / "specs" / "example-workspace.json").read_text(encoding="utf-8"))
        prof = doc["profiles"].pop("<profile>")
        doc["profiles"]["p1"] = prof
        doc["defaults"]["profile"] = "p1"
        prof.update({"business_id": "1", "app_id": "1", "system_user_id": "1", "ad_account_id": "act_1",
                     "page_id": "1", "dataset_id": "1", "catalog_id": "1", "feed_id": "9",
                     "product_sets": {"main": "1"}})
        jsonschema.validate(doc, schema)

    def test_uniquify_no_crop_keeps_dimensions(self) -> None:
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("pillow not installed")
        import uniquify
        with tempfile.TemporaryDirectory() as td:
            src = pathlib.Path(td) / "a.jpg"
            Image.new("RGB", (64, 48), (200, 30, 30)).save(src, "JPEG")
            dst = pathlib.Path(td) / "a.v01.jpg"
            uniquify.uniq_image(src, dst, uniquify.seed_for(src, "v01"), crop=False)
            with Image.open(dst) as image:
                self.assertEqual(image.size, (64, 48))
            self.assertNotEqual(src.read_bytes(), dst.read_bytes())
            report = uniquify.image_report(src, dst)
            self.assertTrue(report["same_size"])
            self.assertLessEqual(report["dhash"], 8)
            self.assertLessEqual(report["phash"], 8)

    def test_uniquify_hashes_separate_distinct_images(self) -> None:
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            self.skipTest("pillow not installed")
        import uniquify
        a = Image.new("L", (64, 64), 0)
        ImageDraw.Draw(a).rectangle((0, 0, 31, 63), fill=255)
        b = Image.new("L", (64, 64), 0)
        ImageDraw.Draw(b).rectangle((0, 0, 63, 31), fill=255)
        self.assertEqual(uniquify.hamming(uniquify.dhash(a), uniquify.dhash(a)), 0)
        self.assertGreater(uniquify.hamming(uniquify.dhash(a), uniquify.dhash(b)), 8)
        self.assertGreater(uniquify.hamming(uniquify.phash(a), uniquify.phash(b)), 8)

if __name__ == "__main__":
    unittest.main(verbosity=2)
