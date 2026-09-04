---
name: dh-dev
description: "End-to-end orchestrator for code improvement tasks on existing codebases. Chains explore (code analysis) → context gathering that first classifies the development direction (단발성/간단한/심화) and then runs a one-sentence restate confirmation gate → plan authoring by a dedicated planning agent (tiered Large/Medium/Small model/effort, Medium default: Opus at high reasoning effort, Large: Fable at max reasoning effort — detailed implementation steps, Definition of Done, adversarial test environment) → adversarial plan preview (parallel contrarian/gap-hunter review lanes) → user review (approve/reject/comment loop) → goal-driven implementation by a dedicated executor agent (Sonnet fixed for every tier; tiered reasoning effort — Large max / Medium high / Small standard) → revision-tracker (revision logging, code quality check, git commit). Use when: adding features to existing code, refactoring modules, performance optimization, bug fixing, improving code quality, enhancing existing functionality, or any code improvement requiring structured planning and tracked execution. Triggers: '기능 개선', '기능 추가', '리팩토링', 'improve', 'enhance', 'refactor', 'optimize', 'fix bug', 'code improvement'."
---
# dh-dev

Orchestrate code improvement tasks through four sequential phases.

```
Step 1 ──→ Step 2 ──→ Step 3 ──→ Step 4
Analyze     Review     Execute    Review
& Plan      (user)     (impl)    & Commit

Step 1 detail:
1-a Analyze → 1-b Direction + Context/Interview → 1-c Restate ✓ → 1-d Plan (agent) → 1-e Adversarial Preview
```

> **Effort:** Run this workflow at maximum reasoning effort. If the current effort is below `max` and the user has not explicitly requested a lower level, raise it to `max` before Step 1 and keep it there through implementation. This governs the orchestrator context itself; the 1-d and Step 3 subagents run at the model/effort chosen by the Model & Effort Tiering policy below — a Medium/Small tier there does not violate this rule. Step 3 always runs on Sonnet by policy; that is a fixed model choice, not a reduction of this rule.

## Agent & Model Policy

Plan authoring, the adversarial preview lanes, and execution each run in **dedicated subagents** — never in the orchestrator context.

| Phase | Agent | Model | Reasoning effort |
| --- | --- | --- | --- |
| Step 1-d Plan Authoring | dedicated planning agent | tiered — decided in 1-c (see Model & Effort Tiering); Medium (default): Opus (`opus`); Large: Fable (`fable`), fallback: highest-reasoning model available (`opus`); Small: Sonnet (`sonnet`) | tiered — Medium (default): `effort: "high"`; Large: maximum `effort: "max"` (ultracode-equivalent); Small: standard |
| Step 1-e Adversarial Preview | 2 parallel review lanes: `contrarian`, `gap_hunter` | Sonnet (`sonnet`); fallback: default model | standard — lanes critique a finished draft, they do not author; max effort is reserved for 1-d and Step 3 |
| Step 3 Execute | dedicated executor agent | **Sonnet (`sonnet`) — fixed for every tier**; fallback: default model. The tier does not select a model here | tiered — decided at Step 3 item 1 (see Model & Effort Tiering); Medium (default): `effort: "high"`; Large: maximum `effort: "max"` (ultracode-equivalent); Small: standard |

