# Development Summary — 2026-03-08

## Run @ 04:53 UTC (cron)

### Plan
- Add one small but practical CLI gate for release-policy expressiveness.
- Cover it with focused CLI tests and README updates.

### Changes
- Added CLI gate: `--require-pass-rate-trend <improving|flat|regressing>` in `src/prompt_regression_min/cli.py`.
- Added failure condition when computed `summary.pass_rate_trend` does not match required value.
- Included `require_pass_rate_trend` in machine-readable `gates` payload.
- Added tests in `tests/test_cli.py`:
  - mismatch fails,
  - matching trend passes,
  - summary JSON gate exposure.
- Updated `README.md` CLI reference and gate semantics.

### Verification
- `python3 -m unittest tests.test_core tests.test_cli`
- Result: **PASS** (106 tests)

### Blockers
- `pytest` is unavailable in host PATH (`pytest: command not found`), so validation used `python3 -m unittest`.

### Next
- Add a fixture-driven example for `--require-pass-rate-trend` (flat-only policy) under `examples/`.

## Run @ 05:23 UTC (cron)

### Plan
- Add one small CLI feature that improves machine-readable output ergonomics for CI debugging.
- Cover the behavior with focused unit tests and README updates.

### Changes
- Added `--summary-json-pretty` to `src/prompt_regression_min/cli.py`.
  - Pretty-prints summary payloads (indent=2) for both stdout (`--summary-json`) and file outputs (`--summary-json <path>`).
- Added test `test_cli_emits_pretty_summary_json_to_stdout` in `tests/test_cli.py`.
- Updated `README.md` usage and machine-readable summary docs with the new flag.

### Verification
- `python3 -m unittest discover -s tests -q`
- Result: **PASS** (107 tests)

### Blockers
- `pytest` is unavailable in host PATH (`pytest: command not found`), so validation uses `unittest`.

### Next
- Add fixture examples showing compact vs pretty summary JSON outputs in CI artifacts.

## Run @ 05:53 UTC (cron)

### Plan
- Close the previous TODO by adding compact-vs-pretty summary smoke examples.
- Add one test that verifies pretty formatting when writing summary JSON to a file.

### Changes
- Added `test_cli_writes_pretty_summary_json_file` in `tests/test_cli.py`.
- Updated `README.md` machine-readable summary section with compact stdout and pretty artifact smoke commands.

### Verification
- `python3 -m unittest tests.test_core tests.test_cli`
- Result: **PASS** (108 tests)

### Blockers
- `pytest` is unavailable in host PATH (`pytest: command not found`), so validation continues via `unittest`.

### Next
- Add a fixture-focused CI snippet that diffs compact vs pretty summary payloads to catch accidental serializer drift.

## Run @ 06:23 UTC (cron)

### Plan
- Implement the pending CI drift guard for compact vs pretty summary JSON serializers.
- Keep docs + workflow behavior aligned with one reproducible smoke check.

### Changes
- Updated `.github/workflows/ci.yml` with a new job step:
  - generate compact summary JSON,
  - generate pretty summary JSON,
  - assert payload parity (`json.loads`) and indentation marker presence.
- Updated `README.md` with the same serializer-parity smoke snippet under machine-readable summary guidance.

### Verification
- `python3 -m unittest discover -s tests -v`
- `PYTHONPATH=src python3 -m prompt_regression_min run ... --summary-json .tmp/summary.compact.json --quiet`
- `PYTHONPATH=src python3 -m prompt_regression_min run ... --summary-json .tmp/summary.pretty.json --summary-json-pretty --quiet`
- `python3` parity assert script (`serializer parity: PASS`)
- Result: **PASS** (108 tests + smoke parity pass)

### Blockers
- `pytest` is unavailable in host PATH (`pytest: command not found`), so verification continues with `unittest` + smoke commands.

### Next
- Add one CLI option to emit summary schema version for downstream long-term parser compatibility.

## Run @ 06:53 UTC (cron)

### Plan
- Add one PR-friendly output artifact so CI jobs can post readable summaries without parsing JSON.
- Cover the new behavior with focused CLI tests and README docs.

### Changes
- Added `--summary-markdown <path>` to `src/prompt_regression_min/cli.py`.
  - Writes compact markdown summary with status, case counters, pass-rate delta, and outcomes.
  - Includes fail reason bullets when gates fail.
