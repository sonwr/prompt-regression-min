# CLI summary status slice note

Keep the reporting loop on one deterministic slice.

- Run the smallest meaningful dataset slice before widening coverage.
- Keep owner, status, and artifact output paths in the same summary bundle.
- Push only after the validation command passes on that same slice.
