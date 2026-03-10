# reviewer_queue_priority_rank_runner_up_note

Use this note when the priority-ranked next-focus queue is clear enough to lead, but reviewers should still keep the runner-up lane visible.

## Input to check first

- `reviewer_queue.next_focus_key`
- `reviewer_queue.next_focus_priority_label`
- `reviewer_queue.runner_up_key`
- `reviewer_queue.runner_up_priority_label`
- `reviewer_queue.next_focus_advantage_summary`

## Paste-ready note

```text
Next reviewer focus: {next_focus_key} ({next_focus_priority_label}). Keep {runner_up_key} ({runner_up_priority_label}) queued next. Margin: {next_focus_advantage_summary}.
```

## Example

```text
Next reviewer focus: fix_regressions (P1 · fix regressions). Keep watch_unchanged_fails (P2 · watch unchanged fails) queued next. Margin: clear lead: +2 case(s), +33.33% queue share, +20.00% active-case rate, +10.00% source-case rate.
```

## When not to use it

- Do not use this note when `next_focus_tie_mode` is `tied`.
- Do not use it when there is no runner-up queue.
- Do not use it if the lead is still too weak to post without a fuller audit.
