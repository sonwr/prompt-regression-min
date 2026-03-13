from pathlib import Path


def test_readme_mentions_summary_five_repo_commit_hold_reason_note() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "docs/CLI_SUMMARY_FIVE_REPO_COMMIT_HOLD_REASON_NOTE.md" in readme
