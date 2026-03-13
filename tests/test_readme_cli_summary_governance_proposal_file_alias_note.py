from pathlib import Path


def test_readme_mentions_cli_summary_governance_proposal_file_alias_note() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "docs/CLI_SUMMARY_GOVERNANCE_PROPOSAL_FILE_ALIAS_NOTE.md" in readme
