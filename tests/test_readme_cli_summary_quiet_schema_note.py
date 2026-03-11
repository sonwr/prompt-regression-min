from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeCliSummaryQuietSchemaNoteTests(unittest.TestCase):
    def test_readme_links_quiet_schema_note(self):
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_QUIET_SCHEMA_NOTE.md', readme)
        self.assertTrue((ROOT / 'docs' / 'CLI_SUMMARY_QUIET_SCHEMA_NOTE.md').exists())

    def test_note_mentions_quiet_and_schema(self):
        note = (ROOT / 'docs' / 'CLI_SUMMARY_QUIET_SCHEMA_NOTE.md').read_text(encoding='utf-8').lower()
        self.assertIn('--quiet', note)
        self.assertIn('schema', note)
        self.assertIn('artifact', note)


if __name__ == '__main__':
    unittest.main()
