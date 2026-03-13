from pathlib import Path


def test_readme_mentions_cli_summary_five_repo_field_order_lock_note() -> None:
    readme = Path('README.md').read_text(encoding='utf-8')
    assert 'docs/CLI_SUMMARY_FIVE_REPO_FIELD_ORDER_LOCK_NOTE.md' in readme
