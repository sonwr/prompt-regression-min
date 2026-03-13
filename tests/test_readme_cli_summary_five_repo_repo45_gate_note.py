from pathlib import Path


def test_readme_mentions_cli_summary_five_repo_repo45_gate_note() -> None:
    text = Path("README.md").read_text(encoding="utf-8")
    assert "docs/CLI_SUMMARY_FIVE_REPO_REPO45_GATE_NOTE.md" in text
