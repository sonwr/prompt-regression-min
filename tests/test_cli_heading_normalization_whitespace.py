import unittest

from prompt_regression_min.cli import _normalize_heading


class NormalizeHeadingWhitespaceTests(unittest.TestCase):
    def test_heading_collapses_internal_whitespace(self) -> None:
        self.assertEqual(
            _normalize_heading('  reviewer   queue\n status  ', 'fallback title'),
            'reviewer queue status',
        )


if __name__ == '__main__':
    unittest.main()
