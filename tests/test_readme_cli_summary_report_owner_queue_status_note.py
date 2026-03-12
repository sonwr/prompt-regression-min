from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryReportOwnerQueueStatusNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_report_owner_queue_status_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_REPORT_OWNER_QUEUE_STATUS_NOTE.md", readme)
        self.assertTrue((ROOT / "docs/CLI_SUMMARY_REPORT_OWNER_QUEUE_STATUS_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
