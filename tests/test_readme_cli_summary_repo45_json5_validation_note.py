from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CliSummaryRepo45Json5ValidationNoteTests(unittest.TestCase):
    def test_readme_mentions_repo45_json5_validation_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_REPO45_JSON5_VALIDATION_NOTE.md', readme)

    def test_note_mentions_json5_and_validation(self) -> None:
        note = (ROOT / 'docs/CLI_SUMMARY_REPO45_JSON5_VALIDATION_NOTE.md').read_text(encoding='utf-8')
        self.assertIn('.json5', note)
        self.assertIn('validation', note)


if __name__ == '__main__':
    unittest.main()
