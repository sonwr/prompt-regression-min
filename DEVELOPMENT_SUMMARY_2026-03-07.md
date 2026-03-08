# Development Summary — 2026-03-07 (Run 00:52 UTC)

## Plan
1. Remove pytest dependency from tests to improve portability.
2. Add case-level outcome semantics for faster CI diagnosis.
3. Document the updated report/test workflow.

## Changes
- Reworked `tests/test_core.py` to built-in `unittest` (no external pytest dependency).
- Extended case report model in `src/prompt_regression_min/core.py`:
  - new per-case field: `outcome` (`regressed`, `improved`, `unchanged_pass`, `unchanged_fail`),
  - new summary field: `outcome_counts`.
- Updated `README.md`:
  - documented case `outcome` + summary `outcome_counts`,
  - added local test command using `python -m unittest`.

## Verification
- `PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*.py" -v` → PASS (2 tests)
- `PYTHONPATH=src python3 -m prompt_regression_min run -d examples/dataset/customer_support.jsonl -b examples/outputs/customer_support.baseline.jsonl -c examples/outputs/customer_support.candidate.jsonl` → expected FAIL (exit 1) due to intentional regressions in sample dataset.

## Next
- Add a compact `--strict` mode to fail on unchanged_fail above threshold.
- Add one end-to-end fixture that exercises all expectation types in one dataset.

---

## Run 01:22 UTC

### Plan
1. Add CI-friendly quality gate thresholds without changing deterministic scoring core.
2. Add CLI tests for new threshold behavior and input validation.
3. Update documentation for new run flags and exit behavior.

### Changes
- Extended `prm run` CLI options:
  - `--max-regressions` (default `0`)
  - `--min-candidate-pass-rate` (default `0.0`, range `[0.0, 1.0]`)
- Updated fail/pass logic to combine both thresholds into a single status decision.
- Added `tests/test_cli.py` covering:
  - configurable regression budget pass case,
  - candidate pass-rate threshold failure case,
  - invalid threshold argument error case.
- Updated `README.md` with new CLI options and revised exit code semantics.

### Verification
- `PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*.py" -v` → PASS (5 tests)

### Next
- Add `--strict` alias preset for common policy defaults (e.g., zero regressions + min pass-rate floor).
- Add a lightweight machine-readable CLI output mode (`--summary-json`) for pipeline parsing.

---

## Run 02:22 UTC

### Plan
1. Add a flexible expectation mode for synonym-style checks.
2. Validate new expectation schema constraints to keep scoring deterministic.
3. Update docs and tests so the behavior is immediately adoptable.

### Changes
- Added new expectation type `contains_any` in `src/prompt_regression_min/core.py`.
- Added schema validation for `contains_any.values` (must be non-empty list of non-empty strings).
- Added tests in `tests/test_core.py`:
  - `test_run_regression_supports_contains_any_expectation`
  - `test_run_regression_rejects_empty_contains_any_values`
- Updated `README.md` expectation list and JSON examples to include `contains_any`.

### Verification
- `PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*.py" -v` → PASS (9 tests)

### Next
- Add a fixture that combines `contains_any` with `not_contains` for policy-safe phrasing checks.
- Introduce `--summary-json` CLI output mode for CI parsers.

---

## Run 02:52 UTC

### Plan
1. Improve CI readability by surfacing case-outcome rollups in terminal output.
2. Keep quality-gate behavior unchanged while improving diagnostics.
3. Validate behavior with existing unit tests.

### Changes
- Updated `src/prompt_regression_min/cli.py` to print `outcome_counts` in CLI summary.
- Updated `README.md` to document terminal `outcome_counts` output.

### Verification
- `PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*.py" -v` → PASS (9 tests)

### Next
- Add `--summary-json` output mode for pipeline-friendly parsing.
- Add one fixture covering all expectation types in a single run.

---

## Run 03:22 UTC

### Plan
1. Add one new deterministic expectation type for prompt-regression checks.
2. Tighten web QA strict validation for failure recovery traceability.
3. Keep changes small, test-backed, and CI-friendly.

### Changes
- Added `starts_with` expectation type in `src/prompt_regression_min/core.py`.
- Added/updated tests in `tests/test_core.py` for `starts_with` pass/fail validation.
- Updated `README.md` to document `starts_with` in supported schema.

### Verification
- `PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*.py" -v` → PASS (11 tests)

### Next
- Add `ends_with` as a companion deterministic matcher if real datasets need suffix contracts.
- Add a single mixed fixture covering all expectation types in one run for docs + smoke testing.

---

## Run 03:52 UTC

### Plan
1. Stabilize local/CI test execution without relying on environment-specific `PYTHONPATH` setup.
2. Fix dataset/baseline alignment validation bug and extend coverage for ID mismatch paths.
3. Add a minimal CI workflow for deterministic unittest + CLI smoke checks.

### Changes
- Fixed duplicated `if missing_baseline_ids` block in `src/prompt_regression_min/core.py`.
- Updated test imports in `tests/test_core.py` and `tests/test_cli.py` to inject `src/` path explicitly.
- Added `tests/test_core.py` cases for:
  - missing baseline IDs,
  - extra/unknown candidate IDs.
- Added `.github/workflows/ci.yml`:
  - Python 3.12 setup,
  - unittest run,
  - module-entry smoke check.

### Verification
- `python3 -m unittest discover -s tests -p "test_*.py" -v` → PASS (13 tests)

### Next
- Add `--summary-json` output mode for CI parsers.
- Add one mixed fixture/example that demonstrates all supported expectation types in a single command.

---

## Run 04:22 UTC

### Plan
1. Add an extra CI policy gate for chronic unchanged failures.
2. Keep quality-gate semantics explicit and configurable from CLI.
3. Back the change with unittest coverage and docs updates.

### Changes
- Extended `prm run` in `src/prompt_regression_min/cli.py` with `--max-unchanged-fail`:
  - default `-1` (disabled),
  - non-negative values enforce an upper bound on `unchanged_fail`.
