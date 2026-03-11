# Reviewer queue queue-share decision card

Use this card when multiple reviewer queues exist and you need the shortest deterministic rule for picking the next queue to surface.

## Decision rule

1. Prefer the queue with the largest case count.
2. If counts tie, prefer the queue with the higher priority rank.
3. If priority rank also ties, compare queue share.
4. If queue share still ties, keep the handoff explicitly shared instead of forcing a fake winner.

## One-line handoff shape

`Next focus: <queue label> leads by queue share and keeps the highest-priority unresolved work visible.`
