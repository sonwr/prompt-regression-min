# CLI reviewer queue share + priority note

When `prompt-regression-min` picks a next-focus reviewer queue, keep two fields together in the human handoff:

- the priority label (for deterministic ordering)
- the queue share (for relative workload size)

That pairing helps reviewers distinguish "first by policy" from "largest by queue pressure" without reopening the full JSON artifact.
