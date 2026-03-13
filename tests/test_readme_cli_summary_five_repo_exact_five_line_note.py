import unittest
from pathlib import Path


class ReadmeExactFiveLineNoteTest(unittest.TestCase):
    def test_readme_mentions_cli_summary_five_repo_exact_five_line_note(self) -> None:
        readme = Path('README.md').read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_FIVE_REPO_EXACT_FIVE_LINE_NOTE.md', readme)


if __name__ == '__main__':
    unittest.main()
