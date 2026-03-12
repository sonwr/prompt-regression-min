from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReviewerQueuePriorityLadderTests(unittest.TestCase):
    def test_readme_links_reviewer_queue_priority_ladder(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        note = ROOT / "docs" / "REVIEWER_QUEUE_PRIORITY_LADDER.md"

        self.assertTrue(note.exists())
        self.assertIn("docs/REVIEWER_QUEUE_PRIORITY_LADDER.md", readme)
        self.assertIn("fix_regressions", note.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
