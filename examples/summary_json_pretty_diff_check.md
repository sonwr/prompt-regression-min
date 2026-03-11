# Summary JSON pretty diff check

Use this when CI needs both machine-stable summary JSON and a human-readable artifact for review.

## Goal

Confirm that compact and pretty summary outputs describe the same regression result.

## Example

```bash
PYTHONPATH=src python3 -m prompt_regression_min.cli run \
  --cases examples/basic/smoke_cases.jsonl \
  --summary-json .tmp/summary.json \
  --summary-json-stdout \
  --quiet

PYTHONPATH=src python3 -m prompt_regression_min.cli run \
  --cases examples/basic/smoke_cases.jsonl \
  --summary-json .tmp/summary.pretty.json \
  --summary-json-pretty \
  --quiet
```

## Review check

```bash
python3 - <<'PY2'
from pathlib import Path
import json
compact = json.loads(Path('.tmp/summary.json').read_text(encoding='utf-8'))
pretty = json.loads(Path('.tmp/summary.pretty.json').read_text(encoding='utf-8'))
assert compact == pretty
print('summary payloads match')
PY2
```
