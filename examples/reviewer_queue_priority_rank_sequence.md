# Reviewer queue priority-rank sequence

Use this note when the summary already exposes reviewer queue priority ranks and you want the shortest route from JSON to a human handoff.

1. Check the best exposed priority rank first (`P1` before `P2`, and so on).
2. Confirm the next-focus queue still wins on the configured tie-break.
3. Keep the runner-up visible when the lead is narrow.
4. Post one sentence that names the queue, rank, and reason.

## Copy-ready handoff shape

`Next reviewer focus: <queue> (priority rank <n>) because it still outranks <runner-up> after the tie-break.`

## When to avoid this shortcut

Do not use the one-line handoff if:

- the next-focus queue is tied,
- the runner-up is missing,
- or the queue share changed after a fresh filter run.

In those cases, switch to `examples/reviewer_queue_priority_rank_tie_card.md` or `examples/reviewer_queue_next_focus_tie_break_card.md` first.
