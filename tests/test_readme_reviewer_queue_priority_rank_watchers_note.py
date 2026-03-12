from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_readme_mentions_reviewer_queue_priority_rank_watchers_note() -> None:
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    assert 'examples/reviewer_queue_priority_rank_watchers_note.md' in readme
    assert (ROOT / 'examples' / 'reviewer_queue_priority_rank_watchers_note.md').exists()
