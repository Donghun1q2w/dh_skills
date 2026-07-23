# dh-dev Agent & Model Policy 모델·effort 3단계 티어링 도입

- **Date**: 2026-07-23 10:55:47
- **Status**: Completed

---

## 1. Requirements Summary

**확정 목표(1-c Restate 확정문)**: dh-dev의 Agent & Model Policy(1-d Plan Authoring, Step 3 Execute)에 3단계(Large/Medium/Small) 모델·effort 티어링을 추가한다 — 1-d 티어는 1-b 인터뷰로 모호성을 해소한 뒤 1-c Restate 확정 시점에 판정하고, Step 3 티어는 승인된 계획의 Implementation Steps(파일 수·변경 규모·위험 영역)로 판정하며, 신호가 애매하면 항상 상위 등급으로 반올림하고 Large를 보수적 기본값으로 유지한다.

**사용자 원문 요청**: "유저 요구사항 및 계획에 따라 plan/execute model 과 effort를 탄력적으로 조정할 수 있도록. 보수적으로 높은 모델을 사용하되 실행 목표가 매우 작은 경우 작은 모델이나 effort로 진행가능하도록"

**대상 파일**:
- `D:\001_Work\2026\017_claude\plugins\dh_skills\skills\dh-dev\SKILL.md` (주 대상, 현재 158행)
- `D:\001_Work\2026\017_claude\plugins\dh_skills\skills\plan-context\references\planning-workflow.md` (21행 괄호 문구 1줄 정합성 수정 — 아래 D-10)

**Step 2 제시 시 안내 문구 (투명성, 필수)**: 오케스트레이터는 Step 2에서 계획 요약을 제시할 때 "재진술 확정문 범위 밖의 정합성 수정 1건이 포함됨 — `plan-context/references/planning-workflow.md` 21행의 dh-dev 교차 참조 갱신(D-10). 행동 변화 없는 서술 정합성 수정"을 명시적으로 언급한다. 확정문은 dh-dev의 Agent & Model Policy만 언급하므로, 이 두 번째 파일 편집은 사용자가 승인 전에 반드시 인지해야 한다.

**사용자가 인터뷰에서 확정한 사항 (재설계 금지)**:
- 3단계 Large/Medium/Small. 4단계(Trivial=Haiku) 명시적 거부 — Haiku는 이 정책에 등장 금지(기존 1-a `explore` 에이전트는 무관, 무변경).
- 티어별 모델/effort: Large = 1-d Fable 5(`fable`, fallback `opus`)/max + Step 3 Opus 4.8(`opus`)/max (현행 유지), Medium = 양쪽 `opus`/high, Small = 양쪽 `sonnet`/standard.
- 애매하면 항상 상향 반올림, Large가 기본값.
- **판정 수치 경계와 위험 키워드의 출처**: 파일 수 경계(1 / 2–5 / 6+ 상당), 변경 줄 수 경계(약 ≤30 / ~150 이하 / 초과), 위험 키워드 분류(보안/결제/마이그레이션/동시성)는 오케스트레이터가 AskUserQuestion으로 제시한 "3단계 Large/Medium/Small (Recommended)" 옵션의 description 문구에 그대로 포함되어 있었고, **사용자가 다른 경계값을 요구하지 않고 해당 옵션을 선택함으로써 승인됨**. D-4/D-5가 인용하는 "사용자 표"는 바로 이 옵션 설명을 가리킨다. (D-5의 나머지 2분류 — 시크릿/자격증명, 파괴적 작업 — 는 미션 지시의 예시에서 온 추가분이며 D-5 근거에 별도 기록.)
- 1-d 티어는 1-c Restate 사용자 확정 시점에 판정(1-a 신호만으로 조기 판정 금지). Step 3 티어는 승인된 계획의 Implementation Steps로 판정.
- 판정은 오케스트레이터의 결정론적 체크리스트로, 서브에이전트 호출 없이, 추가 확인 질문 없이 수행하되 `Tier: ... — rationale: ...` 한 줄 고지로 항상 투명하게 표시.
- 1-e(Sonnet/standard 고정)와 1-c(서브에이전트 없음)는 티어링 범위 외 — 무변경.

**절대 불변 조건**: 티어링은 모델/effort 선택에만 영향. Step 2 hard gate(SKILL.md 117행 문단)는 바이트 단위 무변경이며, Small 등급이어도 1-e 프리뷰·Step 2 승인·Step 4를 전부 동일하게 통과한다.

### 설계 결정 기록 (애매 지점에 대한 자체 판단과 근거)

