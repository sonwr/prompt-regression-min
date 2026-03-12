from __future__ import annotations

from pathlib import Path
import unittest


class ReadmeSummaryReportStatusOwnerQueuePathNoteTests(unittest.TestCase):
    def test_readme_keeps_summary_report_status_owner_queue_path_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / 'README.md').read_text(encoding='utf-8')

        self.assertIn('docs/CLI_SUMMARY_REPORT_STATUS_OWNER_QUEUE_PATH_NOTE.md', readme)
        self.assertTrue((root / 'docs' / 'CLI_SUMMARY_REPORT_STATUS_OWNER_QUEUE_PATH_NOTE.md').exists())


if __name__ == '__main__':
    unittest.main()
