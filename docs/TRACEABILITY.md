# Traceability

Use `./scripts/owl show <ID>` to inspect individual requests and decisions.
Use `./scripts/owl why <FR-ID>` for requirements, tasks, and commits.
Never read the requests, decisions, or index files directly.

Feature specifications and task records live under `docs/specs/`.
Session notes record commands, outcomes, decisions, and local commit evidence.
The derived pre-ATHENA Git history is in `docs/audit/git-history.md`.

Install the ATHENA skill under `$CODEX_HOME/skills/athena` (default
`~/.codex/skills/athena`) or set `ATHENA_SKILL_DIR` before using the gateway.
