from pathlib import Path


def test_readme_summary_five_repo_repo45_no_skip_note() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "CLI_SUMMARY_FIVE_REPO_REPO45_NO_SKIP_NOTE.md" in readme
