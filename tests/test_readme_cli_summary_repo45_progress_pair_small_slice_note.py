from pathlib import Path


def test_readme_mentions_cli_summary_repo45_progress_pair_small_slice_note() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "docs/CLI_SUMMARY_REPO45_PROGRESS_PAIR_SMALL_SLICE_NOTE.md" in readme
