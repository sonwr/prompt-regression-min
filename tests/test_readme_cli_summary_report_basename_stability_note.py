import unittest
from pathlib import Path


class ReadmeCliSummaryReportBasenameStabilityNoteTests(unittest.TestCase):
    def test_readme_mentions_report_basename_stability_note(self) -> None:
        text = Path('README.md').read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_REPORT_BASENAME_STABILITY_NOTE.md', text)


if __name__ == '__main__':
    unittest.main()
