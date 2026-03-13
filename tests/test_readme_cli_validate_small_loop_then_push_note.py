from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ReadmeCliValidateSmallLoopThenPushNoteTest(unittest.TestCase):
    def test_readme_mentions_validate_small_loop_then_push_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_VALIDATE_SMALL_LOOP_THEN_PUSH_NOTE.md', readme)
        note = (ROOT / 'docs' / 'CLI_SUMMARY_VALIDATE_SMALL_LOOP_THEN_PUSH_NOTE.md').read_text(encoding='utf-8')
        self.assertIn('smallest deterministic local validation loop', note)
        self.assertIn('Commit and push only if that loop stays green', note)

if __name__ == '__main__':
    unittest.main()
