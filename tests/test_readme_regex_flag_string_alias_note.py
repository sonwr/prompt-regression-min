from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_mentions_regex_flag_string_alias_note() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "docs/REGEX_FLAG_STRING_ALIAS_NOTE.md" in readme
    assert (ROOT / "docs" / "REGEX_FLAG_STRING_ALIAS_NOTE.md").exists()


def test_regex_flag_string_alias_note_mentions_pipe_and_list_equivalence() -> None:
    note = (ROOT / "docs" / "REGEX_FLAG_STRING_ALIAS_NOTE.md").read_text(encoding="utf-8")
    assert "IGNORECASE|MULTILINE" in note
    assert 'expected.flags: ["IGNORECASE", "MULTILINE"]' in note
