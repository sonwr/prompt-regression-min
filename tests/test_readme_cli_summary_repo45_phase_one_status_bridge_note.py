from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_readme_mentions_cli_summary_repo45_phase_one_status_bridge_note() -> None:
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    assert 'docs/CLI_SUMMARY_REPO45_PHASE_ONE_STATUS_BRIDGE_NOTE.md' in readme
    assert (ROOT / 'docs' / 'CLI_SUMMARY_REPO45_PHASE_ONE_STATUS_BRIDGE_NOTE.md').exists()
