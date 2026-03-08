# Summary JSON handoff walkthrough

Use this walkthrough when you want `prompt-regression-min` to produce both:

- a machine-readable JSON artifact for CI/parsers, and
- a compact markdown note for reviewers.

This keeps regression triage deterministic without forcing reviewers to open raw JSON first.

---

## 1) Generate reviewer-facing markdown + parser-facing JSON together

```bash
python3 -m prompt_regression_min run \
  -d examples/dataset/filtered_out_band_demo.jsonl \
  -b examples/outputs/filtered_out_band_demo.baseline.jsonl \
  -c examples/outputs/filtered_out_band_demo.candidate.jsonl \
  --include-id-regex '^auth-' \
  --max-filtered-out-cases 2 \
  --max-filtered-out-rate 0.5 \
  --summary-json .tmp/filtered-auth.summary.json \
  --summary-markdown .tmp/filtered-auth.summary.md
```

Expected outcomes:

- exit code `0`
- `status=PASS`
- `summary.filtered_out_cases=2`
- `summary.selection_rate=0.5`
- `summary.active_case_ids` shows the shard that actually ran

---

## 2) Pipe markdown directly to stdout for a PR comment draft

```bash
python3 -m prompt_regression_min run \
  -d examples/dataset/word_count_range_release_notes.jsonl \
  -b examples/outputs/word_count_range_release_notes.baseline.jsonl \
  -c examples/outputs/word_count_range_release_notes.candidate.jsonl \
  --summary-markdown - \
  --summary-markdown-title 'release-note reviewer handoff' \
  --quiet
```

Expected outcomes:

- exit code `1`
- markdown heading `## release-note reviewer handoff`
- explicit `Regression IDs`
- gate snapshot lines that explain why CI failed

---

## 3) What downstream automation should read

Prefer explicit JSON fields instead of scraping prose:

- `status`
- `summary_schema_version`
- `tool_version`
- `summary.regression_ids`
- `summary.improved_ids`
- `summary.changed_ids`
- `summary.filtered_out_ids`
- `summary.selected_dataset_ids`
- `summary.active_case_ids`
- `summary.selection_rate`
- `summary.active_case_rate`
- `gates`

This is especially useful for shard-scoped runs where reviewers must see what did **not** run.

---

## 4) Minimal reviewer checklist

Before pasting a markdown summary into a PR or release thread, confirm that it shows:

1. status (`PASS` or `FAIL`)
2. regression/improvement ids when present
3. dataset scope (`source`, `selected`, `active`)
4. filtered-out rate when regex filters were used
5. required gate snapshot values

If one of these is missing, regenerate the artifact instead of editing it manually.
