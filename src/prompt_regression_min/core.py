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
        values = expected.get("values", [])
        return all(str(v) in output for v in values)
    raise ValueError(f"Unsupported expectation type: {kind}")


def run_regression(dataset_path: str, baseline_path: str, candidate_path: str) -> dict[str, Any]:
    dataset_rows = _load_jsonl(Path(dataset_path))
    baseline_rows = _load_jsonl(Path(baseline_path))
    candidate_rows = _load_jsonl(Path(candidate_path))

    baseline_by_id = {r["id"]: r for r in baseline_rows}
    candidate_by_id = {r["id"]: r for r in candidate_rows}

    results: list[CaseResult] = []

    for case in dataset_rows:
        cid = case["id"]
        expected = case["expected"]
        if cid not in baseline_by_id:
            raise ValueError(f"Missing baseline output for id={cid}")
        if cid not in candidate_by_id:
            raise ValueError(f"Missing candidate output for id={cid}")

        b_out = str(baseline_by_id[cid].get("output", ""))
        c_out = str(candidate_by_id[cid].get("output", ""))

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
