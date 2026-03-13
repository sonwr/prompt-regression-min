import unittest
from pathlib import Path


class ReadmeCliSummaryValidateBundleStatusLineNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_validate_bundle_status_line_note(self) -> None:
        readme = Path("README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_VALIDATE_BUNDLE_STATUS_LINE_NOTE.md", readme)


if __name__ == "__main__":
    unittest.main()
