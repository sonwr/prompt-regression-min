from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryRepo45ScenarioJournalReportNoteTests(unittest.TestCase):
    def test_readme_mentions_repo45_scenario_journal_report_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_REPO45_SCENARIO_JOURNAL_REPORT_NOTE.md', readme)
        self.assertTrue((ROOT / 'docs' / 'CLI_SUMMARY_REPO45_SCENARIO_JOURNAL_REPORT_NOTE.md').exists())


if __name__ == '__main__':
    unittest.main()