- Added argument validation (`--max-unchanged-fail >= -1`) and fail reason output.
- Added `tests/test_cli.py` coverage for:
  - threshold breach failure,
  - invalid `--max-unchanged-fail` argument.
- Updated `README.md` CLI reference and exit-gate semantics.

### Verification
- `python3 -m unittest discover -s tests -p "test_*.py" -q` → PASS (15 tests)

### Next
- Add `--summary-json` output mode for machine-readable CI parsing.
- Add a mixed example dataset/run demonstrating all expectation types + gate options.

---

## Run 04:52 UTC

### Plan
1. Add machine-readable CLI summary output for CI/pipeline parsers.
2. Support both stdout and file-path delivery without changing existing text summary behavior.
3. Add tests and docs so teams can adopt it immediately.

### Changes
- Added `--summary-json [path|-]` to `src/prompt_regression_min/cli.py`:
  - no value prints compact JSON payload to stdout,
  - path value writes formatted JSON to file.
- JSON payload includes `status`, `fail_reasons`, and `summary`.
- Added CLI tests:
  - `test_cli_emits_summary_json_to_stdout`
  - `test_cli_writes_summary_json_file`
- Updated `README.md` CLI reference and added a new machine-readable summary section.

### Verification
- `python3 -m unittest discover -s tests -p "test_*.py" -q` → PASS (17 tests)
- `PYTHONPATH=src python3 -m prompt_regression_min run -d examples/dataset/customer_support.jsonl -b examples/outputs/customer_support.baseline.jsonl -c examples/outputs/customer_support.candidate.jsonl --max-regressions 5 --summary-json` → PASS (text summary + JSON payload)

### Next
- Add a `--quiet` mode to emit only JSON for log-noise-sensitive CI stages.
- Add a mixed example fixture that demonstrates all expectation types and policy gates in a single run command.

---

## Run 05:22 UTC

### Plan
1. Add a deterministic suffix matcher to complement `starts_with`.
2. Keep schema validation strict for empty suffix expectations.
3. Update docs/tests to keep CLI and data format in sync.

### Changes
- Added `ends_with` expectation type in `src/prompt_regression_min/core.py`.
- Extended validation to require non-empty `expected.value` for `ends_with`.
- Added tests in `tests/test_core.py`:
  - `test_run_regression_supports_ends_with_expectation`
  - `test_run_regression_rejects_empty_ends_with_value`
- Updated `README.md` supported expectations and dataset JSON examples.

### Verification
- `python3 -m unittest discover -s tests -p "test_*.py" -v` → PASS (19 tests)

### Next
- Add one mixed fixture run that exercises all deterministic expectation types in a single command.
- Consider adding optional case-insensitive variants for `contains_*` matchers while preserving deterministic behavior.

## 2026-03-07 05:57 UTC (cron)

### Plan
1. Improve report ergonomics for CI consumers by exposing explicit unchanged buckets.
2. Tighten regex expectation validation parity with runtime scoring flags.

### Changes
- Updated `src/prompt_regression_min/core.py`:
  - Regex expected-pattern validation now compiles using declared `flags` (validation parity with scorer behavior).
  - Added top-level summary fields: `unchanged_pass`, `unchanged_fail`.
- Updated `src/prompt_regression_min/cli.py`:
  - Printed explicit `unchanged_pass` / `unchanged_fail` lines in terminal summary.
- Expanded tests:
  - `test_run_regression_summary_exposes_unchanged_buckets`
  - `test_run_regression_validates_regex_with_declared_flags`
  - CLI summary-json assertion now checks `summary.unchanged_fail` presence.
- Updated `README.md` to mention explicit unchanged counters in summaries.

### Validation
- `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py' -v`
- Result: 21 tests passed.

### Notes
- No breaking CLI flag changes; output is additive and backward-compatible.

## 2026-03-07 06:22 UTC (cron)

### Plan
1. Add a stricter deterministic matcher for exact-format text validation.
2. Keep docs/tests in lockstep for CI-safe rollout.

### Changes
- Added `regex_fullmatch` expectation type in `src/prompt_regression_min/core.py` (full-string regex match).
- Extended validation/scoring logic to treat `regex` and `regex_fullmatch` consistently with shared flag handling.
- Added core test `test_run_regression_supports_regex_fullmatch_expectation`.
- Updated `README.md` support matrix and dataset examples for `regex_fullmatch`.

### Validation
- `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py' -v`
- Result: 22 tests passed.

### Next
- Add a small fixture pack that demonstrates when `regex` passes but `regex_fullmatch` intentionally fails.

## 2026-03-07 06:52 UTC (cron)

### Plan
1. Add a deterministic multi-allowed exact matcher for enum-like outputs.
2. Keep schema validation strict and docs/tests in sync.

### Changes
- Added `equals_any` expectation type in `src/prompt_regression_min/core.py`:
  - passes when normalized output exactly matches one allowed value.
- Added validation for `equals_any.values` (must be non-empty list of non-empty strings).
- Added tests in `tests/test_core.py`:
  - `test_run_regression_supports_equals_any_expectation`
  - `test_run_regression_rejects_empty_equals_any_values`
- Updated `README.md` support matrix and dataset schema examples for `equals_any`.

### Validation
- `python3 -m unittest discover -s tests -q`
- Result: 24 tests passed.

### Next
- Add one mixed fixture dataset demonstrating `equals_any` with `regex_fullmatch` in a single CI smoke run.

## 2026-03-07 07:22 UTC (cron)

### Plan
1. Add a reusable mixed fixture pack for `equals_any` + `regex_fullmatch` smoke checks.
2. Lock behavior with a CLI-level fixture test and docs command.

### Changes
- Added fixture files:
  - `examples/dataset/mixed_expectations.jsonl`
  - `examples/outputs/mixed_expectations.baseline.jsonl`
  - `examples/outputs/mixed_expectations.candidate.jsonl`
