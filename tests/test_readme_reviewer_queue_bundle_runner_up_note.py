from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReviewerQueueBundleRunnerUpNoteTests(unittest.TestCase):
    def test_readme_mentions_bundle_runner_up_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_bundle_runner_up_note.md", readme)
        self.assertTrue((ROOT / "examples" / "reviewer_queue_bundle_runner_up_note.md").exists())


if __name__ == "__main__":
    unittest.main()
