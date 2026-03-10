# Sentence Count Range Authoring

Use `sentence_count_range` when the output should stay within a narrow sentence budget but exact wording can vary.

## Minimal dataset shape

```json
{
  "id": "release-note-summary",
  "expected": {
    "type": "sentence_count_range",
    "min_sentences": 2,
    "max_sentences": 3
  }
}
```

## Good fits

- short release-note summaries
- support replies with a strict brevity window
- evaluator outputs where structure matters more than exact phrasing

## Avoid when

- exact wording is required (`exact`, `exact_ci`)
- specific keywords must appear (`contains_all`, `contains_any`)
- line or paragraph layout matters more than sentence count

## Authoring tips

- Prefer both `min_sentences` and `max_sentences` when you want a narrow style guardrail.
- Use a single bound when you only care about a floor or ceiling.
- Keep multilingual punctuation in mind; the matcher already counts `.`, `!`, `?`, `。`, and `！`/`？` style endings.
- Pair this with walkthrough artifacts when adding a new gate so reviewers can see the intended pass/fail shape quickly.
