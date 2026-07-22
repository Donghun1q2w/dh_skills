# dh-dev/plan-context 플래닝 단계 개선 — ouroboros interview 패턴 이식

- **Date**: 2026-07-22 21:17:02
- **Status**: Completed

---

## 1. Requirements Summary

ouroboros `interview` 스킬(MCP 서버 기반 Socratic 인터뷰)에서 관찰된 4개 상호작용 패턴을, MCP 서버 없이 **대화 컨텍스트만을 상태 저장소로 사용하는** 이 저장소의 스킬/서브에이전트 아키텍처에 맞게 이식한다. 대상은 실행 코드가 아니라 스킬 정의 마크다운 문서 4개다.

| # | 개선안 | 대상 파일 |
| --- | --- | --- |
| 1 | 계획 초안 적대적 프리뷰 패널 (contrarian + gap_hunter 병렬 레인) | `skills\dh-dev\SKILL.md` |
| 2 | 경량 Restate 확인 게이트 (1-b 직후, 고비용 플래닝 에이전트 호출 전) | `skills\dh-dev\SKILL.md` |
| 3 | 모호성 원장 + Refine 게이트 (Interview Mode 한정) | `skills\plan-context\SKILL.md`, `references\planning-workflow.md`, `references\templates.md` |
| 4 | 신뢰도 기반 사실확인 라우팅 + Dialectic Rhythm Guard (Interview Mode 한정) | `skills\plan-context\SKILL.md`, `references\planning-workflow.md` |

**절대 제약**: MCP 서버 신설 금지. 2026-06-26 개정에서 확립된 Step 2 hard gate(승인 전 실행 금지)를 약화시키지 않고 강화. 개선 3·4는 Interview Mode에만 적용하며 Direct/Consensus/Review 모드 섹션은 무변경.

### Key Design Decisions (설계 결정과 근거)

| # | 결정 | 근거 |
| --- | --- | --- |
| D-1 | **적대적 패널은 2-레인(contrarian, gap_hunter) + 오케스트레이터 로컬 구조 검사(게이트)로 설계. closer 서브에이전트 레인은 두지 않음** | ouroboros의 closer는 MCP가 관리하는 인터뷰 완결성 기준을 적용하는 레인이었으나 우리에겐 그 상태 저장소가 없다. 우리의 정준 기준(Required Plan Sections 8개 존재 여부, DoD 이진 판정 가능 여부, DoD↔테스트 매핑)은 전부 기계적으로 검사 가능하므로 서브에이전트가 아니라 오케스트레이터의 결정론적 체크리스트가 더 싸고 더 신뢰성 있다. 이 구조 검사가 ouroboros closer의 "게이트" 역할을 그대로 승계한다(구조 검사 실패 = HIGH 발견으로 취급). 레인을 2개로 줄여 비용/지연도 절반. |
| D-2 | **1-b/1-c 사이 삽입은 전면 재번호 방식(1-c=Restate, 1-d=Plan Authoring, 1-e=Adversarial Preview)** | "1-b2" 같은 인터스티셜 번호는 저장소 관행에 없고 가독성이 나쁘다. `Step 1-c` 문자열의 저장소 전체 참조가 `skills\dh-dev\SKILL.md` 내부 3곳(23, 80, 91행)뿐임을 grep으로 확인했으므로 재번호 파급 범위가 완전히 통제된다(과거 계획/개정 이력 문서는 역사 기록이라 무변경). |
| D-3 | **패널은 신규 초안당 1회만 실행, HIGH 발견 시 1-d 재작성도 1회만, 재작성 후에는 레인 재스폰 없이 구조 검사만 재실행** | 미션 요구("1회 되돌려 보완 후 Step 2로 진행")에 부합하고 무한 루프를 원천 차단. Step 2 Comment 루프의 수정본은 사용자가 매 반복 직접 검토하므로 패널 재실행은 이중 게이트 + 토큰 낭비다. 미해소 HIGH는 숨기지 않고 Step 2 "Reviewer notes"로 사용자에게 그대로 노출해 사용자가 결정한다 — hard gate 강화 방향. |
| D-4 | **패널 레인 모델은 Sonnet, 통상 effort** | 레인은 완성된 초안에 대한 비평이지 저작이 아니다. max-reasoning 예산은 1-d(Fable 5)와 Step 3(Opus 4.8)에 예약하는 기존 정책과 "lightest-weight path" 원칙에 부합. |
| D-5 | **Restate 게이트는 항상 실행(스킵 조건 없음), 오케스트레이터 단독, 서브에이전트 없음** | 비용이 질문 1개인 반면, 오해 비용은 max-reasoning 플랜 전체다. 스킵 휴리스틱을 두면 그 판단 자체가 새 모호성이 된다. 재진술 불수렴 시 3회 후 사용자가 문장을 직접 작성하는 탈출구를 명시. |
| D-6 | **Restate 확인은 "플랜 저작 승인"일 뿐 "구현 승인"이 아님을 문서에 명문화** | 2026-06-26 hard gate와의 충돌 가능성을 문장 단위로 차단. |
| D-7 | **dh-dev 1-b 인터뷰에도 개선 3·4의 Interview Mode 메커니즘(원장/Refine/라우팅)이 적용됨을 양쪽 문서에 명시** | dh-dev 1-b는 이미 "per plan-context rules"로 인터뷰를 위임하고 있다. 단, planning-workflow.md의 Invocation Contexts에 "Phase A-2 모드는 dh-dev에서 진입하지 않는다"는 기존 규칙이 있으므로, "메커니즘은 적용되나 Interview Mode의 플랜 저작 단계(7-8)는 dh-dev에서 절대 실행되지 않는다"는 예외 문구를 추가해 모순을 제거한다. |
| D-8 | **dh-dev에 references/ 디렉토리를 신설하지 않음** | 변경 후 예상 라인 수: dh-dev/SKILL.md 약 180행(현재 121행), planning-workflow.md 약 255행(현재 177행), plan-context/SKILL.md 약 272행(현재 268행), templates.md 약 175행(현재 142행) — 전부 500행 기준의 절반 안팎이라 progressive disclosure 분리가 불필요하며, 신설 시 README 트리 갱신 부담만 늘어난다. |
| D-9 | **Refine 게이트 옵션은 4개(Confirm / Add to Constraints / Add to Out of scope / Rewrite)** | `AskUserQuestion`은 선택지 4개 제한이 있다. ouroboros의 5번째 옵션 "Add context"는 자유서술 응답(Other)으로 흡수하고, 자유서술은 Rewrite 입력으로 취급한다고 명시. |
| D-10 | **카운터 의미론: PATH 1a 자동채택과 PATH 1b의 단순 "Yes, correct" 클릭은 카운터 증가, 실질적 사용자 답변(정정 제공, PATH 2 답변)만 0으로 리셋** | ouroboros 원형의 "비-사용자 답변(자동채택/추론확인)" 정의를 그대로 승계하되 rubber-stamp와 실질 답변의 경계를 이진 판정 가능하게 명문화. |
| D-11 | **비차단 통보에 이모지(ℹ️) 미사용, `Auto-confirmed:` 평문 접두어 사용** | 사용자 전역 지침(이모지 회피)과 Windows 한글 환경 인코딩 안전성. "§" 문자도 전체 산출물에서 금지. |
| D-12 | **원장 상태값에 `Waived` 추가(Open/Partially resolved/Resolved/Waived)** | 사용자가 "알아서 해줘/해당 없음"으로 트랙을 명시적으로 포기하는 경우를 이진 판정 가능하게 기록하기 위함. |

