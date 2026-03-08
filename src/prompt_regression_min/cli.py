from __future__ import annotations

import argparse
import json
import re
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
    run_cmd.add_argument("-d", "--dataset", required=True, help="Path to dataset JSONL")
    run_cmd.add_argument("-b", "--baseline", required=True, help="Path to baseline outputs JSONL")
    run_cmd.add_argument("-c", "--candidate", required=True, help="Path to candidate outputs JSONL")
    run_cmd.add_argument("-r", "--report", required=False, help="Write full JSON report to file")
    run_cmd.add_argument(
        "--include-id-regex",
        default=None,
        help=(
            "Only evaluate dataset cases whose id matches this regex. "
            "Useful for deterministic shard runs."
        ),
    )
    run_cmd.add_argument(
        "--exclude-id-regex",
        default=None,
        help="Exclude dataset cases whose id matches this regex.",
    )
    run_cmd.add_argument(
        "--max-regressions",
        type=int,
        default=0,
        help="Maximum allowed regressions before failing (default: 0)",
    )
    run_cmd.add_argument(
        "--max-regression-rate",
        type=float,
        default=None,
        help=(
            "Maximum allowed regression rate in range [0.0, 1.0]. "
            "Example: 0.05 allows up to 5% regressed active cases. Disabled by default."
        ),
    )
    run_cmd.add_argument(
        "--min-candidate-pass-rate",
        type=float,
        default=0.0,
        help="Minimum allowed candidate pass rate in range [0.0, 1.0] (default: 0.0)",
    )
    run_cmd.add_argument(
        "--max-unchanged-fail",
        type=int,
        default=-1,
        help=(
            "Maximum allowed unchanged failing cases (baseline fail + candidate fail). "
            "Use -1 to disable this gate (default: -1)"
        ),
    )
    run_cmd.add_argument(
        "--max-unchanged-fail-rate",
        type=float,
        default=None,
        help=(
            "Maximum allowed unchanged failing-case rate in range [0.0, 1.0]. "
            "Example: 0.20 allows at most 20% unchanged failing cases. Disabled by default."
        ),
    )
    run_cmd.add_argument(
        "--forbid-unchanged-fail-id-regex",
        default=None,
        help=(
            "Fail if any unchanged failing case id matches this regex. "
            "Use for critical flows that must not remain broken (e.g., ^auth-|checkout)."
        ),
    )
    run_cmd.add_argument(
        "--summary-json",
        nargs="?",
        const="-",
        default=None,
        help=(
            "Emit machine-readable JSON summary. "
            "Use without value to print JSON to stdout, or pass a file path to write it."
        ),
    )
    run_cmd.add_argument(
        "--summary-json-pretty",
        action="store_true",
        help=(
            "Pretty-print --summary-json payloads with indentation. "
            "Applies to stdout and file output."
        ),
    )
    run_cmd.add_argument(
        "--summary-markdown",
        default=None,
        help=(
            "Write a compact markdown summary to file (for PR comments/release notes). "
            "Use '-' to print markdown to stdout. File paths are always overwritten."
        ),
    )
    run_cmd.add_argument(
        "--summary-markdown-title",
        default="prompt-regression-min summary",
        help=(
            "Heading text used for --summary-markdown output. "
            "Useful for PR comments that need repo- or workflow-specific titles."
        ),
    )
    run_cmd.add_argument(
        "--require-summary-schema-version",
        type=int,
        default=None,
        help=(
            "Fail if the emitted summary schema version does not match this value. "
            "Useful for downstream CI/parser compatibility policies."
        ),
    )
    run_cmd.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress human-readable summary lines; keep machine-readable outputs (e.g., --summary-json).",
    )
    run_cmd.add_argument(
        "--max-skipped-cases",
        type=int,
        default=-1,
        help=(
            "Maximum allowed disabled/skipped dataset cases. "
            "Use -1 to disable this gate (default: -1)."
        ),
    )
    run_cmd.add_argument(
        "--min-delta-pass-rate-pp",
        type=float,
        default=None,
        help=(
            "Minimum allowed candidate-baseline pass-rate delta in percentage points. "
            "Example: 0 means no regression in pass rate, 2.5 means candidate must improve by at least +2.5pp. "
            "Disabled by default."
        ),
    )
    run_cmd.add_argument(
        "--max-delta-pass-rate-pp",
        type=float,
        default=None,
        help=(
            "Maximum allowed candidate-baseline pass-rate delta in percentage points. "
            "Useful to catch unexpectedly large swings. Disabled by default."
        ),
    )
    run_cmd.add_argument(
        "--min-improved",
        type=int,
        default=0,
        help=(
            "Minimum required improved case count (baseline fail + candidate pass). "
            "Default: 0."
        ),
    )
    run_cmd.add_argument(
        "--max-improved",
        type=int,
        default=-1,
        help=(
            "Maximum allowed improved case count (baseline fail + candidate pass). "
            "Use -1 to disable this gate (default: -1)."
        ),
    )
    run_cmd.add_argument(
        "--max-improved-rate",
        type=float,
        default=None,
        help=(
            "Maximum allowed improved-case rate in range [0.0, 1.0]. "
            "Example: 0.10 allows at most 10% improved cases. Disabled by default."
        ),
    )
    run_cmd.add_argument(
        "--max-changed-cases",
        type=int,
        default=-1,
        help=(
            "Maximum allowed changed cases (regressed + improved). "
            "Use -1 to disable this gate (default: -1)."
        ),
    )
    run_cmd.add_argument(
        "--max-changed-rate",
        type=float,
        default=None,
        help=(
            "Maximum allowed changed-case rate in range [0.0, 1.0]. "
            "Example: 0.20 allows at most 20% changed cases. Disabled by default."
        ),
    )
    run_cmd.add_argument(
        "--min-active-cases",
        type=int,
        default=1,
        help=(
            "Minimum required number of active (non-disabled) dataset cases. "
            "Default: 1."
        ),
    )
    run_cmd.add_argument(
        "--max-filtered-out-cases",
        type=int,
        default=-1,
        help=(
            "Maximum allowed regex-filtered-out cases. "
            "Use -1 to disable this gate (default: -1)."
        ),
    )
    run_cmd.add_argument(
        "--max-filtered-out-rate",
        type=float,
        default=None,
        help=(
            "Maximum allowed regex-filtered-out rate in range [0.0, 1.0]. "
            "Computed against original dataset case count before filters. Disabled by default."
        ),
    )
    run_cmd.add_argument(
        "--min-unchanged-pass",
        type=int,
        default=0,
        help=(
            "Minimum required unchanged passing cases (baseline pass + candidate pass). "
            "Default: 0."
        ),
    )
    run_cmd.add_argument(
        "--max-unchanged-pass",
        type=int,
        default=-1,
        help=(
            "Maximum allowed unchanged passing cases (baseline pass + candidate pass). "
            "Use -1 to disable this gate (default: -1)."
        ),
    )
    run_cmd.add_argument(
        "--min-stability-rate",
        type=float,
        default=None,
        help=(
            "Minimum allowed stability rate in range [0.0, 1.0]. "
            "Stability rate = unchanged / active cases. Disabled by default."
        ),
    )
    run_cmd.add_argument(
        "--require-pass-rate-trend",
        choices=("improving", "flat", "regressing"),
        default=None,
        help=(
            "Require summary pass_rate_trend to match this value. "
            "Useful for release gates that allow only improving/flat trends."
        ),
    )

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "run":
        if args.max_regressions < 0:
            print("error: --max-regressions must be >= 0", file=sys.stderr)
            raise SystemExit(2)
        if args.max_regression_rate is not None and not 0.0 <= args.max_regression_rate <= 1.0:
            print("error: --max-regression-rate must be between 0.0 and 1.0", file=sys.stderr)
            raise SystemExit(2)
        if not 0.0 <= args.min_candidate_pass_rate <= 1.0:
            print("error: --min-candidate-pass-rate must be between 0.0 and 1.0", file=sys.stderr)
            raise SystemExit(2)
        if args.max_unchanged_fail < -1:
            print("error: --max-unchanged-fail must be >= -1", file=sys.stderr)
            raise SystemExit(2)
        if args.max_skipped_cases < -1:
            print("error: --max-skipped-cases must be >= -1", file=sys.stderr)
            raise SystemExit(2)
        if args.max_unchanged_fail_rate is not None and not 0.0 <= args.max_unchanged_fail_rate <= 1.0:
            print("error: --max-unchanged-fail-rate must be between 0.0 and 1.0", file=sys.stderr)
            raise SystemExit(2)
        if args.min_delta_pass_rate_pp is not None and not -100.0 <= args.min_delta_pass_rate_pp <= 100.0:
            print("error: --min-delta-pass-rate-pp must be between -100.0 and 100.0", file=sys.stderr)
            raise SystemExit(2)
        if args.max_delta_pass_rate_pp is not None and not -100.0 <= args.max_delta_pass_rate_pp <= 100.0:
            print("error: --max-delta-pass-rate-pp must be between -100.0 and 100.0", file=sys.stderr)
            raise SystemExit(2)
        if args.min_improved < 0:
            print("error: --min-improved must be >= 0", file=sys.stderr)
            raise SystemExit(2)
        if args.max_improved < -1:
            print("error: --max-improved must be >= -1", file=sys.stderr)
            raise SystemExit(2)
        if args.max_improved_rate is not None and not 0.0 <= args.max_improved_rate <= 1.0:
            print("error: --max-improved-rate must be between 0.0 and 1.0", file=sys.stderr)
            raise SystemExit(2)
        if args.max_changed_cases < -1:
            print("error: --max-changed-cases must be >= -1", file=sys.stderr)
            raise SystemExit(2)
        if args.max_changed_rate is not None and not 0.0 <= args.max_changed_rate <= 1.0:
            print("error: --max-changed-rate must be between 0.0 and 1.0", file=sys.stderr)
            raise SystemExit(2)
        if args.min_active_cases < 1:
            print("error: --min-active-cases must be >= 1", file=sys.stderr)
            raise SystemExit(2)
        if args.max_filtered_out_cases < -1:
            print("error: --max-filtered-out-cases must be >= -1", file=sys.stderr)
            raise SystemExit(2)
        if args.max_filtered_out_rate is not None and not 0.0 <= args.max_filtered_out_rate <= 1.0:
            print("error: --max-filtered-out-rate must be between 0.0 and 1.0", file=sys.stderr)
            raise SystemExit(2)
        if args.min_unchanged_pass < 0:
            print("error: --min-unchanged-pass must be >= 0", file=sys.stderr)
            raise SystemExit(2)
        if args.max_unchanged_pass < -1:
            print("error: --max-unchanged-pass must be >= -1", file=sys.stderr)
            raise SystemExit(2)
        if args.min_stability_rate is not None and not 0.0 <= args.min_stability_rate <= 1.0:
            print("error: --min-stability-rate must be between 0.0 and 1.0", file=sys.stderr)
            raise SystemExit(2)

        try:
            if args.include_id_regex is not None:
                re.compile(args.include_id_regex)
            if args.exclude_id_regex is not None:
                re.compile(args.exclude_id_regex)
            if args.forbid_unchanged_fail_id_regex is not None:
                re.compile(args.forbid_unchanged_fail_id_regex)
            report = run_regression(
                args.dataset,
                args.baseline,
                args.candidate,
                include_id_regex=args.include_id_regex,
                exclude_id_regex=args.exclude_id_regex,
            )
        except re.error as exc:
            print(f"error: invalid regex: {exc}", file=sys.stderr)
            raise SystemExit(2)
        except (OSError, ValueError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            raise SystemExit(2)

        summary = report["summary"]

        def emit(line: str) -> None:
            if not args.quiet:
                print(line)

        emit("prompt-regression-min summary")
        emit(f"- cases: {summary['cases']}")
        emit(f"- filtered_out_cases: {summary.get('filtered_out_cases', 0)}")
        emit(f"- filtered_out_rate: {summary.get('filtered_out_rate', 0.0) * 100:.2f}%")
        if summary.get("filtered_out_ids"):
            emit(f"- filtered_out_ids: {', '.join(summary['filtered_out_ids'])}")
        emit(f"- skipped_cases: {summary.get('skipped_cases', 0)}")
        if summary.get("skipped_ids"):
            emit(f"- skipped_ids: {', '.join(summary['skipped_ids'])}")
        emit(
            f"- baseline: {summary['baseline_passes']} "
            f"({summary['baseline_pass_rate'] * 100:.1f}%)"
        )
        emit(
            f"- candidate: {summary['candidate_passes']} "
            f"({summary['candidate_pass_rate'] * 100:.1f}%)"
        )
        emit(
            f"- delta: {summary['delta_passes']} "
            f"({summary['delta_pass_rate_pp']:+.2f}pp)"
        )
        emit(f"- pass_rate_trend: {summary.get('pass_rate_trend', 'flat')}")
        emit(f"- regressions: {summary['regressions']}")
        emit(f"- regression_rate: {summary.get('regression_rate', 0.0) * 100:.2f}%")
        if summary["regression_ids"]:
            emit(f"- regression_ids: {', '.join(summary['regression_ids'])}")
        emit(f"- improved: {summary['improved']}")
        if summary["improved_ids"]:
            emit(f"- improved_ids: {', '.join(summary['improved_ids'])}")
        emit(f"- changed: {summary.get('changed', summary['regressions'] + summary['improved'])}")
        emit(f"- changed_rate: {summary.get('changed_rate', 0.0) * 100:.2f}%")
        emit(f"- unchanged: {summary['unchanged']}")
        emit(f"- stability_rate: {summary.get('stability_rate', 0.0) * 100:.2f}%")
        emit(f"- unchanged_pass: {summary.get('unchanged_pass', 0)}")
        emit(f"- unchanged_fail: {summary.get('unchanged_fail', 0)}")
        emit(f"- unchanged_fail_rate: {summary.get('unchanged_fail_rate', 0.0) * 100:.2f}%")
        if summary.get("unchanged_fail_ids"):
            emit(f"- unchanged_fail_ids: {', '.join(summary['unchanged_fail_ids'])}")
        outcome_counts = summary.get("outcome_counts", {})
        if outcome_counts:
            emit(
                "- outcome_counts: "
                f"regressed={outcome_counts.get('regressed', 0)}, "
                f"improved={outcome_counts.get('improved', 0)}, "
                f"unchanged_pass={outcome_counts.get('unchanged_pass', 0)}, "
                f"unchanged_fail={outcome_counts.get('unchanged_fail', 0)}"
            )

        fail_reasons: list[str] = []
        if summary["regressions"] > args.max_regressions:
            fail_reasons.append(
                f"regressions {summary['regressions']} exceeded max {args.max_regressions}"
            )
        if (
            args.max_regression_rate is not None
            and summary.get("regression_rate", 0.0) > args.max_regression_rate
        ):
            fail_reasons.append(
                "regression rate "
                f"{summary.get('regression_rate', 0.0):.4f} exceeded max {args.max_regression_rate:.4f}"
            )
        summary_schema_version = 1

        if summary["candidate_pass_rate"] < args.min_candidate_pass_rate:
            fail_reasons.append(
                "candidate pass rate "
                f"{summary['candidate_pass_rate']:.4f} below min {args.min_candidate_pass_rate:.4f}"
            )
        unchanged_fail_count = summary.get("outcome_counts", {}).get("unchanged_fail", 0)
        if args.max_unchanged_fail >= 0 and unchanged_fail_count > args.max_unchanged_fail:
            fail_reasons.append(
                f"unchanged failing cases {unchanged_fail_count} exceeded max {args.max_unchanged_fail}"
            )
        unchanged_fail_rate = summary.get("unchanged_fail_rate", 0.0)
        if (
            args.max_unchanged_fail_rate is not None
            and unchanged_fail_rate > args.max_unchanged_fail_rate
        ):
            fail_reasons.append(
                f"unchanged failing-case rate {unchanged_fail_rate:.4f} exceeded max {args.max_unchanged_fail_rate:.4f}"
            )
        if args.forbid_unchanged_fail_id_regex is not None:
            blocked_pattern = re.compile(args.forbid_unchanged_fail_id_regex)
            blocked_ids = [
                case_id for case_id in summary.get("unchanged_fail_ids", []) if blocked_pattern.search(case_id)
            ]
            if blocked_ids:
                fail_reasons.append(
                    "forbidden unchanged failing ids matched regex "
                    f"{args.forbid_unchanged_fail_id_regex}: {', '.join(blocked_ids)}"
                )
        skipped_case_count = summary.get("skipped_cases", 0)
        if args.max_skipped_cases >= 0 and skipped_case_count > args.max_skipped_cases:
            fail_reasons.append(
                f"skipped cases {skipped_case_count} exceeded max {args.max_skipped_cases}"
            )
        if (
            args.min_delta_pass_rate_pp is not None
            and summary["delta_pass_rate_pp"] < args.min_delta_pass_rate_pp
        ):
            fail_reasons.append(
                "pass-rate delta "
                f"{summary['delta_pass_rate_pp']:+.2f}pp below min {args.min_delta_pass_rate_pp:+.2f}pp"
            )
        if (
            args.max_delta_pass_rate_pp is not None
            and summary["delta_pass_rate_pp"] > args.max_delta_pass_rate_pp
        ):
            fail_reasons.append(
                "pass-rate delta "
                f"{summary['delta_pass_rate_pp']:+.2f}pp exceeded max {args.max_delta_pass_rate_pp:+.2f}pp"
            )
        if summary["improved"] < args.min_improved:
            fail_reasons.append(
                f"improved cases {summary['improved']} below min {args.min_improved}"
            )
        if args.max_improved >= 0 and summary["improved"] > args.max_improved:
            fail_reasons.append(
                f"improved cases {summary['improved']} exceeded max {args.max_improved}"
            )
        improved_rate = summary["improved"] / summary["cases"] if summary["cases"] else 0.0
        if args.max_improved_rate is not None and improved_rate > args.max_improved_rate:
            fail_reasons.append(
                f"improved rate {improved_rate:.4f} exceeded max {args.max_improved_rate:.4f}"
            )
        changed_count = summary.get("changed", summary["regressions"] + summary["improved"])
        changed_rate = summary.get("changed_rate", 0.0)
        if args.max_changed_cases >= 0 and changed_count > args.max_changed_cases:
            fail_reasons.append(
                f"changed cases {changed_count} exceeded max {args.max_changed_cases}"
            )
        if args.max_changed_rate is not None and changed_rate > args.max_changed_rate:
            fail_reasons.append(
                f"changed rate {changed_rate:.4f} exceeded max {args.max_changed_rate:.4f}"
            )
        unchanged_pass_count = summary.get("outcome_counts", {}).get("unchanged_pass", 0)
        if unchanged_pass_count < args.min_unchanged_pass:
            fail_reasons.append(
                f"unchanged passing cases {unchanged_pass_count} below min {args.min_unchanged_pass}"
            )
        if args.max_unchanged_pass >= 0 and unchanged_pass_count > args.max_unchanged_pass:
            fail_reasons.append(
                f"unchanged passing cases {unchanged_pass_count} exceeded max {args.max_unchanged_pass}"
            )
        if summary.get("active_cases", summary["cases"]) < args.min_active_cases:
            fail_reasons.append(
                "active cases "
                f"{summary.get('active_cases', summary['cases'])} below min {args.min_active_cases}"
            )
        stability_rate = summary.get("stability_rate", 0.0)
        if args.min_stability_rate is not None and stability_rate < args.min_stability_rate:
            fail_reasons.append(
                f"stability rate {stability_rate:.4f} below min {args.min_stability_rate:.4f}"
            )
        if (
            args.require_pass_rate_trend is not None
            and summary.get("pass_rate_trend") != args.require_pass_rate_trend
        ):
            fail_reasons.append(
                "pass rate trend "
                f"{summary.get('pass_rate_trend', 'unknown')} does not match required {args.require_pass_rate_trend}"
            )
        if (
            args.require_summary_schema_version is not None
            and summary_schema_version != args.require_summary_schema_version
        ):
            fail_reasons.append(
                "summary schema version "
                f"{summary_schema_version} does not match required {args.require_summary_schema_version}"
            )
        filtered_out_case_count = summary.get("filtered_out_cases", 0)
        if args.max_filtered_out_cases >= 0 and filtered_out_case_count > args.max_filtered_out_cases:
            fail_reasons.append(
                f"filtered-out cases {filtered_out_case_count} exceeded max {args.max_filtered_out_cases}"
            )
        filtered_out_rate = summary.get("filtered_out_rate", 0.0)
        if args.max_filtered_out_rate is not None and filtered_out_rate > args.max_filtered_out_rate:
            fail_reasons.append(
                f"filtered-out rate {filtered_out_rate:.4f} exceeded max {args.max_filtered_out_rate:.4f}"
            )

        status = "FAIL" if fail_reasons else "PASS"
        if fail_reasons:
            emit(f"- status: FAIL ({'; '.join(fail_reasons)})")
        else:
            emit("- status: PASS")

        if args.summary_json is not None:
            gates = {
                "max_regressions": args.max_regressions,
                "max_regression_rate": args.max_regression_rate,
                "min_candidate_pass_rate": args.min_candidate_pass_rate,
                "max_unchanged_fail": args.max_unchanged_fail,
                "max_unchanged_fail_rate": args.max_unchanged_fail_rate,
                "forbid_unchanged_fail_id_regex": args.forbid_unchanged_fail_id_regex,
                "max_skipped_cases": args.max_skipped_cases,
                "min_delta_pass_rate_pp": args.min_delta_pass_rate_pp,
                "max_delta_pass_rate_pp": args.max_delta_pass_rate_pp,
                "min_improved": args.min_improved,
                "max_improved": args.max_improved,
                "max_improved_rate": args.max_improved_rate,
                "max_changed_cases": args.max_changed_cases,
                "max_changed_rate": args.max_changed_rate,
                "min_active_cases": args.min_active_cases,
                "max_filtered_out_cases": args.max_filtered_out_cases,
                "max_filtered_out_rate": args.max_filtered_out_rate,
                "min_unchanged_pass": args.min_unchanged_pass,
                "max_unchanged_pass": args.max_unchanged_pass,
                "min_stability_rate": args.min_stability_rate,
                "require_pass_rate_trend": args.require_pass_rate_trend,
                "require_summary_schema_version": args.require_summary_schema_version,
                "include_id_regex": args.include_id_regex,
                "exclude_id_regex": args.exclude_id_regex,
            }
            payload = {
                "status": status,
                "summary_schema_version": summary_schema_version,
                "tool_version": __version__,
                "fail_reasons": fail_reasons,
                "summary": summary,
                "gates": gates,
            }
            json_indent = 2 if args.summary_json_pretty else None
            if args.summary_json == "-":
                print(json.dumps(payload, ensure_ascii=False, indent=json_indent))
            else:
                summary_path = Path(args.summary_json)
                try:
                    summary_path.parent.mkdir(parents=True, exist_ok=True)
                    summary_path.write_text(
                        json.dumps(payload, ensure_ascii=False, indent=json_indent),
                        encoding="utf-8",
                    )
                except OSError as exc:
                    print(
                        f"error: failed to write summary json to {summary_path}: {exc}",
                        file=sys.stderr,
                    )
                    raise SystemExit(2)
                emit(f"- summary_json: {summary_path}")

        if args.summary_markdown:
            markdown_lines = [
                f"## {args.summary_markdown_title}",
                "",
                f"- Tool version: `{__version__}`",
                "- Summary schema version: `1`",
                (
                    f"- Required schema version gate: `{args.require_summary_schema_version}`"
                    if args.require_summary_schema_version is not None
                    else "- Required schema version gate: _not set_"
                ),
                f"- Status: **{status}**",
                (
                    f"- Dataset scope: source={summary.get('dataset_cases', summary['cases'])}, "
                    f"selected={summary.get('selected_dataset_cases', summary['cases'])}, "
                    f"active={summary.get('active_cases', summary['cases'])}"
                ),
                (
                    f"- Cases: {summary['cases']} "
                    f"(active={summary.get('active_cases', summary['cases'])}, "
                    f"skipped={summary.get('skipped_cases', 0)}, "
                    f"filtered_out={summary.get('filtered_out_cases', 0)})"
                ),
                (
                    f"- Pass rate: baseline {summary['baseline_pass_rate'] * 100:.1f}% "
                    f"-> candidate {summary['candidate_pass_rate'] * 100:.1f}% "
                    f"(delta {summary['delta_pass_rate_pp']:+.2f}pp)"
                ),
                f"- Pass-rate trend: `{summary.get('pass_rate_trend', 'flat')}`",
                f"- Stability rate: {summary.get('stability_rate', 0.0) * 100:.2f}%",
                (
                    "- Outcomes: "
                    f"regressions={summary['regressions']}, "
                    f"improved={summary['improved']}, "
                    f"unchanged_pass={summary.get('unchanged_pass', 0)}, "
                    f"unchanged_fail={summary.get('unchanged_fail', 0)}"
                ),
            ]
            regression_ids = summary.get("regression_ids", [])
            improved_ids = summary.get("improved_ids", [])
            markdown_lines.append("- Gate snapshot:")
            gate_lines = [
                f"  - max_regressions={args.max_regressions}",
                (
                    f"  - max_regression_rate={args.max_regression_rate}"
                    if args.max_regression_rate is not None
                    else "  - max_regression_rate=disabled"
                ),
                f"  - min_candidate_pass_rate={args.min_candidate_pass_rate}",
                f"  - max_unchanged_fail={args.max_unchanged_fail}",
                (
                    f"  - max_unchanged_fail_rate={args.max_unchanged_fail_rate}"
                    if args.max_unchanged_fail_rate is not None
                    else "  - max_unchanged_fail_rate=disabled"
                ),
                (
                    f"  - forbid_unchanged_fail_id_regex={args.forbid_unchanged_fail_id_regex}"
                    if args.forbid_unchanged_fail_id_regex is not None
                    else "  - forbid_unchanged_fail_id_regex=disabled"
                ),
                f"  - max_skipped_cases={args.max_skipped_cases}",
                (
                    f"  - max_changed_cases={args.max_changed_cases}"
                    if args.max_changed_cases >= 0
                    else "  - max_changed_cases=disabled"
                ),
                (
                    f"  - max_changed_rate={args.max_changed_rate}"
                    if args.max_changed_rate is not None
                    else "  - max_changed_rate=disabled"
                ),
                (
                    f"  - max_filtered_out_cases={args.max_filtered_out_cases}"
                    if args.max_filtered_out_cases >= 0
                    else "  - max_filtered_out_cases=disabled"
                ),
                (
                    f"  - max_filtered_out_rate={args.max_filtered_out_rate}"
                    if args.max_filtered_out_rate is not None
                    else "  - max_filtered_out_rate=disabled"
                ),
                f"  - min_active_cases={args.min_active_cases}",
                f"  - min_improved={args.min_improved}",
                (
                    f"  - max_improved={args.max_improved}"
                    if args.max_improved >= 0
                    else "  - max_improved=disabled"
                ),
                (
                    f"  - max_improved_rate={args.max_improved_rate}"
                    if args.max_improved_rate is not None
                    else "  - max_improved_rate=disabled"
                ),
                (
                    f"  - min_stability_rate={args.min_stability_rate}"
                    if args.min_stability_rate is not None
                    else "  - min_stability_rate=disabled"
                ),
                (
                    f"  - require_pass_rate_trend={args.require_pass_rate_trend}"
                    if args.require_pass_rate_trend is not None
                    else "  - require_pass_rate_trend=disabled"
                ),
            ]
            markdown_lines.extend(gate_lines)
            if regression_ids:
                markdown_lines.append(
                    "- Regression IDs: " + ", ".join(f"`{case_id}`" for case_id in regression_ids)
                )
            if improved_ids:
                markdown_lines.append(
                    "- Improved IDs: " + ", ".join(f"`{case_id}`" for case_id in improved_ids)
                )
            if args.include_id_regex or args.exclude_id_regex:
                markdown_lines.append(
                    "- Case filters: include="
                    + (f"`{args.include_id_regex}`" if args.include_id_regex else "_all_")
                    + ", exclude="
                    + (f"`{args.exclude_id_regex}`" if args.exclude_id_regex else "_none_")
                )
            if summary.get("changed_ids"):
                markdown_lines.append(
                    "- Changed IDs: " + ", ".join(f"`{case_id}`" for case_id in summary["changed_ids"])
                )
            if summary.get("filtered_out_ids"):
                markdown_lines.append(
                    "- Filtered-out IDs: " + ", ".join(f"`{case_id}`" for case_id in summary["filtered_out_ids"])
                )
            if summary.get("skipped_ids"):
                markdown_lines.append(
                    "- Skipped IDs: " + ", ".join(f"`{case_id}`" for case_id in summary["skipped_ids"])
                )
            if summary.get("unchanged_fail_ids"):
                markdown_lines.append(
                    "- Unchanged fail IDs: " + ", ".join(f"`{case_id}`" for case_id in summary["unchanged_fail_ids"])
                )
            if fail_reasons:
                markdown_lines.append("- Fail reasons:")
                markdown_lines.extend([f"  - {reason}" for reason in fail_reasons])
            markdown_text = "\n".join(markdown_lines) + "\n"
            if args.summary_markdown == "-":
                print(markdown_text, end="")
            else:
                md_path = Path(args.summary_markdown)
                try:
                    md_path.parent.mkdir(parents=True, exist_ok=True)
                    md_path.write_text(markdown_text, encoding="utf-8")
                except OSError as exc:
                    print(f"error: failed to write summary markdown to {md_path}: {exc}", file=sys.stderr)
                    raise SystemExit(2)
                emit(f"- summary_markdown: {md_path}")

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
            emit(f"- report: {report_path}")

        if fail_reasons:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