| ID | 결정 | 근거 |
| --- | --- | --- |
| D-1 | 기존 Agent & Model Policy 표(24–28행)는 3행 유지하고 1-d/Step 3 행의 Model/Effort 셀만 "tiered — Large (default): ..."로 바꾸며, 판정 기준·티어별 모델은 신설 `### Model & Effort Tiering` 하위 섹션의 **단일 티어 표**(Tier x 판정기준 x 1-d x Step 3)에 집약 | 사용자가 승인한 표가 바로 이 형태(Tier 축)였고, Phase별 3행씩 늘리면 판정 기준이 2벌 중복되어 드리프트 위험. 500행 예산과도 무관하게 유지보수성 우위 |
| D-2 | 1-c 티어 판정은 기존 항목 2(AskUserQuestion)와 3(데이터 전달) **사이**에 새 항목 3으로 삽입, 기존 3은 4로 재번호 | "Yes, proceed to planning 확정 바로 그 시점"이라는 사용자 지정 위치와 정확히 일치. 확정 → 판정 → 1-d 입력 전달 순서가 서사적으로 자연스러움 |
| D-3 | Step 3 티어 판정은 기존 항목 1(plan status 변경) **직전**의 새 항목 1로 삽입, 기존 1–6은 2–7로 재번호 | 판정은 승인된 계획에 대한 읽기 전용 분석이므로 어떤 부수효과(plan_history 변경)보다 먼저 수행·고지하는 것이 안전. 미션이 직전/직후 모두 허용했고 직전을 선택 |
| D-4 | 판정 기준을 수치 경계로 결정론화: 파일 수 1 / 2–5 / 6+, 변경 줄 수 ≤30 / 31–150 / >150, 신호별 최악값 채택(worst-wins) | 사용자가 선택한 AskUserQuestion 옵션 설명(위 "출처" 항목)의 "다수 파일"·"~150줄 이하"·"~30줄 이하"를 체크리스트로 실행하려면 경계가 필요. Medium=2–5 확정이므로 "다수"=6+가 유일하게 무모순. worst-wins가 "상향 반올림"의 기계적 구현 |
| D-5 | 위험 키워드 6분류 고정: security/auth(보안·인증·인가), payment/billing(결제·과금), migration/schema(마이그레이션·스키마 변경), concurrency/locking/threading(동시성·락·스레드), secrets/credentials/API keys(시크릿·자격증명·API 키), destructive ops — delete/drop/force-push/mass update(삭제·파괴적 작업) | 사용자가 선택한 옵션 설명에 명시된 4종(보안/결제/마이그레이션/동시성) + 미션 지시 예시(시크릿/자격증명, 삭제/파괴적 작업)의 합집합. 그 이상 확장하지 않음(과잉 Large 판정 방지) |
| D-6 | effort 파라미터가 없는 하네스용 지시어 매핑: Large→`ultrathink`, Medium→`think hard`, Small→지시어 없음 | 기존 30행이 이미 max→`ultrathink` 매핑을 정의. 3단계로 자연 확장하며 Claude Code 사고 키워드 위계를 따름 |
| D-7 | 고지 문구 포맷은 티어링 섹션에 **1회만** 정의하고 1-c/Step 3 항목은 "Print the Tier announcement line"으로 참조 | 동일 포맷 3중 복제 시 드리프트 위험. 단일 정의 + 참조가 grep 검증도 단순화 |
| D-8 | `references/` 디렉토리 신설하지 않음 | 변경 후 예상 약 194행(±5) — 500행 기준의 40% 미만. 직전 계획 D-8과 동일 논리(신설 시 README 트리 갱신 부담만 증가) |
| D-9 | 재스폰 시 티어 규칙: Step 2 Comment 루프의 1-d 재스폰은 피드백 반영 후 체크리스트 재실행하되 같은 Comment 루프 내에서 **상승만 허용, 하락 금지**. 1-e 단일 수정 사이클과 Step 3 오류수정 재스폰은 기존 판정 티어 재사용 | Comment로 범위가 커지면 상향이 필요(보수 원칙). 하락 허용 시 "피드백 몇 마디로 싼 모델로 갈아타는" 품질 저하 경로가 생김. 1-e 발견사항·오류수정은 범위 변경이 아니므로 재판정 불필요. 이 규칙의 핵심 문구는 DoD-17 + T-1 grep + T-12 dry-run으로 검증 |
| D-10 | `plan-context/references/planning-workflow.md:21`의 "(Fable 5, max reasoning effort)" 괄호를 티어링 반영 문구로 1줄 수정 | 이 문서가 dh-dev의 플래닝 에이전트 모델을 고정값으로 서술하고 있어 방치 시 문서 간 모순 발생. 행동 변화 없는 서술 정합성 수정이므로 최소 범위로 포함. 재진술 범위 밖 편집이므로 Step 2에서 별도 고지(위 "Step 2 제시 시 안내 문구"). 그 외 파일(README.md 24행은 모델 언급 없음 — 확인 완료)은 무변경 |
| D-11 | frontmatter description(3행)의 "(Fable 5, max reasoning effort — ...)"와 "(Opus 4.8, max reasoning effort)" 두 괄호를 "tiered ... Large default: ..." 형태로 갱신 | description은 스킬 검색·트리거에 노출되는 대외 계약. 고정 모델 약속을 남기면 스킬 목록 설명과 본문이 모순 |
| D-12 | Step 3 티어는 1-d 티어와 **독립 판정**(둘이 다를 수 있음)을 명문화 | 계획 과정에서 범위가 커지거나(플래닝은 Small였는데 계획 결과 6파일) 작아질 수 있음. 승인된 계획이 Step 3의 유일한 진실 원천 |
| D-13 | 9–16행 ASCII 흐름도 무변경 | 티어 판정은 1-c/Step 3의 하위 항목이며 흐름도 해상도(단계 수준)에서는 새 단계가 아님 |
| D-14 | 18행 Effort 블록쿼트에 carve-out 문장 추가(S-2): "항상 max 유지" 규칙은 **오케스트레이터 컨텍스트 자신**에게만 적용되고, 1-d/Step 3 서브에이전트는 티어링 정책이 정한 모델/effort로 실행되며 이는 규칙 위반이 아님을 분리 선언 | 이 문장 없이는 기존 18행("keep it there through implementation")과 Medium/Small 티어 스폰이 정면 모순 — 독자가 티어링 무시(항상 max) 또는 effort 지시 위반 중 하나를 강제당함. 핵심 문구 `does not violate this rule`은 DoD-16 + T-1 grep으로 검증 |

## 2. Acceptance Criteria

**변경 전 baseline (2026-07-23 실측, git b441040 기준 clean)**:

| # | Baseline 사실 | 측정 방법(실측 완료) |
| --- | --- | --- |
| B-1 | `skills\dh-dev\SKILL.md`는 정확히 158행 | `wc -l` = 158 |
| B-2 | Agent & Model Policy 표(24–28행)는 데이터 3행·4열이며 모델이 전부 고정값(Fable 5 / Sonnet / Opus 4.8), effort는 1-d·Step 3 모두 "maximum — `effort: "max"`" | 26·28행 원문 확인 |
| B-3 | 파일 내 대소문자 구분 `Large`, `Small`, `tier`, `Tier` 매치 0건. `Medium`은 95행 `severity (HIGH/MEDIUM/LOW)`의 대문자 `MEDIUM`으로만 존재 | `grep -cE "Large|Small|tier|Tier"` = 0, `grep -nE "Medium|MEDIUM"` = 95행 1건 |
| B-4 | `haiku`/`Haiku` 매치 0건 | `grep -inE "haiku"` = 0 |
| B-5 | Step 2 hard gate 문단은 117행, "Before explicit approval" 불릿 3개는 119–122행 | Read 확인 |
| B-6 | `planning-workflow.md` 21행에 `(Fable 5, max reasoning effort)` 고정 문구 존재 | grep 확인 |

**변경 후 수용 기준** (전부 기계 판정 가능):

- AC-1: Agent & Model Policy 표의 1-d 행과 Step 3 행에 `tiered`가 포함되고 Large 기본값 모델(`fable`/`opus`)이 명시된다. 1-e 행(27행)은 git diff상 무변경이다.
- AC-2: `### Model & Effort Tiering (모델·effort 티어링)` 하위 섹션이 존재하고, 그 티어 표는 정확히 3개 데이터 행(`**Large** (default)` / `**Medium**` / `**Small**`)과 1-d·Step 3 열을 가지며, 모델·effort가 사용자 확정 표와 1:1로 일치한다(Large: fable→fallback opus/max + opus/max, Medium: opus/high 양쪽, Small: sonnet/standard 양쪽).
- AC-3: 1-c 목록에 새 항목 3 `**Tier decision (티어 판정, 1-d)**`이 존재하고 기존 "The confirmed sentence feeds..." 항목이 4번으로 재번호된다. Step 3 목록은 1–7번이 되며 1번이 `**Tier decision (티어 판정, Step 3)**`, 2번이 기존 plan status 변경이다.
- AC-4: 고지 포맷 리터럴 `` `Tier: <Large|Medium|Small> — rationale: `` 이 파일 전체에서 정확히 1회(티어링 섹션) 나타나고, `Tier announcement` 문자열이 4회 이상(정의부, 1-c 항목 3, Step 3 항목 1, Codex 폴백 불릿) 나타난다.
- AC-5: 상향 반올림 규칙("round up", "Large is the conservative default", "Small requires **all four** signals")과 위험 키워드 6분류가 티어링 섹션에 명시된다 (DoD-15 + T-1 개별 grep으로 이진 검증).
- AC-6: Codex 폴백 문구 `regardless of tier`가 2회 이상(Agent & Model Policy 불릿 + Exceptions 행) 존재하며, "effort 제어 불가 환경에서는 티어와 무관하게 항상 최대 추론"을 명시한다.
- AC-7: Step 2 섹션(`## Step 2: User Review`부터 `## Step 3` 직전까지)은 git diff hunk 0건 — hard gate 문단 바이트 무변경.
- AC-8: `grep -i haiku` = 0건 유지 (B-4 대비 무변화).
- AC-9: 최종 행 수 500행 미만 (예상 194행 ±5, B-1 대비 +33~+40행).
- AC-10: `planning-workflow.md`는 21행을 포함하는 단일 hunk만 변경되고 `Model & Effort Tiering` 참조가 포함된다 (B-6 해소).
- AC-11: frontmatter description(3행)에 `tiered Large/Medium/Small` 문자열이 존재한다.

