from __future__ import annotations

from pathlib import Path
import unittest


class ReadmeSummaryJsonAndPrCommentHandoffTests(unittest.TestCase):
    def test_readme_keeps_summary_json_and_pr_comment_handoff_example(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/summary_json_and_pr_comment_handoff.md", readme)
        self.assertTrue((root / "examples" / "summary_json_and_pr_comment_handoff.md").exists())


if __name__ == "__main__":
    unittest.main()
