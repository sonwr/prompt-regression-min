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


class CliSummaryReviewMarkdownAliasTests(unittest.TestCase):
    def test_cli_accepts_summary_review_markdown_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            dataset = tmp / "dataset.jsonl"
            baseline = tmp / "baseline.jsonl"
            candidate = tmp / "candidate.jsonl"
            summary_md = tmp / "summary-review.md"

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
                    "--summary-review-markdown", str(summary_md),
                ],
                cwd=ROOT,
                env={**os.environ, "PYTHONPATH": str(SRC)},
                capture_output=True,
                text=True,
                check=True,
            )

            self.assertTrue(summary_md.exists())
            self.assertIn("prompt-regression-min summary", summary_md.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
