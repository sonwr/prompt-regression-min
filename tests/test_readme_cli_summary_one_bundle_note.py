from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryOneBundleNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_one_bundle_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_ONE_BUNDLE_NOTE.md", readme)
        self.assertIn("JSON, Markdown, and HTML artifacts together", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_ONE_BUNDLE_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
