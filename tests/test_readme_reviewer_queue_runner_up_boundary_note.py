from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
NOTE = ROOT / "examples" / "reviewer_queue_runner_up_boundary_note.md"


def test_readme_mentions_runner_up_boundary_note() -> None:
    readme = README.read_text(encoding="utf-8")
    assert "examples/reviewer_queue_runner_up_boundary_note.md" in readme
    assert "runner-up visible" in readme


def test_runner_up_boundary_note_mentions_narrow_margin() -> None:
    note = NOTE.read_text(encoding="utf-8")
    assert "runner-up" in note
    assert "margin is still narrow" in note
