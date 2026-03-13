from pathlib import Path


def test_readme_mentions_cli_summary_repo45_reports_directory_validate_status_note() -> None:
    readme = Path('README.md').read_text(encoding='utf-8')

    assert 'docs/CLI_SUMMARY_REPO45_REPORTS_DIRECTORY_VALIDATE_STATUS_NOTE.md' in readme


def test_cli_summary_repo45_reports_directory_validate_status_note_mentions_validate_before_push() -> None:
    doc = Path('docs/CLI_SUMMARY_REPO45_REPORTS_DIRECTORY_VALIDATE_STATUS_NOTE.md').read_text(encoding='utf-8')

    assert 'reports_directory' in doc
    assert 'validate' in doc
    assert 'commit/push or hold status' in doc
