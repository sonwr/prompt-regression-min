## prompt-regression-min summary
- Status: **FAIL**
- Summary schema version: `1`
- Pass-rate trend: `regressing`
- Regression IDs: `auth-login`
- Outcome: the walkthrough FAIL fixture still demonstrates a deterministic regression reviewers can paste directly into a blocking PR comment.
- Reviewer next step: keep the PR blocked until `auth-login` is fixed, then rerun `./scripts/regenerate_walkthrough_artifacts.sh` to refresh the committed reviewer note.
