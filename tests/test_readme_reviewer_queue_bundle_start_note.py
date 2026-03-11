import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReviewerQueueBundleStartNoteTest(unittest.TestCase):
    def test_readme_mentions_reviewer_queue_bundle_start_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_bundle_start_note.md", readme)
        self.assertTrue((ROOT / "examples" / "reviewer_queue_bundle_start_note.md").exists())
