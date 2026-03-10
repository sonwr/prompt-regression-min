# Reviewer queue zero-queue playbook

Use this note when the report passes but `reviewer_queue.total` is `0` and you still need a short human handoff.

## When to use it

Use this playbook when all of the following are true:

- `status` is `PASS`
- `reviewer_queue.total` is `0`
- `regressions` is `0`
- `improved` may be `0` or greater

## Copy-ready handoff line

```text
No reviewer queue generated: 0 follow-up lanes, 0 queued cases, stable handoff safe.
```

## Why it helps

A zero-queue result is easy to misread as missing output. This playbook makes it explicit that the queue is empty because no reviewer follow-up lane was required, not because the artifact is incomplete.

## Suggested checks

- Confirm `follow_up_priority_summary` is `none`.
- Confirm `next_focus_handoff_summary` is `none`.
- Confirm the active-case rate and pass-rate trend already tell the story you need.
