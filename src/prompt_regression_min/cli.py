from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import run_regression


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prm",
        description="Minimal prompt/workflow regression checker",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run_cmd = sub.add_parser("run", help="Run regression check")
    run_cmd.add_argument("--dataset", required=True, help="Path to dataset JSONL")
    run_cmd.add_argument("--baseline", required=True, help="Path to baseline outputs JSONL")
    run_cmd.add_argument("--candidate", required=True, help="Path to candidate outputs JSONL")
    run_cmd.add_argument("--report", required=False, help="Write full JSON report to file")

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "run":
        report = run_regression(args.dataset, args.baseline, args.candidate)
        summary = report["summary"]

        print("prompt-regression-min summary")
        print(f"- cases: {summary['cases']}")
        print(
            f"- baseline: {summary['baseline_passes']} "
            f"({summary['baseline_pass_rate'] * 100:.1f}%)"
        )
        print(
            f"- candidate: {summary['candidate_passes']} "
            f"({summary['candidate_pass_rate'] * 100:.1f}%)"
        )
        print(f"- regressions: {summary['regressions']}")
        print(f"- improved: {summary['improved']}")
        print(f"- unchanged: {summary['unchanged']}")

        if args.report:
            report_path = Path(args.report)
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"- report: {report_path}")

        if summary["regressions"] > 0:
            raise SystemExit(1)
