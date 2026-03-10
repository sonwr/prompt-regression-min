# Reviewer queue priority-rank tie checklist

Use this when two reviewer queues expose the same priority rank and you need a deterministic human handoff.

## Quick checklist

1. Confirm the tied queues really share the same `priority_rank`.
2. Compare `queue_share` and prefer the larger queue when the lead is visible.
3. If `queue_share` also ties, compare `source_case_rate` and prefer the queue touching more source cases.
4. If both still tie, post a tie-aware handoff instead of inventing a winner.

## Tie-aware handoff sentence

`Next reviewer focus is tied between <queue A> and <queue B>; both share priority rank <n>, so keep both queues visible in the handoff.`

## Avoid

- Naming a unique winner when the metadata still shows a true tie.
- Hiding the runner-up when the advantage is effectively zero.
