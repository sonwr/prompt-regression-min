from __future__ import annotations

from pathlib import Path
import unittest


class ReadmeSummaryQueueFocusPrCommentNoteTests(unittest.TestCase):
    def test_readme_mentions_summary_queue_focus_pr_comment_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_QUEUE_FOCUS_PR_COMMENT_NOTE.md", readme)
        self.assertTrue((root / "docs" / "CLI_SUMMARY_QUEUE_FOCUS_PR_COMMENT_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
