from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReviewerQueueSummaryOutputTrioTests(unittest.TestCase):
    def test_readme_mentions_reviewer_queue_summary_output_trio(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')

        self.assertIn('examples/reviewer_queue_summary_output_trio.md', readme)
        self.assertTrue((ROOT / 'examples' / 'reviewer_queue_summary_output_trio.md').exists())


if __name__ == '__main__':
    unittest.main()
