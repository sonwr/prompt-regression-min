from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryReportTrioStartTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_report_trio_start(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_REPORT_TRIO_START.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_REPORT_TRIO_START.md").exists())


if __name__ == "__main__":
    unittest.main()
