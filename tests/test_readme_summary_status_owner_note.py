from __future__ import annotations

from pathlib import Path
import unittest


class ReadmeSummaryStatusOwnerNoteTests(unittest.TestCase):
    def test_readme_keeps_summary_status_owner_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / 'README.md').read_text(encoding='utf-8')

        self.assertIn('docs/CLI_SUMMARY_STATUS_OWNER_NOTE.md', readme)
        self.assertTrue((root / 'docs' / 'CLI_SUMMARY_STATUS_OWNER_NOTE.md').exists())


if __name__ == '__main__':
    unittest.main()
