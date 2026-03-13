from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryReportReviewLoopNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_report_review_loop_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_REPORT_REVIEW_LOOP_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_REPORT_REVIEW_LOOP_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
