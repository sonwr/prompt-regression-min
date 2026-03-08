# CI artifact walkthrough

This walkthrough shows how to interpret the machine-readable summary artifacts that `prompt-regression-min` can upload from CI.

## Why this exists

When a pull request fails a prompt regression gate, reviewers should not have to reconstruct what happened from terminal logs alone.

Use uploaded summary artifacts to answer three questions quickly:

1. Did the run pass or fail?
2. Which gate failed?
3. Which case IDs changed, regressed, or stayed broken?

## PASS artifact example

Command:

```bash
PYTHONPATH=src python3 -m prompt_regression_min run \
  --dataset examples/dataset/walkthrough_pass_artifact_demo.jsonl \
  --baseline examples/outputs/walkthrough_pass_artifact_demo.baseline.jsonl \
  --candidate examples/outputs/walkthrough_pass_artifact_demo.candidate.jsonl \
  --summary-json .tmp/pass-summary.json \
  --summary-markdown .tmp/pass-summary.md \
  --min-improved 1
```

Fixture files:

- `examples/dataset/walkthrough_pass_artifact_demo.jsonl`
- `examples/outputs/walkthrough_pass_artifact_demo.baseline.jsonl`
- `examples/outputs/walkthrough_pass_artifact_demo.candidate.jsonl`

What to verify:

- `status` is `PASS`
- `fail_reasons` is empty
- `summary.improved_ids` is populated when the policy expects wins
- `gates` records the exact threshold values used in CI

Representative JSON excerpt:

```json
{
  "status": "PASS",
  "fail_reasons": [],
  "summary": {
    "regressions": 0,
    "improved": 1,
    "improved_ids": ["checkout-copy"]
  },
  "gates": {
    "min_improved": 1,
    "max_regressions": 0
  }
}
```

## FAIL artifact example

Command (expected non-zero exit):

```bash
PYTHONPATH=src python3 -m prompt_regression_min run \
  --dataset examples/dataset/walkthrough_fail_artifact_demo.jsonl \
  --baseline examples/outputs/walkthrough_fail_artifact_demo.baseline.jsonl \
  --candidate examples/outputs/walkthrough_fail_artifact_demo.candidate.jsonl \
  --summary-json .tmp/fail-summary.json \
  --summary-markdown .tmp/fail-summary.md
```

Fixture files:

- `examples/dataset/walkthrough_fail_artifact_demo.jsonl`
- `examples/outputs/walkthrough_fail_artifact_demo.baseline.jsonl`
- `examples/outputs/walkthrough_fail_artifact_demo.candidate.jsonl`

Stable snapshot filenames committed in-repo:

- `examples/artifacts/walkthrough-pass.summary.json`
- `examples/artifacts/walkthrough-pass.summary.md`
- `examples/artifacts/walkthrough-fail.summary.json`
- `examples/artifacts/walkthrough-fail.summary.md`

Regenerate the committed snapshots locally with:

```bash
./scripts/regenerate_walkthrough_artifacts.sh
```

What to verify:

- `status` is `FAIL`
- `fail_reasons` explains the blocking gate in plain text
- `summary.regression_ids` or `summary.unchanged_fail_ids` narrows triage scope
- the Markdown artifact is short enough to paste into a PR comment without editing

Representative JSON excerpt:

```json
{
  "status": "FAIL",
  "fail_reasons": [
    "regressions 1 exceeded max 0"
  ],
  "summary": {
    "regressions": 1,
    "regression_ids": ["auth-login"]
  }
}
```

## Reviewer triage flow

1. Open the JSON artifact first for exact counters and IDs.
2. Open the Markdown artifact second for a compact human summary.
3. Check `gates` to confirm whether the failure came from policy configuration or output quality.
4. If the run filtered out cases, inspect `filtered_out_ids` before approving the change.

## Recommended PR note template

```text
Regression check: FAIL
Blocking gate: regressions 1 exceeded max 0
Primary ids: auth-login
Artifacts reviewed: fail-summary.json, fail-summary.md
```
