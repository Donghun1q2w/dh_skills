---
name: revision-tracker
description: "Track project file modifications by generating revision log files under docs\\revisions\\ and maintaining an index at docs\\revision_history.md. Triggers automatically when files in a project are modified. Creates timestamped markdown revision entries with file-level diff summaries and plan/rationale context. Always read docs\\revision_history.md before modifying files to understand project context and prior changes. Use when: files are edited/added/deleted in a project, code changes are made, refactoring is performed, features are added, or bugs are fixed."
---

# Revision Tracker

Generate structured revision logs for every project file modification.

## Pre-Modification: Context Check

**Before modifying any file**, read `docs\revision_history.md` if it exists. Use it to understand:
- Prior changes and their rationale
- Project structure evolution
- Ongoing plans or multi-step work

If the file does not exist, create it after completing the current modification.

## Post-Modification: Revision Logging

After completing file modifications, execute these steps in order:

### 1. Create Revision Entry

Create a file at `docs\revisions\YYYY-MM-DD_HHMMSS_<slug>.md` where:
- `YYYY-MM-DD_HHMMSS` — modification date and time
- `<slug>` — short kebab-case summary (e.g., `fix-auth-bug`, `add-user-api`)

Use the template from `references/templates.md` (Revision Entry Template section).

Content must include:
- **Summary**: One-line description of the change
- **Rationale / Plan**: Why the change was made, plan context if applicable
- **Changed Files**: Table listing each file with status (added/modified/deleted) and brief description
- **Details**: Per-file diff summary — what was added, removed, or changed

### 2. Update Revision History Index

Append an entry to `docs\revision_history.md`. Create the file if it does not exist.

Use the template from `references/templates.md` (Revision History Template section).

Each entry includes:
- Date/time
- One-line summary
- Link to the revision detail file
- List of affected files

### 3. Create Directory If Needed

Ensure `docs\revisions\` directory exists before writing. Create it if missing.

## File Structure

```
project/
├── docs/
│   ├── revision_history.md          # Index of all revisions
│   └── revisions/
│       ├── 2026-03-01_143022_add-login-api.md
│       ├── 2026-03-02_091500_fix-db-connection.md
│       └── 2026-03-03_160045_refactor-auth-module.md
└── src/
    └── ...
```

## References

- File templates: `references/templates.md`
