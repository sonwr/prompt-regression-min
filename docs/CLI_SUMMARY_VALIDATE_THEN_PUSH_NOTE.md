# CLI_SUMMARY_VALIDATE_THEN_PUSH_NOTE

Keep the smallest deterministic summary validation green before push whenever README, CLI output, or saved summary artifact wording changes.

Suggested loop:

```bash
python3 -m unittest tests/test_core.py tests/test_cli.py
```

If the change widens the summary contract, rerun the full discovery pass before pushing.
