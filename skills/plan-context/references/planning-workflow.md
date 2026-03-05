# Planning Workflow Details

Detailed procedures for each planning mode. All plan files save to `docs\plans\`.

## Table of Contents

- [Interview Mode](#interview-mode)
- [Direct Mode](#direct-mode)
- [Consensus Mode](#consensus-mode)
- [Review Mode](#review-mode)
- [Quality Criteria](#quality-criteria)
- [Tool Usage](#tool-usage)

---

## Interview Mode

Triggered by broad/vague requests (vague verbs, no specific files, touches 3+ areas).

1. **Classify the request**: Broad triggers interview mode
2. **Ask one focused question** via `AskUserQuestion` for preferences, scope, constraints
3. **Gather codebase facts first**: Spawn `explore` agent to find patterns/implementations before asking the user
4. **Build on answers**: Each question builds on the previous answer
5. **Consult Analyst** (Opus) for hidden requirements, edge cases, risks
6. **Create plan** when user signals readiness: "create the plan", "I'm ready"
7. Save plan to `docs\plans\YYYY-MM-DD_HHMMSS_<slug>.md`

### Question Classification

| Type | Examples | Action |
|------|----------|--------|
| Codebase Fact | "What patterns exist?", "Where is X?" | Explore first, do not ask user |
| User Preference | "Priority?", "Timeline?" | Ask user via AskUserQuestion |
| Scope Decision | "Include feature Y?" | Ask user |
| Requirement | "Performance constraints?" | Ask user |

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
   - Viable Options (>=2) with bounded pros/cons
   - If only one viable option, explicit invalidation rationale for rejected alternatives
   - Deliberate mode adds: pre-mortem (3 failure scenarios) + expanded test plan (unit/integration/e2e/observability)

2. **User feedback** *(--interactive only)*: Present draft plan + RALPLAN-DR summary via `AskUserQuestion`:
   - Proceed to review
   - Request changes (return to step 1)
   - Skip review (go to step 7)
   Without `--interactive`, auto-proceed to step 3.

3. **Architect** reviews via `Task(subagent_type="oh-my-claudecode:architect", ...)`:
   - Strongest steelman counterargument (antithesis) against favored option
   - At least one meaningful tradeoff tension
   - Synthesis path when possible
   - Deliberate mode: explicitly flag principle violations
   **Wait for completion before step 4. Steps 3 and 4 must be sequential, never parallel.**

4. **Critic** evaluates via `Task(subagent_type="oh-my-claudecode:critic", ...)`:
   - Verify principle-option consistency, fair alternative exploration, risk mitigation clarity
   - Verify testable acceptance criteria and concrete verification steps
   - Reject shallow alternatives, driver contradictions, vague risks, weak verification
   - Deliberate mode: reject missing/weak pre-mortem or expanded test plan

5. **Re-review loop** (max 5 iterations): If Critic rejects:
   a. Collect rejection feedback from Architect + Critic
   b. Planner produces revised plan
   c. Return to step 3 (Architect review)
   d. Return to step 4 (Critic evaluation)
   e. If max iterations reached, present best version to user

6. **Apply improvements**: Merge accepted improvements into plan. Final output **MUST** include ADR:
   - Decision, Drivers, Alternatives considered, Why chosen, Consequences, Follow-ups

7. **Final approval** *(--interactive only)*: Present plan via `AskUserQuestion`:
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
|-----------|----------|
| Clarity | 80%+ claims cite file/line |
| Testability | 90%+ criteria are concrete |
| Verification | All file refs exist |
| Specificity | No vague terms without metrics ("fast" -> "p99 < 200ms") |

### Final Checklist

- [ ] Plan has testable acceptance criteria (90%+ concrete)
- [ ] Plan references specific files/lines where applicable (80%+ claims)
- [ ] All risks have mitigations identified
- [ ] No vague terms without metrics
- [ ] Plan saved to `docs\plans\`
- [ ] Consensus mode: RALPLAN-DR summary + ADR section included
- [ ] Deliberate mode: pre-mortem + expanded test plan included

---

## Tool Usage

- `AskUserQuestion` for preference questions (scope, priority, timeline) — provides clickable UI
- Plain text for questions needing specific values (port numbers, names)
- `explore` agent (Haiku, 30s timeout) to gather codebase facts before asking user
- `Task(subagent_type="oh-my-claudecode:architect", ...)` for architectural review in consensus mode
- `Task(subagent_type="oh-my-claudecode:critic", ...)` for plan evaluation in consensus/review modes
- `Task(subagent_type="oh-my-claudecode:analyst", ...)` for requirements analysis
- **Consensus mode agent calls MUST be sequential (Architect then Critic), never parallel**
