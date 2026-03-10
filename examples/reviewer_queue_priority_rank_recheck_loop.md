# Reviewer queue priority-rank recheck loop

Use this short loop after you post a reviewer queue summary and want to confirm the top priority bucket still deserves first attention.

## Recheck loop
1. Re-run the same summary command against the refreshed input set.
2. Compare the top `priority_rank` bucket with the last posted result.
3. If the top bucket changed, update the handoff note before assigning work.
4. If the top bucket is unchanged, keep the previous assignment and only refresh the evidence timestamp.

## Good handoff line
`Recheck complete: priority rank 1 is still instruction-following with 42.9% of open failures, so the current reviewer focus remains valid.`
