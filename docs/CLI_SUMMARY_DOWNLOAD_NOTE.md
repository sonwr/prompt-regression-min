# CLI summary download note

When a saved summary bundle is headed toward a lightweight web review or a reviewer handoff, keep JSON/Markdown/HTML paths explicit enough to act like download targets.

Small validated loop:

1. rerun the targeted unittest slice
2. regenerate the saved summary artifacts
3. confirm the path summary is still readable in one short status line

That keeps summary output stable for both terminal reviewers and simple download-oriented UIs.
