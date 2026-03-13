import unittest
from pathlib import Path


class ReadmeFiveRepoNoPushHoldLineNoteTests(unittest.TestCase):
    def test_readme_mentions_five_repo_no_push_hold_line_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        text = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_FIVE_REPO_NO_PUSH_HOLD_LINE_NOTE.md", text)
        self.assertTrue((root / "docs" / "CLI_SUMMARY_FIVE_REPO_NO_PUSH_HOLD_LINE_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
