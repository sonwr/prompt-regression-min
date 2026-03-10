# Reviewer queue priority labels quick reference

Use this page when a regression summary includes reviewer-queue priority labels and you want a compact reminder of how to describe them in handoff notes.

## Priority label meanings

- `P1 now` — review this queue first because it represents the most urgent regression follow-up.
- `P2 next` — review this queue after the lead bucket; it is still actionable but not the tightest bottleneck.
- `P3 later` — keep this queue visible for batching, not for immediate interruption.

## Suggested handoff sentence pattern

```text
Next focus: <label> (<count> cases, <queue share>% of reviewer queue); runner-up: <label>.
```

## Example handoff lines

- `Next focus: formatting regressions (4 cases, 50.0% of reviewer queue); runner-up: billing regressions.`
- `Next focus: tool-call mismatches (2 cases, 33.3% of reviewer queue); runner-up: empty-output regressions.`
- `Next focus: none; reviewer queue is empty.`

## When to mention runner-up context

Mention the runner-up when:

1. the next-focus queue has ties,
2. the advantage is small, or
3. a reviewer needs batching context for the next pass.

Skip it when the queue is empty or one bucket clearly dominates.
