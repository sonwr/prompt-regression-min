from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeFilteredScopeBudgetNoteTests(unittest.TestCase):
    def test_readme_mentions_filtered_scope_budget_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_filtered_scope_budget_note.md", readme)
        self.assertTrue((ROOT / "examples" / "reviewer_queue_filtered_scope_budget_note.md").exists())


if __name__ == "__main__":
    unittest.main()
