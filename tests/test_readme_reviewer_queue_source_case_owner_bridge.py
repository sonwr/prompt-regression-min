from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
NOTE = ROOT / "examples" / "reviewer_queue_source_case_owner_bridge.md"


def test_readme_mentions_source_case_owner_bridge() -> None:
    readme = README.read_text(encoding="utf-8")
    assert "examples/reviewer_queue_source_case_owner_bridge.md" in readme
    assert "owner who should act next" in readme


def test_source_case_owner_bridge_note_keeps_owner_action_visible() -> None:
    note = NOTE.read_text(encoding="utf-8")
    assert "source_case_rate stays highest" in note
    assert "should reopen the shared report bundle" in note
