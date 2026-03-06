from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import Any


@dataclass
class CaseResult:
    id: str
    baseline_pass: bool
    candidate_pass: bool
    baseline_output: str
    candidate_output: str
    expectation: dict[str, Any]


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                rows.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc
    return rows


def _score(output: str, expected: dict[str, Any]) -> bool:
    kind = expected.get("type")
    if kind == "exact":
        return output.strip() == str(expected.get("value", "")).strip()
    if kind == "substring":
        needle = str(expected.get("value", ""))
        return needle in output
    if kind == "contains_all":
        values = expected.get("values")
        if not isinstance(values, list):
            raise ValueError("contains_all expectation requires a list in expected.values")
        return all(str(v) in output for v in values)
    raise ValueError(f"Unsupported expectation type: {kind}")


def _index_rows_by_id(rows: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for idx, row in enumerate(rows, start=1):
        if "id" not in row:
            raise ValueError(f"Missing id field in {label} row #{idx}")
        rid = str(row["id"])
        if rid in by_id:
            raise ValueError(f"Duplicate id in {label}: {rid}")
        by_id[rid] = row
    return by_id


def _validate_expected(expected: dict[str, Any], case_id: str) -> None:
    kind = expected.get("type")
    if not isinstance(kind, str):
        raise ValueError(f"Invalid expected.type in dataset id={case_id}: must be a string")

    if kind in {"exact", "substring"}:
        if "value" not in expected:
            raise ValueError(f"Missing expected.value for type={kind} in dataset id={case_id}")
        return

    if kind == "contains_all":
        values = expected.get("values")
        if not isinstance(values, list):
            raise ValueError(
                f"Invalid expected.values for type=contains_all in dataset id={case_id}: must be a list"
            )
        if not values:
            raise ValueError(
                f"Invalid expected.values for type=contains_all in dataset id={case_id}: must be non-empty"
            )
        return

    raise ValueError(f"Unsupported expected.type in dataset id={case_id}: {kind}")


def run_regression(dataset_path: str, baseline_path: str, candidate_path: str) -> dict[str, Any]:
    dataset_rows = _load_jsonl(Path(dataset_path))
    baseline_rows = _load_jsonl(Path(baseline_path))
    candidate_rows = _load_jsonl(Path(candidate_path))

    dataset_by_id = _index_rows_by_id(dataset_rows, "dataset")
    baseline_by_id = _index_rows_by_id(baseline_rows, "baseline")
    candidate_by_id = _index_rows_by_id(candidate_rows, "candidate")

    dataset_ids = set(dataset_by_id)
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

    for cid, case in dataset_by_id.items():
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

        b_out = str(baseline_row["output"])
        c_out = str(candidate_row["output"])

        b_pass = _score(b_out, expected)
        c_pass = _score(c_out, expected)

        results.append(
            CaseResult(
                id=cid,
                baseline_pass=b_pass,
                candidate_pass=c_pass,
                baseline_output=b_out,
                candidate_output=c_out,
                expectation=expected,
            )
        )

    baseline_passes = sum(1 for r in results if r.baseline_pass)
    candidate_passes = sum(1 for r in results if r.candidate_pass)

    regressions = sum(1 for r in results if r.baseline_pass and not r.candidate_pass)
    improved = sum(1 for r in results if not r.baseline_pass and r.candidate_pass)
    unchanged = len(results) - regressions - improved

    summary = {
        "cases": len(results),
        "baseline_passes": baseline_passes,
        "candidate_passes": candidate_passes,
        "baseline_pass_rate": round(baseline_passes / len(results), 4) if results else 0.0,
        "candidate_pass_rate": round(candidate_passes / len(results), 4) if results else 0.0,
        "regressions": regressions,
        "improved": improved,
        "unchanged": unchanged,
    }

    return {
        "summary": summary,
        "cases": [asdict(r) for r in results],
    }
