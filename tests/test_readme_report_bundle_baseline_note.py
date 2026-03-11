from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReportBundleBaselineNoteTests(unittest.TestCase):
    def test_readme_mentions_report_bundle_baseline_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_report_bundle_baseline_note.md", readme)
        self.assertTrue((ROOT / "examples" / "reviewer_queue_report_bundle_baseline_note.md").exists())


if __name__ == "__main__":
    unittest.main()
