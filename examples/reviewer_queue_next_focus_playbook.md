# Reviewer queue next-focus playbook

Use this playbook when `prompt-regression-min` produces markdown / PR-comment summaries with reviewer-queue metadata and you need to decide the first rerun lane quickly.

## What to read first

1. `Reviewer queue dominant focus`
2. `Reviewer queue next-focus key`
3. `Reviewer queue next-focus case count`
4. `Reviewer queue next-focus active-case rate`
5. `Reviewer queue next-focus source-case rate`
6. `Reviewer queue next-focus tie mode`

## Recommended interpretation

- `fix_regressions` -> rerun or debug the regression ids first.
- `watch_unchanged_fails` -> verify carryover failures before spending time on new formatting.
- `confirm_filtered_scope` -> confirm whether filters removed the right cases before reading pass/fail deltas.
- `resolve_skipped_cases` -> restore disabled or missing execution coverage before trusting the shard summary.

## Example command

```bash
python -m prompt_regression_min run \
  --dataset examples/dataset/word_count_range_release_notes.jsonl \
  --baseline examples/outputs/word_count_range_release_notes.baseline.jsonl \
  --candidate examples/outputs/word_count_range_release_notes.candidate.jsonl \
  --score word_count_range:min=5,max=12 \
  --summary-markdown - \
  --summary-pr-comment -
```

## Fast triage rule

If `Reviewer queue next-focus tie mode` is `tied`, keep the documented follow-up priority order:

`fix_regressions -> watch_unchanged_fails -> confirm_filtered_scope -> resolve_skipped_cases`

That preserves deterministic reviewer handoffs even when multiple queue buckets are equally large.
