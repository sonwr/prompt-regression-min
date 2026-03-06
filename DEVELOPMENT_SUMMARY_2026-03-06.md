# prompt-regression-min — Development Summary (through 2026-03-06)

This document summarizes what was built and improved during the initial development sprint.

## 1) Initial MVP Delivered

Initial repository bootstrap included:

- Python package structure (`src/prompt_regression_min`)
- CLI command: `prm run`
- Core comparison engine (`baseline` vs `candidate`)
- JSONL dataset + output examples
- Basic README and quickstart
- CI-friendly behavior (non-zero exit on regressions)

## 2) Core Validation and Correctness Hardening

A large set of defensive checks was added to prevent silent failures and ambiguous results.

### Dataset/input integrity

- Fail on duplicate IDs
- Fail on missing IDs in baseline/candidate
- Reject unknown IDs not present in dataset
- Reject empty dataset
- Enforce JSONL rows are JSON objects
- Allow UTF-8 BOM on first line for better cross-platform compatibility

### Expectation schema/type validation

- Validate `expected.type` and supported values
- Validate `expected.value` type for `exact`/`substring`
- Validate `contains_all.values` is a non-empty string list
- Reject empty `substring` expectation values
- Provide clearer validation error messages

### Output schema validation

- Require `output` field presence
- Require `output` to be a string type

## 3) Reporting and CLI UX Improvements

### Summary/report enhancements

- Added pass-rate deltas:
  - `delta_passes`
  - `delta_pass_rate_pp`
- Added case ID lists:
  - `regression_ids`
  - `improved_ids`
- CLI shows regression/improvement IDs directly

### CLI ergonomics and reliability

- Added short aliases:
  - `-d` dataset
  - `-b` baseline
  - `-c` candidate
  - `-r` report
- Added `--version`
- Enabled module execution:
  - `python -m prompt_regression_min`
- Improved error handling:
  - clean `error: ...` output for invalid input
  - explicit non-zero code for invalid execution state
  - graceful report-write failure handling

## 4) Documentation Expansion

README was significantly expanded to include:

- project motivation
- vision and philosophy
- data format details
- CLI reference and exit code behavior
- CI/CD usage guidance
- roadmap and contribution direction

Additional docs clarifications were added for behavior details (e.g., `exact` whitespace handling).

## 5) Repository Hygiene and Structure Fixes

- Flattened accidental nested directory structure so project files sit at repo root.
- Removed unrelated local workspace files from tracked history and `.gitignore`-protected them.

## 6) Current State

`prompt-regression-min` currently provides a stable minimal baseline for deterministic regression checks with practical CI integration and stronger input safety.

## 7) Development Status Change (Requested)

Per owner request, ongoing automated development jobs for `prompt-regression-min` have been stopped.

Stopped jobs:

- Temporary nonstop sprint for prompt-regression-min
- Daily prompt-regression-min continuous development
- Related next-day sprint check-in reminder

(Trend analysis cron for separate idea scouting remains active.)

---

## Key commits (selected)

- `b7aba42` — bootstrap MVP
- `aa5846d` — flatten repo structure
- `576832a` — major README expansion
- `cc22609` → `f646e63` — correctness/validation + CLI/report hardening series

