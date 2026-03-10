# Reviewer queue priority-rank triage

Use this quick note when the summary already exposes `priority_rank`, but a human reviewer still needs a fast triage sentence.

## Triage recipe

1. Check the dominant `next_focus_group` first.
2. Confirm whether `priority_rank_gap` is positive, zero, or tied.
3. Read the queue share and follow-up priority lines together.
4. Turn the result into one short handoff sentence.

## Example handoff sentence

```text
Triage: start with safety-review because it keeps rank 1, owns the largest queue share, and still has the strongest follow-up priority.
```

## Compact decision rules

- Positive rank gap → keep the current leader as the first follow-up target.
- Zero gap with a tie → mention the runner-up explicitly so reviewers know the choice is close.
- Small queue share but rank 1 → call out why the rank still wins, instead of assuming volume alone explains the result.
- If the queue is empty, switch to a completion/status update instead of a triage message.
