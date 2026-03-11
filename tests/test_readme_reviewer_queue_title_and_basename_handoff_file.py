from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReadmeReviewerQueueTitleAndBasenameHandoffFileTest(unittest.TestCase):
    def test_readme_link_target_exists(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        rel = "examples/reviewer_queue_title_and_basename_handoff.md"
        self.assertIn(rel, readme)
        path = ROOT / rel
        self.assertTrue(path.exists())
        note = path.read_text(encoding="utf-8")
        self.assertIn("bundle basename", note)
        self.assertIn("JSON, Markdown, and HTML", note)


if __name__ == "__main__":
    unittest.main()
