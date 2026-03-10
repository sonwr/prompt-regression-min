# Reviewer queue small-batch handoff

Use this pattern when the queue is small enough that the reviewer only needs one compact status note.

## When to use it

- Fewer than 10 candidate cases need review.
- One focus group clearly dominates the queue.
- The next reviewer does not need a full incident-style escalation note.

## Recommended handoff fields

- `next_focus_group`
- `next_focus_label`
- `next_focus_case_count`
- `next_focus_share`
- `followup_priority`
- `top_two_summary`

## Example handoff line

```text
Next focus: policy-refusal (4 cases, 44.4% of queue); follow-up priority is high because it leads the next group by 2 cases.
```

## Why it helps

A short handoff keeps CI comments readable while still giving a reviewer enough context to pick the next batch without opening the JSON artifact first.
