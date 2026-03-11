from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliReviewerQueueSourceCaseRateNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_reviewer_queue_source_case_rate_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_REVIEWER_QUEUE_SOURCE_CASE_RATE_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_REVIEWER_QUEUE_SOURCE_CASE_RATE_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
