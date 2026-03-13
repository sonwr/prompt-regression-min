from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / 'README.md'
NOTE = ROOT / 'docs' / 'CLI_SUMMARY_REPO45_SCENARIO_SHOWCASE_RESULT_CARD_NOTE.md'


def test_readme_mentions_repo45_scenario_showcase_result_card_note() -> None:
    readme = README.read_text(encoding='utf-8')
    assert 'docs/CLI_SUMMARY_REPO45_SCENARIO_SHOWCASE_RESULT_CARD_NOTE.md' in readme
    assert 'scenario_showcase' in readme


def test_repo45_scenario_showcase_result_card_note_keeps_validation_gate_visible() -> None:
    note = NOTE.read_text(encoding='utf-8')
    assert 'scenario_showcase' in note
    assert 'result card' in note
    assert 'validation-backed' in note
