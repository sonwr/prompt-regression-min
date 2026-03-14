from pathlib import Path
import unittest


class ReadmeCliSummaryRepo45StdinReportBundleNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_repo45_stdin_report_bundle_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")
        note = (root / "docs" / "CLI_SUMMARY_REPO45_STDIN_REPORT_BUNDLE_NOTE.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_REPO45_STDIN_REPORT_BUNDLE_NOTE.md", readme)
        self.assertIn("stdin-fed YAML/JSON scenario replay", note)
        self.assertIn("markdown/html/json report bundle", note)
        self.assertIn("five-line report", note)


if __name__ == "__main__":
    unittest.main()
