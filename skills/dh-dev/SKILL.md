---

## name: dh-dev description: "End-to-end orchestrator for code improvement tasks on existing codebases. Chains explore (code analysis) → plan-context (structured planning) → user review (approve/reject/comment loop) → ultrawork (parallel implementation) → revision-tracker (revision logging, code quality check, git commit). Use when: adding features to existing code, refactoring modules, performance optimization, bug fixing, improving code quality, enhancing existing functionality, or any code improvement requiring structured planning and tracked execution. Triggers: '기능 개선', '기능 추가', '리팩토링', 'improve', 'enhance', 'refactor', 'optimize', 'fix bug', 'code improvement'."

# dh-dev

Orchestrate code improvement tasks through four sequential phases.

```
Step 1 ──→ Step 2 ──→ Step 3 ──→ Step 4
Analyze     Review     Execute    Review
& Plan      (user)     (impl)    & Commit
```

## Step 1: Analyze & Plan

### 1-a. Code Analysis

Explore target files/modules to understand current structure, behavior, and dependencies.

- Use `explore` agent to scan target code — file list, function/class structure, call relationships
- If target code cannot be found, ask user to confirm path/file

### 1-b. Planning

Invoke `/plan-context` skill to produce a structured plan.

- Incorporate context from `docs\revision_history.md`, `docs\plan_history.md`, and git history (if `.git` exists)
- Write concrete Implementation Steps with file references
- Include before/after comparison criteria in Acceptance Criteria
- Output: plan document saved to `docs\plans\`

## Step 2: User Review

Present plan summary and affected file list. Offer three choices:

| Choice | Action |
| --- | --- |
| **Approve** | Proceed to Step 3 |
| **Reject** | Set plan status to `Rejected (user rejected)` in `docs\plan_history.md`, record reason, end skill |
| **Comment** | Revise plan per user feedback, mark previous plan `Superseded`, return to Step 1-b |

Comment loop: max **5** iterations. After 5, present final version with approve/reject only. Summarize changes as diff on each iteration.

## Step 3: Execute

1. Update plan status to `In Progress` in `docs\plan_history.md`
2. Invoke `/ultrawork` skill — convert Implementation Steps to tasks, run independent tasks in parallel
3. On error: report to user, confirm whether to fix or abort

## Step 4: Review & Commit

1. Invoke `/revision-tracker` skill — create revision entry, run code quality check, propose git commit
2. Update plan status to `Completed` in `docs\plan_history.md`

## Exceptions

| Situation | Handling |
| --- | --- |
| Target code not found | Ask user for correct path/file |
| Error during Step 3 | Report error, confirm fix or abort |
| Code quality issues in Step 4 | Apply simplify fixes, re-propose commit |
| User requests abort mid-workflow | Record current state in plan_history, end skill |
