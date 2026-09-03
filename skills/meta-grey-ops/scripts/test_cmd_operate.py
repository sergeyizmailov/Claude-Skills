#!/usr/bin/env python3
"""Offline contract tests for cmd_operate.py. No network or real credentials."""

from __future__ import annotations

import json
import os
import pathlib
import tempfile
import unittest
from unittest import mock

os.environ.setdefault("META_TOKEN", "TEST_TOKEN")

import cmd_operate
import metaops


class FakeWorkspace:
    def __init__(self, state_root: pathlib.Path, profile_data: dict):
        self._state_root = state_root
        self._profile_data = profile_data
        self.data = {"profiles": {"test": dict(profile_data)}}

    @property
    def state_root(self) -> pathlib.Path:
        return self._state_root

    def profile(self, requested=None):
        return "test", dict(self._profile_data)


def make_args(**overrides):
    ns = mock.Mock()
    ns.profile = None
    ns.timeout = 30
    for key, value in overrides.items():
        setattr(ns, key, value)
    return ns


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.addCleanup(self.td.cleanup)
        self.root = pathlib.Path(self.td.name)
        self.workspace = FakeWorkspace(
            self.root, {"ad_account_id": "act_1", "page_id": "2", "dataset_id": "3"}
        )

    def test_review_summary_and_exit_code_on_disapproved(self):
        ads = {
            "111": {"id": "111", "account_id": "1", "name": "A", "effective_status": "ACTIVE",
                    "configured_status": "ACTIVE", "issues_info": None, "ad_review_feedback": None},
            "222": {"id": "222", "account_id": "1", "name": "B", "effective_status": "DISAPPROVED",
                    "configured_status": "ACTIVE", "issues_info": None,
                    "ad_review_feedback": {"global": "bad landing page"}},
        }

        def fake_get(path, params=None, context=""):
            return ads[path]

        args = make_args(
            workspace_obj=self.workspace, state=None, ids="111,222", all=False,
            previews=False, format="DESKTOP_FEED_STANDARD,MOBILE_FEED_STANDARD",
        )
        with mock.patch.object(metaops.graph, "get", side_effect=fake_get):
            code, payload = cmd_operate.command_review(args, metaops)

        self.assertEqual(code, 1)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["data"]["summary"], {"ACTIVE": 1, "DISAPPROVED": 1})
        self.assertEqual(payload["data"]["blocking"], 1)
        self.assertEqual(payload["error"]["kind"], "ad_review")

    def test_review_ok_when_nothing_blocking(self):
        ads = {"111": {"id": "111", "account_id": "1", "name": "A", "effective_status": "ACTIVE",
                       "configured_status": "ACTIVE", "issues_info": None, "ad_review_feedback": None}}
        args = make_args(
            workspace_obj=self.workspace, state=None, ids="111", all=False,
            previews=False, format="DESKTOP_FEED_STANDARD",
        )
        with mock.patch.object(metaops.graph, "get", side_effect=lambda path, params=None, context="": ads[path]):
            code, payload = cmd_operate.command_review(args, metaops)
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])

    def test_review_all_reads_review_fields_on_the_account_edge(self):
        args = make_args(
            workspace_obj=self.workspace, state=None, ids=None, all=True,
            previews=False, format="DESKTOP_FEED_STANDARD",
        )
        response = {"data": [
            {"id": "111", "account_id": "1", "name": "A", "effective_status": "ACTIVE", "configured_status": "ACTIVE"},
            {"id": "222", "account_id": "1", "name": "B", "effective_status": "DISAPPROVED", "configured_status": "ACTIVE"},
        ]}
        with mock.patch.object(metaops.graph, "get", return_value=response) as get:
            code, payload = cmd_operate.command_review(args, metaops)
        self.assertEqual(code, 1)
        get.assert_called_once_with(
            "act_1/ads", params={"fields": cmd_operate.AD_REVIEW_FIELDS, "limit": 500},
            context="review ads",
        )
        self.assertEqual(payload["data"]["blocking"], 1)

    def test_review_all_reports_empty_account_accurately(self):
        args = make_args(
            workspace_obj=self.workspace, state=None, ids=None, all=True,
            previews=False, format="DESKTOP_FEED_STANDARD",
        )
        with mock.patch.object(metaops.graph, "get", return_value={"data": []}):
            with self.assertRaisesRegex(metaops.MetaOpsError, "no ads found on act_1"):
                cmd_operate.command_review(args, metaops)

    def test_review_rejects_unknown_ad_format(self):
        args = make_args(
            workspace_obj=self.workspace, state=None, ids="111", all=False,
            previews=True, format="NOT_A_REAL_FORMAT",
        )
        with self.assertRaises(metaops.MetaOpsError):
            cmd_operate.command_review(args, metaops)

    def test_review_rejects_an_ad_from_another_profile_account(self):
        args = make_args(
            workspace_obj=self.workspace, state=None, ids="111", all=False,
            previews=False, format="DESKTOP_FEED_STANDARD",
        )
        ad = {"id": "111", "account_id": "2", "effective_status": "ACTIVE"}
        with mock.patch.object(metaops.graph, "get", return_value=ad):
            with self.assertRaisesRegex(metaops.MetaOpsError, "cross-profile"):
                cmd_operate.command_review(args, metaops)

    def test_review_requires_workspace(self):
        args = make_args(workspace_obj=None, state=None, ids="111", all=False,
                         previews=False, format="")
        with self.assertRaises(metaops.MetaOpsError):
            cmd_operate.command_review(args, metaops)


