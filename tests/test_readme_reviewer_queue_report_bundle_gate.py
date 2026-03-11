from pathlib import Path


def test_readme_mentions_reviewer_queue_report_bundle_gate() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "examples/reviewer_queue_report_bundle_gate.md" in readme
    assert "selected reviewer queue tied to its saved report bundle" in readme
