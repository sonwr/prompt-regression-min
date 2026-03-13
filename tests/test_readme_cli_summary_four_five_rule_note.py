import unittest
from pathlib import Path


class ReadmeFourFiveRuleNoteTest(unittest.TestCase):
    def test_readme_mentions_four_five_rule_note(self) -> None:
        text = Path("README.md").read_text(encoding="utf-8")
        self.assertIn("docs/CLI_SUMMARY_FIVE_REPO_FOUR_FIVE_RULE_NOTE.md", text)


if __name__ == "__main__":
    unittest.main()
