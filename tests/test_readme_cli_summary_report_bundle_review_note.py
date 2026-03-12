from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_readme_mentions_cli_summary_report_bundle_review_note() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "docs/CLI_SUMMARY_REPORT_BUNDLE_REVIEW_NOTE.md" in readme
    assert (ROOT / "docs/CLI_SUMMARY_REPORT_BUNDLE_REVIEW_NOTE.md").exists()
