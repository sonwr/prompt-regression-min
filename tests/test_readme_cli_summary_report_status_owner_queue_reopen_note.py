import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")


class ReadmeCliSummaryReportStatusOwnerQueueReopenNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_report_status_owner_queue_reopen_note(self) -> None:
        self.assertIn("docs/CLI_SUMMARY_REPORT_STATUS_OWNER_QUEUE_REOPEN_NOTE.md", README)


if __name__ == "__main__":
    unittest.main()
