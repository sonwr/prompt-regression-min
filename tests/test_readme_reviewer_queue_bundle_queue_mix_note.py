from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReviewerQueueBundleQueueMixNoteTests(unittest.TestCase):
    def test_readme_mentions_bundle_queue_mix_note_example(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_bundle_queue_mix_note.md", readme)
        self.assertTrue((ROOT / "examples" / "reviewer_queue_bundle_queue_mix_note.md").exists())


if __name__ == "__main__":
    unittest.main()
