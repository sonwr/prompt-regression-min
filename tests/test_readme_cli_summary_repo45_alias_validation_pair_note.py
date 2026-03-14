from pathlib import Path


def test_readme_cli_summary_repo45_alias_validation_pair_note() -> None:
    text = Path("README.md").read_text(encoding="utf-8")
    assert "docs/CLI_SUMMARY_REPO45_ALIAS_VALIDATION_PAIR_NOTE.md" in text
