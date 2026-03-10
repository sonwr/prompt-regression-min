# Reviewer Queue Next-Focus One-Liners

Use these short patterns when the summary payload already tells you which reviewer queue should move first, but the PR comment still needs a tight human sentence.

## Formula

```text
Next focus: <queue label> first (<count> case(s), <queue share> of queued follow-up, <source-case rate> of source cases).
```

## Examples

- `Next focus: fix regressions first (2 case(s), 66.67% of queued follow-up, 20.00% of source cases).`
- `Next focus: review improvements first (3 case(s), 50.00% of queued follow-up, 15.00% of source cases).`
- `Next focus: investigate flaky cases first (1 case, 100.00% of queued follow-up, 5.00% of source cases).`

## When to use this instead of a longer handoff

Use the one-liner when:

- the queue winner is unique,
- the PR comment is space-constrained,
- the reviewer already has the full summary JSON or markdown artifact.

Use a longer handoff when:

- priority ties need explanation,
- the runner-up queue changes the actual execution order,
- you need to paste ids or dominant failure themes directly into the comment.

## Pair with

- `examples/reviewer_queue_priority_handoff_card.md`
- `examples/reviewer_queue_handoff_sequence.md`
- `examples/reviewer_queue_next_focus_playbook.md`
