from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReviewerQueueNextFocusOwnerPingTests(unittest.TestCase):
    def test_readme_mentions_next_focus_owner_ping(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')

        self.assertIn('examples/reviewer_queue_next_focus_owner_ping.md', readme)
        self.assertTrue((ROOT / 'examples' / 'reviewer_queue_next_focus_owner_ping.md').exists())


if __name__ == '__main__':
    unittest.main()