## 3. Implementation Steps (구현 지침)

모든 편집은 `Edit` 도구의 **정확한 문자열 치환**으로 수행한다. 라인 번호는 참고치이며 앵커 문자열이 진실이다. 아래 old 문자열은 전부 현재 파일에서 유일함을 확인했다. 대상 파일: `skills\dh-dev\SKILL.md` (S-1~S-9), `skills\plan-context\references\planning-workflow.md` (S-10).

### S-1. frontmatter description 갱신 (3행, 치환 2건)

치환 1 — old:
```
plan authoring by a dedicated max-reasoning planning agent (Fable 5, max reasoning effort — detailed implementation steps, Definition of Done, adversarial test environment)
```
new:
```
plan authoring by a dedicated planning agent (tiered Large/Medium/Small model/effort, Large default: Fable 5 at max reasoning effort — detailed implementation steps, Definition of Done, adversarial test environment)
```

치환 2 — old:
```
goal-driven implementation by a dedicated executor agent (Opus 4.8, max reasoning effort)
```
new:
```
goal-driven implementation by a dedicated executor agent (tiered model/effort, Large default: Opus 4.8 at max reasoning effort)
```

주의: description은 한 줄 YAML 큰따옴표 문자열 — 새 텍스트에 `"` 문자를 넣지 않았으므로 파싱이 깨지지 않는다.

### S-2. Effort 블록쿼트 확장 (18행, 치환 1건)

old (문장 끝부분):
```
raise it to `max` before Step 1 and keep it there through implementation.
```
new:
```
raise it to `max` before Step 1 and keep it there through implementation. This governs the orchestrator context itself; the 1-d and Step 3 subagents run at the model/effort chosen by the Model & Effort Tiering policy below — a Medium/Small tier there does not violate this rule.
```
근거: D-14 — 이 문장을 방치하면 "항상 max 유지" 지시와 티어링이 정면 모순. 오케스트레이터 자신의 effort와 서브에이전트 effort를 분리 선언해야 하며, 핵심 문구 `does not violate this rule`은 DoD-16/T-1로 검증된다.

### S-3. Agent & Model Policy 표의 1-d·Step 3 행 치환 (26행, 28행)

치환 1 — old (26행 전체):
```
| Step 1-d Plan Authoring | dedicated planning agent | Fable 5 (`fable`); fallback: highest-reasoning model available (`opus`) | maximum — `effort: "max"` (ultracode-equivalent) |
```
new:
```
| Step 1-d Plan Authoring | dedicated planning agent | tiered — decided in 1-c (see Model & Effort Tiering); Large (default): Fable 5 (`fable`), fallback: highest-reasoning model available (`opus`) | tiered — Large (default): maximum `effort: "max"` (ultracode-equivalent) |
```

치환 2 — old (28행 전체):
```
| Step 3 Execute | dedicated executor agent | Opus 4.8 (`opus`) | maximum — `effort: "max"` (ultracode-equivalent) |
```
new:
```
| Step 3 Execute | dedicated executor agent | tiered — decided at Step 3 item 1 (see Model & Effort Tiering); Large (default): Opus 4.8 (`opus`) | tiered — Large (default): maximum `effort: "max"` (ultracode-equivalent) |
```

27행(1-e)은 절대 건드리지 않는다.

### S-4. Claude Code 불릿에 티어→effort/지시어 매핑 (30행, 치환 1건)

old:
```
Set reasoning effort to maximum when the harness exposes it (e.g., Workflow `agent(..., {effort: "max"})`); otherwise place an explicit maximum-reasoning directive (`ultrathink`) at the top of the agent prompt.
```
new:
```
Set reasoning effort to the decided tier's level when the harness exposes it (e.g., Workflow `agent(..., {effort: "max"})` — Large: `"max"`, Medium: `"high"`, Small: harness default); otherwise map the tier to a reasoning directive at the top of the agent prompt — Large: `ultrathink`, Medium: `think hard`, Small: no directive.
```

### S-5. Codex 불릿에 티어링 폴백 추가 (31행, 문장 끝 추가)

old (불릿 끝부분):
```
For Step 1-e, run the two lanes as two sequential single-purpose passes and synthesize afterward.
```
new:
```
For Step 1-e, run the two lanes as two sequential single-purpose passes and synthesize afterward. Tiering fallback: when reasoning effort cannot be controlled per pass, still decide and announce the tier, but run every 1-d/Step 3 pass at maximum reasoning regardless of tier — append `(fallback: max reasoning — no effort control)` to the Tier announcement line. A lower tier is never permission to run a weaker pass in such environments.
```

### S-6. `### Model & Effort Tiering` 하위 섹션 신설 (32행 불릿 직후, `## Step 1: Analyze & Plan` 직전에 삽입)

삽입 앵커: `- Subagents cannot interact with the user. All questions, interviews, and approvals happen in the orchestrator (main context) — never inside the planning or executor agents.` 라인 바로 뒤, 빈 줄 1개를 두고 아래 블록 전체를 verbatim 삽입 (블록 끝에도 빈 줄 1개 유지 후 `## Step 1`):

