---
name: plan-context
description: "Provide project context before planning, execute structured planning workflow, and archive completed plans to docs\\plans\\ with indexing at docs\\plan_history.md. Read docs\\revision_history.md and docs\\plan_history.md to understand prior changes and past plans. Search existing plans for similar topics. Supports interview, direct, consensus (RALPLAN-DR), and review modes. Triggers when: entering plan mode, writing proposals/plans/specs/reviews (제안서/계획서/사양서/검토서), 'plan this', 'plan the'."
---

# Plan Context

Provide project context before planning and archive completed plans as structured documents.

## Phase A: Pre-Planning Context Check

Execute **before** starting plan work.

### 0. Detect Project State

Before gathering context, check which sources are available. The combination determines which branches of Phase A run.

| Check | How |
| --- | --- |
| Git repository | `.git` directory exists at project root |
| Revision history | `docs\revision_history.md` exists |
| Plan history | `docs\plan_history.md` exists |
| Wiki knowledge base | `docs\wiki\` directory exists |

Behavior matrix:

| `.git` | `revision_history.md` | `plan_history.md` | `docs\wiki\` | Phase A Branch |
| --- | --- | --- | --- | --- |
| ✓ | ✓ | ✓ | ✓ | Full path: Steps 1, 2, 3-A, 4, 5, 6 (Git variant summary) |
| ✓ | ✗ or ✓ | ✗ or ✓ | ✗ or ✓ | Steps 1/2 skipped if file missing; 3-A always runs; Step 5 skipped if `docs\wiki\` missing |
| ✗ | ✓ | ✓ or ✗ | ✗ or ✓ | Steps 1/2 run from docs only; 3-B replaces 3-A; Step 5 runs only if `docs\wiki\` exists |
| ✗ | ✗ | ✗ | ✗ | Bootstrap: announce first plan, run 3-B with file system only; Step 5 skipped |

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

### 3. Explore Change History (변경 이력 탐색)

Branch based on Step 0 detection. Run **3-A** when `.git` exists, otherwise **3-B**. Never run both.

#### 3-A. Git Repository

- Run `git log --oneline -10` — understand recent commit topics and pace
- Run `git diff --stat` — identify currently unstaged changes
- If `docs\revision_history.md` exists, cross-reference: note commits not yet reflected in revision_history

#### 3-B. Non-Git Project

When `.git` is absent, derive change context from the file system and revision tracker.

- If `docs\revisions\` exists: list the 5 most recently modified revision files and read their summaries
- Collect recently modified source files (last 7 days):
  - PowerShell: `Get-ChildItem -Recurse -File | Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) } | Sort-Object LastWriteTime -Descending | Select-Object -First 20`
  - Bash: `find . -type f -mtime -7 -not -path '*/node_modules/*' -not -path '*/.*' | xargs ls -lt | head -20`
  - Or use `Glob` followed by inspecting file metadata via `Read`/`Bash`
- If `docs\revision_history.md` exists, cross-reference modified files against documented revisions; note files modified but not logged
- Record in the Context Summary that no git tracking is present — change history is approximate (mtime-based, not commit-based)
- If neither `.git` nor `docs\revision_history.md` exists, note this is a **bootstrap state** and proceed with the file-system snapshot only

### 4. Search Similar Past Plans

Extract keywords from the current planning topic and search for similar cases:

- Search `docs\plan_history.md` for matching entries
- Search `docs\plans\` directory for related documents
- If similar past plans are found, read them and note:
  - Success/failure factors
  - Approach taken
  - Open questions or lessons learned

### 5. Search Wiki Knowledge Base (위키 지식 탐색)

If `docs\wiki\` exists, use the `dh-wiki` skill to surface persisted knowledge relevant to the planning topic. Skip this step if the directory is absent.

- Extract 2-5 keywords from the planning topic (domain terms, component names, technologies)
- Run `dh_wiki_query({ query: "<keyword>" })` for the primary keyword; add `tags`/`category` filters when the topic clearly maps to one (e.g., `architecture`, `decision`, `pattern`, `convention`)
- Optionally run `dh_wiki_list()` first to scan available pages when keywords are uncertain
- For each hit, call `dh_wiki_read({ page: "<slug>" })` and note:
  - Existing architectural decisions or patterns that constrain the plan
  - Prior debugging notes or conventions that should be honored
  - Cross-references (`[[page-name]]`) worth following
- Record findings to feed into the Context Summary (Wiki Knowledge section)

### 6. Present Context Summary

Present a concise summary to inform the planning work. Use the **Git variant** when `.git` exists, otherwise use the **Non-Git variant**.

**Git variant:**

```
## Project Context

