from pathlib import Path


def test_readme_mentions_summary_validation_gate_owner_note() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/CLI_SUMMARY_VALIDATION_GATE_OWNER_NOTE.md" in readme
