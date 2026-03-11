# Reviewer queue report outputs bundle note

Use one stable bundle label when summary JSON, Markdown notes, and PR-comment artifacts need to stay aligned across reruns.

Quick rule:
- choose one bundle basename,
- keep JSON/Markdown paths predictable,
- keep the reviewer-facing status line tied to the same artifact bundle name.

Example:

```bash
prompt-regression-min summary \
  --summary-json artifacts/reviewer-queue.json \
  --summary-markdown artifacts/reviewer-queue.md
```

If the queue title changes but the scope stays the same, prefer keeping the bundle basename stable and adjust only the human-facing heading.
