# Reviewer queue priority-rank status line

Use this tiny template when the summary already exposes `next_focus_group`, `next_focus_priority_rank`, and the queue-share context.

## One-line template

`Next reviewer focus: <queue> (rank #<rank>, <share>% of queued regressions).`

## When to use it

- the summary already picked a unique next-focus queue,
- you want a human-ready sentence without reopening the JSON payload,
- and the PR comment only needs the single most important reviewer routing cue.

## Fallback

If the rank is tied or the lead is narrow, pair this note with `examples/reviewer_queue_priority_margin_card.md` before posting.
