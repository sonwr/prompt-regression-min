import unittest
from pathlib import Path


class ReadmeCliSummaryProposalInputMarkdownPathNoteTest(unittest.TestCase):
    def test_readme_mentions_cli_summary_proposal_input_markdown_path_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / 'README.md').read_text(encoding='utf-8')
        note = (root / 'docs' / 'CLI_SUMMARY_PROPOSAL_INPUT_MARKDOWN_PATH_NOTE.md').read_text(encoding='utf-8')

        self.assertIn('docs/CLI_SUMMARY_PROPOSAL_INPUT_MARKDOWN_PATH_NOTE.md', readme)
        self.assertIn('proposal_input_markdown_path', note)
        self.assertIn('five-line repo summary', note)


if __name__ == '__main__':
    unittest.main()
