from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SummaryValidatedFiveRepoOneLineNoteTests(unittest.TestCase):
    def test_readme_mentions_summary_validated_five_repo_one_line_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_VALIDATED_FIVE_REPO_ONE_LINE_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_VALIDATED_FIVE_REPO_ONE_LINE_NOTE.md").exists())
