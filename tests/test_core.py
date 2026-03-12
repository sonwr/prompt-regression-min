from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from prompt_regression_min.core import run_regression


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


class RegressionCoreTests(unittest.TestCase):
    def test_readme_mentions_reviewer_queue_bundle_gate_note(self) -> None:
        readme = (Path(__file__).resolve().parents[1] / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_bundle_gate_note.md", readme)
        self.assertTrue(
            (Path(__file__).resolve().parents[1] / "examples" / "reviewer_queue_bundle_gate_note.md").exists()
        )

    def test_readme_mentions_report_bundle_reopen_check(self) -> None:
        readme = (Path(__file__).resolve().parents[1] / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_report_bundle_reopen_check.md", readme)
        self.assertTrue(
            (Path(__file__).resolve().parents[1] / "examples" / "reviewer_queue_report_bundle_reopen_check.md").exists()
        )

    def test_readme_mentions_priority_rank_scope_release_note(self) -> None:
        readme = (Path(__file__).resolve().parents[1] / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_priority_rank_scope_release_note.md", readme)
        self.assertTrue(
            (Path(__file__).resolve().parents[1] / "examples" / "reviewer_queue_priority_rank_scope_release_note.md").exists()
        )

    def test_readme_mentions_report_bundle_scope_note(self) -> None:
        readme = (Path(__file__).resolve().parents[1] / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_report_bundle_scope_note.md", readme)
        self.assertTrue(
            (Path(__file__).resolve().parents[1] / "examples" / "reviewer_queue_report_bundle_scope_note.md").exists()
        )

    def test_run_regression_supports_paragraph_count_range_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "paragraph_count_range", "min_paragraphs": 2, "max_paragraphs": 2}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Alpha ships now.\n\nBeta follows soon."}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Alpha ships now."}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_rejects_paragraph_count_range_without_bounds(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "paragraph_count_range"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Alpha."}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Alpha."}])

            with self.assertRaises(ValueError) as exc:
                run_regression(str(dataset), str(baseline), str(candidate))

            self.assertIn("set min_paragraphs, max_paragraphs, or both", str(exc.exception))

    def test_run_regression_supports_sentence_count_range_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "sentence_count_range", "min_sentences": 2, "max_sentences": 3}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Alpha ships now. Beta follows soon!"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Alpha ships now"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_rejects_sentence_count_range_without_bounds(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "sentence_count_range"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Alpha."}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Alpha."}])

            with self.assertRaises(ValueError) as exc:
                run_regression(str(dataset), str(baseline), str(candidate))

            self.assertIn("set min_sentences, max_sentences, or both", str(exc.exception))

    def test_run_regression_counts_korean_and_japanese_sentence_punctuation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "sentence_count_range", "min_sentences": 2, "max_sentences": 2}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "안녕하세요. 테스트입니다."}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "좋습니다。続けます！"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 0)
            self.assertEqual(report["summary"]["unchanged_pass"], 1)
            self.assertEqual(report["summary"]["improved"], 0)

    def test_run_regression_ignores_inverted_sentence_punctuation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "sentence_count_range", "min_sentences": 2, "max_sentences": 2}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "¿Listo? ¡Vamos!"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Listo? Vamos!"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 0)
            self.assertEqual(report["summary"]["unchanged_pass"], 1)

    def test_run_regression_supports_contains_all_ordered_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "contains_all_ordered", "values": ["step 1", "step 2", "step 3"]}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "step 1 -> step 2 -> step 3"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "step 2 -> step 1 -> step 3"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_contains_all_ordered_ci_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "contains_all_ordered_ci", "values": ["alpha", "beta", "gamma"]}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ALPHA then beta then Gamma"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "beta before ALPHA then gamma"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_regex_flags_as_pipe_delimited_string(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "regex", "pattern": "^alpha.+omega$", "flags": " ignorecase | dotall "}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ALPHA\nmid\nomega"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "beta\nmid\nomega"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_regex_flag_alias_for_single_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "regex", "pattern": "^alpha$", "flag": "ignorecase"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ALPHA"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "beta"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_regex_flags_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "regex", "pattern": "^alpha.+omega$", "regex_flags": "ignorecase,dotall"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ALPHA\nmid\nomega"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "omega\nmid\nalpha"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_regex_flags_as_comma_delimited_string(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "regex", "pattern": "^alpha.+omega$", "flags": "ignorecase, dotall"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ALPHA\nmid\nomega"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "omega\nmid\nalpha"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_regex_flags_list_with_blank_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "regex", "pattern": "^alpha.+omega$", "flags": [" ignorecase ", "", " dotall ", "   "]}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ALPHA\nmid\nomega"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "omega\nmid\nalpha"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_regex_flags_as_newline_delimited_string(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "regex", "pattern": "^alpha.+omega$", "flags": "ignorecase\n dotall"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ALPHA\nmid\nomega"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "omega\nmid\nalpha"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_short_regex_flag_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "regex", "pattern": "^alpha.+omega$", "flags": ["i", "s"]}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ALPHA\nmid\nomega"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "omega\nmid\nalpha"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_regex_verbose_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{
                    "id": "case-1",
                    "expected": {
                        "type": "regex",
                        "pattern": """
                            ^alpha   # prefix\n                            \s+beta  # separator\n                            \s+omega$
                        """,
                        "flags": ["verbose", "ignorecase"],
                    },
                }],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ALPHA beta omega"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "beta omega"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_rejects_non_string_non_list_regex_flags(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "regex", "pattern": "alpha", "flags": 123}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "alpha"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "alpha"}])

            with self.assertRaises(ValueError) as exc:
                run_regression(str(dataset), str(baseline), str(candidate))

            self.assertIn("must be a list or string", str(exc.exception))

    def test_run_regression_rejects_unsupported_regex_flag_from_pipe_string(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "regex", "pattern": "alpha", "flags": "ignorecase | nope"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "alpha"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "alpha"}])

            with self.assertRaises(ValueError) as exc:
                run_regression(str(dataset), str(baseline), str(candidate))

            self.assertIn("Unsupported regex flag in dataset id=case-1: NOPE", str(exc.exception))

    def test_run_regression_supports_byte_count_range_for_multibyte_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "byte_count_range", "min_bytes": 6, "max_bytes": 6}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "가나"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "abc"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_rejects_byte_count_range_without_bounds(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "byte_count_range"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "가나"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "가나"}])

            with self.assertRaises(ValueError) as exc:
                run_regression(str(dataset), str(baseline), str(candidate))

            self.assertIn("set min_bytes, max_bytes, or both", str(exc.exception))

    def test_run_regression_supports_byte_count_range_for_single_emoji_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "byte_count_range", "min_bytes": 4, "max_bytes": 4}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "🔥"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "💡"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 0)
            self.assertEqual(report["summary"]["unchanged_pass"], 1)

    def test_run_regression_supports_exact_ci_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "exact_ci", "value": "approved"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "APPROVED"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "rejected"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_not_exact_ci_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "not_exact_ci", "value": "forbidden"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Allowed"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "FORBIDDEN"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_not_exact_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "not_exact", "value": "Forbidden"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Allowed"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Forbidden"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_substring_ci_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "substring_ci",
                            "value": "error code",
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ERROR CODE: E42"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Status okay"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_not_substring_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "not_substring", "value": "secret"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "public summary only"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "contains secret token"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_not_substring_ci_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "not_substring_ci", "value": "secret"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "PUBLIC SUMMARY"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Contains SeCrEt token"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_starts_with_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "starts_with",
                            "value": "Order #",
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Order #1234 shipped"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Your Order #1234 shipped"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_rate"], 1.0)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_starts_with_ci_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "starts_with_ci",
                            "value": "order #",
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ORDER #1234 shipped"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Your ORDER #1234 shipped"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_not_starts_with_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "not_starts_with",
                            "value": "Error:",
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Success: order confirmed"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Error: missing token"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_not_starts_with_ci_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "not_starts_with_ci",
                            "value": "error:",
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "SUCCESS: order confirmed"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "ERROR: missing token"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_ends_with_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "ends_with",
                            "value": "resolved",
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Ticket resolved"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Ticket is pending"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_ends_with_ci_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "ends_with_ci",
                            "value": "resolved",
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Ticket RESOLVED"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Ticket is pending"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_not_ends_with_ci_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "not_ends_with_ci",
                            "value": "resolved",
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Ticket pending"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Ticket RESOLVED"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_contains_any_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "contains_any",
                            "values": ["reset", "password"],
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "reset link sent"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "contact support"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_equals_any_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "equals_any",
                            "values": ["Approved", "Pending"],
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Approved"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Rejected"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_equals_any_ci_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "equals_any_ci",
                            "values": ["approved", "pending"],
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "APPROVED"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Rejected"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_rejects_empty_equals_any_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "equals_any", "values": []}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Approved"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Approved"}])

            with self.assertRaisesRegex(ValueError, "type=equals_any"):
                run_regression(str(dataset), str(baseline), str(candidate))

    def test_run_regression_rejects_empty_equals_any_ci_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "equals_any_ci", "values": []}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Approved"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Approved"}])

            with self.assertRaisesRegex(ValueError, "type=equals_any_ci"):
                run_regression(str(dataset), str(baseline), str(candidate))

    def test_run_regression_supports_not_contains_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "not_contains",
                            "values": ["SSN", "credit card"],
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Your order is shipped."}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "SSN required to proceed."}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_contains_none_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "contains_none",
                            "values": ["SSN", "credit card"],
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Order confirmation sent."}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "SSN required."}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)

    def test_run_regression_supports_contains_none_ci_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "contains_none_ci",
                            "values": ["ssn", "credit card"],
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Order confirmation sent."}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Credit Card required."}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)

    def test_run_regression_supports_contains_all_ci_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "contains_all_ci",
                            "values": ["order", "resolved"],
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ORDER issue RESOLVED."}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "order status pending"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_contains_any_ci_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "contains_any_ci",
                            "values": ["approved", "pending"],
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "APPROVED"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "rejected"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)

    def test_run_regression_supports_not_contains_ci_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "not_contains_ci",
                            "values": ["ssn", "credit card"],
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Order confirmation sent."}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Credit Card required."}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)

    def test_run_regression_supports_regex_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "input": "Give me order status",
                        "expected": {
                            "type": "regex",
                            "pattern": "order\\s+#?\\d{4}",
                            "flags": ["IGNORECASE"],
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Order #1234 is shipped."}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "No order number provided."}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])
            self.assertEqual(report["summary"]["outcome_counts"]["regressed"], 1)
            self.assertEqual(report["cases"][0]["outcome"], "regressed")

    def test_run_regression_supports_regex_ci_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "regex_ci",
                            "pattern": "^approved$",
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "APPROVED"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "REJECTED"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_not_regex_ci_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "not_regex_ci",
                            "pattern": "(ssn|credit card)",
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Order confirmation sent."}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Credit Card required."}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_rejects_empty_substring_ci_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "substring_ci", "value": ""}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "ok"}])

            with self.assertRaisesRegex(ValueError, "type=substring_ci"):
                run_regression(str(dataset), str(baseline), str(candidate))

    def test_run_regression_rejects_empty_starts_with_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "starts_with", "value": ""}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "ok"}])

            with self.assertRaisesRegex(ValueError, "type=starts_with"):
                run_regression(str(dataset), str(baseline), str(candidate))

    def test_run_regression_rejects_empty_ends_with_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "ends_with", "value": ""}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "ok"}])

            with self.assertRaisesRegex(ValueError, "type=ends_with"):
                run_regression(str(dataset), str(baseline), str(candidate))

    def test_run_regression_rejects_empty_starts_with_ci_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "starts_with_ci", "value": ""}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "ok"}])

            with self.assertRaisesRegex(ValueError, "type=starts_with_ci"):
                run_regression(str(dataset), str(baseline), str(candidate))

    def test_run_regression_rejects_empty_ends_with_ci_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "ends_with_ci", "value": ""}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "ok"}])

            with self.assertRaisesRegex(ValueError, "type=ends_with_ci"):
                run_regression(str(dataset), str(baseline), str(candidate))

    def test_run_regression_rejects_empty_not_ends_with_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "not_ends_with", "value": ""}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "ok"}])

            with self.assertRaisesRegex(ValueError, "type=not_ends_with"):
                run_regression(str(dataset), str(baseline), str(candidate))

    def test_run_regression_rejects_empty_contains_any_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "contains_any", "values": []}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "ok"}])

            with self.assertRaisesRegex(ValueError, "type=contains_any"):
                run_regression(str(dataset), str(baseline), str(candidate))

    def test_run_regression_rejects_empty_not_contains_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "not_contains", "values": []}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "ok"}])

            with self.assertRaisesRegex(ValueError, "type=not_contains"):
                run_regression(str(dataset), str(baseline), str(candidate))

    def test_run_regression_supports_regex_fullmatch_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "regex_fullmatch",
                            "pattern": "Order #[0-9]{4}",
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Order #1234"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Order #1234 shipped"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_rejects_unknown_regex_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "regex",
                            "pattern": "ok",
                            "flags": ["CASE_INSENSITIVE"],
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "ok"}])

            with self.assertRaisesRegex(ValueError, "Unsupported regex flag"):
                run_regression(str(dataset), str(baseline), str(candidate))

    def test_run_regression_supports_case_insensitive_regex_flag_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "regex",
                            "pattern": "hello",
                            "flags": [" ignorecase "],
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "HELLO world"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "HELLO again"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 0)
            self.assertEqual(report["summary"]["candidate_passes"], 1)

    def test_run_regression_supports_not_regex_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "not_regex",
                            "pattern": "\\b(SSN|credit card)\\b",
                            "flags": ["IGNORECASE"],
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Order confirmation sent."}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Credit card required."}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_not_regex_fullmatch_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "not_regex_fullmatch",
                            "pattern": "(Approved|Pending)",
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Rejected"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "Approved"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_regex_fullmatch_ci_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "regex_fullmatch_ci",
                            "pattern": "status: (approved|pending)",
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "STATUS: APPROVED"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "STATUS: approved now"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_not_regex_fullmatch_ci_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "not_regex_fullmatch_ci",
                            "pattern": "(approved|pending)",
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "Rejected"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "APPROVED"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])


    def test_run_regression_summary_exposes_unchanged_buckets(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "substring", "value": "ok"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "bad"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "still bad"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["unchanged_pass"], 0)
            self.assertEqual(report["summary"]["unchanged_fail"], 1)
            self.assertEqual(report["summary"]["stability_rate"], 1.0)
            self.assertEqual(report["summary"]["unchanged_fail_rate"], 1.0)
            self.assertEqual(report["summary"]["unchanged_fail_ids"], ["case-1"])

    def test_run_regression_validates_regex_with_declared_flags(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "expected": {
                            "type": "regex",
                            "pattern": "^ok$",
                            "flags": ["MULTILINE"],
                        },
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "header\nok\nfooter"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "header\nnope\nfooter"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)

    def test_run_regression_rejects_missing_baseline_case_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "case-1", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "case-2", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ok"}])
            _write_jsonl(
                candidate,
                [
                    {"id": "case-1", "output": "ok"},
                    {"id": "case-2", "output": "ok"},
                ],
            )

            with self.assertRaisesRegex(ValueError, "Baseline is missing ids"):
                run_regression(str(dataset), str(baseline), str(candidate))

    def test_run_regression_rejects_unknown_candidate_case_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "substring", "value": "ok"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ok"}])
            _write_jsonl(
                candidate,
                [
                    {"id": "case-1", "output": "ok"},
                    {"id": "case-extra", "output": "ok"},
                ],
            )

            with self.assertRaisesRegex(ValueError, "Candidate has unknown ids"):
                run_regression(str(dataset), str(baseline), str(candidate))

    def test_run_regression_skips_disabled_cases_in_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "case-1", "expected": {"type": "substring", "value": "ok"}},
                    {
                        "id": "case-2",
                        "disabled": True,
                        "expected": {"type": "substring", "value": "ok"},
                    },
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "case-1", "output": "ok"},
                    {"id": "case-2", "output": "bad"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "case-1", "output": "ok"},
                    {"id": "case-2", "output": "still bad"},
                ],
            )

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["dataset_cases"], 2)
            self.assertEqual(report["summary"]["cases"], 1)
            self.assertEqual(report["summary"]["skipped_cases"], 1)
            self.assertEqual(report["summary"]["skipped_ids"], ["case-2"])

    def test_run_regression_fails_when_all_cases_are_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {
                        "id": "case-1",
                        "disabled": True,
                        "expected": {"type": "substring", "value": "ok"},
                    }
                ],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "ok"}])

            with self.assertRaisesRegex(ValueError, "No active dataset cases"):
                run_regression(str(dataset), str(baseline), str(candidate))

    def test_run_regression_filters_cases_by_include_exclude_regex(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "auth-1", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "billing-1", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "auth-2", "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "auth-1", "output": "ok"},
                    {"id": "billing-1", "output": "ok"},
                    {"id": "auth-2", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "auth-1", "output": "ok"},
                    {"id": "billing-1", "output": "bad"},
                    {"id": "auth-2", "output": "ok"},
                ],
            )

            report = run_regression(
                str(dataset),
                str(baseline),
                str(candidate),
                include_id_regex=r"^auth-",
                exclude_id_regex=r"-2$",
            )

            self.assertEqual(report["summary"]["dataset_cases"], 3)
            self.assertEqual(report["summary"]["selected_dataset_cases"], 1)
            self.assertEqual(report["summary"]["selected_dataset_ids"], ["auth-1"])
            self.assertEqual(report["summary"]["selection_rate"], 0.3333)
            self.assertEqual(report["summary"]["active_case_ids"], ["auth-1"])
            self.assertEqual(report["summary"]["cases"], 1)
            self.assertEqual(report["summary"]["filtered_out_cases"], 2)
            self.assertEqual(report["summary"]["filtered_out_rate"], 0.6667)
            self.assertEqual(report["summary"]["filtered_out_ids"], ["auth-2", "billing-1"])

    def test_run_regression_fails_when_id_filter_selects_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "substring", "value": "ok"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "ok"}])

            with self.assertRaisesRegex(ValueError, "selection is empty"):
                run_regression(
                    str(dataset),
                    str(baseline),
                    str(candidate),
                    include_id_regex=r"^auth-",
                )

    def test_run_regression_rejects_empty_dataset_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "   ", "expected": {"type": "substring", "value": "ok"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "ok"}])

            with self.assertRaisesRegex(ValueError, "Invalid empty id in dataset"):
                run_regression(str(dataset), str(baseline), str(candidate))

    def test_run_regression_rejects_empty_baseline_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "substring", "value": "ok"}}],
            )
            _write_jsonl(baseline, [{"id": "", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "ok"}])

            with self.assertRaisesRegex(ValueError, "Invalid empty id in baseline"):
                run_regression(str(dataset), str(baseline), str(candidate))

    def test_run_regression_rejects_empty_candidate_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "substring", "value": "ok"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "   ", "output": "ok"}])

            with self.assertRaisesRegex(ValueError, "Invalid empty id in candidate"):
                run_regression(str(dataset), str(baseline), str(candidate))


    def test_run_regression_sorts_summary_id_lists_for_reproducibility(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [
                    {"id": "z-case", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "a-case", "expected": {"type": "substring", "value": "ok"}},
                    {"id": "m-case", "disabled": True, "expected": {"type": "substring", "value": "ok"}},
                ],
            )
            _write_jsonl(
                baseline,
                [
                    {"id": "z-case", "output": "ok"},
                    {"id": "a-case", "output": "bad"},
                    {"id": "m-case", "output": "ok"},
                ],
            )
            _write_jsonl(
                candidate,
                [
                    {"id": "z-case", "output": "bad"},
                    {"id": "a-case", "output": "ok"},
                    {"id": "m-case", "output": "ok"},
                ],
            )

            report = run_regression(
                str(dataset),
                str(baseline),
                str(candidate),
                include_id_regex=r"^(z-case|a-case|m-case)$",
                exclude_id_regex=r"^a-case$",
            )

            self.assertEqual(report["summary"]["filtered_out_ids"], ["a-case"])
            self.assertEqual(report["summary"]["skipped_ids"], ["m-case"])
            self.assertEqual(report["summary"]["regression_ids"], ["z-case"])
            self.assertEqual(report["summary"]["improved_ids"], [])
            self.assertEqual(report["summary"]["unchanged_fail_ids"], [])

    def test_run_regression_sets_pass_rate_trend_to_improving(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "substring", "value": "ok"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "bad"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "ok"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))
            self.assertEqual(report["summary"]["pass_rate_trend"], "improving")
            self.assertEqual(report["summary"]["improvement_rate"], 1.0)

    def test_run_regression_sets_pass_rate_trend_to_regressing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "substring", "value": "ok"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "bad"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))
            self.assertEqual(report["summary"]["pass_rate_trend"], "regressing")


    def test_run_regression_supports_regex_flags_as_tab_delimited_string(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "regex", "pattern": "^alpha.+omega$", "flags": "ignorecase	dotall"}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ALPHA\nmid\nomega"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "omega\nmid\nalpha"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_rejects_whitespace_only_regex_flags_string(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "regex", "pattern": "alpha", "flags": "   \n\t  "}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "alpha"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "alpha"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 0)
            self.assertEqual(report["summary"]["unchanged_pass"], 1)