---

## 2. Acceptance Criteria

**변경 전 기준선 (2026-07-22 실측, grep/Read로 검증 완료)**:

| ID | 기준선 항목 | 실측값 |
| --- | --- | --- |
| B-1 | `skills\dh-dev\SKILL.md` 총 라인 수 | 121행 |
| B-2 | `skills\plan-context\SKILL.md` 총 라인 수 | 268행 |
| B-3 | `skills\plan-context\references\planning-workflow.md` 총 라인 수 | 177행 |
| B-4 | `skills\plan-context\references\templates.md` 총 라인 수 | 142행 |
| B-5 | `skills\` 전체에서 `Restate\|contrarian\|gap_hunter\|ledger\|원장\|Auto-confirm\|Rhythm` grep 히트 | 0건 |
| B-6 | 저장소 전체 `*.md`에서 `Step 1-c` 히트 | 3건, 전부 `skills\dh-dev\SKILL.md`(23, 80, 91행) |
| B-7 | dh-dev SKILL.md 하위단계 헤딩 | `### 1-a.`(32행), `### 1-b.`(39행), `### 1-c. Plan Authoring`(46행)만 존재; `1-d`/`1-e` 없음 |
| B-8 | planning-workflow.md Interview Mode 절차 | 번호 목록 7단계(36–42행), 하위섹션은 Question Classification·Design Option Presentation 2개뿐 |
| B-9 | dh-dev Step 2 hard gate 문단 | 82–89행에 존재 |
| B-10 | dh-dev `references\` 디렉토리 | 존재하지 않음 (`Test-Path` False) |

**변경 후 수용 기준** (각각 이진 판정):

- **AC-1**: `skills\dh-dev\SKILL.md`에 `### 1-c. Restate Gate (재진술 확인 게이트)` 헤딩이 `### 1-b.` 헤딩과 `### 1-d.` 헤딩 사이에 존재하고, 본문에 "Yes, proceed to planning" / "Adjust wording" / "Missing scope" 3개 옵션과 "3 cycles" 탈출 규칙, "not implementation approval" 취지 문장이 포함된다.
- **AC-2**: 동일 파일에 `### 1-e. Adversarial Plan Preview (계획 초안 적대적 검증)` 헤딩이 `### 1-d.`와 `## Step 2` 사이에 존재하고, 본문에 `contrarian`·`gap_hunter` 두 레인 명칭, `HIGH/MEDIUM/LOW` 심각도, "once"(1회 재작성) 규칙, 구조 검사(게이트) 절차, "The panel never approves the plan" 취지 문장이 포함된다.
- **AC-3**: Agent & Model Policy 표에 `Step 1-d Plan Authoring` 행과 `Step 1-e` 신규 행이 존재하고, `Step 1-c Plan Authoring` 문자열은 저장소 전체 `*.md`에서 0건이다 (기준선 B-6 대비: 3건 → 0건).
- **AC-4**: dh-dev Step 2의 hard gate 문단(현재 82–89행)은 문자 그대로 무변경이며, Step 2 첫 문단에만 Reviewer notes 제시 문구가 추가된다. Comment 루프의 `Step 1-c` 참조 2건은 `Step 1-d`로 치환된다.
- **AC-5**: `skills\plan-context\SKILL.md` Core Rules에 `Interview Mode only:`로 시작하는 불릿이 정확히 2개 추가되고, Phase A-2 모드 표의 Interview 행 Behavior만 수정되며, 그 외 기존 불릿/행/섹션은 무변경이다.
- **AC-6**: planning-workflow.md Interview Mode 섹션에 `### Ambiguity Ledger (모호성 원장)`, `### Refine Gate (자유서술 구조화 게이트)`, `### Fact-Confirmation Routing (신뢰도 기반 사실확인 라우팅)` 3개 하위섹션이 존재하고, 번호 절차가 8단계로 확장된다 (기준선 B-8 대비: 7 → 8단계).
- **AC-7**: Question Classification 표의 Codebase Fact 행 Action이 Fact-Confirmation Routing을 참조한다.
- **AC-8**: Direct Mode(64–72행), Consensus Mode(75–128행), Review Mode(131–138행) 섹션은 git diff 기준 무변경 hunk이다.
- **AC-9**: templates.md에 `## Interview Mode Templates (인터뷰 모드 템플릿)` 섹션(원장 스냅샷 표 + Refine 페이로드 형식)이 Plan History Template과 Status Values 사이에 추가되고, 기존 섹션은 무변경이다.
- **AC-10**: planning-workflow.md Invocation Contexts에 dh-dev 1-b 인터뷰가 Interview Mode 메커니즘을 사용하되 플랜 저작 단계(7–8)는 진입하지 않는다는 예외 불릿이 존재한다.
- **AC-11**: 변경된 4개 파일 모두 총 라인 수 500행 미만이다 (기준선 B-1~B-4 대비 증가량이 각각 +100행 이내).
- **AC-12**: 신규 파일 생성 0건, README.md 무변경, `ℹ️` 등 이모지·`§` 문자 신규 유입 0건, 한글 read-back 시 mojibake(`U+FFFD`, `占쏙옙`, `ï»¿`) 0건.

