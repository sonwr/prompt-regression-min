from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryFiveRepoKoreanShortLineNoteTest(unittest.TestCase):
    def test_readme_mentions_korean_short_line_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/CLI_SUMMARY_FIVE_REPO_KOREAN_SHORT_LINE_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_FIVE_REPO_KOREAN_SHORT_LINE_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