```markdown
### Model & Effort Tiering (모델·effort 티어링)

1-d Plan Authoring and Step 3 Execute scale their subagent's model and reasoning effort to the size of the job. Three tiers — **Large is the conservative default**; when in doubt, round up.

| Tier | Signals (판정 기준) | 1-d Plan Authoring | Step 3 Execute |
| --- | --- | --- | --- |
| **Large** (default) | 6+ files or architectural/cross-module change; any risk-keyword hit; >150 changed lines expected; or any signal ambiguous or unestimable | Fable 5 (`fable`); fallback `opus` — `effort: "max"` | Opus 4.8 (`opus`) — `effort: "max"` |
| **Medium** | 2–5 files; logic changes present but localized and low-risk; 31–150 changed lines expected; no risk-keyword hit | Opus (`opus`) — `effort: "high"` | Opus (`opus`) — `effort: "high"` |
| **Small** | single file; no new logic or algorithm (config/docs/typo/rename level); ≤30 changed lines expected; no risk-keyword hit | Sonnet (`sonnet`) — standard effort | Sonnet (`sonnet`) — standard effort |

**Classification checklist (판정 체크리스트)** — run by the orchestrator alone: deterministic, no subagent, and never an extra user question (the tier is announced, not asked). Score every signal, then take the **highest** tier any single signal produces:

1. **File count** — distinct files expected to change: 1 → Small; 2–5 → Medium; 6+ → Large; unestimable → Large
2. **Change size** — estimated changed lines in total: ≤30 → Small; 31–150 → Medium; >150 → Large; unestimable → Large
3. **Logic novelty** — none, config/docs/typo/rename level (e.g., changing a config value, fixing wording in docs, renaming without signature changes) → Small; modified or new logic that stays localized (e.g., adding an if-branch or a parameter inside an existing function, adjusting an existing query or output format) → Medium; new algorithms or architectural/cross-module changes (e.g., a new module, a changed algorithmic-complexity profile, a modified public interface or cross-module contract) → Large
4. **Risk keywords (위험 영역)** — any hit forces Large: security/auth (보안·인증·인가), payment/billing (결제·과금), migration or schema change (마이그레이션·스키마 변경), concurrency/locking/threading (동시성·락·스레드), secrets/credentials/API keys (시크릿·자격증명·API 키), destructive operations such as delete/drop/force-push/mass update (삭제·파괴적 작업)

**Round-up rule (상향 반올림)**: signals that conflict, straddle a boundary, or cannot be estimated always resolve to the higher tier. Small requires **all four** signals to land in the Small band.

**Tier decision timing (판정 시점):**

- **1-d tier** — decided in 1-c item 3, at the moment the user confirms the restatement. Never earlier: 1-a exploration signals alone must not set the tier — the 1-b interview and the restatement can still change scope. Inputs: 1-a analysis, 1-b interview answers, the confirmed sentence.
- **Step 3 tier** — decided at Step 3 item 1 from the approved plan's **Implementation Steps** (target-file count, per-step diff sketches/pseudocode for change size, risk keywords in the steps and Risks sections). Judged independently of the 1-d tier — the two may differ.
- **Re-spawns** — a Step 2 Comment-loop revision re-runs the checklist with the user feedback applied; the tier may rise but never falls within the same comment loop. The single 1-e revision cycle and Step 3 error-fix re-spawns reuse the already-decided tier.

**Tier announcement (등급 고지)** — print exactly one line immediately before spawning the phase agent, in this form:

`Tier: <Large|Medium|Small> — rationale: <파일 수>, <예상 변경 규모>, <로직/위험 근거> → <model>/<effort>`

Example: `Tier: Small — rationale: 단일 파일, 예상 12줄 변경, 문서 전용, 위험 키워드 없음 → Sonnet/standard`

**Invariant (불변 조건)**: tiering selects model and reasoning effort **only**. Every tier — including Small — runs the identical workflow: 1-e adversarial preview, the Step 2 user review with its hard gate, Step 3 evidence verification, and Step 4. No tier skips, weakens, or auto-approves any gate. 1-e stays fixed at Sonnet/standard for every tier; 1-c has no subagent and is not tiered.
```

(체크리스트 3번의 밴드별 예시는 판정 결정론성을 위한 것 — 예시 추가로 블록 행 수는 변하지 않음, 행 길이만 증가.)

### S-7. 1-c에 티어 판정 항목 삽입 (59행, 치환 1건 — 1줄이 2줄이 됨)

old (59행 전체, 유일 매치):
```
3. The confirmed sentence feeds the planning-agent input and the plan's Requirements Summary. Everything else from 1-b is passed to 1-d in full multi-section form — the restatement is the only place where one-line compression is the goal.
```
new (2개 목록 항목):
```
3. **Tier decision (티어 판정, 1-d)** — the moment the user selects **Yes, proceed to planning**, run the Model & Effort Tiering checklist (Agent & Model Policy) against the confirmed scope — inputs: 1-a analysis, 1-b interview answers, the confirmed sentence. Never decide earlier from 1-a exploration signals alone, and never ask the user an extra tier-confirmation question. Print the Tier announcement line, then proceed to item 4 — 1-d is spawned at this tier with the inputs item 4 describes.
4. The confirmed sentence feeds the planning-agent input and the plan's Requirements Summary. Everything else from 1-b is passed to 1-d in full multi-section form — the restatement is the only place where one-line compression is the goal.
```
항목 3의 끝이 항목 4로의 인계를 명시한다("then proceed to item 4") — 두 항목은 같은 스폰 이벤트의 티어 결정(3)과 입력 구성(4)이다. 61행 "Confirming the restatement authorizes **plan authoring (1-d) only**..." 문단은 무변경.

### S-8. Step 3에 티어 판정 항목 삽입 및 재번호 (130–139행, 치환 5건 + 자체 점검 1건)

치환 1 — old (130행):
```
1. Update plan status to `In Progress` in `docs\plan_history.md`
```
new (2개 항목):
```
1. **Tier decision (티어 판정, Step 3)** — before any status change, run the Model & Effort Tiering checklist (Agent & Model Policy) against the approved plan's **Implementation Steps**: count distinct target files, estimate total change size from each step's expected-diff sketch/pseudocode, and scan the Implementation Steps and Risks sections for risk keywords. Orchestrator-only, no subagent, no extra user question. Print the Tier announcement line before proceeding. This tier is judged independently of the 1-d tier — the two may differ.
2. Update plan status to `In Progress` in `docs\plan_history.md`
```

치환 2 — old (131행 앞부분): `2. If the native ` → new: `3. If the native ` (해당 행 나머지 무변경; old 문자열은 행 전체를 앵커로 사용해도 됨)

치환 3 — old (132행):
```
3. Spawn the executor agent per the Agent & Model Policy (Opus 4.8, max reasoning effort). Executor rules:
```
new:
```
4. Spawn the executor agent per the Agent & Model Policy at the tier decided in item 1 (Large default: Opus 4.8, max reasoning effort). Executor rules:
```

치환 4 — old (137행):
```
4. Parallelization: if the Implementation Steps contain independent groups with no file overlap, the orchestrator may spawn one executor agent per group (same model/effort) in parallel; otherwise use a single executor agent.
```
new:
```
5. Parallelization: if the Implementation Steps contain independent groups with no file overlap, the orchestrator may spawn one executor agent per group in parallel — every group uses the single tier decided in item 1 (the tier is judged once per Step 3 from the whole plan, never per group); otherwise use a single executor agent.
```

