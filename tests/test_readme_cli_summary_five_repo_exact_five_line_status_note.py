from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryFiveRepoExactFiveLineStatusNoteTests(unittest.TestCase):
    def test_readme_mentions_cli_summary_five_repo_exact_five_line_status_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_FIVE_REPO_EXACT_FIVE_LINE_STATUS_NOTE.md', readme)
        self.assertTrue((ROOT / 'docs' / 'CLI_SUMMARY_FIVE_REPO_EXACT_FIVE_LINE_STATUS_NOTE.md').exists())


if __name__ == '__main__':
    unittest.main()
