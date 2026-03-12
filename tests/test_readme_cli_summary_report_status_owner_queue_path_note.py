import unittest
from pathlib import Path


class ReadmeCliSummaryReportStatusOwnerQueuePathNoteTests(unittest.TestCase):
    def test_readme_mentions_status_owner_queue_path_note(self) -> None:
        readme = Path(__file__).resolve().parents[1] / 'README.md'
        text = readme.read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_REPORT_STATUS_OWNER_QUEUE_PATH_NOTE.md', text)


if __name__ == '__main__':
    unittest.main()
