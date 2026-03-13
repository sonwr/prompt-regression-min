from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


class CliSummaryMarkdownAliasTests(unittest.TestCase):
    def test_cli_accepts_summary_md_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            dataset = tmp / "dataset.jsonl"
            baseline = tmp / "baseline.jsonl"
            candidate = tmp / "candidate.jsonl"
            summary_md = tmp / "summary.md"

            dataset.write_text(json.dumps({"id": "case-1", "expected": {"type": "substring", "value": "ok"}}) + "\n", encoding="utf-8")
            baseline.write_text(json.dumps({"id": "case-1", "output": "ok"}) + "\n", encoding="utf-8")
            candidate.write_text(json.dumps({"id": "case-1", "output": "ok"}) + "\n", encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "prompt_regression_min.cli",
                    "run",
                    "--dataset", str(dataset),
                    "--baseline", str(baseline),
                    "--candidate", str(candidate),
                    "--summary-md", str(summary_md),
                    "--quiet",
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                check=True,
                capture_output=True,
                text=True,
            )

            summary = summary_md.read_text(encoding="utf-8")
            self.assertIn("## prompt-regression-min summary", summary)
            self.assertIn("- Status: **PASS**", summary)


if __name__ == "__main__":
    unittest.main()
