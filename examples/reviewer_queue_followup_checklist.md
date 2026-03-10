# Reviewer queue follow-up checklist

Use this short checklist when a reviewer-queue summary already passes tests but still needs a sharper handoff.

## Minimum loop

1. Run the focused validation command:
   ```bash
   python3 -m unittest tests/test_core.py tests/test_cli.py
   ```
2. Regenerate any committed walkthrough or example artifacts touched by the summary change.
3. Check that the markdown/JSON output makes the next focus group and priority label obvious.

## Handoff questions

- Which focus group should a reviewer open first?
- Is the queue share or source-case rate visible enough for shard sizing?
- If two groups tie, does the summary explain the tie clearly?

## Commit rule

Do not commit reviewer-queue output changes until tests pass and generated examples are refreshed.