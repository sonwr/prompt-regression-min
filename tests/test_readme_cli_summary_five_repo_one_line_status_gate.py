import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ReadmeCliSummaryFiveRepoOneLineStatusGateTests(unittest.TestCase):
    def test_readme_mentions_gate(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/CLI_SUMMARY_FIVE_REPO_ONE_LINE_STATUS_GATE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_FIVE_REPO_ONE_LINE_STATUS_GATE.md").exists())

if __name__ == "__main__":
    unittest.main()
