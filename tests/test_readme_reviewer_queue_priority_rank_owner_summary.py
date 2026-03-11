from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReviewerQueuePriorityRankOwnerSummaryTests(unittest.TestCase):
    def test_readme_mentions_reviewer_queue_priority_rank_owner_summary(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_priority_rank_owner_summary.md", readme)
        self.assertTrue((ROOT / "examples" / "reviewer_queue_priority_rank_owner_summary.md").exists())


if __name__ == "__main__":
    unittest.main()
