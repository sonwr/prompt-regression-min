from __future__ import annotations

import unittest

from prompt_regression_min.cli import _build_parser


class SummaryReleaseMarkdownAliasTest(unittest.TestCase):
    def test_summary_release_md_alias_targets_summary_markdown(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(
            [
                "run",
                "-d",
                "dataset.jsonl",
                "-b",
                "baseline.jsonl",
                "-c",
                "candidate.jsonl",
                "--summary-release-md",
                "release.md",
            ]
        )
        self.assertEqual(args.summary_markdown, "release.md")


if __name__ == "__main__":
    unittest.main()
