from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CliSummaryRepo45PhaseOneGateNoteTests(unittest.TestCase):
    def test_readme_mentions_repo45_phase_one_gate_note(self) -> None:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('docs/CLI_SUMMARY_REPO45_PHASE_ONE_GATE_NOTE.md', readme)

    def test_note_mentions_phase_one_pair_and_validation_gate(self) -> None:
        note = (ROOT / 'docs' / 'CLI_SUMMARY_REPO45_PHASE_ONE_GATE_NOTE.md').read_text(encoding='utf-8')
        self.assertIn('repo 4 and repo 5 visible as the same mandatory pair', note)
        self.assertIn('scenario-file input first', note)
        self.assertIn('validation command stays green', note)


if __name__ == '__main__':
    unittest.main()
