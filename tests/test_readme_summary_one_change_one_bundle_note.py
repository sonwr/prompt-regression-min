from __future__ import annotations

from pathlib import Path
import unittest


class ReadmeSummaryOneChangeOneBundleNoteTests(unittest.TestCase):
    def test_readme_keeps_one_change_one_bundle_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / 'README.md').read_text(encoding='utf-8')

        self.assertIn('docs/CLI_SUMMARY_ONE_CHANGE_ONE_BUNDLE_NOTE.md', readme)
        self.assertTrue((root / 'docs' / 'CLI_SUMMARY_ONE_CHANGE_ONE_BUNDLE_NOTE.md').exists())


if __name__ == '__main__':
    unittest.main()
