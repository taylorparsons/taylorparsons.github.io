# Feature Spec: 20261020-publish

Status: Done
Created: 2026-10-20
Inputs: CR-20261020-1312
Decisions: D-20261020-1313, D-20261020-1331

## Summary

Publish the reviewed security, lint, and workflow changes to protected main.

## Requirements

- FR-008: Publish changes. (Sources: CR-20261020-1312; D-20261020-1313)
  Use a branch and PR merge, preserve prior commits, and ignore Finder metadata.
- FR-009: Verify release. (Sources: CR-20261020-1312; D-20261020-1331)
  Confirm remote and local main, Pages completion, and homepage availability.
  Use Actions publishing and prevent competing legacy root builds.

## Acceptance

1. A PR containing the reviewed commits merges into main without weakening
   branch protection. Finder metadata is not tracked. (Verifies: FR-008)
2. Remote main contains the implementation commits and local main is aligned.
   The Pages workflow succeeds and the public homepage responds successfully.
   The weekly Dependabot configuration exists on the default branch.
   (Verifies: FR-009)
3. Owl records the merge and deployment evidence. (Verifies: FR-009)

## Edge cases

- If remote main has advanced, reconcile through the PR before merging.
  (Verifies: FR-008)
- Keep deployment failures visible; resolve release failures before claiming
  the site is published successfully. (Verifies: FR-009)