- Added tests in `tests/test_cli.py`:
  - `test_cli_writes_summary_markdown_file`
  - `test_cli_summary_markdown_includes_fail_reasons`
- Updated `README.md` usage + machine-readable summary section with `--summary-markdown`.

### Verification
- `python3 -m unittest discover -s tests -q`
- Result: **PASS** (110 tests)

### Blockers
- `pytest` is unavailable in host PATH (`pytest: command not found`), so validation continues via `unittest`.

### Next
- Add `--summary-markdown-template` support for teams that want custom markdown headings/ordering while preserving parser-safe defaults.

## Run @ 07:23 UTC (cron)

### Plan
- Increase CI fixture realism coverage beyond unit tests.
- Ensure one expected-fail fixture is explicitly asserted in workflow smoke checks.

### Changes
- Updated `.github/workflows/ci.yml`:
  - Added filtered-out gate smoke fixture (`filtered_out_band_demo`).
  - Added expected-fail smoke fixture (`fail_payload_gate_demo`) that must return non-zero when gate fails.

### Verification
- `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py' -v`
- Result: **PASS** (110 tests)

### Blockers
- None.

### Next
- Add CI artifact upload for summary JSON/Markdown files to improve PR triage visibility.

## Run @ 08:23 UTC (cron)

### Plan
- Finish the pending CI artifact visibility TODO for failed/passing summary outputs.
- Keep README guidance aligned with the new artifact retention behavior.

### Changes
- Updated `.github/workflows/ci.yml` to:
  - persist expected-fail summary JSON + Markdown artifacts under `.tmp/`,
  - assert those FAIL artifacts are populated,
  - upload `.tmp/` via `actions/upload-artifact@v4` with `if: always()`.
- Updated `README.md` machine-readable summary guidance with CI artifact retention advice for `.tmp/` outputs.

### Verification
- `PYTHONPATH=src python3 -m unittest discover -s tests -q`
- `PYTHONPATH=src python3 -m prompt_regression_min run ... --summary-json .tmp/fail-summary.json --summary-markdown .tmp/fail-summary.md` (expected non-zero)
- Result: **PASS** (112 tests + expected FAIL artifact smoke pass)

### Blockers
- `pytest` is still unavailable in host PATH, so validation continues via `unittest` + smoke commands.

### Next
- Add an examples/artifacts walkthrough that shows what uploaded PASS vs FAIL summaries look like in CI for reviewer triage.

## Run @ 09:00 UTC (cron)

### Plan
- Close the pending reviewer-triage TODO with one concrete artifact walkthrough.
- Keep README navigation aligned so CI users can find the example quickly.

### Changes
- Added `examples/ci_artifact_walkthrough.md` with PASS vs FAIL summary artifact examples, reviewer triage flow, and a PR note template.
- Updated `README.md` CI/CD section to link directly to the walkthrough as the reviewer playbook for uploaded `.tmp/` artifacts.

### Verification
- `PYTHONPATH=src python3 -m unittest discover -s tests -v`
- Result: **PASS** (112 tests)

### Blockers
- `pytest` is still unavailable in host PATH, so validation continues via `unittest`.

### Next
- Add one downloadable fixture pair whose generated summary artifacts exactly match the walkthrough screenshots/snippets.

## Run @ 09:10 UTC (cron)

### Plan
- Finish the walkthrough TODO by shipping copyable PASS/FAIL fixture pairs.
- Lock the documented IDs with fixture-based CLI tests and update README navigation.

### Changes
- Added walkthrough fixture pairs:
  - `examples/dataset/walkthrough_pass_artifact_demo.jsonl`
  - `examples/outputs/walkthrough_pass_artifact_demo.{baseline,candidate}.jsonl`
  - `examples/dataset/walkthrough_fail_artifact_demo.jsonl`
  - `examples/outputs/walkthrough_fail_artifact_demo.{baseline,candidate}.jsonl`
- Updated `examples/ci_artifact_walkthrough.md` so its PASS/FAIL commands now point at those downloadable fixtures.
- Added CLI tests that assert the documented `improved_ids` (`checkout-copy`) and `regression_ids` (`auth-login`) stay stable.
- Updated `README.md` CI artifact walkthrough note to mention the reproducible fixture pairs.

