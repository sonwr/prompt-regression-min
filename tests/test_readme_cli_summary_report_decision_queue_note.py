from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryReportDecisionQueueNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_report_decision_queue_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')

        self.assertIn('docs/CLI_SUMMARY_REPORT_DECISION_QUEUE_NOTE.md', readme)
        self.assertTrue((ROOT / 'docs' / 'CLI_SUMMARY_REPORT_DECISION_QUEUE_NOTE.md').exists())


if __name__ == '__main__':
    unittest.main()
