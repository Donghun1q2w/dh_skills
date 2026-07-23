# Planning Workflow Details

Detailed procedures for each planning mode. All plan files save to `docs\plans\`.

## Table of Contents

- [Invocation Contexts](#invocation-contexts)
- [Interview Mode](#interview-mode)
- [Direct Mode](#direct-mode)
- [Consensus Mode](#consensus-mode)
- [Review Mode](#review-mode)
- [Quality Criteria](#quality-criteria)
- [Tool Usage](#tool-usage)

---

## Invocation Contexts

When `plan-context` is called by `dh-dev`:

- Run **Phase A only** (context gathering) and return the Context Summary to the orchestrator. Do **not** proceed to Phase A-2 — plan authoring is done by dh-dev's dedicated planning agent (model/effort per dh-dev's Model & Effort Tiering; Large default: Fable 5, max reasoning effort), not by this workflow. The Phase A-2 modes below (Interview/Direct/Consensus/Review) are never entered from dh-dev.
- Phase B is invoked afterward by the orchestrator solely for file naming, directory creation, and `docs\plan_history.md` indexing of the agent-authored plan. Preserve the plan body's sections verbatim (dh-dev Required Plan Sections) — do not restructure it into the Plan Document Template body.
- All user feedback and approval happen exclusively in `dh-dev` Step 2 — never inside this workflow. Do not auto-proceed to implementation even if the request is detailed, uses `--direct`, or includes "go ahead" language.
- Exception to the above: when dh-dev runs its 1-b interview in the orchestrator, the Interview Mode **mechanics** below do apply — ambiguity ledger, Refine gate, fact-confirmation routing, one question at a time. What is never entered from dh-dev is Interview Mode plan authoring (steps 7-8): the plan is always authored by dh-dev's dedicated planning agent.

Approval tooling is environment-specific:

- Use `AskUserQuestion` when it is available.
- In Codex, if no clickable approval tool is available, ask for plain-text approval and stop.

---

## Interview Mode

Triggered by broad/vague requests (vague verbs, no specific files, touches 3+ areas).

1. **Classify the request**: Broad triggers interview mode
2. **Initialize the ambiguity ledger (모호성 원장)**: open the five tracks (see Ambiguity Ledger below) and show the initial snapshot
3. **Ask one focused question** via `AskUserQuestion` for preferences, scope, constraints — target the most-stale `Open` track unless the user steers elsewhere
4. **Gather codebase facts first**: Spawn `explore` agent to find patterns/implementations before asking the user, then route the result via Fact-Confirmation Routing (below)
5. **Build on answers**: Each question builds on the previous answer; reasoning-bearing free-form answers pass the Refine Gate (below) before being committed to the ledger
6. **Consult Analyst** (Opus) for hidden requirements, edge cases, risks
7. **Create plan** when user signals readiness ("create the plan", "I'm ready") — if any ledger track is still `Open`, list the open tracks and ask one confirmation question before proceeding
8. Save plan to `docs\plans\YYYY-MM-DD_HHMMSS_<slug>.md`

### Question Classification

| Type | Examples | Action |
| --- | --- | --- |
| Codebase Fact | "What patterns exist?", "Where is X?" | Explore first, then route via Fact-Confirmation Routing (below) — never ask the user blind |
| User Preference | "Priority?", "Timeline?" | Ask user via AskUserQuestion |
| Scope Decision | "Include feature Y?" | Ask user |
| Requirement | "Performance constraints?" | Ask user |

### Ambiguity Ledger (모호성 원장)

Interview Mode only. The ledger is conversation-context state — no file, no server. It exists to keep the interview from collapsing into a single subtopic.

- **Tracks (fixed five)**: Scope (범위), Constraints (제약), Success Criteria (성공 기준), Non-goals (제외 범위), Verification (검증 방법)
- **Status per track**: `Open` → `Partially resolved` → `Resolved`. The user may also waive a track ("not applicable", "decide for me") — record it as `Waived` with the user's wording.
- **Display cadence**: show the compact snapshot (canonical format: `templates.md`, Interview Mode Templates) after each processed answer, and always before the readiness confirmation in step 7.
- **Anti-fixation rule**: if a track has stayed `Open` and untouched for 3 consecutive questions while another track is being drilled, the next question must target the most-stale `Open` track — unless the user explicitly steered the current thread.
- **Commit rule**: content enters the ledger only from short factual answers, or through a confirmed Refine Gate payload — never from unconfirmed paraphrase.
- Confirmed payloads are stored and later passed to plan authoring **in full multi-section form** — the snapshot is a display index, never a replacement summary.

### Refine Gate (자유서술 구조화 게이트)

Interview Mode only. When a user answer carries reasoning, constraints, or scope decisions (heuristic: multi-sentence, a decision plus its justification, or named trade-offs), do not pass it on raw and do not compress it to one line. Structure it, confirm it, then commit it.

1. Build the structured payload (canonical format: `templates.md`, Interview Mode Templates): Decision / Reasoning / Constraints (user-stated) / Out of scope (user-stated) / Codebase context (orchestrator-verified). The last field may contain only facts the orchestrator actually verified this session — never inferred ones.
2. Ask exactly one confirmation via `AskUserQuestion` with 4 options: **Confirm as structured** / **Add to Constraints** / **Add to Out of scope** / **Rewrite**. Free-text replies may add anything else (extra context, corrections) — treat them as `Rewrite` input. "Add to ..." re-presents the amended payload for one more confirmation.
3. Commit to the ledger only after confirmation.

**Skip condition**: short factual answers — a single proper noun, a yes/no, no reasoning — skip the gate and commit directly.

### Fact-Confirmation Routing (신뢰도 기반 사실확인 라우팅)

Interview Mode only. Route every explored codebase fact through one of three paths. Maintain a **non-user-answer counter** in conversation context (starts at 0).

**PATH 1a — Auto-adopt (자동 채택)** — when ALL of the following hold:

- an exact answer was found in a manifest/config/lockfile-class source (e.g., `pyproject.toml`, `package.json`, `*.csproj`, `.mcp.json`)
- it is purely descriptive of current state — not a decision about what new behavior should do
- it is unambiguous — a single clear answer, not multiple candidates

Then adopt immediately, show a one-line non-blocking notice — `Auto-confirmed: Python 3.12, FastAPI (pyproject.toml)` — and increment the counter. Never block on the user for PATH 1a facts.

**PATH 1b — Evidence confirmation (근거 확인)** — medium/low confidence: pattern inference, multiple candidates, or a manifest inconsistency. Show the evidence with file references and ask one question: **Yes, correct** / **No, let me correct**. A bare "Yes, correct" increments the counter (a rubber-stamp is not a substantive answer). A correction resets the counter to 0.

**PATH 2 — Direct user question**: preferences, scope, requirements per Question Classification — a normal `AskUserQuestion`. Any substantive user answer resets the counter to 0.

**Dialectic Rhythm Guard (문답 리듬 가드)**: when the counter reaches 3, the next question MUST be a PATH 2 direct user question, targeting the most-stale `Open` ledger track. Reset the counter after the user answers. This keeps the interview a dialogue with the user, not a monologue against the codebase.

### Design Option Presentation

Chunk options — never present all at once:

1. **Overview** (2-3 sentences)
2. **Option A** with trade-offs → wait for reaction
3. **Option B** with trade-offs → wait for reaction
4. **Recommendation** (only after options discussed)

---

## Direct Mode

Triggered by `--direct` or detailed requests with clear scope.

1. **Quick Analysis**: Optional brief Analyst consultation
2. **Create plan**: Generate comprehensive work plan immediately
3. Save plan to `docs\plans\YYYY-MM-DD_HHMMSS_<slug>.md`
4. **Review** (optional): Critic review if requested

---

## Consensus Mode

Triggered by `--consensus` or "ralplan". Uses RALPLAN-DR structured deliberation.

**Modes**: Short (default, bounded) and Deliberate (`--deliberate` or high-risk: auth/security, data migration, destructive changes, production incidents, compliance/PII, public API breakage).

### Steps

1. **Planner** creates initial plan with **RALPLAN-DR summary**:

   - Principles (3-5)
   - Decision Drivers (top 3)
   - Viable Options (&gt;=2) with bounded pros/cons
   - If only one viable option, explicit invalidation rationale for rejected alternatives
   - Deliberate mode adds: pre-mortem (3 failure scenarios) + expanded test plan (unit/integration/e2e/observability)

2. **User feedback** *(--interactive only)*: Present draft plan + RALPLAN-DR summary via `AskUserQuestion` when available, otherwise plain text:

   - Proceed to review
   - Request changes (return to step 1)
   - Skip review (go to step 7)

   Without `--interactive`, auto-proceed to step 3.

3. **Architect** reviews via `Task(subagent_type="oh-my-claudecode:architect", ...)`:

   - Strongest steelman counterargument (antithesis) against favored option
   - At least one meaningful tradeoff tension
   - Synthesis path when possible
   - Deliberate mode: explicitly flag principle violations **Wait for completion before step 4. Steps 3 and 4 must be sequential, never parallel.**

4. **Critic** evaluates via `Task(subagent_type="oh-my-claudecode:critic", ...)`:

   - Verify principle-option consistency, fair alternative exploration, risk mitigation clarity
   - Verify testable acceptance criteria and concrete verification steps
   - Reject shallow alternatives, driver contradictions, vague risks, weak verification
   - Deliberate mode: reject missing/weak pre-mortem or expanded test plan

5. **Re-review loop** (max 5 iterations): If Critic rejects: a. Collect rejection feedback from Architect + Critic b. Planner produces revised plan c. Return to step 3 (Architect review) d. Return to step 4 (Critic evaluation) e. If max iterations reached, present best version to user

6. **Apply improvements**: Merge accepted improvements into plan. Final output **MUST** include ADR:

   - Decision, Drivers, Alternatives considered, Why chosen, Consequences, Follow-ups

7. **Final approval** *(--interactive only)*: Present plan via `AskUserQuestion` when available, otherwise plain text:

   - Approve and implement
   - Request changes (return to step 1)
   - Reject

   Without `--interactive`, output final plan and stop.

8. Save approved plan to `docs\plans\YYYY-MM-DD_HHMMSS_<slug>.md`

---

## Review Mode

Triggered by `--review` or "review this plan".

1. Read plan file from `docs\plans\`
2. Evaluate via Critic using `Task(subagent_type="oh-my-claudecode:critic", ...)`
3. Return verdict: APPROVED, REVISE (with specific feedback), or REJECT (replanning required)

---

## Quality Criteria

| Criterion | Standard |
| --- | --- |
| Clarity | 80%+ claims cite file/line |
| Testability | 90%+ criteria are concrete |
| Verification | All file refs exist |
| Specificity | No vague terms without metrics ("fast" -&gt; "p99 &lt; 200ms") |

### Final Checklist

- [ ] Plan has testable acceptance criteria (90%+ concrete)

- [ ] Plan references specific files/lines where applicable (80%+ claims)

- [ ] All risks have mitigations identified

- [ ] No vague terms without metrics

- [ ] Plan saved to `docs\plans\`

- [ ] Interview mode: every ledger track `Resolved` or `Waived` before plan creation

- [ ] Consensus mode: RALPLAN-DR summary + ADR section included

- [ ] Deliberate mode: pre-mortem + expanded test plan included

---

## Tool Usage

- `AskUserQuestion` for preference questions (scope, priority, timeline) when available — provides clickable UI
- Plain-text approval prompts in Codex when `AskUserQuestion` is unavailable
- Plain text for questions needing specific values (port numbers, names)
- Refine gate confirmations and PATH 1b fact confirmations use `AskUserQuestion` when available; in Codex, plain-text with the same options
- `explore` agent (Haiku, 30s timeout) to gather codebase facts before asking user
- `Task(subagent_type="oh-my-claudecode:architect", ...)` for architectural review in consensus mode
- `Task(subagent_type="oh-my-claudecode:critic", ...)` for plan evaluation in consensus/review modes
- `Task(subagent_type="oh-my-claudecode:analyst", ...)` for requirements analysis
- **Consensus mode agent calls MUST be sequential (Architect then Critic), never parallel**
