# Reviewer queue priority-rank playbook

Use this when a summary artifact already exposes the reviewer queue, and you need one short explanation of why the next-focus lane is ordered ahead of the rest.

## What to read

1. `Reviewer queue follow-up priority`
2. `Reviewer queue next-focus priority label`
3. `Reviewer queue next-focus tie mode`
4. `Reviewer queue runner-up priority label`

## Quick interpretation rule

- If tie mode is `unique`, act on the `next-focus` lane first.
- If tie mode is `tied`, keep the documented `P1`, `P2`, ... ranking in the handoff even when the top buckets have the same case count.
- If there is a runner-up, paste it beside the next-focus lane so reviewers can see the second branch without opening JSON.

## Copy-ready handoff pattern

```text
Follow-up order: <P1 label> -> <P2 label> -> ...
Start now: <next-focus priority label>
Tie mode: <unique|tied>
Runner-up: <runner-up priority label|none>
```

## Example

```text
Follow-up order: P1 · fix regressions -> P2 · watch unchanged fails
Start now: P1 · fix regressions
Tie mode: unique
Runner-up: P2 · watch unchanged fails
```
