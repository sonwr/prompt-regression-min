from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReviewerQueueTrendBundleHandoffTests(unittest.TestCase):
    def test_readme_mentions_trend_bundle_handoff(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('examples/reviewer_queue_trend_bundle_handoff.md', readme)

    def test_example_mentions_pass_rate_trend_and_bundle(self) -> None:
        example = (ROOT / 'examples' / 'reviewer_queue_trend_bundle_handoff.md').read_text(encoding='utf-8')
        self.assertIn('pass-rate trend gate', example)
        self.assertIn('JSON / Markdown / HTML summary bundle', example)


if __name__ == '__main__':
    unittest.main()
