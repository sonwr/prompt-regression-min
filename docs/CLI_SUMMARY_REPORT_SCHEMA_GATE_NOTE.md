# CLI summary report schema gate note

Keep summary handoff changes small and reviewable: when a run emits machine-readable summary output plus markdown handoff text, the schema contract should remain explicit before pushing formatting-only tweaks.

Use `--require-summary-schema-version` during verification when a workflow depends on stable JSON payload shape, and keep the markdown handoff aligned with the same validated summary data instead of inventing a parallel status path.

The shortest safe slice is one schema-checked summary run plus one matching markdown artifact, then commit only after the validation command stays green.
