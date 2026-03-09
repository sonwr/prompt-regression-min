from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path
import re
from typing import Any


SUPPORTED_EXPECTED_TYPES = (
    "exact",
    "exact_ci",
    "not_exact",
    "not_exact_ci",
    "substring",
    "substring_ci",
    "not_substring",
    "not_substring_ci",
    "starts_with",
    "starts_with_ci",
    "not_starts_with",
    "not_starts_with_ci",
    "ends_with",
    "ends_with_ci",
    "not_ends_with",
    "not_ends_with_ci",
    "equals_any",
    "equals_any_ci",
    "contains_all",
    "contains_all_ci",
    "contains_any",
    "contains_any_ci",
    "contains_all_ordered",
    "contains_all_ordered_ci",
    "not_contains",
    "not_contains_ci",
    "contains_none",
    "contains_none_ci",
    "regex",
    "regex_ci",
    "regex_fullmatch",
    "regex_fullmatch_ci",
    "not_regex",
    "not_regex_ci",
    "not_regex_fullmatch",
    "not_regex_fullmatch_ci",
    "word_count_range",
    "line_count_range",
    "char_count_range",
)
REGEX_FLAG_MAP = {
    "IGNORECASE": re.IGNORECASE,
    "MULTILINE": re.MULTILINE,
    "DOTALL": re.DOTALL,
}


def _normalize_regex_flag_name(flag_name: Any) -> str:
    if not isinstance(flag_name, str):
        return ""
    return flag_name.strip().upper()


def _count_words(value: str) -> int:
    return len(re.findall(r"\S+", value))


def _count_lines(value: str) -> int:
    if not value:
        return 0
    return len(value.splitlines())


@dataclass
class CaseResult:
    id: str
    baseline_pass: bool
    candidate_pass: bool
    outcome: str
    baseline_output: str
    candidate_output: str
    expectation: dict[str, Any]


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            stripped = line.strip()
            if line_no == 1:
                stripped = stripped.lstrip("\ufeff")
            if not stripped:
                continue
            try:
                parsed = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc
            if not isinstance(parsed, dict):
                raise ValueError(
                    f"Invalid JSONL row at {path}:{line_no}: expected a JSON object per line"
                )
            rows.append(parsed)
    return rows


