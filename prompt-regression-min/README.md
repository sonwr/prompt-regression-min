# prompt-regression-min

A minimal regression checker for prompt or workflow changes in LLM-powered apps.

## Why

When prompts, routing logic, or model settings change, quality can silently regress.
`prompt-regression-min` gives you a tiny, reproducible baseline check with JSONL datasets and simple scoring.

## Features

- Compare **baseline** vs **candidate** outputs on the same dataset
- Lightweight scorers:
  - exact match
  - contains-all
  - substring
- Human-readable CLI summary
- JSON report export for CI

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

prm run \
  --dataset examples/dataset/customer_support.jsonl \
  --baseline examples/outputs/customer_support.baseline.jsonl \
  --candidate examples/outputs/customer_support.candidate.jsonl \
  --report report.json
```

## Dataset format (JSONL)

Each line:

```json
{
  "id": "case-1",
  "input": "How do I reset my password?",
  "expected": {
    "type": "contains_all",
    "values": ["reset", "email", "security"]
  }
}
```

Supported expectation types:

- `exact`: `{"type":"exact","value":"..."}`
- `contains_all`: `{"type":"contains_all","values":["a","b"]}`
- `substring`: `{"type":"substring","value":"..."}`

## Output format (JSONL)

Each line:

```json
{
  "id": "case-1",
  "output": "Use the password reset page and check your email."
}
```

## CLI

```bash
prm run --dataset <path> --baseline <path> --candidate <path> [--report report.json]
```

Example summary:

- baseline pass rate
- candidate pass rate
- regression count
- improved count
- unchanged count

## CI usage

Use `--report report.json` and parse `summary.regressions`.
Fail pipeline if regressions exceed your threshold.

## Roadmap

- weighted scoring
- semantic similarity scorer
- HTML report
- GitHub Action wrapper

## License

MIT
