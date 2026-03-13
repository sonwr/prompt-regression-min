import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ReadmeCliSummaryFourFiveNonSkipRuleTests(unittest.TestCase):
    def test_readme_mentions_four_five_non_skip_rule(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/CLI_SUMMARY_FOUR_FIVE_NON_SKIP_RULE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_FOUR_FIVE_NON_SKIP_RULE.md").exists())

if __name__ == "__main__":
    unittest.main()
