from pathlib import Path
import unittest


class ReadmeReviewerQueuePriorityRankOwnerReadyBridgeTest(unittest.TestCase):
    def test_readme_mentions_owner_ready_bridge(self) -> None:
        readme = Path('README.md').read_text()
        self.assertIn(
            'examples/reviewer_queue_priority_rank_owner_ready_bridge.md',
            readme,
        )


if __name__ == '__main__':
    unittest.main()
