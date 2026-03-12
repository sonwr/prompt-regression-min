from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
NOTE = ROOT / "docs" / "CLI_SUMMARY_SHORT_REPO_STATUS_LINE_NOTE.md"


class ReadmeCliSummaryShortRepoStatusLineNoteTests(unittest.TestCase):
    def test_readme_mentions_note(self) -> None:
        readme = README.read_text(encoding="utf-8")
        self.assertIn("docs/CLI_SUMMARY_SHORT_REPO_STATUS_LINE_NOTE.md", readme)

    def test_note_mentions_four_fields(self) -> None:
        note = NOTE.read_text(encoding="utf-8")
        self.assertIn("repo name", note)
        self.assertIn("commit/push state or hold reason", note)


if __name__ == "__main__":
    unittest.main()
