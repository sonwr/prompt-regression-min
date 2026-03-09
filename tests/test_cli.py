from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import subprocess
import unittest
from unittest import mock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from prompt_regression_min import cli


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


class PromptRegressionCliTests(unittest.TestCase):
    def test_cli_emits_summary_pr_comment_to_stdout(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset_path = tmp_path / "dataset.jsonl"
            baseline_path = tmp_path / "baseline.jsonl"
            candidate_path = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset_path,
                [{"id": "checkout-copy", "expected": {"type": "substring", "value": "ok"}}],
            )
            _write_jsonl(baseline_path, [{"id": "checkout-copy", "output": "ok"}])
            _write_jsonl(candidate_path, [{"id": "checkout-copy", "output": "ok"}])

            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "--dataset",
                        str(dataset_path),
                        "--baseline",
                        str(baseline_path),
                        "--candidate",
                        str(candidate_path),
                        "--summary-pr-comment",
                        "-",
                        "--summary-pr-comment-title",
                        "release gate reviewer note",
                        "--quiet",
                    ],
                ):
                    exit_code = cli.main()

            self.assertIsNone(exit_code)
            rendered = stdout.getvalue()
            self.assertIn("## release gate reviewer note", rendered)
            self.assertIn("- Summary schema version: `1`", rendered)
            self.assertIn(f"- Tool version: `{cli.__version__}`", rendered)
            self.assertIn("- Required schema version gate: _disabled_", rendered)
            self.assertIn("- Stable IDs: `checkout-copy`", rendered)
            self.assertNotIn("- Reviewer queue total:", rendered)
            self.assertIn("approval-ready", rendered)


    def test_summary_markdown_stdout_word_count_range_fixture_surfaces_regression_id(self) -> None:
        root = Path(__file__).resolve().parents[1]
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "--dataset",
                        str(root / "examples" / "dataset" / "word_count_range_release_notes.jsonl"),
                        "--baseline",
                        str(root / "examples" / "outputs" / "word_count_range_release_notes.baseline.jsonl"),
                        "--candidate",
                        str(root / "examples" / "outputs" / "word_count_range_release_notes.candidate.jsonl"),
                        "--summary-markdown",
                        "-",
                        "--summary-markdown-title",
                        "word-count release-note gate",
                    ],
                ):
                    cli.main()
        self.assertEqual(exc.exception.code, 1)
        markdown = output.getvalue()
        self.assertIn("## word-count release-note gate", markdown)
        self.assertIn("- Regression IDs (2): `release-note-bullets`, `release-note-short`", markdown)
        self.assertIn("- Reviewer queue groups: 1", markdown)
        self.assertIn("- Reviewer queue group keys: fix_regressions", markdown)
        self.assertIn("- Reviewer queue group labels: fix regressions", markdown)
        self.assertIn("- Reviewer queue largest group: fix_regressions (2 case(s), 100.00% of active cases, 100.00% overall queue rate, 100.00% source-case rate, 100.00% of queued follow-up)", markdown)
        self.assertIn("- Reviewer queue largest group label: fix regressions", markdown)
        self.assertIn("- Reviewer queue largest group IDs: `release-note-bullets`, `release-note-short`", markdown)
        self.assertIn("- Reviewer queue priority labels: fix_regressions=P1 · fix regressions", markdown)
        self.assertIn("- Reviewer queue follow-up priority: fix_regressions", markdown)
        self.assertIn("- Reviewer queue follow-up labels: fix regressions", markdown)
        self.assertIn("- Reviewer queue priority ranks: fix_regressions=P1", markdown)
        self.assertIn("- Reviewer queue next-focus key: fix_regressions", markdown)
        self.assertIn("- Reviewer queue next-focus label: fix regressions", markdown)
        self.assertIn("- Reviewer queue next-focus priority label: P1 · fix regressions", markdown)
        self.assertIn("- Reviewer queue next focus: fix_regressions: `release-note-bullets`, `release-note-short`", markdown)
        self.assertIn("- Reviewer queue next-focus case count: 2", markdown)
        self.assertIn("- Reviewer queue next-focus active-case rate: 100.00% of active cases", markdown)
        self.assertIn("- Reviewer queue next-focus source-case rate: 100.00% of source cases", markdown)
        self.assertIn("- Reviewer queue next-focus priority rank: 1 of 1", markdown)
        self.assertIn("- Reviewer queue next-focus tie mode: unique", markdown)
        self.assertIn("- Reviewer queue next-focus queue share: 100.00% of queued follow-up", markdown)
        self.assertIn("- Status: **FAIL**", markdown)
    def test_summary_markdown_includes_active_case_rate_for_filtered_shards(self) -> None:
        root = Path(__file__).resolve().parents[1]
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "--dataset",
                    str(root / "examples" / "dataset" / "filtered_out_band_demo.jsonl"),
                    "--baseline",
                    str(root / "examples" / "outputs" / "filtered_out_band_demo.baseline.jsonl"),
                    "--candidate",
                    str(root / "examples" / "outputs" / "filtered_out_band_demo.candidate.jsonl"),
                    "--include-id-regex",
                    "^auth-",
                    "--max-filtered-out-cases",
                    "2",
                    "--max-filtered-out-rate",
                    "0.5",
                    "--summary-markdown",
                    "-",
                ],
            ):
                cli.main()
        markdown = output.getvalue()
        self.assertIn("- Selection rate: 50.00% of source cases", markdown)
        self.assertIn("- Active-case rate: 50.00% of source cases", markdown)
        self.assertIn("- Skipped-case budget usage: 0/disabled (0.00% source-case rate)", markdown)
        self.assertIn("- Filtered-out budget usage: 2/2 (50.00% source-case rate, 100.00% of queued follow-up)", markdown)

    def test_summary_pr_comment_includes_changed_ids_and_rate_for_reviewer_triage(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "stable-pass", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "reg-1", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "stable-pass", "output": "ok"},
                    {"id": "reg-1", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "stable-pass", "output": "ok"},
                    {"id": "reg-1", "output": "bad"},
                ],
            )

            output = io.StringIO()
            with self.assertRaises(SystemExit):
                with contextlib.redirect_stdout(output):
                    with mock.patch(
                        "sys.argv",
                        [
                            "prm",
                            "run",
                            "-d",
                            str(dataset),
                            "-b",
                            str(baseline),
                            "-c",
                            str(candidate),
                            "--summary-pr-comment",
                            "-",
                            "--quiet",
                        ],
                    ):
                        cli.main()
            pr_comment = output.getvalue()
            self.assertIn("- Regression IDs (1): `reg-1`", pr_comment)
            self.assertIn("- Regression rate: 50.00% of active cases", pr_comment)
            self.assertIn("- Regression source-case rate: 50.00% of source cases", pr_comment)
            self.assertIn("- Changed IDs (1): `reg-1`", pr_comment)
            self.assertIn("- Changed-case rate: 50.00% of active cases", pr_comment)
            self.assertIn("- Changed source-case rate: 50.00% of source cases", pr_comment)
            self.assertIn("- Selection rate: 100.00% of source cases", pr_comment)
            self.assertIn("- Active-case rate: 100.00% of source cases", pr_comment)
            self.assertIn("- Stable IDs: `stable-pass`", pr_comment)
            self.assertIn("- Stable-case rate: 50.00% of active cases", pr_comment)
            self.assertIn("- Stable source-case rate: 50.00% of source cases", pr_comment)
            self.assertIn("- Reviewer queue total: 1 case(s)", pr_comment)
            self.assertIn("- Reviewer queue group keys: fix_regressions", pr_comment)
            self.assertIn("- Reviewer queue group labels: fix regressions", pr_comment)
            self.assertIn("- Reviewer queue priority labels: fix_regressions=P1 · fix regressions", pr_comment)
            self.assertIn("- Reviewer queue largest group: fix_regressions (1 case(s), 50.00% of active cases, 50.00% overall queue rate, 50.00% source-case rate, 100.00% of queued follow-up)", pr_comment)
            self.assertIn("- Reviewer queue largest group label: fix regressions", pr_comment)
            self.assertIn("- Reviewer queue next-focus priority label: P1 · fix regressions", pr_comment)
            self.assertIn("- Reviewer queue follow-up priority: fix_regressions", pr_comment)
            self.assertIn("- Reviewer queue follow-up labels: fix regressions", pr_comment)
            self.assertIn("- Reviewer queue priority ranks: fix_regressions=P1", pr_comment)
            self.assertIn("- Reviewer queue next-focus key: fix_regressions", pr_comment)
            self.assertIn("- Reviewer queue next-focus label: fix regressions", pr_comment)
            self.assertIn("- Reviewer queue next focus: fix_regressions: `reg-1`", pr_comment)
            self.assertIn("- Reviewer queue next-focus case count: 1", pr_comment)
            self.assertIn("- Reviewer queue next-focus active-case rate: 50.00% of active cases", pr_comment)
            self.assertIn("- Reviewer queue next-focus source-case rate: 50.00% of source cases", pr_comment)
            self.assertIn("- Reviewer queue next-focus priority rank: 1 of 1", pr_comment)
            self.assertIn("- Reviewer queue next-focus tie mode: unique", pr_comment)
            self.assertIn("- Reviewer queue next-focus queue share: 100.00% of queued follow-up", pr_comment)
            self.assertIn("- Reviewer queue (regressions): 1 case(s) / 50.00% of active cases / 50.00% of source cases", pr_comment)

    def test_summary_json_exposes_next_focus_alias_fields_for_bots(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"
            summary_json = tmp_path / "summary.json"

            _write_jsonl(
                dataset,
                [
                    {"id": "reg-1", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "watch-1", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "reg-1", "output": "ok"},
                    {"id": "watch-1", "output": "bad"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "reg-1", "output": "bad"},
                    {"id": "watch-1", "output": "bad"},
                ],
            )

            with self.assertRaises(SystemExit):
                with mock.patch(
                    "sys.argv",
                    [
                        "prm", "run",
                        "-d", str(dataset),
                        "-b", str(baseline),
                        "-c", str(candidate),
                        "--summary-json", str(summary_json),
                        "--quiet",
                    ],
                ):
                    cli.main()

            payload = json.loads(summary_json.read_text(encoding="utf-8"))
            reviewer_queue = payload["reviewer_queue"]
            self.assertEqual(reviewer_queue["next_focus_key"], "fix_regressions")
            self.assertEqual(reviewer_queue["next_focus_label"], "fix regressions")
            self.assertEqual(reviewer_queue["next_focus_ids"], ["reg-1"])
            self.assertEqual(reviewer_queue["next_focus_case_count"], 1)
            self.assertEqual(reviewer_queue["next_focus_queue_share"], 0.5)
            self.assertEqual(reviewer_queue["next_focus_tie_mode"], "tied")
            self.assertEqual(
                reviewer_queue["next_focus_group"],
                {
                    "key": "fix_regressions",
                    "label": "fix regressions",
                    "priority_label": "P1 · fix regressions",
                    "priority_rank": 1,
                    "ids": ["reg-1"],
                    "case_count": 1,
                    "active_case_rate": 0.5,
                    "source_case_rate": 0.5,
                    "queue_share": 0.5,
                    "tie_mode": "tied",
                },
            )

    def test_summary_json_exposes_reviewer_queue_group_maps_for_bots(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "reg-1", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "watch-1", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "skip-1", "expected": {"type": "substring", "value": "ok"}, "disabled": True},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "reg-1", "output": "ok"},
                    {"id": "watch-1", "output": "bad"},
                    {"id": "skip-1", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "reg-1", "output": "bad"},
                    {"id": "watch-1", "output": "bad"},
                    {"id": "skip-1", "output": "ok"},
                ],
            )

            output = io.StringIO()
            with self.assertRaises(SystemExit):
                with contextlib.redirect_stdout(output):
                    with mock.patch(
                        "sys.argv",
                        [
                            "prm",
                            "run",
                            "-d",
                            str(dataset),
                            "-b",
                            str(baseline),
                            "-c",
                            str(candidate),
                            "--summary-json",
                            "-",
                            "--quiet",
                        ],
                    ):
                        cli.main()

            payload = json.loads(output.getvalue())
            reviewer_queue = payload["reviewer_queue"]
            self.assertEqual(
                reviewer_queue["group_counts_by_key"],
                {
                    "fix_regressions": 1,
                    "watch_unchanged_fails": 1,
                    "resolve_skipped_cases": 1,
                },
            )
            self.assertEqual(
                reviewer_queue["group_labels_by_key"],
                {
                    "fix_regressions": "fix regressions",
                    "watch_unchanged_fails": "watch unchanged fails",
                    "resolve_skipped_cases": "resolve skipped cases",
                },
            )
            self.assertEqual(
                reviewer_queue["group_rates_by_key"],
                {
                    "fix_regressions": 0.5,
                    "watch_unchanged_fails": 0.5,
                    "resolve_skipped_cases": 0.5,
                },
            )
            self.assertEqual(
                reviewer_queue["group_source_case_rates_by_key"],
                {
                    "fix_regressions": 0.3333,
                    "watch_unchanged_fails": 0.3333,
                    "resolve_skipped_cases": 0.3333,
                },
            )
            self.assertEqual(
                reviewer_queue["group_queue_shares_by_key"],
                {
                    "fix_regressions": 0.3333,
                    "watch_unchanged_fails": 0.3333,
                    "resolve_skipped_cases": 0.3333,
                },
            )
            self.assertEqual(
                reviewer_queue["group_ids_by_key"],
                {
                    "fix_regressions": ["reg-1"],
                    "watch_unchanged_fails": ["watch-1"],
                    "resolve_skipped_cases": ["skip-1"],
                },
            )
            self.assertEqual(reviewer_queue["follow_up_priority"], ["fix_regressions", "watch_unchanged_fails", "resolve_skipped_cases"])

    def test_summary_pr_comment_surfaces_tied_largest_group_labels(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "reg-1", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "watch-1", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "reg-1", "output": "ok"},
                    {"id": "watch-1", "output": "bad"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "reg-1", "output": "bad"},
                    {"id": "watch-1", "output": "bad"},
                ],
            )

            output = io.StringIO()
            with self.assertRaises(SystemExit):
                with contextlib.redirect_stdout(output):
                    with mock.patch(
                        "sys.argv",
                        [
                            "prm",
                            "run",
                            "-d",
                            str(dataset),
                            "-b",
                            str(baseline),
                            "-c",
                            str(candidate),
                            "--summary-pr-comment",
                            "-",
                            "--quiet",
                        ],
                    ):
                        cli.main()
            pr_comment = output.getvalue()
            self.assertIn("- Reviewer queue tied largest groups: fix_regressions, watch_unchanged_fails", pr_comment)
            self.assertIn("- Reviewer queue largest-group tie count: 2", pr_comment)
            self.assertIn("- Reviewer queue tied largest labels: fix regressions, watch unchanged fails", pr_comment)
            self.assertIn("- Reviewer queue next-focus tie mode: tied", pr_comment)
            self.assertIn("- Reviewer queue next-focus key: fix_regressions", pr_comment)
            self.assertIn("- Reviewer queue next-focus label: fix regressions", pr_comment)
            self.assertIn("- Reviewer queue next focus: fix_regressions: `reg-1`", pr_comment)

    def test_summary_pr_comment_includes_improvement_rate_for_reviewer_triage(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "imp-1", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "stable-pass", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "imp-1", "output": "bad"},
                    {"id": "stable-pass", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "imp-1", "output": "ok"},
                    {"id": "stable-pass", "output": "ok"},
                ],
            )

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--summary-pr-comment",
                        "-",
                        "--quiet",
                    ],
                ):
                    cli.main()
            pr_comment = output.getvalue()
            self.assertIn("- Improved IDs (1): `imp-1`", pr_comment)
            self.assertIn("- Improvement rate: 50.00% of active cases", pr_comment)
            self.assertIn("- Improvement source-case rate: 50.00% of source cases", pr_comment)
            self.assertIn("- Stable-case rate: 50.00% of active cases", pr_comment)
            self.assertIn("- Stable source-case rate: 50.00% of source cases", pr_comment)

    def test_summary_pr_comment_includes_selection_and_active_case_rates_for_filtered_scope(self) -> None:
        root = Path(__file__).resolve().parents[1]
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "--dataset",
                    str(root / "examples" / "dataset" / "filtered_out_band_demo.jsonl"),
                    "--baseline",
                    str(root / "examples" / "outputs" / "filtered_out_band_demo.baseline.jsonl"),
                    "--candidate",
                    str(root / "examples" / "outputs" / "filtered_out_band_demo.candidate.jsonl"),
                    "--include-id-regex",
                    "^auth-",
                    "--summary-pr-comment",
                    "-",
                    "--quiet",
                ],
            ):
                cli.main()
        pr_comment = output.getvalue()
        self.assertIn("- Selection rate: 50.00% of source cases", pr_comment)
        self.assertIn("- Active-case rate: 100.00% of source cases", pr_comment)
        self.assertIn("- Filtered-out IDs: `billing-invoice`, `search-query`", pr_comment)

    def test_summary_pr_comment_includes_unchanged_fail_watchlist_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "watch-auth", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "stable-pass", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "watch-auth", "output": "bad"},
                    {"id": "stable-pass", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "watch-auth", "output": "bad"},
                    {"id": "stable-pass", "output": "ok"},
                ],
            )

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--summary-pr-comment",
                        "-",
                        "--quiet",
                    ],
                ):
                    cli.main()
            pr_comment = output.getvalue()
            self.assertIn("- Stable IDs: `stable-pass`", pr_comment)
            self.assertIn("- Unchanged fail IDs: `watch-auth`", pr_comment)
            self.assertIn("- Watchlist rate: 50.00% of active cases", pr_comment)
            self.assertIn("- Watchlist source-case rate: 50.00% of source cases", pr_comment)
            self.assertIn("- Reviewer queue total: 1 case(s)", pr_comment)
            self.assertIn("- Reviewer queue (watchlist): 1 case(s) / 50.00% of active cases / 50.00% of source cases", pr_comment)

    def test_summary_pr_comment_exposes_reviewer_queue_breakdown_for_filtered_and_skipped_scope(self) -> None:
        root = Path(__file__).resolve().parents[1]
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "--dataset",
                    str(root / "examples" / "dataset" / "filtered_out_band_demo.jsonl"),
                    "--baseline",
                    str(root / "examples" / "outputs" / "filtered_out_band_demo.baseline.jsonl"),
                    "--candidate",
                    str(root / "examples" / "outputs" / "filtered_out_band_demo.candidate.jsonl"),
                    "--include-id-regex",
                    "^auth-",
                    "--summary-pr-comment",
                    "-",
                    "--quiet",
                ],
            ):
                cli.main()
        pr_comment = output.getvalue()
        self.assertIn("- Reviewer queue total: 2 case(s)", pr_comment)
        self.assertIn("- Reviewer queue source-case rate: 50.00% of source cases", pr_comment)
        self.assertIn("- Reviewer queue dominant focus: confirm filtered-out scope", pr_comment)
        self.assertIn("- Reviewer queue largest group IDs: `billing-invoice`, `search-query`", pr_comment)
        self.assertIn("- Reviewer queue (filtered-out scope): 2 case(s) / 100.00% of active cases / 50.00% of source cases", pr_comment)


    def test_summary_markdown_includes_unchanged_pass_ids_for_handoff_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "stable-pass", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "reg-1", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "stable-pass", "output": "ok"},
                    {"id": "reg-1", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "stable-pass", "output": "ok"},
                    {"id": "reg-1", "output": "bad"},
                ],
            )

            output = io.StringIO()
            with self.assertRaises(SystemExit):
                with contextlib.redirect_stdout(output):
                    with mock.patch(
                        "sys.argv",
                        [
                            "prm",
                            "run",
                            "-d",
                            str(dataset),
                            "-b",
                            str(baseline),
                            "-c",
                            str(candidate),
                            "--summary-markdown",
                            "-",
                            "--quiet",
                        ],
                    ):
                        cli.main()
            markdown = output.getvalue()
            self.assertIn("- Reviewer handoff: stable=1, regressions=1, improved=0, watchlist=0", markdown)
            self.assertIn("- Coverage watch: selected=2, active=2, skipped=0, filtered_out=0", markdown)
            self.assertIn("- Regression rate: 50.00% of active cases", markdown)
            self.assertIn("- Improvement rate: 0.00% of active cases", markdown)
            self.assertIn("- Unchanged pass IDs (1): `stable-pass`", markdown)
            self.assertIn("- Regression IDs (1): `reg-1`", markdown)


    def test_summary_markdown_includes_changed_case_budget_usage_when_gate_is_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "stable-pass", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "improved", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "stable-pass", "output": "ok"},
                    {"id": "improved", "output": "bad"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "stable-pass", "output": "ok"},
                    {"id": "improved", "output": "ok"},
                ],
            )

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--summary-markdown",
                        "-",
                        "--max-changed-cases",
                        "2",
                        "--quiet",
                    ],
                ):
                    cli.main()
            markdown = output.getvalue()
            self.assertIn("- Regression budget usage: 0/0 (0.00% active-case rate)", markdown)
            self.assertIn("- Changed-case budget usage: 1/2 (50.00% active-case rate)", markdown)
            self.assertIn("- Unchanged-fail budget usage: 0/disabled (0.00% active-case rate)", markdown)
            self.assertIn("- Skipped-case budget usage: 0/disabled (0.00% source-case rate)", markdown)
            self.assertIn("- Filtered-out budget usage: 0/disabled (0.00% source-case rate)", markdown)

    def test_summary_markdown_includes_skipped_case_budget_usage_when_gate_is_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "active-pass", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "skip-me", "disabled": True, "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "active-pass", "output": "ok"},
                    {"id": "skip-me", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "active-pass", "output": "ok"},
                    {"id": "skip-me", "output": "ok"},
                ],
            )

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--summary-markdown",
                        "-",
                        "--max-skipped-cases",
                        "1",
                        "--quiet",
                    ],
                ):
                    cli.main()
            markdown = output.getvalue()
            self.assertIn("- Skipped-case budget usage: 1/1 (50.00% source-case rate)", markdown)
            self.assertIn("- Filtered-out budget usage: 0/disabled (0.00% source-case rate)", markdown)

    def test_cli_allows_configurable_regression_budget(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "bad"}])

            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--max-regressions",
                    "1",
                ],
            ):
                cli.main()

    def test_cli_fails_when_regression_rate_exceeds_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "a", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "b", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "a", "output": "ok"},
                    {"id": "b", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "a", "output": "ok"},
                    {"id": "b", "output": "bad"},
                ],
            )

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-regressions",
                        "1",
                        "--max-regression-rate",
                        "0.25",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_rejects_invalid_max_regression_rate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-regression-rate",
                        "1.5",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)

    def test_cli_fails_when_candidate_pass_rate_below_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "a", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "b", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "a", "output": "ok"},
                    {"id": "b", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "a", "output": "ok"},
                    {"id": "b", "output": "bad"},
                ],
            )

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-regressions",
                        "2",
                        "--min-candidate-pass-rate",
                        "0.9",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_prints_summary_markdown_to_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "keep-pass", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "reg-1", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "imp-1", "expected": {"type": "substring", "value": "great"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "keep-pass", "output": "ok"},
                    {"id": "reg-1", "output": "ok"},
                    {"id": "imp-1", "output": "bad"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "keep-pass", "output": "ok"},
                    {"id": "reg-1", "output": "bad"},
                    {"id": "imp-1", "output": "great"},
                ],
            )

            output = io.StringIO()
            with self.assertRaises(SystemExit) as exc:
                with contextlib.redirect_stdout(output):
                    with mock.patch(
                        "sys.argv",
                        [
                            "prm",
                            "run",
                            "-d",
                            str(dataset),
                            "-b",
                            str(baseline),
                            "-c",
                            str(candidate),
                            "--summary-markdown",
                            "-",
                            "--quiet",
                        ],
                    ):
                        cli.main()
            self.assertEqual(exc.exception.code, 1)

            rendered = output.getvalue()
            self.assertIn("## prompt-regression-min summary", rendered)
            self.assertIn(f"- Tool version: `{cli.__version__}`", rendered)
            self.assertIn("- Status: **FAIL**", rendered)
            self.assertIn("- Pass-rate trend: `flat`", rendered)
            self.assertIn("- Stability rate: 33.33%", rendered)
            self.assertIn("- Gate snapshot:", rendered)
            self.assertIn("  - max_regressions=0", rendered)
            self.assertIn("  - forbid_unchanged_fail_id_regex=disabled", rendered)
            self.assertIn("  - min_delta_pass_rate_pp=disabled", rendered)
            self.assertIn("  - max_delta_pass_rate_pp=disabled", rendered)
            self.assertIn("  - max_changed_cases=disabled", rendered)
            self.assertIn("  - max_filtered_out_cases=disabled", rendered)
            self.assertIn("  - min_active_cases=1", rendered)
            self.assertIn("  - min_improved=0", rendered)
            self.assertIn("  - max_improved=disabled", rendered)
            self.assertIn("  - max_improved_rate=disabled", rendered)
            self.assertIn("  - min_unchanged_pass=0", rendered)
            self.assertIn("  - max_unchanged_pass=disabled", rendered)
            self.assertIn("  - min_stability_rate=disabled", rendered)
            self.assertIn("  - require_summary_schema_version=disabled", rendered)
            self.assertIn("- Regression IDs (1): `reg-1`", rendered)
            self.assertIn("- Improved IDs (1): `imp-1`", rendered)
            self.assertIn("- Changed IDs (2): `imp-1`, `reg-1`", rendered)
            self.assertIn("- Changed-case rate: 66.67%", rendered)
            self.assertNotIn("prompt-regression-min summary\n- cases:", rendered)


    def test_cli_allows_custom_summary_markdown_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "keep-pass", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "keep-pass", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "keep-pass", "output": "ok"}])

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--summary-markdown",
                        "-",
                        "--summary-markdown-title",
                        "checkout gate summary",
                        "--quiet",
                    ],
                ):
                    cli.main()

            rendered = output.getvalue()
            self.assertIn("## checkout gate summary", rendered)
            self.assertNotIn("## prompt-regression-min summary", rendered)

    def test_cli_fails_when_unchanged_fail_count_exceeds_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "a", "expected": {"type": "substring", "value": "ok"}}],
            )
            _write_jsonl(baseline, [{"id": "a", "output": "bad"}])
            _write_jsonl(candidate, [{"id": "a", "output": "still bad"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-unchanged-fail",
                        "0",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)


    def test_cli_fails_when_summary_schema_version_gate_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--require-summary-schema-version",
                        "2",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_exposes_summary_schema_version_gate_in_summary_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            output = io.StringIO()
            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--require-summary-schema-version",
                    "1",
                    "--summary-json",
                ],
            ):
                with contextlib.redirect_stdout(output):
                    cli.main()

            lines = [line for line in output.getvalue().splitlines() if line.strip()]
            summary_payload = json.loads(lines[-1])
            self.assertEqual(summary_payload["summary_schema_version"], 1)
            self.assertEqual(summary_payload["gates"]["require_summary_schema_version"], 1)

    def test_cli_emits_summary_json_to_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            output = io.StringIO()
            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--summary-json",
                ],
            ):
                with contextlib.redirect_stdout(output):
                    cli.main()

            lines = [line for line in output.getvalue().splitlines() if line.strip()]
            summary_payload = json.loads(lines[-1])
            self.assertEqual(summary_payload["status"], "PASS")
            self.assertEqual(summary_payload["summary_schema_version"], 1)
            self.assertEqual(summary_payload["tool_version"], cli.__version__)
            self.assertIn("summary", summary_payload)
            self.assertIn("unchanged_fail", summary_payload["summary"])
            self.assertIn("gates", summary_payload)
            self.assertEqual(summary_payload["gates"]["max_regressions"], 0)

    def test_cli_quiet_mode_suppresses_human_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            output = io.StringIO()
            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--summary-json",
                    "--quiet",
                ],
            ):
                with contextlib.redirect_stdout(output):
                    cli.main()

            raw = output.getvalue()
            self.assertNotIn("prompt-regression-min summary", raw)
            self.assertNotIn("- baseline:", raw)
            self.assertNotIn("- candidate:", raw)
            self.assertNotIn("- delta:", raw)
            self.assertNotIn("- outcome_counts:", raw)
            lines = [line for line in raw.splitlines() if line.strip()]
            summary_payload = json.loads(lines[-1])
            self.assertEqual(summary_payload["status"], "PASS")

    def test_cli_writes_summary_json_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"
            summary_file = tmp_path / "artifacts" / "summary.json"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--summary-json",
                    str(summary_file),
                ],
            ):
                cli.main()

            payload = json.loads(summary_file.read_text(encoding="utf-8"))
            self.assertEqual(payload["status"], "PASS")
            self.assertIn("summary", payload)

    def test_cli_emits_pretty_summary_json_to_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            output = io.StringIO()
            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--summary-json",
                    "--summary-json-pretty",
                    "--quiet",
                ],
            ):
                with contextlib.redirect_stdout(output):
                    cli.main()

            raw = output.getvalue()
            self.assertIn('\n  "status": "PASS"', raw)
            json_start = raw.find("{")
            self.assertGreaterEqual(json_start, 0)
            payload = json.loads(raw[json_start:])
            self.assertEqual(payload["status"], "PASS")

    def test_cli_writes_pretty_summary_json_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"
            summary_file = tmp_path / "artifacts" / "summary.pretty.json"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--summary-json",
                    str(summary_file),
                    "--summary-json-pretty",
                ],
            ):
                cli.main()

            raw = summary_file.read_text(encoding="utf-8")
            self.assertIn('\n  "status": "PASS"', raw)
            payload = json.loads(raw)
            self.assertEqual(payload["status"], "PASS")

    def test_cli_fail_payload_fixture_exposes_fail_reasons_and_gates(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        dataset = repo_root / "examples" / "dataset" / "fail_payload_gate_demo.jsonl"
        baseline = repo_root / "examples" / "outputs" / "fail_payload_gate_demo.baseline.jsonl"
        candidate = repo_root / "examples" / "outputs" / "fail_payload_gate_demo.candidate.jsonl"

        output = io.StringIO()
        with self.assertRaises(SystemExit) as exc:
            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--max-unchanged-fail",
                    "0",
                    "--summary-json",
                ],
            ):
                with contextlib.redirect_stdout(output):
                    cli.main()

        self.assertEqual(exc.exception.code, 1)
        lines = [line for line in output.getvalue().splitlines() if line.strip()]
        payload = json.loads(lines[-1])
        self.assertEqual(payload["status"], "FAIL")
        self.assertIn("fail_reasons", payload)
        self.assertTrue(any("unchanged failing cases" in reason for reason in payload["fail_reasons"]))
        self.assertEqual(payload["gates"]["max_unchanged_fail"], 0)

    def test_cli_rejects_invalid_min_candidate_pass_rate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--min-candidate-pass-rate",
                        "1.2",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)

    def test_cli_fails_when_unchanged_fail_rate_exceeds_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "a", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "b", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "a", "output": "ok"},
                    {"id": "b", "output": "bad"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "a", "output": "ok"},
                    {"id": "b", "output": "still bad"},
                ],
            )

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-unchanged-fail-rate",
                        "0.4",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_rejects_invalid_max_unchanged_fail_rate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-unchanged-fail-rate",
                        "1.1",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)

    def test_cli_rejects_invalid_max_unchanged_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-unchanged-fail",
                        "-2",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)


    def test_cli_mixed_fixture_supports_equals_any_and_regex_fullmatch(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        dataset = repo_root / "examples" / "dataset" / "mixed_expectations.jsonl"
        baseline = repo_root / "examples" / "outputs" / "mixed_expectations.baseline.jsonl"
        candidate = repo_root / "examples" / "outputs" / "mixed_expectations.candidate.jsonl"

        output = io.StringIO()
        with mock.patch(
            "sys.argv",
            [
                "prm",
                "run",
                "-d",
                str(dataset),
                "-b",
                str(baseline),
                "-c",
                str(candidate),
                "--max-regressions",
                "0",
                "--summary-json",
            ],
        ):
            with contextlib.redirect_stdout(output):
                cli.main()

        lines = [line for line in output.getvalue().splitlines() if line.strip()]
        summary_payload = json.loads(lines[-1])
        self.assertEqual(summary_payload["status"], "PASS")
        self.assertEqual(summary_payload["summary"]["regressions"], 0)
        self.assertEqual(summary_payload["summary"]["improved"], 1)

    def test_cli_prints_skipped_case_counters(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "a", "expected": {"type": "substring", "value": "ok"}},
                    {
                        "id": "b",
                        "disabled": True,
                        "expected": {"type": "substring", "value": "ok"},
                    },
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "a", "output": "ok"},
                    {"id": "b", "output": "bad"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "a", "output": "ok"},
                    {"id": "b", "output": "bad"},
                ],
            )

            output = io.StringIO()
            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                ],
            ):
                with contextlib.redirect_stdout(output):
                    cli.main()

            text = output.getvalue()
            self.assertIn("- skipped_cases: 1", text)
            self.assertIn("- skipped_ids: b", text)

    def test_cli_prints_unchanged_fail_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "a", "expected": {"type": "substring", "value": "ok"}}],
            )
            _write_jsonl(baseline, [{"id": "a", "output": "bad"}])
            _write_jsonl(candidate, [{"id": "a", "output": "still bad"}])

            output = io.StringIO()
            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--max-unchanged-fail",
                    "1",
                ],
            ):
                with contextlib.redirect_stdout(output):
                    cli.main()

            text = output.getvalue()
            self.assertIn("- unchanged_fail_ids: a", text)

    def test_cli_fails_when_delta_pass_rate_pp_below_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "a", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "b", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "a", "output": "ok"},
                    {"id": "b", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "a", "output": "ok"},
                    {"id": "b", "output": "bad"},
                ],
            )

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-regressions",
                        "1",
                        "--min-delta-pass-rate-pp",
                        "0",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_rejects_invalid_min_delta_pass_rate_pp(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--min-delta-pass-rate-pp",
                        "101",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)

    def test_cli_fails_when_delta_pass_rate_pp_exceeds_max_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "a", "expected": {"type": "substring", "value": "ok"}}],
            )
            _write_jsonl(baseline, [{"id": "a", "output": "bad"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-regressions",
                        "1",
                        "--max-delta-pass-rate-pp",
                        "50",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_rejects_invalid_max_delta_pass_rate_pp(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-delta-pass-rate-pp",
                        "101",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)

    def test_cli_fails_when_skipped_cases_exceed_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "a", "expected": {"type": "substring", "value": "ok"}},
                    {
                        "id": "b",
                        "disabled": True,
                        "expected": {"type": "substring", "value": "ok"},
                    },
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "a", "output": "ok"},
                    {"id": "b", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "a", "output": "ok"},
                    {"id": "b", "output": "ok"},
                ],
            )

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-skipped-cases",
                        "0",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_rejects_invalid_max_skipped_cases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-skipped-cases",
                        "-2",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)

    def test_cli_fails_when_improved_cases_below_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "a", "expected": {"type": "substring", "value": "ok"}}],
            )
            _write_jsonl(baseline, [{"id": "a", "output": "bad"}])
            _write_jsonl(candidate, [{"id": "a", "output": "still bad"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--min-improved",
                        "1",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_passes_when_improved_cases_meet_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "a", "expected": {"type": "substring", "value": "ok"}}],
            )
            _write_jsonl(baseline, [{"id": "a", "output": "bad"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--min-improved",
                    "1",
                ],
            ):
                cli.main()

    def test_cli_rejects_invalid_min_improved(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--min-improved",
                        "-1",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)

    def test_cli_fails_when_improved_cases_exceed_max(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "a", "expected": {"type": "substring", "value": "ok"}}],
            )
            _write_jsonl(baseline, [{"id": "a", "output": "bad"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-improved",
                        "0",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_fails_when_improved_rate_exceeds_max(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "a", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "b", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "a", "output": "bad"},
                    {"id": "b", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "a", "output": "ok"},
                    {"id": "b", "output": "ok"},
                ],
            )

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-regressions",
                        "0",
                        "--max-improved-rate",
                        "0.4",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_rejects_invalid_max_improved_rate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-improved-rate",
                        "1.1",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)

    def test_cli_rejects_invalid_max_improved(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-improved",
                        "-2",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)

    def test_cli_fails_when_active_cases_below_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "a", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "b", "disabled": True, "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}, {"id": "b", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}, {"id": "b", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--min-active-cases",
                        "2",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_rejects_invalid_min_active_cases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--min-active-cases",
                        "0",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)

    def test_cli_fails_when_filtered_out_cases_exceed_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "auth-a", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "billing-a", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "auth-a", "output": "ok"},
                    {"id": "billing-a", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "auth-a", "output": "ok"},
                    {"id": "billing-a", "output": "ok"},
                ],
            )

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--include-id-regex",
                        "^auth-",
                        "--max-filtered-out-cases",
                        "0",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_rejects_invalid_max_filtered_out_cases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-filtered-out-cases",
                        "-2",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)

    def test_cli_fails_when_filtered_out_rate_exceeds_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "auth-a", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "billing-a", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(baseline, [{"id": "auth-a", "output": "ok"}, {"id": "billing-a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "auth-a", "output": "ok"}, {"id": "billing-a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--include-id-regex",
                        "^auth-",
                        "--max-filtered-out-rate",
                        "0.4",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_rejects_invalid_max_filtered_out_rate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-filtered-out-rate",
                        "1.1",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)

    def test_cli_fails_when_changed_cases_exceed_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "a", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "b", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}, {"id": "b", "output": "bad"}])
            _write_jsonl(candidate, [{"id": "a", "output": "bad"}, {"id": "b", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-regressions",
                        "2",
                        "--max-changed-cases",
                        "1",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_fails_when_changed_rate_exceeds_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "a", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "b", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}, {"id": "b", "output": "bad"}])
            _write_jsonl(candidate, [{"id": "a", "output": "bad"}, {"id": "b", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-regressions",
                        "2",
                        "--max-changed-rate",
                        "0.40",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_rejects_invalid_max_changed_rate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-changed-rate",
                        "1.2",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)

    def test_cli_supports_case_id_regex_filters(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "auth-a", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "billing-a", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "auth-a", "output": "ok"},
                    {"id": "billing-a", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "auth-a", "output": "ok"},
                    {"id": "billing-a", "output": "bad"},
                ],
            )

            output = io.StringIO()
            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--include-id-regex",
                    "^auth-",
                ],
            ):
                with contextlib.redirect_stdout(output):
                    cli.main()

            text = output.getvalue()
            self.assertIn("- filtered_out_cases: 1", text)
            self.assertIn("- filtered_out_rate: 50.00%", text)
            self.assertIn("- filtered_out_ids: billing-a", text)

    def test_cli_fails_when_unchanged_pass_below_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "a", "expected": {"type": "substring", "value": "ok"}}],
            )
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "bad"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-regressions",
                        "1",
                        "--min-unchanged-pass",
                        "1",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_rejects_invalid_min_unchanged_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--min-unchanged-pass",
                        "-1",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)

    def test_cli_fails_when_unchanged_pass_exceeds_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-unchanged-pass",
                        "0",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_rejects_invalid_max_unchanged_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-unchanged-pass",
                        "-2",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)

    def test_cli_fixture_unchanged_pass_band_policy_passes(self) -> None:
        root = Path(__file__).resolve().parents[1]
        dataset = root / "examples" / "dataset" / "unchanged_pass_band_demo.jsonl"
        baseline = root / "examples" / "outputs" / "unchanged_pass_band_demo.baseline.jsonl"
        candidate = root / "examples" / "outputs" / "unchanged_pass_band_demo.candidate.jsonl"

        output = io.StringIO()
        with mock.patch(
            "sys.argv",
            [
                "prm",
                "run",
                "-d",
                str(dataset),
                "-b",
                str(baseline),
                "-c",
                str(candidate),
                "--min-unchanged-pass",
                "3",
                "--max-unchanged-pass",
                "3",
                "--summary-json",
            ],
        ):
            with contextlib.redirect_stdout(output):
                cli.main()

        payload = json.loads([line for line in output.getvalue().splitlines() if line.strip()][-1])
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["summary"]["unchanged_pass"], 3)
        self.assertEqual(payload["gates"]["min_unchanged_pass"], 3)
        self.assertEqual(payload["gates"]["max_unchanged_pass"], 3)

    def test_cli_fixture_improved_band_policy_passes(self) -> None:
        root = Path(__file__).resolve().parents[1]
        dataset = root / "examples" / "dataset" / "improved_band_demo.jsonl"
        baseline = root / "examples" / "outputs" / "improved_band_demo.baseline.jsonl"
        candidate = root / "examples" / "outputs" / "improved_band_demo.candidate.jsonl"

        output = io.StringIO()
        with mock.patch(
            "sys.argv",
            [
                "prm",
                "run",
                "-d",
                str(dataset),
                "-b",
                str(baseline),
                "-c",
                str(candidate),
                "--min-improved",
                "1",
                "--max-improved",
                "1",
                "--max-regressions",
                "0",
                "--summary-json",
            ],
        ):
            with contextlib.redirect_stdout(output):
                cli.main()

        payload = json.loads([line for line in output.getvalue().splitlines() if line.strip()][-1])
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["summary"]["improved"], 1)
        self.assertEqual(payload["gates"]["min_improved"], 1)
        self.assertEqual(payload["gates"]["max_improved"], 1)

    def test_cli_fixture_filtered_out_band_policy_passes(self) -> None:
        root = Path(__file__).resolve().parents[1]
        dataset = root / "examples" / "dataset" / "filtered_out_band_demo.jsonl"
        baseline = root / "examples" / "outputs" / "filtered_out_band_demo.baseline.jsonl"
        candidate = root / "examples" / "outputs" / "filtered_out_band_demo.candidate.jsonl"

        output = io.StringIO()
        with mock.patch(
            "sys.argv",
            [
                "prm",
                "run",
                "-d",
                str(dataset),
                "-b",
                str(baseline),
                "-c",
                str(candidate),
                "--include-id-regex",
                "^auth-",
                "--max-filtered-out-cases",
                "2",
                "--max-filtered-out-rate",
                "0.5",
                "--summary-json",
            ],
        ):
            with contextlib.redirect_stdout(output):
                cli.main()

        payload = json.loads([line for line in output.getvalue().splitlines() if line.strip()][-1])
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["summary"]["filtered_out_cases"], 2)
        self.assertEqual(payload["summary"]["filtered_out_rate"], 0.5)
        self.assertEqual(payload["gates"]["max_filtered_out_cases"], 2)
        self.assertEqual(payload["gates"]["max_filtered_out_rate"], 0.5)

    def test_cli_walkthrough_pass_fixture_matches_documented_improved_id(self) -> None:
        root = Path(__file__).resolve().parents[1]
        dataset = root / "examples" / "dataset" / "walkthrough_pass_artifact_demo.jsonl"
        baseline = root / "examples" / "outputs" / "walkthrough_pass_artifact_demo.baseline.jsonl"
        candidate = root / "examples" / "outputs" / "walkthrough_pass_artifact_demo.candidate.jsonl"

        output = io.StringIO()
        with mock.patch(
            "sys.argv",
            [
                "prm",
                "run",
                "-d",
                str(dataset),
                "-b",
                str(baseline),
                "-c",
                str(candidate),
                "--min-improved",
                "1",
                "--summary-json",
            ],
        ):
            with contextlib.redirect_stdout(output):
                cli.main()

        payload = json.loads([line for line in output.getvalue().splitlines() if line.strip()][-1])
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["summary"]["improved_ids"], ["checkout-copy"])

    def test_cli_walkthrough_fail_fixture_matches_documented_regression_id(self) -> None:
        root = Path(__file__).resolve().parents[1]
        dataset = root / "examples" / "dataset" / "walkthrough_fail_artifact_demo.jsonl"
        baseline = root / "examples" / "outputs" / "walkthrough_fail_artifact_demo.baseline.jsonl"
        candidate = root / "examples" / "outputs" / "walkthrough_fail_artifact_demo.candidate.jsonl"

        output = io.StringIO()
        with self.assertRaises(SystemExit) as exc:
            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--summary-json",
                ],
            ):
                with contextlib.redirect_stdout(output):
                    cli.main()
        self.assertEqual(exc.exception.code, 1)

        payload = json.loads([line for line in output.getvalue().splitlines() if line.strip()][-1])
        self.assertEqual(payload["status"], "FAIL")
        self.assertEqual(payload["summary"]["regression_ids"], ["auth-login"])

    def test_cli_rejects_invalid_case_id_regex(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--include-id-regex",
                        "[invalid",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)


    def test_cli_fails_when_stability_rate_below_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "a", "expected": {"type": "substring", "value": "ok"}}],
            )
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "bad"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-regressions",
                        "1",
                        "--min-stability-rate",
                        "0.1",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_fails_when_forbidden_unchanged_fail_id_regex_matches(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "auth-login", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "auth-login", "output": "bad"}])
            _write_jsonl(candidate, [{"id": "auth-login", "output": "still bad"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--forbid-unchanged-fail-id-regex",
                        "^auth-",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_rejects_invalid_forbidden_unchanged_fail_id_regex(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--forbid-unchanged-fail-id-regex",
                        "[invalid",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)

    def test_cli_rejects_invalid_min_stability_rate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--min-stability-rate",
                        "1.2",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 2)

    def test_cli_fails_when_pass_rate_trend_does_not_match_required_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--require-pass-rate-trend",
                        "improving",
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

    def test_cli_passes_when_pass_rate_trend_matches_required_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "bad"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--require-pass-rate-trend",
                    "improving",
                    "--summary-json",
                ],
            ):
                cli.main()

    def test_cli_summary_json_exposes_required_pass_rate_trend_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "bad"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            output = io.StringIO()
            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--require-pass-rate-trend",
                    "improving",
                    "--summary-json",
                ],
            ):
                with contextlib.redirect_stdout(output):
                    cli.main()

            payload = json.loads([line for line in output.getvalue().splitlines() if line.strip()][-1])
            self.assertEqual(payload["status"], "PASS")
            self.assertEqual(payload["gates"]["require_pass_rate_trend"], "improving")



    def test_walkthrough_artifact_drift_helper_passes_for_committed_snapshots(self) -> None:
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, str(root / "scripts" / "check_walkthrough_artifact_drift.py")],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("walkthrough artifact drift: PASS", result.stdout)
        self.assertIn("summary_schema_version=1", result.stdout)

    def test_walkthrough_markdown_snapshots_keep_schema_and_status_markers(self) -> None:
        root = Path(__file__).resolve().parents[1]
        pass_md = (root / "examples" / "artifacts" / "walkthrough-pass.summary.md").read_text(encoding="utf-8")
        fail_md = (root / "examples" / "artifacts" / "walkthrough-fail.summary.md").read_text(encoding="utf-8")

        self.assertIn("## prompt-regression-min summary", pass_md)
        self.assertIn(f"- Tool version: `{cli.__version__}`", pass_md)
        self.assertIn("- Summary schema version: `1`", pass_md)
        self.assertIn("- Required schema version gate: `1`", pass_md)
        self.assertIn("- Status: **PASS**", pass_md)
        self.assertIn("- Selected dataset IDs: `checkout-copy`, `policy-note`", pass_md)
        self.assertIn("- Selection rate: 100.00% of source cases", pass_md)
        self.assertIn("- Active case IDs: `checkout-copy`, `policy-note`", pass_md)

        self.assertIn("## prompt-regression-min summary", fail_md)
        self.assertIn(f"- Tool version: `{cli.__version__}`", fail_md)
        self.assertIn("- Summary schema version: `1`", fail_md)
        self.assertIn("- Required schema version gate: `1`", fail_md)
        self.assertIn("- Status: **FAIL**", fail_md)

        walkthrough_pass_pr_comment = (root / "examples" / "artifacts" / "walkthrough-pass.pr-comment.md").read_text(encoding="utf-8")
        self.assertIn("## walkthrough approval note", walkthrough_pass_pr_comment)
        self.assertIn("Summary schema version: `1`", walkthrough_pass_pr_comment)
        self.assertIn(f"Tool version: `{cli.__version__}`", walkthrough_pass_pr_comment)
        self.assertIn("Required schema version gate: `1`", walkthrough_pass_pr_comment)
        self.assertIn("Pass-rate trend: `improving`", walkthrough_pass_pr_comment)
        self.assertIn("Improved IDs (1): `checkout-copy`", walkthrough_pass_pr_comment)
        self.assertIn("Changed IDs (1): `checkout-copy`", walkthrough_pass_pr_comment)
        self.assertIn("Stable IDs: `policy-note`", walkthrough_pass_pr_comment)

        walkthrough_fail_pr_comment = (root / "examples" / "artifacts" / "walkthrough-fail.pr-comment.md").read_text(encoding="utf-8")
        self.assertIn("## walkthrough blocker note", walkthrough_fail_pr_comment)
        self.assertIn("Summary schema version: `1`", walkthrough_fail_pr_comment)
        self.assertIn(f"Tool version: `{cli.__version__}`", walkthrough_fail_pr_comment)
        self.assertIn("Required schema version gate: `1`", walkthrough_fail_pr_comment)
        self.assertIn("Pass-rate trend: `regressing`", walkthrough_fail_pr_comment)
        self.assertIn("auth-login", walkthrough_fail_pr_comment)
        self.assertIn("Status: **FAIL**", walkthrough_fail_pr_comment)

        word_count_md = (root / "examples" / "artifacts" / "word-count-range.summary.md").read_text(encoding="utf-8")
        self.assertIn("## word-count release-note gate", word_count_md)
        word_count_pr_comment = (root / "examples" / "artifacts" / "word-count-range.pr-comment.md").read_text(encoding="utf-8")
        self.assertIn("## word-count blocker note", word_count_pr_comment)
        self.assertIn("Summary schema version: `1`", word_count_pr_comment)
        self.assertIn(f"Tool version: `{cli.__version__}`", word_count_pr_comment)
        self.assertIn("Required schema version gate: _disabled_", word_count_pr_comment)
        self.assertIn("release-note-bullets", word_count_pr_comment)
        self.assertIn("release-note-short", word_count_pr_comment)
        self.assertIn(f"- Tool version: `{cli.__version__}`", word_count_md)
        self.assertIn("- Summary schema version: `1`", word_count_md)
        self.assertIn("- Status: **FAIL**", word_count_md)
        self.assertIn("- Selected dataset IDs: `release-note-bullets`, `release-note-short`", word_count_md)
        self.assertIn("- Active case IDs: `release-note-bullets`, `release-note-short`", word_count_md)

    def test_cli_writes_summary_markdown_file_with_custom_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"
            summary_md = tmp_path / "artifacts" / "summary.custom.md"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--summary-markdown",
                    str(summary_md),
                    "--summary-markdown-title",
                    "nightly reviewer handoff",
                ],
            ):
                cli.main()

            markdown = summary_md.read_text(encoding="utf-8")
            self.assertIn("## nightly reviewer handoff", markdown)
            self.assertNotIn("## prompt-regression-min summary", markdown)

    def test_cli_writes_summary_pr_comment_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"
            pr_comment = tmp_path / "artifacts" / "summary.pr-comment.md"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--summary-pr-comment",
                    str(pr_comment),
                    "--summary-pr-comment-title",
                    "review snapshot",
                ],
            ):
                cli.main()

            rendered = pr_comment.read_text(encoding="utf-8")
            self.assertIn("## review snapshot", rendered)
            self.assertIn("- Status: **PASS**", rendered)
            self.assertIn("- Summary schema version: `1`", rendered)
            self.assertIn("- Pass-rate trend: `flat`", rendered)
            self.assertIn("- Coverage watch: selected=1, active=1, skipped=0, filtered_out=0", rendered)
            self.assertIn("- Stable IDs: `a`", rendered)
            self.assertIn("approval-ready", rendered)

    def test_cli_summary_pr_comment_includes_case_filters_and_coverage_watch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"
            pr_comment = tmp_path / "artifacts" / "summary.pr-comment.md"

            _write_jsonl(
                dataset,
                [
                    {"id": "auth-pass", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "ops-skip", "expected": {"type": "substring", "value": "ok"}, "disabled": True},
                    {"id": "billing-out", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "auth-pass", "output": "ok"},
                    {"id": "ops-skip", "output": "ok"},
                    {"id": "billing-out", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "auth-pass", "output": "ok"},
                    {"id": "ops-skip", "output": "ok"},
                    {"id": "billing-out", "output": "ok"},
                ],
            )

            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--include-id-regex",
                    "^auth-|^ops-",
                    "--summary-pr-comment",
                    str(pr_comment),
                ],
            ):
                cli.main()

            rendered = pr_comment.read_text(encoding="utf-8")
            self.assertIn("- Coverage watch: selected=2, active=1, skipped=1, filtered_out=1", rendered)
            self.assertIn("- Case filters: include=`^auth-|^ops-`, exclude=_none_", rendered)
            self.assertIn("- Filtered-out IDs: `billing-out`", rendered)
            self.assertIn("- Filtered-out rate: 33.33% of source cases", rendered)
            self.assertIn("- Skipped IDs: `ops-skip`", rendered)
            self.assertIn("- Skipped-case rate: 100.00% of active cases", rendered)
            self.assertIn("- Skipped source-case rate: 33.33% of source cases", rendered)


    def test_cli_allows_custom_summary_pr_comment_title_without_changing_markdown_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"
            summary_md = tmp_path / "summary.md"
            pr_comment = tmp_path / "summary.pr-comment.md"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--summary-markdown",
                    str(summary_md),
                    "--summary-markdown-title",
                    "release gate summary",
                    "--summary-pr-comment",
                    str(pr_comment),
                    "--summary-pr-comment-title",
                    "review snapshot",
                ],
            ):
                cli.main()

            self.assertIn("## release gate summary", summary_md.read_text(encoding="utf-8"))
            rendered = pr_comment.read_text(encoding="utf-8")
            self.assertIn("## review snapshot", rendered)
            self.assertNotIn("## release gate summary", rendered)

    def test_cli_prints_summary_pr_comment_to_stdout_when_dash_is_used(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "auth-login", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "auth-login", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "auth-login", "output": "nope"}])

            stdout = io.StringIO()
            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--summary-pr-comment",
                    "-",
                ],
            ), mock.patch("sys.stdout", stdout):
                with self.assertRaises(SystemExit) as ctx:
                    cli.main()

            self.assertEqual(ctx.exception.code, 1)
            rendered = stdout.getvalue()
            self.assertIn("## prompt-regression-min summary", rendered)
            self.assertIn("- Status: **FAIL**", rendered)
            self.assertIn("- Regression IDs (1): `auth-login`", rendered)
            self.assertIn("- Changed IDs (1): `auth-login`", rendered)
            self.assertIn("- Why it failed:", rendered)
            self.assertIn("keep the PR blocked", rendered)

    def test_cli_applies_custom_summary_pr_comment_title_to_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "auth-login", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "auth-login", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "auth-login", "output": "nope"}])

            stdout = io.StringIO()
            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--summary-pr-comment",
                    "-",
                    "--summary-pr-comment-title",
                    "stdout blocker note",
                ],
            ), mock.patch("sys.stdout", stdout):
                with self.assertRaises(SystemExit) as ctx:
                    cli.main()

            self.assertEqual(ctx.exception.code, 1)
            rendered = stdout.getvalue()
            self.assertIn("## stdout blocker note", rendered)
            self.assertNotIn("## prompt-regression-min summary", rendered)

    def test_cli_prints_summary_markdown_to_stdout_when_dash_is_used(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            output = io.StringIO()
            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--summary-markdown",
                    "-",
                    "--summary-markdown-title",
                    "stdout reviewer handoff",
                    "--quiet",
                ],
            ):
                with contextlib.redirect_stdout(output):
                    cli.main()

            markdown = output.getvalue()
            self.assertIn("## stdout reviewer handoff", markdown)
            self.assertIn(f"- Tool version: `{cli.__version__}`", markdown)
            self.assertIn("- Status: **PASS**", markdown)
            self.assertNotIn("summary_markdown:", markdown)

    def test_cli_writes_summary_markdown_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"
            summary_md = tmp_path / "artifacts" / "summary.md"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--summary-markdown",
                    str(summary_md),
                ],
            ):
                cli.main()

            markdown = summary_md.read_text(encoding="utf-8")
            self.assertIn("## prompt-regression-min summary", markdown)
            self.assertIn(f"- Tool version: `{cli.__version__}`", markdown)
            self.assertIn("- Summary schema version: `1`", markdown)
            self.assertIn("- Required schema version gate: _not set_", markdown)
            self.assertIn("- Status: **PASS**", markdown)

    def test_cli_summary_markdown_includes_required_schema_version_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"
            summary_md = tmp_path / "artifacts" / "summary.md"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--summary-markdown",
                    str(summary_md),
                    "--require-summary-schema-version",
                    "1",
                ],
            ):
                cli.main()

            markdown = summary_md.read_text(encoding="utf-8")
            self.assertIn("- Required schema version gate: `1`", markdown)
            self.assertIn("  - require_summary_schema_version=1", markdown)

    def test_cli_summary_markdown_gate_snapshot_includes_changed_and_filtered_budget_lines(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"
            summary_md = tmp_path / "artifacts" / "summary.md"

            _write_jsonl(dataset, [{"id": "auth-1", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "auth-1", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "auth-1", "output": "ok"}])

            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--summary-markdown",
                    str(summary_md),
                    "--max-changed-cases",
                    "0",
                    "--max-filtered-out-cases",
                    "0",
                    "--max-filtered-out-rate",
                    "0.0",
                ],
            ):
                cli.main()

            markdown = summary_md.read_text(encoding="utf-8")
            self.assertIn("  - max_changed_cases=0", markdown)
            self.assertIn("  - max_filtered_out_cases=0", markdown)
            self.assertIn("  - max_filtered_out_rate=0.0", markdown)

    def test_cli_summary_markdown_includes_case_filters(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"
            summary_md = tmp_path / "artifacts" / "summary.md"

            _write_jsonl(dataset, [{"id": "auth-1", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "auth-1", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "auth-1", "output": "ok"}])

            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--summary-markdown",
                    str(summary_md),
                    "--include-id-regex",
                    "^auth-",
                    "--exclude-id-regex=-canary$",
                ],
            ):
                cli.main()

            markdown = summary_md.read_text(encoding="utf-8")
            self.assertIn("- Case filters: include=`^auth-`, exclude=`-canary$`", markdown)

    def test_cli_summary_markdown_includes_forbidden_unchanged_fail_regex_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"
            summary_md = tmp_path / "artifacts" / "summary.md"

            _write_jsonl(dataset, [{"id": "auth-login", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "auth-login", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "auth-login", "output": "ok"}])

            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--summary-markdown",
                    str(summary_md),
                    "--forbid-unchanged-fail-id-regex",
                    "^auth-",
                ],
            ):
                cli.main()

            markdown = summary_md.read_text(encoding="utf-8")
            self.assertIn("  - forbid_unchanged_fail_id_regex=^auth-", markdown)

    def test_cli_summary_markdown_includes_filtered_skipped_and_unchanged_fail_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"
            summary_md = tmp_path / "artifacts" / "summary.md"

            _write_jsonl(
                dataset,
                [
                    {"id": "auth-keep", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "ops-skip", "disabled": True, "expected": {"type": "substring", "value": "ok"}},
                    {"id": "billing-out", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "auth-keep", "output": "bad"},
                    {"id": "ops-skip", "output": "bad"},
                    {"id": "billing-out", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "auth-keep", "output": "still bad"},
                    {"id": "ops-skip", "output": "bad"},
                    {"id": "billing-out", "output": "ok"},
                ],
            )

            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--summary-markdown",
                    str(summary_md),
                    "--include-id-regex",
                    "^auth-|^ops-",
                    "--max-unchanged-fail",
                    "1",
                ],
            ):
                cli.main()

            markdown = summary_md.read_text(encoding="utf-8")
            self.assertIn("- Filtered-out IDs (1): `billing-out`", markdown)
            self.assertIn("- Scope reduction: 33.33% of source cases removed by filters", markdown)
            self.assertIn("- Skipped IDs (1): `ops-skip`", markdown)
            self.assertIn("- Skipped-case rate: 100.00% of active cases", markdown)
            self.assertIn("- Skipped source-case rate: 33.33% of source cases", markdown)
            self.assertIn("- Unchanged fail IDs (1): `auth-keep`", markdown)

    def test_cli_summary_markdown_includes_fail_reasons(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"
            summary_md = tmp_path / "artifacts" / "summary.md"

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "bad"}])

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--summary-markdown",
                        str(summary_md),
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

            markdown = summary_md.read_text(encoding="utf-8")
            self.assertIn("- Status: **FAIL**", markdown)
    def test_summary_markdown_includes_active_case_rate_for_filtered_shards(self) -> None:
        root = Path(__file__).resolve().parents[1]
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with mock.patch(
                "sys.argv",
                [
                    "prm",
                    "run",
                    "--dataset",
                    str(root / "examples" / "dataset" / "filtered_out_band_demo.jsonl"),
                    "--baseline",
                    str(root / "examples" / "outputs" / "filtered_out_band_demo.baseline.jsonl"),
                    "--candidate",
                    str(root / "examples" / "outputs" / "filtered_out_band_demo.candidate.jsonl"),
                    "--include-id-regex",
                    "^auth-",
                    "--max-filtered-out-cases",
                    "2",
                    "--max-filtered-out-rate",
                    "0.5",
                    "--summary-markdown",
                    "-",
                ],
            ):
                cli.main()
        markdown = output.getvalue()
        self.assertIn("- Selection rate: 50.00% of source cases", markdown)
        self.assertIn("- Active-case rate: 50.00% of source cases", markdown)

    def test_summary_pr_comment_includes_unchanged_fail_watchlist_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "watch-auth", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "stable-pass", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "watch-auth", "output": "bad"},
                    {"id": "stable-pass", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "watch-auth", "output": "bad"},
                    {"id": "stable-pass", "output": "ok"},
                ],
            )

            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--summary-pr-comment",
                        "-",
                        "--quiet",
                    ],
                ):
                    cli.main()
            pr_comment = output.getvalue()
            self.assertIn("- Stable IDs: `stable-pass`", pr_comment)
            self.assertIn("- Unchanged fail IDs: `watch-auth`", pr_comment)
            self.assertIn("- Watchlist rate: 50.00% of active cases", pr_comment)
            self.assertIn("- Watchlist source-case rate: 50.00% of source cases", pr_comment)
            self.assertIn("- Reviewer queue total: 1 case(s)", pr_comment)
            self.assertIn("- Reviewer queue (watchlist): 1 case(s) / 50.00% of active cases / 50.00% of source cases", pr_comment)

    def test_summary_markdown_includes_unchanged_pass_ids_for_handoff_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "stable-pass", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "reg-1", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "stable-pass", "output": "ok"},
                    {"id": "reg-1", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "stable-pass", "output": "ok"},
                    {"id": "reg-1", "output": "bad"},
                ],
            )

            output = io.StringIO()
            with self.assertRaises(SystemExit):
                with contextlib.redirect_stdout(output):
                    with mock.patch(
                        "sys.argv",
                        [
                            "prm",
                            "run",
                            "-d",
                            str(dataset),
                            "-b",
                            str(baseline),
                            "-c",
                            str(candidate),
                            "--summary-markdown",
                            "-",
                            "--quiet",
                        ],
                    ):
                        cli.main()
            markdown = output.getvalue()
            self.assertIn("- Unchanged pass IDs (1): `stable-pass`", markdown)
            self.assertIn("- Regression IDs (1): `reg-1`", markdown)

            self.assertIn("- Fail reasons:", markdown)