- Added CLI test `test_cli_mixed_fixture_supports_equals_any_and_regex_fullmatch` in `tests/test_cli.py`.
- Updated `README.md` with a runnable mixed-fixture smoke command.

### Validation
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`
- Result: 25 tests passed.

### Next
- Add a companion failing mixed fixture where `regex` passes but `regex_fullmatch` fails, for policy-gate demos.

## 2026-03-07 07:52 UTC (cron)

### Plan
1. Add practical case-selection control to keep regression suites maintainable during iteration.
2. Keep summary/report outputs explicit about what was skipped.

### Changes
- Updated `src/prompt_regression_min/core.py`:
  - added optional dataset field `disabled` (boolean),
  - skipped cases are excluded from scoring but retained for ID-alignment validation,
  - summary now includes `dataset_cases`, `active_cases`, `skipped_cases`, `skipped_ids`,
  - raises clear error when all dataset cases are disabled.
- Updated `src/prompt_regression_min/cli.py` to print `skipped_cases` and `skipped_ids`.
- Added tests:
  - core: `test_run_regression_skips_disabled_cases_in_summary`, `test_run_regression_fails_when_all_cases_are_disabled`
  - cli: `test_cli_prints_skipped_case_counters`
- Updated `README.md` data-format section to document `disabled: true` behavior.

### Validation
- `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py' -v`
- `PYTHONPATH=src python3 -m prompt_regression_min run -d examples/dataset/mixed_expectations.jsonl -b examples/outputs/mixed_expectations.baseline.jsonl -c examples/outputs/mixed_expectations.candidate.jsonl --max-regressions 0 --summary-json`
- Result: 28 tests passed, mixed-fixture smoke run passed.

### Next
- Add `--include-disabled`/`--only-enabled` style selector flags for dataset slicing without editing files.
- Add one example dataset that demonstrates staged rollout with disabled cases.

---

## Run 08:22 UTC

### Plan
1. Add a new CI gate for pass-rate delta so teams can enforce non-regression or minimum uplift.
2. Add CLI tests for threshold behavior and invalid input guardrails.
3. Update docs to make the new gate operational immediately.

### Changes
- Added `--min-delta-pass-rate-pp` to `prm run` in `src/prompt_regression_min/cli.py`.
  - Supports explicit gate on `candidate_pass_rate - baseline_pass_rate` in percentage points.
  - Validation range: `[-100.0, 100.0]`.
  - Adds fail reason when delta is below threshold.
- Added CLI tests in `tests/test_cli.py`:
  - fails when delta gate is violated,
  - rejects invalid delta threshold.
- Updated `README.md` CLI reference and exit-code semantics for the new gate.

### Verification
- `python3 -m unittest discover -s tests -p 'test_*.py'` → PASS (30 tests)

### Next
- Add optional gate for minimum improvement case count (e.g., `--min-improved-cases`).
- Emit gate configuration in JSON summary payload for easier CI audit trails.

## 08:52 UTC - Skipped-case quality gate for CLI

Plan:
- Add a new optional quality gate to control disabled dataset drift in CI.
- Back it with CLI tests and docs updates.

Changes:
- Added `--max-skipped-cases` to `src/prompt_regression_min/cli.py` with argument validation and fail-reason integration.
- Added CLI tests:
  - `test_cli_fails_when_skipped_cases_exceed_threshold`
  - `test_cli_rejects_invalid_max_skipped_cases`
- Updated `README.md` CLI reference and exit code quality-gate description.

Validation:
- `PYTHONPATH=src python3 -m unittest tests.test_cli tests.test_core -v` (32 tests, PASS)


## 2026-03-07 09:22 UTC (cron)

### Plan
1. Add a new CI gate for minimum improved case count.
2. Keep gate behavior deterministic and test-covered.

### Changes
- Extended `prm run` in `src/prompt_regression_min/cli.py` with `--min-improved` (default `0`).
  - validates `--min-improved >= 0`,
  - fails quality gate when `summary.improved` is below threshold.
- Added CLI tests in `tests/test_cli.py`:
  - `test_cli_fails_when_improved_cases_below_threshold`
  - `test_cli_passes_when_improved_cases_meet_threshold`
  - `test_cli_rejects_invalid_min_improved`
- Updated `README.md` CLI reference and exit-code gate description to include `--min-improved`.

### Validation
- `python3 -m unittest tests/test_core.py tests/test_cli.py`
- Result: 35 tests passed.

### Next
- Add gate configuration echo in `--summary-json` payload for CI auditability.
- Add one docs example command showing combined usage of `--min-delta-pass-rate-pp` + `--min-improved`.

---

## Run 09:52 UTC

### Plan
1. Add a negative regex expectation for policy/safety style assertions.
2. Extend tests to cover the new scorer deterministically.
3. Document the new expectation in README.

### Changes
- Added `not_regex` expectation support in `src/prompt_regression_min/core.py`:
  - accepted in `SUPPORTED_EXPECTED_TYPES`,
  - validated with the same `pattern` + optional `flags` schema,
  - scored as PASS only when regex search does **not** match output.
- Added `test_run_regression_supports_not_regex_expectation` in `tests/test_core.py`.
- Updated `README.md` feature list + expectation examples with `not_regex` usage.

### Verification
- `python3 -m unittest -q tests/test_core.py tests/test_cli.py` → PASS (36 tests)

### Next
- Add one combined fixture dataset that uses `regex`, `regex_fullmatch`, and `not_regex` together for CI smoke coverage.
- Consider adding a CLI guard flag (e.g., `--max-policy-violations`) mapped to `not_regex` case IDs by tag.

---

## Run 10:22 UTC

### Plan
1. Expose unchanged failing case IDs in prompt-regression output for faster triage.
2. Keep compatibility by extending summary payload instead of changing existing fields.
3. Add unit tests to lock console and summary behavior.

