import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReportBundleStartTest(unittest.TestCase):
    def test_readme_mentions_report_bundle_start(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_report_bundle_start.md", readme)
        self.assertTrue((ROOT / "examples" / "reviewer_queue_report_bundle_start.md").exists())
