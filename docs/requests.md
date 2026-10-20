# Customer Requests (append-only)

## CR-20261020-1231

### Metadata
- **Date:** 2026-10-20 12:31
- **Source:** chat

### Request (verbatim):
can you review and fix these ?
Bandit Security Scan: taylor
Branch: main (170a2325)

Summary:

🔴 HIGH Severity: 0
🟡 MEDIUM Severity: 3
🟢 LOW Severity: 0
Total Issues: 3
Scan Configuration:

Minimum Severity: MEDIUM
Minimum Confidence: MEDIUM
Files Scanned: 429 lines of code
🟡 MEDIUM Severity Issues (3)
1. blacklist
CWE: 22 - https://cwe.mitre.org/data/definitions/22.html

Confidence: HIGH

Location: ./scripts/collect_credits.py:27

Issue: Audit url open for permitted schemes. Allowing use of file:/ or custom schemes is often unexpected.

Code:

26             try:
27                 with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=25) as response:
28                     text = response.read().decode('utf-8')

More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b310-urllib-urlopen

2. blacklist
CWE: 20 - https://cwe.mitre.org/data/definitions/20.html

Confidence: HIGH

Location: ./scripts/collect_credits.py:98

Issue: Using xml.etree.ElementTree.fromstring to parse untrusted XML data is known to be vulnerable to XML attacks. Replace xml.etree.ElementTree.fromstring with its defusedxml equivalent function or make sure defusedxml.defuse_stdlib() is called

Code:

97             pom_url = 'https://repo.maven.apache.org/maven2/' + group.replace('.', '/') + '/' + artifact + '/' + version + '/' + artifact + '-' + version + '.pom'
98             root = ET.fromstring(get(pom_url)); ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
99             source = root.findtext('m:scm/m:url', namespaces=ns) or root.findtext('m:url', namespaces=ns) or ''

More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b313-b320-xml-bad-elementtree

3. blacklist
CWE: 20 - https://cwe.mitre.org/data/definitions/20.html

Confidence: HIGH

Location: ./scripts/collect_credits.py:199

Issue: Using xml.etree.ElementTree.fromstring to parse untrusted XML data is known to be vulnerable to XML attacks. Replace xml.etree.ElementTree.fromstring with its defusedxml equivalent function or make sure defusedxml.defuse_stdlib() is called

Code:

198     elif base == 'pom.xml':
199         root = ET.fromstring(text); ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
200         for dep in root.findall('.//m:dependency', ns):

More Info: https://bandit.readthedocs.io/en/1.9.4/blacklists/blacklist_calls.html#b313-b320-xml-bad-elementtree



🔴 Lint Scan: taylor
Branch: main | Duration: 1.16s | Linters Executed: 4

Summary
| Linter | Files Scanned | 🔴 Errors | 🟡 Warnings | 🔵 Info | Total | Status | |---|---|---|---|---|---|---| | ruff | 4 | 1 | 12 | 0 | 13 | ⚠️ Issues | | eslint | 1 | 0 | 0 | 0 | 0 | ❌ Failed | | yamllint | 1 | 3 | 6 | 0 | 9 | ⚠️ Issues | | markdownlint | 2 | 0 | 12 | 0 | 12 | ⚠️ Issues | | Total | — | 4 | 30 | 0 | 34 | — |

Detailed Findings
ruff (13 findings)
🟡 scripts/build.py:2:1 — [I001] Import block is un-sorted or un-formatted
🔴 scripts/build.py:3:14 — [F401] json imported but unused
🟡 scripts/build.py:13:2 — [C408] Unnecessary dict() call (rewrite as a literal)
🟡 scripts/build.py:14:2 — [C408] Unnecessary dict() call (rewrite as a literal)
🟡 scripts/build.py:15:2 — [C408] Unnecessary dict() call (rewrite as a literal)
🟡 scripts/build.py:16:2 — [C408] Unnecessary dict() call (rewrite as a literal)
🟡 scripts/build.py:17:2 — [C408] Unnecessary dict() call (rewrite as a literal)
🟡 scripts/build.py:18:2 — [C408] Unnecessary dict() call (rewrite as a literal)
🟡 scripts/build.py:19:2 — [C408] Unnecessary dict() call (rewrite as a literal)
🟡 scripts/collect_credits.py:138:42 — [invalid-syntax] Compound statements are not allowed on the same line as simple statements
🟡 scripts/credits.py:65:52 — [B023] Function definition does not bind loop variable x
🟡 scripts/credits.py:75:50 — [B023] Function definition does not bind loop variable source_root
🟡 scripts/credits.py:75:75 — [B023] Function definition does not bind loop variable repo

yamllint (9 findings)
🟡 ./.github/workflows/deploy.yml:1:1 — [document-start] missing document start "---"
🟡 ./.github/workflows/deploy.yml:6:1 — [truthy] truthy value should be one of [false, true]
🟡 ./.github/workflows/deploy.yml:30:73 — [comments] too few spaces before comment: expected 2
🟡 ./.github/workflows/deploy.yml:34:80 — [comments] too few spaces before comment: expected 2
🔴 ./.github/workflows/deploy.yml:34:81 — [87 > 80 characters) (line-length] line too long
🟡 ./.github/workflows/deploy.yml:38:86 — [comments] too few spaces before comment: expected 2
🔴 ./.github/workflows/deploy.yml:38:81 — [93 > 80 characters) (line-length] line too long
🟡 ./.github/workflows/deploy.yml:58:77 — [comments] too few spaces before comment: expected 2
🔴 ./.github/workflows/deploy.yml:58:81 — [84 > 80 characters) (line-length] line too long

markdownlint (12 findings)
🟡 assets/images/IMAGES.md:8:81 — [error] MD013/line-length Line length [Expected: 80; Actual: 132]
🟡 README.md:3:28 — [error] MD034/no-bare-urls Bare URL used [Context: "https://taylorparsons.github.i..."]
🟡 README.md:12:81 — [error] MD013/line-length Line length [Expected: 80; Actual: 148]
🟡 README.md:12:6 — [error] MD034/no-bare-urls Bare URL used [Context: "http://localhost:8000/"]
🟡 README.md:16:81 — [error] MD013/line-length Line length [Expected: 80; Actual: 211]
🟡 README.md:20:81 — [error] MD013/line-length Line length [Expected: 80; Actual: 322]
🟡 README.md:24:81 — [error] MD013/line-length Line length [Expected: 80; Actual: 136]
🟡 README.md:28:81 — [error] MD013/line-length Line length [Expected: 80; Actual: 384]
🟡 README.md:30:81 — [error] MD013/line-length Line length [Expected: 80; Actual: 422]
🟡 README.md:32:81 — [error] MD013/line-length Line length [Expected: 80; Actual: 407]
🟡 README.md:34:81 — [error] MD013/line-length Line length [Expected: 80; Actual: 223]
🟡 README.md:38:81 — [error] MD013/line-length Line length [Expected: 80; Actual: 380]

## CR-20261020-1242

### Metadata
- **Date:** 2026-10-20 12:42
- **Source:** chat

### Request (verbatim):
are you also able to fix the issus found with $git-workflow-automation

## CR-20261020-1312

### Metadata
- **Date:** 2026-10-20 13:12
- **Source:** chat

### Request (verbatim):
ok check in change on main and push to remote
