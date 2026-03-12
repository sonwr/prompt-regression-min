import unittest

from prompt_regression_min.cli import _normalize_heading


class NormalizeHeadingTests(unittest.TestCase):
    def test_blank_heading_uses_fallback(self) -> None:
        self.assertEqual(_normalize_heading("   ", "fallback title"), "fallback title")

    def test_heading_is_trimmed(self) -> None:
        self.assertEqual(_normalize_heading("  reviewer note  ", "fallback title"), "reviewer note")


if __name__ == "__main__":
    unittest.main()
