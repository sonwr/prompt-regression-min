# sentence_count_range walkthrough

Use `sentence_count_range` when prompt quality depends on response shape rather than exact wording.

## Example expectation

```json
{"id": "case-1", "expected": {"type": "sentence_count_range", "min_sentences": 2, "max_sentences": 4}}
```

## Why it helps

- catches overly short answers,
- catches rambly answers,
- stays resilient when wording changes but structure should stay compact.

## Quick smoke command

```bash
python3 -m prompt_regression_min.cli   --dataset sample.jsonl   --baseline baseline.jsonl   --candidate candidate.jsonl
```

## Reviewer note

Pair this expectation with summary outputs when you want a PR comment to explain that a reply drifted because it became too terse or too long.
