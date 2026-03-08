# Shard filter walkthrough

Use this walkthrough when you want a small, deterministic subset run instead of evaluating the whole dataset.

`prompt-regression-min` already exposes `--include-id-regex` and `--exclude-id-regex`.
This guide shows how to combine them with the filtered-out gates and reviewer-facing summaries.

## Why shard runs matter

Shard runs are useful when:

- a repo owns only one feature area,
- a PR touches one workflow slice,
- or CI time is too expensive for full-suite runs on every push.

The main risk is hidden scope shrinkage.
If a regex silently filters out too much of the dataset, a PASS result can be misleading.
That is why the summary includes:

- `selected_dataset_ids`
- `active_case_ids`
- `filtered_out_ids`
- `selection_rate`
- `filtered_out_rate`

## Copyable command

```bash
python3 -m prompt_regression_min run \
  -d examples/dataset/filtered_out_band_demo.jsonl \
  -b examples/outputs/filtered_out_band_demo.baseline.jsonl \
  -c examples/outputs/filtered_out_band_demo.candidate.jsonl \
  --include-id-regex '^auth-' \
  --max-filtered-out-cases 2 \
  --max-filtered-out-rate 0.5 \
  --summary-json - \
  --summary-markdown - \
  --summary-markdown-title "auth shard release gate" \
  --quiet
```

## What to verify

### In terminal/JSON

Confirm:

- `status`
- `summary.filtered_out_cases`
- `summary.filtered_out_rate`
- `summary.selection_rate`
- `summary.selected_dataset_ids`
- `summary.filtered_out_ids`

### In markdown summary

Confirm the reviewer can see, without opening JSON:

- custom heading (`auth shard release gate`)
- dataset scope (`source`, `selected`, `active`)
- filtered-out IDs
- filtered-out rate
- changed IDs when present
- gate snapshot showing filtered-out budgets

## Review guidance

A shard PASS is credible only when the summary still makes the skipped scope obvious.
If the filtered-out rate is unexpectedly high, either:

1. widen the regex,
2. add a separate shard for the missing feature area,
3. or block the merge until the shard policy is explicit.

## Related examples

- `examples/gate_policy_recipes.md`
- `examples/ci_artifact_walkthrough.md`
- `examples/artifacts/walkthrough-pass.summary.md`
- `examples/artifacts/walkthrough-fail.summary.md`
