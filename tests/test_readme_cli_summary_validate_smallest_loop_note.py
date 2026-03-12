from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryValidateSmallestLoopNoteTests(unittest.TestCase):
    def test_readme_mentions_validate_smallest_loop_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_VALIDATE_SMALLEST_LOOP_NOTE.md", readme)


if __name__ == "__main__":
    unittest.main()
