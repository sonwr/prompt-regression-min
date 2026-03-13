from pathlib import Path


def test_readme_mentions_five_repo_validate_hold_status_note() -> None:
    readme = Path(__file__).resolve().parents[1] / "README.md"
    assert "docs/CLI_SUMMARY_FIVE_REPO_VALIDATE_HOLD_STATUS_NOTE.md" in readme.read_text(encoding="utf-8")
