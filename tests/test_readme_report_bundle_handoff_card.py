from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReportBundleHandoffCardTests(unittest.TestCase):
    def test_readme_mentions_report_bundle_handoff_card(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')

        self.assertIn('examples/reviewer_queue_report_bundle_handoff_card.md', readme)
        self.assertTrue((ROOT / 'examples' / 'reviewer_queue_report_bundle_handoff_card.md').exists())


if __name__ == '__main__':
    unittest.main()
