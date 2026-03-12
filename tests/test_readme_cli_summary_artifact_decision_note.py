from pathlib import Path
import unittest


class ReadmeCliSummaryArtifactDecisionNoteTest(unittest.TestCase):
    def test_note_mentions_shared_summary_bundle(self) -> None:
        note = Path("docs/CLI_SUMMARY_ARTIFACT_DECISION_NOTE.md")
        self.assertTrue(note.exists())
        text = note.read_text(encoding="utf-8")
        self.assertIn("json", text.lower())
        self.assertIn("markdown", text.lower())
        self.assertIn("html", text.lower())


if __name__ == "__main__":
    unittest.main()
