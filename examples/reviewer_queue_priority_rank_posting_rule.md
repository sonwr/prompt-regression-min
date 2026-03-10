# Reviewer queue priority-rank posting rule

Use this note when the CLI already exposes `priority_rank` metadata and you need a quick yes/no rule before posting the handoff.

## Posting rule

Post the priority-rank winner only when all three are true:

1. the winning queue has the best exposed `priority_rank`,
2. the handoff sentence still mentions queue share or source-case rate when the lead is narrow,
3. the runner-up is still visible when the rank lead is not decisive.

## Safe one-line pattern

`Post <queue> first (P<rank>) because it still leads on exposed rank and impact; keep <runner-up> visible if the margin stays narrow.`