### Verification
- `PYTHONPATH=src python3 -m unittest tests.test_core tests.test_cli`
- Result: **PASS** (114 tests)

### Blockers
- `pytest` is still unavailable in host PATH, so verification continues via `unittest`.

### Next
- Add a tiny smoke script/CI step that regenerates the walkthrough PASS/FAIL summary artifacts into `.tmp/` and diffs key IDs against the docs.

## Run @ 09:20 UTC (cron)

### Plan
- Close the walkthrough-artifact TODO by pinning the documented PASS/FAIL fixture pair in CI.
- Re-verify the documented improved/regression IDs through real summary artifact generation.

### Changes
- Updated `.github/workflows/ci.yml` with a new walkthrough smoke step.
- CI now regenerates PASS/FAIL summary JSON + Markdown artifacts for the documented walkthrough fixtures and asserts:
  - PASS fixture keeps `improved_ids == ['checkout-copy']`
  - FAIL fixture keeps `regression_ids == ['auth-login']`
  - FAIL markdown artifact still mentions `auth-login`

### Verification
- `PYTHONPATH=src python3 -m unittest tests.test_core tests.test_cli`
- PASS/FAIL walkthrough artifact smoke commands (JSON + Markdown generation)
- Result: **PASS** (114 tests + walkthrough artifact alignment smoke pass)

### Blockers
- `pytest` is still unavailable in host PATH, so verification continues via `unittest` + smoke commands.

### Next
- Add a tiny docs-linked artifact snapshot example (`examples/artifacts/`) so the walkthrough references stable generated filenames as well as stable IDs.

## Run @ 09:30 UTC (cron)

### Plan
- Close the pending docs-linked artifact snapshot TODO with committed PASS/FAIL walkthrough outputs.
- Keep CI and README aligned around stable snapshot filenames instead of CI-only `.tmp/` paths.

### Changes
- Added committed walkthrough artifact snapshots under `examples/artifacts/`:
  - `walkthrough-pass.summary.json`
  - `walkthrough-pass.summary.md`
  - `walkthrough-fail.summary.json`
  - `walkthrough-fail.summary.md`
- Updated `examples/ci_artifact_walkthrough.md` and `README.md` to reference the stable snapshot filenames.
- Updated `.github/workflows/ci.yml` with a smoke check that validates the committed snapshot payloads stay aligned with documented PASS/FAIL IDs and markdown status text.

### Verification
- `PYTHONPATH=src python3 -m prompt_regression_min run ... --summary-json examples/artifacts/walkthrough-pass.summary.json --summary-markdown examples/artifacts/walkthrough-pass.summary.md --quiet`
- `PYTHONPATH=src python3 -m prompt_regression_min run ... --max-regressions 0 --summary-json examples/artifacts/walkthrough-fail.summary.json --summary-markdown examples/artifacts/walkthrough-fail.summary.md --quiet` (expected FAIL)
- `PYTHONPATH=src python3 -m unittest tests.test_core tests.test_cli`
- Result: **PASS** (114 tests + committed snapshot verification pass)

### Blockers
- `pytest` is still unavailable in host PATH, so validation continues via `unittest` + CLI smoke commands.

### Next
- Add a tiny regeneration helper script for `examples/artifacts/` so contributors can refresh committed snapshot outputs with one copy-paste command.

## Run @ 09:40 UTC (cron)

### Plan
- Close the committed-artifact refresh TODO with one copy-paste regeneration helper.
- Wire the helper into docs and CI so snapshot refresh stays reproducible.

### Changes
- Added `scripts/regenerate_walkthrough_artifacts.sh` to regenerate committed PASS/FAIL walkthrough summary artifacts under `examples/artifacts/`.
- Updated `README.md` and `examples/ci_artifact_walkthrough.md` to document the one-command regeneration flow.
- Updated `.github/workflows/ci.yml` so the committed snapshot smoke step now runs the helper before asserting stable IDs/status text.

### Verification
- `PYTHONPATH=src python3 -m unittest tests.test_core tests.test_cli`
- `./scripts/regenerate_walkthrough_artifacts.sh`
- Result: **PASS** (114 tests + walkthrough artifact regeneration pass)

### Blockers
- `pytest` is still unavailable in host PATH, so validation continues via `unittest` + CLI smoke commands.

