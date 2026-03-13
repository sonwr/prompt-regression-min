from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
DOC = ROOT / "docs" / "CLI_SUMMARY_REPO45_REPORT_DOWNLOADS_ALIAS_NOTE.md"


class CliSummaryRepo45ReportDownloadsAliasNoteTests(unittest.TestCase):
    def test_readme_mentions_report_downloads_alias_note(self) -> None:
        text = README.read_text(encoding="utf-8")
        self.assertIn("docs/CLI_SUMMARY_REPO45_REPORT_DOWNLOADS_ALIAS_NOTE.md", text)

    def test_note_mentions_report_downloads_aliases(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("report.outputs.downloads", text)
        self.assertIn("report_downloads", text)


if __name__ == "__main__":
    unittest.main()
