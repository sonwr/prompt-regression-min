from pathlib import Path


def test_readme_mentions_plain_text_five_line_note() -> None:
    readme = Path('README.md').read_text(encoding='utf-8')

    assert 'docs/CLI_SUMMARY_PLAIN_TEXT_FIVE_LINE_NOTE.md' in readme


def test_plain_text_five_line_note_mentions_exact_format() -> None:
    doc = Path('docs/CLI_SUMMARY_PLAIN_TEXT_FIVE_LINE_NOTE.md').read_text(encoding='utf-8')

    assert 'plain text' in doc
    assert 'five total lines' in doc
    assert 'commit/push status' in doc
