from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"


class ReadmeReviewerQueueReportBundleTitleGateTests(unittest.TestCase):
    def test_readme_mentions_report_bundle_title_gate(self) -> None:
        readme = README_PATH.read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_report_bundle_title_gate.md", readme)
        self.assertTrue((ROOT / "examples" / "reviewer_queue_report_bundle_title_gate.md").exists())


if __name__ == "__main__":
    unittest.main()
