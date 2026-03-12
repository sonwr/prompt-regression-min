from pathlib import Path


def test_readme_mentions_five_repo_compact_status_gate() -> None:
    text = Path("README.md").read_text(encoding="utf-8")
    assert "docs/CLI_SUMMARY_FIVE_REPO_COMPACT_STATUS_GATE.md" in text
