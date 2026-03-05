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

### 4. Update Project Documentation

If `README.md` or `CLAUDE.md` exists at project root, check for a directory tree section (code block showing project structure). If found:
- Add any newly created files/directories to the tree
- Remove any deleted files/directories from the tree
- Keep the tree's existing formatting style and indentation

### 5. Code Quality Check (Optional)

If the current session has access to `/simplify` or `/code-review` skills, invoke them on the changed source files **before committing**.

**Trigger conditions** (all must be true):
- Source code files were modified (`.py`, `.js`, `.ts`, `.cs`, `.java`, `.go`, `.rs`, `.c`, `.cpp`, etc.)
- The modification is not a docs-only or config-only change
- At least one skill (`simplify` or `code-review`) is available

**Execution order**:
1. `/simplify` first — fix reuse, quality, efficiency issues in changed code
2. If `/simplify` made changes, update the revision entry's Changed Files and Details sections
3. `/code-review` optionally — only if the user requests or the change is complex (>100 lines, >5 files)

**Skip conditions** (any one):
- Only documentation/config files changed
- User explicitly requests to skip review
- Neither skill is available in the session

### 6. Git Commit

If `.git\` exists at project root, propose a commit after logging the revision.

**Write the commit message using the `/commit` skill** (skill_donghun:commit). Follow its format, type rules, and Korean subject convention.

- **Staged files**: List only the files added/modified/deleted in the current modification (including the revision entry and updated docs)

#### Step 1: Present the commit proposal

Show the proposed commit to the user:

```
Proposed commit:
  git add <file1> <file2> ...
  git commit -m "<type>(<scope>): <subject>

  <description>"
```

Include a description (body) when the change needs context — explain why, not what.

#### Step 2: Ask the user

Ask whether to proceed with the commit. Offer three choices:
- **Commit** — execute as proposed
- **Edit then commit** — let the user modify the message, then execute
- **Skip** — do not commit; leave the proposal as reference only

#### Step 3: Execute or skip

- **Commit / Edit then commit**: Run `git add` for the listed files, then `git commit` with the (possibly edited) message. Report the result (commit hash).
- **Skip**: No action. The proposal remains visible for manual use later.

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
