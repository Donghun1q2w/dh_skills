---
name: dh-dev
description: "End-to-end orchestrator for code improvement tasks on existing codebases. Chains explore (code analysis) → plan authoring by a dedicated max-reasoning planning agent (Fable 5, max reasoning effort — detailed implementation steps, Definition of Done, adversarial test environment) → user review (approve/reject/comment loop) → goal-driven implementation by a dedicated executor agent (Opus 4.8, max reasoning effort) → revision-tracker (revision logging, code quality check, git commit). Use when: adding features to existing code, refactoring modules, performance optimization, bug fixing, improving code quality, enhancing existing functionality, or any code improvement requiring structured planning and tracked execution. Triggers: '기능 개선', '기능 추가', '리팩토링', 'improve', 'enhance', 'refactor', 'optimize', 'fix bug', 'code improvement'."
---
# dh-dev

Orchestrate code improvement tasks through four sequential phases.

```
Step 1 ──→ Step 2 ──→ Step 3 ──→ Step 4
Analyze     Review     Execute    Review
& Plan      (user)     (impl)    & Commit
```

> **Effort:** Run this workflow at maximum reasoning effort. If the current effort is below `max` and the user has not explicitly requested a lower level, raise it to `max` before Step 1 and keep it there through implementation.

## Agent & Model Policy

Plan authoring and execution each run in a **dedicated subagent** — never in the orchestrator context.

| Phase | Agent | Model | Reasoning effort |
| --- | --- | --- | --- |
| Step 1-c Plan Authoring | dedicated planning agent | Fable 5 (`fable`); fallback: highest-reasoning model available (`opus`) | maximum — `effort: "max"` (ultracode-equivalent) |
| Step 3 Execute | dedicated executor agent | Opus 4.8 (`opus`) | maximum — `effort: "max"` (ultracode-equivalent) |

- **Claude Code**: spawn via the `Agent`/`Task` tool with the `model` override. Set reasoning effort to maximum when the harness exposes it (e.g., Workflow `agent(..., {effort: "max"})`); otherwise place an explicit maximum-reasoning directive (`ultrathink`) at the top of the agent prompt.
- **Codex / environments without subagent model or effort control**: run the phase as a separate, single-purpose pass in the current context with maximum reasoning. All other rules (inputs, required outputs, goal contract) still apply.
- Subagents cannot interact with the user. All questions, interviews, and approvals happen in the orchestrator (main context) — never inside the planning or executor agents.

## Step 1: Analyze & Plan

### 1-a. Code Analysis

Explore target files/modules to understand current structure, behavior, and dependencies.

- Use `explore` agent to scan target code — file list, function/class structure, call relationships
- If target code cannot be found, ask user to confirm path/file

### 1-b. Context Gathering

Run `plan-context` Phase A in the orchestrator to build the context summary:

- Incorporate context from `docs\revision_history.md`, `docs\plan_history.md`, wiki knowledge, and change history — git history when `.git` exists, file-system mtime when `.git` is absent (handled by plan-context Phase A)
- If requirements are vague, interview the user here (one question at a time, per plan-context rules) — the planning agent cannot ask the user anything

### 1-c. Plan Authoring (dedicated planning agent)

Spawn the planning agent per the Agent & Model Policy. Do **not** author the plan in the orchestrator context.

Agent input — include all of:

- User requirements and interview answers from 1-b
- 1-a analysis results (files, structures, call relationships)
- 1-b context summary (revision/plan history, wiki knowledge, similar past plans)
- The Required Plan Sections below and plan-context quality criteria (`plan-context/references/planning-workflow.md`, Quality Criteria)

Agent mission: using maximum reasoning, produce an **implementation-ready plan so detailed that the executor makes no design decisions of its own** — only follows directives and verifies against the stated conditions.

