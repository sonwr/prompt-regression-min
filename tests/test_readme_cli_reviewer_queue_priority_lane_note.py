from __future__ import annotations

from pathlib import Path
import unittest


class ReadmeCliReviewerQueuePriorityLaneNoteTests(unittest.TestCase):
    def test_readme_keeps_reviewer_queue_priority_lane_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_REVIEWER_QUEUE_PRIORITY_LANE_NOTE.md", readme)
        self.assertTrue((root / "docs" / "CLI_REVIEWER_QUEUE_PRIORITY_LANE_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
