## word-count release-note gate
- Status: **FAIL**
- Summary schema version: `1`
- Pass-rate trend: `regressing`
- Regression ids: `release-note-bullets`, `release-note-short`
- Why it failed: both candidate release notes fell below the configured minimum word-count band.
- Reviewer next step: ask the author to expand the candidate release notes, then rerun `./scripts/regenerate_walkthrough_artifacts.sh` before merging.
