from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummarySchemaGateNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_schema_gate_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_SCHEMA_GATE_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_SCHEMA_GATE_NOTE.md").exists())

    def test_note_mentions_explicit_schema_gate(self) -> None:
        note = (ROOT / "docs" / "CLI_SUMMARY_SCHEMA_GATE_NOTE.md").read_text(encoding="utf-8")

        self.assertIn("render one summary JSON artifact", note)
        self.assertIn("require one explicit summary schema version gate", note)
        self.assertIn("pair the JSON artifact with one markdown or PR-comment handoff", note)


if __name__ == "__main__":
    unittest.main()
