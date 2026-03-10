# `byte_count_range` authoring guide

Use `byte_count_range` when the exact text can vary but the output still needs to stay within a predictable transport or storage budget.

## When to use it

Choose this expectation when you care about serialized size more than token count or character count.

Good fits:

- webhook payload summaries,
- compact PR comments,
- machine-readable status lines,
- outputs that must stay under a provider byte ceiling.

## Minimal case

```json
{"id":"status-line","expected":{"type":"byte_count_range","min_bytes":40,"max_bytes":120}}
```

## Practical tip

Prefer a small safety margin instead of setting the upper bound exactly at the provider limit. A little headroom makes formatting changes less noisy while still catching true bloat regressions.

## Review checklist

- Are `min_bytes` or `max_bytes` set explicitly?
- Does the range reflect the real transport budget?
- Would `word_count_range` or `char_count_range` communicate the intent more clearly?
