from pathlib import Path


def test_readme_mentions_reviewer_queue_priority_rank_release_bundle_note() -> None:
    readme = Path('README.md').read_text(encoding='utf-8')
    assert 'examples/reviewer_queue_priority_rank_release_bundle_note.md' in readme
    assert Path('examples/reviewer_queue_priority_rank_release_bundle_note.md').exists()
