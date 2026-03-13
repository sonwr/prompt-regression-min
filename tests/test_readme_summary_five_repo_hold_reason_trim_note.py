from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeSummaryFiveRepoHoldReasonTrimNoteTests(unittest.TestCase):
    def test_readme_mentions_summary_five_repo_hold_reason_trim_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_FIVE_REPO_HOLD_REASON_TRIM_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_FIVE_REPO_HOLD_REASON_TRIM_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
