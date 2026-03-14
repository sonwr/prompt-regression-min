from __future__ import annotations

import unittest

from prompt_regression_min.cli import _build_parser


class SummaryOwnerMarkdownAliasTest(unittest.TestCase):
    def test_summary_owner_md_alias_targets_summary_markdown(self) -> None:
        parser = _build_parser()
        args = parser.parse_args([
            "run", "-d", "dataset.jsonl", "-b", "baseline.jsonl", "-c", "candidate.jsonl",
            "--summary-owner-md", "owner.md",
        ])
        self.assertEqual(args.summary_markdown, "owner.md")


if __name__ == "__main__":
    unittest.main()
