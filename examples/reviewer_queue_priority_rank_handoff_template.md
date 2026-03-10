# Reviewer queue priority-rank handoff template

Use this template when the summary output already includes `priority_rank` and you want a compact maintainer-facing note.

## Template

```text
Primary focus: <group_label> (priority rank <rank>, <share>% of queue)
Why now: <one-sentence reason tied to failures, blockers, or review load>
Runner-up: <group_label or none>
Next move: <single concrete action>
Proof line: <command, artifact, or summary field to re-check>
```

## Example

```text
Primary focus: formatting regressions (priority rank 1, 42.9% of queue)
Why now: This group leads the queue and has the highest failing-case concentration.
Runner-up: policy mismatches
Next move: Review the top formatting cases first and regenerate the PR comment after fixes land.
Proof line: python3 -m prompt_regression_min summary --format pr-comment
```
