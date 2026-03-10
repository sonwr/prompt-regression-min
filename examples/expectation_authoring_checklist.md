# Expectation authoring checklist

Use this quick checklist before adding or reviewing dataset expectations.

## 1. Pick the narrowest expectation

- Prefer `exact` / `exact_ci` when the response should be fixed.
- Prefer `substring`, `starts_with`, or `ends_with` when only one slice matters.
- Prefer range types (`word_count_range`, `line_count_range`, `paragraph_count_range`, `sentence_count_range`, `byte_count_range`) when length matters more than exact wording.
- Prefer regex only when simpler expectation types cannot express the rule.

## 2. Make the failure mode obvious

- Good: `starts_with` for ticket prefixes like `Order #`.
- Good: `contains_none_ci` for forbidden sensitive strings.
- Good: `sentence_count_range` when a summary must stay brief.
- Weak: regex for a plain prefix check.

## 3. Keep ranges intentional

- Use a single bound when only a minimum or maximum matters.
- Use both bounds when the format needs a tight envelope.
- Remember that `byte_count_range` measures UTF-8 bytes, which is useful for emoji and multibyte text budgets.

## 4. Use regex flags carefully

- Prefer explicit flags over embedding complex inline regex behavior.
- Supported flag styles include lists, a single `flag`, and pipe-delimited `flags` strings.
- Keep `verbose` regex patterns readable when the rule is truly complex.

## 5. Add reviewer-friendly evidence

When you add a new expectation family, also add:

- a focused unit test,
- a small walkthrough or example when the behavior is not obvious,
- regenerated committed artifacts if output schema or summaries changed.
