from pathlib import Path


def test_readme_mentions_summary_validate_owner_queue_mini_loop_note() -> None:
    readme = Path('README.md').read_text(encoding='utf-8')

    assert 'docs/SUMMARY_VALIDATE_OWNER_QUEUE_MINI_LOOP_NOTE.md' in readme
