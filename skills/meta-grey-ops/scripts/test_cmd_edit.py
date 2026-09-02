#!/usr/bin/env python3
"""Offline contract tests for cmd_edit.py. No network or real credentials."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import tempfile
import unittest
from unittest import mock

import cmd_edit
import metaops

os.environ.setdefault("META_TOKEN", "TEST_TOKEN")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="command", required=True)
    cmd_edit.register(sub, metaops)
    return ap


def make_workspace(root: pathlib.Path) -> metaops.meta_workspace.Workspace:
    path = root / "workspace.json"
    path.write_text(json.dumps({
        "schema": metaops.meta_workspace.WORKSPACE_SCHEMA,
        "name": "contract",
        "api_version": metaops.graph.API_VERSION,
        "blocked_accounts": [],
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
    }), encoding="utf-8")
    return metaops.meta_workspace.load_workspace(str(path))


def fake_child(stdout: str, returncode: int = 0, argv: list[str] | None = None) -> metaops.ChildResult:
    return metaops.ChildResult(argv=argv or [], returncode=returncode, stdout=stdout, stderr="")


class CmdEditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.workspace = make_workspace(self.root)
        self.ap = build_parser()

    def parse(self, argv: list[str], timeout: int = 30) -> argparse.Namespace:
        args = self.ap.parse_args(argv)
        args.workspace_obj = self.workspace
        args.profile = "test"
        args.timeout = timeout
        return args

    # --- JSON line parsing -------------------------------------------------

    def test_parse_last_json_line_picks_final_line(self) -> None:
        stdout = "human line one\n{\"not\": \"this one\"}\nhuman line two\n{\"schema\": \"edit.result/v1\", \"ok\": true}\n"
        self.assertEqual(
            cmd_edit._parse_last_json_line(stdout),
            {"schema": "edit.result/v1", "ok": True},
        )

    def test_parse_last_json_line_empty_when_absent(self) -> None:
        self.assertEqual(cmd_edit._parse_last_json_line("no json here\n"), {})

    # --- edit status ---------------------------------------------------------

    def test_edit_status_active_requires_confirm_spend(self) -> None:
        args = self.parse(["edit", "status", "--ids", "1,2", "--status", "ACTIVE"])
        with self.assertRaises(metaops.MetaOpsError):
            args.handler(args)

    def test_edit_status_active_with_confirm_translates_to_activate(self) -> None:
        args = self.parse([
            "edit", "status", "--ids", "1,2", "--status", "ACTIVE", "--confirm", "SPEND",
        ])
        with mock.patch.object(
            metaops, "run_child",
            return_value=fake_child('{"schema": "edit.result/v1", "ok": true, "count": 2}\n'),
        ) as run_child:
            code, payload = args.handler(args)
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["data"]["count"], 2)
        script, child_args, _timeout = run_child.call_args[0]
        self.assertEqual(script, "edit.py")
        self.assertEqual(child_args, ["--ids", "1,2", "--status", "ACTIVE", "--confirm", "ACTIVATE"])

    def test_edit_status_paused_needs_no_confirm(self) -> None:
        args = self.parse(["edit", "status", "--ids", "1,2", "--status", "PAUSED"])
        with mock.patch.object(
            metaops, "run_child",
            return_value=fake_child('{"schema": "edit.result/v1", "ok": true}\n'),
        ) as run_child:
            code, payload = args.handler(args)
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        _script, child_args, _timeout = run_child.call_args[0]
        self.assertNotIn("--confirm", child_args)

    def test_edit_status_state_account_mismatch_refused(self) -> None:
        state_path = self.root / "state.json"
        state_path.write_text(json.dumps({"spec_account": "act_2", "objects": {}}), encoding="utf-8")
        args = self.parse([
            "edit", "status", "--state", str(state_path), "--level", "campaign", "--status", "PAUSED",
        ])
        with self.assertRaises(metaops.MetaOpsError):
            args.handler(args)

    def test_edit_status_state_matching_account_passes(self) -> None:
        state_path = self.root / "state.json"
        state_path.write_text(json.dumps({"spec_account": "act_1", "objects": {}}), encoding="utf-8")
        args = self.parse([
            "edit", "status", "--state", str(state_path), "--level", "campaign", "--status", "PAUSED",
        ])
        with mock.patch.object(
            metaops, "run_child",
            return_value=fake_child('{"schema": "edit.result/v1", "ok": true}\n'),
        ) as run_child:
            code, _payload = args.handler(args)
        self.assertEqual(code, 0)
        _script, child_args, _timeout = run_child.call_args[0]
        self.assertEqual(child_args, ["--state", str(state_path), "--level", "campaign", "--status", "PAUSED"])

    def test_edit_status_all_routes_through_profile_account(self) -> None:
        args = self.parse(["edit", "status", "--all", "--level", "adset", "--status", "PAUSED"])
        with mock.patch.object(
            metaops, "run_child",
            return_value=fake_child('{"schema": "edit.result/v1", "ok": true}\n'),
        ) as run_child:
            args.handler(args)
        _script, child_args, _timeout = run_child.call_args[0]
        self.assertEqual(
            child_args, ["--account", "act_1", "--level", "adset", "--all", "--status", "PAUSED"]
        )

    def test_edit_status_child_failure_is_reported(self) -> None:
        args = self.parse(["edit", "status", "--ids", "1", "--status", "PAUSED"])
        with mock.patch.object(
            metaops, "run_child",
            return_value=fake_child("boom\n", returncode=1),
        ):
            code, payload = args.handler(args)
        self.assertEqual(code, 1)
        self.assertFalse(payload["ok"])

    # --- edit budget -----------------------------------------------------

    def test_edit_budget_positive_pct_requires_confirm(self) -> None:
        args = self.parse(["edit", "budget", "--ids", "1", "--budget-pct", "+20"])
        with self.assertRaises(metaops.MetaOpsError):
            args.handler(args)

    def test_edit_budget_negative_pct_needs_no_confirm(self) -> None:
        args = self.parse(["edit", "budget", "--ids", "1", "--budget-pct", "-15"])
        with mock.patch.object(
            metaops, "run_child",
            return_value=fake_child('{"schema": "edit.result/v1", "ok": true}\n'),
        ) as run_child:
            code, _payload = args.handler(args)
        self.assertEqual(code, 0)
        _script, child_args, _timeout = run_child.call_args[0]
        self.assertEqual(child_args, ["--ids", "1", "--budget-pct", "-15"])

    def test_edit_budget_minor_always_requires_confirm(self) -> None:
        args = self.parse(["edit", "budget", "--ids", "1", "--budget-minor", "500"])
        with self.assertRaises(metaops.MetaOpsError):
            args.handler(args)
        args = self.parse([
            "edit", "budget", "--ids", "1", "--budget-minor", "500", "--confirm", "SPEND",
            "--force-step",
        ])
        with mock.patch.object(
            metaops, "run_child",
            return_value=fake_child('{"schema": "edit.result/v1", "ok": true}\n'),
        ) as run_child:
            code, _payload = args.handler(args)
        self.assertEqual(code, 0)
        _script, child_args, _timeout = run_child.call_args[0]
        self.assertEqual(child_args, ["--ids", "1", "--budget-minor", "500", "--force-step"])

    def test_edit_budget_rejects_both_forms(self) -> None:
        # argparse's mutually-exclusive group refuses --budget-minor with --budget-pct at parse time.
        with self.assertRaises(SystemExit):
            self.ap.parse_args([
                "edit", "budget", "--ids", "1", "--budget-minor", "500", "--budget-pct", "+10",
            ])

    # --- edit rename -----------------------------------------------------

    def test_edit_rename_builds_args(self) -> None:
        args = self.parse(["edit", "rename", "--ids", "1,2", "--prefix", "J41|", "--suffix", "|v2"])
        with mock.patch.object(
            metaops, "run_child",
            return_value=fake_child('{"schema": "edit.result/v1", "ok": true}\n'),
        ) as run_child:
            code, _payload = args.handler(args)
        self.assertEqual(code, 0)
        _script, child_args, _timeout = run_child.call_args[0]
        self.assertEqual(
            child_args, ["--ids", "1,2", "--rename-prefix", "J41|", "--rename-suffix", "|v2"]
        )

    # --- edit ramp ---------------------------------------------------------

    def test_edit_ramp_requires_confirm_ramp(self) -> None:
        args = self.parse(["edit", "ramp", "--ids", "1", "--steps", "20,20"])
        with self.assertRaises(metaops.MetaOpsError):
            args.handler(args)

    def test_edit_ramp_wrong_confirm_literal_refused(self) -> None:
        args = self.parse(["edit", "ramp", "--ids", "1", "--steps", "20", "--confirm", "YES"])
        with self.assertRaises(metaops.MetaOpsError):
            args.handler(args)

    def test_edit_ramp_step_over_guard_refused(self) -> None:
        args = self.parse(["edit", "ramp", "--ids", "1", "--steps", "25", "--confirm", "RAMP"])
        with self.assertRaises(metaops.MetaOpsError):
            args.handler(args)

    def test_edit_ramp_sequential_calls_match_steps(self) -> None:
        args = self.parse(["edit", "ramp", "--ids", "1", "--steps", "20,20,20", "--confirm", "RAMP"])
        with mock.patch.object(
            metaops, "run_child",
            return_value=fake_child('{"schema": "edit.result/v1", "ok": true}\n'),
        ) as run_child:
            code, payload = args.handler(args)
        self.assertEqual(code, 0)
        self.assertEqual(run_child.call_count, 3)
        for call in run_child.call_args_list:
            _script, child_args, _timeout = call[0]
            self.assertEqual(child_args, ["--ids", "1", "--budget-pct", "+20"])
        self.assertEqual(len(payload["data"]["steps"]), 3)

    def test_edit_ramp_stops_on_first_child_failure(self) -> None:
        args = self.parse(["edit", "ramp", "--ids", "1", "--steps", "20,20,20", "--confirm", "RAMP"])
        with mock.patch.object(
            metaops, "run_child",
            side_effect=[
                fake_child('{"schema": "edit.result/v1", "ok": true}\n'),
                fake_child("boom\n", returncode=1),
            ],
        ) as run_child:
            code, payload = args.handler(args)
        self.assertEqual(code, 1)
        self.assertFalse(payload["ok"])
        self.assertEqual(run_child.call_count, 2)

    # --- clone -----------------------------------------------------------

    def test_clone_builds_positional_and_optional_args(self) -> None:
        args = self.parse([
            "clone", "campaign", "1234", "--times", "2", "--prefix", "S2|",
            "--start", "2030-01-01T00:00:00+00:00",
        ])
        with mock.patch.object(
            metaops, "run_child",
            return_value=fake_child('{"schema": "clone.result/v1", "ok": true}\n'),
        ) as run_child:
            code, payload = args.handler(args)
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        script, child_args, _timeout = run_child.call_args[0]
        self.assertEqual(script, "clone.py")
        self.assertEqual(
            child_args,
            ["campaign", "1234", "--times", "2", "--prefix", "S2|", "--start", "2030-01-01T00:00:00+00:00"],
        )

    def test_clone_requires_workspace(self) -> None:
        args = self.parse(["clone", "ad", "42"])
        args.workspace_obj = None
        with self.assertRaises(metaops.MetaOpsError):
            args.handler(args)

    def test_clone_child_failure_nonzero_exit(self) -> None:
        args = self.parse(["clone", "ad", "42"])
        with mock.patch.object(
            metaops, "run_child",
            return_value=fake_child('{"schema": "clone.result/v1", "ok": false}\n', returncode=1),
        ):
            code, payload = args.handler(args)
        self.assertEqual(code, 1)
        self.assertFalse(payload["ok"])

    # --- rules -------------------------------------------------------------

    def test_rules_ladder_pause_requires_confirm(self) -> None:
        args = self.parse([
            "rules", "ladder", "--target-minor", "1200", "--event", "results",
            "--level", "ADSET", "--mode", "pause",
        ])
        with self.assertRaises(metaops.MetaOpsError):
            args.handler(args)

    def test_rules_ladder_notify_no_confirm_needed_and_account_from_profile(self) -> None:
        args = self.parse([
            "rules", "ladder", "--target-minor", "1200", "--event", "results", "--level", "ADSET",
        ])
        with mock.patch.object(
            metaops, "run_child",
            return_value=fake_child('{"schema": "rules.result/v1", "ok": true}\n'),
        ) as run_child:
            code, _payload = args.handler(args)
        self.assertEqual(code, 0)
        script, child_args, _timeout = run_child.call_args[0]
        self.assertEqual(script, "rules.py")
        self.assertEqual(child_args, [
            "--account", "act_1", "--target-minor", "1200", "--event", "results",
            "--level", "ADSET", "--rungs", "0-6", "--mode", "notify", "--prefix", "LADDER|",
        ])

    def test_rules_ladder_pause_with_confirm_passes(self) -> None:
        args = self.parse([
            "rules", "ladder", "--target-minor", "1200", "--event", "results", "--level", "ADSET",
            "--mode", "pause", "--confirm", "RULES",
        ])
        with mock.patch.object(
            metaops, "run_child",
            return_value=fake_child('{"schema": "rules.result/v1", "ok": true}\n'),
        ) as run_child:
            code, _payload = args.handler(args)
        self.assertEqual(code, 0)
        _script, child_args, _timeout = run_child.call_args[0]
        self.assertIn("--mode", child_args)
        self.assertEqual(child_args[child_args.index("--mode") + 1], "pause")

    def test_rules_list_uses_profile_account(self) -> None:
        args = self.parse(["rules", "list"])
        with mock.patch.object(
            metaops, "run_child",
            return_value=fake_child('{"schema": "rules.result/v1", "ok": true, "rules": []}\n'),
        ) as run_child:
            code, payload = args.handler(args)
        self.assertEqual(code, 0)
        _script, child_args, _timeout = run_child.call_args[0]
        self.assertEqual(child_args, ["--account", "act_1", "--list"])
        self.assertEqual(payload["data"]["rules"], [])

    def test_rules_history_since_passthrough(self) -> None:
        args = self.parse(["rules", "history", "--since", "2026-09-01T00:00:00+00:00"])
        with mock.patch.object(
            metaops, "run_child",
            return_value=fake_child('{"schema": "rules.result/v1", "ok": true}\n'),
        ) as run_child:
            args.handler(args)
        _script, child_args, _timeout = run_child.call_args[0]
        self.assertEqual(
            child_args, ["--account", "act_1", "--history", "--since", "2026-09-01T00:00:00+00:00"]
        )

    def test_rules_execute_child_args(self) -> None:
        args = self.parse(["rules", "execute", "--rule-id", "999"])
        with mock.patch.object(
            metaops, "run_child",
            return_value=fake_child('{"schema": "rules.result/v1", "ok": true}\n'),
        ) as run_child:
            args.handler(args)
        _script, child_args, _timeout = run_child.call_args[0]
        self.assertEqual(child_args, ["--account", "act_1", "--execute", "999"])

    def test_rules_delete_requires_confirm_delete(self) -> None:
        args = self.parse(["rules", "delete", "--prefix", "LADDER|"])
        with self.assertRaises(metaops.MetaOpsError):
            args.handler(args)

    def test_rules_delete_with_confirm_passes(self) -> None:
        args = self.parse(["rules", "delete", "--prefix", "LADDER|", "--confirm", "DELETE"])
        with mock.patch.object(
            metaops, "run_child",
            return_value=fake_child('{"schema": "rules.result/v1", "ok": true, "deleted": []}\n'),
        ) as run_child:
            code, payload = args.handler(args)
        self.assertEqual(code, 0)
        _script, child_args, _timeout = run_child.call_args[0]
        self.assertEqual(child_args, ["--account", "act_1", "--delete-prefix", "LADDER|"])
        self.assertEqual(payload["data"]["deleted"], [])


if __name__ == "__main__":
    unittest.main()
