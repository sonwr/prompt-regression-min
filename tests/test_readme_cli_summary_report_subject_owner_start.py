from pathlib import Path
import unittest


class ReadmeCliSummaryReportSubjectOwnerStartTest(unittest.TestCase):
    def test_readme_mentions_subject_owner_start_note(self) -> None:
        readme = Path('README.md').read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_REPORT_SUBJECT_OWNER_START.md', readme)


if __name__ == '__main__':
    unittest.main()
