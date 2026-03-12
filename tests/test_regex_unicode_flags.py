from __future__ import annotations

import unittest

from prompt_regression_min.core import _score


class RegexUnicodeFlagsTests(unittest.TestCase):
    def test_regex_accepts_unicode_flag_aliases(self) -> None:
        self.assertTrue(_score("안녕", {"type": "regex", "pattern": r"^안녕$", "flags": ["UNICODE"]}))
        self.assertTrue(_score("안녕", {"type": "regex", "pattern": r"^안녕$", "flags": "U"}))


if __name__ == "__main__":
    unittest.main()
