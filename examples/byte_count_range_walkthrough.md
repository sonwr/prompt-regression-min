# byte_count_range walkthrough

Use `byte_count_range` when the output must fit a strict UTF-8 byte budget, especially for multilingual UI labels, commit titles, or short notification text.

## Why bytes instead of characters?

Character counts can look safe while still exceeding platform limits because many non-ASCII characters take multiple UTF-8 bytes.

Examples:

- `OpenClaw update` -> mostly 1 byte per character
- `오픈클로 업데이트` -> several characters consume 3 bytes each

If the downstream system enforces bytes, test bytes.

## Minimal dataset pattern

```jsonl
{"id":"ui-label-ko","input":"Generate a short Korean CTA label.","expected":{"type":"byte_count_range","min_bytes":1,"max_bytes":24}}
{"id":"commit-title","input":"Write a concise commit title.","expected":{"type":"byte_count_range","min_bytes":1,"max_bytes":72}}
```

Use `min_bytes` / `max_bytes` explicitly so the dataset matches the validator contract used by `prompt-regression-min`.

## Typical workflow

1. Add a `byte_count_range` expectation to the dataset.
2. Run baseline and candidate outputs through `prm run`.
3. Paste the markdown or PR-comment summary into the review thread if the candidate exceeds the byte budget.

## Good fit

Use this scorer for:

- UI copy with hard storage or transport limits
- commit / release titles with multilingual text
- notification text that must stay under byte-based provider limits

## Not a good fit

Do not use it when the real requirement is semantic quality, tone, or sentence structure. In those cases, pair a byte budget with a separate content expectation.
