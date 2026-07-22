---
name: dh-dev
description: "End-to-end orchestrator for code improvement tasks on existing codebases. Chains explore (code analysis) → context gathering with a one-sentence restate confirmation gate → plan authoring by a dedicated max-reasoning planning agent (Fable 5, max reasoning effort — detailed implementation steps, Definition of Done, adversarial test environment) → adversarial plan preview (parallel contrarian/gap-hunter review lanes) → user review (approve/reject/comment loop) → goal-driven implementation by a dedicated executor agent (Opus 4.8, max reasoning effort) → revision-tracker (revision logging, code quality check, git commit). Use when: adding features to existing code, refactoring modules, performance optimization, bug fixing, improving code quality, enhancing existing functionality, or any code improvement requiring structured planning and tracked execution. Triggers: '기능 개선', '기능 추가', '리팩토링', 'improve', 'enhance', 'refactor', 'optimize', 'fix bug', 'code improvement'."
---
# dh-dev

Orchestrate code improvement tasks through four sequential phases.

```
Step 1 ──→ Step 2 ──→ Step 3 ──→ Step 4
Analyze     Review     Execute    Review
& Plan      (user)     (impl)    & Commit

Step 1 detail:
1-a Analyze → 1-b Context/Interview → 1-c Restate ✓ → 1-d Plan (agent) → 1-e Adversarial Preview
```

> **Effort:** Run this workflow at maximum reasoning effort. If the current effort is below `max` and the user has not explicitly requested a lower level, raise it to `max` before Step 1 and keep it there through implementation.

## Agent & Model Policy

Plan authoring, the adversarial preview lanes, and execution each run in **dedicated subagents** — never in the orchestrator context.

| Phase | Agent | Model | Reasoning effort |
| --- | --- | --- | --- |
| Step 1-d Plan Authoring | dedicated planning agent | Fable 5 (`fable`); fallback: highest-reasoning model available (`opus`) | maximum — `effort: "max"` (ultracode-equivalent) |
| Step 1-e Adversarial Preview | 2 parallel review lanes: `contrarian`, `gap_hunter` | Sonnet (`sonnet`); fallback: default model | standard — lanes critique a finished draft, they do not author; max effort is reserved for 1-d and Step 3 |
| Step 3 Execute | dedicated executor agent | Opus 4.8 (`opus`) | maximum — `effort: "max"` (ultracode-equivalent) |

- **Claude Code**: spawn via the `Agent`/`Task` tool with the `model` override. Set reasoning effort to maximum when the harness exposes it (e.g., Workflow `agent(..., {effort: "max"})`); otherwise place an explicit maximum-reasoning directive (`ultrathink`) at the top of the agent prompt.
- **Codex / environments without subagent model or effort control**: run the phase as a separate, single-purpose pass in the current context with maximum reasoning. All other rules (inputs, required outputs, goal contract) still apply. For Step 1-e, run the two lanes as two sequential single-purpose passes and synthesize afterward.
- Subagents cannot interact with the user. All questions, interviews, and approvals happen in the orchestrator (main context) — never inside the planning or executor agents.

## Step 1: Analyze & Plan

### 1-a. Code Analysis

Explore target files/modules to understand current structure, behavior, and dependencies.

- Use `explore` agent to scan target code — file list, function/class structure, call relationships
- If target code cannot be found, ask user to confirm path/file

### 1-b. Context Gathering

Run `plan-context` Phase A in the orchestrator to build the context summary:

- Incorporate context from `docs\revision_history.md`, `docs\plan_history.md`, wiki knowledge, and change history — git history when `.git` exists, file-system mtime when `.git` is absent (handled by plan-context Phase A)
- If requirements are vague, interview the user here per plan-context Interview Mode mechanics — one question at a time, ambiguity ledger (모호성 원장), Refine gate, fact-confirmation routing (see plan-context references/planning-workflow.md, Interview Mode) — the planning agent cannot ask the user anything

### 1-c. Restate Gate (재진술 확인 게이트)

Run in the orchestrator immediately after 1-b, **before** spawning the expensive planning agent. No subagent, no max-reasoning cost — one cheap checkpoint to prevent a wasted max-reasoning plan built on a misunderstanding.

1. Restate the agreed goal as **one sentence** covering target (what/where), the change, and the success criterion. Derive it from the 1-b answers and, when present, the resolved ambiguity-ledger tracks. Test: a third party reading only this sentence should reach the same conclusion about what is being built.
2. Confirm via `AskUserQuestion` (Codex: plain-text question, end the turn). Options:
   - **Yes, proceed to planning** — pass the confirmed sentence to 1-d as the top-line goal statement
   - **Adjust wording** — apply the user's correction and restate again (max 3 cycles; after the 3rd, ask the user to write the sentence verbatim and use it as-is)
   - **Missing scope** — return to the 1-b interview for the missing scope, then restate again
