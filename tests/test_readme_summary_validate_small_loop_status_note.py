from __future__ import annotations

from pathlib import Path
import unittest


class ReadmeSummaryValidateSmallLoopStatusNoteTests(unittest.TestCase):
    def test_readme_mentions_summary_validate_small_loop_status_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_VALIDATE_SMALL_LOOP_STATUS_NOTE.md", readme)
        self.assertTrue((root / "docs" / "CLI_SUMMARY_VALIDATE_SMALL_LOOP_STATUS_NOTE.md").exists())
