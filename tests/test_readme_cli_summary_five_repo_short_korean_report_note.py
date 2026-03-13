import unittest
from pathlib import Path


class ReadmeFiveRepoShortKoreanReportNoteTest(unittest.TestCase):
    def test_readme_mentions_cli_summary_five_repo_short_korean_report_note(self) -> None:
        readme = Path('README.md').read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_FIVE_REPO_SHORT_KOREAN_REPORT_NOTE.md', readme)


if __name__ == '__main__':
    unittest.main()
