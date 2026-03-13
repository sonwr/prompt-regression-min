from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ReadmeSummaryRepo45PhaseOneProposalPrecedenceNoteTests(unittest.TestCase):
    def test_readme_mentions_repo45_phase_one_proposal_precedence_note(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("docs/CLI_SUMMARY_REPO45_PHASE_ONE_PROPOSAL_PRECEDENCE_NOTE.md", readme)
        self.assertTrue((ROOT / "docs" / "CLI_SUMMARY_REPO45_PHASE_ONE_PROPOSAL_PRECEDENCE_NOTE.md").exists())


if __name__ == "__main__":
    unittest.main()
