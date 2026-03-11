from __future__ import annotations

from pathlib import Path
import unittest


class ReadmeSummaryPrCommentStdoutNoteTests(unittest.TestCase):
    def test_readme_keeps_summary_pr_comment_stdout_note(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("--summary-pr-comment -", readme)
        self.assertIn("examples/ci_pr_comment_stdout.md", readme)
        self.assertTrue((root / "examples" / "ci_pr_comment_stdout.md").exists())


if __name__ == "__main__":
    unittest.main()
