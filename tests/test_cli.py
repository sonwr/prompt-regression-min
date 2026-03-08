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

            _write_jsonl(dataset, [{"id": "a", "expected": {"type": "substring", "value": "ok"}}])
            _write_jsonl(baseline, [{"id": "a", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "a", "output": "ok"}])

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
                        "--quiet",
                    ],
                ):
                    cli.main()

            rendered = output.getvalue()
            self.assertIn("## prompt-regression-min summary", rendered)
            self.assertIn("- Status: **PASS**", rendered)
            self.assertNotIn("prompt-regression-min summary\n- cases:", rendered)

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
        self.assertIn("- Summary schema version: `1`", pass_md)
        self.assertIn("- Status: **PASS**", pass_md)

        self.assertIn("## prompt-regression-min summary", fail_md)
        self.assertIn("- Summary schema version: `1`", fail_md)
        self.assertIn("- Status: **FAIL**", fail_md)

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
            self.assertIn("- Summary schema version: `1`", markdown)
            self.assertIn("- Status: **PASS**", markdown)

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
            self.assertIn("- Fail reasons:", markdown)


if __name__ == "__main__":
    unittest.main()
