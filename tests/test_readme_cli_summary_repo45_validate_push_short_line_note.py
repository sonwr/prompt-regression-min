from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryRepo45ValidatePushShortLineNoteTests(unittest.TestCase):
    def test_readme_mentions_repo45_validate_push_short_line_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/CLI_SUMMARY_REPO45_VALIDATE_PUSH_SHORT_LINE_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_REPO45_VALIDATE_PUSH_SHORT_LINE_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
