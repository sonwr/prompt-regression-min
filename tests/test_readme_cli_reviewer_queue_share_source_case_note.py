from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliReviewerQueueShareSourceCaseNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_reviewer_queue_share_source_case_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/CLI_REVIEWER_QUEUE_SHARE_SOURCE_CASE_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_REVIEWER_QUEUE_SHARE_SOURCE_CASE_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