### Changes
- Added `summary.unchanged_fail_ids` in `src/prompt_regression_min/core.py`.
- Updated CLI output in `src/prompt_regression_min/cli.py` to print `- unchanged_fail_ids: ...` when present.
- Added/updated tests:
  - `tests/test_core.py::test_run_regression_summary_exposes_unchanged_buckets` now verifies `unchanged_fail_ids`.
  - New `tests/test_cli.py::test_cli_prints_unchanged_fail_ids`.

### Verification
- `PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*.py" -v` → PASS (37 tests)

### Next
- Add optional machine-readable per-outcome ID slices (`regressed_ids`, `improved_ids`, `unchanged_fail_ids`) to a compact summary-only artifact mode.
- Add one fixture with multiple unchanged failures to verify deterministic ID ordering.

---

## Run 10:52 UTC

### Plan
1. Add case-insensitive deterministic expectation variants for common policy/content checks.
2. Extend mixed fixture assets to include one CI-style case.
3. Keep new behavior fully covered by unit tests.

### Changes
- Added new expectation types in `src/prompt_regression_min/core.py`:
  - `contains_all_ci`
  - `contains_any_ci`
  - `not_contains_ci`
- Extended expectation schema validation to support the new CI variants with the same non-empty list constraints.
- Added core tests:
  - `test_run_regression_supports_contains_all_ci_expectation`
  - `test_run_regression_supports_contains_any_ci_expectation`
  - `test_run_regression_supports_not_contains_ci_expectation`
- Updated docs in `README.md` (supported type list + JSON examples).
- Extended mixed fixture files with `mx-4` case using `not_contains_ci`.

### Verification
- `python3 -m unittest discover -s tests -p "test_*.py"` → PASS (40 tests)

### Next
- Add a dedicated CLI smoke command in README that demonstrates CI-style expectations + summary JSON output in one run.
- Consider optional normalizer hooks (e.g., whitespace collapsing) while preserving deterministic defaults.

## Run 11:22 UTC

### Plan
1. Add one deterministic case-insensitive enum matcher for prompt regression checks.
2. Extend tests/docs so teams can adopt it safely in CI.

### Changes
- Added `equals_any_ci` expectation type in `src/prompt_regression_min/core.py`.
- Added tests in `tests/test_core.py`:
  - `test_run_regression_supports_equals_any_ci_expectation`
  - `test_run_regression_rejects_empty_equals_any_ci_values`
- Updated `README.md` supported expectation list and schema examples.

### Verification
- `python3 -m unittest discover -s tests -v` → PASS (42 tests)

### Next
- Add a mixed fixture case that demonstrates `equals_any_ci` together with one strict CLI gate in a single smoke command.

## Run 11:52 UTC

### Plan
1. Add a full-string negative regex expectation to cover enum/policy rejection patterns.
2. Keep scoring + schema validation symmetric and test-covered.

### Changes
- Updated `src/prompt_regression_min/core.py`:
  - added `not_regex_fullmatch` to `SUPPORTED_EXPECTED_TYPES`.
  - implemented scorer behavior: PASS only when fullmatch does **not** occur.
  - extended schema validation path to accept and validate `not_regex_fullmatch` like other regex types.
- Added `test_run_regression_supports_not_regex_fullmatch_expectation` in `tests/test_core.py`.
- Updated `README.md` expectation matrix + JSON examples to include `not_regex_fullmatch`.

### Verification
- `python3 -m unittest tests.test_core tests.test_cli`
- Result: 43 tests passed.

### Next
- Add a mixed fixture row for `not_regex_fullmatch` and include a one-command CLI smoke example in README.

## Run 12:22 UTC

### Plan
1. Add an explicit active-coverage quality gate to prevent under-sized runs from passing.
2. Keep CLI behavior deterministic and fully test-backed.

### Changes
- Updated `src/prompt_regression_min/cli.py`:
  - added `--min-active-cases` (default: `1`).
  - added argument validation (`>= 1`).
  - quality gate now fails if `summary.active_cases` is below threshold.
- Added tests in `tests/test_cli.py`:
  - `test_cli_fails_when_active_cases_below_threshold`
  - `test_cli_rejects_invalid_min_active_cases`
- Updated `README.md`:
  - CLI reference now includes `--min-active-cases`.
  - exit-code policy section includes active-case threshold requirement.

### Verification
- `PYTHONPATH=src python3 -m unittest tests/test_cli.py -v`
- Result: PASS (19 tests)

### Next
- Add a short CI recipe in README showing `--min-active-cases` combined with `--max-skipped-cases` to enforce dataset coverage discipline.

## Run 12:52 UTC

### Plan
1. Add a normalized regression-rate metric for easier policy gating.
2. Expose the metric in CLI output and gate controls.
3. Keep docs/tests aligned with the new gate.

### Changes
- Updated `src/prompt_regression_min/core.py`:
  - summary now includes `regression_rate` (`regressions / active_cases`).
- Updated `src/prompt_regression_min/cli.py`:
  - added `--max-regression-rate` (optional, range `[0.0, 1.0]`).
  - prints `regression_rate` in human-readable summary.
  - fails quality gate when actual regression rate exceeds threshold.
- Added tests:
  - `tests/test_core.py`: asserts `summary.regression_rate`.
  - `tests/test_cli.py`:
    - `test_cli_fails_when_regression_rate_exceeds_threshold`
    - `test_cli_rejects_invalid_max_regression_rate`
- Updated `README.md` CLI reference and exit-policy description.

### Verification
- `PYTHONPATH=src python3 -m unittest discover -s tests -v`
- Result: PASS (47 tests)

### Next
- Add README policy examples combining `--max-regression-rate` with `--min-active-cases`.
- Consider emitting gate config values in summary JSON for audit-friendly CI traces.

---

## Run 13:22 UTC

### Plan
1. Add one new deterministic expectation operator for prompt regression scoring.
2. Add one stricter replay guard for web QA checkpoint logs.
3. Cover both with unittest + CLI JSON assertions.