### Next
- Add a tiny helper/test that diffs regenerated walkthrough artifacts against repo-tracked snapshots and prints a contributor-friendly drift summary when docs/examples go stale.

## Run @ 09:50 UTC (cron)

### Plan
- Close the pending snapshot-refresh TODO with one drift-detection helper around committed walkthrough artifacts.
- Keep docs/CI/examples aligned with a contributor-friendly regeneration + diff flow.

### Changes
- Added a walkthrough artifact drift helper (script + docs wiring) so contributors can compare regenerated PASS/FAIL summary artifacts against committed snapshots before pushing docs changes.
- Extended `README.md`, `examples/ci_artifact_walkthrough.md`, and tests to keep the artifact refresh path reproducible and parser-safe.
- Re-ran the full unittest suite to confirm the expanded CLI/core surface still holds.

### Verification
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`
- Result: **PASS** (114 tests)

### Blockers
- `pytest` is still unavailable in host PATH, so validation continues via `unittest`.

### Next
- Add a small schema/version marker to summary JSON or drift helper output so downstream CI parsers can detect format changes explicitly.


## Run @ 10:20 UTC (cron)

### Plan
- Add one tiny human-readable schema signal so markdown summaries expose the same contract version as JSON outputs.
- Re-run CLI/core tests to keep reviewer-facing artifacts parser-safe and docs-aligned.

### Changes
- Added `Summary schema version: 1` to `--summary-markdown` output in `src/prompt_regression_min/cli.py`.
- Extended `tests/test_cli.py` to pin the new markdown marker.
- Updated `README.md` machine-readable summary guidance to note markdown/JSON schema-marker parity.

### Verification
- `python3 -m unittest tests.test_core tests.test_cli`
- Result: **PASS**

### Blockers
- `pytest` is still unavailable in host PATH, so validation continues via `unittest`.

### Next
- Add one fixture-level smoke check that the committed markdown walkthrough snapshots retain the schema marker after regeneration.

## Run @ 10:30 UTC (cron)

### Plan
- Close the markdown-schema-marker TODO by asserting committed walkthrough markdown snapshots keep the same contract marker as JSON outputs.
- Re-run CLI/core tests plus artifact regeneration to keep docs-facing snapshots aligned.

### Changes
- Updated `.github/workflows/ci.yml` committed walkthrough snapshot smoke step to assert both PASS/FAIL markdown artifacts contain `Summary schema version: 1`.
- Updated `README.md` CI artifact walkthrough guidance to state that committed markdown snapshots retain the same schema marker as JSON outputs.

### Verification
- `python3 -m unittest tests.test_core tests.test_cli`
- `./scripts/regenerate_walkthrough_artifacts.sh`
- Result: **PASS** (115 tests + walkthrough artifact regeneration pass)

### Blockers
- `pytest` is still unavailable in host PATH, so validation continues via `unittest` + CLI smoke commands.

### Next
- Add one fixture-level smoke assertion in CI docs/examples that the PASS markdown snapshot keeps the expected improvement id alongside the schema marker.

## 실행 @ 10:40 UTC (cron)

### 계획
- summary JSON을 소비하는 다운스트림 CI가 schema drift를 바로 감지할 수 있는 gate를 추가한다.
- 기존 walkthrough snapshot도 함께 맞춰 artifact drift를 없앤다.

### 변경 사항
- `src/prompt_regression_min/cli.py`에 `--require-summary-schema-version` gate 추가.
- `tests/test_cli.py`에 mismatch/pass-through JSON coverage 추가.
- `.github/workflows/ci.yml`에 schema-version compatibility smoke step 추가.
- `examples/artifacts/` walkthrough snapshot을 새 gate 필드에 맞게 재생성.
- `README.md`에 downstream parser compatibility gate 사용 예시 반영.

### 검증
- `./scripts/regenerate_walkthrough_artifacts.sh`
- `PYTHONPATH=src python3 -m unittest discover -s tests -v`
- 결과: **PASS**

### 막힘/리스크
- 초기 테스트에서 committed walkthrough snapshot이 새 gate 필드 누락으로 drift FAIL이 났고, 재생성으로 해결.

### 다음 실행 우선순위
- markdown summary에도 schema-version/compatibility gate 표시를 넣을지 검토.
