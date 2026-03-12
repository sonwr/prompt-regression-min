import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"


class ReadmeReportBundleFollowupCardTest(unittest.TestCase):
    def test_readme_mentions_report_bundle_followup_card(self) -> None:
        readme = README_PATH.read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_report_bundle_followup_card.md", readme)
        self.assertTrue((ROOT / "examples" / "reviewer_queue_report_bundle_followup_card.md").exists())


if __name__ == "__main__":
    unittest.main()
