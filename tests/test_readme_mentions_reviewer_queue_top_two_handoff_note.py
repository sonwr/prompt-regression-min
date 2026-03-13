from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReviewerQueueTopTwoHandoffNoteTests(unittest.TestCase):
    def test_readme_mentions_reviewer_queue_top_two_handoff_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('docs/CLI_REVIEWER_QUEUE_TOP_TWO_HANDOFF_NOTE.md', readme)
        self.assertTrue((ROOT / 'docs' / 'CLI_REVIEWER_QUEUE_TOP_TWO_HANDOFF_NOTE.md').exists())


if __name__ == '__main__':
    unittest.main()
