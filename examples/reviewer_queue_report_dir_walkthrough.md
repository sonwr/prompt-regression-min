# Reviewer queue report-dir walkthrough

Use this mini checklist when reviewer-queue output changes affect more than one artifact at once.

## Goal

Keep JSON, markdown, PR-comment, and stdout handoff surfaces aligned enough that a maintainer can confirm the dominant next focus in one pass.

## Fast proof loop

```bash
python3 -m unittest tests/test_core.py tests/test_cli.py
```

After the tests pass, regenerate the committed walkthrough artifacts that cover the changed summary or rendering surface.

## What to confirm

- The same next-focus group appears across JSON and markdown.
- Tie-break labels and priority language stay consistent.
- PR-comment output still reads like a compact handoff instead of a raw data dump.
- The walkthrough notes mention which artifact is best for humans and which is best for automation.
