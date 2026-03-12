import unittest

from prompt_regression_min.core import _score


class RegexFlagAliasTests(unittest.TestCase):
    def test_regex_flag_singular_alias_accepts_string(self) -> None:
        self.assertTrue(
            _score(
                "ALPHA\nomega",
                {"type": "regex", "pattern": "^alpha$", "regex_flag": "IGNORECASE|MULTILINE"},
            )
        )


if __name__ == "__main__":
    unittest.main()
