from __future__ import annotations

from pathlib import Path
import unittest


class ReadmeReviewerQueueTitleAndBasenameHandoffTests(unittest.TestCase):
    def test_readme_mentions_reviewer_queue_title_and_basename_handoff(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_title_and_basename_handoff.md", readme)
        self.assertTrue((root / "examples" / "reviewer_queue_title_and_basename_handoff.md").exists())


if __name__ == "__main__":
    unittest.main()
