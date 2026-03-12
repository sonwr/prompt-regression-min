from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / 'docs' / 'CLI_SUMMARY_REPORT_BASENAME_STATUS_NOTE.md'


class ReadmeSummaryReportBasenameStatusNoteTests(unittest.TestCase):
    def test_readme_mentions_summary_report_basename_status_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_REPORT_BASENAME_STATUS_NOTE.md', readme)
        self.assertTrue(NOTE.exists())
