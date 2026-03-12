from __future__ import annotations

from pathlib import Path
import unittest


class ReadmeCliSummaryBundlePathsNoteTests(unittest.TestCase):
    def test_readme_keeps_cli_summary_bundle_paths_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / 'README.md').read_text(encoding='utf-8')

        self.assertIn('docs/CLI_SUMMARY_BUNDLE_PATHS_NOTE.md', readme)
        self.assertIn('machine-readable JSON path and the reviewer-facing markdown path', readme)
        self.assertTrue((root / 'docs' / 'CLI_SUMMARY_BUNDLE_PATHS_NOTE.md').exists())


if __name__ == '__main__':
    unittest.main()
