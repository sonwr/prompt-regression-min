from pathlib import Path


def test_readme_mentions_repo45_scenario_report_validate_pair_note() -> None:
    root = Path(__file__).resolve().parents[1]
    readme = (root / "README.md").read_text(encoding="utf-8")
    note = (root / "docs" / "CLI_SUMMARY_REPO45_SCENARIO_REPORT_VALIDATE_PAIR_NOTE.md").read_text(encoding="utf-8")

    assert "docs/CLI_SUMMARY_REPO45_SCENARIO_REPORT_VALIDATE_PAIR_NOTE.md" in readme
    assert "scenario-file -> JSON/Markdown/HTML report replay" in note
    assert "five-line report" in note
