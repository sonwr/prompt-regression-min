from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ReadmeCliSummaryQuietDualTitleNoteTests(unittest.TestCase):
    def test_readme_mentions_quiet_dual_title_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_QUIET_DUAL_TITLE_NOTE.md', readme)
        self.assertIn('--summary-markdown-title', readme)
        self.assertIn('--summary-pr-comment-title', readme)

    def test_quiet_dual_title_note_keeps_quiet_stdout_scope(self) -> None:
        note = (ROOT / 'docs' / 'CLI_SUMMARY_QUIET_DUAL_TITLE_NOTE.md').read_text(encoding='utf-8')
        self.assertIn('quiet stdout', note)
        self.assertIn('two explicit reviewer-facing titles', note)

if __name__ == '__main__':
    unittest.main()
