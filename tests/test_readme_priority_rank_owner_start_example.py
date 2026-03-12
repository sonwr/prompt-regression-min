from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / 'README.md'


class ReadmePriorityRankOwnerStartExampleTests(unittest.TestCase):
    def test_readme_mentions_priority_rank_owner_start_example(self) -> None:
        readme = README_PATH.read_text(encoding='utf-8')
        self.assertIn('examples/reviewer_queue_priority_rank_owner_start.md', readme)
        self.assertTrue((ROOT / 'examples' / 'reviewer_queue_priority_rank_owner_start.md').exists())


if __name__ == '__main__':
    unittest.main()