**Required Plan Sections** (supersets plan-context's standard output format):

1. **Requirements Summary**
2. **Acceptance Criteria** — testable, 90%+ concrete, including before/after comparison criteria against current behavior/metrics (capture the pre-change baseline)
3. **Implementation Steps (구현 지침)** — per step: target file/function references, exact change specification, interfaces/signatures, data structures, algorithm outline, error handling, edge cases. Include pseudocode or an expected-diff sketch for any non-trivial change.
4. **Code Writing Guide (코드 작성 가이드)** — project conventions to follow, patterns to use and to avoid, naming rules, encoding rules (UTF-8 for Korean text), dependency/library constraints
5. **Definition of Done (개발 완료조건)** — binary-checkable conditions only; performance targets quantified ("fast" → "p99 < 200ms")
6. **Adversarial Test Environment (적대적 테스트 환경)** — how to set up and run tests designed to break the implementation: boundary values, malformed/hostile inputs, failure injection, concurrency/scale cases where relevant, plus expected results. Every Definition of Done item maps to at least one test.
7. **Risks and Mitigations**
8. **Verification Steps**

Post-processing (orchestrator): save the returned plan to `docs\plans\YYYY-MM-DD_HHMMSS_<slug>.md` and update `docs\plan_history.md`. plan-context Phase B applies here **only** for file naming, directory creation, and plan_history indexing — the document body is the planning agent's output with the Required Plan Sections preserved verbatim (prepend the Date/Status metadata header from templates.md; do not restructure into the Summary/Background/Proposal template).

## Step 2: User Review

Present plan summary and affected file list. Offer three choices:

| Choice | Action |
| --- | --- |
| **Approve** | Proceed to Step 3 |
| **Reject** | Set plan status to `Rejected (user rejected)` in `docs\plan_history.md`, record reason, end skill |
| **Comment** | Revise plan per user feedback, mark previous plan `Superseded`, return to Step 1-c |

**Hard gate**: Stop after presenting these choices. Do not continue to Step 3 until the user explicitly replies with approval after seeing the plan. A user's initial request to "proceed", "go ahead", or use this skill is not approval for Step 3.

Before explicit approval:
- Do not edit implementation/source files except the plan document and plan history entry.
- Do not set the plan status to `In Progress`.
- Do not spawn the executor agent, or invoke `/revision-tracker` or any other executor.

In Codex, if a clickable approval UI is unavailable, ask a plain-text approval question and end the turn.

Comment loop: max **5** iterations. After 5, present final version with approve/reject only. Summarize changes as diff on each iteration. Plan revisions also run through the dedicated planning agent (Step 1-c) with the user feedback appended to its input.

## Step 3: Execute (dedicated executor agent)

1. Update plan status to `In Progress` in `docs\plan_history.md`
2. If the native `/goal` feature is available, register the plan's Definition of Done items as the active goals for the session
3. Spawn the executor agent per the Agent & Model Policy (Opus 4.8, max reasoning effort). Executor rules:
   - **Goal contract first**: before writing any code, read the plan document and extract the **Definition of Done** and **Adversarial Test Environment** sections. Adopt them as the goal. Meeting every completion condition and passing the adversarial tests is the top priority — above speed and token cost.
   - Implement strictly following the **Implementation Steps** and **Code Writing Guide**. Do not re-litigate design decisions already made in the plan; if a directive is impossible as written, stop and report instead of improvising.
   - **Goal-seeking loop**: implement → build and run the adversarial tests → analyze failures → fix → re-run. Repeat until all Definition of Done items pass. If not converging (e.g., the same test still fails after 5 fix attempts) or genuinely blocked, stop and report the gap with evidence — never ship a partial result as done.
   - Return to the orchestrator: changed-file list, test-run evidence (commands + output), and a Definition of Done checklist with per-item pass/fail.
4. Parallelization: if the Implementation Steps contain independent groups with no file overlap, the orchestrator may spawn one executor agent per group (same model/effort) in parallel; otherwise use a single executor agent.
5. The orchestrator verifies the returned evidence against the plan before Step 4. An executor "done" claim without a fully green Definition of Done checklist is not done.
6. On error: report to user, confirm whether to fix or abort.

## Step 4: Review & Commit

1. Invoke `/revision-tracker` skill — create revision entry, run code quality check, propose git commit
2. Confirm every Definition of Done item is verified with Step 3 evidence, then update plan status to `Completed` in `docs\plan_history.md`

## Exceptions

| Situation | Handling |
| --- | --- |
| Target code not found | Ask user for correct path/file |
| Error during Step 3 | Report error, confirm fix or abort |
| Executor cannot meet a Definition of Done item | Report the gap with evidence; ask user: revise plan / accept as partial / abort |
| Environment lacks subagent model/effort control | Apply the fallback in Agent & Model Policy (separate max-reasoning pass in current context) |
| Code quality issues in Step 4 | Apply simplify fixes, re-propose commit |
| User requests abort mid-workflow | Record current state in plan_history, end skill |
