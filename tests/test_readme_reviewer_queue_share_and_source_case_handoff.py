from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReviewerQueueShareAndSourceCaseHandoffTests(unittest.TestCase):
    def test_readme_mentions_share_and_source_case_handoff(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_share_and_source_case_handoff.md", readme)
        self.assertTrue((ROOT / "examples" / "reviewer_queue_share_and_source_case_handoff.md").exists())


if __name__ == "__main__":
    unittest.main()
