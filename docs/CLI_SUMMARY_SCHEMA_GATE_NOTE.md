# CLI summary schema gate note

Use this note when reviewer or CI tooling depends on a stable summary JSON contract.

Recommended loop:

1. render one summary JSON artifact
2. require one explicit summary schema version gate
3. pair the JSON artifact with one markdown or PR-comment handoff
4. rerun the same command before widening automation

This keeps parser-facing automation narrow, reproducible, and easy to review.
