from __future__ import annotations

import unittest
from pathlib import Path


class ReadmeCliSummaryReportOutputSlugTrioNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_report_output_slug_trio_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_REPORT_OUTPUT_SLUG_TRIO_NOTE.md", readme)
        self.assertTrue((root / "docs" / "CLI_SUMMARY_REPORT_OUTPUT_SLUG_TRIO_NOTE.md").exists())
