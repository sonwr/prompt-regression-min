from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeSummaryStdinBundleNoteTests(unittest.TestCase):
    def test_readme_mentions_summary_stdin_bundle_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        note = ROOT / "examples" / "summary_stdin_bundle_note.md"

        self.assertIn("examples/summary_stdin_bundle_note.md", readme)
        self.assertTrue(note.exists())
        self.assertIn("one explicit report basename", note.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
