# Pass-rate gate walkthrough

This walkthrough shows how to combine deterministic pass-rate thresholds when you want a stricter quality gate than `--max-regressions 0` alone.

## Why use it

Use these flags when you need to protect release quality with a small, copyable contract:

- `--min-candidate-pass-rate` keeps the candidate above an absolute floor
- `--min-delta-pass-rate-pp` prevents quiet pass-rate regressions
- `--require-pass-rate-trend` makes the summary trend explicit in CI handoff
- `--min-unchanged-pass` protects the stable passing core during shard-scoped reruns

## Copyable gate

```bash
PYTHONPATH=src python3 -m prompt_regression_min run \
  --dataset examples/dataset/customer_support.jsonl \
  --baseline examples/outputs/customer_support.baseline.jsonl \
  --candidate examples/outputs/customer_support.candidate.jsonl \
  --min-candidate-pass-rate 0.75 \
  --min-delta-pass-rate-pp 0 \
  --require-pass-rate-trend improving
```

## Interpretation

- If the candidate stays above `75%` and does not lose pass rate vs baseline, the gate can pass.
- If pass rate drops, the CLI exits non-zero and the fail reason names the pass-rate delta contract.
- If the trend is `flat` or `regressing` while `improving` is required, the summary makes the mismatch explicit for reviewers.

## Stable-core variant

For release branches where you care about preserving already-good cases, add `--min-unchanged-pass`:

```bash
PYTHONPATH=src python3 -m prompt_regression_min run \
  --dataset examples/dataset/customer_support.jsonl \
  --baseline examples/outputs/customer_support.baseline.jsonl \
  --candidate examples/outputs/customer_support.candidate.jsonl \
  --min-candidate-pass-rate 0.75 \
  --min-delta-pass-rate-pp 0 \
  --min-unchanged-pass 3 \
  --require-pass-rate-trend improving
```

## Reviewer handoff tip

Pair this gate with `--summary-pr-comment -` when CI needs a paste-ready note that explains whether the failure came from regressions, pass-rate drift, or stable-core erosion.
