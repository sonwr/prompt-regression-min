from __future__ import annotations

from pathlib import Path
import unittest


class ReadmeReviewerQueueOwnerEscalationCardTests(unittest.TestCase):
    def test_readme_mentions_owner_escalation_card_example(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("examples/reviewer_queue_owner_escalation_card.md", readme)
        self.assertTrue((root / "examples" / "reviewer_queue_owner_escalation_card.md").exists())


if __name__ == "__main__":
    unittest.main()
