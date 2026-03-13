from pathlib import Path
import unittest

README = Path(__file__).resolve().parents[1] / 'README.md'


class ReadmeCliSummaryReviewerQueuePrioritySummaryNoteTests(unittest.TestCase):
    def test_readme_mentions_reviewer_queue_priority_summary(self) -> None:
        text = README.read_text(encoding='utf-8')
        self.assertIn('Reviewer queue follow-up priority summary', text)


if __name__ == '__main__':
    unittest.main()