치환 5 — old (138행 앞부분): `5. The orchestrator verifies` → `6. The orchestrator verifies`, old (139행 앞부분): `6. On error:` → `7. On error:` (각 행 나머지 무변경).

**자체 점검 (필수 — 5건 치환 직후, S-9 진행 전)**: S-8은 5건의 개별 치환이므로 부분 적용(예: 치환 1·3만 적용) 시 번호 중복/누락이 생길 수 있다. 5건을 마친 즉시 T-11의 (b)·(c) 검사를 실행한다 — `1. **Tier decision (티어 판정, Step 3)**`와 `2. Update plan status`가 각 1회 존재하고, `## Step 3`~`## Step 4` 구간의 최상위 목록 선두 번호가 정확히 `1.`~`7.` 순서(중복·누락 없음)인지 확인. **이 검사를 통과해야 S-9로 진행**하며, 실패 시 누락된 치환을 재적용한 뒤 재검사한다.

### S-9. Exceptions 표 갱신 (153행 수정 + 신규 1행)

치환 — old (153행 전체):
```
| Environment lacks subagent model/effort control | Apply the fallback in Agent & Model Policy (separate max-reasoning pass in current context) |
```
new:
```
| Environment lacks subagent model/effort control | Apply the fallback in Agent & Model Policy (separate pass in current context; without per-pass effort control, always run at maximum reasoning regardless of tier) |
```

신규 행 삽입 — 위 치환된 행 바로 아래에 추가:
```
| Tier signals ambiguous, conflicting, or unestimable | Round up to the higher tier — Large is the default; never ask the user an extra tier-confirmation question |
```

### S-10. plan-context 교차 참조 정합성 수정 (`skills\plan-context\references\planning-workflow.md` 21행, 치환 1건)

old (부분 문자열, 파일 내 유일):
```
plan authoring is done by dh-dev's dedicated planning agent (Fable 5, max reasoning effort), not by this workflow.
```
new:
```
plan authoring is done by dh-dev's dedicated planning agent (model/effort per dh-dev's Model & Effort Tiering; Large default: Fable 5, max reasoning effort), not by this workflow.
```
이 파일의 다른 행은 일절 변경 금지 (git diff 단일 hunk 검증 — AC-10). 이 편집은 재진술 범위 밖 정합성 수정이므로 Step 2 제시 시 안내 문구(1번 섹션)에 따라 사용자에게 명시 고지된다.

**무변경 확인 대상**: 9–16행 흐름도(D-13), 27행 1-e 표 행, 36–48행(1-a/1-b), 61행, 63–105행(1-d/1-e), 107–126행(Step 2 전체), 141–144행(Step 4), `README.md`(24행에 모델 언급 없음 — 확인 완료).

## 4. Code Writing Guide (코드 작성 가이드)

- **500행 규칙**: SKILL.md는 500행 미만 유지. 이번 변경 후 예상 약 194행(158 + 삽입 33행 + 1-c 1행 + Step 3 1행 + Exceptions 1행) — 여유 충분, `references/` 신설 금지(D-8).
- **제목 병기 패턴**: 신설 소제목·볼드 라벨은 "영문 (한글 부제)" 형식 — `### Model & Effort Tiering (모델·effort 티어링)`, `**Tier decision (티어 판정, 1-d)**`, `**Round-up rule (상향 반올림)**` 등 S-6/S-7/S-8의 verbatim을 그대로 사용.
- **표 형식**: 기존과 동일한 GFM 파이프 표, 구분행 `| --- |`. 셀 내 줄바꿈 금지.
- **경로 표기**: 프로젝트 경로는 백슬래시(`docs\plan_history.md`), 스킬 내부 상대 참조는 슬래시 — 기존 관행 유지.
- **인코딩**: UTF-8(BOM 없음)로 저장. 한글 텍스트 포함 편집 후 반드시 UTF-8 read-back으로 mojibake 검사(U+FFFD, `占쏙옙`, `ï»¿` 등) — Verification Steps 4번.
- **금지**: 이모지 추가 금지(기존 15행 `✓`는 기존 문자이므로 무변경으로 보존), `§` 문자 금지. 이모지 판정 범위는 T-3에 정의(U+1F300–U+1FAFF, U+2600–U+27BF).
- **편집 방식**: 반드시 앵커 문자열 기반 exact-match Edit. 파일 전체 재작성(Write) 금지 — 무변경 영역의 바이트 보존이 DoD에 걸려 있음. 다건 치환 단계(S-8)는 명시된 자체 점검을 통과한 후에만 다음 단계로 진행.
- **문체**: 본문은 기존 파일과 동일하게 영어 서술 + 한글 괄호 병기, em-dash(`—`) 사용 패턴 유지.

## 5. Definition of Done (개발 완료조건)

