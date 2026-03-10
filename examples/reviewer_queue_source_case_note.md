# Reviewer queue source-case note

Use this note when you want to explain why the next reviewer focus matters relative to the whole source dataset, not just the active queue.

## One-line pattern

`Next focus: <queue> — <n> case(s), <active-rate> of active cases, <source-rate> of source cases.`

## Why this helps

- queue share explains follow-up pressure inside the current queue,
- active-case rate explains pressure inside the selected slice,
- source-case rate explains how visible the issue is in the full dataset.

## Example

`Next focus: fix_regressions — 3 case(s), 60.00% of active cases, 15.00% of source cases.`

## When to prefer this note

- when the selected queue dominates the active slice but not the full dataset,
- when you need a compact PR comment sentence,
- when a reviewer needs quick context without reopening JSON output.

## Related examples

- `examples/reviewer_queue_next_focus_status_line.md`
- `examples/reviewer_queue_share_quick_note.md`
- `examples/reviewer_queue_priority_rank_status_line.md`
