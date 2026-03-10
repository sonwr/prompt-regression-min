# JSONL case hygiene

Use this checklist when adding or reviewing regression cases so the dataset stays small, deterministic, and easy to debug.

## Keep each case focused

- Prefer one behavior contract per case.
- Split mixed goals into separate cases when a failure would be hard to interpret.
- Keep prompts short unless the long prompt is the thing being tested.

## Make ids stable

- Use ids that describe the contract, not the current wording.
- Avoid ids that depend on ordering like `case-17` when a semantic name would survive edits.
- Keep renamed ids rare so historical diffs stay readable.

## Preserve deterministic expectations

- Use the narrowest expectation that explains the requirement.
- Prefer explicit ranges over vague regex when length or structure matters.
- Avoid expectations that would pass obviously low-quality answers.

## Review the debugging surface

A good case should let a reviewer answer three questions quickly:

1. What behavior was expected?
2. Why did baseline or candidate fail?
3. Which output field or expectation should be changed if the policy evolved?

## Before commit

- Run `python3 -m unittest`.
- Regenerate committed walkthrough artifacts if output or summary text changed.
- Skim the diff to ensure new cases read like durable product contracts, not temporary prompts.
