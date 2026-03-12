# Summary stdout owner handoff

Use one run when you want a compact terminal summary for a reviewer plus a clear owner note for follow-up.

```bash
PYTHONPATH=src python3 -m prompt_regression_min.cli run \
  --cases examples/cases/basic.jsonl \
  --summary-stdout \
  --summary-title "Nightly regression snapshot"
```

Recommended follow-up: paste the stdout summary into the issue or PR comment, then attach the richer report bundle only if the gate fails.
