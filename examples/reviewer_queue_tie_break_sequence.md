# Reviewer queue tie-break sequence

Use this when two reviewer queues look close enough that a one-line handoff still feels risky.

## 4-step tie-break
1. Prefer the queue with the higher queue-share percentage.
2. If queue share ties, prefer the queue with the lower source-case pass rate.
3. If both still tie, prefer the queue with the larger absolute failing-case count.
4. If the tie still remains, keep the current winner narrow and mention the runner-up explicitly.

## Copy-ready handoff
- `Next reviewer focus: <winner> leads on queue share / risk; keep <runner-up> visible as the immediate follow-up.`

## Quick exit rule
If you cannot explain the winner in one sentence after these four checks, do not force a winner; use a rank note instead.
