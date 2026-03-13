from __future__ import annotations

import unittest

from prompt_regression_min.cli import _normalize_heading


class HeadingNormalizationTests(unittest.TestCase):
    def test_normalize_heading_collapses_internal_whitespace(self) -> None:
        self.assertEqual(_normalize_heading("  review   summary\n lane  ", "fallback"), "review summary lane")

    def test_normalize_heading_falls_back_for_blank_values(self) -> None:
        self.assertEqual(_normalize_heading("   ", "prompt-regression-min summary"), "prompt-regression-min summary")


if __name__ == "__main__":
    unittest.main()
