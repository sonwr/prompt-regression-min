from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryFiveRepoHoldReasonStatusNoteTests(unittest.TestCase):
    def test_readme_mentions_hold_reason_status_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/CLI_SUMMARY_FIVE_REPO_HOLD_REASON_STATUS_NOTE.md", readme)

    def test_note_mentions_validation_and_hold_reason(self) -> None:
        note = (ROOT / "docs" / "CLI_SUMMARY_FIVE_REPO_HOLD_REASON_STATUS_NOTE.md").read_text(encoding="utf-8")
        self.assertIn("validation result", note)
        self.assertIn("hold reason", note)


if __name__ == "__main__":
    unittest.main()
