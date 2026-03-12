import unittest
from pathlib import Path


class ReadmeCliSummaryReportStatusPathBadgeNoteTests(unittest.TestCase):
    def test_readme_mentions_status_path_badge_note(self) -> None:
        readme = Path(__file__).resolve().parents[1] / 'README.md'
        text = readme.read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_REPORT_STATUS_PATH_BADGE_NOTE.md', text)


if __name__ == '__main__':
    unittest.main()
