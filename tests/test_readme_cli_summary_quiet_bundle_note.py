from __future__ import annotations

from pathlib import Path
import unittest


class ReadmeCliSummaryQuietBundleNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_quiet_bundle_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_QUIET_BUNDLE_NOTE.md", readme)
        self.assertTrue((root / "docs" / "CLI_SUMMARY_QUIET_BUNDLE_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
