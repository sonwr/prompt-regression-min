# line_count_range walkthrough

This walkthrough shows a small, deterministic way to validate line-budget contracts for UI copy, release notes, or support macros.

## Why use `line_count_range`

`line_count_range` is useful when word count is too loose but exact string matching is too brittle.
Use it when the output should stay within a visible number of rendered lines.

Common examples:

- short release notes that must fit a changelog card,
- customer-support macros that should stay within a 3-6 line reply budget,
- onboarding hints that must remain scannable in a narrow panel.

## Example dataset row

```json
{"id":"release-note-lines","expected":{"type":"line_count_range","min":3,"max":5}}
```

A candidate output with four non-empty lines passes.
A candidate output with two lines or six lines fails.

## Copyable smoke fixture

Create three files in a temp directory.

### `dataset.jsonl`

```json
{"id":"release-note-lines","expected":{"type":"line_count_range","min":3,"max":5}}
```

### `baseline.jsonl`

```json
{"id":"release-note-lines","output":"Release shipped\nCheckout fixes landed\nCopy updated\nMonitoring enabled"}
```

### `candidate.jsonl`

```json
{"id":"release-note-lines","output":"Release shipped\nCheckout fixes landed\nCopy updated\nMonitoring enabled\nQA replay docs linked"}
```

## Run the check

```bash
prm run \
  --dataset dataset.jsonl \
  --baseline baseline.jsonl \
  --candidate candidate.jsonl \
  --summary-markdown - \
  --summary-pr-comment - \
  --quiet
```

Expected result:

- exit code `0`
- status `PASS`
- stable ids include `release-note-lines`

## Turn the same run into a blocker example

Change `candidate.jsonl` to six lines:

```json
{"id":"release-note-lines","output":"Release shipped\nCheckout fixes landed\nCopy updated\nMonitoring enabled\nQA replay docs linked\nKnown issue note added"}
```

Run the same command again.

Expected result:

- exit code `1`
- status `FAIL`
- regression ids include `release-note-lines`
- the PR-comment output is ready to paste into a reviewer note

## Reviewer-note habit

For line-budget checks, use the markdown summary when you need a durable artifact and the PR-comment summary when you need a compact handoff.
That keeps the same deterministic fixture useful for both CI and human review.
