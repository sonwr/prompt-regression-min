# reviewer_queue_priority_rank_scope_quickstart

Use this when the reviewer queue already exposes a clear priority-rank winner and you need the shortest human handoff without reopening the larger playbooks.

## Fast path

1. Confirm `summary.reviewer_queue.next_focus_key` is present.
2. Confirm `summary.reviewer_queue.next_focus_tie_mode` is `unique`.
3. Copy the existing `next_focus_handoff_summary` or `next_focus_group` details.
4. Keep the note scope-limited to the current queue winner; do not imply broader rerun coverage.

## One-line handoff pattern

```text
Next reviewer focus: <priority label> · <queue label> · ids=<case ids> · active=<active-case rate> · source=<source-case rate>.
```

## Hold instead of post

Stay on hold when any of these is true:

- `next_focus_tie_mode` is `tied`
- the winner still needs a boundary qualifier
- filtered-out or skipped scope is the real review blocker

If that happens, switch to the fuller tie/hold playbooks before posting the handoff.
