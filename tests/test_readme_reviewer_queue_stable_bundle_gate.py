from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReviewerQueueStableBundleGateTests(unittest.TestCase):
    def test_readme_mentions_reviewer_queue_stable_bundle_gate(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_stable_bundle_gate.md", readme)
        self.assertTrue((ROOT / "examples" / "reviewer_queue_stable_bundle_gate.md").exists())


if __name__ == "__main__":
    unittest.main()
