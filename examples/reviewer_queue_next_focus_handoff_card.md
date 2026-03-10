# reviewer queue next-focus handoff card

Use this when the summary already computed `next_focus_group` and you need a short reviewer note without reopening the JSON.

## Copy-ready template

```text
Next focus: <queue key>
Priority: <priority label>
IDs: <comma-separated case ids>
Queue share: <queued follow-up share>
Active-case rate: <active-case rate>
Source-case rate: <source-case rate>
Why now: <advantage summary>
```

## Minimum fields to verify

- `summary.reviewer_queue.next_focus_group.key`
- `summary.reviewer_queue.next_focus_group.priority_label`
- `summary.reviewer_queue.next_focus_group.ids`
- `summary.reviewer_queue.next_focus_group.queue_share`
- `summary.reviewer_queue.next_focus_group.active_case_rate`
- `summary.reviewer_queue.next_focus_group.source_case_rate`
- `summary.reviewer_queue.next_focus_advantage_summary`

## One-line variant

```text
Next focus: <priority label> — <queue key> owns <queue share> of queued follow-up (<active-case rate> active / <source-case rate> source); <advantage summary>.
```