class MonitorTelegramTests(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.addCleanup(self.td.cleanup)
        self.root = pathlib.Path(self.td.name)
        self.workspace = FakeWorkspace(self.root, {"ad_account_id": "act_1", "page_id": "2"})

    def test_telegram_missing_env_raises_before_any_network(self):
        os.environ.pop("TG_BOT_TOKEN", None)
        os.environ.pop("TG_CHAT_ID", None)
        args = make_args(
            workspace_obj=self.workspace, accounts="act_1,act_2", stall_impressions=40,
            telegram=True, log=None, out_json=None,
        )

        def boom(*a, **kw):
            raise AssertionError("run_child must not be called when telegram env is missing")

        with mock.patch.object(metaops, "run_child", side_effect=boom):
            with self.assertRaises(metaops.MetaOpsError):
                cmd_operate.command_monitor(args, metaops)

    def test_telegram_payload_shape_and_exit_code(self):
        os.environ["TG_BOT_TOKEN"] = "FAKE_TG_TOKEN"
        os.environ["TG_CHAT_ID"] = "999"
        self.addCleanup(os.environ.pop, "TG_BOT_TOKEN", None)
        self.addCleanup(os.environ.pop, "TG_CHAT_ID", None)
        self.workspace.data["profiles"]["second"] = {"ad_account_id": "act_2"}

        rows = [
            {"account": "act_1", "verdict": "OK", "status_label": "ACTIVE",
             "spend_yesterday": 10.0, "spend_today": 9.0, "currency": "USD", "ads": {}},
            {"account": "act_2", "verdict": "STALL", "status_label": "ACTIVE",
             "spend_yesterday": 5.0, "spend_today": 5.0, "currency": "USD",
             "ads": {"DISAPPROVED": 0, "WITH_ISSUES": 0}, "stalled_adsets": [{"id": "a1"}]},
        ]

        def fake_run_child(script, child_args, timeout):
            self.assertEqual(script, "monitor.py")
            json_path = pathlib.Path(child_args[child_args.index("--json") + 1])
            json_path.write_text(json.dumps(rows), encoding="utf-8")
            return metaops.ChildResult(argv=["monitor.py"], returncode=1, stdout="", stderr="")

        posted = {}

        class FakeSession:
            def post(self, url, json=None, timeout=None):
                posted["url"] = url
                posted["payload"] = json
                return mock.Mock(json=lambda: {"ok": True, "result": {}})

        args = make_args(
            workspace_obj=self.workspace, accounts="act_1,act_2", stall_impressions=40,
            telegram=True, log=None, out_json=None,
        )
        with mock.patch.object(metaops, "run_child", side_effect=fake_run_child), \
             mock.patch.object(metaops, "echo_child", lambda c: None), \
             mock.patch.object(metaops.graph, "session", return_value=FakeSession()):
            code, payload = cmd_operate.command_monitor(args, metaops)

        self.assertEqual(code, 1)
        self.assertIn("FAKE_TG_TOKEN", posted["url"])
        self.assertEqual(posted["payload"]["chat_id"], "999")
        self.assertEqual(posted["payload"]["parse_mode"], "HTML")
        self.assertIn("STALL", posted["payload"]["text"])
        self.assertEqual(posted["payload"]["link_preview_options"], {"is_disabled": True})
        self.assertEqual(payload["data"]["telegram"]["sent"], 1)
        self.assertEqual(payload["data"]["verdict_counts"]["STALL"], 1)


class ConfirmLiteralTests(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.addCleanup(self.td.cleanup)
        self.workspace = FakeWorkspace(
            pathlib.Path(self.td.name), {"ad_account_id": "act_1", "page_id": "2"}
        )

    def test_comments_hide_requires_literal_confirm(self):
        args = make_args(
            workspace_obj=self.workspace, comments_mode="hide", ads="1,2", all=False,
            matching="scam", all_comments=False, confirm="NOPE", dry_run=False,
        )
        with mock.patch.object(metaops, "run_child", side_effect=AssertionError("must not run")):
            with self.assertRaises(metaops.MetaOpsError):
                cmd_operate.command_comments(args, metaops)

    def test_comments_delete_requires_matching(self):
        args = make_args(
            workspace_obj=self.workspace, comments_mode="delete", ads="1,2", all=False,
            matching=None, all_comments=False, confirm="DELETE", dry_run=False,
        )
        with mock.patch.object(metaops, "run_child", side_effect=AssertionError("must not run")):
            with self.assertRaises(metaops.MetaOpsError):
                cmd_operate.command_comments(args, metaops)

    def test_comments_hide_accepts_literal_confirm_and_runs(self):
        args = make_args(
            workspace_obj=self.workspace, comments_mode="hide", ads="1,2", all=False,
            matching="scam", all_comments=False, confirm="HIDE", dry_run=False,
        )
        summary_line = json.dumps({"schema": "comments.result/v1", "mode": "hide",
                                   "posts_checked": 1, "acted": 2, "dry_run": False})

        def fake_run_child(script, child_args, timeout):
            self.assertEqual(script, "comments.py")
            self.assertIn("--hide-matching", child_args)
            return metaops.ChildResult(argv=[], returncode=0, stdout=summary_line, stderr="")

        with mock.patch.object(metaops, "run_child", side_effect=fake_run_child), \
             mock.patch.object(metaops, "echo_child", lambda c: None):
            code, payload = cmd_operate.command_comments(args, metaops)
        self.assertEqual(code, 0)
        self.assertEqual(payload["data"]["summary"]["acted"], 2)

    def test_page_set_requires_literal_confirm(self):
        args = make_args(
            workspace_obj=self.workspace, page_mode="set", page=None,
            avatar="a.jpg", cover=None, about=None, website=None, confirm="NOPE",
        )
        with mock.patch.object(metaops, "run_child", side_effect=AssertionError("must not run")):
            with self.assertRaises(metaops.MetaOpsError):
                cmd_operate.command_page(args, metaops)

    def test_page_set_requires_at_least_one_field(self):
        args = make_args(
            workspace_obj=self.workspace, page_mode="set", page=None,
            avatar=None, cover=None, about=None, website=None, confirm="PAGE",
        )
        with mock.patch.object(metaops, "run_child", side_effect=AssertionError("must not run")):
            with self.assertRaises(metaops.MetaOpsError):
                cmd_operate.command_page(args, metaops)


class LeaderboardTests(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.addCleanup(self.td.cleanup)
        self.root = pathlib.Path(self.td.name)
        self.workspace = FakeWorkspace(self.root, {"ad_account_id": "act_1", "page_id": "2"})

    def test_leaderboard_aggregates_by_ad_name_across_accounts(self):
        self.workspace.data["profiles"]["second"] = {"ad_account_id": "act_2"}
        fixtures = {
            "act_1": [
                {"ad_name": "creative_03_v1", "spend": "10.5", "impressions": "100", "clicks": "5",
                 "account_currency": "USD", "actions": [{"action_type": "lead", "value": "2"}]},
                {"ad_name": "creative_03_v2", "spend": "1.0", "impressions": "10", "clicks": "0",
                 "account_currency": "USD", "actions": []},
            ],
            "act_2": [
                {"ad_name": "creative_03_v1", "spend": "20.25", "impressions": "200", "clicks": "8",
                 "account_currency": "USD", "actions": [{"action_type": "lead", "value": "3"}]},
            ],
        }

        def fake_run_child(script, child_args, timeout):
            self.assertEqual(script, "insights.py")
            account = child_args[child_args.index("--account") + 1]
            json_path = pathlib.Path(child_args[child_args.index("--json") + 1])
            json_path.parent.mkdir(parents=True, exist_ok=True)
            json_path.write_text(json.dumps(fixtures[account]), encoding="utf-8")
            summary = json.dumps({"schema": "insights.result/v1", "account": account, "rows": len(fixtures[account])})
            return metaops.ChildResult(argv=[], returncode=0, stdout=summary, stderr="")

        accounts_path = self.root / "accounts.json"
        accounts_path.write_text(json.dumps([{"account_id": "act_1"}, {"account_id": "act_2"}]),
                                 encoding="utf-8")
        args = make_args(
            workspace_obj=self.workspace, accounts=str(accounts_path), date_preset="yesterday",
            csv=None, top=20, insights_mode="leaderboard",
        )
        with mock.patch.object(metaops, "run_child", side_effect=fake_run_child), \
             mock.patch.object(metaops, "echo_child", lambda c: None):
            code, payload = cmd_operate.command_insights(args, metaops)

        self.assertEqual(code, 0)
        board = payload["data"]["leaderboard"]
        self.assertEqual(board[0]["ad_name"], "creative_03_v1")
        self.assertAlmostEqual(board[0]["spend"], 30.75)
        self.assertEqual(board[0]["impressions"], 300)
        self.assertEqual(board[0]["clicks"], 13)
        self.assertEqual(board[0]["accounts"], ["act_1", "act_2"])
        self.assertAlmostEqual(board[0]["actions"]["lead"], 5.0)
        self.assertEqual(board[1]["ad_name"], "creative_03_v2")

    def test_leaderboard_refuses_to_sum_different_currencies(self):
        self.workspace.data["profiles"]["second"] = {"ad_account_id": "act_2"}
        fixtures = {
            "act_1": [{"ad_name": "creative", "spend": "10", "account_currency": "USD"}],
            "act_2": [{"ad_name": "creative", "spend": "10", "account_currency": "EUR"}],
        }

        def fake_run_child(script, child_args, timeout):
            account = child_args[child_args.index("--account") + 1]
            json_path = pathlib.Path(child_args[child_args.index("--json") + 1])
            json_path.write_text(json.dumps(fixtures[account]), encoding="utf-8")
            return metaops.ChildResult(argv=[], returncode=0, stdout="{}", stderr="")

        accounts_path = self.root / "accounts.json"
        accounts_path.write_text(json.dumps([{"account_id": "act_1"}, {"account_id": "act_2"}]), encoding="utf-8")
        args = make_args(
            workspace_obj=self.workspace, accounts=str(accounts_path), date_preset="yesterday",
            csv=None, top=20, insights_mode="leaderboard",
        )
        with mock.patch.object(metaops, "run_child", side_effect=fake_run_child), \
             mock.patch.object(metaops, "echo_child", lambda c: None):
            code, payload = cmd_operate.command_insights(args, metaops)
        self.assertEqual(code, 1)
        self.assertEqual(payload["phase"], "currency_mismatch")
        self.assertEqual(payload["data"]["currencies"], ["EUR", "USD"])

    def test_leaderboard_rejects_an_undeclared_account_before_reads(self):
        args = make_args(
            workspace_obj=self.workspace, accounts="act_99", date_preset="yesterday",
            csv=None, top=20, insights_mode="leaderboard",
        )
        with mock.patch.object(metaops, "run_child") as child:
            with self.assertRaisesRegex(metaops.MetaOpsError, "not declared"):
                cmd_operate.command_insights(args, metaops)
        child.assert_not_called()


if __name__ == "__main__":
    unittest.main()
