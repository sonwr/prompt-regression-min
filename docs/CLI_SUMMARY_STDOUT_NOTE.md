# cli summary stdout note

Use this note when the quickest reviewer handoff should stay on stdout instead of creating extra files.

Preferred loop:

1. run one deterministic dataset/baseline/candidate check,
2. emit `--summary-json -` or `--summary-markdown -`,
3. reuse the same payload in CI, PR comments, or local review.

This keeps the machine-readable summary and the human-readable handoff tied to the same single-run evidence path.
