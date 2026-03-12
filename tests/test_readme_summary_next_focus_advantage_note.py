from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeSummaryNextFocusAdvantageNoteTests(unittest.TestCase):
    def test_readme_mentions_summary_next_focus_advantage_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_NEXT_FOCUS_ADVANTAGE_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_NEXT_FOCUS_ADVANTAGE_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
