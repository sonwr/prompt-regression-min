from pathlib import Path
import unittest


class ReadmeCliSummaryHtmlBundleReopenNoteTests(unittest.TestCase):
    def test_readme_mentions_html_bundle_reopen_note(self) -> None:
        readme = Path('README.md').read_text(encoding='utf-8')

        self.assertIn('docs/CLI_SUMMARY_HTML_BUNDLE_REOPEN_NOTE.md', readme)
        self.assertIn('JSON, Markdown, and HTML summary bundle', readme)


if __name__ == '__main__':
    unittest.main()
