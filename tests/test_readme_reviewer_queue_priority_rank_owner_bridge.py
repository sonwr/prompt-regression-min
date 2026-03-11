from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReviewerQueuePriorityRankOwnerBridgeTests(unittest.TestCase):
    def test_readme_mentions_priority_rank_owner_bridge(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_priority_rank_owner_bridge.md", readme)
        self.assertTrue((ROOT / "examples" / "reviewer_queue_priority_rank_owner_bridge.md").exists())


if __name__ == "__main__":
    unittest.main()
