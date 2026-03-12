from pathlib import Path
import unittest


class ReadmeCliSummaryQueueFocusOwnerNoteTests(unittest.TestCase):
    def test_readme_mentions_queue_focus_owner_note(self) -> None:
        readme = Path("README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_QUEUE_FOCUS_OWNER_NOTE.md", readme)
        self.assertIn("queue focus, status, and the next review action", readme)


if __name__ == "__main__":
    unittest.main()