---

## 3. Implementation Steps (구현 지침)

> 실행자 지침: 아래 편집은 **문자열 앵커 기준**으로 적용한다(라인 번호는 2026-07-22 실측 참고치 — 선행 편집으로 밀릴 수 있으므로 Edit 도구의 exact-match를 신뢰 원천으로 사용). 파일당 위에서 아래 순서로 적용. 모든 신규 텍스트는 아래 명세를 **그대로(verbatim)** 사용하고 재설계하지 않는다.

### 파일 1: `D:\001_Work\2026\017_claude\plugins\dh_skills\skills\dh-dev\SKILL.md` (편집 D1–D13)

**D1. frontmatter description 갱신 (3행)** — 다음 부분 문자열을 치환:

- old: `Chains explore (code analysis) → plan authoring by a dedicated max-reasoning planning agent (Fable 5, max reasoning effort — detailed implementation steps, Definition of Done, adversarial test environment) → user review (approve/reject/comment loop)`
- new: `Chains explore (code analysis) → context gathering with a one-sentence restate confirmation gate → plan authoring by a dedicated max-reasoning planning agent (Fable 5, max reasoning effort — detailed implementation steps, Definition of Done, adversarial test environment) → adversarial plan preview (parallel contrarian/gap-hunter review lanes) → user review (approve/reject/comment loop)`

**D2. 다이어그램 확장 (9–13행 코드블록)** — 기존 3줄 다이어그램 아래, 같은 코드블록 안에 빈 줄 1개 + 다음 2줄 추가:

```
Step 1 detail:
1-a Analyze → 1-b Context/Interview → 1-c Restate ✓ → 1-d Plan (agent) → 1-e Adversarial Preview
```

**D3. Agent & Model Policy 도입문 (19행)** — 치환:

- old: `Plan authoring and execution each run in a **dedicated subagent** — never in the orchestrator context.`
- new: `Plan authoring, the adversarial preview lanes, and execution each run in **dedicated subagents** — never in the orchestrator context.`

**D4. 정책 표 갱신 (21–24행)** — `| Step 1-c Plan Authoring |` → `| Step 1-d Plan Authoring |`로 치환하고, 그 행 바로 아래에 신규 행 추가:

```markdown
| Step 1-e Adversarial Preview | 2 parallel review lanes: `contrarian`, `gap_hunter` | Sonnet (`sonnet`); fallback: default model | standard — lanes critique a finished draft, they do not author; max effort is reserved for 1-d and Step 3 |
```

**D5. Codex 폴백 불릿 (27행)** — 문장 끝에 추가:

- old: `All other rules (inputs, required outputs, goal contract) still apply.`
- new: `All other rules (inputs, required outputs, goal contract) still apply. For Step 1-e, run the two lanes as two sequential single-purpose passes and synthesize afterward.`

**D6. 1-b 인터뷰 불릿 갱신 (44행)** — 치환:

- old: `- If requirements are vague, interview the user here (one question at a time, per plan-context rules) — the planning agent cannot ask the user anything`
- new: `- If requirements are vague, interview the user here per plan-context Interview Mode mechanics — one question at a time, ambiguity ledger (모호성 원장), Refine gate, fact-confirmation routing (see plan-context references/planning-workflow.md, Interview Mode) — the planning agent cannot ask the user anything`

**D7. 신규 섹션 1-c Restate Gate 삽입** — D6 편집된 불릿(1-b 마지막 줄)과 `### 1-c. Plan Authoring (dedicated planning agent)` 헤딩 사이에 다음 블록 삽입 (앞뒤 빈 줄 1개씩):