### Changes
- Added `not_exact` expectation type to `src/prompt_regression_min/core.py` with schema validation and README examples.
- Added regression test coverage for `not_exact` in `tests/test_core.py`.
- Extended web QA validator with `--enforce-checkpoint-status-tokens`:
  - new validation path in `scripts/validate_web_qa_report.py`,
  - function tests in `tests/test_validate_web_qa_report.py`,
  - CLI JSON test in `tests/test_validate_web_qa_report_cli.py`,
  - documentation updates in `README.md` and `skills/web-qa-playwright/SKILL.md`.

### Verification
- `python3 -m unittest tests.test_core tests.test_cli` (prompt-regression-min) → PASS (48 tests)
- `python3 -m unittest tests.test_validate_web_qa_report tests.test_validate_web_qa_report_cli` (openclaw-codex-pm-skills) → PASS (37 tests)

### Next
- Add fixture-level examples showing `not_exact` + regex family in one mixed dataset.
- Add cross-check that checkpoint PASS/FAIL token aligns with checklist result token for the same check id.

## Run 13:52 UTC

### Plan
1. Add case-insensitive boundary matchers to reduce brittle casing regressions.
2. Extend deterministic schema validation for the new matcher types.
3. Update docs and verify with unit tests.

### Changes
- Added two new expectation types in `src/prompt_regression_min/core.py`:
  - `starts_with_ci`
  - `ends_with_ci`
- Extended validation to treat both as non-empty string `value` expectations.
- Added tests in `tests/test_core.py`:
  - `test_run_regression_supports_starts_with_ci_expectation`
  - `test_run_regression_supports_ends_with_ci_expectation`
- Updated `README.md` supported expectation list + data format examples.

### Verification
- `python3 -m unittest discover -s tests -p "test_*.py" -v` → PASS (50 tests)

### Next
- Add optional `equals_exact_ci` alias decision (or reject explicitly) after collecting user feedback.
- Add one mixed fixture case that demonstrates both new `_ci` boundary matchers in a single sample run.

## Run update (2026-03-07 14:xx UTC) — Changed-budget quality gates

Plan:
1. Add a blast-radius gate to prevent large, noisy candidate swings from silently passing relaxed regression thresholds.
2. Extend CLI + summary payload with changed-case metrics (`regressed + improved`) and add focused tests.
3. Update docs so CI users can immediately adopt the new knobs.

Changes:
- Added `summary.changed` and `summary.changed_rate` to `run_regression` output.
- Added new CLI gates:
  - `--max-changed-cases`
  - `--max-changed-rate`
- Added validation for the new flags and included changed metrics in terminal summary output.
- Added CLI tests for changed-case budget/rate failure paths and invalid rate handling.
- Updated README CLI reference + exit-code gate description + summary field note.

Verification:
- `python3 -m unittest discover -s tests -q` → PASS.

Notes:
- This run focused on deterministic rollout control in CI: teams can now cap total behavior churn even when regressions are budgeted.

## 2026-03-07 14:52 UTC (cron)

### Plan
1. Improve CI auditability of `--summary-json` output without changing scoring semantics.
2. Keep gate settings machine-readable so downstream parsers can explain PASS/FAIL decisions.

### Changes
- Updated `src/prompt_regression_min/cli.py`:
  - `--summary-json` payload now includes a `gates` object with the effective quality-gate config.
- Updated `tests/test_cli.py` to assert `gates` exists in stdout JSON payload.
- Updated `README.md` summary JSON schema to document the new `gates` object.

### Validation
- `python3 -m unittest tests.test_cli tests.test_core -v`
- Result: PASS.

### Next
- Add one fixture showcasing a FAIL payload where `fail_reasons` and `gates` are consumed together by CI.

## 2026-03-07 15:22 UTC (cron)

### Plan
1. Add a deterministic FAIL fixture for `--summary-json` auditability checks.
2. Verify fail payload includes both `fail_reasons` and effective `gates` settings.

### Changes
- Added FAIL fixture pack:
  - `examples/dataset/fail_payload_gate_demo.jsonl`
  - `examples/outputs/fail_payload_gate_demo.baseline.jsonl`
  - `examples/outputs/fail_payload_gate_demo.candidate.jsonl`
- Added CLI test `test_cli_fail_payload_fixture_exposes_fail_reasons_and_gates` in `tests/test_cli.py`.
- Updated `README.md` with a runnable FAIL payload fixture command and expected JSON assertions.

### Validation
- `python3 -m unittest tests/test_cli.py tests/test_core.py -v`
- Result: PASS (54 tests).

### Next
- Add one docs-level CI snippet (e.g., jq) that gates on both `status` and a specific `fail_reasons` token.

---

## Run 15:52 UTC

### Plan
1. Add case-insensitive substring expectation support for tolerant output assertions.
2. Validate the new scorer path with focused regression and schema tests.
3. Update docs so the new matcher is immediately usable in datasets.

### Changes
- Added `substring_ci` to supported expectation types in `src/prompt_regression_min/core.py`.
- Implemented scoring logic for `substring_ci` (`needle.lower() in output.lower()`).
- Extended dataset validation so `substring_ci` requires a non-empty `expected.value`.
- Added tests:
  - `tests/test_core.py::test_run_regression_supports_substring_ci_expectation`
  - `tests/test_core.py::test_run_regression_rejects_empty_substring_ci_value`
- Updated `README.md` scorer list and expectation examples with `substring_ci` usage.

### Verification
- `python3 -m unittest tests.test_core tests.test_cli` → PASS (56 tests)

### Next
- Add explicit `not_substring` / `not_substring_ci` expectation types to make negative matching more ergonomic than single-item `not_contains`.
- Add a compact fixture that demonstrates mixed case-insensitive matchers (`substring_ci`, `contains_any_ci`, `equals_any_ci`) in one dataset.

---

