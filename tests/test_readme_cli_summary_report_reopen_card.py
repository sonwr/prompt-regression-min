from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryReportReopenCardTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_report_reopen_card(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_REPORT_REOPEN_CARD.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_REPORT_REOPEN_CARD.md").exists())


if __name__ == "__main__":
    unittest.main()
