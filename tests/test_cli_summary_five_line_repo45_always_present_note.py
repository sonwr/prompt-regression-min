from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CliSummaryFiveLineRepo45AlwaysPresentNoteTests(unittest.TestCase):
    def test_readme_mentions_repo45_always_present_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/CLI_SUMMARY_FIVE_LINE_REPO45_ALWAYS_PRESENT_NOTE.md", readme)

    def test_note_mentions_exactly_five_lines_and_repo45_presence(self) -> None:
        note = (ROOT / "docs" / "CLI_SUMMARY_FIVE_LINE_REPO45_ALWAYS_PRESENT_NOTE.md").read_text(encoding="utf-8")
        self.assertIn("exactly five lines", note)
        self.assertIn("Repo 4 and repo 5 should always be present", note)

if __name__ == "__main__":
    unittest.main()