- **Claude Code**: spawn via the `Agent`/`Task` tool with the `model` override. Set reasoning effort to the decided tier's level when the harness exposes it (e.g., Workflow `agent(..., {effort: "max"})` — Large: `"max"`, Medium: `"high"`, Small: harness default); otherwise map the tier to a reasoning directive at the top of the agent prompt — Large: `ultrathink`, Medium: `think hard`, Small: no directive.
- **Codex / environments without subagent model or effort control**: run the phase as a separate, single-purpose pass in the current context with maximum reasoning. All other rules (inputs, required outputs, goal contract) still apply. For Step 1-e, run the two lanes as two sequential single-purpose passes and synthesize afterward. Tiering fallback: when reasoning effort cannot be controlled per pass, still decide and announce the tier, but run every 1-d/Step 3 pass at maximum reasoning regardless of tier — append `(fallback: max reasoning — no effort control)` to the Tier announcement line. A lower tier is never permission to run a weaker pass in such environments. Model fallback: when the model cannot be selected per pass, proceed with whatever default model the environment provides — both the 1-d model tiers and the Step 3 Sonnet fixture are best-effort there. The tier is still decided and announced, and it still selects reasoning effort only.
- Subagents cannot interact with the user. All questions, interviews, and approvals happen in the orchestrator (main context) — never inside the planning or executor agents.

### Model & Effort Tiering (모델·effort 티어링)

1-d Plan Authoring and Step 3 Execute scale their subagent's reasoning effort to the size of the job; 1-d additionally scales the model, while Step 3 always runs on Sonnet. Three tiers — **Medium is the default**. Large is reserved for jobs that positively meet a Large signal; ambiguous or unestimable signals resolve to Medium, not Large.

| Tier | Signals (판정 기준) | 1-d Plan Authoring | Step 3 Execute |
| --- | --- | --- | --- |
| **Large** | 10+ files; architectural change or a modified cross-module contract (public interface); >400 changed lines expected; or any risk-keyword hit — at least one signal must positively land here | Fable (`fable`); fallback `opus` — `effort: "max"` | Sonnet (`sonnet`) — `effort: "max"` |
| **Medium** (default) | 2–9 files; logic changes present but contained inside existing module boundaries; 31–400 changed lines expected; no risk-keyword hit — also the landing tier whenever a signal is ambiguous or unestimable | Opus (`opus`) — `effort: "high"` | Sonnet (`sonnet`) — `effort: "high"` |
| **Small** | single file; no new logic or algorithm (config/docs/typo/rename level); ≤30 changed lines expected; no risk-keyword hit | Sonnet (`sonnet`) — standard effort | Sonnet (`sonnet`) — standard effort |

**Classification checklist (판정 체크리스트)** — run by the orchestrator alone: deterministic, no subagent, and never an extra user question (the tier is announced, not asked). Score every signal, then take the **highest** tier any single signal produces:

1. **File count** — distinct files expected to change: 1 → Small; 2–9 → Medium; 10+ → Large; unestimable → Medium
2. **Change size** — estimated changed lines in total: ≤30 → Small; 31–400 → Medium; >400 → Large; unestimable → Medium
3. **Logic novelty** — none, config/docs/typo/rename level (e.g., changing a config value, fixing wording in docs, renaming without signature changes) → Small; modified or new logic — including a new algorithm — that stays inside existing module boundaries and changes no public interface (e.g., adding an if-branch or a parameter inside an existing function, adjusting an existing query or output format, replacing an internal algorithm) → Medium; architectural change or a modified cross-module contract (e.g., a new module other modules must call, a changed public interface or exported signature, a changed data contract between modules) → Large
4. **Risk keywords (위험 영역)** — any hit forces Large: security/auth (보안·인증·인가), payment/billing (결제·과금), migration or schema change (마이그레이션·스키마 변경), concurrency/locking/threading (동시성·락·스레드), secrets/credentials/API keys (시크릿·자격증명·API 키), destructive operations such as delete/drop/force-push/mass update (삭제·파괴적 작업)

**Tier resolution rule (등급 결정 규칙)**:

- Take the **highest** tier any single signal produces.
- **Small** requires **all four** signals to land in the Small band.
- **Large requires positive evidence** — at least one signal must actually land in the Large band (10+ files, >400 changed lines, an architectural or cross-module contract change, or a risk-keyword hit). An impression that the job "might be big" is not evidence.
- **Ambiguous, conflicting-but-unestimable, or missing signals resolve to Medium**, never to Large. Anything that is neither clearly Small nor positively Large is Medium.
- Signals that straddle a boundary while still being estimable follow the numbers as written (e.g., 9 files → Medium, 10 files → Large; 400 lines → Medium, 401 lines → Large).

