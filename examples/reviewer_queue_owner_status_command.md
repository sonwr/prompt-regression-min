# reviewer_queue_owner_status_command

Use this tiny pattern after the next reviewer queue is already decided and you want one command-shaped handoff line.

## Template

```text
Review <queue_label> next; confirm <top_reason> and post the owner update once <proof_signal> is visible.
```

## Fill in

- `<queue_label>`: selected next-focus reviewer queue
- `<top_reason>`: the dominant reason it won (share, rank, or tie-break)
- `<proof_signal>`: the concrete thing that makes the owner update credible

## Example

```text
Review policy next; confirm the highest regression share and post the owner update once the PR comment summary is regenerated.
```
