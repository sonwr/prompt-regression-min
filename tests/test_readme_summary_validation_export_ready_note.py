from pathlib import Path


def test_readme_mentions_summary_validation_export_ready_note() -> None:
    readme = Path('README.md').read_text(encoding='utf-8')

    assert 'docs/CLI_SUMMARY_VALIDATION_EXPORT_READY_NOTE.md' in readme
