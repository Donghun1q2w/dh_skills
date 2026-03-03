---
name: plan-context
description: "Provide project context before planning and archive completed plans to docs\\plans\\ with indexing at docs\\plan_history.md. Read docs\\revision_history.md and docs\\plan_history.md to understand prior changes and past plans. Search existing plans for similar topics. Triggers when: entering plan mode, writing proposals/plans/specs/reviews (제안서/계획서/사양서/검토서)."
---

# Plan Context

Provide project context before planning and archive completed plans as structured documents.

## Phase A: Pre-Planning Context Check

Execute **before** starting plan work.

### 1. Read Revision History

Read `docs\revision_history.md` if it exists. Understand:
- Recent file modifications and their rationale
- Project structure evolution
- Ongoing multi-step work

### 2. Read Plan History

Read `docs\plan_history.md` if it exists. Understand:
- Previous plans and their current status
- Patterns of past decisions
- Deferred or superseded plans that may be relevant

### 3. Search Similar Past Plans

Extract keywords from the current planning topic and search for similar cases:
- Search `docs\plan_history.md` for matching entries
- Search `docs\plans\` directory for related documents
- If similar past plans are found, read them and note:
  - Success/failure factors
  - Approach taken
  - Open questions or lessons learned

### 4. Present Context Summary

Present a concise summary to inform the planning work:

```
## Project Context

### Recent Changes (최근 변경)
- <date> — <summary> (from revision_history)
- <date> — <summary>

### Related Past Plans (관련 과거 계획)
- <date> — <title> (Status: <status>) — <key takeaway>

### Similar Cases (유사 사례)
- <plan title> — <relevance and lessons>

### Notes
- <any important context, caveats, or dependencies>
```

If no history files exist, state that this appears to be the first documented plan and proceed.

## Phase B: Post-Planning Logging

Execute **after** the plan is finalized and approved.

### 1. Create Plan Document

Create a file at `docs\plans\YYYY-MM-DD_HHMMSS_<slug>.md` where:
- `YYYY-MM-DD_HHMMSS` — plan creation date and time
- `<slug>` — short kebab-case title (e.g., `add-auth-system`, `refactor-db-layer`)

Use the template from `references/templates.md` (Plan Document Template section).

Content must include:
- **Summary**: 2-3 sentence overview
- **Background**: Why this plan exists
- **Proposal**: Step-by-step plan details
- **Impact**: Files, dependencies, and risk table
- **Open Questions**: Unresolved items (omit section if none)

### 2. Update Plan History Index

Prepend an entry to `docs\plan_history.md`. Create the file if it does not exist.

Use the template from `references/templates.md` (Plan History Template section).

Each entry includes:
- Date/time
- Plan title
- Link to the plan detail file
- Status (default: **Proposed**)
- 2-3 sentence summary

### 3. Create Directory If Needed

Ensure `docs\plans\` directory exists before writing. Create it if missing.

### 4. Update Project Documentation

If `README.md` or `CLAUDE.md` exists at project root, check for a directory tree section (code block showing project structure). If found:
- Add any newly created files/directories to the tree
- Keep the tree's existing formatting style and indentation

## Boundary with revision-tracker

| Concern | Skill | Output Location |
|---------|-------|-----------------|
| Plan documents | `plan-context` | `docs\plans\`, `docs\plan_history.md` |
| File modification logs | `revision-tracker` | `docs\revisions\`, `docs\revision_history.md` |

Plan document creation triggers `revision-tracker` for the file-level change log separately. This skill does **not** include a commit step — `revision-tracker` handles that.

## File Structure

```
project/
├── docs/
│   ├── plan_history.md               # Index of all plans
│   ├── plans/
│   │   ├── 2026-03-01_143022_add-login-api.md
│   │   ├── 2026-03-02_091500_refactor-db-layer.md
│   │   └── 2026-03-03_160045_add-caching.md
│   ├── revision_history.md           # (managed by revision-tracker)
│   └── revisions/                    # (managed by revision-tracker)
└── src/
    └── ...
```

## References

- File templates: `references/templates.md`
