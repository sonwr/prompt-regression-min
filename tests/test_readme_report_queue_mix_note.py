from pathlib import Path
import unittest


class ReadmeReportQueueMixNoteTests(unittest.TestCase):
    def test_readme_mentions_report_queue_mix_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / 'README.md').read_text(encoding='utf-8')

        self.assertIn('docs/REPORT_QUEUE_MIX_NOTE.md', readme)
        note = root / 'docs' / 'REPORT_QUEUE_MIX_NOTE.md'
        self.assertTrue(note.exists())
        note_text = note.read_text(encoding='utf-8')
        self.assertIn('queue mix', note_text.lower())
        self.assertIn('report bundle', note_text.lower())


if __name__ == '__main__':
    unittest.main()