```markdown
### 1-c. Restate Gate (재진술 확인 게이트)

Run in the orchestrator immediately after 1-b, **before** spawning the expensive planning agent. No subagent, no max-reasoning cost — one cheap checkpoint to prevent a wasted max-reasoning plan built on a misunderstanding.

1. Restate the agreed goal as **one sentence** covering target (what/where), the change, and the success criterion. Derive it from the 1-b answers and, when present, the resolved ambiguity-ledger tracks. Test: a third party reading only this sentence should reach the same conclusion about what is being built.
2. Confirm via `AskUserQuestion` (Codex: plain-text question, end the turn). Options:
   - **Yes, proceed to planning** — pass the confirmed sentence to 1-d as the top-line goal statement
   - **Adjust wording** — apply the user's correction and restate again (max 3 cycles; after the 3rd, ask the user to write the sentence verbatim and use it as-is)
   - **Missing scope** — return to the 1-b interview for the missing scope, then restate again
3. The confirmed sentence feeds the planning-agent input and the plan's Requirements Summary. Everything else from 1-b is passed to 1-d in full multi-section form — the restatement is the only place where one-line compression is the goal.

Confirming the restatement authorizes **plan authoring (1-d) only**. It is not approval to implement — the Step 2 hard gate is unchanged.
```

**D8. 1-c → 1-d 재명명 및 입력 목록 보강** — 헤딩 치환: `### 1-c. Plan Authoring (dedicated planning agent)` → `### 1-d. Plan Authoring (dedicated planning agent)`. Agent input 목록의 첫 불릿(`- User requirements and interview answers from 1-b`) 바로 아래에 신규 불릿 추가:

```markdown
- The confirmed goal restatement from 1-c (top-line goal statement)
```

**D9. Post-processing 문단 이동** — 70행의 `Post-processing (orchestrator): save the returned plan to ...` 문단 전체를 1-d 섹션 끝에서 **삭제**하고, D10에서 삽입할 1-e 섹션의 마지막 문단으로 **재배치**하되 도입부만 수정: `Post-processing (orchestrator):` → `Post-processing (orchestrator, after the 1-e verdict):` (나머지 문장은 무변경 유지).

**D10. 신규 섹션 1-e 삽입** — 1-d 섹션 끝(Required Plan Sections 목록의 `8. **Verification Steps**` 다음, D9로 문단 삭제 후)과 `## Step 2: User Review` 사이에 다음 블록 삽입:

```markdown
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
```

이 블록 바로 아래에 D9의 이동 문단(`Post-processing (orchestrator, after the 1-e verdict): save the returned plan to ...`)을 배치.

**D11. Step 2 첫 문단 갱신 (74행)** — 치환:

- old: `Present plan summary and affected file list. Offer three choices:`
- new: `Present the plan summary, affected file list, and the 1-e Reviewer notes (검토 노트) — including any unresolved HIGH finding, marked as such. Offer three choices:`

**D12. Comment 루프 참조 재번호 (80, 91행)** — `return to Step 1-c` → `return to Step 1-d`; `the dedicated planning agent (Step 1-c)` → `the dedicated planning agent (Step 1-d)`. (82–89행 hard gate 문단은 **손대지 않는다**.)

**D13. Exceptions 표에 3행 추가 (120행 마지막 행 아래)**:

```markdown
| Restate gate not converging after 3 cycles | Ask the user to write the one-sentence goal verbatim; use it as-is |
| HIGH findings remain after the single 1-e revision cycle | Do not loop again; surface them unresolved in Step 2 Reviewer notes — the user decides |
| Environment lacks parallel subagents for 1-e | Run the two lanes sequentially (Agent & Model Policy fallback) |
```

### 파일 2: `D:\001_Work\2026\017_claude\plugins\dh_skills\skills\plan-context\SKILL.md` (편집 P1–P2)

**P1. Phase A-2 모드 표 Interview 행 (166행)** — 치환:

- old: `| Interview | Default for broad/vague requests | Interactive requirements gathering, one question at a time |`
- new: `| Interview | Default for broad/vague requests | Interactive requirements gathering, one question at a time, tracked by an ambiguity ledger (모호성 원장) |`

**P2. Core Rules 불릿 2개 추가** — `- Classify questions: codebase facts -> explore first; user preferences/scope/requirements -> ask user` 불릿 바로 아래에 삽입:

```markdown
- Interview Mode only: track open ambiguity in a five-track **ambiguity ledger (모호성 원장)** — Scope / Constraints / Success Criteria / Non-goals / Verification — and pass reasoning-bearing free-form answers through the **Refine gate** before committing them (see `references/planning-workflow.md`, Interview Mode)
- Interview Mode only: route explored codebase facts by confidence — high-confidence facts auto-adopt with a non-blocking notice, medium/low confidence requires user confirmation; after 3 consecutive non-user answers the next question MUST go directly to the user (Dialectic Rhythm Guard — see `references/planning-workflow.md`, Interview Mode)
```

그 외 섹션(Phase A, Phase B, Plan Output Format, Direct/Consensus/Review 관련 행)은 일절 무변경.

### 파일 3: `D:\001_Work\2026\017_claude\plugins\dh_skills\skills\plan-context\references\planning-workflow.md` (편집 W1–W6)

