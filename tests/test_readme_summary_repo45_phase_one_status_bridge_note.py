from pathlib import Path


def test_readme_mentions_summary_repo45_phase_one_status_bridge_note() -> None:
    readme = Path('README.md').read_text(encoding='utf-8')

    assert 'docs/CLI_SUMMARY_REPO45_PHASE_ONE_STATUS_BRIDGE_NOTE.md' in readme


def test_repo45_phase_one_status_bridge_note_mentions_mandatory_pair() -> None:
    doc = Path('docs/CLI_SUMMARY_REPO45_PHASE_ONE_STATUS_BRIDGE_NOTE.md').read_text(encoding='utf-8')

    assert 'oss-launchpad-cli' in doc
    assert 'governance-sandbox' in doc
    assert 'scenario-file input first' in doc
    assert 'validation' in doc
