from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryQueueWinnerValidateSlugNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_queue_winner_validate_slug_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_QUEUE_WINNER_VALIDATE_SLUG_NOTE.md', readme)
        note = (ROOT / 'docs' / 'CLI_SUMMARY_QUEUE_WINNER_VALIDATE_SLUG_NOTE.md').read_text(encoding='utf-8')
        self.assertIn('winning reviewer queue first', note)
        self.assertIn('validation command second', note)
        self.assertIn('saved output slug third', note)


if __name__ == '__main__':
    unittest.main()
