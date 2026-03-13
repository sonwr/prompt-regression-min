from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryQueueShareStatusCardNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_queue_share_status_card_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_QUEUE_SHARE_STATUS_CARD_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_QUEUE_SHARE_STATUS_CARD_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