def _score(output: str, expected: dict[str, Any]) -> bool:
    kind = expected.get("type")
    if kind == "exact":
        return output.strip() == str(expected.get("value", "")).strip()
    if kind == "exact_ci":
        return output.strip().lower() == str(expected.get("value", "")).strip().lower()
    if kind == "not_exact":
        return output.strip() != str(expected.get("value", "")).strip()
    if kind == "not_exact_ci":
        return output.strip().lower() != str(expected.get("value", "")).strip().lower()
    if kind == "substring":
        needle = str(expected.get("value", ""))
        return needle in output
    if kind == "substring_ci":
        needle = str(expected.get("value", ""))
        return needle.lower() in output.lower()
    if kind == "not_substring":
        needle = str(expected.get("value", ""))
        return needle not in output
    if kind == "not_substring_ci":
        needle = str(expected.get("value", ""))
        return needle.lower() not in output.lower()
    if kind == "starts_with":
        prefix = str(expected.get("value", ""))
        return output.startswith(prefix)
    if kind == "starts_with_ci":
        prefix = str(expected.get("value", ""))
        return output.lower().startswith(prefix.lower())
    if kind == "not_starts_with":
        prefix = str(expected.get("value", ""))
        return not output.startswith(prefix)
    if kind == "not_starts_with_ci":
        prefix = str(expected.get("value", ""))
        return not output.lower().startswith(prefix.lower())
    if kind == "ends_with":
        suffix = str(expected.get("value", ""))
        return output.endswith(suffix)
    if kind == "ends_with_ci":
        suffix = str(expected.get("value", ""))
        return output.lower().endswith(suffix.lower())
    if kind == "not_ends_with":
        suffix = str(expected.get("value", ""))
        return not output.endswith(suffix)
    if kind == "not_ends_with_ci":
        suffix = str(expected.get("value", ""))
        return not output.lower().endswith(suffix.lower())
    if kind == "equals_any":
        values = expected.get("values")
        if not isinstance(values, list):
            raise ValueError("equals_any expectation requires a list in expected.values")
        normalized_output = output.strip()
        return any(normalized_output == str(v).strip() for v in values)
    if kind == "equals_any_ci":
        values = expected.get("values")
        if not isinstance(values, list):
            raise ValueError("equals_any_ci expectation requires a list in expected.values")
        normalized_output = output.strip().lower()
        return any(normalized_output == str(v).strip().lower() for v in values)
    if kind == "contains_all":
        values = expected.get("values")
        if not isinstance(values, list):
            raise ValueError("contains_all expectation requires a list in expected.values")
        return all(str(v) in output for v in values)
    if kind == "contains_all_ci":
        values = expected.get("values")
        if not isinstance(values, list):
            raise ValueError("contains_all_ci expectation requires a list in expected.values")
        output_lower = output.lower()
        return all(str(v).lower() in output_lower for v in values)
    if kind == "contains_any":
        values = expected.get("values")
        if not isinstance(values, list):
            raise ValueError("contains_any expectation requires a list in expected.values")
        return any(str(v) in output for v in values)
    if kind == "contains_any_ci":
        values = expected.get("values")
        if not isinstance(values, list):
            raise ValueError("contains_any_ci expectation requires a list in expected.values")
        output_lower = output.lower()
        return any(str(v).lower() in output_lower for v in values)
    if kind == "contains_all_ordered":
        values = expected.get("values")
        if not isinstance(values, list):
            raise ValueError("contains_all_ordered expectation requires a list in expected.values")
        start = 0
        for value in values:
            needle = str(value)
            idx = output.find(needle, start)
            if idx == -1:
                return False
            start = idx + len(needle)
        return True
    if kind == "contains_all_ordered_ci":
        values = expected.get("values")
        if not isinstance(values, list):
            raise ValueError("contains_all_ordered_ci expectation requires a list in expected.values")
        output_lower = output.lower()
        start = 0
        for value in values:
            needle = str(value).lower()
            idx = output_lower.find(needle, start)
            if idx == -1:
                return False
            start = idx + len(needle)
        return True
    if kind == "not_contains":
        values = expected.get("values")
        if not isinstance(values, list):
            raise ValueError("not_contains expectation requires a list in expected.values")
        return all(str(v) not in output for v in values)
    if kind == "not_contains_ci":
        values = expected.get("values")
        if not isinstance(values, list):
            raise ValueError("not_contains_ci expectation requires a list in expected.values")
        output_lower = output.lower()
        return all(str(v).lower() not in output_lower for v in values)
    if kind == "contains_none":
        values = expected.get("values")
        if not isinstance(values, list):
            raise ValueError("contains_none expectation requires a list in expected.values")
        return all(str(v) not in output for v in values)
    if kind == "contains_none_ci":
        values = expected.get("values")
        if not isinstance(values, list):
            raise ValueError("contains_none_ci expectation requires a list in expected.values")
        output_lower = output.lower()
        return all(str(v).lower() not in output_lower for v in values)
    if kind == "word_count_range":
        min_words = expected.get("min_words")
        max_words = expected.get("max_words")
        word_count = _count_words(output)
        if min_words is not None and word_count < min_words:
            return False
        if max_words is not None and word_count > max_words:
            return False
        return True
    if kind == "line_count_range":
        min_lines = expected.get("min_lines")
        max_lines = expected.get("max_lines")
        line_count = _count_lines(output)
        if min_lines is not None and line_count < min_lines:
            return False
        if max_lines is not None and line_count > max_lines:
            return False
        return True
    if kind == "char_count_range":
        min_chars = expected.get("min_chars")
        max_chars = expected.get("max_chars")
        char_count = len(output)
        if min_chars is not None and char_count < min_chars:
            return False
        if max_chars is not None and char_count > max_chars:
            return False
        return True

    if kind in {"regex", "regex_ci", "regex_fullmatch", "regex_fullmatch_ci", "not_regex", "not_regex_ci", "not_regex_fullmatch", "not_regex_fullmatch_ci"}:
        pattern = expected.get("pattern")
        if not isinstance(pattern, str):
            raise ValueError(f"{kind} expectation requires expected.pattern as a string")

        raw_flags = expected.get("flags", [])
        if not isinstance(raw_flags, list):
            raise ValueError(f"{kind} expectation requires expected.flags as a list")

        flags = 0
        for raw_flag_name in raw_flags:
            flag_name = _normalize_regex_flag_name(raw_flag_name)
            if flag_name not in REGEX_FLAG_MAP:
                supported_flags = ", ".join(REGEX_FLAG_MAP)
                raise ValueError(
                    f"Unsupported regex flag: {raw_flag_name}. Supported flags: {supported_flags}"
                )
            flags |= REGEX_FLAG_MAP[flag_name]

        if kind in {"regex_ci", "regex_fullmatch_ci", "not_regex_ci", "not_regex_fullmatch_ci"}:
            flags |= re.IGNORECASE

        try:
            compiled = re.compile(pattern, flags=flags)
        except re.error as exc:
            raise ValueError(f"Invalid regex pattern: {exc}") from exc
        if kind in {"regex_fullmatch", "regex_fullmatch_ci"}:
            return compiled.fullmatch(output) is not None
        if kind in {"not_regex", "not_regex_ci"}:
            return compiled.search(output) is None
        if kind in {"not_regex_fullmatch", "not_regex_fullmatch_ci"}:
            return compiled.fullmatch(output) is None
        return compiled.search(output) is not None
    supported = ", ".join(SUPPORTED_EXPECTED_TYPES)
    raise ValueError(f"Unsupported expectation type: {kind}. Supported types: {supported}")


