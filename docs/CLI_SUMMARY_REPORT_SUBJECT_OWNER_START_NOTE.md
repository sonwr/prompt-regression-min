# CLI summary report subject+owner start note

Use one saved summary bundle when reviewers need the report subject and owner visible without reopening raw stdout first.

Suggested pattern:

```bash
PYTHONPATH=src python3 -m prompt_regression_min.cli compare \
  --baseline examples/baseline.jsonl \
  --candidate examples/candidate.jsonl \
  --summary-report artifacts/review/summary \
  --report-subject "release-review" \
  --report-owner "maintainer"
```

Keep the first handoff small:
- one subject
- one owner
- one shared JSON/Markdown/HTML bundle