**W1. Invocation Contexts 예외 불릿 추가** — `- All user feedback and approval happen exclusively in ...` 불릿(23행) 바로 아래에 삽입:

```markdown
- Exception to the above: when dh-dev runs its 1-b interview in the orchestrator, the Interview Mode **mechanics** below do apply — ambiguity ledger, Refine gate, fact-confirmation routing, one question at a time. What is never entered from dh-dev is Interview Mode plan authoring (steps 7-8): the plan is always authored by dh-dev's dedicated planning agent.
```

**W2. Interview Mode 번호 절차 교체 (36–42행)** — 기존 7단계 목록 전체를 다음 8단계로 치환:

```markdown
1. **Classify the request**: Broad triggers interview mode
2. **Initialize the ambiguity ledger (모호성 원장)**: open the five tracks (see Ambiguity Ledger below) and show the initial snapshot
3. **Ask one focused question** via `AskUserQuestion` for preferences, scope, constraints — target the most-stale `Open` track unless the user steers elsewhere
4. **Gather codebase facts first**: Spawn `explore` agent to find patterns/implementations before asking the user, then route the result via Fact-Confirmation Routing (below)
5. **Build on answers**: Each question builds on the previous answer; reasoning-bearing free-form answers pass the Refine Gate (below) before being committed to the ledger
6. **Consult Analyst** (Opus) for hidden requirements, edge cases, risks
7. **Create plan** when user signals readiness ("create the plan", "I'm ready") — if any ledger track is still `Open`, list the open tracks and ask one confirmation question before proceeding
8. Save plan to `docs\plans\YYYY-MM-DD_HHMMSS_<slug>.md`
```

**W3. Question Classification 표 Codebase Fact 행 치환**:

- old: `| Codebase Fact | "What patterns exist?", "Where is X?" | Explore first, do not ask user |`
- new: `| Codebase Fact | "What patterns exist?", "Where is X?" | Explore first, then route via Fact-Confirmation Routing (below) — never ask the user blind |`

**W4. 신규 하위섹션 3개 삽입** — `### Question Classification` 표 끝과 `### Design Option Presentation` 사이에 다음을 순서대로 삽입 (구분선 없이 헤딩 연속):

```markdown
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
```

**W5. Quality Criteria Final Checklist에 1항목 추가** — `- [ ] Plan saved to \`docs\plans\\\`` 항목 아래에:

```markdown
- [ ] Interview mode: every ledger track `Resolved` or `Waived` before plan creation
```

**W6. Tool Usage에 1불릿 추가** — `- Plain text for questions needing specific values (port numbers, names)` 아래에:

```markdown
- Refine gate confirmations and PATH 1b fact confirmations use `AskUserQuestion` when available; in Codex, plain-text with the same options
```

Direct Mode / Consensus Mode / Review Mode 섹션은 일절 무변경.

### 파일 4: `D:\001_Work\2026\017_claude\plugins\dh_skills\skills\plan-context\references\templates.md` (편집 T1)

**T1. 신규 섹션 삽입** — `## Plan History Template` 섹션의 닫는 코드펜스(123행) 뒤, `## Status Values`(125행) 앞에 삽입:

````markdown
## Interview Mode Templates (인터뷰 모드 템플릿)

Chat-display formats used by Interview Mode (`planning-workflow.md`). Not saved to files.

### Ambiguity Ledger Snapshot (모호성 원장 스냅샷)

```markdown
### Ambiguity Ledger (모호성 원장)
| Track | Status | Latest resolution |
| --- | --- | --- |
| Scope (범위) | Resolved | <one-line pointer> |
| Constraints (제약) | Partially resolved | <one-line pointer> |
| Success Criteria (성공 기준) | Open | — |
| Non-goals (제외 범위) | Open | — |
| Verification (검증 방법) | Waived | user: "decide for me" |
```

Status values: `Open` / `Partially resolved` / `Resolved` / `Waived`.

### Refine Gate Structured Payload (자유서술 구조화 페이로드)

```markdown
Decision: <the decision>
Reasoning: <user's rationale, faithful to their wording>
Constraints (user-stated): <explicit constraints>
Out of scope (user-stated): <explicit exclusions>
Codebase context (orchestrator-verified): <file/config facts verified this session>
```
````

### 편집하지 않는 것 (명시적 무변경 목록)

