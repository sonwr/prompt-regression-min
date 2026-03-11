# Reviewer queue report-owner alias note

Use this when a regression summary fixture still carries `report_author` or `report_authors` fields and you want the release note to preserve ownership without a schema detour.

Keep the loop short:
1. confirm the alias still lands in the human summary
2. confirm JSON stays machine-readable
3. reopen only after the same bundle stays green
