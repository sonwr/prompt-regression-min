from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeFiveRepoExactFiveLineNoteTests(unittest.TestCase):
    def test_readme_mentions_five_repo_exact_five_line_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_FIVE_REPO_EXACT_FIVE_LINE_NOTE.md", readme)
        self.assertIn("exactly five lines", readme)


if __name__ == "__main__":
    unittest.main()
