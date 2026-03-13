from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryRepo45ReportFileAliasNoteTests(unittest.TestCase):
    def test_readme_mentions_repo45_report_file_alias_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        note = (ROOT / 'docs' / 'CLI_SUMMARY_REPO45_REPORT_FILE_ALIAS_NOTE.md').read_text(encoding='utf-8')

        self.assertIn('docs/CLI_SUMMARY_REPO45_REPORT_FILE_ALIAS_NOTE.md', readme)
        self.assertIn('repo 4', note)
        self.assertIn('repo 5', note)
        self.assertIn('report-file alias', note)


if __name__ == '__main__':
    unittest.main()