| # | 조건 (전부 이진 판정*) |
| --- | --- |
| DoD-1 | `skills\dh-dev\SKILL.md`에 `### Model & Effort Tiering (모델·effort 티어링)` 제목이 정확히 1회 존재한다 |
| DoD-2 | 티어 표에 `| **Large** (default) |`, `| **Medium** |`, `| **Small** |`로 시작하는 데이터 행이 각 1개씩 존재하고, Large 행에 `` `fable` ``·`` `opus` ``·`"max"`, Medium 행에 `` `opus` ``·`"high"`, Small 행에 `` `sonnet` ``·`standard`가 포함된다 |
| DoD-3 | Agent & Model Policy 표의 1-d·Step 3 행이 각각 행별 앵커(`| Step 1-d Plan Authoring | dedicated planning agent | tiered — decided in 1-c`, `| Step 3 Execute | dedicated executor agent | tiered — decided at Step 3 item 1`)로 정확히 1회씩 매치되고, 1-e 행(`| Step 1-e Adversarial Preview |`)은 git diff상 무변경이다 |
| DoD-4 | `## Step 2: User Review`부터 `## Step 3` 직전까지 git diff hunk가 0건이다 (hard gate 문단 바이트 무변경) |
| DoD-5 | `grep -i haiku` 결과가 0건이다 |
| DoD-6 | 1-c 목록에 `3. **Tier decision (티어 판정, 1-d)**`와 `4. The confirmed sentence feeds`가 각 정확히 1회 존재하고 1-c 최상위 번호가 정확히 1–4 순서이며, Step 3 목록은 `1. **Tier decision (티어 판정, Step 3)**`·`2. Update plan status`가 각 정확히 1회 존재하고 최상위 번호가 정확히 1–7 순서(중복·누락 없음)이다 — T-11로 문자열·순번 단위 검증 |
| DoD-7 | 리터럴 `` `Tier: <Large|Medium|Small> — rationale: `` 이 정확히 1회, `Tier announcement`(대소문자 일치)가 4회 이상 존재한다 |
| DoD-8 | Invariant 문단이 존재한다: `including Small`과 `No tier skips` 문자열이 각각 1회 이상 존재 |
| DoD-9 | `regardless of tier`가 2회 이상 존재한다 (Codex 불릿 + Exceptions 행) |
| DoD-10 | `wc -l` 결과가 500 미만이다 (기대치 189–199) |
| DoD-11 | git diff 추가 라인에 `§` 및 이모지 문자가 0건이다 — 이모지 = U+1F300–U+1FAFF, U+2600–U+27BF(T-3에 정의; 신규 텍스트가 다수 사용하는 `→` U+2192·`—` U+2014는 이 범위 밖이므로 오탐 없음. 기존 `✓` U+2713은 범위 안이지만 무변경 행이므로 추가 라인에 나타나지 않음) |
| DoD-12 | `planning-workflow.md`의 git diff가 정확히 1개 hunk이며 그 안에 `Model & Effort Tiering`이 포함된다 |
| DoD-13 | UTF-8 read-back에서 한글 샘플(티어 판정, 등급 고지, 상향 반올림, 위험 영역)이 온전하고 U+FFFD·`占쏙옙`·`ï»¿` 매치가 0건이다 |
| DoD-14 | frontmatter description에 `tiered Large/Medium/Small`이 존재한다 |
| DoD-15 | 티어링 섹션에 Round-up rule 핵심 문구(`resolve to the higher tier`, `Small requires **all four**`)가 존재하고, 위험 키워드 6개 카테고리명(`security/auth`, `payment/billing`, `migration or schema change`, `concurrency/locking/threading`, `secrets/credentials/API keys`, `destructive operations`)이 각각 1회 이상 존재한다 (AC-5 대응) |
| DoD-16 | 18행 Effort 블록쿼트 carve-out 문장의 핵심 문구 `does not violate this rule`이 정확히 1회 존재한다 (D-14 대응) |
| DoD-17 | Re-spawns 불릿의 티어 단조 규칙 문구 `never falls within the same comment loop`이 정확히 1회 존재한다 (D-9 대응) |

\* 각주: DoD-13은 두 부분으로 구성된다 — mojibake 시그니처 스캔(U+FFFD·`占쏙옙`·`ï»¿` 검색 0건)은 기계적 이진 판정이지만, "한글 샘플이 온전히 렌더링됨" 확인은 T-9 read-back 출력을 **사람이 육안으로 확인하는 필수 수동 체크**다. 이 항목만 예외적으로 수동 확인을 포함하며, 생략할 수 없다(전역 인코딩 정책의 필수 검증 절차).

## 6. Adversarial Test Environment (적대적 테스트 환경)

실행 환경: 저장소 루트 `D:\001_Work\2026\017_claude\plugins\dh_skills`에서 Bash(Git Bash) grep/sed/diff/wc + UTF-8 read-back. dry-run은 문서만을 근거로 한 데스크 체크(수정된 SKILL.md 문구 인용 필수).

| ID | 테스트 | 절차 | 기대 결과 | 검증 DoD |
| --- | --- | --- | --- | --- |
| T-1 | 구조 grep 배터리 (전건 `grep -F` 고정 문자열, 대소문자 구분) | (1) `### Model & Effort Tiering` = 1. (2) 티어 3행 앵커 `| **Large** (default) |`·`| **Medium** |`·`| **Small** |` 각 = 1. (3) **행별 앵커** — `| Step 1-d Plan Authoring | dedicated planning agent | tiered — decided in 1-c` = 1, `| Step 3 Execute | dedicated executor agent | tiered — decided at Step 3 item 1` = 1, `tiered Large/Medium/Small` = 1(3행 치환 1), `tiered model/effort, Large default: Opus 4.8` = 1(3행 치환 2) — 집계 카운트 없이 치환 단위로 판별. (4) `Tier: <Large|Medium|Small>` = 1; `Tier announcement` ≥ 4. (5) `including Small` ≥ 1; `No tier skips` ≥ 1; `regardless of tier` ≥ 2. (6) 위험 키워드 6분류 개별 확인: `security/auth`·`payment/billing`·`migration or schema change`·`concurrency/locking/threading`·`secrets/credentials/API keys`·`destructive operations` 각 ≥ 1. (7) Round-up 문구: `resolve to the higher tier` = 1, `Small requires **all four**` = 1. (8) carve-out: `does not violate this rule` = 1. (9) 단조 규칙: `never falls within the same comment loop` = 1 | 전 항목 기대 수치 일치 | DoD-1,2,3,7,8,9,14,15,16,17 |
| T-2 | diff hunk 격리 | `git diff -U0 skills/dh-dev/SKILL.md`의 hunk가 다음 범위에만 존재: 3행(description), 18행, 26·28행, 30–31행, 32행 직후 삽입 블록, 1-c 항목 3–4, Step 3 목록, Exceptions 표. 특히 `## Step 2: User Review`~`## Step 3` 사이 hunk 0건, 27행(1-e 행)·88–105행(1-e 섹션) hunk 0건 | 예상 외 hunk 0건 | DoD-3,4 |
| T-3 | 네거티브 grep | `grep -ic haiku`(=0); `grep -c '§'`(=0); `git diff | grep '^+'`의 추가 라인에서 이모지 스캔 — 판정 범위는 **U+1F300–U+1FAFF 및 U+2600–U+27BF로 한정**(Python heredoc으로 코드포인트 검사). 명시적 제외: `→` U+2192(Arrows 블록)·`—` U+2014는 범위 밖이므로 신규 텍스트의 정상 사용이 오탐되지 않음; 기존 `✓` U+2713은 범위 안이지만 무변경 행이라 추가 라인에 등장하지 않음 | 전부 0건 | DoD-5,11 |
| T-4 | dry-run (a) 명백 Large — 위험 키워드 강제 | 가상 요청 "결제 검증 로직 리팩토링 — 4개 파일, 예상 120줄, 로직 수정": 체크리스트 적용 — 파일 4→Medium, 줄 수 120→Medium, 로직 수정→Medium, **결제(payment) 키워드 히트→Large**. worst-wins로 Large. 기대 고지: `Tier: Large — rationale: 4개 파일, 예상 120줄, 결제(위험 키워드) → Fable(fallback opus)/max` | 파일·줄 신호가 Medium이어도 위험 키워드 1건으로 Large 확정 — 근거 문구는 체크리스트 4번 "any hit forces Large" | DoD-2,15 + 체크리스트 규칙 |
| T-5 | dry-run (b) 명백 Small | 가상 요청 "README 오탈자 1건 수정": 파일 1→Small, 예상 2줄→Small, 로직 없음(문서)→Small, 위험 키워드 없음. 4개 신호 전부 Small 밴드 → Small. 기대 고지: `Tier: Small — rationale: 단일 파일, 예상 2줄 변경, 문서 전용, 위험 키워드 없음 → Sonnet/standard` | Small 판정 — "Small requires all four signals" 조건 충족 확인 | DoD-2 |
| T-6 | dry-run (c) 애매 → 상향 반올림 | (c-1) "로그 포맷 개선, 대상 파일 수 미정": 파일 수 unestimable→Large ⇒ 다른 신호와 무관하게 Large. 기대 고지: `Tier: Large — rationale: 파일 수 미정(unestimable), 예상 규모 미정, 로직 수정 → Fable(fallback opus)/max`. (c-2) "1개 파일, 예상 30~40줄 로직 수정": 줄 수가 30 경계에 걸침 → 31–150 밴드로 상향 ⇒ Medium(로직 수정도 Medium) — Small 불가. 기대 고지: `Tier: Medium — rationale: 1개 파일, 예상 35줄(30–40 경계 상향), 국소 로직 수정, 위험 키워드 없음 → Opus/high` | c-1은 Large, c-2는 Medium — 근거는 Round-up rule 문장("straddle a boundary ... resolve to the higher tier", "unestimable → Large"). 두 케이스 모두 기대 고지 문자열과 형식 일치 확인 | Round-up rule, Exceptions 신규 행 |
| T-7 | hard gate 우회 공격 (이전 계획 T-12 패턴) | 문서만 근거로 5개 공격 질문에 "불가"가 도출되는지 확인: (a) "Small 티어니 계획이 뻔한데 Step 2 승인 생략하고 실행하자" → Invariant "Every tier — including Small — runs ... Step 2 user review with its hard gate" + 무변경 hard gate 문단으로 차단 (b) "Small이면 1-e 프리뷰 생략 가능?" → Invariant "runs the identical workflow: 1-e adversarial preview"로 차단 (c) "1-a 탐색에서 이미 Small로 보이니 인터뷰 전에 Sonnet으로 1-d 스폰" → "Never decide earlier from 1-a exploration signals alone"(1-c 항목 3 + 판정 시점 불릿)으로 차단 (d) "Codex는 effort 제어가 안 되니 Small은 약하게 처리" → "run every 1-d/Step 3 pass at maximum reasoning regardless of tier"로 차단 (e) "유저에게 티어를 낮출지 물어보자" → "never ask the user an extra tier-confirmation question"(체크리스트 + Exceptions 행)으로 차단 | 5건 모두 명시 문구 인용으로 차단됨. 하나라도 문구가 없으면 해당 문구 보강 후 T-1부터 재실행 | DoD-4,8,9 |
| T-8 | 행 수 | `wc -l skills/dh-dev/SKILL.md` | < 500 (기대 189–199) | DoD-10 |
| T-9 | 한글 무결성 read-back | `PYTHONIOENCODING=utf-8` + heredoc으로 Python `open(encoding='utf-8')` 읽기, "티어 판정"·"등급 고지"·"상향 반올림"·"위험 영역" 포함 라인 출력 후 육안 확인; U+FFFD/`占쏙옙`/`ï»¿` 검색 0건 확인 | 한글 온전, mojibake 시그니처 0건 | DoD-13 |
| T-10 | 교차 파일 격리 | `git diff skills/plan-context/references/planning-workflow.md` — hunk 1개, 21행 포함, `Model & Effort Tiering` 문자열 포함. `git status --porcelain`에서 이번 작업으로 변경된 파일이 위 2개(+ 계획/이력 문서)뿐인지 확인 | 단일 hunk, 스코프 외 파일 무변경 | DoD-12 |
| T-11 | 목록 문자열·순번 완전성 (S-8 부분 적용 탐지) | (a) `grep -Fc '3. **Tier decision (티어 판정, 1-d)**'` = 1; `grep -Fc '4. The confirmed sentence feeds'` = 1. (b) `grep -Fc '1. **Tier decision (티어 판정, Step 3)**'` = 1; `grep -Fc '2. Update plan status'` = 1. (c) 순번 추출 — `sed -n '/^## Step 3/,/^## Step 4/p' skills/dh-dev/SKILL.md | grep -oE '^[0-9]+\.'` 출력이 정확히 `1.` `2.` `3.` `4.` `5.` `6.` `7.` 순서(중복·누락 없음, 하위 불릿은 들여쓰기라 `^` 앵커에 안 걸림); 같은 방식으로 `sed -n '/^### 1-c/,/^### 1-d/p'` 구간의 선두 번호가 정확히 `1.`–`4.` 순서 | 전 항목 일치 — S-8의 5건 치환 중 일부만 적용된 경우(예: 1·3만 적용) (b) 또는 (c)에서 즉시 탐지됨 | DoD-6 |
| T-12 | dry-run (d) Comment 루프 티어 단조 검사 | 가상 시나리오: 1-d 티어가 Medium으로 판정·고지된 계획이 Step 2 Comment로 (d-1) "범위를 파일 1개, 10줄로 축소해달라" 피드백 수신 — 체크리스트 재실행 시 신호는 Small 밴드지만, Re-spawns 불릿 "the tier may rise but never falls within the same comment loop"에 따라 **Medium 유지**(하락 금지). (d-2) "파일 7개로 확장해달라" 피드백 — 재실행 결과 Large로 **상승 허용**. 각 결과를 수정된 SKILL.md의 Re-spawns 불릿 인용과 함께 기록 | d-1은 Medium 유지, d-2는 Large 상승 — 두 방향 모두 명시 문구 인용으로 도출됨. 문구가 없으면 보강 후 T-1부터 재실행 | DoD-17 |

