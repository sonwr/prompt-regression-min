from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReviewerQueueSmallSliceNoteTests(unittest.TestCase):
    def test_readme_mentions_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/CLI_REVIEWER_QUEUE_SMALL_SLICE_NOTE.md", readme)

    def test_note_mentions_rerun_backed_queue_slice(self) -> None:
        note = (ROOT / "docs" / "CLI_REVIEWER_QUEUE_SMALL_SLICE_NOTE.md").read_text(encoding="utf-8")
        self.assertIn("rerun-backed reviewer-queue slice", note)
        self.assertIn("saved summary", note)


if __name__ == "__main__":
    unittest.main()
