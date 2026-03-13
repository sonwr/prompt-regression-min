from pathlib import Path
import unittest


class ReadmeCliSummaryRepo45PhaseOneReportPairStatusNoteTests(unittest.TestCase):
    def test_readme_mentions_repo45_phase_one_report_pair_status_note(self) -> None:
        readme = Path('README.md').read_text(encoding='utf-8')

        self.assertIn('docs/CLI_SUMMARY_REPO45_PHASE_ONE_REPORT_PAIR_STATUS_NOTE.md', readme)

    def test_repo45_phase_one_report_pair_status_note_mentions_repo4_repo5_and_hold_rule(self) -> None:
        doc = Path('docs/CLI_SUMMARY_REPO45_PHASE_ONE_REPORT_PAIR_STATUS_NOTE.md').read_text(encoding='utf-8')

        self.assertIn('oss-launchpad-cli', doc)
        self.assertIn('governance-sandbox', doc)
        self.assertIn('markdown/html report generation', doc)
        self.assertIn('hold commit/push', doc)


if __name__ == '__main__':
    unittest.main()
