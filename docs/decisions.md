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

## D-20261020-1313
Date: 2026-10-20 13:13
Inputs: CR-20261020-1312
PRD: Publication

Decision: Publish the four reviewed local commits through a temporary branch and pull request, then merge into main with a merge commit, fast-forward local main, and verify the Pages deployment. Ignore Finder .DS_Store metadata that appeared as untracked files.
Rationale: The user explicitly authorized checking in and pushing the changes to remote main. Administrator-enforced branch protection requires a PR. A merge commit preserves the existing ATHENA-linked implementation history without disabling protection. Current remote main remains cf85f006b532c72710a84dbe87585cbfe3708387. Repository settings permit merge commits.
Alternatives considered: A direct main push would be rejected. Bypassing or weakening protection is unnecessary. Squashing would discard the existing traceable commit chain. Finder metadata is not source material and will be ignored rather than committed.

## D-20261020-1331
Date: 2026-10-20 13:31
Inputs: CR-20261020-1312
PRD: Publication

Decision: Change GitHub Pages build_type from legacy to workflow and redeploy the reviewed artifact through the existing Actions workflow.
Rationale: Remote main and both Actions deployment jobs succeeded, but repeated public homepage requests returned GitHub HTTP 404. The Pages API reported legacy publishing from main at /, while the renderer writes index.html under site/ and the workflow uploads site/. Root-source publishing cannot serve the generated homepage. The existing README explicitly requires GitHub Actions as the Pages source. A one-setting correction aligns hosting with the reviewed artifact.
Alternatives considered: Committing generated HTML to the repository root would duplicate build output and bypass the existing design. Moving the source to docs would publish audit records instead of the site. No application code or branch protection changes are needed.

## D-20261104-1541
Date: 2026-11-04 15:41
Inputs: CR-20261104-1541
PRD: Project catalog

Decision: Add Selenium MCP as a ninth project entry with its generated project guide and upstream recognition card, following the existing catalog pattern. Describe it as a local MCP browser automation server for Claude and Codex with a compact default tool profile for testing web apps and automating online workflows.
Rationale: The request says to follow the same pattern as other projects. The public README describes MCP browser control and test generation, plus a 42-tool default profile estimated at about 3.8k tokens.
Alternatives considered: Add only a homepage link, rejected because the catalog's existing project pattern includes setup details and recognition; claim broader functionality beyond the README, rejected to keep copy evidence-bound.

## D-20261104-1546
Date: 2026-11-04 15:46
Inputs: CR-20261104-1541
PRD: Project catalog additions

Decision: Use the upstream README at commit 80d7e95fa53abccab8733897ee2598892dac3fae for the tool count and context size: 43 core tools at about 3.9k tokens, or 77 tools at about 6.4k tokens with SELENIUM_MCP_TOOLS=all.
Rationale: The exact current README differs from a cached search result, so the source revision controls the portfolio copy.
Alternatives considered: Keep the cached 42-tool and 3.8k-token figures, rejected because they are stale for the reviewed source revision.

## D-20261104-1623
Date: 2026-11-04 16:23
Inputs: CR-20261104-1622
PRD: Project catalog additions

Decision: Replace all Selenium MCP portfolio and recognition data with Taylor's Rust repository at https://github.com/taylorparsons/selenium-mcp, reviewed at main commit f07674da48494dad8d06c9cafe23da41c819d8ed. Describe the Rust MCP server, its under-30 MB idle RSS claim, optional Chroma and FFmpeg integrations, Chrome automation, Claude setup, and generic stdio MCP client registration from that revision.
Rationale: The previous project URL resolved to an unrelated Python implementation. The user confirms their work is the Rust repository at the supplied Taylor Parsons URL.
Alternatives considered: Retain the Python content because GitHub redirected there, rejected because it is not the user's project; describe Codex-specific configuration, deferred because the Rust README only documents Claude Code CLI and generic stdio MCP client configuration.
