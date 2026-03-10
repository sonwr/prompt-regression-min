# Regex flag aliases

`prompt-regression-min` accepts both long-form regex flags and short aliases in `expected.flags`.

Supported aliases:

- `i` -> `IGNORECASE`
- `m` -> `MULTILINE`
- `s` -> `DOTALL`
- `x` -> `VERBOSE`

Example dataset row:

```json
{"id":"case-1","expected":{"type":"regex","pattern":"^alpha.+omega$","flags":["i","s"]}}
```

Use aliases when you want compact JSONL expectations without losing readability in review diffs.
