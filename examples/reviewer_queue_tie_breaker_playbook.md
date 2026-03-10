# Reviewer Queue Tie-Breaker Playbook

Use this note when two queue groups look equally urgent.

## Tie-break order

1. Higher failing-case count
2. Higher queue share
3. Higher source-case rate
4. Lower reviewer context-switch cost

## Posting rule

When the top two groups are still tied after metrics, post both values in the handoff and state which group should move first.

Example:

```text
Next focus: policy-tone (tied with format-precision on count/share; move policy-tone first because it keeps the reviewer in the same case family).
```

## Why this helps

- keeps PR comments deterministic
- reduces reviewer hesitation
- makes repeated runs easier to compare
