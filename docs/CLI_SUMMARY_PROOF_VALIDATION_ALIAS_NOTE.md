# CLI_SUMMARY_PROOF_VALIDATION_ALIAS_NOTE

Treat `proof_validation_command` as a JSON-friendly alias of `validation_command` when downstream CI or review bots want one obvious first-proof gate.
Use it for automation that needs a stable field name without changing the underlying validation contract.
