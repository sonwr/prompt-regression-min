# Regex flag string alias note

Use a single string like `IGNORECASE|MULTILINE` or `I M` when a fixture should keep regex flags readable without expanding them into a JSON list.

This keeps replay fixtures small while preserving the same validator behavior as `expected.flags: ["IGNORECASE", "MULTILINE"]`.
