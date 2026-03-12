from pathlib import Path


def test_readme_mentions_five_repo_one_line_status_note() -> None:
    text = Path("README.md").read_text(encoding="utf-8")
    assert "docs/CLI_SUMMARY_FIVE_REPO_ONE_LINE_STATUS_NOTE.md" in text
