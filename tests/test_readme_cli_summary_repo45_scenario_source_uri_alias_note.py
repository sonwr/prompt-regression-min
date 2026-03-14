from pathlib import Path


def test_readme_cli_summary_repo45_scenario_source_uri_alias_note() -> None:
    root = Path(__file__).resolve().parents[1]
    readme = (root / "README.md").read_text(encoding="utf-8")
    note = (root / "docs" / "CLI_SUMMARY_REPO45_SCENARIO_SOURCE_URI_ALIAS_NOTE.md").read_text(encoding="utf-8")

    assert "docs/CLI_SUMMARY_REPO45_SCENARIO_SOURCE_URI_ALIAS_NOTE.md" in readme
    assert "scenario_source_uri" in note
    assert "JSON/Markdown/HTML" in note
