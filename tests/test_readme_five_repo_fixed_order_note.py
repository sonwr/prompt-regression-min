from pathlib import Path


def test_readme_mentions_five_repo_fixed_order_note() -> None:
    text = Path("README.md").read_text(encoding="utf-8")
    assert "docs/CLI_SUMMARY_FIVE_REPO_FIXED_ORDER_NOTE.md" in text
