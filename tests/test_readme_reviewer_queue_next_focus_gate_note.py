from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReviewerQueueNextFocusGateNoteTests(unittest.TestCase):
    def test_readme_mentions_next_focus_gate_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_next_focus_gate_note.md", readme)
        self.assertTrue((ROOT / "examples" / "reviewer_queue_next_focus_gate_note.md").exists())


if __name__ == "__main__":
    unittest.main()
