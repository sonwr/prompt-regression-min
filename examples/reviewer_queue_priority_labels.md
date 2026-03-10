# Reviewer queue priority labels

Use reviewer queue priority labels to explain *why* a follow-up group is first in line, not just *which* group is largest.

## Why this file exists

When the queue summary is copied into PR comments or incident notes, maintainers need a stable phrase that survives without the full JSON payload.
Priority labels give the queue handoff a compact human-readable explanation.

## Suggested interpretation

- `priority: highest` — act now; this group should lead the next review pass
- `priority: elevated` — likely next after the highest bucket clears
- `priority: normal` — worth reviewing, but not the main bottleneck
- `priority: none` — no active reviewer queue to triage

## Recommended handoff format

```text
Next focus: policy drift (priority: highest, cases: 4, queue share: 50.00%)
Runner-up: formatting drift (priority: elevated, cases: 3, queue share: 37.50%)
```

## Authoring note

If two groups are tied on count, keep the priority label visible even when the tie summary already names both groups.
That prevents tie-break logic from disappearing in markdown summaries and PR comments.
