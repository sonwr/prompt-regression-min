from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CliSummaryRepo45ReportBundleCodeAliasNoteTests(unittest.TestCase):
    def test_readme_mentions_repo45_report_bundle_code_alias_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_REPO45_REPORT_BUNDLE_CODE_ALIAS_NOTE.md', readme)

    def test_note_mentions_report_bundle_code_and_validation(self) -> None:
        note = (ROOT / 'docs' / 'CLI_SUMMARY_REPO45_REPORT_BUNDLE_CODE_ALIAS_NOTE.md').read_text(encoding='utf-8')
        self.assertIn('report_bundle_code', note)
        self.assertIn('validation', note)


if __name__ == '__main__':
    unittest.main()
