from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryOneLineReviewStatusNoteTest(unittest.TestCase):
    def test_note_exists_with_one_line_review_cues(self) -> None:
        note = (ROOT / "docs" / "CLI_SUMMARY_ONE_LINE_REVIEW_STATUS_NOTE.md").read_text(encoding="utf-8")
        self.assertIn("one honest review line", note)
        self.assertIn("validation state", note)
        self.assertIn("saved artifact bundle status", note)


if __name__ == "__main__":
    unittest.main()