- dh-dev Step 2 hard gate 문단(82–89행), Step 3, Step 4 전체
- plan-context Phase A(Step 0–6), Phase B, Boundary, File Structure 섹션
- planning-workflow.md의 Direct/Consensus/Review Mode 섹션
- templates.md의 Context Summary/Plan Document/Plan History/Status Values/Notes 섹션
- `README.md`(신규 파일이 없으므로 트리 갱신 불필요), `docs\` 이하 역사 기록 문서, `.codex-plugin\plugin.json`
- 신규 파일·디렉토리 생성 없음 (D-8 결정)

---

## 4. Code Writing Guide (코드 작성 가이드)

- **500행 규칙**: 각 SKILL.md는 500행 미만 유지. 이번 변경 후 예상치는 dh-dev 약 180행, plan-context 약 272행으로 여유가 크므로 references 분리 금지(불필요한 구조 변경).
- **Progressive disclosure**: 상세 절차는 `references/*.md`, SKILL.md에는 요약 불릿 + 참조 포인터만 — P2 불릿이 이 패턴을 따름(본문은 planning-workflow.md에).
- **한글 부제 병기**: 신규 섹션 제목은 "영문 (한글 부제)" 형식 — `Restate Gate (재진술 확인 게이트)`, `Adversarial Plan Preview (계획 초안 적대적 검증)`, `Ambiguity Ledger (모호성 원장)`, `Refine Gate (자유서술 구조화 게이트)`, `Fact-Confirmation Routing (신뢰도 기반 사실확인 라우팅)`, `Reviewer notes (검토 노트)`, `Dialectic Rhythm Guard (문답 리듬 가드)`.
- **표 형식**: 기존 파이프 테이블 스타일( `| --- |` 구분행 ) 유지. Agent & Model Policy·Exceptions 표에 행 추가 시 열 수(각 4열, 2열) 정확히 일치시킬 것.
- **Codex 이중 분기 관행**: 새 상호작용 지점(1-c 게이트, 1-e 레인, Refine/PATH 1b 확인)마다 `AskUserQuestion` 사용 + Codex 평문 폴백을 명시 — D5/D7/W6이 담당.
- **경로 표기**: 본문 내 프로젝트 경로는 기존 관행대로 백슬래시(`docs\plans\`), 스킬 내부 상대 참조는 슬래시(`references/planning-workflow.md`).
- **인코딩**: 모든 파일 쓰기는 UTF-8(BOM 없음). 편집 후 반드시 한글 포함 라인을 read-back하여 mojibake 검사(U+FFFD, `占쏙옙`, `ï»¿`, 한글 자리 `?`). 이모지 신규 유입 금지(`Auto-confirmed:` 평문 접두어 사용), `§` 문자 금지. 기존 문서에 이미 쓰이는 `→`, `✓`, `✗`는 사용 가능.
- **금지**: 기존 hard gate 문구 수정, Interview Mode 외 모드로의 규칙 누출, `Step 1-c` 문자열 잔존, 새 MCP 도구/서버 언급.

---

## 5. Definition of Done (개발 완료조건)

| # | 조건 (이진 판정) |
| --- | --- |
| DoD-1 | `skills\dh-dev\SKILL.md`에 `### 1-c. Restate Gate (재진술 확인 게이트)` 헤딩이 존재하고, 헤딩 순서가 정확히 `1-a → 1-b → 1-c(Restate) → 1-d(Plan Authoring) → 1-e(Adversarial Plan Preview)`다 |
| DoD-2 | 동일 파일에서 `grep -c "contrarian"` ≥ 2, `grep -c "gap_hunter"` ≥ 2이며, 1-e 본문에 `HIGH`, `once`, `Reviewer notes`가 모두 포함된다 |
| DoD-3 | 저장소 전체 `*.md`에서 `Step 1-c` 문자열이 0건이다 |
| DoD-4 | dh-dev Step 2의 hard gate 문단(현재 82–89행 블록: `**Hard gate**: ...`부터 `In Codex, ...end the turn.`까지)이 git diff에서 무변경이다 |
| DoD-5 | Agent & Model Policy 표가 4행(헤더 제외 3개 phase: 1-d, 1-e, Step 3)이고, Exceptions 표에 신규 3행이 존재한다 |
| DoD-6 | `skills\plan-context\SKILL.md` Core Rules에 `Interview Mode only:` 불릿이 정확히 2개 추가되었고, git diff에서 이 파일의 변경 hunk가 P1 표 행 + P2 불릿 2개뿐이다 |
| DoD-7 | `planning-workflow.md` Interview Mode에 `### Ambiguity Ledger (모호성 원장)`, `### Refine Gate (자유서술 구조화 게이트)`, `### Fact-Confirmation Routing (신뢰도 기반 사실확인 라우팅)` 3개 헤딩이 존재하고 번호 절차가 `8.`까지 있다 |
| DoD-8 | `planning-workflow.md`의 Direct/Consensus/Review Mode 섹션(현재 64–138행)이 git diff에서 무변경이다 |
| DoD-9 | `templates.md`에 `## Interview Mode Templates (인터뷰 모드 템플릿)` 헤딩이 Plan History Template과 Status Values 사이에 존재한다 |
| DoD-10 | Invocation Contexts에 `steps 7-8` 예외 불릿(W1)이 존재하고, dh-dev SKILL.md 1-b 불릿이 `Interview Mode mechanics`를 참조한다 |
| DoD-11 | 변경된 4개 파일의 총 라인 수가 각각 500행 미만이다 |
| DoD-12 | 신규 생성 파일 0건(git status 기준 이 작업으로 인한 untracked 추가 없음), README.md 무변경 |
| DoD-13 | 4개 파일 read-back에서 mojibake 시그니처(U+FFFD, `占쏙옙`, `ï»¿`) 0건, 신규 유입 이모지 0건, `§` 0건 |

---

## 6. Adversarial Test Environment (적대적 테스트 환경)

실행 코드가 아닌 스킬 문서 변경이므로 테스트는 **문서 정합성 검증**으로 설계한다. 전부 저장소 루트(`D:\001_Work\2026\017_claude\plugins\dh_skills`)에서 실행.

| 테스트 | 절차 | 기대 결과 | 검증 대상 DoD |
| --- | --- | --- | --- |
| T-1 헤딩 순서 | `Grep "^### 1-" skills\dh-dev\SKILL.md -n` | 정확히 5건, 순서 1-a/1-b/1-c(Restate)/1-d(Plan Authoring)/1-e(Adversarial) | DoD-1 |
| T-2 dangling 재번호 | `Grep "Step 1-c"` 저장소 전체 `*.md`; 추가로 `Grep "1-c" skills\dh-dev\SKILL.md -n`으로 잔존 참조가 전부 Restate 게이트 문맥인지 육안 확인 | `Step 1-c` 0건; `1-c` 잔존건은 모두 Restate 참조 | DoD-3 |
| T-3 레인·심각도 존재 | `Grep "contrarian\|gap_hunter\|HIGH/MEDIUM/LOW\|Reviewer notes" skills\dh-dev\SKILL.md -c` | 각 항목 ≥ 1건, contrarian/gap_hunter 각 ≥ 2건 | DoD-2 |
| T-4 hard gate 불변 | `git diff -U0 skills\dh-dev\SKILL.md` 후 `**Hard gate**`~`end the turn.` 블록이 어떤 hunk에도 포함되지 않음을 확인 | 해당 블록 무변경 | DoD-4 |
| T-5 표 열 정합 | Agent & Model Policy·Exceptions 표를 Read하여 각 행의 파이프 열 수가 헤더와 동일한지 확인 | 4열/2열 전행 일치, 렌더 깨짐 없음 | DoD-5 |
| T-6 모드 격리 | `git diff skills\plan-context\references\planning-workflow.md`의 hunk 위치가 Invocation Contexts·Interview Mode·Quality Criteria·Tool Usage 범위에만 존재; Direct(`## Direct Mode`)~Review(`## Review Mode`) 사이 hunk 0건. `git diff skills\plan-context\SKILL.md` hunk가 모드 표 Interview 행+Core Rules 2불릿뿐 | Interview 외 모드 diff 0건 | DoD-6, DoD-8 |
| T-7 상호참조 왕복 | dh-dev 1-b가 참조하는 `Interview Mode` 헤딩, `templates.md, Interview Mode Templates` 참조, W1의 `steps 7-8`이 실제 존재하는지 각 파일 Read로 확인 | 모든 참조 대상 실존, 단계 번호 일치(8단계 목록에서 7-8이 플랜 저작/저장) | DoD-7, DoD-9, DoD-10 |
| T-8 라인 수 한도 | 4개 파일 Read 후 마지막 라인 번호 확인 | 전부 < 500 | DoD-11 |
| T-9 신규 파일·README | `git status --short`에서 이 작업으로 추가된 untracked 파일 없음; `git diff README.md` 비어 있음 | 0건/무변경 | DoD-12 |
| T-10 인코딩 적대 검사 | `PYTHONIOENCODING=utf-8` 하에 Python heredoc으로 4개 파일을 `encoding='utf-8'`로 읽어 (a) `U+FFFD` 카운트, (b) `占쏙옙`/`ï»¿`/`§` 검색, (c) 신규 섹션의 한글 부제 5종(`재진술 확인 게이트` 등)을 그대로 출력해 육안 확인 | (a)(b) 0건, (c) 한글 온전 출력 | DoD-13 |
| T-11 dry-run 시나리오 트레이스 (게이트 순서 검증) | 가상 요청 "우리 앱 로깅 좀 개선해줘"(모호·파일 미지정)를 변경된 문서만 보고 수기 트레이스: ① 1-a 탐색 → ② 1-b 인터뷰 진입, 원장 5트랙 Open 스냅샷 표시 → ③ explore가 `pyproject.toml`에서 `structlog` 발견 → PATH 1a 자동채택 통보+카운터 1 → ④ 로그 포맷 후보 2개 발견 → PATH 1b 확인, "Yes, correct" 클릭 → 카운터 2 → ⑤ 또 하나의 매니페스트 사실 자동채택 → 카운터 3 → ⑥ **다음 질문이 강제 PATH 2**(가장 오래된 Open 트랙 = Success Criteria)로 라우팅되는지 문서 규칙으로 도출 가능한지 확인 → ⑦ 사용자가 3문장 자유서술(결정+근거+제외범위) 답변 → Refine 게이트 발동, 4옵션 확인 후 원장 커밋, 카운터 0 리셋 → ⑧ 전 트랙 Resolved/Waived → dh-dev 1-c Restate 1문장 확인("Yes, proceed to planning") → ⑨ 1-d 플랜 저작 → ⑩ 1-e 패널: gap_hunter가 HIGH(DoD 항목에 테스트 미매핑) 반환 → 1-d 1회 재작성 → 구조 검사만 재실행 → ⑪ Step 2에서 Reviewer notes와 함께 제시, hard gate 정지. 각 전이가 문서의 명시 규칙만으로 유도되는지(설계 판단 불필요) 확인 | 11개 전이 전부 문서 규칙만으로 유도됨; 모순·공백 발견 시 실패 | DoD-1, 2, 7, 10 종합 |
| T-12 hard gate 우회 시도 (적대) | 문서만 근거로 다음 3개 공격 질문에 "불가"가 도출되는지 확인: (a) "Restate에서 Yes 받았으니 바로 Step 3 가도 되나?" → 1-c의 "not approval to implement" 문장으로 차단 (b) "1-e 패널이 무발견이면 Step 2 생략 가능한가?" → "The panel never approves" 문장으로 차단 (c) "HIGH가 남았는데 패널을 한 번 더 돌려 통과시킬 수 있나?" → "once"/"Do not loop again" 규칙으로 차단 | 3건 모두 명시 문구로 차단 | DoD-2, DoD-4 |

---

## 7. Risks and Mitigations

| 위험 | 영향 | 완화 |
| --- | --- | --- |
| 재번호(1-c→1-d) 누락으로 dangling reference | 오케스트레이터가 잘못된 단계로 점프 | 파급 범위를 grep으로 사전 확정(3곳뿐, B-6); T-2가 저장소 전체를 재검증 |
| 신규 게이트가 hard gate를 약화한다는 오독 | 승인 전 구현 착수 사고 | D-6/T-12: "플랜 저작 승인일 뿐" 문장과 "패널은 승인 주체가 아님" 문장을 본문에 명문화; hard gate 문단 자체는 바이트 단위 무변경(DoD-4) |
| 1-e 재작성 루프 폭주 | 토큰 낭비·지연 | 재작성 1회 한도 + 재작성 후 레인 재스폰 금지(구조 검사만) + Exceptions 행으로 탈출 경로 명시 |
| Interview Mode 규칙이 Direct/Consensus/Review로 누출 | 승인 범위 초과(범위 확장) | 모든 신규 규칙에 "Interview Mode only" 접두; 편집 위치를 Interview 섹션·Core Rules 불릿으로 한정; T-6이 diff hunk 위치로 기계 검증 |
| dh-dev 1-b와 Invocation Contexts의 "Phase A-2 미진입" 규칙 충돌 | 문서 모순 → 실행 시 혼선 | W1 예외 불릿이 "메커니즘은 적용, 플랜 저작(7-8단계)은 미진입"으로 경계를 명시; T-7 왕복 검증 |
| AskUserQuestion 4옵션 제한과 ouroboros 5옵션 원형 불일치 | Refine 게이트 실행 불가 | D-9: 4옵션으로 재설계, "Add context"는 자유서술(Rewrite 입력 취급)으로 흡수함을 본문 명시 |
| 카운터 리셋 조건 모호("Yes, correct"가 리셋인가?) | Rhythm Guard 오작동 | D-10: rubber-stamp=증가, 실질 답변(정정·PATH 2 답변)=리셋을 W4 본문에 이진 규칙으로 명문화 |
| Windows 편집 중 한글/특수문자 인코딩 손상 | 문서 mojibake | UTF-8 강제 + T-10 적대적 read-back(전역 인코딩 정책 준수); 이모지·`§` 신규 유입 금지 |
| 문서 비대화로 500행 규칙 위반 | 저장소 컨벤션 위반 | 변경 후 예상 최대 272행(plan-context SKILL.md), 여유 확인 완료(D-8); T-8이 기계 검증 |
| 레인 명칭·심각도 어휘가 자유 변형되어 합성 불능 | 오케스트레이터가 결과를 상관 못 함 | 1-e 본문에 출력 계약(`severity — section — finding — suggested fix`)과 레인 명칭을 백틱 리터럴로 고정 |

---

## 8. Verification Steps

구현 완료 후 실행자가 순서대로 수행(전부 자가 검증 가능 — 사용자 위임 불가):

1. **T-1~T-3 실행**: 헤딩 순서 grep, `Step 1-c` 저장소 전체 grep, 레인/심각도 grep — 기대치 불일치 시 즉시 수정 후 재실행.
2. **git diff 검사 (T-4, T-6, T-9)**: `git diff skills\dh-dev\SKILL.md skills\plan-context\` 출력에서 hard gate 블록 미포함, Direct/Consensus/Review hunk 0건, README 무변경을 확인.
3. **표 렌더 검사 (T-5)**: 변경된 표 3개(정책 표, Exceptions, Question Classification)를 Read하여 열 수 일치 확인.
4. **상호참조 왕복 (T-7) + 라인 수 (T-8)**: 참조 대상 헤딩 실존 확인, 4개 파일 라인 수 < 500 확인.
5. **인코딩 read-back (T-10)**: UTF-8로 4개 파일 재독 후 한글 부제 5종을 실제 출력하여 육안 확인, mojibake 시그니처 0건 확인 — 결과를 보고서에 "무엇을 읽어 어떻게 확인했는지"와 함께 기재.
6. **dry-run 트레이스 (T-11) + 우회 공격 (T-12)**: 시나리오 11개 전이와 공격 3건을 문서 인용(파일:섹션)과 함께 기록. 하나라도 문서 규칙만으로 유도되지 않으면 해당 규칙 문구를 보강하고 1번부터 재검증.
7. **DoD 체크리스트 산출**: DoD-1~13 각각 pass/fail + 근거(grep 출력, diff 요약, read-back 샘플)를 오케스트레이터에 반환. 전 항목 green이 아니면 완료 보고 금지.
8. 이후 dh-dev Step 4에서 `/revision-tracker`가 개정 로그를 생성하고, 본 계획의 plan_history 상태를 `Completed`로 갱신한다(실행자 범위 밖 — 오케스트레이터 담당).

---

### 참고: 검증에 사용한 원본 파일 (절대 경로)

- `D:\001_Work\2026\017_claude\plugins\dh_skills\skills\dh-dev\SKILL.md` (121행)
- `D:\001_Work\2026\017_claude\plugins\dh_skills\skills\plan-context\SKILL.md` (268행)
- `D:\001_Work\2026\017_claude\plugins\dh_skills\skills\plan-context\references\planning-workflow.md` (177행)
- `D:\001_Work\2026\017_claude\plugins\dh_skills\skills\plan-context\references\templates.md` (142행)
