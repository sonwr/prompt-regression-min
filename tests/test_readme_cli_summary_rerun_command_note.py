from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_mentions_cli_summary_rerun_command_note() -> None:
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')

    assert 'docs/CLI_SUMMARY_RERUN_COMMAND_NOTE.md' in readme
    assert (ROOT / 'docs' / 'CLI_SUMMARY_RERUN_COMMAND_NOTE.md').exists()
