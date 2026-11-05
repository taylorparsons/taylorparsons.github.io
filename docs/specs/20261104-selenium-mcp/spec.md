# Feature Spec: 20261104-selenium-mcp

Status: Done
Created: 2026-11-04
Inputs: CR-20261104-1541, CR-20261104-1622
Decisions: D-20261104-1541, D-20261104-1546, D-20261104-1623

## Summary

Add Taylor's released Rust Selenium MCP browser automation project to the public
catalog using the existing project and recognition page pattern.

## Requirements

- FR-010: Document Selenium MCP. (Sources: CR-20261104-1541, CR-20261104-1622; D-20261104-1541, D-20261104-1546, D-20261104-1623)
  Add a catalog card, generated project guide, relevant use case, and upstream
  recognition record for Taylor's Rust MCP server. Describe its local browser
  testing, README-reported under-30 MB idle RSS, Cargo installation, and MCP
  client setup from the reviewed repository documentation.

## Acceptance

1. The homepage and use-cases page include Selenium MCP. (Verifies: FR-010)
2. The project guide identifies the Rust implementation, links to its source,
   and gives documented Cargo requirements and setup steps. (Verifies: FR-010)
3. A recognition page exists and links to the reviewed source revision.
   (Verifies: FR-010)

## Edge cases

- Keep unsupported claims about privacy, security, or browser compatibility
  out of the guide. (Verifies: FR-010)
