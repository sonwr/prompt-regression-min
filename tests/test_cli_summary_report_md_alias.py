from __future__ import annotations

import unittest

from prompt_regression_min.cli import _build_parser


class SummaryReportMarkdownAliasTests(unittest.TestCase):
    def test_summary_report_md_alias_maps_to_summary_markdown(self) -> None:
        parser = _build_parser()
        args = parser.parse_args([
            "run",
            "-d",
            "dataset.jsonl",
            "-b",
            "baseline.jsonl",
            "-c",
            "candidate.jsonl",
            "--summary-report-md",
            "summary.md",
        ])

        self.assertEqual(args.summary_markdown, "summary.md")


if __name__ == "__main__":
    unittest.main()
