from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryFiveRepoCommitHoldShortReasonNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_five_repo_commit_hold_short_reason_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_FIVE_REPO_COMMIT_HOLD_SHORT_REASON_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_FIVE_REPO_COMMIT_HOLD_SHORT_REASON_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
