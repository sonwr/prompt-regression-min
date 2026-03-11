# Reviewer queue report bundle alias note

If one review run should reopen both human and machine artifacts, prefer one shared bundle directory and one shared basename.

Minimal handoff:

- reopen the JSON summary first for exact ids and queue metadata
- reopen the markdown or PR-comment artifact second for human-ready wording
- keep both artifacts under the same bundle name so reruns do not drift

This keeps reviewer queue follow-up deterministic when one rerun produces multiple report surfaces.