**Tier decision timing (판정 시점):**

- **1-d tier** — decided in 1-c item 3, at the moment the user confirms the restatement. Never earlier: 1-a exploration signals alone must not set the tier — the 1-b interview and the restatement can still change scope. Inputs: 1-a analysis, 1-b interview answers, the confirmed sentence.
- **Step 3 tier** — decided at Step 3 item 1 from the approved plan's **Implementation Steps** (target-file count, per-step diff sketches/pseudocode for change size, risk keywords in the steps and Risks sections). Judged independently of the 1-d tier — the two may differ. At Step 3 the tier selects **reasoning effort only**; the model is always Sonnet.
- **Re-spawns** — a Step 2 Comment-loop revision re-runs the checklist with the user feedback applied; the tier may rise but never falls within the same comment loop. The single 1-e revision cycle and Step 3 error-fix re-spawns reuse the already-decided tier.

**Tier announcement (등급 고지)** — print exactly one line immediately before spawning the phase agent, in this form:

`Tier: <Large|Medium|Small> — rationale: <파일 수>, <예상 변경 규모>, <로직/위험 근거> → <model>/<effort>`

Examples:

- 1-d, Small: `Tier: Small — rationale: 단일 파일, 예상 12줄 변경, 문서 전용, 위험 키워드 없음 → Sonnet/standard`
- 1-d, Medium (default): `Tier: Medium — rationale: 3개 파일, 예상 120줄 변경, 기존 모듈 내부 로직 수정, 위험 키워드 없음 → Opus/high`
- Step 3, Medium: `Tier: Medium — rationale: 3개 파일, 예상 120줄 변경, 기존 모듈 내부 로직 수정, 위험 키워드 없음 → Sonnet/high`

**Invariant (불변 조건)**: tiering selects model and reasoning effort **only**. Every tier — including Small — runs the identical workflow: 1-e adversarial preview, the Step 2 user review with its hard gate, Step 3 evidence verification, and Step 4. No tier skips, weakens, or auto-approves any gate. 1-e stays fixed at Sonnet/standard for every tier; Step 3 stays fixed at Sonnet for every tier and varies only in effort; 1-c has no subagent and is not tiered.

**Orthogonality (직교성)**: the tier and the **development direction (개발 방향, 1-b)** are two independent axes and must never be conflated. The tier decides how much model and reasoning effort a subagent gets; the development direction decides how much generality, reuse, and coverage the plan's content demands. The direction never raises or lowers a tier, and the tier never changes the direction's requirements. A 심화 job can be Small, and a Large job can be 단발성 — these two examples are the logical consequence of the two axes being independent, not a new policy or a new exception.

## Step 1: Analyze & Plan

### 1-a. Code Analysis

Explore target files/modules to understand current structure, behavior, and dependencies.

- Use `explore` agent to scan target code — file list, function/class structure, call relationships
- If target code cannot be found, ask user to confirm path/file

### 1-b. Direction & Context Gathering (개발 방향·맥락 수집)

Run in the orchestrator, in this order.

**1. Development direction question (개발 방향 질문) — asked first, before any other 1-b work.**

Ask via `AskUserQuestion` (Codex: plain-text question, end the turn). Exactly one question, three options:

| Option | 뜻 | 전형적 상황 |
| --- | --- | --- |
| **단발성 (one-off)** | 지금 이 문제만 해결하면 되는 일회성 작업 | 임시 스크립트, 1회성 데이터 처리, 재사용 계획 없음 |
| **간단한 (simple)** | 앞으로도 쓰지만 확장 계획은 없는 실용 기능 | 사내 도구의 기능 하나, 반복 사용하는 유틸리티 |
| **심화 (deep)** | 오래 유지·확장할 기반 기능 | 공용 모듈, 여러 곳에서 호출될 인터페이스, 장기 유지보수 대상 |

