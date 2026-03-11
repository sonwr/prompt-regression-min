from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReviewerQueueCaseCountStatusLineTests(unittest.TestCase):
    def test_readme_mentions_reviewer_queue_case_count_status_line(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_case_count_status_line.md", readme)
        self.assertTrue((ROOT / "examples" / "reviewer_queue_case_count_status_line.md").exists())


if __name__ == "__main__":
    unittest.main()