매핑 확인: DoD-1~17 각각이 T-1~T-12 중 최소 1개에 매핑됨 (5번 섹션 표의 대응 표기 + 본 표의 마지막 열). AC-5는 DoD-15→T-1로, DoD-6은 T-11로 각각 전용 검증 경로를 가진다.

주의: T-1~T-3·T-11의 grep은 **대소문자 구분**으로 실행할 것 — 기존 95행 `severity (HIGH/MEDIUM/LOW)`의 `MEDIUM`은 이번 변경과 무관한 기존 문자열이므로 `Medium` 카운트에 포함되면 안 된다(B-3). 고정 문자열 매치는 `grep -F`를 사용해 `|`·`*`·`<`가 정규식으로 해석되는 것을 방지한다.

## 7. Risks and Mitigations

| 위험 | 영향 | 완화 |
| --- | --- | --- |
| 티어링이 Step 2 hard gate 약화로 오독됨 ("Small이니 자동 진행") | 승인 없는 구현 착수 사고 | Invariant 문단 명문화(S-6) + Step 2 섹션 바이트 무변경(DoD-4) + 우회 공격 5종 데스크 체크(T-7) |
| S-8의 5건 치환 중 일부만 적용되어 Step 3 목록 번호가 중복/누락됨 | 목록 파손 — 항목 참조("item 1") 불일치, 워크플로우 오독 | S-8 자체 점검(치환 직후 T-11 (b)·(c) 실행, 통과 전 S-9 진행 금지) + T-11 순번 완전성 검사(DoD-6) |
| 1-c/Step 3 항목 재번호가 외부 문서의 항목 번호 참조를 깨뜨림 | 문서 간 참조 불일치 | 사전 조사 완료: `planning-workflow.md` 19–24행은 dh-dev 단계명만 참조하고 항목 번호는 참조하지 않음. 내부 상호참조("1-c item 3", "Step 3 item 1")는 S-6에서 새 번호 기준으로 작성 |
| `effort: "high"` 파라미터를 노출하지 않는 하네스 | Medium 티어 실행 불가 | S-4의 지시어 매핑(Medium→`think hard`)과 S-5의 "제어 불가 시 티어 무관 max" 폴백이 이중 안전망 |
| Comment 루프에서 범위 축소 피드백을 빌미로 티어를 내려 재플래닝 품질 저하 | 값싼 모델이 수정판 작성 | D-9 규칙: 같은 Comment 루프 내 티어는 상승만 허용, 하락 금지(S-6 Re-spawns 불릿) — DoD-17 grep + T-12 dry-run으로 규칙 존재와 작동을 모두 검증 |
| "로직 신규성" 신호의 판정이 실행마다 달라짐 | 같은 변경에 다른 티어 — 비결정성 | 체크리스트 3번에 밴드별 구체 예시 명시(S-6: config 값 변경/if-분기 추가/신규 모듈 등) + 애매하면 Round-up rule로 상향 |
| grep 검증이 기존 `MEDIUM`(95행)과 충돌해 오탐 | 검증 신뢰도 저하 | 모든 티어명 grep은 대소문자 구분 + 앵커를 `**Medium**` 형태로 지정(T-1), baseline B-3에 기록 |
| description YAML 문자열 파손 | 스킬 로드 실패 | S-1은 기존 따옴표 내부 부분 치환만 수행, 새 `"` 문자 0개. 검증 시 frontmatter 3행이 한 줄로 유지되는지 확인(Verification 2) |
| 문서 비대화로 500행 규칙 위반 | 저장소 컨벤션 위반 | 예상 194행(±5) — 여유 61% 확인(D-8), T-8이 기계 검증 |
| Codex에서 티어 고지 자체를 생략해 투명성 상실 | 판정 근거 불가시 | S-5가 "still decide and announce the tier"를 명시 — 폴백에서도 고지는 항상 수행, effort만 max로 상향 |

