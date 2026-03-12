from pathlib import Path
import unittest


class CliSummaryTitleSplitNoteTest(unittest.TestCase):
    def test_note_exists_with_dual_title_guidance(self) -> None:
        note = Path("docs/CLI_SUMMARY_TITLE_SPLIT_NOTE.md")
        self.assertTrue(note.exists())
        text = note.read_text(encoding="utf-8")
        self.assertIn("markdown and PR-comment titles", text)
        self.assertIn("reviewer-facing handoff", text)


if __name__ == "__main__":
    unittest.main()
