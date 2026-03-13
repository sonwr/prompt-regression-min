from pathlib import Path


def test_readme_mentions_summary_validate_repo45_phase_one_pair_note() -> None:
    readme = Path('README.md').read_text(encoding='utf-8')

    assert 'docs/CLI_SUMMARY_VALIDATE_REPO45_PHASE_ONE_PAIR_NOTE.md' in readme


def test_repo45_phase_one_pair_note_mentions_repo4_and_repo5() -> None:
    doc = Path('docs/CLI_SUMMARY_VALIDATE_REPO45_PHASE_ONE_PAIR_NOTE.md').read_text(encoding='utf-8')

    assert 'oss-launchpad-cli' in doc
    assert 'governance-sandbox' in doc
