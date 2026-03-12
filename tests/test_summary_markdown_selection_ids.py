from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SummaryMarkdownSelectionIdsTests(unittest.TestCase):
    def test_markdown_summary_lists_skipped_and_filtered_out_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            dataset = Path(tmpdir) / "dataset.jsonl"
            baseline = Path(tmpdir) / "baseline.jsonl"
            candidate = Path(tmpdir) / "candidate.jsonl"
            summary_md = Path(tmpdir) / "summary.md"
            dataset.write_text(
                """{"id":"auth-keep","input":"a","expected":{"type":"substring","value":"ok"}}
{"id":"billing-out","input":"b","expected":{"type":"substring","value":"ok"}}
{"id":"ops-skip","input":"c","disabled":true,"expected":{"type":"substring","value":"ok"}}
""",
                encoding="utf-8",
            )
            baseline.write_text(
                """{"id":"auth-keep","output":"ok"}
{"id":"billing-out","output":"ok"}
{"id":"ops-skip","output":"ok"}
""",
                encoding="utf-8",
            )
            candidate.write_text(
                """{"id":"auth-keep","output":"ok"}
{"id":"billing-out","output":"ok"}
{"id":"ops-skip","output":"ok"}
""",
                encoding="utf-8",
            )
            env = os.environ.copy()
            env["PYTHONPATH"] = str(ROOT / "src")
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "prompt_regression_min",
                    "run",
                    "-d",
                    str(dataset),
                    "-b",
                    str(baseline),
                    "-c",
                    str(candidate),
                    "--exclude-id-regex",
                    "^billing-",
                    "--summary-markdown",
                    str(summary_md),
                    "--quiet",
                ],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            rendered = summary_md.read_text(encoding="utf-8")
            self.assertIn('- Skipped IDs (1): `ops-skip`', rendered)
            self.assertIn('- Filtered-out IDs (1): `billing-out`', rendered)


if __name__ == "__main__":
    unittest.main()
