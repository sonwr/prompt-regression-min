from pathlib import Path


def test_readme_mentions_reviewer_queue_share_bundle_owner_status_line() -> None:
    text = Path("README.md").read_text(encoding="utf-8")
    assert "examples/reviewer_queue_share_bundle_owner_status_line.md" in text
