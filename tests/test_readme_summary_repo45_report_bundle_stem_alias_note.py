from pathlib import Path
import unittest


class ReadmeSummaryRepo45ReportBundleStemAliasNoteTests(unittest.TestCase):
    def test_readme_mentions_repo45_report_bundle_stem_alias_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/CLI_SUMMARY_REPO45_REPORT_BUNDLE_STEM_ALIAS_NOTE.md", readme)
        note = (root / "docs" / "CLI_SUMMARY_REPO45_REPORT_BUNDLE_STEM_ALIAS_NOTE.md").read_text(encoding="utf-8")
        self.assertIn("report_bundle_stem", note)
        self.assertIn("validation status", note)


if __name__ == "__main__":
    unittest.main()