Record the answer as the **development direction (개발 방향)**. It shapes only the plan's generality and coverage requirements (table below) and is passed to 1-d. It is **not** a tier: it never changes the Model & Effort Tiering result, and it never skips, weakens, or shortens any gate — 1-e adversarial preview, the Step 2 hard gate, and Step 3 evidence verification apply identically to 단발성. If the user declines to choose or gives no answer, default to **간단한 (simple)** and state that assumption in the plan's Requirements Summary.

**Asked once per workflow run.** A 1-c **Missing scope** return to 1-b resumes at item 3 (interview) and reuses the direction already recorded — do not re-ask the direction question. The same holds for Step 2 Comment-loop revisions. The direction changes only when the user explicitly asks to change it; if they do, record the new direction and note the change in the plan's Requirements Summary.

**Generality requirements by direction (개발 방향별 범용성 요구)** — the four axes rise step by step; each level includes everything the level to its left requires. This table is the single definition; 1-d references it rather than restating it.

| 축 (axis) | 단발성 (one-off) | 간단한 (simple) | 심화 (deep) |
| --- | --- | --- | --- |
| **설정 외부화·하드코딩 제거** | 하드코딩 허용. 단, 바뀔 수 있는 값은 파일 상단 상수로 모을 것 | 경로·임계값·모드 등 변하는 값은 상수 또는 함수 인자로 분리 | 설정 파일 또는 환경변수로 외부화하고, 기본값·검증 규칙·설정 누락 시 동작을 명시 |
| **재사용 인터페이스·확장점** | 단일 함수 또는 스크립트로 끝냄. 인터페이스 설계 불필요 | 호출 가능한 함수 단위로 분리하고 시그니처(인자·반환·예외)를 계획에 명시 | 공개 인터페이스와 확장점(주입 지점, 옵션 매개변수, 훅)을 설계하고 하위 호환 규칙을 명시 |
| **경계·예외 입력 처리** | 정상 입력 기준 동작 + 실패 시 원인을 알 수 있는 오류 메시지 | 주요 경계값(빈 값, 최소·최대, 잘못된 형식) 처리와 각각의 기대 동작 명시 | 위 항목 + 비정상·악의적 입력, 부분 실패, 재시도·롤백 정책 명시 |
| **테스트·문서 커버리지** | 실행 예시 1개와 결과 확인 방법 | 핵심 경로 테스트 + 사용법 주석 또는 README 한 문단 | 경계·실패 케이스를 포함한 테스트 세트 + 인터페이스 문서와 사용 예시 |

**2. Context summary.** Run `plan-context` Phase A in the orchestrator to build the context summary:

- Incorporate context from `docs\revision_history.md`, `docs\plan_history.md`, wiki knowledge, and change history — git history when `.git` exists, file-system mtime when `.git` is absent (handled by plan-context Phase A)

**3. Interview.** If requirements are vague, interview the user here per plan-context Interview Mode mechanics — one question at a time, ambiguity ledger (모호성 원장), Refine gate, fact-confirmation routing (see plan-context references/planning-workflow.md, Interview Mode) — the planning agent cannot ask the user anything. The direction question in item 1 is separate from the ambiguity ledger and is asked even when the request is already specific.

### 1-c. Restate Gate (재진술 확인 게이트)

Run in the orchestrator immediately after 1-b, **before** spawning the expensive planning agent. No subagent, no max-reasoning cost — one cheap checkpoint to prevent a wasted max-reasoning plan built on a misunderstanding.

1. Restate the agreed goal as **one sentence** covering target (what/where), the change, and the success criterion. Derive it from the 1-b answers and, when present, the resolved ambiguity-ledger tracks. Test: a third party reading only this sentence should reach the same conclusion about what is being built.
2. Confirm via `AskUserQuestion` (Codex: plain-text question, end the turn). Options:
   - **Yes, proceed to planning** — pass the confirmed sentence to 1-d as the top-line goal statement
   - **Adjust wording** — apply the user's correction and restate again (max 3 cycles; after the 3rd, ask the user to write the sentence verbatim and use it as-is)
   - **Missing scope** — return to the 1-b interview for the missing scope, then restate again
