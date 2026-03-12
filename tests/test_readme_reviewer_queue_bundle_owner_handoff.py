from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReviewerQueueBundleOwnerHandoffTests(unittest.TestCase):
    def test_readme_mentions_reviewer_queue_bundle_owner_handoff(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_bundle_owner_handoff.md", readme)
        self.assertTrue((ROOT / "examples" / "reviewer_queue_bundle_owner_handoff.md").exists())


if __name__ == "__main__":
    unittest.main()
