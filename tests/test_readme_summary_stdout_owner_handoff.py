from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReadmeSummaryStdoutOwnerHandoffTests(unittest.TestCase):
    def test_readme_mentions_summary_stdout_owner_handoff(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/summary_stdout_owner_handoff.md", readme)
        self.assertTrue((ROOT / "examples" / "summary_stdout_owner_handoff.md").exists())


if __name__ == "__main__":
    unittest.main()
