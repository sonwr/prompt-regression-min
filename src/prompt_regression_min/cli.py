from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from . import __version__
from .core import run_regression


def _build_reviewer_queue(summary: dict[str, object]) -> dict[str, object]:
    active_cases = int(summary.get("active_cases", summary.get("cases", 0)) or 0)
    dataset_cases = int(summary.get("dataset_cases", summary.get("cases", active_cases)) or 0)
    groups: list[dict[str, object]] = []
    total = 0
    queue_specs = [
        ("fix_regressions", "fix regressions", list(summary.get("regression_ids", []))),
        ("watch_unchanged_fails", "watch unchanged fails", list(summary.get("unchanged_fail_ids", []))),
        ("confirm_filtered_scope", "confirm filtered-out scope", list(summary.get("filtered_out_ids", []))),
        ("resolve_skipped_cases", "resolve skipped cases", list(summary.get("skipped_ids", []))),
    ]
    queue_priority_index = {key: idx for idx, (key, _, _) in enumerate(queue_specs)}
    for key, label, ids in queue_specs:
        if not ids:
            continue
        count = len(ids)
        group_rate = (count / active_cases) if active_cases else 0.0
        group_source_case_rate = (count / dataset_cases) if dataset_cases else 0.0
        groups.append({
            "key": key,
            "label": label,
            "ids": ids,
            "count": count,
            "rate": round(group_rate, 4),
            "source_case_rate": round(group_source_case_rate, 4),
        })
        total += len(ids)
    for group in groups:
        count = int(group["count"])
        group["queue_share"] = 0.0 if total == 0 else round(count / total, 4)
    rate = (total / active_cases) if active_cases else 0.0
    source_case_rate = (total / dataset_cases) if dataset_cases else 0.0
    largest_group = max(groups, key=lambda item: (int(item["count"]), item["key"]), default=None)
    follow_up_priority = [
        str(group["key"])
        for group in sorted(
            groups,
            key=lambda item: (-int(item["count"]), queue_priority_index[str(item["key"])]),
        )
    ]
    follow_up_priority_ranks = {
        key: idx for idx, key in enumerate(follow_up_priority, start=1)
    }
    largest_group_priority_rank = (
        None
        if largest_group is None
        else follow_up_priority.index(str(largest_group["key"])) + 1
    )
    largest_group_keys = [
        str(group["key"])
        for group in groups
        if largest_group is not None and int(group["count"]) == int(largest_group["count"])
    ]
    largest_group_labels = [
        str(group["label"])
        for group in groups
        if largest_group is not None and int(group["count"]) == int(largest_group["count"])
    ]
    return {
        "total": total,
        "rate": round(rate, 4),
        "source_case_rate": round(source_case_rate, 4),
        "active_cases": active_cases,
        "dataset_cases": dataset_cases,
        "groups": groups,
        "group_count": len(groups),
        "group_keys": [str(group["key"]) for group in groups],
        "group_labels": [str(group["label"]) for group in groups],
        "follow_up_priority": follow_up_priority,
        "follow_up_priority_ranks": follow_up_priority_ranks,
        "largest_group_priority_rank": largest_group_priority_rank,
        "largest_group_keys": largest_group_keys,
        "largest_group_labels": largest_group_labels,
        "largest_group_tie_count": len(largest_group_keys),
        "largest_group_has_ties": len(largest_group_keys) > 1,
        "largest_group_key": None if largest_group is None else largest_group["key"],
        "largest_group_label": None if largest_group is None else largest_group["label"],
        "largest_group_ids": [] if largest_group is None else list(largest_group["ids"]),
        "largest_group_count": 0 if largest_group is None else int(largest_group["count"]),
        "largest_group_rate": 0.0 if largest_group is None else float(largest_group["rate"]),
        "largest_group_source_case_rate": 0.0 if largest_group is None else float(largest_group["source_case_rate"]),
        "largest_group_queue_share": 0.0 if largest_group is None or total == 0 else round(float(largest_group["count"]) / total, 4),
    }


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
            "Useful for repo- or workflow-specific markdown handoff titles."
        ),
    )
    run_cmd.add_argument(
        "--summary-pr-comment",
        default=None,
        help=(
            "Write a compact reviewer-note markdown snapshot to file (for PR comments). "
            "Use '-' to print the PR-comment snapshot to stdout. File paths are always overwritten."
        ),
    )
    run_cmd.add_argument(
        "--summary-pr-comment-title",
        default="prompt-regression-min summary",
        help=(
            "Heading text used for --summary-pr-comment output. "
            "Lets reviewer-note snapshots use a different title than --summary-markdown."
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
                "reviewer_queue": _build_reviewer_queue(summary),
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

        regression_ids = summary.get("regression_ids", [])
        improved_ids = summary.get("improved_ids", [])

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
                f"- Selection rate: {summary.get('selection_rate', 1.0) * 100:.2f}% of source cases",
                f"- Active-case rate: {(summary.get('active_cases', summary['cases']) / summary.get('dataset_cases', summary['cases']) * 100 if summary.get('dataset_cases', summary['cases']) else 0.0):.2f}% of source cases",
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
                f"- Regression rate: {summary.get('regression_rate', 0.0) * 100:.2f}% of active cases",
                f"- Improvement rate: {(summary.get('improved', 0) / summary.get('active_cases', summary['cases']) * 100 if summary.get('active_cases', summary['cases']) else 0.0):.2f}% of active cases",
                (
                    f"- Regression budget usage: {summary['regressions']}/{args.max_regressions} "
                    f"({(summary.get('regression_rate', 0.0) * 100):.2f}% active-case rate)"
                ),
                (
                    f"- Changed-case budget usage: {summary.get('changed', summary['regressions'] + summary.get('improved', 0))}/"
                    + (str(args.max_changed_cases) if args.max_changed_cases >= 0 else "disabled")
                    + f" ({summary.get('changed_rate', 0.0) * 100:.2f}% active-case rate)"
                ),
                (
                    f"- Unchanged-fail budget usage: {summary.get('unchanged_fail', 0)}/"
                    + (str(args.max_unchanged_fail) if args.max_unchanged_fail >= 0 else "disabled")
                    + f" ({summary.get('unchanged_fail_rate', 0.0) * 100:.2f}% active-case rate)"
                ),
                (
                    f"- Skipped-case budget usage: {summary.get('skipped_cases', 0)}/"
                    + (str(args.max_skipped_cases) if args.max_skipped_cases >= 0 else "disabled")
                    + f" ({(summary.get('skipped_cases', 0) / summary.get('dataset_cases', summary['cases']) * 100 if summary.get('dataset_cases', summary['cases']) else 0.0):.2f}% source-case rate)"
                ),
                (
                    f"- Filtered-out budget usage: {summary.get('filtered_out_cases', 0)}/"
                    + (str(args.max_filtered_out_cases) if args.max_filtered_out_cases >= 0 else "disabled")
                    + f" ({summary.get('filtered_out_rate', 0.0) * 100:.2f}% source-case rate)"
                ),
                (
                    "- Reviewer handoff: "
                    f"stable={summary.get('unchanged_pass', 0)}, "
                    f"regressions={summary['regressions']}, "
                    f"improved={summary['improved']}, "
                    f"watchlist={summary.get('unchanged_fail', 0)}"
                ),
                (
                    "- Coverage watch: "
                    f"selected={summary.get('selected_dataset_cases', summary['cases'])}, "
                    f"active={summary.get('active_cases', summary['cases'])}, "
                    f"skipped={summary.get('skipped_cases', 0)}, "
                    f"filtered_out={summary.get('filtered_out_cases', 0)}"
                ),
            ]
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
                    f"  - min_delta_pass_rate_pp={args.min_delta_pass_rate_pp}"
                    if args.min_delta_pass_rate_pp is not None
                    else "  - min_delta_pass_rate_pp=disabled"
                ),
                (
                    f"  - max_delta_pass_rate_pp={args.max_delta_pass_rate_pp}"
                    if args.max_delta_pass_rate_pp is not None
                    else "  - max_delta_pass_rate_pp=disabled"
                ),
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
                    f"  - min_unchanged_pass={args.min_unchanged_pass}"
                ),
                (
                    f"  - max_unchanged_pass={args.max_unchanged_pass}"
                    if args.max_unchanged_pass >= 0
                    else "  - max_unchanged_pass=disabled"
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
                (
                    f"  - require_summary_schema_version={args.require_summary_schema_version}"
                    if args.require_summary_schema_version is not None
                    else "  - require_summary_schema_version=disabled"
                ),
            ]
            markdown_lines.extend(gate_lines)
            if summary.get("selected_dataset_ids"):
                markdown_lines.append(
                    "- Selected dataset IDs: "
                    + ", ".join(f"`{case_id}`" for case_id in summary["selected_dataset_ids"])
                )
            if summary.get("active_case_ids"):
                markdown_lines.append(
                    "- Active case IDs: "
                    + ", ".join(f"`{case_id}`" for case_id in summary["active_case_ids"])
                )
            if regression_ids:
                markdown_lines.append(
                    f"- Regression IDs ({len(regression_ids)}): " + ", ".join(f"`{case_id}`" for case_id in regression_ids)
                )
                markdown_lines.append(
                    f"- Regression source-case rate: {(len(regression_ids) / summary.get('dataset_cases', summary['cases'])) * 100:.2f}% of source cases"
                )
            if improved_ids:
                markdown_lines.append(
                    f"- Improved IDs ({len(improved_ids)}): " + ", ".join(f"`{case_id}`" for case_id in improved_ids)
                )
                markdown_lines.append(
                    f"- Improvement source-case rate: {(len(improved_ids) / summary.get('dataset_cases', summary['cases'])) * 100:.2f}% of source cases"
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
                    f"- Changed IDs ({len(summary['changed_ids'])}): " + ", ".join(f"`{case_id}`" for case_id in summary["changed_ids"])
                )
                markdown_lines.append(
                    f"- Changed-case rate: {summary.get('changed_rate', 0.0) * 100:.2f}%"
                )
                markdown_lines.append(
                    f"- Changed source-case rate: {(len(summary['changed_ids']) / summary.get('dataset_cases', summary['cases'])) * 100:.2f}% of source cases"
                )
            if summary.get("filtered_out_ids"):
                markdown_lines.append(
                    f"- Filtered-out IDs ({len(summary['filtered_out_ids'])}): " + ", ".join(f"`{case_id}`" for case_id in summary["filtered_out_ids"])
                )
                markdown_lines.append(
                    f"- Filtered-out rate: {summary.get('filtered_out_rate', 0.0) * 100:.2f}% of source cases"
                )
                markdown_lines.append(
                    f"- Scope reduction: {summary.get('filtered_out_rate', 0.0) * 100:.2f}% of source cases removed by filters"
                )
            if summary.get("skipped_ids"):
                markdown_lines.append(
                    f"- Skipped IDs ({len(summary['skipped_ids'])}): " + ", ".join(f"`{case_id}`" for case_id in summary["skipped_ids"])
                )
                markdown_lines.append(
                    f"- Skipped-case rate: {summary.get('skipped_rate', 0.0) * 100:.2f}% of active cases"
                )
                markdown_lines.append(
                    f"- Skipped source-case rate: {(len(summary['skipped_ids']) / summary.get('dataset_cases', summary['cases'])) * 100:.2f}% of source cases"
                )
            if summary.get("unchanged_pass_ids"):
                markdown_lines.append(
                    f"- Unchanged pass IDs ({len(summary['unchanged_pass_ids'])}): " + ", ".join(f"`{case_id}`" for case_id in summary["unchanged_pass_ids"])
                )
            if summary.get("unchanged_fail_ids"):
                markdown_lines.append(
                    f"- Unchanged fail IDs ({len(summary['unchanged_fail_ids'])}): " + ", ".join(f"`{case_id}`" for case_id in summary["unchanged_fail_ids"])
                )
            review_queue = []
            reviewer_queue_total = 0
            if regression_ids:
                review_queue.append("fix regressions: " + ", ".join(f"`{case_id}`" for case_id in regression_ids))
                reviewer_queue_total += len(regression_ids)
            if summary.get("unchanged_fail_ids"):
                review_queue.append("watch unchanged fails: " + ", ".join(f"`{case_id}`" for case_id in summary["unchanged_fail_ids"]))
                reviewer_queue_total += len(summary["unchanged_fail_ids"])
            if summary.get("filtered_out_ids"):
                review_queue.append("confirm filtered-out scope: " + ", ".join(f"`{case_id}`" for case_id in summary["filtered_out_ids"]))
                reviewer_queue_total += len(summary["filtered_out_ids"])
            if summary.get("skipped_ids"):
                review_queue.append("resolve skipped cases: " + ", ".join(f"`{case_id}`" for case_id in summary["skipped_ids"]))
                reviewer_queue_total += len(summary["skipped_ids"])
            if review_queue:
                reviewer_queue_summary = _build_reviewer_queue(summary)
                markdown_lines.append(f"- Reviewer queue total: {reviewer_queue_total} case(s)")
                markdown_lines.append(
                    f"- Reviewer queue groups: {reviewer_queue_summary.get('group_count', 0)}"
                )
                if reviewer_queue_summary.get("group_keys"):
                    markdown_lines.append(
                        "- Reviewer queue group keys: "
                        + ", ".join(str(key) for key in reviewer_queue_summary["group_keys"])
                    )
                if reviewer_queue_summary.get("group_labels"):
                    markdown_lines.append(
                        "- Reviewer queue group labels: "
                        + ", ".join(str(label) for label in reviewer_queue_summary["group_labels"])
                    )
                markdown_lines.append(
                    f"- Reviewer queue rate: {(reviewer_queue_total / summary.get('active_cases', summary['cases'])) * 100:.2f}% of active cases"
                )
                markdown_lines.append(
                    f"- Reviewer queue source-case rate: {(reviewer_queue_total / summary.get('dataset_cases', summary['cases'])) * 100:.2f}% of source cases"
                )
                markdown_lines.append(
                    "- Reviewer queue largest group: "
                    f"{reviewer_queue_summary.get('largest_group_key') or 'none'} "
                    f"({reviewer_queue_summary.get('largest_group_count', 0)} case(s), "
                    f"{reviewer_queue_summary.get('largest_group_rate', 0.0) * 100:.2f}% of active cases, "
                    f"{reviewer_queue_summary.get('rate', 0.0) * 100:.2f}% overall queue rate, "
                    f"{reviewer_queue_summary.get('largest_group_source_case_rate', 0.0) * 100:.2f}% source-case rate, "
                    f"{reviewer_queue_summary.get('largest_group_queue_share', 0.0) * 100:.2f}% of queued follow-up)"
                )
                dominant_label_map = {
                    "fix_regressions": "fix regressions",
                    "watch_unchanged_fails": "watch unchanged fails",
                    "confirm_filtered_scope": "confirm filtered-out scope",
                    "resolve_skipped_cases": "resolve skipped cases",
                }
                dominant_key = reviewer_queue_summary.get('largest_group_key')
                dominant_label = reviewer_queue_summary.get('largest_group_label')
                if dominant_label:
                    markdown_lines.append(
                        "- Reviewer queue largest group label: " + dominant_label
                    )
                if dominant_key:
                    markdown_lines.append(
                        "- Reviewer queue dominant focus: "
                        + dominant_label_map.get(dominant_key, dominant_key)
                    )
                if reviewer_queue_summary.get("follow_up_priority"):
                    markdown_lines.append(
                        "- Reviewer queue follow-up priority: "
                        + " -> ".join(str(key) for key in reviewer_queue_summary["follow_up_priority"])
                    )
                    markdown_lines.append(
                        "- Reviewer queue follow-up labels: "
                        + " -> ".join(
                            dominant_label_map.get(str(key), str(key))
                            for key in reviewer_queue_summary["follow_up_priority"]
                        )
                    )
                    if reviewer_queue_summary.get("follow_up_priority_ranks"):
                        markdown_lines.append(
                            "- Reviewer queue priority ranks: "
                            + ", ".join(
                                f"{key}=P{reviewer_queue_summary['follow_up_priority_ranks'][str(key)]}"
                                for key in reviewer_queue_summary["follow_up_priority"]
                            )
                        )
                if reviewer_queue_summary.get("largest_group_priority_rank") is not None:
                    markdown_lines.append(
                        f"- Reviewer queue next-focus priority rank: {reviewer_queue_summary.get('largest_group_priority_rank')} of {len(reviewer_queue_summary.get('follow_up_priority', []))}"
                    )
                if reviewer_queue_summary.get("largest_group_keys"):
                    markdown_lines.append(
                        "- Reviewer queue tied largest groups: "
                        + ", ".join(str(key) for key in reviewer_queue_summary["largest_group_keys"])
                    )
                    markdown_lines.append(
                        f"- Reviewer queue largest-group tie count: {reviewer_queue_summary.get('largest_group_tie_count', 0)}"
                    )
                if reviewer_queue_summary.get("largest_group_labels"):
                    markdown_lines.append(
                        "- Reviewer queue tied largest labels: "
                        + ", ".join(str(label) for label in reviewer_queue_summary["largest_group_labels"])
                    )
                if reviewer_queue_summary.get("largest_group_ids"):
                    markdown_lines.append(
                        "- Reviewer queue largest group IDs: "
                        + ", ".join(
                            f"`{case_id}`" for case_id in reviewer_queue_summary["largest_group_ids"]
                        )
                    )
                    if dominant_label:
                        markdown_lines.append(
                            "- Reviewer queue next-focus label: " + dominant_label
                        )
                    markdown_lines.append(
                        "- Reviewer queue next focus: "
                        + f"{reviewer_queue_summary.get('largest_group_key')}: "
                        + ", ".join(
                            f"`{case_id}`" for case_id in reviewer_queue_summary["largest_group_ids"]
                        )
                    )
                    markdown_lines.append(
                        f"- Reviewer queue next-focus case count: {reviewer_queue_summary.get('largest_group_count', 0)}"
                    )
                    markdown_lines.append(
                        f"- Reviewer queue next-focus active-case rate: {reviewer_queue_summary.get('largest_group_rate', 0.0) * 100:.2f}% of active cases"
                    )
                    markdown_lines.append(
                        f"- Reviewer queue next-focus source-case rate: {reviewer_queue_summary.get('largest_group_source_case_rate', 0.0) * 100:.2f}% of source cases"
                    )
                    markdown_lines.append(
                        f"- Reviewer queue next-focus queue share: {reviewer_queue_summary.get('largest_group_queue_share', 0.0) * 100:.2f}% of queued follow-up"
                    )
                markdown_lines.append("- Reviewer queue: " + " | ".join(review_queue))
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

        if args.summary_pr_comment:
            pr_comment_lines = [
                f"## {args.summary_pr_comment_title}",
                f"- Status: **{status}**",
                "- Summary schema version: `1`",
                f"- Tool version: `{__version__}`",
                (
                    f"- Required schema version gate: `{args.require_summary_schema_version}`"
                    if args.require_summary_schema_version is not None
                    else "- Required schema version gate: _disabled_"
                ),
                f"- Pass-rate trend: `{summary.get('pass_rate_trend', 'flat')}`",
                (
                    f"- Coverage watch: selected={summary.get('selected_dataset_cases', summary['cases'])}, "
                    f"active={summary.get('active_cases', summary['cases'])}, "
                    f"skipped={summary.get('skipped_cases', 0)}, "
                    f"filtered_out={summary.get('filtered_out_cases', 0)}"
                ),
                f"- Selection rate: {summary.get('selection_rate', 1.0) * 100:.2f}% of source cases",
                f"- Active-case rate: {summary.get('active_case_rate', 1.0) * 100:.2f}% of source cases",
            ]
            if args.include_id_regex or args.exclude_id_regex:
                pr_comment_lines.append(
                    "- Case filters: include="
                    + (f"`{args.include_id_regex}`" if args.include_id_regex else "_all_")
                    + ", exclude="
                    + (f"`{args.exclude_id_regex}`" if args.exclude_id_regex else "_none_")
                )
            if regression_ids:
                pr_comment_lines.append(
                    f"- Regression IDs ({len(regression_ids)}): " + ", ".join(f"`{case_id}`" for case_id in regression_ids)
                )
                pr_comment_lines.append(
                    f"- Regression rate: {(len(regression_ids) / summary.get('active_cases', summary['cases'])) * 100:.2f}% of active cases"
                )
                pr_comment_lines.append(
                    f"- Regression source-case rate: {(len(regression_ids) / summary.get('dataset_cases', summary['cases'])) * 100:.2f}% of source cases"
                )
            if improved_ids:
                pr_comment_lines.append(
                    f"- Improved IDs ({len(improved_ids)}): " + ", ".join(f"`{case_id}`" for case_id in improved_ids)
                )
                pr_comment_lines.append(
                    f"- Improvement rate: {(len(improved_ids) / summary.get('active_cases', summary['cases'])) * 100:.2f}% of active cases"
                )
                pr_comment_lines.append(
                    f"- Improvement source-case rate: {(len(improved_ids) / summary.get('dataset_cases', summary['cases'])) * 100:.2f}% of source cases"
                )
            if summary.get("changed_ids"):
                pr_comment_lines.append(
                    f"- Changed IDs ({len(summary['changed_ids'])}): " + ", ".join(f"`{case_id}`" for case_id in summary["changed_ids"])
                )
                pr_comment_lines.append(
                    f"- Changed-case rate: {summary.get('changed_rate', 0.0) * 100:.2f}% of active cases"
                )
                pr_comment_lines.append(
                    f"- Changed source-case rate: {(len(summary['changed_ids']) / summary.get('dataset_cases', summary['cases'])) * 100:.2f}% of source cases"
                )
            if summary.get("unchanged_pass_ids"):
                pr_comment_lines.append(
                    "- Stable IDs: " + ", ".join(f"`{case_id}`" for case_id in summary["unchanged_pass_ids"])
                )
                pr_comment_lines.append(
                    f"- Stable-case rate: {(len(summary['unchanged_pass_ids']) / summary.get('active_cases', summary['cases'])) * 100:.2f}% of active cases"
                )
                pr_comment_lines.append(
                    f"- Stable source-case rate: {(len(summary['unchanged_pass_ids']) / summary.get('dataset_cases', summary['cases'])) * 100:.2f}% of source cases"
                )
            if summary.get("unchanged_fail_ids"):
                pr_comment_lines.append(
                    "- Unchanged fail IDs: " + ", ".join(f"`{case_id}`" for case_id in summary["unchanged_fail_ids"])
                )
                pr_comment_lines.append(
                    f"- Watchlist rate: {summary.get('unchanged_fail_rate', 0.0) * 100:.2f}% of active cases"
                )
                pr_comment_lines.append(
                    f"- Watchlist source-case rate: {(len(summary['unchanged_fail_ids']) / summary.get('dataset_cases', summary['cases'])) * 100:.2f}% of source cases"
                )
            if summary.get("filtered_out_ids"):
                pr_comment_lines.append(
                    "- Filtered-out IDs: " + ", ".join(f"`{case_id}`" for case_id in summary["filtered_out_ids"])
                )
                pr_comment_lines.append(
                    f"- Filtered-out rate: {summary.get('filtered_out_rate', 0.0) * 100:.2f}% of source cases"
                )
            if summary.get("skipped_ids"):
                pr_comment_lines.append(
                    "- Skipped IDs: " + ", ".join(f"`{case_id}`" for case_id in summary["skipped_ids"])
                )
                pr_comment_lines.append(
                    f"- Skipped-case rate: {summary.get('skipped_rate', 0.0) * 100:.2f}% of active cases"
                )
                pr_comment_lines.append(
                    f"- Skipped source-case rate: {(len(summary['skipped_ids']) / summary.get('dataset_cases', summary['cases'])) * 100:.2f}% of source cases"
                )
            reviewer_queue = []
            reviewer_queue_total = 0
            if regression_ids:
                reviewer_queue.append("fix regressions: " + ", ".join(f"`{case_id}`" for case_id in regression_ids))
                reviewer_queue_total += len(regression_ids)
            if summary.get("unchanged_fail_ids"):
                reviewer_queue.append("watch unchanged fails: " + ", ".join(f"`{case_id}`" for case_id in summary["unchanged_fail_ids"]))
                reviewer_queue_total += len(summary["unchanged_fail_ids"])
            if summary.get("filtered_out_ids"):
                reviewer_queue.append("confirm filtered-out scope: " + ", ".join(f"`{case_id}`" for case_id in summary["filtered_out_ids"]))
                reviewer_queue_total += len(summary["filtered_out_ids"])
            if summary.get("skipped_ids"):
                reviewer_queue.append("resolve skipped cases: " + ", ".join(f"`{case_id}`" for case_id in summary["skipped_ids"]))
                reviewer_queue_total += len(summary["skipped_ids"])
            if reviewer_queue:
                active_cases = summary.get('active_cases', summary['cases'])
                reviewer_queue_summary = _build_reviewer_queue(summary)
                pr_comment_lines.append(f"- Reviewer queue total: {reviewer_queue_total} case(s)")
                pr_comment_lines.append(
                    f"- Reviewer queue groups: {reviewer_queue_summary.get('group_count', 0)}"
                )
                if reviewer_queue_summary.get("group_keys"):
                    pr_comment_lines.append(
                        "- Reviewer queue group keys: "
                        + ", ".join(str(key) for key in reviewer_queue_summary["group_keys"])
                    )
                if reviewer_queue_summary.get("group_labels"):
                    pr_comment_lines.append(
                        "- Reviewer queue group labels: "
                        + ", ".join(str(label) for label in reviewer_queue_summary["group_labels"])
                    )
                pr_comment_lines.append(
                    f"- Reviewer queue rate: {(reviewer_queue_total / active_cases) * 100:.2f}% of active cases"
                )
                pr_comment_lines.append(
                    f"- Reviewer queue source-case rate: {(reviewer_queue_total / summary.get('dataset_cases', summary['cases'])) * 100:.2f}% of source cases"
                )
                pr_comment_lines.append(
                    "- Reviewer queue largest group: "
                    f"{reviewer_queue_summary.get('largest_group_key') or 'none'} "
                    f"({reviewer_queue_summary.get('largest_group_count', 0)} case(s), "
                    f"{reviewer_queue_summary.get('largest_group_rate', 0.0) * 100:.2f}% of active cases, "
                    f"{reviewer_queue_summary.get('rate', 0.0) * 100:.2f}% overall queue rate, "
                    f"{reviewer_queue_summary.get('largest_group_source_case_rate', 0.0) * 100:.2f}% source-case rate, "
                    f"{reviewer_queue_summary.get('largest_group_queue_share', 0.0) * 100:.2f}% of queued follow-up)"
                )
                dominant_label_map = {
                    "fix_regressions": "fix regressions",
                    "watch_unchanged_fails": "watch unchanged fails",
                    "confirm_filtered_scope": "confirm filtered-out scope",
                    "resolve_skipped_cases": "resolve skipped cases",
                }
                dominant_key = reviewer_queue_summary.get('largest_group_key')
                dominant_label = reviewer_queue_summary.get('largest_group_label')
                if dominant_label:
                    pr_comment_lines.append(
                        "- Reviewer queue largest group label: " + dominant_label
                    )
                if dominant_key:
                    pr_comment_lines.append(
                        "- Reviewer queue dominant focus: "
                        + dominant_label_map.get(dominant_key, dominant_key)
                    )
                if reviewer_queue_summary.get("follow_up_priority"):
                    pr_comment_lines.append(
                        "- Reviewer queue follow-up priority: "
                        + " -> ".join(str(key) for key in reviewer_queue_summary["follow_up_priority"])
                    )
                    pr_comment_lines.append(
                        "- Reviewer queue follow-up labels: "
                        + " -> ".join(
                            dominant_label_map.get(str(key), str(key))
                            for key in reviewer_queue_summary["follow_up_priority"]
                        )
                    )
                    if reviewer_queue_summary.get("follow_up_priority_ranks"):
                        pr_comment_lines.append(
                            "- Reviewer queue priority ranks: "
                            + ", ".join(
                                f"{key}=P{reviewer_queue_summary['follow_up_priority_ranks'][str(key)]}"
                                for key in reviewer_queue_summary["follow_up_priority"]
                            )
                        )
                if reviewer_queue_summary.get("largest_group_priority_rank") is not None:
                    pr_comment_lines.append(
                        f"- Reviewer queue next-focus priority rank: {reviewer_queue_summary.get('largest_group_priority_rank')} of {len(reviewer_queue_summary.get('follow_up_priority', []))}"
                    )
                if reviewer_queue_summary.get("largest_group_keys"):
                    pr_comment_lines.append(
                        "- Reviewer queue tied largest groups: "
                        + ", ".join(str(key) for key in reviewer_queue_summary["largest_group_keys"])
                    )
                    pr_comment_lines.append(
                        f"- Reviewer queue largest-group tie count: {reviewer_queue_summary.get('largest_group_tie_count', 0)}"
                    )
                if reviewer_queue_summary.get("largest_group_labels"):
                    pr_comment_lines.append(
                        "- Reviewer queue tied largest labels: "
                        + ", ".join(str(label) for label in reviewer_queue_summary["largest_group_labels"])
                    )
                if reviewer_queue_summary.get("largest_group_ids"):
                    pr_comment_lines.append(
                        "- Reviewer queue largest group IDs: "
                        + ", ".join(
                            f"`{case_id}`" for case_id in reviewer_queue_summary["largest_group_ids"]
                        )
                    )
                reviewer_queue_groups = {group['key']: group for group in reviewer_queue_summary.get('groups', [])}
                if regression_ids:
                    regression_group = reviewer_queue_groups.get('fix_regressions', {})
                    pr_comment_lines.append(
                        f"- Reviewer queue (regressions): {len(regression_ids)} case(s) / {(len(regression_ids) / active_cases) * 100:.2f}% of active cases / {regression_group.get('source_case_rate', 0.0) * 100:.2f}% of source cases"
                    )
                if summary.get("unchanged_fail_ids"):
                    watchlist_group = reviewer_queue_groups.get('watch_unchanged_fails', {})
                    pr_comment_lines.append(
                        f"- Reviewer queue (watchlist): {len(summary['unchanged_fail_ids'])} case(s) / {(len(summary['unchanged_fail_ids']) / active_cases) * 100:.2f}% of active cases / {watchlist_group.get('source_case_rate', 0.0) * 100:.2f}% of source cases"
                    )
                if summary.get("filtered_out_ids"):
                    filtered_group = reviewer_queue_groups.get('confirm_filtered_scope', {})
                    pr_comment_lines.append(
                        f"- Reviewer queue (filtered-out scope): {len(summary['filtered_out_ids'])} case(s) / {(len(summary['filtered_out_ids']) / active_cases) * 100:.2f}% of active cases / {filtered_group.get('source_case_rate', 0.0) * 100:.2f}% of source cases"
                    )
                if summary.get("skipped_ids"):
                    skipped_group = reviewer_queue_groups.get('resolve_skipped_cases', {})
                    pr_comment_lines.append(
                        f"- Reviewer queue (skipped cases): {len(summary['skipped_ids'])} case(s) / {(len(summary['skipped_ids']) / active_cases) * 100:.2f}% of active cases / {skipped_group.get('source_case_rate', 0.0) * 100:.2f}% of source cases"
                    )
                pr_comment_lines.append("- Reviewer queue: " + " | ".join(reviewer_queue))
                if reviewer_queue_summary.get("largest_group_ids"):
                    if dominant_label:
                        pr_comment_lines.append(
                            "- Reviewer queue next-focus label: " + dominant_label
                        )
                    pr_comment_lines.append(
                        "- Reviewer queue next focus: "
                        + f"{reviewer_queue_summary.get('largest_group_key')}: "
                        + ", ".join(
                            f"`{case_id}`" for case_id in reviewer_queue_summary["largest_group_ids"]
                        )
                    )
                    pr_comment_lines.append(
                        f"- Reviewer queue next-focus case count: {reviewer_queue_summary.get('largest_group_count', 0)}"
                    )
                    pr_comment_lines.append(
                        f"- Reviewer queue next-focus active-case rate: {reviewer_queue_summary.get('largest_group_rate', 0.0) * 100:.2f}% of active cases"
                    )
                    pr_comment_lines.append(
                        f"- Reviewer queue next-focus source-case rate: {reviewer_queue_summary.get('largest_group_source_case_rate', 0.0) * 100:.2f}% of source cases"
                    )
                    pr_comment_lines.append(
                        f"- Reviewer queue next-focus queue share: {reviewer_queue_summary.get('largest_group_queue_share', 0.0) * 100:.2f}% of queued follow-up"
                    )
            if fail_reasons:
                pr_comment_lines.append("- Why it failed:")
                pr_comment_lines.extend([f"  - {reason}" for reason in fail_reasons])
                pr_comment_lines.append(
                    "- Reviewer next step: keep the PR blocked until the failing IDs are fixed, then rerun the regression command."
                )
            else:
                pr_comment_lines.append(
                    "- Reviewer next step: this snapshot is approval-ready; paste it into the PR comment once surrounding checks pass."
                )
            pr_comment_text = "\n".join(pr_comment_lines) + "\n"
            if args.summary_pr_comment == "-":
                print(pr_comment_text, end="")
            else:
                pr_comment_path = Path(args.summary_pr_comment)
                try:
                    pr_comment_path.parent.mkdir(parents=True, exist_ok=True)
                    pr_comment_path.write_text(pr_comment_text, encoding="utf-8")
                except OSError as exc:
                    print(
                        f"error: failed to write summary PR comment to {pr_comment_path}: {exc}",
                        file=sys.stderr,
                    )
                    raise SystemExit(2)
                emit(f"- summary_pr_comment: {pr_comment_path}")

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
