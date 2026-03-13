from pathlib import Path


def test_readme_mentions_summary_repo45_short_kr_status_note() -> None:
    readme = Path('README.md').read_text(encoding='utf-8')

    assert 'docs/CLI_SUMMARY_REPO45_SHORT_KR_STATUS_NOTE.md' in readme


def test_repo45_short_kr_status_note_mentions_korean_five_line_rule() -> None:
    doc = Path('docs/CLI_SUMMARY_REPO45_SHORT_KR_STATUS_NOTE.md').read_text(encoding='utf-8')

    assert 'oss-launchpad-cli' in doc
    assert 'governance-sandbox' in doc
    assert 'Korean' in doc
    assert 'five short lines' in doc