3. The confirmed sentence feeds the planning-agent input and the plan's Requirements Summary. Everything else from 1-b is passed to 1-d in full multi-section form — the restatement is the only place where one-line compression is the goal.

Confirming the restatement authorizes **plan authoring (1-d) only**. It is not approval to implement — the Step 2 hard gate is unchanged.

### 1-d. Plan Authoring (dedicated planning agent)

Spawn the planning agent per the Agent & Model Policy. Do **not** author the plan in the orchestrator context.

Agent input — include all of:

- User requirements and interview answers from 1-b
- The confirmed goal restatement from 1-c (top-line goal statement)
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

### 1-e. Adversarial Plan Preview (계획 초안 적대적 검증)

Pressure-test the draft **before** the user sees it (Step 2). Spawn both lanes in one parallel batch per the Agent & Model Policy:

- **`contrarian` lane** — attacks the draft: hidden assumptions, scope-creep risk, design decisions the plan makes implicitly without recording them, directives that contradict the 1-a analysis or user-stated 1-b constraints.
- **`gap_hunter` lane** — hunts omissions: missing acceptance criteria, unhandled edge cases, Definition of Done items that are not binary-checkable, DoD items with no matching adversarial test, constraints stated in 1-b but absent from the plan.

Lane input: the plan draft, the confirmed restatement (1-c), the 1-a analysis, and the 1-b context summary. Lane output: a findings list, each as `severity (HIGH/MEDIUM/LOW) — plan section — finding — suggested fix`. Lanes only critique — they never edit the plan and never talk to the user.

Deterministic synthesis (orchestrator):

1. **Structure check (gate)** — checked locally by the orchestrator, no agent: all 8 Required Plan Sections present; every DoD item binary-checkable; every DoD item mapped to at least one adversarial test. Any failure counts as a HIGH finding.
2. Any HIGH finding → return to 1-d **once**: re-spawn the planning agent with all findings appended and the instruction to address each finding or state a per-finding disposition. After this single revision, re-run the structure check only — do **not** re-spawn the lanes.
3. No HIGH findings, or the single revision cycle is done → proceed. Carry every remaining finding and disposition into Step 2 as **Reviewer notes (검토 노트)**; mark any unresolved HIGH finding as such.

The panel runs once per fresh draft; Step 2 Comment-loop revisions are user-directed and are not re-panelled. The panel never approves the plan — only the user approves, in Step 2.

Post-processing (orchestrator, after the 1-e verdict): save the returned plan to `docs\plans\YYYY-MM-DD_HHMMSS_<slug>.md` and update `docs\plan_history.md`. plan-context Phase B applies here **only** for file naming, directory creation, and plan_history indexing — the document body is the planning agent's output with the Required Plan Sections preserved verbatim (prepend the Date/Status metadata header from templates.md; do not restructure into the Summary/Background/Proposal template).

## Step 2: User Review

Present the plan summary, affected file list, and the 1-e Reviewer notes (검토 노트) — including any unresolved HIGH finding, marked as such. Offer three choices:

| Choice | Action |
| --- | --- |
| **Approve** | Proceed to Step 3 |
| **Reject** | Set plan status to `Rejected (user rejected)` in `docs\plan_history.md`, record reason, end skill |
| **Comment** | Revise plan per user feedback, mark previous plan `Superseded`, return to Step 1-d |

**Hard gate**: Stop after presenting these choices. Do not continue to Step 3 until the user explicitly replies with approval after seeing the plan. A user's initial request to "proceed", "go ahead", or use this skill is not approval for Step 3.

Before explicit approval:
- Do not edit implementation/source files except the plan document and plan history entry.
- Do not set the plan status to `In Progress`.
- Do not spawn the executor agent, or invoke `/revision-tracker` or any other executor.

In Codex, if a clickable approval UI is unavailable, ask a plain-text approval question and end the turn.

Comment loop: max **5** iterations. After 5, present final version with approve/reject only. Summarize changes as diff on each iteration. Plan revisions also run through the dedicated planning agent (Step 1-d) with the user feedback appended to its input.

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
| Restate gate not converging after 3 cycles | Ask the user to write the one-sentence goal verbatim; use it as-is |
| HIGH findings remain after the single 1-e revision cycle | Do not loop again; surface them unresolved in Step 2 Reviewer notes — the user decides |
| Environment lacks parallel subagents for 1-e | Run the two lanes sequentially (Agent & Model Policy fallback) |
