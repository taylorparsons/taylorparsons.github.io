# Feature Spec: 20261020-git-hardening

Status: Done
Created: 2026-10-20
Inputs: CR-20261020-1242
Decisions: D-20261020-1242

## Summary

Resolve the earlier branch protection and Dependabot findings with live GitHub
settings and locally reviewed version-update configuration.

## Requirements

- FR-005: Protect main. (Sources: CR-20261020-1242; D-20261020-1242)
  Require PRs, forbid force pushes/deletion, and enforce for administrators.
  Zero required approvals preserve solo ownership. No deployment-only checks.
- FR-006: Enable updates. (Sources: CR-20261020-1242; D-20261020-1242)
  Enable alerts and automated security fixes. Prepare weekly Actions/pip updates.
- FR-007: Verify settings. (Sources: CR-20261020-1242; D-20261020-1242)
  Validate configuration, read back settings, and describe publication state.

## Acceptance

1. The protection API returns enabled administrator enforcement, a PR policy
   with zero approvals, and disabled force pushes/deletion. No unavailable
   status checks prevent merges. (Verifies: FR-005, FR-007)
2. GitHub confirms vulnerability alerts and automated fixes enabled.
   (Verifies: FR-006, FR-007)
3. Dependabot configuration parses, passes YAML lint, and covers Actions and
   pip on a weekly schedule. Documentation describes PR-based publishing.
   (Verifies: FR-006, FR-007)
4. Completion evidence distinguishes live settings from the local files that
   require merging into the default branch. (Verifies: FR-007)

## Edge cases

- Never require another reviewer for the owner to merge. (Verifies: FR-005)
- Do not require checks that run only after merging. (Verifies: FR-005)
- API failures must remain visible; do not report an intended policy as live.
  (Verifies: FR-007)
