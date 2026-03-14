import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / 'examples' / 'dataset' / 'walkthrough_pass_artifact_demo.jsonl'
BASELINE = ROOT / 'examples' / 'outputs' / 'walkthrough_pass_artifact_demo.baseline.jsonl'
CANDIDATE = ROOT / 'examples' / 'outputs' / 'walkthrough_pass_artifact_demo.candidate.jsonl'
CLI = [sys.executable, '-m', 'prompt_regression_min.cli', 'run']


class CliSummaryQueueMdAliasTests(unittest.TestCase):
    def test_cli_accepts_summary_queue_md_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / 'queue.md'
            completed = subprocess.run(
                CLI
                + [
                    '--dataset', str(DATASET),
                    '--baseline', str(BASELINE),
                    '--candidate', str(CANDIDATE),
                    '--summary-queue-md', str(output_path),
                ],
                cwd=ROOT,
                env={'PYTHONPATH': 'src'},
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertEqual(completed.returncode, 0)
            self.assertTrue(output_path.exists())
            text = output_path.read_text(encoding='utf-8')
            self.assertIn('prompt-regression-min summary', text)
            self.assertIn('Coverage watch', text)


if __name__ == '__main__':
    unittest.main()
