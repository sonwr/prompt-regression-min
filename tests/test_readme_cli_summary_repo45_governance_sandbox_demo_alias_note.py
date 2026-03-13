from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryRepo45GovernanceSandboxDemoAliasNoteTests(unittest.TestCase):
    def test_readme_mentions_repo45_governance_sandbox_demo_alias_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/CLI_SUMMARY_REPO45_GOVERNANCE_SANDBOX_DEMO_ALIAS_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_REPO45_GOVERNANCE_SANDBOX_DEMO_ALIAS_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
