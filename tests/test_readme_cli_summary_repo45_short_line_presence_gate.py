from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryRepo45ShortLinePresenceGateTests(unittest.TestCase):
    def test_readme_mentions_repo45_short_line_presence_gate(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_REPO45_SHORT_LINE_PRESENCE_GATE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_REPO45_SHORT_LINE_PRESENCE_GATE.md").exists())


if __name__ == "__main__":
    unittest.main()
