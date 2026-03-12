# CLI Summary Validate Smallest Loop Note

Before pushing a summary/doc tweak, rerun the smallest deterministic CLI contract first:

```bash
python3 -m unittest tests/test_core.py tests/test_cli.py
```

Use the full discovery pass only when the change widens beyond the smallest reproducible summary loop.
