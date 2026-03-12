from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryQuietTitleSplitNoteTest(unittest.TestCase):
    def test_readme_mentions_quiet_title_split_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/CLI_SUMMARY_QUIET_TITLE_SPLIT_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_QUIET_TITLE_SPLIT_NOTE.md").exists())

    def test_note_mentions_quiet_and_both_titles(self) -> None:
        note = (ROOT / "docs" / "CLI_SUMMARY_QUIET_TITLE_SPLIT_NOTE.md").read_text(encoding="utf-8")
        self.assertIn("--quiet", note)
        self.assertIn("--summary-markdown-title", note)
        self.assertIn("--summary-pr-comment-title", note)


if __name__ == "__main__":
    unittest.main()
