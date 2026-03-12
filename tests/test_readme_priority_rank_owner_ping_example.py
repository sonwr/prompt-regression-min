from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
EXAMPLE = ROOT / "examples" / "reviewer_queue_priority_rank_owner_ping.md"


def test_readme_mentions_priority_rank_owner_ping_example() -> None:
    readme = README.read_text(encoding="utf-8")

    assert "examples/reviewer_queue_priority_rank_owner_ping.md" in readme
    assert EXAMPLE.exists()
