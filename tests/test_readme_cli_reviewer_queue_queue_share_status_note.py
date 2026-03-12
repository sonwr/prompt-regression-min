from __future__ import annotations

from pathlib import Path
import unittest


class ReadmeCliReviewerQueueQueueShareStatusNoteTests(unittest.TestCase):
    def test_readme_mentions_queue_share_status_note(self) -> None:
        readme = Path("README.md").read_text(encoding="utf-8")
        self.assertIn("docs/CLI_REVIEWER_QUEUE_QUEUE_SHARE_STATUS_NOTE.md", readme)


if __name__ == "__main__":
    unittest.main()
