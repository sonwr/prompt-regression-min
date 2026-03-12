# CLI Summary Validate Then Push Note

When a summary or reviewer-queue change touches saved artifacts, validate the smallest deterministic command first and only then push the doc/example update.

Minimum loop:
1. run the smallest matching unittest slice,
2. confirm stdout and saved artifact wording still match,
3. push only after the validation proof is green.
