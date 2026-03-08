# prompt-regression-min

Minimal, deterministic regression checks for prompt and workflow changes in LLM-powered products.

`prompt-regression-min` helps teams answer one practical question before shipping:

> **Did this prompt/model/workflow change improve quality, or quietly break something?**

---

## Table of Contents

- [Project Introduction](#project-introduction)
- [Vision](#vision)
- [Philosophy](#philosophy)
- [Who This Is For](#who-this-is-for)
- [What It Does Today](#what-it-does-today)
- [Quickstart](#quickstart)
- [Core Concepts](#core-concepts)
- [Data Format](#data-format)
- [CLI Reference](#cli-reference)
- [Example Output](#example-output)
- [CI/CD Integration](#cicd-integration)
- [Development Direction](#development-direction)
- [Quality and Contribution Guidelines](#quality-and-contribution-guidelines)
- [FAQ](#faq)
- [License](#license)

---

## Project Introduction

In real-world LLM systems, regressions rarely appear as crashes. They show up as:

- answers becoming less specific,
- policies being skipped,
- key terms disappearing,
- or edge-cases quietly failing.

`prompt-regression-min` is intentionally small and strict.
It compares **baseline** and **candidate** outputs on the same test set and reports:

- pass-rate changes,
- regressions,
- improvements,
- unchanged behavior.

The goal is to become a lightweight quality gate that is easy to adopt in any repo.

---

## Vision

Build a "small but reliable" open-source quality layer for LLM iteration.

### Near-term vision

- Make prompt/workflow evaluation reproducible in under 5 minutes.
- Integrate cleanly with CI for pass/fail decisions.
- Keep logic deterministic and easy to audit.

### Mid-term vision

- Add weighted and semantic scoring while keeping deterministic baselines.
- Provide richer developer reports (JSON + HTML).
- Support team-level quality contracts (per-domain thresholds).

### Long-term vision

A composable evaluation toolkit where teams can plug in:

- syntax-level checks,
- semantic checks,
- policy checks,
- and business KPI checks,

without losing simplicity.

---

## Philosophy

### 1) Determinism first
If quality cannot be reproduced, it cannot be trusted.

### 2) Small surface area
Fewer moving parts means easier adoption and lower maintenance cost.

### 3) Explicit tradeoffs
Every scorer has failure modes; make them visible instead of hiding complexity.

### 4) CI-native by default
Tooling should fit shipping workflows, not add ceremony.

### 5) Open by design
Readable code, inspectable data format, and practical docs over hype.

---

## Who This Is For

- Teams iterating on prompts rapidly
- Agent/workflow products with frequent model routing changes
- Developers who need fast regression signals before deploy
- OSS maintainers who want transparent quality checks in public repos

---

## What It Does Today

- Compares **baseline** vs **candidate** outputs on shared cases
- Supports lightweight expectation scorers:
  - `exact`
  - `exact_ci`
  - `not_exact`
  - `not_exact_ci`
  - `substring`
  - `substring_ci`
  - `not_substring`
  - `not_substring_ci`
  - `contains_all`
  - `contains_all_ci`
  - `contains_any`
  - `contains_any_ci`
  - `equals_any`
  - `equals_any_ci`
  - `not_contains`
  - `not_contains_ci`
  - `contains_none` (alias of `not_contains`)
  - `contains_none_ci` (alias of `not_contains_ci`)
  - `starts_with`
  - `starts_with_ci`
  - `not_starts_with`
  - `not_starts_with_ci`
  - `ends_with`
  - `ends_with_ci`
  - `not_ends_with`
  - `not_ends_with_ci`
  - `regex` (with optional `IGNORECASE`, `MULTILINE`, `DOTALL` flags; case/whitespace-insensitive tokens like `" ignorecase "` are normalized)
  - `regex_ci` (alias of `regex` with implicit `IGNORECASE`)
  - `regex_fullmatch` (same flags, but requires the entire output to match)
  - `not_regex` (same flags, but fails if the pattern appears anywhere)
  - `not_regex_ci` (alias of `not_regex` with implicit `IGNORECASE`)
  - `not_regex_fullmatch` (same flags, but fails if the entire output matches the pattern)
- Produces:
  - terminal summary (including `outcome_counts` rollup and explicit `unchanged_pass` / `unchanged_fail` counters)
  - machine-readable JSON report (including `summary.regression_ids` / `summary.improved_ids`)
- Exits with non-zero status when regressions are detected (CI-friendly)

---

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# either CLI entrypoint
prm run \
  --dataset examples/dataset/customer_support.jsonl \
  --baseline examples/outputs/customer_support.baseline.jsonl \
  --candidate examples/outputs/customer_support.candidate.jsonl \
  --report report.json

# or module execution
python -m prompt_regression_min run \
  --dataset examples/dataset/customer_support.jsonl \
  --baseline examples/outputs/customer_support.baseline.jsonl \
  --candidate examples/outputs/customer_support.candidate.jsonl \
  --report report.json
```

---

## Core Concepts

- **Dataset**: test cases with expectations
- **Baseline output**: currently accepted behavior
- **Candidate output**: new behavior after a change
- **Regression**: baseline passes, candidate fails
- **Improvement**: baseline fails, candidate passes

This framing keeps release discussions objective and diff-driven.

---

## Data Format

### Dataset JSONL

Each line:

```json
{
  "id": "case-1",
  "input": "How do I reset my password?",
  "expected": {
    "type": "contains_all",
    "values": ["reset", "email"]
  }
}
```

Supported `expected.type` values:

- `exact` (`value` must be a string; leading/trailing whitespace is ignored on both expected and output):
  ```json
  { "type": "exact", "value": "..." }
  ```
- `exact_ci` (case-insensitive variant of `exact`; still trims surrounding whitespace):
  ```json
  { "type": "exact_ci", "value": "approved" }
  ```
- `not_exact` (`value` must be a string; passes only when normalized output differs):
  ```json
  { "type": "not_exact", "value": "Forbidden" }
  ```
- `not_exact_ci` (case-insensitive variant of `not_exact`; still trims surrounding whitespace):
  ```json
  { "type": "not_exact_ci", "value": "forbidden" }
  ```
- `substring` (`value` must be a non-empty string):
  ```json
  { "type": "substring", "value": "..." }
  ```
- `substring_ci` (case-insensitive variant of `substring`):
  ```json
  { "type": "substring_ci", "value": "error code" }
  ```
- `not_substring` (fails if the output includes the forbidden token):
  ```json
  { "type": "not_substring", "value": "secret" }
  ```
- `not_substring_ci` (case-insensitive variant of `not_substring`):
  ```json
  { "type": "not_substring_ci", "value": "secret" }
  ```
- `contains_all` (requires a non-empty `values` list of non-empty strings):
  ```json
  { "type": "contains_all", "values": ["a", "b"] }
  ```
- `contains_all_ci` (case-insensitive variant of `contains_all`):
  ```json
  { "type": "contains_all_ci", "values": ["order", "resolved"] }
  ```
- `starts_with` (`value` must be a non-empty string prefix):
  ```json
  { "type": "starts_with", "value": "Order #" }
  ```
- `starts_with_ci` (case-insensitive variant of `starts_with`; `value` must be a non-empty string prefix):
  ```json
  { "type": "starts_with_ci", "value": "order #" }
  ```
- `not_starts_with` (`value` must be a non-empty string prefix that must not appear at output start):
  ```json
  { "type": "not_starts_with", "value": "Error:" }
  ```
- `not_starts_with_ci` (case-insensitive variant of `not_starts_with`):
  ```json
  { "type": "not_starts_with_ci", "value": "error:" }
  ```
- `ends_with` (`value` must be a non-empty string suffix):
  ```json
  { "type": "ends_with", "value": "resolved" }
  ```
- `ends_with_ci` (case-insensitive variant of `ends_with`; `value` must be a non-empty string suffix):
  ```json
  { "type": "ends_with_ci", "value": "resolved" }
  ```
- `not_ends_with` (`value` must be a non-empty string suffix that must not appear at output end):
  ```json
  { "type": "not_ends_with", "value": "debug" }
  ```
- `not_ends_with_ci` (case-insensitive variant of `not_ends_with`):
  ```json
  { "type": "not_ends_with_ci", "value": "debug" }
  ```
- `contains_any` (candidate output must include at least one value from a non-empty `values` list):
  ```json
  { "type": "contains_any", "values": ["reset", "password"] }
  ```
- `contains_any_ci` (case-insensitive variant of `contains_any`):
  ```json
  { "type": "contains_any_ci", "values": ["approved", "pending"] }
  ```
- `equals_any` (normalized output must exactly match one candidate in a non-empty `values` list):
  ```json
  { "type": "equals_any", "values": ["Approved", "Pending"] }
  ```
- `equals_any_ci` (case-insensitive variant of `equals_any`):
  ```json
  { "type": "equals_any_ci", "values": ["approved", "pending"] }
  ```
- `not_contains` (candidate output must not include any value from a non-empty `values` list):
  ```json
  { "type": "not_contains", "values": ["SSN", "credit card"] }
  ```
- `not_contains_ci` (case-insensitive variant of `not_contains`):
  ```json
  { "type": "not_contains_ci", "values": ["ssn", "credit card"] }
  ```
- `contains_none` (readability alias of `not_contains`):
  ```json
  { "type": "contains_none", "values": ["SSN", "credit card"] }
  ```
- `contains_none_ci` (readability alias of `not_contains_ci`):
  ```json
  { "type": "contains_none_ci", "values": ["ssn", "credit card"] }
  ```
- `regex` (requires non-empty `pattern`; optional `flags` list):
  ```json
  { "type": "regex", "pattern": "order\\s+#?\\d{4}", "flags": ["IGNORECASE"] }
  ```
- `regex_fullmatch` (same as `regex` but requires full-string match):
  ```json
  { "type": "regex_fullmatch", "pattern": "Order #[0-9]{4}" }
  ```
- `not_regex` (same as `regex` but requires the pattern to *not* appear in output):
  ```json
  { "type": "not_regex", "pattern": "\\b(SSN|credit card)\\b", "flags": ["IGNORECASE"] }
  ```
- `not_regex_fullmatch` (same as `regex_fullmatch` but requires full-string *non-match*):
  ```json
  { "type": "not_regex_fullmatch", "pattern": "(Approved|Pending)" }
  ```

### Output JSONL

Each line:

```json
{
  "id": "case-1",
  "output": "Use the reset link and check your email inbox."
}
```

Both baseline and candidate output files must contain the same IDs used in the dataset.

IDs must be non-empty, non-whitespace strings across dataset/baseline/candidate rows.

Dataset files must be non-empty (at least one valid JSONL case).

Optional dataset field:
- `disabled` (boolean): if `true`, the case is skipped from scoring but still validated for ID alignment.

At least one case must remain active after applying `disabled: true` filters.

When `--report` is used, each case includes an `outcome` field:
- `regressed`
- `improved`
- `unchanged_pass`
- `unchanged_fail`

The report summary includes `outcome_counts` for quick CI diagnostics, plus `changed` / `changed_rate` to track blast radius.

---

## CLI Reference

```bash
prm run \
  --dataset <dataset.jsonl> \
  --baseline <baseline.jsonl> \
  --candidate <candidate.jsonl> \
  [--report report.json] \
  [--max-regressions 0] \
  [--max-regression-rate <float>] \
  [--min-candidate-pass-rate 0.0] \
  [--max-unchanged-fail -1] \
  [--max-unchanged-fail-rate <float>] \
  [--forbid-unchanged-fail-id-regex <regex>] \
  [--max-skipped-cases -1] \
  [--min-delta-pass-rate-pp <float>] \
  [--max-delta-pass-rate-pp <float>] \
  [--min-improved 0] \
  [--max-improved -1] \
  [--max-improved-rate 1.0] \
  [--max-changed-cases -1] \
  [--max-changed-rate <float>] \
  [--min-active-cases 1] \
  [--max-filtered-out-cases -1] \
  [--max-filtered-out-rate <float>] \
  [--min-unchanged-pass 0] \
  [--max-unchanged-pass -1] \
  [--min-stability-rate <float>] \
  [--require-pass-rate-trend <improving|flat|regressing>] \
  [--include-id-regex <regex>] \
  [--exclude-id-regex <regex>] \
  [--summary-json [path|-]] \
  [--summary-json-pretty] \
  [--summary-markdown path] \
  [--quiet]

# short aliases: -d, -b, -c, -r
```

Use `--include-id-regex` / `--exclude-id-regex` to run deterministic subsets (e.g., shard by feature area) without editing the source dataset.

### Exit codes

- `0`: quality gate passed (`regressions <= max-regressions`, regression rate meets `--max-regression-rate` when enabled, candidate pass rate meets threshold, unchanged fails are within `--max-unchanged-fail` and `--max-unchanged-fail-rate` when enabled, critical unchanged failing ids do not match `--forbid-unchanged-fail-id-regex` when enabled, skipped cases are within `max-skipped-cases` when enabled, pass-rate delta stays within `--min-delta-pass-rate-pp` / `--max-delta-pass-rate-pp` when enabled, improved cases meet `--min-improved` / `--max-improved` / `--max-improved-rate` when enabled, changed-case budget/rate meet `--max-changed-cases` / `--max-changed-rate` when enabled, active cases meet `--min-active-cases`, filtered-out case budget/rate meet `--max-filtered-out-cases` / `--max-filtered-out-rate` when enabled, unchanged passing cases stay within `--min-unchanged-pass` / `--max-unchanged-pass` gates, stability rate meets `--min-stability-rate` when enabled, and pass-rate trend matches `--require-pass-rate-trend` when enabled)
- `1`: quality gate failed
- `>1`: invalid input / runtime error

Terminal summary now includes `pass_rate_trend` (`improving` | `flat` | `regressing`) for quick directional triage.

### Mixed expectation fixture (CI smoke)

Use the fixture pack to smoke-test `equals_any` + `regex_fullmatch` together:

```bash
python3 -m prompt_regression_min run \
  -d examples/dataset/mixed_expectations.jsonl \
  -b examples/outputs/mixed_expectations.baseline.jsonl \
  -c examples/outputs/mixed_expectations.candidate.jsonl \
  --max-regressions 0 \
  --summary-json
```

### FAIL payload fixture (CI audit smoke)

Use this fixture to verify that `fail_reasons` and `gates` are emitted together in FAIL mode:

```bash
python3 -m prompt_regression_min run \
  -d examples/dataset/fail_payload_gate_demo.jsonl \
  -b examples/outputs/fail_payload_gate_demo.baseline.jsonl \
  -c examples/outputs/fail_payload_gate_demo.candidate.jsonl \
  --max-unchanged-fail 0 \
  --summary-json
```

Expected: exit code `1`, JSON payload `status=FAIL`, non-empty `fail_reasons`, and `gates.max_unchanged_fail=0`.

### Unchanged-pass band fixture (CI policy smoke)

Use this fixture to enforce a bounded unchanged-pass policy (minimum and maximum both fixed to `3`):

```bash
python3 -m prompt_regression_min run \
  -d examples/dataset/unchanged_pass_band_demo.jsonl \
  -b examples/outputs/unchanged_pass_band_demo.baseline.jsonl \
  -c examples/outputs/unchanged_pass_band_demo.candidate.jsonl \
  --min-unchanged-pass 3 \
  --max-unchanged-pass 3 \
  --summary-json
```

Expected: exit code `0`, JSON payload `status=PASS`, `summary.unchanged_pass=3`, and gate echo values `gates.min_unchanged_pass=3` + `gates.max_unchanged_pass=3`.

### Improved-band fixture (CI policy smoke)

Use this fixture to enforce an exact improved-case budget (`min=max=1`) while still banning regressions:

```bash
python3 -m prompt_regression_min run \
  -d examples/dataset/improved_band_demo.jsonl \
  -b examples/outputs/improved_band_demo.baseline.jsonl \
  -c examples/outputs/improved_band_demo.candidate.jsonl \
  --max-regressions 0 \
  --min-improved 1 \
  --max-improved 1 \
  --summary-json
```

Expected: exit code `0`, JSON payload `status=PASS`, `summary.improved=1`, and gate echo values `gates.min_improved=1` + `gates.max_improved=1`.

### Filtered-out band fixture (CI shard-policy smoke)

Use this fixture to enforce a bounded filtered-out shard policy while selecting `auth-*` case IDs:

```bash
python3 -m prompt_regression_min run \
  -d examples/dataset/filtered_out_band_demo.jsonl \
  -b examples/outputs/filtered_out_band_demo.baseline.jsonl \
  -c examples/outputs/filtered_out_band_demo.candidate.jsonl \
  --include-id-regex '^auth-' \
  --max-filtered-out-cases 2 \
  --max-filtered-out-rate 0.5 \
  --summary-json
```

Expected: exit code `0`, JSON payload `status=PASS`, `summary.filtered_out_cases=2`, `summary.filtered_out_rate=0.5`, and gate echo values `gates.max_filtered_out_cases=2` + `gates.max_filtered_out_rate=0.5`.

### Machine-readable summary

Use `--summary-json` for CI parsers:

- `--summary-json` (no value): print compact JSON payload to stdout
- `--summary-json artifacts/summary.json`: write JSON payload to file
- `--summary-json-pretty`: pretty-print summary JSON (`indent=2`) for stdout/file outputs
- `--summary-markdown artifacts/summary.md`: write a compact markdown summary for PR comments/release notes
- `--quiet`: suppress human-readable summary lines (useful when CI logs should only keep JSON/artifact paths)
- In CI, persist `.tmp/` summary artifacts (JSON + Markdown) with `actions/upload-artifact` so failed gates stay reviewable after the job exits.

Compact vs pretty smoke commands:

```bash
# compact JSON (single-line payload)
python3 -m prompt_regression_min run \
  -d examples/dataset/mixed_expectations.jsonl \
  -b examples/outputs/mixed_expectations.baseline.jsonl \
  -c examples/outputs/mixed_expectations.candidate.jsonl \
  --summary-json --quiet

# pretty JSON artifact (human diff-friendly)
python3 -m prompt_regression_min run \
  -d examples/dataset/mixed_expectations.jsonl \
  -b examples/outputs/mixed_expectations.baseline.jsonl \
  -c examples/outputs/mixed_expectations.candidate.jsonl \
  --summary-json artifacts/summary.pretty.json --summary-json-pretty
```

CI parity smoke (serializer drift guard):

```bash
python3 -m prompt_regression_min run \
  -d examples/dataset/mixed_expectations.jsonl \
  -b examples/outputs/mixed_expectations.baseline.jsonl \
  -c examples/outputs/mixed_expectations.candidate.jsonl \
  --summary-json .tmp/summary.compact.json --quiet

python3 -m prompt_regression_min run \
  -d examples/dataset/mixed_expectations.jsonl \
  -b examples/outputs/mixed_expectations.baseline.jsonl \
  -c examples/outputs/mixed_expectations.candidate.jsonl \
  --summary-json .tmp/summary.pretty.json --summary-json-pretty --quiet

python3 - <<'PY'
import json
from pathlib import Path

compact = json.loads(Path('.tmp/summary.compact.json').read_text(encoding='utf-8'))
pretty = json.loads(Path('.tmp/summary.pretty.json').read_text(encoding='utf-8'))
assert compact == pretty, 'compact/pretty summary payload mismatch'
PY
```

Payload shape:

```json
{
  "status": "PASS|FAIL",
  "fail_reasons": ["..."],
  "summary": {"...": "..."},
  "gates": {
    "max_regressions": 0,
    "max_regression_rate": null,
    "min_candidate_pass_rate": 0.0,
    "max_unchanged_fail": -1,
    "max_skipped_cases": -1,
    "min_delta_pass_rate_pp": null,
    "min_improved": 0,
    "max_changed_cases": -1,
    "max_changed_rate": null,
    "min_active_cases": 1,
    "max_filtered_out_cases": -1,
    "max_filtered_out_rate": null,
    "min_unchanged_pass": 0,
    "max_unchanged_pass": -1
  }
}
```

### Local test command

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*.py" -v
```

---

## Example Output

```text
prompt-regression-min summary
- cases: 3
- baseline: 3 (100.0%)
- candidate: 2 (66.7%)
- delta: -1 (-33.33pp)
- regressions: 1
- improved: 0
- unchanged: 2
- report: report.json
```

---

## CI/CD Integration

### CI artifact review walkthrough

If your workflow uploads `.tmp/` summary artifacts, use [`examples/ci_artifact_walkthrough.md`](examples/ci_artifact_walkthrough.md) as the reviewer playbook.
It shows what PASS vs FAIL summary JSON/Markdown artifacts look like and how to triage them quickly in pull requests.
The walkthrough now points at copyable fixture pairs (`walkthrough_pass_artifact_demo.*`, `walkthrough_fail_artifact_demo.*`) so reviewers can regenerate the documented artifacts exactly.

It also ships stable snapshot filenames under `examples/artifacts/` so docs can reference concrete PASS/FAIL artifact paths without depending on CI-only `.tmp/` names.
Both committed markdown snapshots retain `Summary schema version: 1` so reviewer-facing artifacts expose the same contract marker as JSON outputs.

Regenerate those committed walkthrough snapshots with one command:

```bash
./scripts/regenerate_walkthrough_artifacts.sh
```

Summary JSON now includes explicit parser metadata:

- `summary_schema_version`: stable schema marker for downstream CI parsers
- generated summary markdown now includes the same schema marker for human review parity
- `tool_version`: package version that produced the artifact

Use the generated report and fail deployment when regressions exceed your tolerance.

Example policy:

- block merge if `summary.regressions > 0`
- allow merge if regressions are zero and candidate pass rate is above threshold

This lets teams move fast while preserving quality guarantees.

---

## Development Direction

The project will be developed continuously with an MVP-first approach.

### Phase 1 (current)

- Deterministic baseline/candidate comparison
- Minimal scorer set
- CI-friendly behavior

### Phase 2

- Weighted case scoring
- Better case-level diff output
- Optional threshold flags (e.g., max allowed regressions)

### Phase 3

- Semantic similarity scorer (configurable)
- HTML report for team review
- GitHub Action wrapper for easy adoption

### Phase 4

- Domain packs (support, compliance, coding-assistant, etc.)
- Plugin interface for custom scorers
- Longitudinal quality trends across releases

---

## Quality and Contribution Guidelines

Contributions are welcome.

When proposing changes:

1. Keep behavior deterministic unless explicitly labeled experimental.
2. Add or update example cases for new scoring behavior.
3. Prefer readability over clever abstractions.
4. Document tradeoffs in PR descriptions.

Suggested commit style:

- `feat:` new capability
- `fix:` bug or correctness issue
- `docs:` documentation
- `refactor:` non-functional code changes

---

## FAQ

### Why not use semantic scoring only?

Semantic scoring is useful, but deterministic checks are easier to trust and debug.
`prompt-regression-min` starts with strict checks and can layer semantics later.

### Is this a benchmark framework?

Not exactly. It is a practical regression guard for day-to-day shipping.

### Can I use this for agents, not just prompts?

Yes. Any workflow producing text outputs can be compared via baseline/candidate files.

---

## License

MIT
