# Reviewer queue handoff sequence

Use this sequence when the summary already includes reviewer-queue metadata and you need to turn it into a short human handoff.

## 1. Read the queue in this order

1. `next_focus_group`
2. `runner_up_group`
3. `follow_up_priority`
4. `queue_mix_summary`

## 2. Write the handoff in this order

- lead queue label and priority
- affected IDs
- active-case rate
- source-case rate
- whether the lead is unique, tied, or only queue

## 3. Short templates

### Unique lead

`Focus first on <label> (<ids>) because it leads the queued follow-up at <queue share> and covers <active rate> of active cases.`

### Tied lead

`<label> is tied for first with <peer label>; keep both queues visible before narrowing the reviewer handoff.`

### Single queue

`Only <label> remains in the reviewer queue, so the handoff can stay compact and approval-focused.`

## 4. Don’t do this

- don’t list raw IDs before explaining the queue label
- don’t hide source-case rate when a filter removed many cases
- don’t call a queue dominant if the tie mode is `tied`
- don’t skip the runner-up when the advantage summary is small
