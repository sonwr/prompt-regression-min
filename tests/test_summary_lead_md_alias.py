from __future__ import annotations

import unittest

from prompt_regression_min.cli import _build_parser


class SummaryLeadMarkdownAliasTest(unittest.TestCase):
    def test_summary_lead_md_alias_targets_summary_markdown(self) -> None:
        parser = _build_parser()
        args = parser.parse_args([
            "run", "-d", "dataset.jsonl", "-b", "baseline.jsonl", "-c", "candidate.jsonl",
            "--summary-lead-md", "lead.md",
        ])
        self.assertEqual(args.summary_markdown, "lead.md")


if __name__ == "__main__":
    unittest.main()
