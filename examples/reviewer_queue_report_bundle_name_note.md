# Reviewer queue report bundle name note

Keep reviewer-facing report bundles on one stable basename whenever JSON, markdown, and HTML artifacts are meant to travel together.

Recommended rule:

- set `--report-file-stem` once per handoff
- reuse the same stem for JSON, markdown, and HTML outputs
- mention that shared basename in the human reviewer note

This keeps reopen commands, CI artifacts, and review comments pointing at the same bundle without filename drift.
