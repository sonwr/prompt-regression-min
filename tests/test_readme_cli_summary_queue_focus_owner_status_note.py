from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryQueueFocusOwnerStatusNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_queue_focus_owner_status_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_QUEUE_FOCUS_OWNER_STATUS_NOTE.md', readme)

    def test_note_mentions_queue_focus_owner_and_status_line(self) -> None:
        note = (ROOT / 'docs' / 'CLI_SUMMARY_QUEUE_FOCUS_OWNER_STATUS_NOTE.md').read_text(encoding='utf-8')
        self.assertIn('active queue focus', note)
        self.assertIn('owner', note)
        self.assertIn('status line', note)


if __name__ == '__main__':
    unittest.main()
