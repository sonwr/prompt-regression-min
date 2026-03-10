# Pass-rate trend gate walkthrough

This walkthrough focuses on the `--require-pass-rate-trend` contract when reviewer handoff needs the trend label itself to be stable and explicit.

## Why use it

Use this when the numeric pass-rate gates are not enough on their own and reviewers need CI to spell out whether the run is `improving`, `flat`, or `regressing`.

## Copyable improving gate

```bash
PYTHONPATH=src python3 -m prompt_regression_min run \
  --dataset examples/dataset/customer_support.jsonl \
  --baseline examples/outputs/customer_support.baseline.jsonl \
  --candidate examples/outputs/customer_support.candidate.jsonl \
  --require-pass-rate-trend improving \
  --summary-pr-comment -
```

## What this adds beyond pass-rate floors

- `--min-candidate-pass-rate` answers "is the candidate good enough?"
- `--min-delta-pass-rate-pp` answers "did pass rate fall?"
- `--require-pass-rate-trend` answers "does the reviewer-facing trend label match the release expectation?"

That last contract matters when a release branch expects visible improvement rather than a merely non-regressing result.

## Flat-trend acceptance variant

If a maintenance branch is allowed to stay flat while preserving stable cases, switch the trend contract instead of weakening the whole gate:

```bash
PYTHONPATH=src python3 -m prompt_regression_min run \
  --dataset examples/dataset/customer_support.jsonl \
  --baseline examples/outputs/customer_support.baseline.jsonl \
  --candidate examples/outputs/customer_support.candidate.jsonl \
  --min-unchanged-pass 3 \
  --require-pass-rate-trend flat
```

## Reviewer handoff tip

Pair the trend gate with `--summary-pr-comment -` so CI emits a paste-ready note that names the exact trend mismatch instead of forcing reviewers to infer it from raw rates.
