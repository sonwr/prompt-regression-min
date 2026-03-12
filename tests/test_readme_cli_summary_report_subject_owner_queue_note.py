from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryReportSubjectOwnerQueueNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_report_subject_owner_queue_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/CLI_SUMMARY_REPORT_SUBJECT_OWNER_QUEUE_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_REPORT_SUBJECT_OWNER_QUEUE_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
