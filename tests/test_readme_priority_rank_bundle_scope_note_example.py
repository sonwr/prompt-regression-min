from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmePriorityRankBundleScopeNoteExampleTests(unittest.TestCase):
    def test_readme_mentions_priority_rank_bundle_scope_note_example(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_priority_rank_bundle_scope_note.md", readme)
        self.assertTrue((ROOT / "examples" / "reviewer_queue_priority_rank_bundle_scope_note.md").exists())


if __name__ == "__main__":
    unittest.main()
