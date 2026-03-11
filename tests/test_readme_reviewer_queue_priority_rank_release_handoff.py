from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReviewerQueuePriorityRankReleaseHandoffTests(unittest.TestCase):
    def test_readme_mentions_priority_rank_release_handoff(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_priority_rank_release_handoff.md", readme)
        self.assertTrue((ROOT / "examples" / "reviewer_queue_priority_rank_release_handoff.md").exists())


if __name__ == "__main__":
    unittest.main()
