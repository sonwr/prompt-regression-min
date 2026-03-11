from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmePriorityRankReopenTiebreakTests(unittest.TestCase):
    def test_readme_mentions_priority_rank_reopen_tiebreak_example(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('examples/reviewer_queue_priority_rank_reopen_tiebreak.md', readme)
        self.assertTrue((ROOT / 'examples' / 'reviewer_queue_priority_rank_reopen_tiebreak.md').exists())
