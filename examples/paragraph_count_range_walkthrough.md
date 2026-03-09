# Paragraph-count range walkthrough

Use this walkthrough when outputs should stay scannable as short memo blocks instead of one long wall of text.

## Why use `paragraph_count_range`

`paragraph_count_range` is useful for release summaries, reviewer notes, onboarding blurbs, or support replies where structure matters more than exact wording.

Common examples:

- release notes that should stay within 2-3 short sections,
- PR handoff notes that should separate status from next steps,
- support macros that need one explanation paragraph and one action paragraph.

## Example dataset row

```json
{"id":"release-summary","expected":{"type":"paragraph_count_range","min_paragraphs":2,"max_paragraphs":3}}
```

## Copyable smoke fixture

### `dataset.jsonl`

```json
{"id":"release-summary","expected":{"type":"paragraph_count_range","min_paragraphs":2,"max_paragraphs":3}}
```

### `baseline.jsonl`

```json
{"id":"release-summary","output":"Release shipped with checkout fixes.\n\nMonitoring dashboards were refreshed for launch review."}
```

### `candidate.jsonl`

```json
{"id":"release-summary","output":"Release shipped with checkout fixes and refreshed monitoring dashboards."}
```

## Run the check

```bash
prm run \
  --dataset dataset.jsonl \
  --baseline baseline.jsonl \
  --candidate candidate.jsonl \
  --summary-markdown - \
  --quiet
```

Expected result:

- exit code `1`
- status `FAIL`
- regression ids include `release-summary`

## Recovery tip

If the candidate collapses too much structure, split the output back into explicit paragraphs before reaching for a semantic scorer. That keeps the regression contract deterministic and easy to review.
