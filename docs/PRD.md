# Product requirements

## Existing product

A generated static catalog documents public projects and upstream recognition.
Python scripts build the site and collect public dependency attribution.
GitHub Actions deploys the generated `site/` directory to GitHub Pages.

## Security and lint remediation

- FR-001: HTTPS fetching. (Sources: CR-20261020-1231; D-20261020-1231)
  Restrict requests and redirects to HTTPS URLs with a host. Reject unsafe URLs
  before cache access or network use.
- FR-002: Harden XML. (Sources: CR-20261020-1231; D-20261020-1231)
  Parse downloaded and source Maven XML with entity protection. Declare and
  document the required parser dependency.
- FR-003: Correct lint. (Sources: CR-20261020-1231; D-20261020-1231)
  Resolve reported Python, YAML, and Markdown findings and provide browser
  ESLint configuration while preserving rendered site content.
- FR-004: Verify fixes. (Sources: CR-20261020-1231; D-20261020-1231)
  Check unsafe URL and XML rejection, normal Maven parsing, site rendering,
  and the requested security and lint scans.

## Backlog

- Shipped locally: `20261020-security-lint`, implementing FR-001 through FR-004.
  Sources: CR-20261020-1231; D-20261020-1231. Evidence:
  `tests/test_collect_credits.py` and feature session notes. Pending merge.

## Execution plan

1. Record the supplied scan report and remediation scope through Owl.
2. Harden collector networking and XML parsing; fix syntax and lint findings.
3. Add targeted security regression tests and ESLint configuration.
4. Run Bandit, Ruff, ESLint, yamllint, markdownlint, and the site build.
5. Record evidence and create the local traceable commit.
