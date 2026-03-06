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
  - `substring`
  - `contains_all`
- Produces:
  - terminal summary
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
- `substring` (`value` must be a non-empty string):
  ```json
  { "type": "substring", "value": "..." }
  ```
- `contains_all` (requires a non-empty `values` list of non-empty strings):
  ```json
  { "type": "contains_all", "values": ["a", "b"] }
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

Dataset files must be non-empty (at least one valid JSONL case).

---

## CLI Reference

```bash
prm run \
  --dataset <dataset.jsonl> \
  --baseline <baseline.jsonl> \
  --candidate <candidate.jsonl> \
  [--report report.json]

# short aliases: -d, -b, -c, -r
```

### Exit codes

- `0`: no regressions
- `1`: regressions detected
- `>1`: invalid input / runtime error

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
