# Reviewer queue next-focus status line

Use this when you need a one-line human handoff after the summary payload already selected the next reviewer queue.

## Status line template

`Next focus: <queue> leads with <share/rate evidence>; reviewer should inspect <priority reason> before moving to <runner-up or follow-up queue>.`

## Minimum ingredients

- selected queue name
- one compact evidence phrase (`share`, `count`, `source-case rate`, or tie-break reason)
- the concrete priority reason
- the next queue to watch, when it matters

## Example

`Next focus: policy queue leads with 42% of open cases and the top source-case rate; reviewer should inspect skipped safety language before moving to billing as runner-up.`

## Rule of thumb

If the sentence cannot be pasted into a PR comment without opening JSON again, it is still too vague.