3. **Tier decision (티어 판정, 1-d)** — the moment the user selects **Yes, proceed to planning**, run the Model & Effort Tiering checklist (Agent & Model Policy — defined there once; do not restate it here) against the confirmed scope — inputs: 1-a analysis, 1-b interview answers, the confirmed sentence. The 1-b development direction is **not** an input to this decision. Never decide earlier from 1-a exploration signals alone, and never ask the user an extra tier-confirmation question. Print the Tier announcement line, then proceed to item 4 — 1-d is spawned at this tier with the inputs item 4 describes.
4. The confirmed sentence feeds the planning-agent input and the plan's Requirements Summary. Everything else from 1-b — including the recorded **development direction (개발 방향)** — is passed to 1-d in full multi-section form; the restatement is the only place where one-line compression is the goal.

Confirming the restatement authorizes **plan authoring (1-d) only**. It is not approval to implement — the Step 2 hard gate is unchanged.

### 1-d. Plan Authoring (dedicated planning agent)

Spawn the planning agent per the Agent & Model Policy. Do **not** author the plan in the orchestrator context.

Agent input — include all of:

- User requirements and interview answers from 1-b
- The confirmed goal restatement from 1-c (top-line goal statement)
- 1-a analysis results (files, structures, call relationships)
- 1-b context summary (revision/plan history, wiki knowledge, similar past plans)
- The **development direction (개발 방향)** recorded in 1-b (단발성 / 간단한 / 심화) and the matching column of the Generality requirements table in 1-b
- The Required Plan Sections below and plan-context quality criteria (`plan-context/references/planning-workflow.md`, Quality Criteria)

Agent mission: using maximum reasoning, produce an **implementation-ready plan so detailed that the executor makes no design decisions of its own** — only follows directives and verifies against the stated conditions.