## Run 16:22 UTC

### Plan
1. Add case-insensitive exact matchers for stricter prompt regression contracts.
2. Cover the new matchers with deterministic core tests.
3. Update docs so schema adoption is immediate.

### Changes
- Added new expectation types in `src/prompt_regression_min/core.py`:
  - `exact_ci`
  - `not_exact_ci`
- Extended scoring and schema validation to support both matchers.
- Added tests in `tests/test_core.py`:
  - `test_run_regression_supports_exact_ci_expectation`
  - `test_run_regression_supports_not_exact_ci_expectation`
- Updated `README.md` supported expectation list and JSON snippets for both new types.

### Verification
- `python3 -m unittest tests/test_core.py tests/test_cli.py` → PASS (58 tests)

### Next
- Add a small mixed fixture that demonstrates `exact_ci` + `not_exact_ci` together in one CI-friendly run.
- Consider adding a normalization policy toggle (`--trim-output`/`--no-trim-output`) for explicit whitespace contracts.

## Session 16:53 UTC

### Plan
- Close a validation consistency gap for case-insensitive prefix/suffix expectations.
- Add regression tests and align README wording with enforced constraints.

### Changes
- Fixed expectation validation in `src/prompt_regression_min/core.py`:
  - `starts_with_ci` and `ends_with_ci` now require non-empty `expected.value`, matching the already-enforced behavior of `starts_with`/`ends_with`.
- Added tests in `tests/test_core.py`:
  - `test_run_regression_rejects_empty_starts_with_ci_value`
  - `test_run_regression_rejects_empty_ends_with_ci_value`
- Updated README expectation reference:
  - Clarified that `starts_with_ci` requires a non-empty prefix and `ends_with_ci` requires a non-empty suffix.

### Verification
- `python3 -m unittest -q tests/test_core.py tests/test_cli.py`
- Result: `Ran 60 tests ... OK`

### Outcome
- Upgrade delivered: case-insensitive prefix/suffix rules now enforce deterministic, non-trivial expectations.
- Documentation and tests now reflect runtime behavior exactly.

---

## Run 17:22 UTC

### Plan
1. Add deterministic case-sharding support to CLI runs without editing dataset files.
2. Strengthen strict QA validator evidence guarantees for failed checks.
3. Cover both additions with unit tests and README updates.

### Changes
- Added ID-regex selection controls to `prompt-regression-min`:
  - `--include-id-regex`
  - `--exclude-id-regex`
- Extended `run_regression(...)` in `src/prompt_regression_min/core.py` with filter-aware selection and new summary fields:
  - `id_filter_include_regex`, `id_filter_exclude_regex`
  - `filtered_out_cases`, `filtered_out_ids`
- Updated CLI output + `--summary-json` payload gates to include filter configuration.
- Added tests in `tests/test_core.py` and `tests/test_cli.py` for:
  - include/exclude ID filtering behavior,
  - empty selection handling,
  - invalid regex handling.
- Updated `README.md` CLI reference to document case-ID regex filters.

### Verification
- `python3 -m unittest tests.test_core tests.test_cli` → PASS (64 tests)

### Skill principles applied
- Applied Playwright-interactive style reproducibility discipline by adding deterministic shard controls (`--include-id-regex` / `--exclude-id-regex`) and explicit filter metadata in machine-readable outputs.

### Next
- Add `--case-id-file` support for explicit case allowlists to enable stable nightly shard orchestration across CI providers.

## Run 17:52 UTC

### Plan
1. Add a guardrail for over-filtered shard runs so CI can enforce minimum dataset coverage.
2. Keep machine-readable output audit-friendly by surfacing the new gate in summary JSON.
3. Verify behavior with focused CLI tests.

### Changes
- Updated `src/prompt_regression_min/cli.py`:
  - added `--max-filtered-out-cases` (default `-1`, disabled),
  - added argument validation (`>= -1`),
  - fail gate now triggers when `summary.filtered_out_cases` exceeds threshold,
  - included gate in `--summary-json` payload under `gates.max_filtered_out_cases`.
- Added tests in `tests/test_cli.py`:
  - `test_cli_fails_when_filtered_out_cases_exceed_threshold`
  - `test_cli_rejects_invalid_max_filtered_out_cases`
- Updated `README.md` CLI/exit-policy/JSON payload docs for the new gate.

