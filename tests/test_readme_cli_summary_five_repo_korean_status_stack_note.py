from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryFiveRepoKoreanStatusStackNoteTest(unittest.TestCase):
    def test_readme_mentions_five_repo_korean_status_stack_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        note = (ROOT / 'docs' / 'CLI_SUMMARY_FIVE_REPO_KOREAN_STATUS_STACK_NOTE.md').read_text(encoding='utf-8')

        self.assertIn('docs/CLI_SUMMARY_FIVE_REPO_KOREAN_STATUS_STACK_NOTE.md', readme)
        self.assertIn('repo name', note)
        self.assertIn('validation status', note)
        self.assertIn('short hold reason', note)


if __name__ == '__main__':
    unittest.main()
