from pathlib import Path


def test_readme_mentions_cli_summary_report_basename_stability_note() -> None:
    root = Path(__file__).resolve().parents[1]
    readme = (root / "README.md").read_text(encoding="utf-8")
    assert "docs/CLI_SUMMARY_REPORT_BASENAME_STABILITY_NOTE.md" in readme
    assert (root / "docs" / "CLI_SUMMARY_REPORT_BASENAME_STABILITY_NOTE.md").exists()
