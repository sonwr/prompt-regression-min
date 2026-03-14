from pathlib import Path
import unittest


class ReadmeSummaryRepo45ReportOutputTagAliasNoteTests(unittest.TestCase):
    def test_readme_mentions_repo45_report_output_tag_alias_note(self) -> None:
        readme = Path('README.md').read_text(encoding='utf-8')
        note = Path('docs/CLI_SUMMARY_REPO45_REPORT_OUTPUT_TAG_ALIAS_NOTE.md').read_text(encoding='utf-8')

        self.assertIn('docs/CLI_SUMMARY_REPO45_REPORT_OUTPUT_TAG_ALIAS_NOTE.md', readme)
        self.assertIn('report_output_tag', note)
        self.assertIn('JSON/Markdown/HTML bundle', note)


if __name__ == '__main__':
    unittest.main()
