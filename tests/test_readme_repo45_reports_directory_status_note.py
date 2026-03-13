from pathlib import Path


def test_readme_mentions_repo45_reports_directory_status_note() -> None:
    root = Path(__file__).resolve().parents[1]
    readme = (root / "README.md").read_text(encoding="utf-8")
    note = (root / "docs" / "CLI_SUMMARY_REPO45_REPORTS_DIRECTORY_STATUS_NOTE.md").read_text(encoding="utf-8")
    assert "CLI_SUMMARY_REPO45_REPORTS_DIRECTORY_STATUS_NOTE.md" in readme
    assert "reports_directory" in note
    assert "green validation rerun" in note
