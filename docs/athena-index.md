# Athena Feature Index

**Purpose**: Lightweight index to reduce token overhead by loading only active features.  
**Last updated**: 2026-10-20

## How to Use This Index

**For Athena agents**: Load this athena-index.md first. Only load specs marked as "Active" below. Skip "Archived" features unless explicitly requested by user.

**For humans**: This index shows all features. Archived features are complete and should not be modified.

---

## Active Features (Load these during sessions)

*No active features currently. All features are archived.*

---

## Archived Features (Skip unless explicitly requested)

### 20261020-git-hardening
- **Status**: Done
- **Spec**: docs/specs/20261020-git-hardening/spec.md
- **Summary**: 

### 20261020-security-lint
- **Status**: Done
- **Spec**: docs/specs/20261020-security-lint/spec.md
- **Summary**: 

---

## Token Optimization

**Without athena-index.md**:
- Load all 2 specs = ~1,000 tokens

**With athena-index.md**:
- Load athena-index.md only = ~1100 tokens
- Load 0 active specs = ~0 tokens
- **Total**: ~1100 tokens
- **Savings**: ~-10% reduction

**Usage Pattern**:
1. Athena loads athena-index.md first
2. Identifies active features (currently: 0)
3. Skips 2 archived features
4. If user asks about archived feature, load on-demand
