from __future__ import annotations

from pathlib import Path
import unittest


class ReadmeSummaryFiveRepoHoldReasonNoteTests(unittest.TestCase):
    def test_readme_mentions_summary_five_repo_hold_reason_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / 'README.md').read_text(encoding='utf-8')

        self.assertIn('docs/CLI_SUMMARY_FIVE_REPO_HOLD_REASON_NOTE.md', readme)
        self.assertTrue((root / 'docs' / 'CLI_SUMMARY_FIVE_REPO_HOLD_REASON_NOTE.md').exists())
