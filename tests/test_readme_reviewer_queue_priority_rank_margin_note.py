from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
EXAMPLE = ROOT / "examples" / "reviewer_queue_priority_rank_margin_note.md"


class ReviewerQueuePriorityRankMarginNoteReadmeTests(unittest.TestCase):
    def test_readme_mentions_priority_rank_margin_note_example(self) -> None:
        readme = README.read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_priority_rank_margin_note.md", readme)
        self.assertTrue(EXAMPLE.exists())

    def test_priority_rank_margin_note_keeps_gap_language_compact(self) -> None:
        note = EXAMPLE.read_text(encoding="utf-8")

        self.assertIn("runner-up queue", note)
        self.assertIn("case-count gap", note)
        self.assertIn("queue-share gap", note)


if __name__ == "__main__":
    unittest.main()
