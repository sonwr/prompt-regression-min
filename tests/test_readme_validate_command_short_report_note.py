from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeValidateCommandShortReportNoteTests(unittest.TestCase):
    def test_readme_mentions_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        note = ROOT / "docs" / "CLI_SUMMARY_VALIDATE_COMMAND_SHORT_REPORT_NOTE.md"

        self.assertIn("docs/CLI_SUMMARY_VALIDATE_COMMAND_SHORT_REPORT_NOTE.md", readme)
        self.assertTrue(note.exists())


if __name__ == "__main__":
    unittest.main()
