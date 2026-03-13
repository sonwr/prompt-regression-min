from __future__ import annotations

import unittest
from pathlib import Path


class ReadmeSummaryQueueOwnerValidateStatusNoteTests(unittest.TestCase):
    def test_readme_mentions_summary_queue_owner_validate_status_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_QUEUE_OWNER_VALIDATE_STATUS_NOTE.md", readme)
        self.assertTrue((root / "docs" / "CLI_SUMMARY_QUEUE_OWNER_VALIDATE_STATUS_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
