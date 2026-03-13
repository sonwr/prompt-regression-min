from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryRepo45PhaseOneStatusNoteTests(unittest.TestCase):
    def test_readme_mentions_repo45_phase_one_status_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        note = (ROOT / "docs" / "CLI_SUMMARY_REPO45_PHASE_ONE_STATUS_NOTE.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_REPO45_PHASE_ONE_STATUS_NOTE.md", readme)
        self.assertIn("repo 4 stays active", note)
        self.assertIn("repo 5 stays scenario-file/report-first", note)
        self.assertIn("commit/push claims still wait", note)


if __name__ == "__main__":
    unittest.main()