def _index_rows_by_id(rows: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for idx, row in enumerate(rows, start=1):
        if "id" not in row:
            raise ValueError(f"Missing id field in {label} row #{idx}")
        rid = str(row["id"])
        if not rid.strip():
            raise ValueError(f"Invalid empty id in {label} row #{idx}")
        if rid in by_id:
            raise ValueError(f"Duplicate id in {label}: {rid}")
        by_id[rid] = row
    return by_id


def _validate_expected(expected: dict[str, Any], case_id: str) -> None:
    kind = expected.get("type")
    if not isinstance(kind, str):
        raise ValueError(f"Invalid expected.type in dataset id={case_id}: must be a string")

    if kind in {
        "exact",
        "exact_ci",
        "not_exact",
        "not_exact_ci",
        "substring",
        "substring_ci",
        "not_substring",
        "not_substring_ci",
        "starts_with",
        "starts_with_ci",
        "not_starts_with",
        "not_starts_with_ci",
        "ends_with",
        "ends_with_ci",
        "not_ends_with",
        "not_ends_with_ci",
    }:
        if "value" not in expected:
            raise ValueError(f"Missing expected.value for type={kind} in dataset id={case_id}")
        value = expected.get("value")
        if not isinstance(value, str):
            raise ValueError(
                f"Invalid expected.value for type={kind} in dataset id={case_id}: must be a string"
            )
        if kind in {
            "substring",
            "substring_ci",
            "not_substring",
            "not_substring_ci",
            "starts_with",
            "starts_with_ci",
            "not_starts_with",
            "not_starts_with_ci",
            "ends_with",
            "ends_with_ci",
            "not_ends_with",
            "not_ends_with_ci",
        } and not value.strip():
            raise ValueError(
                f"Invalid expected.value for type={kind} in dataset id={case_id}: must be a non-empty string"
            )
        return

    if kind in {"equals_any", "equals_any_ci"}:
        values = expected.get("values")
        if not isinstance(values, list):
            raise ValueError(
                f"Invalid expected.values for type={kind} in dataset id={case_id}: must be a list"
            )
        if not values:
            raise ValueError(
                f"Invalid expected.values for type={kind} in dataset id={case_id}: must be non-empty"
            )
        if any(not isinstance(v, str) or not v.strip() for v in values):
            raise ValueError(
                f"Invalid expected.values for type={kind} in dataset id={case_id}: every item must be a non-empty string"
            )
        return

    if kind in {"contains_all", "contains_all_ci"}:
        values = expected.get("values")
        if not isinstance(values, list):
            raise ValueError(
                f"Invalid expected.values for type={kind} in dataset id={case_id}: must be a list"
            )
        if not values:
            raise ValueError(
                f"Invalid expected.values for type={kind} in dataset id={case_id}: must be non-empty"
            )
        if any(not isinstance(v, str) or not v.strip() for v in values):
            raise ValueError(
                f"Invalid expected.values for type={kind} in dataset id={case_id}: every item must be a non-empty string"
            )
        return

    if kind in {"contains_any", "contains_any_ci", "contains_all_ordered", "contains_all_ordered_ci"}:
        values = expected.get("values")
        if not isinstance(values, list):
            raise ValueError(
                f"Invalid expected.values for type={kind} in dataset id={case_id}: must be a list"
            )
        if not values:
            raise ValueError(
                f"Invalid expected.values for type={kind} in dataset id={case_id}: must be non-empty"
            )
        if any(not isinstance(v, str) or not v.strip() for v in values):
            raise ValueError(
                f"Invalid expected.values for type={kind} in dataset id={case_id}: every item must be a non-empty string"
            )
        return

    if kind in {"not_contains", "not_contains_ci", "contains_none", "contains_none_ci"}:
        values = expected.get("values")
        if not isinstance(values, list):
            raise ValueError(
                f"Invalid expected.values for type={kind} in dataset id={case_id}: must be a list"
            )
        if not values:
            raise ValueError(
                f"Invalid expected.values for type={kind} in dataset id={case_id}: must be non-empty"
            )
        if any(not isinstance(v, str) or not v.strip() for v in values):
            raise ValueError(
                f"Invalid expected.values for type={kind} in dataset id={case_id}: every item must be a non-empty string"
            )
        return

    if kind == "word_count_range":
        min_words = expected.get("min_words")
        max_words = expected.get("max_words")
        if min_words is None and max_words is None:
            raise ValueError(
                f"Invalid word_count_range expectation in dataset id={case_id}: set min_words, max_words, or both"
            )
        if min_words is not None and (not isinstance(min_words, int) or min_words < 0):
            raise ValueError(
                f"Invalid expected.min_words for type={kind} in dataset id={case_id}: must be an integer >= 0"
            )
        if max_words is not None and (not isinstance(max_words, int) or max_words < 0):
            raise ValueError(
                f"Invalid expected.max_words for type={kind} in dataset id={case_id}: must be an integer >= 0"
            )
        if min_words is not None and max_words is not None and min_words > max_words:
            raise ValueError(
                f"Invalid word_count_range expectation in dataset id={case_id}: min_words must be <= max_words"
            )
        return
    if kind == "line_count_range":
        min_lines = expected.get("min_lines")
        max_lines = expected.get("max_lines")
        if min_lines is None and max_lines is None:
            raise ValueError(
                f"Invalid line_count_range expectation in dataset id={case_id}: set min_lines, max_lines, or both"
            )
        if min_lines is not None and (not isinstance(min_lines, int) or min_lines < 0):
            raise ValueError(
                f"Invalid expected.min_lines for type={kind} in dataset id={case_id}: must be an integer >= 0"
            )
        if max_lines is not None and (not isinstance(max_lines, int) or max_lines < 0):
            raise ValueError(
                f"Invalid expected.max_lines for type={kind} in dataset id={case_id}: must be an integer >= 0"
            )
        if min_lines is not None and max_lines is not None and min_lines > max_lines:
            raise ValueError(
                f"Invalid line_count_range expectation in dataset id={case_id}: min_lines must be <= max_lines"
            )
        return
    if kind in {"regex", "regex_ci", "regex_fullmatch", "regex_fullmatch_ci", "not_regex", "not_regex_ci", "not_regex_fullmatch", "not_regex_fullmatch_ci"}:
        pattern = expected.get("pattern")
        if not isinstance(pattern, str) or not pattern.strip():
            raise ValueError(
                f"Invalid expected.pattern for type={kind} in dataset id={case_id}: must be a non-empty string"
            )

        flags = expected.get("flags", [])
        if not isinstance(flags, list):
            raise ValueError(
                f"Invalid expected.flags for type={kind} in dataset id={case_id}: must be a list"
            )
        normalized_flags: list[str] = []
        for raw_flag_name in flags:
            flag_name = _normalize_regex_flag_name(raw_flag_name)
            if flag_name not in REGEX_FLAG_MAP:
                supported_flags = ", ".join(REGEX_FLAG_MAP)
                raise ValueError(
                    f"Unsupported regex flag in dataset id={case_id}: {raw_flag_name}. Supported flags: {supported_flags}"
                )
            normalized_flags.append(flag_name)

        flags_value = 0
        for flag_name in normalized_flags:
            flags_value |= REGEX_FLAG_MAP[flag_name]

        if kind in {"regex_ci", "regex_fullmatch_ci", "not_regex_ci", "not_regex_fullmatch_ci"}:
            flags_value |= re.IGNORECASE

        try:
            re.compile(pattern, flags=flags_value)
        except re.error as exc:
            raise ValueError(
                f"Invalid expected.pattern for type={kind} in dataset id={case_id}: {exc}"
            ) from exc
        return

    supported = ", ".join(SUPPORTED_EXPECTED_TYPES)
    raise ValueError(
        f"Unsupported expected.type in dataset id={case_id}: {kind}. Supported types: {supported}"
    )


def _derive_outcome(baseline_pass: bool, candidate_pass: bool) -> str:
    if baseline_pass and not candidate_pass:
        return "regressed"
    if not baseline_pass and candidate_pass:
        return "improved"
    if baseline_pass and candidate_pass:
        return "unchanged_pass"
    return "unchanged_fail"


def _is_dataset_case_disabled(case: dict[str, Any], case_id: str) -> bool:
    raw_disabled = case.get("disabled", False)
    if not isinstance(raw_disabled, bool):
        raise ValueError(
            f"Invalid disabled field in dataset id={case_id}: must be a boolean"
        )
    return raw_disabled


def run_regression(
    dataset_path: str,
    baseline_path: str,
    candidate_path: str,
    include_id_regex: str | None = None,
    exclude_id_regex: str | None = None,
) -> dict[str, Any]:
    dataset_rows = _load_jsonl(Path(dataset_path))
    baseline_rows = _load_jsonl(Path(baseline_path))
    candidate_rows = _load_jsonl(Path(candidate_path))

    if not dataset_rows:
        raise ValueError("Dataset is empty: provide at least one case")

    source_dataset_case_count = len(dataset_rows)

    include_pattern = re.compile(include_id_regex) if include_id_regex else None
    exclude_pattern = re.compile(exclude_id_regex) if exclude_id_regex else None

    filtered_out_ids: list[str] = []
    if include_pattern is not None or exclude_pattern is not None:
        filtered_dataset_rows: list[dict[str, Any]] = []
        for row in dataset_rows:
            case_id = str(row.get("id", ""))
            include_ok = include_pattern.search(case_id) is not None if include_pattern else True
            exclude_hit = exclude_pattern.search(case_id) is not None if exclude_pattern else False
            if include_ok and not exclude_hit:
                filtered_dataset_rows.append(row)
            else:
                filtered_out_ids.append(case_id)
        dataset_rows = filtered_dataset_rows

    if not dataset_rows:
        raise ValueError("Dataset selection is empty after applying id filters")

    dataset_by_id = _index_rows_by_id(dataset_rows, "dataset")
    baseline_by_id = _index_rows_by_id(baseline_rows, "baseline")
    candidate_by_id = _index_rows_by_id(candidate_rows, "candidate")

    dataset_ids = set(dataset_by_id)

    id_filters_enabled = include_id_regex is not None or exclude_id_regex is not None
    if id_filters_enabled:
        baseline_by_id = {cid: row for cid, row in baseline_by_id.items() if cid in dataset_ids}
        candidate_by_id = {cid: row for cid, row in candidate_by_id.items() if cid in dataset_ids}

    extra_baseline_ids = sorted(set(baseline_by_id) - dataset_ids)
    if extra_baseline_ids:
        preview = ", ".join(extra_baseline_ids[:5])
        if len(extra_baseline_ids) > 5:
            preview += ", ..."
        raise ValueError(f"Baseline has unknown ids not present in dataset: {preview}")

    extra_candidate_ids = sorted(set(candidate_by_id) - dataset_ids)
    if extra_candidate_ids:
        preview = ", ".join(extra_candidate_ids[:5])
        if len(extra_candidate_ids) > 5:
            preview += ", ..."
        raise ValueError(f"Candidate has unknown ids not present in dataset: {preview}")

    missing_baseline_ids = sorted(dataset_ids - set(baseline_by_id))
    if missing_baseline_ids:
        preview = ", ".join(missing_baseline_ids[:5])
        if len(missing_baseline_ids) > 5:
            preview += ", ..."
        raise ValueError(f"Baseline is missing ids present in dataset: {preview}")

    missing_candidate_ids = sorted(dataset_ids - set(candidate_by_id))
    if missing_candidate_ids:
        preview = ", ".join(missing_candidate_ids[:5])
        if len(missing_candidate_ids) > 5:
            preview += ", ..."
        raise ValueError(f"Candidate is missing ids present in dataset: {preview}")

    results: list[CaseResult] = []
    skipped_ids: list[str] = []

    for cid, case in dataset_by_id.items():
        if _is_dataset_case_disabled(case, cid):
            skipped_ids.append(cid)
            continue

        if "expected" not in case:
            raise ValueError(f"Missing expected field in dataset id={cid}")
        expected = case["expected"]
        if not isinstance(expected, dict):
            raise ValueError(f"Invalid expected field in dataset id={cid}: must be an object")
        _validate_expected(expected, cid)

        baseline_row = baseline_by_id[cid]
        candidate_row = candidate_by_id[cid]

        if "output" not in baseline_row:
            raise ValueError(f"Missing output field in baseline id={cid}")
        if "output" not in candidate_row:
            raise ValueError(f"Missing output field in candidate id={cid}")

        b_raw = baseline_row["output"]
        c_raw = candidate_row["output"]
        if not isinstance(b_raw, str):
            raise ValueError(f"Invalid output field in baseline id={cid}: must be a string")
        if not isinstance(c_raw, str):
            raise ValueError(f"Invalid output field in candidate id={cid}: must be a string")

        b_out = b_raw
        c_out = c_raw

        b_pass = _score(b_out, expected)
        c_pass = _score(c_out, expected)

        results.append(
            CaseResult(
                id=cid,
                baseline_pass=b_pass,
                candidate_pass=c_pass,
                outcome=_derive_outcome(b_pass, c_pass),
                baseline_output=b_out,
                candidate_output=c_out,
                expectation=expected,
            )
        )

    if not results:
        raise ValueError(
            "No active dataset cases to evaluate: every case is disabled"
        )

    baseline_passes = sum(1 for r in results if r.baseline_pass)
    candidate_passes = sum(1 for r in results if r.candidate_pass)

    regression_ids = [r.id for r in results if r.baseline_pass and not r.candidate_pass]
    improved_ids = [r.id for r in results if not r.baseline_pass and r.candidate_pass]
    unchanged_pass_ids = [r.id for r in results if r.baseline_pass and r.candidate_pass]
    unchanged_fail_ids = [r.id for r in results if not r.baseline_pass and not r.candidate_pass]

    regressions = len(regression_ids)
    improved = len(improved_ids)
    changed_ids = sorted(regression_ids + improved_ids)
    unchanged = len(results) - regressions - improved
    changed = len(changed_ids)
    regression_rate = round(regressions / len(results), 4)
    changed_rate = round(changed / len(results), 4)

    baseline_pass_rate = round(baseline_passes / len(results), 4) if results else 0.0
    candidate_pass_rate = round(candidate_passes / len(results), 4) if results else 0.0

    outcome_counts = {
        "regressed": sum(1 for r in results if r.outcome == "regressed"),
        "improved": sum(1 for r in results if r.outcome == "improved"),
        "unchanged_pass": sum(1 for r in results if r.outcome == "unchanged_pass"),
        "unchanged_fail": sum(1 for r in results if r.outcome == "unchanged_fail"),
    }

    unchanged_pass = outcome_counts["unchanged_pass"]
    unchanged_fail = outcome_counts["unchanged_fail"]
    unchanged_fail_rate = round(unchanged_fail / len(results), 4)
    stability_rate = round(unchanged / len(results), 4)

    selected_dataset_case_count = len(dataset_rows)
    selected_dataset_ids = sorted(row["id"] for row in dataset_rows)
    active_case_ids = sorted(result.id for result in results)
    filtered_out_rate = round(len(filtered_out_ids) / source_dataset_case_count, 4)
    skipped_rate = round(len(skipped_ids) / len(results), 4) if results else 0.0
    selection_rate = round(selected_dataset_case_count / source_dataset_case_count, 4)

    pass_rate_trend = "flat"
    if candidate_pass_rate > baseline_pass_rate:
        pass_rate_trend = "improving"
    elif candidate_pass_rate < baseline_pass_rate:
        pass_rate_trend = "regressing"

    summary = {
        "dataset_cases": source_dataset_case_count,
        "selected_dataset_cases": selected_dataset_case_count,
        "selection_rate": selection_rate,
        "selected_dataset_ids": selected_dataset_ids,
        "cases": len(results),
        "active_case_ids": active_case_ids,
        "id_filter_include_regex": include_id_regex,
        "id_filter_exclude_regex": exclude_id_regex,
        "filtered_out_cases": len(filtered_out_ids),
        "filtered_out_rate": filtered_out_rate,
        "filtered_out_ids": sorted(filtered_out_ids),
        "active_cases": len(results),
        "skipped_cases": len(skipped_ids),
        "skipped_rate": skipped_rate,
        "skipped_ids": sorted(skipped_ids),
        "baseline_passes": baseline_passes,
        "candidate_passes": candidate_passes,
        "baseline_pass_rate": baseline_pass_rate,
        "candidate_pass_rate": candidate_pass_rate,
        "delta_passes": candidate_passes - baseline_passes,
        "delta_pass_rate_pp": round((candidate_pass_rate - baseline_pass_rate) * 100, 2),
        "pass_rate_trend": pass_rate_trend,
        "regressions": regressions,
        "regression_rate": regression_rate,
        "improved": improved,
        "changed": changed,
        "changed_ids": changed_ids,
        "changed_rate": changed_rate,
        "unchanged": unchanged,
        "stability_rate": stability_rate,
        "unchanged_pass": unchanged_pass,
        "unchanged_pass_ids": sorted(unchanged_pass_ids),
        "unchanged_fail": unchanged_fail,
        "unchanged_fail_rate": unchanged_fail_rate,
        "regression_ids": sorted(regression_ids),
        "improved_ids": sorted(improved_ids),
        "unchanged_fail_ids": sorted(unchanged_fail_ids),
        "outcome_counts": outcome_counts,
    }

    return {
        "summary": summary,
        "cases": [asdict(r) for r in results],
    }
