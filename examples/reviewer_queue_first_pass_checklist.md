# Reviewer queue first-pass checklist

Use this checklist when the summary already exposes reviewer-queue metadata and you need a fast first pass before posting a PR comment.

## First-pass order

1. Check `Reviewer queue total` to see whether any follow-up exists.
2. Read `Reviewer queue next-focus key` and `Reviewer queue next-focus label` first.
3. Confirm the pasted note includes the `next-focus` ids before mentioning runner-up lanes.
4. If tie mode is `tied`, preserve `Reviewer queue next-focus tie summary` in the handoff.
5. If the queue is empty, prefer the zero-queue playbook instead of inventing filler text.

## Use with

- `examples/reviewer_queue_handoff_sequence.md`
- `examples/reviewer_queue_priority_decision_card.md`
- `examples/reviewer_queue_zero_queue_playbook.md`
