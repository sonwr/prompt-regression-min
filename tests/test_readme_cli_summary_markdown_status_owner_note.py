from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"


class ReadmeCliSummaryMarkdownStatusOwnerNoteTests(unittest.TestCase):
    def test_readme_mentions_markdown_status_owner_note(self) -> None:
        readme = README_PATH.read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_MARKDOWN_STATUS_OWNER_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_MARKDOWN_STATUS_OWNER_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
