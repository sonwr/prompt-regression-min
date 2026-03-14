from pathlib import Path


def test_readme_mentions_five_repo_short_report_discipline_note() -> None:
    text = Path("README.md").read_text(encoding="utf-8")
    assert "docs/CLI_SUMMARY_FIVE_REPO_SHORT_REPORT_DISCIPLINE_NOTE.md" in text
