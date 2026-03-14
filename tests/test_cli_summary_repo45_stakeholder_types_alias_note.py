from pathlib import Path
import unittest


class CliSummaryRepo45StakeholderTypesAliasNoteTest(unittest.TestCase):
    def test_readme_mentions_stakeholder_types_alias_note(self) -> None:
        readme = Path('README.md').read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_REPO45_STAKEHOLDER_TYPES_ALIAS_NOTE.md', readme)

    def test_note_exists_and_mentions_stakeholder_types(self) -> None:
        note = Path('docs/CLI_SUMMARY_REPO45_STAKEHOLDER_TYPES_ALIAS_NOTE.md')
        self.assertTrue(note.exists())
        content = note.read_text(encoding='utf-8')
        self.assertIn('stakeholder_types', content)
        self.assertIn('repo 4', content)
        self.assertIn('repo 5', content)


if __name__ == '__main__':
    unittest.main()
