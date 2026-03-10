# Reviewer queue priority-rank ready signal

Use this quick check after the CLI exposes a priority-rank winner and you need to decide whether that result is ready for a human handoff.

Call the exposed queue **ready to post** only when all of the following are true:

1. the winning queue is named clearly,
2. the displayed priority rank is unique or the tie mode is explained,
3. the margin or runner-up context is visible when the lead is narrow,
4. the suggested next action still matches the queue that won.

If one of those checks fails, keep the result in review and inspect the JSON or markdown summary before posting a human-facing handoff.

## One-line handoff cue

`Ready to post:` the priority-rank winner is explicit, the lead is credible, and the runner-up context is not hidden.
