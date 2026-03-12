from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / 'README.md'


class ReadmePriorityRankRunnerUpNoteExampleTests(unittest.TestCase):
    def test_readme_mentions_priority_rank_runner_up_note_example(self) -> None:
        readme = README_PATH.read_text(encoding='utf-8')

        self.assertIn('examples/reviewer_queue_priority_rank_runner_up_note.md', readme)
        self.assertTrue((ROOT / 'examples' / 'reviewer_queue_priority_rank_runner_up_note.md').exists())
