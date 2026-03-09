# Reviewer queue tie playbook

Use this note when `summary.reviewer_queue.next_focus_tie_mode` is `tied` and the reviewer handoff needs a deterministic first rerun lane without pretending the queue has a unique winner.

## Goal

Keep the review note reproducible when two or more follow-up buckets have the same case count.

## Deterministic tie rule

1. Read `reviewer_queue.follow_up_priority`.
2. Keep the first key in that ordered list as the default rerun lane.
3. Preserve the tie context in the pasted note by quoting:
   - `Reviewer queue next-focus tie mode`
   - `Reviewer queue next-focus key`
   - `Reviewer queue next focus`
   - `Reviewer queue follow-up priority labels`
4. If the team wants to start with another tied bucket, record that override explicitly in the PR thread instead of editing the generated summary.

## Copy-paste workflow

```bash
prm run \
  --dataset examples/dataset/customer_support.jsonl \
  --baseline examples/outputs/customer_support.baseline.jsonl \
  --candidate examples/outputs/customer_support.candidate.jsonl \
  --summary-pr-comment - \
  --quiet
```

Then keep the generated lines below together in the PR comment:

- `Reviewer queue next-focus tie mode: tied`
- `Reviewer queue next-focus key: ...`
- `Reviewer queue next focus: ...`
- `Reviewer queue follow-up priority labels: ...`

## Why this works

`next_focus_key` already respects the deterministic queue order (`fix_regressions` -> `watch_unchanged_fails` -> `confirm_filtered_scope` -> `resolve_skipped_cases`) after sorting by case count first. That means tied queues stay reproducible without hiding the fact that another same-sized bucket exists.
