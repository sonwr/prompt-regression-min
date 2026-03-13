from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CliSummaryReportSchemaGateNoteTest(unittest.TestCase):
    def test_note_mentions_schema_gate_and_matching_markdown_artifact(self) -> None:
        doc = (ROOT / "docs" / "CLI_SUMMARY_REPORT_SCHEMA_GATE_NOTE.md").read_text(encoding="utf-8")

        self.assertIn("--require-summary-schema-version", doc)
        self.assertIn("machine-readable summary output plus markdown handoff text", doc)
        self.assertIn("one matching markdown artifact", doc)

    def test_note_keeps_commit_gate_after_validation(self) -> None:
        doc = (ROOT / "docs" / "CLI_SUMMARY_REPORT_SCHEMA_GATE_NOTE.md").read_text(encoding="utf-8")

        self.assertIn("commit only after the validation command stays green", doc)


if __name__ == "__main__":
    unittest.main()
