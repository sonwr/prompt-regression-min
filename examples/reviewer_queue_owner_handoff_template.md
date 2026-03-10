# Reviewer queue owner handoff template

Use this quick template when the summary payload already identifies the dominant queue and you only need a compact reviewer-facing note.

## Template

```text
Owner handoff: <queue> reviews <focus area> because it leads on <metric>; follow up with <next check> before merge.
```

## Fill-in order

1. Queue name
2. Focus area or changed scope
3. Metric that justified the queue selection
4. Follow-up check that closes the loop

## Example

```text
Owner handoff: retrieval reviews answer citation changes because it leads on candidate-only failures; follow up with the source-grounding smoke case before merge.
```

## Anti-pattern

```text
Owner handoff: someone should take a look.
```

If the note cannot name the queue and the reason it won, it is too vague to help a reviewer.
