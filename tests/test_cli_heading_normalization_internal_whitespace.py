import unittest

from prompt_regression_min.cli import _normalize_heading


class NormalizeHeadingInternalWhitespaceTests(unittest.TestCase):
    def test_heading_collapses_tabs_and_multiline_spacing(self) -> None:
        self.assertEqual(
            _normalize_heading('\t reviewer\tqueue\n\nstatus \t update  ', 'fallback title'),
            'reviewer queue status update',
        )


if __name__ == '__main__':
    unittest.main()
