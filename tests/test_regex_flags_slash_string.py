from prompt_regression_min.core import _score


def test_regex_supports_slash_delimited_flag_string() -> None:
    expected = {"type": "regex", "pattern": r"^alpha.+omega$", "flags": "ignorecase/dotall"}
    assert _score("ALPHA\nbody\nomega", expected)
