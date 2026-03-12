from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliPassRateTrendGateNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_pass_rate_trend_gate_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_PASS_RATE_TREND_GATE_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_PASS_RATE_TREND_GATE_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