### Recent Changes (최근 변경)
- <date> — <summary> (from revision_history)

### Change History (변경 이력) — git
- Recent commits: <last 10 commits summary>
- Unstaged changes: <file list or "none">
- Untracked in revision_history: <commits not in revision_history, if any>

### Related Past Plans (관련 과거 계획)
- <date> — <title> (Status: <status>) — <key takeaway>

### Similar Cases (유사 사례)
- <plan title> — <relevance and lessons>

### Wiki Knowledge (위키 지식)
- <page-slug> — <key fact / constraint relevant to this plan>
- (omit section if `docs\wiki\` is absent or no relevant pages found)

### Notes
- <any important context, caveats, or dependencies>
```

**Non-Git variant:**

```
## Project Context

### Recent Changes (최근 변경)
- <date> — <summary> (from revision_history, if exists)

### Change History (변경 이력) — file system (no git)
- Recent file modifications (last 7 days): <file list with mtime, top 10>
- Recent revision entries: <last 5 entries from docs/revisions/, if exists>
- Untracked in revision_history: <files modified but not logged, if any>

### Related Past Plans (관련 과거 계획)
- <date> — <title> (Status: <status>) — <key takeaway>

### Similar Cases (유사 사례)
- <plan title> — <relevance and lessons>

### Wiki Knowledge (위키 지식)
- <page-slug> — <key fact / constraint relevant to this plan>
- (omit section if `docs\wiki\` is absent or no relevant pages found)

### Notes
- No git tracking: change history is mtime-based and approximate
- <any important context, caveats, or dependencies>
```

If none of `revision_history.md`, `plan_history.md`, or `.git` exists, state this appears to be the first documented plan (bootstrap state) and proceed with the Non-Git variant using only the file-system snapshot.

For the canonical template files see `references/templates.md` (Context Summary Templates section).

## Phase A-2: Planning Workflow

After presenting the context summary, execute the planning workflow. Select mode based on the request:

| Mode | Trigger | Behavior |
| --- | --- | --- |
| Interview | Default for broad/vague requests | Interactive requirements gathering, one question at a time |
| Direct | `--direct`, or detailed request | Skip interview, generate plan immediately |
| Consensus | `--consensus`, "ralplan" | Planner -&gt; Architect -&gt; Critic loop with RALPLAN-DR |
| Review | `--review`, "review this plan" | Critic evaluation of existing plan |

### Core Rules

- Auto-detect interview vs direct mode based on request specificity (broad = vague verbs, no specific files, 3+ areas)
- Ask **one question at a time** during interviews — never batch multiple questions
- Gather codebase facts via `explore` agent **before** asking the user about them
- Classify questions: codebase facts -&gt; explore first; user preferences/scope/requirements -&gt; ask user
- Plans must reference specific files/lines where applicable (80%+ claims)
- Acceptance criteria must be testable (90%+ concrete, no vague terms without metrics)
- **All plan files save to** `docs\plans\` — never to `.omc\plans\`

### Plan Output Format

Every plan includes:

- Requirements Summary
- Acceptance Criteria (testable)
- Implementation Steps (with file references)
- Risks and Mitigations
- Verification Steps
- For consensus: RALPLAN-DR summary (Principles, Decision Drivers, Options) + ADR section

For detailed procedures of each mode, see `references/planning-workflow.md`.

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
| --- | --- | --- |
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
- Planning workflow details: `references/planning-workflow.md`