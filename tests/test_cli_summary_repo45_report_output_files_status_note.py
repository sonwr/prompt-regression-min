from pathlib import Path
import unittest


class CliSummaryRepo45ReportOutputFilesStatusNoteTest(unittest.TestCase):
    def test_readme_mentions_output_files_status_note(self) -> None:
        readme = Path("README.md").read_text(encoding="utf-8")
        self.assertIn(
            "docs/CLI_SUMMARY_REPO45_REPORT_OUTPUT_FILES_STATUS_NOTE.md",
            readme,
        )

    def test_note_exists_and_mentions_report_output_files(self) -> None:
        note = Path("docs/CLI_SUMMARY_REPO45_REPORT_OUTPUT_FILES_STATUS_NOTE.md")
        self.assertTrue(note.exists())
        content = note.read_text(encoding="utf-8")
        self.assertIn("report.outputs.files", content)
        self.assertIn("repo 4", content)
        self.assertIn("repo 5", content)


if __name__ == "__main__":
    unittest.main()
