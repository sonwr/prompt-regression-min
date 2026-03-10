# reviewer_queue_priority_rank_exit_check

Use this short exit check before posting reviewer-queue priority rank notes in a PR comment or release handoff.

## Exit check

1. Does the selected queue still have the best priority rank (`P1` before `P2`, etc.)?
2. Does the note include the queue label humans will recognize immediately?
3. Does the handoff mention queue share or case count so the rank feels justified?
4. If there is a tie, does the note say so instead of pretending the rank is unique?
5. Can a reviewer copy the line into a PR comment without reopening the JSON summary?

## Pass condition

The final handoff should make the next reviewer focus obvious in one sentence: rank, label, and why it is next.
