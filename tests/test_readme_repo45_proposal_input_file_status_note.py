from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeRepo45ProposalInputFileStatusNoteTests(unittest.TestCase):
    def test_readme_mentions_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/CLI_SUMMARY_REPO45_PROPOSAL_INPUT_FILE_STATUS_NOTE.md", readme)

    def test_note_mentions_proposal_input_file_and_validation(self) -> None:
        note = (ROOT / "docs" / "CLI_SUMMARY_REPO45_PROPOSAL_INPUT_FILE_STATUS_NOTE.md").read_text(encoding="utf-8")
        self.assertIn("proposal_input_file", note)
        self.assertIn("validation", note)


if __name__ == "__main__":
    unittest.main()
