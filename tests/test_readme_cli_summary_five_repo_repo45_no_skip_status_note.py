from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_mentions_cli_summary_five_repo_repo45_no_skip_status_note() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "docs/CLI_SUMMARY_FIVE_REPO_REPO45_NO_SKIP_STATUS_NOTE.md" in readme
    note = (ROOT / "docs" / "CLI_SUMMARY_FIVE_REPO_REPO45_NO_SKIP_STATUS_NOTE.md").read_text(encoding="utf-8")
    assert "repo 4 (`oss-launchpad-cli`) and repo 5 (`governance-sandbox`) must always appear" in note
    assert "validated-or-held status line" in note
