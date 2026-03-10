# Reviewer queue exit check

Use this note when the summary already exposes reviewer-queue metadata and you need one short rule for deciding whether the handoff is ready to paste into a PR comment.

## Exit check

1. Read `Reviewer queue total` first.
2. If the queue is non-zero, keep `Reviewer queue next-focus priority label` and ids in the first sentence.
3. If a runner-up exists, keep it as context instead of splitting the primary action.
4. If the queue is zero, say so directly and skip queue-specific filler.
5. Do not post a handoff until the first sentence tells the reviewer what to do next.

## Pair with

- `examples/reviewer_queue_first_pass_checklist.md`
- `examples/reviewer_queue_priority_handoff_card.md`
- `examples/reviewer_queue_zero_queue_playbook.md`
