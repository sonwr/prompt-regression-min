from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ReadmePriorityRankOwnerHandoffExampleTests(unittest.TestCase):
    def test_readme_mentions_priority_rank_owner_handoff_example(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('examples/reviewer_queue_priority_rank_owner_handoff.md', readme)
        self.assertTrue((ROOT / 'examples' / 'reviewer_queue_priority_rank_owner_handoff.md').exists())

if __name__ == '__main__':
    unittest.main()
