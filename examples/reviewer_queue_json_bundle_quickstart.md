# Reviewer queue JSON bundle quickstart

Use this when a reviewer needs the queue summary plus a reusable JSON artifact path in the same handoff.

## Suggested command

```bash
prompt-regression-min compare \
  --baseline baseline.jsonl \
  --candidate candidate.jsonl \
  --summary-json artifacts/summary.json \
  --summary-markdown artifacts/summary.md
```

## One-line handoff pattern

`Priority review queue is <label>; reopen artifacts/summary.json and artifacts/summary.md together before posting the follow-up.`
