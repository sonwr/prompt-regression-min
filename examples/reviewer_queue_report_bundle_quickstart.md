# Reviewer queue report bundle quickstart

Use this note when you need the shortest deterministic path from a shard run to a reviewer-ready JSON + markdown + PR-comment handoff bundle.

1. Run one shard command with `--summary-json`, `--summary-markdown`, and `--summary-pr-comment` from the same dataset/baseline/candidate inputs.
2. Keep the emitted reviewer queue lines visible so the next-focus lane and runner-up stay coupled to the same artifact bundle.
3. Reopen the markdown artifact first for human review, then fall back to JSON only when routing or parser details matter.
