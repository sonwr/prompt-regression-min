# Reviewer queue priority handoff card

Use this when the summary already exposes reviewer-queue metadata and you need a short sentence for a PR comment or release-review handoff.

## One-line handoff template

`Next reviewer focus: <label> (<count> case(s), <queue_share>% of queue, <source_case_rate>% of source cases); runner-up: <label> (<count> case(s)).`

## Fill order

1. `reviewer_queue.next_focus_label`
2. `reviewer_queue.next_focus_case_count`
3. `reviewer_queue.next_focus_queue_share`
4. `reviewer_queue.next_focus_source_case_rate`
5. `reviewer_queue.runner_up_label`
6. `reviewer_queue.runner_up_case_count`

## Short interpretation

- High queue share + high source-case rate → prioritize this lane first.
- Tie summary present → mention ties before naming a single owner lane.
- No next focus label → say `none` and avoid inventing reviewer routing.

## Use with

- `examples/reviewer_queue_priority_labels.md`
- `examples/reviewer_queue_next_focus_playbook.md`
- `examples/reviewer_queue_runner_up_playbook.md`
- `examples/reviewer_queue_share_quick_note.md`
