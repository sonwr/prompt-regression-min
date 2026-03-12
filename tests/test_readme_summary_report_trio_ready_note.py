from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
NOTE = ROOT / "docs" / "CLI_SUMMARY_REPORT_TRIO_READY_NOTE.md"


class SummaryReportTrioReadyNoteTests(unittest.TestCase):
    def test_readme_mentions_summary_report_trio_ready_note(self) -> None:
        readme = README.read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_REPORT_TRIO_READY_NOTE.md", readme)
        self.assertTrue(NOTE.exists())

    def test_note_keeps_json_markdown_html_bundle_visible(self) -> None:
        note = NOTE.read_text(encoding="utf-8")

        self.assertIn("JSON", note)
        self.assertIn("Markdown", note)
        self.assertIn("HTML", note)
        self.assertIn("stable basename", note)


if __name__ == "__main__":
    unittest.main()
