from pathlib import Path
import unittest


class CliSummaryRepo45ScenarioReportPairStatusNoteTests(unittest.TestCase):
    def test_readme_mentions_repo45_scenario_report_pair_status_note(self) -> None:
        repo = Path(__file__).resolve().parents[1]
        readme = (repo / 'README.md').read_text(encoding='utf-8')

        self.assertIn('docs/CLI_SUMMARY_REPO45_SCENARIO_REPORT_PAIR_STATUS_NOTE.md', readme)
        self.assertTrue((repo / 'docs' / 'CLI_SUMMARY_REPO45_SCENARIO_REPORT_PAIR_STATUS_NOTE.md').exists())
