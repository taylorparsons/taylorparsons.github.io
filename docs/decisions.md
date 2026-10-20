# Decisions (append-only)

## D-20261020-1231
Date: 2026-10-20 12:31
Inputs: CR-20261020-1231
PRD: Security and lint remediation

Decision: Fix the reported collector and lint issues on the current local main at cf85f00. Permit only HTTPS downloads, validate redirect targets, and use defusedxml for both Maven XML paths. Declare the collector dependency and browser ESLint configuration. Preserve rendered site content and existing deployment permissions and triggers.
Rationale: The reported patterns reproduce locally. HTTPS validation must cover redirects as well as initial URLs; hardened XML parsing provides explicit entity protection. Default arguments bind the immediate renderer's enclosing-loop values without changing its output. Initialize only the ATHENA gateway and audit records required by the user's repository instructions.
Alternatives considered: Suppressing Bandit findings would not provide security protection. Adding an HTTP client dependency is unnecessary. Repository protection and remote settings changes are outside this fix request. The reported scan commit 170a2325 is not the current checkout; no remote update is needed to fix the same local patterns.

## D-20261020-1242
Date: 2026-10-20 12:42
Inputs: CR-20261020-1242
PRD: Git workflow hardening

Decision: Address the two earlier findings: enable GitHub main-branch protection and Dependabot alerts/security updates, and prepare weekly GitHub Actions and pip version-update configuration locally.
Rationale: The current GitHub admin API confirms no protection or rulesets and disabled vulnerability alerts and automated fixes. Require pull requests, prohibit force pushes and deletion, and enforce protection for administrators. Set zero required approvals so the owner can merge their own PRs. Do not require status checks that run only after a push to main. Existing local commits stay local because this request does not explicitly ask for a push or PR.
Alternatives considered: Requiring another person's review would block a solo maintainer. Requiring the existing post-push deployment check would block PR merges. Merely preparing a local settings payload would leave both remote findings open. Adding unrelated hooks, commit conventions, signing, or scanning workflows is outside the earlier findings.