if __name__ == "__main__":
    unittest.main()


    def test_cli_summary_markdown_lists_changed_and_filtered_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"
            summary_markdown = tmp_path / "summary.md"

            _write_jsonl(
                dataset,
                [
                    {"id": "keep-pass", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "reg-1", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "filtered-out", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "keep-pass", "output": "ok"},
                    {"id": "reg-1", "output": "ok"},
                    {"id": "filtered-out", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "keep-pass", "output": "ok"},
                    {"id": "reg-1", "output": "bad"},
                    {"id": "filtered-out", "output": "ok"},
                ],
            )

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--exclude-id-regex",
                        "^filtered-",
                        "--summary-markdown",
                        str(summary_markdown),
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)
            rendered = summary_markdown.read_text(encoding="utf-8")
            self.assertIn("- Dataset scope: source=3, selected=2, active=2", rendered)
            self.assertIn("- Selection rate: 66.67% of source cases", rendered)
            self.assertIn("- Changed IDs: `reg-1`", rendered)
            self.assertIn("- Changed-case rate: 50.00%", rendered)
            self.assertIn("- Filtered-out IDs: `filtered-out`", rendered)
            self.assertIn("- Filtered-out rate: 33.33% of source cases", rendered)
            self.assertIn("- Scope reduction: 33.33% of source cases removed by filters", rendered)

    def test_cli_fixture_trend_stability_policy_passes(self) -> None:
        root = Path(__file__).resolve().parents[1]
        dataset = root / "examples" / "dataset" / "trend_stability_demo.jsonl"
        baseline = root / "examples" / "outputs" / "trend_stability_demo.baseline.jsonl"
        candidate = root / "examples" / "outputs" / "trend_stability_demo.candidate.jsonl"

        with tempfile.TemporaryDirectory() as tmpdir:
            summary_path = Path(tmpdir) / "trend-stability-summary.json"
            with self.assertRaises(SystemExit) as ctx, redirect_stdout(io.StringIO()):
                with patch.object(
                    sys,
                    "argv",
                    [
                        "prm",
                        "run",
                        "-d",
                        str(dataset),
                        "-b",
                        str(baseline),
                        "-c",
                        str(candidate),
                        "--max-regressions",
                        "1",
                        "--min-stability-rate",
                        "0.5",
                        "--require-pass-rate-trend",
                        "flat",
                        "--summary-json",
                        str(summary_path),
                        "--quiet",
                    ],
                ):
                    cli.main()

            self.assertEqual(ctx.exception.code, 0)
            payload = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["status"], "PASS")
            self.assertEqual(payload["summary"]["pass_rate_trend"], "flat")
            self.assertEqual(payload["summary"]["stability_rate"], 0.5)
            self.assertEqual(payload["summary"]["regression_ids"], ["checkout-regressed"])
            self.assertEqual(payload["summary"]["improved_ids"], ["checkout-improved"])
            self.assertEqual(payload["gates"]["min_stability_rate"], 0.5)
            self.assertEqual(payload["gates"]["require_pass_rate_trend"], "flat")




    def test_summary_json_includes_structured_reviewer_queue(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"
            summary_json = tmp_path / "summary.json"

            _write_jsonl(
                dataset,
                [
                    {"id": "reg-1", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "watch-1", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "skip-1", "expected": {"type": "substring", "value": "ok"}, "skip": True},
                    {"id": "scope-1", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "reg-1", "output": "ok"},
                    {"id": "watch-1", "output": "bad"},
                    {"id": "skip-1", "output": "ok"},
                    {"id": "scope-1", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "reg-1", "output": "bad"},
                    {"id": "watch-1", "output": "bad"},
                    {"id": "skip-1", "output": "ok"},
                    {"id": "scope-1", "output": "ok"},
                ],
            )

            with self.assertRaises(SystemExit) as exc:
                with mock.patch(
                    "sys.argv",
                    [
                        "prm", "run", "-d", str(dataset), "-b", str(baseline), "-c", str(candidate),
                        "--exclude-id-regex", "^scope-", "--summary-json", str(summary_json), "--quiet"
                    ],
                ):
                    cli.main()
            self.assertEqual(exc.exception.code, 1)

            payload = json.loads(summary_json.read_text(encoding="utf-8"))
            self.assertEqual(payload["reviewer_queue"]["total"], 4)
            self.assertEqual(payload["reviewer_queue"]["rate"], 1.3333)
            self.assertEqual(payload["reviewer_queue"]["source_case_rate"], 1.0)
            self.assertEqual(payload["reviewer_queue"]["group_count"], 4)
            self.assertEqual(
                payload["reviewer_queue"]["follow_up_priority"],
                [
                    "fix_regressions",
                    "watch_unchanged_fails",
                    "confirm_filtered_scope",
                    "resolve_skipped_cases",
                ],
            )
            self.assertEqual(payload["reviewer_queue"]["largest_group_key"], "watch_unchanged_fails")
            self.assertEqual(payload["reviewer_queue"]["largest_group_keys"], ["fix_regressions", "watch_unchanged_fails", "confirm_filtered_scope", "resolve_skipped_cases"])
            self.assertEqual(payload["reviewer_queue"]["largest_group_labels"], ["fix regressions", "watch unchanged fails", "confirm filtered-out scope", "resolve skipped cases"])
            self.assertEqual(payload["reviewer_queue"]["largest_group_count"], 1)
            self.assertEqual(
                payload["reviewer_queue"]["groups"],
                [
                    {"key": "fix_regressions", "label": "fix regressions", "ids": ["reg-1"], "count": 1, "rate": 0.3333, "source_case_rate": 0.25, "queue_share": 0.25},
                    {"key": "watch_unchanged_fails", "label": "watch unchanged fails", "ids": ["watch-1"], "count": 1, "rate": 0.3333, "source_case_rate": 0.25, "queue_share": 0.25},
                    {"key": "confirm_filtered_scope", "label": "confirm filtered-out scope", "ids": ["scope-1"], "count": 1, "rate": 0.3333, "source_case_rate": 0.25, "queue_share": 0.25},
                    {"key": "resolve_skipped_cases", "label": "resolve skipped cases", "ids": ["skip-1"], "count": 1, "rate": 0.3333, "source_case_rate": 0.25, "queue_share": 0.25},
                ],
            )


    def test_summary_json_reviewer_queue_defaults_when_empty(self) -> None:
        payload = cli._build_reviewer_queue({"active_cases": 3})

        self.assertEqual(payload["total"], 0)
        self.assertEqual(payload["source_case_rate"], 0.0)
        self.assertEqual(payload["group_count"], 0)
        self.assertEqual(payload["follow_up_priority"], [])
        self.assertIsNone(payload["largest_group_key"])
        self.assertIsNone(payload["largest_group_label"])
        self.assertEqual(payload["largest_group_count"], 0)
        self.assertIsNone(payload["largest_group_priority_rank"])
        self.assertEqual(payload["largest_group_keys"], [])
        self.assertEqual(payload["largest_group_labels"], [])
        self.assertEqual(payload["groups"], [])

    def test_summary_json_exposes_largest_group_label_for_handoff_copy(self) -> None:
        payload = cli._build_reviewer_queue(
            {
                "active_cases": 3,
                "dataset_cases": 5,
                "regression_ids": ["checkout-copy", "policy-note"],
                "unchanged_fail_ids": ["watch-auth"],
                "filtered_out_ids": [],
                "skipped_ids": [],
            }
        )

        self.assertEqual(payload["largest_group_key"], "fix_regressions")
        self.assertEqual(payload["largest_group_label"], "fix regressions")
        self.assertEqual(payload["largest_group_ids"], ["checkout-copy", "policy-note"])
        self.assertEqual(payload["largest_group_keys"], ["fix_regressions"])
        self.assertEqual(payload["largest_group_labels"], ["fix regressions"])
        self.assertEqual(payload["largest_group_queue_share"], 0.6667)
        self.assertEqual(payload["largest_group_priority_rank"], 1)


    def test_summary_outputs_include_reviewer_queue_for_scope_and_watchlist_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "reg-1", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "watch-1", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "skip-1", "expected": {"type": "substring", "value": "ok"}, "skip": True},
                    {"id": "scope-1", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "reg-1", "output": "ok"},
                    {"id": "watch-1", "output": "bad"},
                    {"id": "skip-1", "output": "ok"},
                    {"id": "scope-1", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "reg-1", "output": "bad"},
                    {"id": "watch-1", "output": "bad"},
                    {"id": "skip-1", "output": "ok"},
                    {"id": "scope-1", "output": "ok"},
                ],
            )

            markdown_output = io.StringIO()
            with contextlib.redirect_stdout(markdown_output):
                with self.assertRaises(SystemExit):
                    with mock.patch(
                        "sys.argv",
                        [
                            "prm", "run", "-d", str(dataset), "-b", str(baseline), "-c", str(candidate),
                            "--exclude-id-regex", "^scope-", "--summary-markdown", "-"
                        ],
                    ):
                        cli.main()
            markdown = markdown_output.getvalue()
            self.assertIn("- Reviewer queue total: 4 case(s)", markdown)
            self.assertIn("- Reviewer queue rate: 133.33% of active cases", markdown)
            self.assertIn("- Reviewer queue source-case rate: 100.00% of source cases", markdown)
            self.assertIn("- Reviewer queue dominant focus: fix regressions", markdown)
            self.assertIn("- Reviewer queue: fix regressions: `reg-1` | watch unchanged fails: `watch-1` | confirm filtered-out scope: `scope-1` | resolve skipped cases: `skip-1`", markdown)

            pr_output = io.StringIO()
            with contextlib.redirect_stdout(pr_output):
                with self.assertRaises(SystemExit):
                    with mock.patch(
                        "sys.argv",
                        [
                            "prm", "run", "-d", str(dataset), "-b", str(baseline), "-c", str(candidate),
                            "--exclude-id-regex", "^scope-", "--summary-pr-comment", "-", "--quiet"
                        ],
                    ):
                        cli.main()
            pr_comment = pr_output.getvalue()
            self.assertIn("- Reviewer queue total: 4 case(s)", pr_comment)
            self.assertIn("- Reviewer queue rate: 133.33% of active cases", pr_comment)
            self.assertIn("- Reviewer queue source-case rate: 100.00% of source cases", pr_comment)
            self.assertIn("- Reviewer queue: fix regressions: `reg-1` | watch unchanged fails: `watch-1` | confirm filtered-out scope: `scope-1` | resolve skipped cases: `skip-1`", pr_comment)