if __name__ == "__main__":
    unittest.main()


    def test_run_regression_supports_word_count_range_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "word_count_range", "min_words": 3, "max_words": 5}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "one two three four"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "one two"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_allows_word_count_range_with_single_bound(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "word_count_range", "max_words": 4}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "one two three"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "one two three four five"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_rejects_invalid_word_count_range_bounds(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "word_count_range", "min_words": 5, "max_words": 2}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "one two three"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "one two three"}])

            with self.assertRaisesRegex(ValueError, "min_words must be <= max_words"):
                run_regression(str(dataset), str(baseline), str(candidate))

    def test_run_regression_word_count_range_example_fixture_surfaces_expected_regression_id(self) -> None:
        root = Path(__file__).resolve().parents[1]
        report = run_regression(
            str(root / "examples" / "dataset" / "word_count_range_release_notes.jsonl"),
            str(root / "examples" / "outputs" / "word_count_range_release_notes.baseline.jsonl"),
            str(root / "examples" / "outputs" / "word_count_range_release_notes.candidate.jsonl"),
        )

        self.assertEqual(report["summary"]["regressions"], 1)
        self.assertEqual(report["summary"]["regression_ids"], ["release-note-short"])
        self.assertEqual(report["summary"]["unchanged_pass"], 1)

    def test_run_regression_supports_line_count_range_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "line_count_range", "min_lines": 2, "max_lines": 3}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "alpha\nbeta"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "alpha beta gamma"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_line_count_range_with_crlf_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "line_count_range", "min_lines": 2, "max_lines": 2}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "alpha\r\nbeta"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "alpha\r\nbeta"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 0)
            self.assertEqual(report["summary"]["unchanged_pass"], 1)

    def test_run_regression_supports_paragraph_count_range_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "paragraph_count_range", "min_paragraphs": 2, "max_paragraphs": 3}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "alpha\n\nbeta"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "alpha\n\nbeta\n\ngamma\n\ndelta"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_rejects_invalid_paragraph_count_range_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "case-1", "expected": {"type": "paragraph_count_range"}}])
            _write_jsonl(baseline, [{"id": "case-1", "output": "alpha"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "alpha"}])

            with self.assertRaises(ValueError) as exc:
                run_regression(str(dataset), str(baseline), str(candidate))

            self.assertIn("Invalid paragraph_count_range expectation", str(exc.exception))

    def test_run_regression_supports_byte_count_range_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "byte_count_range", "min_bytes": 6, "max_bytes": 8}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "테스트"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "테스트메시지"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_char_count_range_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "char_count_range", "min_chars": 5, "max_chars": 12}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "welcome"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "too long for gate"}])

            report = run_regression(dataset, baseline, candidate)

            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_supports_char_count_range_with_min_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "char_count_range", "min_chars": 10}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "short"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "just enough"}])

            report = run_regression(dataset, baseline, candidate)

            self.assertEqual(report["summary"]["improved_ids"], ["case-1"])

    def test_run_regression_supports_char_count_range_with_max_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "char_count_range", "max_chars": 12}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "fits"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "this output is too long"}])

            report = run_regression(dataset, baseline, candidate)

            self.assertEqual(report["summary"]["regression_ids"], ["case-1"])

    def test_run_regression_rejects_invalid_char_count_range_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "case-1", "expected": {"type": "char_count_range"}}])
            _write_jsonl(baseline, [{"id": "case-1", "output": "ok"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "ok"}])

            with self.assertRaises(ValueError) as exc:
                run_regression(dataset, baseline, candidate)

            self.assertIn("Invalid char_count_range expectation", str(exc.exception))

    def test_run_regression_rejects_invalid_line_count_range_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "case-1", "expected": {"type": "line_count_range"}}])
            _write_jsonl(baseline, [{"id": "case-1", "output": "alpha\nbeta"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "alpha\nbeta"}])

            with self.assertRaises(ValueError) as exc:
                run_regression(str(dataset), str(baseline), str(candidate))

            self.assertIn("Invalid line_count_range expectation", str(exc.exception))

    def test_run_regression_rejects_negative_char_count_range_bound(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "char_count_range", "min_chars": -1}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "hello"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "hello"}])

            with self.assertRaises(ValueError) as exc:
                run_regression(str(dataset), str(baseline), str(candidate))

            self.assertIn("Invalid expected.min_chars", str(exc.exception))

    def test_run_regression_rejects_reversed_char_count_range_bounds(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "char_count_range", "min_chars": 12, "max_chars": 5}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "hello"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "hello"}])

            with self.assertRaises(ValueError) as exc:
                run_regression(str(dataset), str(baseline), str(candidate))

            self.assertIn("min_chars must be <= max_chars", str(exc.exception))


    def test_sentence_count_range_treats_unicode_ellipsis_as_sentence_boundary(self) -> None:
        summary = run_regression(
            dataset_path=self._write_jsonl(
                "dataset.jsonl",
                [
                    {
                        "id": "unicode-ellipsis",
                        "expected": {"type": "sentence_count_range", "min_sentences": 2, "max_sentences": 2},
                    }
                ],
            ),
            baseline_path=self._write_jsonl("baseline.jsonl", [{"id": "unicode-ellipsis", "output": "Alpha… Beta!"}]),
            candidate_path=self._write_jsonl("candidate.jsonl", [{"id": "unicode-ellipsis", "output": "Alpha… Beta!"}]),
        )

        self.assertEqual(summary["baseline_passes"], 1)
        self.assertEqual(summary["candidate_passes"], 1)
        self.assertEqual(summary["unchanged_pass_ids"], ["unicode-ellipsis"])


    def test_run_regression_allows_char_count_range_with_single_bound(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "case-1", "expected": {"type": "char_count_range", "max_chars": 6}}])
            _write_jsonl(baseline, [{"id": "case-1", "output": "launch"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "tool"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 0)
            self.assertEqual(report["summary"]["unchanged_pass"], 1)

    def test_run_regression_rejects_invalid_byte_count_range_bounds(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(dataset, [{"id": "case-1", "expected": {"type": "byte_count_range", "min_bytes": 8, "max_bytes": 3}}])
            _write_jsonl(baseline, [{"id": "case-1", "output": "launch"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "tool"}])

            with self.assertRaises(ValueError) as exc:
                run_regression(str(dataset), str(baseline), str(candidate))

            self.assertIn("Invalid byte_count_range expectation", str(exc.exception))

    def test_run_regression_supports_regex_flags_as_semicolon_delimited_string(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            dataset = tmp_path / "dataset.jsonl"
            baseline = tmp_path / "baseline.jsonl"
            candidate = tmp_path / "candidate.jsonl"

            _write_jsonl(
                dataset,
                [{"id": "case-1", "expected": {"type": "regex", "pattern": "^alpha.+omega$", "flags": " ignorecase ; dotall "}}],
            )
            _write_jsonl(baseline, [{"id": "case-1", "output": "ALPHA\nmid\nomega"}])
            _write_jsonl(candidate, [{"id": "case-1", "output": "beta\nmid\nomega"}])

            report = run_regression(str(dataset), str(baseline), str(candidate))

            self.assertEqual(report["summary"]["regressions"], 1)
