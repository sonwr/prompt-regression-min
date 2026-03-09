# Expectation selection guide

Use this guide when deciding which expectation type to add to a dataset case.

## Pick the smallest rule that proves the behavior

- Use `exact` / `exact_ci` when the whole response must match exactly.
- Use `substring` / `substring_ci` when one required phrase proves success.
- Use `contains_all_ordered` when sequence matters more than full formatting.
- Use `regex` / `regex_fullmatch` when the output shape matters but literal text can vary.
- Use range checks (`word_count_range`, `line_count_range`, `paragraph_count_range`, `sentence_count_range`, `char_count_range`, `byte_count_range`) when structure or budget matters more than exact wording.

## Review heuristics

1. Prefer simpler expectations over regex when a substring or exact match is enough.
2. Prefer case-insensitive variants when capitalization is not product-relevant.
3. Use negative expectations (`not_*`) only when blocking unsafe or forbidden output.
4. When multiple signals matter, split them into separate cases instead of making one giant regex.
5. Keep case ids stable so summary JSON, PR comments, and reviewer queues stay reproducible.

## Example mapping

- Approval label with minor capitalization drift -> `exact_ci`
- Ordered checklist handoff -> `contains_all_ordered`
- Release note length budget -> `word_count_range`
- Ticket summary that must not leak secrets -> `not_substring_ci`
- Response header that must start with `Order #` -> `starts_with`

## Related files

- `README.md`
- `examples/quickstart.md`
- `examples/pass_rate_gate_walkthrough.md`
- `examples/word_count_range_walkthrough.md`
