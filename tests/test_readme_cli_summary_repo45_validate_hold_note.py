from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_readme_mentions_cli_summary_repo45_validate_hold_note() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "docs/CLI_SUMMARY_REPO45_VALIDATE_HOLD_NOTE.md" in readme
    assert (ROOT / "docs" / "CLI_SUMMARY_REPO45_VALIDATE_HOLD_NOTE.md").exists()
