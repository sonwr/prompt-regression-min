from pathlib import Path


def test_readme_mentions_summary_repo45_web_demo_result_card_note() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/CLI_SUMMARY_REPO45_WEB_DEMO_RESULT_CARD_NOTE.md" in readme


def test_repo45_web_demo_result_card_note_mentions_web_app_and_five_line_rule() -> None:
    doc = Path("docs/CLI_SUMMARY_REPO45_WEB_DEMO_RESULT_CARD_NOTE.md").read_text(encoding="utf-8")

    assert "web-app" in doc
    assert "result card" in doc
    assert "Korean" in doc
    assert "five short lines" in doc
