import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryRepo45ReportRefAliasNoteTests(unittest.TestCase):
    def test_readme_mentions_repo45_report_ref_alias_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/CLI_SUMMARY_REPO45_REPORT_REF_ALIAS_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_REPO45_REPORT_REF_ALIAS_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