**Required Plan Sections** (supersets plan-context's standard output format):

1. **Requirements Summary**
2. **Acceptance Criteria** — testable, 90%+ concrete, including before/after comparison criteria against current behavior/metrics (capture the pre-change baseline)
3. **Implementation Steps (구현 지침)** — per step: target file/function references, exact change specification, interfaces/signatures, data structures, algorithm outline, error handling, edge cases. Include pseudocode or an expected-diff sketch for any non-trivial change. State the configuration-externalization and reuse-interface/extension-point decisions at the level the development direction requires (1-b, Generality requirements table).
4. **Code Writing Guide (코드 작성 가이드)** — project conventions to follow, patterns to use and to avoid, naming rules, encoding rules (UTF-8 for Korean text), dependency/library constraints
5. **Definition of Done (개발 완료조건)** — binary-checkable conditions only; performance targets quantified ("fast" → "p99 < 200ms"). Include the development direction's boundary/exception-handling and test/documentation coverage requirements as binary items.
6. **Adversarial Test Environment (적대적 테스트 환경)** — how to set up and run tests designed to break the implementation: boundary values, malformed/hostile inputs, failure injection, concurrency/scale cases where relevant, plus expected results. Depth of the boundary and failure cases follows the development direction (1-b table), but the section itself is mandatory at every direction. Every Definition of Done item maps to at least one test.
7. **Risks and Mitigations**
8. **Verification Steps**

**Generality scaling (범용성 요구 반영)** — the development direction from 1-b sets *how demanding* sections 3 through 6 are along the four axes (설정 외부화, 재사용 인터페이스·확장점, 경계·예외 처리, 테스트·문서 커버리지). It never changes *which* sections exist: all 8 sections are mandatory for every direction, including 단발성. A plan that omits a section because "the job is one-off" fails the 1-e structure check.

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

1. **Tier decision (티어 판정, Step 3)** — before any status change, run the Model & Effort Tiering checklist (Agent & Model Policy — defined there once; do not restate it here) against the approved plan's **Implementation Steps**: count distinct target files, estimate total change size from each step's expected-diff sketch/pseudocode, and scan the Implementation Steps and Risks sections for risk keywords. Orchestrator-only, no subagent, no extra user question. Here the tier selects **reasoning effort only** — the executor model is always Sonnet. Print the Tier announcement line (with `Sonnet` as the model) before proceeding. This tier is judged independently of the 1-d tier — the two may differ.
2. Update plan status to `In Progress` in `docs\plan_history.md`
3. If the native `/goal` feature is available, register the plan's Definition of Done items as the active goals for the session
4. Spawn the executor agent per the Agent & Model Policy (model fixed: Sonnet; reasoning effort per the tier decided in item 1 — Large `max`, Medium `high`, Small standard). Executor rules:
   - **Goal contract first**: before writing any code, read the plan document and extract the **Definition of Done** and **Adversarial Test Environment** sections. Adopt them as the goal. Meeting every completion condition and passing the adversarial tests is the top priority — above speed and token cost.
   - Implement strictly following the **Implementation Steps** and **Code Writing Guide**. Do not re-litigate design decisions already made in the plan; if a directive is impossible as written, stop and report instead of improvising.
   - **Goal-seeking loop**: implement → build and run the adversarial tests → analyze failures → fix → re-run. Repeat until all Definition of Done items pass. If not converging (e.g., the same test still fails after 5 fix attempts) or genuinely blocked, stop and report the gap with evidence — never ship a partial result as done.
   - Return to the orchestrator: changed-file list, test-run evidence (commands + output), and a Definition of Done checklist with per-item pass/fail.
5. Parallelization: if the Implementation Steps contain independent groups with no file overlap, the orchestrator may spawn one executor agent per group in parallel — every group uses the single tier decided in item 1 (the tier is judged once per Step 3 from the whole plan, never per group); otherwise use a single executor agent.
6. The orchestrator verifies the returned evidence against the plan before Step 4. An executor "done" claim without a fully green Definition of Done checklist is not done.
7. On error: report to user, confirm whether to fix or abort.

## Step 4: Review & Commit

1. Invoke `/revision-tracker` skill — create revision entry, run code quality check, propose git commit
2. Confirm every Definition of Done item is verified with Step 3 evidence, then update plan status to `Completed` in `docs\plan_history.md`

## Exceptions

| Situation | Handling |
| --- | --- |
| Target code not found | Ask user for correct path/file |
| Error during Step 3 | Report error, confirm fix or abort |
| Executor cannot meet a Definition of Done item | Report the gap with evidence; ask user: revise plan / accept as partial / abort |
| Environment lacks subagent model/effort control | Apply the fallback in Agent & Model Policy (separate pass in current context; without per-pass effort control, always run at maximum reasoning regardless of tier) |
| Tier signals ambiguous or unestimable | Resolve to **Medium** (the default). Large requires at least one signal positively in the Large band; conflicting but estimable signals take the highest tier they produce. Never ask the user an extra tier-confirmation question |
| User declines or cannot choose a development direction | Default to **간단한 (simple)**, state the assumption in the plan's Requirements Summary, and continue. Never block the workflow on this question |
| Code quality issues in Step 4 | Apply simplify fixes, re-propose commit |
| User requests abort mid-workflow | Record current state in plan_history, end skill |
| Restate gate not converging after 3 cycles | Ask the user to write the one-sentence goal verbatim; use it as-is |
| HIGH findings remain after the single 1-e revision cycle | Do not loop again; surface them unresolved in Step 2 Reviewer notes — the user decides |
| Environment lacks parallel subagents for 1-e | Run the two lanes sequentially (Agent & Model Policy fallback) |
