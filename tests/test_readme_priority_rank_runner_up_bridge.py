from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"


class ReadmePriorityRankRunnerUpBridgeTests(unittest.TestCase):
    def test_readme_mentions_priority_rank_runner_up_bridge_example(self) -> None:
        readme = README_PATH.read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_priority_rank_runner_up_bridge.md", readme)
        self.assertTrue((ROOT / "examples" / "reviewer_queue_priority_rank_runner_up_bridge.md").exists())


if __name__ == "__main__":
    unittest.main()
