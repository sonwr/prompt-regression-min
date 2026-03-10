# reviewer queue priority-rank margin note

Use this one-line note when the next reviewer queue already has a priority rank, but you want to explain that the lead is still narrow.

## Template

`Priority rank: P1 {queue_label}; lead remains narrow at {margin_cases} case(s) / {margin_queue_share}% queue share, so keep the runner-up visible in the handoff.`

## Example

`Priority rank: P1 fix regressions; lead remains narrow at 1 case(s) / 8.33% queue share, so keep the runner-up visible in the handoff.`

## When to use it

- The dominant queue is unique, but only barely ahead.
- Reviewers may need the runner-up called out in the same PR comment.
- You want a short explanation without reopening the full summary JSON.
