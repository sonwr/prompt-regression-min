from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeFiveRepoValidateBeforePushLineNoteTests(unittest.TestCase):
    def test_readme_mentions_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/CLI_SUMMARY_FIVE_REPO_VALIDATE_BEFORE_PUSH_LINE_NOTE.md", readme)

    def test_note_mentions_validation_and_push(self) -> None:
        note = (ROOT / "docs" / "CLI_SUMMARY_FIVE_REPO_VALIDATE_BEFORE_PUSH_LINE_NOTE.md").read_text(encoding="utf-8")
        self.assertIn("validation", note)
        self.assertIn("push", note)


if __name__ == "__main__":
    unittest.main()
