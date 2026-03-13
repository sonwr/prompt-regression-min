from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryDownloadNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_download_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_DOWNLOAD_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_DOWNLOAD_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