## 8. Verification Steps

구현(Step 3 executor) 완료 후 오케스트레이터가 순서대로 실행:

1. **구조 검증**: T-1 grep 배터리 전체 + T-11 문자열·순번 검사 실행, 결과 수치를 DoD-1,2,3,6,7,8,9,14,15,16,17 기대값과 대조. 하나라도 불일치 시 해당 S-단계 재적용 후 처음부터 재실행.
2. **diff 격리 검증**: `git diff -U0 skills/dh-dev/SKILL.md` 및 `git diff skills/plan-context/references/planning-workflow.md`로 T-2·T-10 수행 — Step 2 구간 hunk 0건, 1-e 행/섹션 hunk 0건, planning-workflow 단일 hunk. frontmatter 3행이 여전히 한 줄 YAML 문자열인지 확인.
3. **네거티브 검증**: T-3 (haiku 0건, `§` 0건, 추가 라인에서 U+1F300–U+1FAFF·U+2600–U+27BF 범위 이모지 0건) + T-8 (`wc -l` < 500).
4. **한글 무결성 검증 (필수, 생략 금지)**: T-9 — UTF-8 read-back으로 "티어 판정"·"등급 고지"·"상향 반올림"·"위험 영역" 라인을 실제 출력해 육안 확인하고 mojibake 시그니처 검색 0건을 확인 (DoD-13 각주의 수동 체크 부분). 손상 발견 시 성공 보고 금지 — 원인(인코딩) 진단 후 재작성·재검증.
5. **dry-run 데스크 체크**: T-4/T-5/T-6/T-7/T-12를 수정된 문서의 문구 인용(섹션명 + 인용문)과 함께 기록. T-6 c-2와 T-12는 기대 고지 문자열/판정 결과까지 대조. 5개 우회 공격(T-7) 중 1건이라도 명시 문구로 차단되지 않으면 해당 문구를 보강하고 1번부터 재검증.
6. **완료 보고**: DoD-1~17 체크리스트를 항목별 pass/fail + 실행한 명령·출력 증거와 함께 제출. 전 항목 green이 아니면 done 아님. Step 2 제시 시 안내 문구(plan-context 교차 참조 수정 포함 사실)가 실제로 사용자에게 전달되었는지 보고에 포함.

---

## 부록: 1-e Adversarial Plan Preview 검토 노트 (검토 노트)

contrarian·gap_hunter 두 레인이 초안을 검토해 13건(HIGH 4, MEDIUM 6, LOW 3)을 발견했고, 오케스트레이터의 로컬 구조 검사도 DoD-6 테스트 매핑 부재를 별도 확인(gap_hunter와 동일 사안으로 합류)했다. 1-d를 1회 재작성해 13건 전부를 반영했으며, 재작성 후 구조 검사(8개 섹션 존재, DoD 이진 판정 가능성, DoD↔테스트 매핑 완전성)를 재실행해 통과했다 — 미해결 HIGH 없음.

| 발견 ID | 심각도 | 조치 |
| --- | --- | --- |
| HIGH-1 | HIGH | 수치 경계·위험 키워드의 출처를 "사용자가 선택한 AskUserQuestion 옵션 설명"으로 명시적 인용 추가 |
| HIGH-2 | HIGH | 신규 T-11 추가(라벨 문자열 + 순번 완전성 검사, DoD-6 전담) + S-8에 자체 점검 절차 추가 |
| HIGH-3 | HIGH | T-1의 집계 카운트를 행별 앵커 검사로 교체(Step 3 행 누락이 은폐되지 않도록) |
| HIGH-4 | HIGH | DoD-15 신설 + T-1에 위험 카테고리 6종·round-up 문구 개별 grep 추가 |
| MEDIUM-1 | MEDIUM | Step 2 제시 시 plan-context 교차 참조 수정을 명시 고지하는 안내 문구 추가 |
| MEDIUM-2 | MEDIUM | D-14·DoD-16 신설 + carve-out 문구 전용 grep 추가 |
| MEDIUM-3 | MEDIUM | DoD-17 신설 + T-12 dry-run(양방향: 축소 시 유지, 확장 시 상승) 추가 |
| MEDIUM-4 | MEDIUM | 판정 체크리스트 "로직 신규성" 신호에 밴드별 구체 예시 추가 |
| MEDIUM-5 | MEDIUM | T-6 c-2에 Medium 등급의 기대 고지 문자열 명시 |
| MEDIUM-6 | MEDIUM | HIGH-2 조치에 통합(S-8 자체 점검) |
| LOW-1 | LOW | 1-c 항목 3→4 인계 문구 명시화 |
| LOW-2 | LOW | 이모지 판정 유니코드 범위 명시 + 기존 화살표/em-dash 오탐 배제 근거 기록 |
| LOW-3 | LOW | DoD 표에 각주 추가(DoD-13의 수동 체크 성격 명시) |

미해결 HIGH: 없음.
