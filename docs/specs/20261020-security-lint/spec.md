# Feature Spec: 20261020-security-lint

Status: Done
Created: 2026-10-20
Inputs: CR-20261020-1231
Decisions: D-20261020-1231

## Summary

Repair the supplied security and lint findings in the static site tooling.
Keep normal public credit collection and rendered site content working.

## Requirements

- FR-001: HTTPS fetching. (Sources: CR-20261020-1231; D-20261020-1231)
  Validate initial requests and redirects before cache or network use.
- FR-002: Harden XML. (Sources: CR-20261020-1231; D-20261020-1231)
  Use a declared hardened parser on both XML paths.
- FR-003: Correct lint. (Sources: CR-20261020-1231; D-20261020-1231)
  Correct reported lint issues and make browser ESLint runnable.
- FR-004: Verify fixes. (Sources: CR-20261020-1231; D-20261020-1231)
  Record meaningful regression, scan, and build results.

## Acceptance

1. Invalid schemes and missing hosts fail before cache and network access;
   HTTP and file redirects fail, while HTTPS redirects remain supported.
   (Verifies: FR-001, FR-004)
2. Normal Maven manifests and metadata parse; entity payloads are rejected
   by both XML call paths. (Verifies: FR-002, FR-004)
3. The four original Python scripts pass the relevant Ruff rules; Bandit
   reports no medium or high issues. All four linters run successfully on
   their applicable application files. (Verifies: FR-003, FR-004)
4. The site builds with equivalent rendered content and existing deployment
   behavior. (Verifies: FR-003, FR-004)

## Edge cases

- Cached unsafe URLs still fail validation. (Verifies: FR-001)
- Safe cached public metadata remains usable offline. (Verifies: FR-001)
- XML failure remains explicit in source parsing and attribution fallback.
  (Verifies: FR-002)
