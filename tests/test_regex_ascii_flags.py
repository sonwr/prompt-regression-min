from prompt_regression_min.core import _score


def test_regex_ascii_flag_alias_blocks_unicode_word_match():
    expected = {"type": "regex", "pattern": r"^\w+$", "flags": ["ASCII"]}

    assert _score("token_123", expected) is True
    assert _score("한글", expected) is False
