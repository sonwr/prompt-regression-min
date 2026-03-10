# Reviewer queue priority decision card

Use this card when the summary JSON exposes multiple reviewer follow-up queues and you need a fast human handoff.

## Pick the next queue in this order

1. Highest priority rank
2. Largest active-case rate
3. Largest source-case rate
4. Largest queue share
5. Stable key order as final tiebreaker

## One-line handoff template

`Next reviewer focus: <label> — <ids> (<case_count> case(s), <active_rate>% active-case rate, <source_rate>% source-case rate, <queue_share>% of queued follow-up).`

## When to escalate ties

Escalate when two queues still tie after rate and queue-share comparison.
In that case, use the tie summary plus the runner-up summary so reviewers can keep both lanes visible.
