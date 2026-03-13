# CLI summary validate-small-loop then-push note

Keep summary and README edits behind the smallest deterministic local validation loop before commit or push.

Preferred order:
1. Run `python3 -m unittest tests/test_core.py tests/test_cli.py`
2. Re-open the short status wording
3. Commit and push only if that loop stays green

This keeps the five-repo report honest and short.
