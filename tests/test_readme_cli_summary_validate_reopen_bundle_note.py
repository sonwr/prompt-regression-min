from pathlib import Path
import unittest


class ReadmeCliSummaryValidateReopenBundleNoteTests(unittest.TestCase):
    def test_readme_mentions_validate_reopen_bundle_note(self) -> None:
        readme = Path("README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_VALIDATE_REOPEN_BUNDLE_NOTE.md", readme)
        self.assertIn("validate first and only then reopen the saved bundle", readme)


if __name__ == "__main__":
    unittest.main()
