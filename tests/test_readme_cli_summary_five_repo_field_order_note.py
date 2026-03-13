from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / 'README.md'


class ReadmeCliSummaryFiveRepoFieldOrderNoteTests(unittest.TestCase):
    def test_readme_mentions_five_repo_field_order_note(self) -> None:
        readme = README_PATH.read_text(encoding='utf-8')

        self.assertIn('docs/CLI_SUMMARY_FIVE_REPO_FIELD_ORDER_NOTE.md', readme)
        self.assertTrue((ROOT / 'docs' / 'CLI_SUMMARY_FIVE_REPO_FIELD_ORDER_NOTE.md').exists())


if __name__ == '__main__':
    unittest.main()
