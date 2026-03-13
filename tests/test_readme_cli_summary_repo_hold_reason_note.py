from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / 'README.md'
NOTE = ROOT / 'docs' / 'CLI_SUMMARY_REPO_HOLD_REASON_NOTE.md'


class ReadmeCliSummaryRepoHoldReasonNoteTests(unittest.TestCase):
    def test_readme_mentions_note(self) -> None:
        readme = README.read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_REPO_HOLD_REASON_NOTE.md', readme)

    def test_note_mentions_hold_reason(self) -> None:
        note = NOTE.read_text(encoding='utf-8')
        self.assertIn('hold reason', note)
        self.assertIn('validation result', note)


if __name__ == '__main__':
    unittest.main()
