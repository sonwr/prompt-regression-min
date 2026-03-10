# Reviewer queue dominant-focus checklist

Use this when the summary payload already exposes `next_focus_group` and you need a quick human review before posting a PR handoff.

## Checklist

1. Confirm the dominant queue has the highest pending-case count.
2. Confirm the same queue also has the highest share or a tie explained by priority metadata.
3. Check whether the runner-up queue is close enough to mention in the handoff.
4. Reuse the exact queue label shown in JSON/markdown outputs.
5. Keep the posted sentence short enough for a PR comment.

## Example handoff

```text
Dominant reviewer focus: policy-review (7 cases, 43.8% of queue); mention style-review as the runner-up if a second pass is available.
```
