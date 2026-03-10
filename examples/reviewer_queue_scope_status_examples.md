# Reviewer queue scope status examples

Use a scope status line when the regression result is valid, but the reviewer-facing update should explicitly say what slice was exercised.

## Template

```text
Reviewer scope status: checked <scope>, queued <top follow-up bucket>, left <filtered or skipped remainder> outside this pass.
```

## Examples

- `Reviewer scope status: checked checkout prompts only, queued fix_regressions, left catalog copy outside this pass.`
- `Reviewer scope status: checked Korean locale cases, queued watch_unchanged_fails, left English-only fixtures outside this pass.`
- `Reviewer scope status: checked newly edited examples, queued confirm_filtered_scope, left unchanged baseline shards outside this pass.`

Pair this with `selected_dataset_ids`, `filtered_out_ids`, and the reviewer queue summary so the public update stays narrow without hiding omitted scope.