### Verification
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`
- Result: PASS (66 tests).

### Skill principles applied
- Applied deterministic, reproducible gate design by making shard-filter blast radius explicit and machine-verifiable in CI payloads.

### Next
- Add `--min-filtered-in-cases` (or `--min-active-cases` recipe docs) for teams that prefer positive coverage constraints.
- Add a CI snippet that blocks when both filtered-out and skipped-case budgets are exceeded.

## Run 18:22 UTC

### Plan
1. Extend expectation vocabulary with readability aliases while keeping deterministic scoring semantics unchanged.
2. Validate the aliases with regression-core tests.
3. Update docs so CI users can adopt aliases without migration risk.

### Changes
- Updated `src/prompt_regression_min/core.py`:
  - added `contains_none` and `contains_none_ci` as supported expectation types,
  - implemented them as semantic aliases of `not_contains` / `not_contains_ci`,
  - wired validation rules so aliases require non-empty string `values` lists.
- Added coverage in `tests/test_core.py`:
  - `test_run_regression_supports_contains_none_expectation`
  - `test_run_regression_supports_contains_none_ci_expectation`
- Updated `README.md` expectation catalog and examples with alias guidance.

### Verification
- `python3 -m unittest discover -s tests -q` → PASS (68 tests)

### Skill principles applied
- Applied deterministic/reproducible scoring principles by adding human-readable expectation aliases that map to existing evaluator behavior with identical pass/fail semantics.

### Next
- Add `not_contains_all` / `not_contains_any` style operators only if they introduce genuinely distinct semantics (not aliases).

## Run 18:52 UTC

### Plan
1. Improve dataset integrity checks by rejecting blank/whitespace case IDs early.
2. Cover ID validation with deterministic core tests and document the rule.

### Changes
- Updated `src/prompt_regression_min/core.py`:
  - `_index_rows_by_id(...)` now rejects empty/whitespace IDs in dataset/baseline/candidate rows.
- Added tests in `tests/test_core.py`:
  - `test_run_regression_rejects_empty_dataset_id`
  - `test_run_regression_rejects_empty_baseline_id`
- Updated `README.md` data-format section with a new invariant: IDs must be non-empty, non-whitespace strings.

### Verification
- `python3 -m unittest discover -s tests -p 'test_*.py' -v` → PASS (70 tests)

### Skill principle alignment
- Applied reproducibility/stability principles by adding deterministic input validation that prevents ambiguous ID mapping before scoring.

### Next
- Add `test_run_regression_rejects_empty_candidate_id` for full symmetry across all three files.

## Run 19:22 UTC

### Plan
1. Improve summary determinism for CI diff stability.
2. Keep ID-list output order reproducible regardless of dataset declaration order.

### Changes
- Updated `src/prompt_regression_min/core.py` summary assembly:
  - `filtered_out_ids`, `skipped_ids`, `regression_ids`, `improved_ids`, `unchanged_fail_ids` are now sorted before emission.
- Updated tests:
  - `tests/test_core.py::test_run_regression_filters_cases_by_include_exclude_regex` expected sorted `filtered_out_ids`.
  - Added `tests/test_core.py::test_run_regression_sorts_summary_id_lists_for_reproducibility`.

### Verification
- `python3 -m unittest tests.test_core tests.test_cli` → PASS (71 tests)

### Skill principle alignment
- Applied reproducibility-first principle by normalizing summary ID ordering for stable machine parsing and deterministic CI diffs.

## Run 19:52 UTC

### Plan
1. Add a stability gate that protects unchanged passing coverage.
2. Keep CLI/docs/tests aligned for deterministic CI behavior.

### Changes
- Updated `src/prompt_regression_min/cli.py`:
  - Added `--min-unchanged-pass` (default `0`) to require a minimum count of `unchanged_pass` cases.
  - Added argument validation (`>= 0`) and fail-reason emission when unmet.
  - Included the new gate in `--summary-json` payload (`gates.min_unchanged_pass`).
- Updated `tests/test_cli.py`:
  - Added `test_cli_fails_when_unchanged_pass_below_threshold`.
  - Added `test_cli_rejects_invalid_min_unchanged_pass`.
- Updated `README.md` usage and exit-code gate summary to document `--min-unchanged-pass`.

### Verification
- `python3 -m unittest -q tests/test_core.py tests/test_cli.py` → PASS (73 tests)

### Skill principle alignment
- Applied reproducibility + stability principles by adding an explicit guardrail that preserves deterministic unchanged-pass baseline coverage.

## Run Update (UTC 2026-03-07 20:23)

### Plan (1-3 lines)
- Add one practical gate to constrain uncontrolled behavior drift.
- Ensure the new gate is validated at CLI level (pass/fail + invalid argument handling).
- Keep docs in sync with CLI contract.

### Changes completed
- Added `--max-improved` gate in `src/prompt_regression_min/cli.py` (default `-1` disabled).
- Added fail reason when improved cases exceed configured maximum.
- Added argument validation for invalid values (`< -1`).
- Included `max_improved` in `--summary-json` gate payload.
- Added/updated CLI tests in `tests/test_cli.py` for exceed/invalid scenarios.
- Updated README usage and gate semantics to include `--max-improved`.

### Verification
- `python3 -m unittest -q tests.test_core tests.test_cli` ✅ (75 tests passed)

### Blockers / next priority
- No blocker. Next run should add a fixture-driven CI smoke command demonstrating combined `--min-improved` + `--max-improved` band gating.

## Run 20:53 UTC

### Plan
1. Add one complementary stability gate for unchanged passing cases.
2. Keep CLI/test/docs contracts synchronized for CI adoption.

### Changes
- Updated `src/prompt_regression_min/cli.py`:
  - added `--max-unchanged-pass` (default `-1`, disabled),
  - added validation (`>= -1`),
  - added fail reason when unchanged-pass cases exceed threshold,
  - added `max_unchanged_pass` to `--summary-json` gate payload.
- Added tests in `tests/test_cli.py`:
  - `test_cli_fails_when_unchanged_pass_exceeds_threshold`,
  - `test_cli_rejects_invalid_max_unchanged_pass`.
- Updated `README.md` CLI reference, exit-policy text, and summary JSON schema with the new gate.

### Verification
- `python3 -m unittest discover -s tests -q` → PASS (77 tests)

### Skill principle alignment
- Applied deterministic/stability-first CI gating by bounding unchanged-pass volume explicitly and exposing the gate in machine-readable output.

### Next
- Add a fixture-driven CI example that demonstrates `--min-unchanged-pass` and `--max-unchanged-pass` as a bounded band policy.

## 2026-03-07 21:23 UTC (cron)

### Plan
1. Add a fixture-driven unchanged-pass band policy example for CI (`min=max`).
2. Lock the behavior with a CLI test and README command.

### Changes
- Added fixture pack:
  - `examples/dataset/unchanged_pass_band_demo.jsonl`
  - `examples/outputs/unchanged_pass_band_demo.baseline.jsonl`
  - `examples/outputs/unchanged_pass_band_demo.candidate.jsonl`
- Added CLI test `test_cli_fixture_unchanged_pass_band_policy_passes` in `tests/test_cli.py`.
- Updated `README.md` with a runnable unchanged-pass band command and expected JSON gate assertions.

### Validation
- `python3 -m unittest tests/test_core.py tests/test_cli.py -q`
- Result: PASS (78 tests).

### Skill principle alignment
- Applied deterministic/stability principles by adding a fixture-backed bounded unchanged-pass policy and verifying gate echoes in machine-readable JSON output.


## 2026-03-07 21:53 UTC (cron)

### Plan
1. Add a fixture-backed improved-band CI policy example (`min=max`) to constrain behavior churn.
2. Wire the new fixture into CLI tests, docs, and GitHub Actions smoke checks.

### Changes
- Added fixture pack:
  - `examples/dataset/improved_band_demo.jsonl`
  - `examples/outputs/improved_band_demo.baseline.jsonl`
  - `examples/outputs/improved_band_demo.candidate.jsonl`
- Added CLI test `test_cli_fixture_improved_band_policy_passes` in `tests/test_cli.py`.
- Updated CI workflow (`.github/workflows/ci.yml`) with improved-band smoke command.
- Updated `README.md` with runnable improved-band fixture command and expected JSON gate assertions.

### Validation
- `python3 -m unittest discover -s tests -p "test_*.py" -q`
- Result: PASS (79 tests).

### Skill principle alignment
- Applied deterministic/stability-first validation by adding an exact improved-case band fixture and enforcing the policy via automated smoke + machine-readable gate checks.

## 2026-03-07 22:23 UTC (cron)

### Plan
1. Add a proportional stale-failure quality gate to reduce unchanged failing-case drift.
2. Cover the new gate in CLI/core tests and document it in the CLI reference.

### Changes
- Updated `src/prompt_regression_min/core.py`:
  - Added `summary.unchanged_fail_rate` for machine-readable stale-failure tracking.
- Updated `src/prompt_regression_min/cli.py`:
  - Added `--max-unchanged-fail-rate` (range: `0.0..1.0`).
  - Added input validation, summary printout, and fail-reason evaluation for unchanged fail rate budget.
  - Added gate echo for `max_unchanged_fail_rate` in `--summary-json` output.
- Updated tests:
  - `tests/test_core.py`: assert `unchanged_fail_rate` is exposed in summary.
  - `tests/test_cli.py`: added failure/validation coverage for `--max-unchanged-fail-rate`.
- Updated docs:
  - `README.md`: CLI usage and exit-code gate description now include `--max-unchanged-fail-rate`.

### Validation
- `python3 -m unittest tests.test_core tests.test_cli`
- Result: PASS (81 tests).

### Skill principle alignment
- Applied deterministic, parser-safe policy gating by adding a bounded unchanged-fail-rate control with reproducible JSON gate echoes and fixture-style test coverage.

## 2026-03-07 22:53 UTC (cron)

### Plan
1. Tighten filtered-shard auditability with a proportional gate.
2. Fix dataset accounting so filtered-case metrics are computed from original dataset size.
3. Keep behavior test-backed and CI-friendly.

### Changes
- Updated `src/prompt_regression_min/core.py`:
  - `summary.dataset_cases` now reflects original dataset size before ID regex filtering,
  - added `summary.selected_dataset_cases`,
  - added `summary.filtered_out_rate` (`filtered_out_cases / dataset_cases`).
- Updated `src/prompt_regression_min/cli.py`:
  - added `--max-filtered-out-rate` gate (range `0.0..1.0`),
  - prints `filtered_out_rate` in human summary,
  - emits `gates.max_filtered_out_rate` in `--summary-json` payload.
- Added tests:
  - `tests/test_core.py` assertions for corrected dataset accounting + `filtered_out_rate`,
  - `tests/test_core.py::test_run_regression_rejects_empty_candidate_id` (ID validation symmetry),
  - `tests/test_cli.py` pass/fail/validation coverage for `--max-filtered-out-rate`,
  - updated CLI summary assertion to include `filtered_out_rate` line.
- Updated `README.md` CLI reference, gate semantics, and JSON schema snippets for `--max-filtered-out-rate`.

### Validation
- `python3 -m unittest tests/test_core.py tests/test_cli.py -q`
- Result: PASS (84 tests).

### Skill principle alignment
- Applied reproducibility-first principles by making shard-filter blast radius measurable (`filtered_out_rate`) and enforceable via deterministic CI gates.

### Next
- Add a fixture-driven smoke command demonstrating `--max-filtered-out-cases` + `--max-filtered-out-rate` together in one policy profile.

## 2026-03-07 23:23 UTC (cron)

### Plan
1. Add a fixture-backed shard policy smoke example for filtered-out case budget/rate gates.
2. Lock behavior with a CLI fixture test and README command.

### Changes
- Added fixture pack:
  - `examples/dataset/filtered_out_band_demo.jsonl`
  - `examples/outputs/filtered_out_band_demo.baseline.jsonl`
  - `examples/outputs/filtered_out_band_demo.candidate.jsonl`
- Added CLI test `test_cli_fixture_filtered_out_band_policy_passes` in `tests/test_cli.py`.
- Updated `README.md` with a runnable filtered-out band command and expected JSON gate assertions.

### Validation
- `python3 -m unittest tests/test_core.py tests/test_cli.py -q`
- Result: PASS (85 tests).

### Skill principle alignment
- Applied deterministic/reproducible policy-gate principles by adding a fixture-driven shard budget profile with machine-verifiable gate echoes.

## 2026-03-08T00:00Z — Iteration: upper-bound pass-rate delta gate

Plan
- Add a new CLI gate to cap unexpectedly large pass-rate swings.
- Keep behavior deterministic and machine-readable by adding the gate to fail reasons + summary-json payload.
- Add focused tests and README updates.

Changes
- Added `--max-delta-pass-rate-pp` to `src/prompt_regression_min/cli.py`.
- Added argument validation (`-100.0..100.0`) and fail-reason logic when delta exceeds the configured max.
- Included the new gate in `--summary-json` payload under `gates.max_delta_pass_rate_pp`.
- Added tests in `tests/test_cli.py` for both fail-path and invalid-argument path.
- Updated usage/help text in `README.md`.

Verification
- `python3 -m unittest -v tests.test_cli`
- Result: PASS (44 tests)
