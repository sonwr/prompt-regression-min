from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .core import run_regression


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prm",
        description="Minimal prompt/workflow regression checker",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
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
        try:
            report = run_regression(args.dataset, args.baseline, args.candidate)
        except (OSError, ValueError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            raise SystemExit(2)

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
        print(
            f"- delta: {summary['delta_passes']} "
            f"({summary['delta_pass_rate_pp']:+.2f}pp)"
        )
        print(f"- regressions: {summary['regressions']}")
        print(f"- improved: {summary['improved']}")
        print(f"- unchanged: {summary['unchanged']}")

        if args.report:
            report_path = Path(args.report)
            try:
                report_path.parent.mkdir(parents=True, exist_ok=True)
                report_path.write_text(
                    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
                )
            except OSError as exc:
                print(f"error: failed to write report to {report_path}: {exc}", file=sys.stderr)
                raise SystemExit(2)
            print(f"- report: {report_path}")

        if summary["regressions"] > 0:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
