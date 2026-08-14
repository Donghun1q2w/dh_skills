**Date**: 2026-08-14 13:57:18
**Status**: Completed

---

# dh-dev 스킬 모델·effort 정책 및 워크플로우 개정 계획

## 1. Requirements Summary

`skills/dh-dev/SKILL.md`의 모델·effort 정책과 워크플로우를 개정해 — (1) Step 3 구현 에이전트 모델을 Sonnet으로 고정하되 effort는 등급대로 유지, (2) 공통 등급 판정에서 Large(최대 추론) 기준을 대폭 상향(10개 이상 파일 / 400줄 초과 / 아키텍처·모듈 간 계약 변경 / 위험 키워드)하고 기본값을 Medium으로 변경, (3) 1-b 초반에 개발 방향을 '단발성 / 간단한 / 심화'로 묻는 절차 신설, (4) 개발 방향이 올라갈수록(단발성 → 간단한 → 심화) 설정 외부화·재사용 인터페이스와 확장점·경계 예외 처리·테스트와 문서 커버리지 요구가 단계적으로 높아지도록 계획 필수 항목에 반영 — 하며, 성공 기준은 문서 내 관련 표·체크리스트·예외 표가 서로 모순 없이 갱신되고 기존 게이트(1-e 적대적 검증, Step 2 사용자 승인, 완료조건 증거 검증)는 모든 등급에서 그대로 유지되는 것이다.

> 용어 확정: 위 (4)의 "올라갈수록"은 **개발 방향**(단발성 → 간단한 → 심화)만을 가리키며 티어(Large/Medium/Small)와는 무관하다. 원 요청의 "심화로 갈수록"과 같은 뜻이고, S11에서 추가하는 직교성 문단과 정확히 일치한다. 티어는 범용성 요구 수준을 올리거나 내리지 않는다.

### 변경 대상

- 유일한 편집 파일: `D:\001_Work\2026\017_claude\plugins\dh_skills\skills\dh-dev\SKILL.md` (현행 195줄)
- 참조만: `skills\plan-context\SKILL.md`, `skills\plan-context\references\planning-workflow.md` (Interview Mode 메커니즘은 그대로 재사용하며 수정하지 않는다)

### 확정된 설계 결정 (실행자는 이 결정을 재검토하지 않는다)

| 항목 | 결정 |
| --- | --- |
| Step 3 모델 | 모든 등급에서 Sonnet 고정. 등급은 reasoning effort만 선택 |
| Step 3 effort | Large `max` / Medium `high` / Small standard |
| 1-d 모델 | Large: Fable 5(`fable`, 대체 `opus`), Medium(기본): Opus, Small: Sonnet |
| 등급 기본값 | Medium (기존 Large에서 변경) |
| Large 진입 조건 | 10개 이상 파일 / 400줄 초과 / 아키텍처·모듈 간 계약(공개 인터페이스) 변경 / 위험 키워드 적중 — 이 중 하나가 **적극적으로** 성립할 때만 |
| 애매·추정 불가 | Medium으로 반올림 (기존 "애매하면 Large" 규칙 폐기) |
| 개발 방향 분류 | 1-b 맨 처음 질문. 티어링과 직교(별개 축). 계획 문서의 범용성·확장성 요구 수준만 바꾼다 |
| 범용성 축 정의 위치 | 1-b에 표 한 벌만 두고 1-d에서 참조 (중복 정의 금지) |
| 등급 판정 체크리스트 정의 위치 | `### Model & Effort Tiering` 한 벌만 유지. 1-c 항목 3과 Step 3 항목 1은 참조만 |
| 게이트 | 1-e 적대적 검증, Step 2 승인 하드 게이트, Step 3 증거 검증, Step 4 — 모든 등급·모든 개발 방향에서 그대로 유지 |

---

## 2. Acceptance Criteria

변경 전 기준선(현행 문장)과 변경 후 상태를 쌍으로 명시한다. 모든 항목은 문자열 검색으로 확인 가능하다.

| 번호 | 변경 전 (현행 SKILL.md) | 변경 후 (합격 조건) |
| --- | --- | --- |
| AC-1 | 3행 frontmatter: `goal-driven implementation by a dedicated executor agent (tiered model/effort, Large default: Opus at max reasoning effort)` | frontmatter에 `Sonnet` 고정과 effort 티어링이 명시되고, `Large default: Opus at max reasoning effort` 문구가 사라짐 |
| AC-2 | 3행 frontmatter: `tiered Large/Medium/Small model/effort, Large default: Fable 5 at max reasoning effort` | `Medium default: Opus at high reasoning effort` 형태로 기본값이 Medium임이 드러남 |
| AC-3 | 3행 frontmatter: `context gathering with a one-sentence restate confirmation gate` | `development-direction classification (단발성/간단한/심화)`가 재진술 게이트 앞에 추가됨 |
| AC-4 | 15행 다이어그램: `1-b Context/Interview` | `1-b Direction + Context/Interview` |
| AC-5 | 28행 표: Step 3 Execute의 Model 칸 `tiered — decided at Step 3 item 1 ...; Large (default): Opus (\`opus\`)` | Model 칸이 `Sonnet (\`sonnet\`) — fixed for every tier`로 바뀌고, Reasoning effort 칸만 티어링을 설명 |
| AC-6 | 40행 표 Large 행 신호: `6+ files or architectural/cross-module change; any risk-keyword hit; >150 changed lines expected; or any signal ambiguous or unestimable` | `10+ files`, `>400 changed lines`, `architectural or cross-module contract (public interface) change`, `risk-keyword hit`만 남고 `any signal ambiguous or unestimable`이 Large 행에서 제거됨 |
| AC-7 | 41행 표 Medium 행: `2–5 files; ... 31–150 changed lines` | `2–9 files; ... 31–400 changed lines` 이며 행 제목이 `**Medium** (default)` |
| AC-8 | 40행 표 Large 행 제목 `**Large** (default)` | `**Large**` (기본값 표기 제거) |
| AC-9 | 42행 Small 행 | `single file`, `≤30 changed lines`, `no new logic`, `no risk-keyword hit` 그대로 유지 (변경 없음) |
| AC-10 | 46-47행 체크리스트: `6+ → Large; unestimable → Large`, `>150 → Large; unestimable → Large` | `10+ → Large; unestimable → Medium`, `>400 → Large; unestimable → Medium` |
| AC-11 | 48행 체크리스트 3항목: `new algorithms or architectural/cross-module changes ... → Large` | 새 알고리즘이 모듈 경계 안에 머물면 Medium, 아키텍처·공개 인터페이스·모듈 간 계약 변경만 Large로 재분류됨 |
| AC-12 | 51행: `**Round-up rule (상향 반올림)**: signals that conflict, straddle a boundary, or cannot be estimated always resolve to the higher tier.` | `**Tier resolution rule (등급 결정 규칙)**`로 대체되며 "Large는 적극적 근거 필요 / 추정 불가는 Medium"이 명시됨 |
| AC-13 | 36행: `Three tiers — **Large is the conservative default**; when in doubt, round up.` | `Medium is the default` 취지의 문장으로 대체되고 `when in doubt, round up` 문구가 문서 전체에서 사라짐 |
| AC-14 | 63행 예시 1개 (Small) | Small·Medium(1-d)·Medium(Step 3) 3개 예시가 있고, Step 3 예시의 모델이 `Sonnet`임 |
| AC-15 | 65행 Invariant | `Step 3 always runs on Sonnet; at Step 3 the tier selects reasoning effort only` 문장과 개발 방향 직교성 문장이 추가됨 |
| AC-16 | 76-81행 1-b | 1-b가 번호 매긴 3단계(방향 질문 → 맥락 요약 → 인터뷰)로 재구성되고, 개발 방향 3지선다와 범용성 4축 표가 존재 |
| AC-17 | 93행 1-c 항목 4 | 개발 방향이 1-d로 전달된다는 문구 포함 |
| AC-18 | 101-107행 1-d 입력 목록 | 개발 방향과 범용성 표 참조 불릿이 추가됨 (총 6개 → 7개 불릿) |
| AC-19 | 111-120행 Required Plan Sections | 8개 섹션 목록·번호·제목 그대로 유지되고, 3·5·6번 항목에 개발 방향 연동 문구가 추가되며 목록 뒤에 **Generality scaling** 문단이 추가됨 |
| AC-20 | 164행 Step 3 항목 1 | "모델은 Sonnet 고정, 등급은 effort만 선택" 문장 포함 |
| AC-21 | 167행 Step 3 항목 4 | `(Large default: Opus, max reasoning effort)` → `(model fixed: Sonnet; effort per the tier decided in item 1)` |
| AC-22 | 189행 예외 표 행 | 애매 신호 처리가 `Round up to the higher tier — Large is the default` → Medium 반올림으로 교체 |
| AC-23 | 예외 표 데이터 행 10개(현행 185-194행) | 애매 신호 행이 2행으로 분리되어 개발 방향 미선택 행이 추가되고, 데이터 행이 11개가 됨 |
| AC-24 | 전체 | `150`이라는 변경 규모 숫자와 `6+ files` 표현이 문서 어디에도 남지 않음 |
| AC-25 | 전체 | 1-e·Step 2 하드 게이트·Step 3 증거 검증·Step 4 관련 문장이 삭제·약화되지 않음 (해당 문단 문자열 그대로 존재) |
| AC-26 | 전체 | 등급 판정 체크리스트가 문서에 **한 번만** 정의됨 (1-c 항목 3, Step 3 항목 1은 참조 문구만) |
| AC-27 | 전체 | UTF-8 인코딩 유지, 한글 깨짐 문자(U+FFFD, `占쏙옙`, `ï»¿`) 0건, 금지 기호(U+00A7 섹션 기호) 0건 |
| AC-28 | 120행 뒤에는 아무 문단도 없음 | `Generality scaling (범용성 요구 반영)` 문단이 존재하고 `all 8 sections are mandatory for every direction` 문구를 포함 |
| AC-29 | 31행 말미: `A lower tier is never permission to run a weaker pass in such environments.` | 그 뒤에 `Model fallback:` 문장이 이어져 모델 선택 불가 환경 처리와 "등급은 여전히 effort만 결정" 취지가 명시됨 |
| AC-30 | 1-b에 개발 방향 개념 자체가 없음 | 1-b에 `Asked once per workflow run` 문단이 있어 1-c Missing scope 복귀 시 방향 재질문을 금지함 |
| AC-31 | 1-b는 불릿 2개 구조 | 1-b가 `**1. Development direction question`, `**2. Context summary.`, `**3. Interview.`의 번호 매긴 3단계 구조를 가짐 |

---

## 3. Implementation Steps (구현 지침)

편집은 위에서 아래 순서로 진행한다. 모든 편집은 `Edit` 도구의 정확 문자열 치환으로 수행하고, 파일 전체 재작성(`Write`)은 금지한다(인코딩 사고 방지).

### S1. frontmatter description 갱신 (3행)

**기존 (해당 부분만 발췌 — 3행의 일부)**

```
Chains explore (code analysis) → context gathering with a one-sentence restate confirmation gate → plan authoring by a dedicated planning agent (tiered Large/Medium/Small model/effort, Large default: Fable 5 at max reasoning effort — detailed implementation steps, Definition of Done, adversarial test environment) → adversarial plan preview (parallel contrarian/gap-hunter review lanes) → user review (approve/reject/comment loop) → goal-driven implementation by a dedicated executor agent (tiered model/effort, Large default: Opus at max reasoning effort) → revision-tracker (revision logging, code quality check, git commit).
```

**교체 문구**

```
Chains explore (code analysis) → context gathering that first classifies the development direction (단발성/간단한/심화) and then runs a one-sentence restate confirmation gate → plan authoring by a dedicated planning agent (tiered Large/Medium/Small model/effort, Medium default: Opus at high reasoning effort, Large: Fable 5 at max reasoning effort — detailed implementation steps, Definition of Done, adversarial test environment) → adversarial plan preview (parallel contrarian/gap-hunter review lanes) → user review (approve/reject/comment loop) → goal-driven implementation by a dedicated executor agent (Sonnet fixed for every tier; tiered reasoning effort — Large max / Medium high / Small standard) → revision-tracker (revision logging, code quality check, git commit).
```

3행의 나머지(앞의 `End-to-end orchestrator...` 문장과 뒤의 `Use when: ...`, `Triggers: ...`)는 손대지 않는다.

### S2. 개요 다이어그램 갱신 (15행)

**기존**

```
1-a Analyze → 1-b Context/Interview → 1-c Restate ✓ → 1-d Plan (agent) → 1-e Adversarial Preview
```

**교체 문구**

```
1-a Analyze → 1-b Direction + Context/Interview → 1-c Restate ✓ → 1-d Plan (agent) → 1-e Adversarial Preview
```

### S3. Effort 인용블록 보강 (18행)

**기존 (문장 말미)**

```
This governs the orchestrator context itself; the 1-d and Step 3 subagents run at the model/effort chosen by the Model & Effort Tiering policy below — a Medium/Small tier there does not violate this rule.
```

**교체 문구**

```
This governs the orchestrator context itself; the 1-d and Step 3 subagents run at the model/effort chosen by the Model & Effort Tiering policy below — a Medium/Small tier there does not violate this rule. Step 3 always runs on Sonnet by policy; that is a fixed model choice, not a reduction of this rule.
```

### S4. Agent & Model Policy 표 갱신 (26·28행)

**기존 26행**

```
| Step 1-d Plan Authoring | dedicated planning agent | tiered — decided in 1-c (see Model & Effort Tiering); Large (default): Fable 5 (`fable`), fallback: highest-reasoning model available (`opus`) | tiered — Large (default): maximum `effort: "max"` (ultracode-equivalent) |
```

**교체 문구**

```
| Step 1-d Plan Authoring | dedicated planning agent | tiered — decided in 1-c (see Model & Effort Tiering); Medium (default): Opus (`opus`); Large: Fable 5 (`fable`), fallback: highest-reasoning model available (`opus`); Small: Sonnet (`sonnet`) | tiered — Medium (default): `effort: "high"`; Large: maximum `effort: "max"` (ultracode-equivalent); Small: standard |
```

**기존 28행**

```
| Step 3 Execute | dedicated executor agent | tiered — decided at Step 3 item 1 (see Model & Effort Tiering); Large (default): Opus (`opus`) | tiered — Large (default): maximum `effort: "max"` (ultracode-equivalent) |
```

**교체 문구**

```
| Step 3 Execute | dedicated executor agent | **Sonnet (`sonnet`) — fixed for every tier**; fallback: default model. The tier does not select a model here | tiered — decided at Step 3 item 1 (see Model & Effort Tiering); Medium (default): `effort: "high"`; Large: maximum `effort: "max"` (ultracode-equivalent); Small: standard |
```

27행(1-e 행)과 30행·32행의 환경별 지침 불릿은 변경하지 않는다. 30행의 effort 매핑(`Large: "max"`, `Medium: "high"`, `Small: harness default` / `ultrathink`·`think hard`·directive 없음)은 새 정책과 이미 정합하므로 그대로 둔다. 31행은 아래 S4-2에서 한 문장만 덧붙인다.

### S4-2. 모델 통제 불가 환경 폴백 보강 (31행)

Step 3가 모든 등급 Sonnet 고정으로 바뀌면서, 모델을 고를 수 없는 환경에서 이 고정을 어떻게 다루는지가 비게 된다. 31행 불릿 **끝에** 한 문장을 덧붙인다(앞부분은 그대로 유지).

**기존 31행 말미**

```
A lower tier is never permission to run a weaker pass in such environments.
```

**교체 문구**

```
A lower tier is never permission to run a weaker pass in such environments. Model fallback: when the model cannot be selected per pass, proceed with whatever default model the environment provides — both the 1-d model tiers and the Step 3 Sonnet fixture are best-effort there. The tier is still decided and announced, and it still selects reasoning effort only.
```

예외 표의 `Environment lacks subagent model/effort control` 행은 이 불릿을 가리키고 있으므로 문구 변경 없이 그대로 둔다(참조가 자동으로 새 문장을 포함한다).

### S5. 티어링 절 도입 문장 교체 (36행)

**기존**

```
1-d Plan Authoring and Step 3 Execute scale their subagent's model and reasoning effort to the size of the job. Three tiers — **Large is the conservative default**; when in doubt, round up.
```

**교체 문구**

```
1-d Plan Authoring and Step 3 Execute scale their subagent's reasoning effort to the size of the job; 1-d additionally scales the model, while Step 3 always runs on Sonnet. Three tiers — **Medium is the default**. Large is reserved for jobs that positively meet a Large signal; ambiguous or unestimable signals resolve to Medium, not Large.
```

### S6. 등급 표 교체 (38-42행)

**기존 (표 전체)**

```
| Tier | Signals (판정 기준) | 1-d Plan Authoring | Step 3 Execute |
| --- | --- | --- | --- |
| **Large** (default) | 6+ files or architectural/cross-module change; any risk-keyword hit; >150 changed lines expected; or any signal ambiguous or unestimable | Fable 5 (`fable`); fallback `opus` — `effort: "max"` | Opus (`opus`) — `effort: "max"` |
| **Medium** | 2–5 files; logic changes present but localized and low-risk; 31–150 changed lines expected; no risk-keyword hit | Opus (`opus`) — `effort: "high"` | Opus (`opus`) — `effort: "high"` |
| **Small** | single file; no new logic or algorithm (config/docs/typo/rename level); ≤30 changed lines expected; no risk-keyword hit | Sonnet (`sonnet`) — standard effort | Sonnet (`sonnet`) — standard effort |
```

**교체 문구**

```
| Tier | Signals (판정 기준) | 1-d Plan Authoring | Step 3 Execute |
| --- | --- | --- | --- |
| **Large** | 10+ files; architectural change or a modified cross-module contract (public interface); >400 changed lines expected; or any risk-keyword hit — at least one signal must positively land here | Fable 5 (`fable`); fallback `opus` — `effort: "max"` | Sonnet (`sonnet`) — `effort: "max"` |
| **Medium** (default) | 2–9 files; logic changes present but contained inside existing module boundaries; 31–400 changed lines expected; no risk-keyword hit — also the landing tier whenever a signal is ambiguous or unestimable | Opus (`opus`) — `effort: "high"` | Sonnet (`sonnet`) — `effort: "high"` |
| **Small** | single file; no new logic or algorithm (config/docs/typo/rename level); ≤30 changed lines expected; no risk-keyword hit | Sonnet (`sonnet`) — standard effort | Sonnet (`sonnet`) — standard effort |
```

### S7. 판정 체크리스트 교체 (44-49행)

**기존 44행 도입 문장**

```
**Classification checklist (판정 체크리스트)** — run by the orchestrator alone: deterministic, no subagent, and never an extra user question (the tier is announced, not asked). Score every signal, then take the **highest** tier any single signal produces:
```

이 문장은 **그대로 유지**한다(수정 금지). 이어지는 1-4번 항목만 아래로 교체한다.

**기존 46-49행**

```
1. **File count** — distinct files expected to change: 1 → Small; 2–5 → Medium; 6+ → Large; unestimable → Large
2. **Change size** — estimated changed lines in total: ≤30 → Small; 31–150 → Medium; >150 → Large; unestimable → Large
3. **Logic novelty** — none, config/docs/typo/rename level (e.g., changing a config value, fixing wording in docs, renaming without signature changes) → Small; modified or new logic that stays localized (e.g., adding an if-branch or a parameter inside an existing function, adjusting an existing query or output format) → Medium; new algorithms or architectural/cross-module changes (e.g., a new module, a changed algorithmic-complexity profile, a modified public interface or cross-module contract) → Large
4. **Risk keywords (위험 영역)** — any hit forces Large: security/auth (보안·인증·인가), payment/billing (결제·과금), migration or schema change (마이그레이션·스키마 변경), concurrency/locking/threading (동시성·락·스레드), secrets/credentials/API keys (시크릿·자격증명·API 키), destructive operations such as delete/drop/force-push/mass update (삭제·파괴적 작업)
```

**교체 문구**

```
1. **File count** — distinct files expected to change: 1 → Small; 2–9 → Medium; 10+ → Large; unestimable → Medium
2. **Change size** — estimated changed lines in total: ≤30 → Small; 31–400 → Medium; >400 → Large; unestimable → Medium
3. **Logic novelty** — none, config/docs/typo/rename level (e.g., changing a config value, fixing wording in docs, renaming without signature changes) → Small; modified or new logic — including a new algorithm — that stays inside existing module boundaries and changes no public interface (e.g., adding an if-branch or a parameter inside an existing function, adjusting an existing query or output format, replacing an internal algorithm) → Medium; architectural change or a modified cross-module contract (e.g., a new module other modules must call, a changed public interface or exported signature, a changed data contract between modules) → Large
4. **Risk keywords (위험 영역)** — any hit forces Large: security/auth (보안·인증·인가), payment/billing (결제·과금), migration or schema change (마이그레이션·스키마 변경), concurrency/locking/threading (동시성·락·스레드), secrets/credentials/API keys (시크릿·자격증명·API 키), destructive operations such as delete/drop/force-push/mass update (삭제·파괴적 작업)
```

(4번 항목은 원문과 동일하다. 문맥 유지를 위해 함께 인용했을 뿐이므로 실제 치환 범위에서 빼도 무방하다.)

### S8. 반올림 규칙 교체 (51행)

**기존**

```
**Round-up rule (상향 반올림)**: signals that conflict, straddle a boundary, or cannot be estimated always resolve to the higher tier. Small requires **all four** signals to land in the Small band.
```

**교체 문구**

```
**Tier resolution rule (등급 결정 규칙)**:

- Take the **highest** tier any single signal produces.
- **Small** requires **all four** signals to land in the Small band.
- **Large requires positive evidence** — at least one signal must actually land in the Large band (10+ files, >400 changed lines, an architectural or cross-module contract change, or a risk-keyword hit). An impression that the job "might be big" is not evidence.
- **Ambiguous, conflicting-but-unestimable, or missing signals resolve to Medium**, never to Large. Anything that is neither clearly Small nor positively Large is Medium.
- Signals that straddle a boundary while still being estimable follow the numbers as written (e.g., 9 files → Medium, 10 files → Large; 400 lines → Medium, 401 lines → Large).
```

### S9. 판정 시점 불릿 갱신 (55-57행)

55행(1-d tier)과 57행(Re-spawns)은 변경하지 않는다. 56행만 교체한다.

**기존 56행**

```
- **Step 3 tier** — decided at Step 3 item 1 from the approved plan's **Implementation Steps** (target-file count, per-step diff sketches/pseudocode for change size, risk keywords in the steps and Risks sections). Judged independently of the 1-d tier — the two may differ.
```

**교체 문구**

```
- **Step 3 tier** — decided at Step 3 item 1 from the approved plan's **Implementation Steps** (target-file count, per-step diff sketches/pseudocode for change size, risk keywords in the steps and Risks sections). Judged independently of the 1-d tier — the two may differ. At Step 3 the tier selects **reasoning effort only**; the model is always Sonnet.
```

### S10. 등급 고지 예시 보강 (63행)

**기존**

```
Example: `Tier: Small — rationale: 단일 파일, 예상 12줄 변경, 문서 전용, 위험 키워드 없음 → Sonnet/standard`
```

**교체 문구**

```
Examples:

- 1-d, Small: `Tier: Small — rationale: 단일 파일, 예상 12줄 변경, 문서 전용, 위험 키워드 없음 → Sonnet/standard`
- 1-d, Medium (default): `Tier: Medium — rationale: 3개 파일, 예상 120줄 변경, 기존 모듈 내부 로직 수정, 위험 키워드 없음 → Opus/high`
- Step 3, Medium: `Tier: Medium — rationale: 3개 파일, 예상 120줄 변경, 기존 모듈 내부 로직 수정, 위험 키워드 없음 → Sonnet/high`
```

61행의 고지 형식 문자열(`Tier: <Large|Medium|Small> — rationale: ... → <model>/<effort>`)은 그대로 둔다.

### S11. 불변 조건 보강 (65행)

**기존**

```
**Invariant (불변 조건)**: tiering selects model and reasoning effort **only**. Every tier — including Small — runs the identical workflow: 1-e adversarial preview, the Step 2 user review with its hard gate, Step 3 evidence verification, and Step 4. No tier skips, weakens, or auto-approves any gate. 1-e stays fixed at Sonnet/standard for every tier; 1-c has no subagent and is not tiered.
```

**교체 문구**

```
**Invariant (불변 조건)**: tiering selects model and reasoning effort **only**. Every tier — including Small — runs the identical workflow: 1-e adversarial preview, the Step 2 user review with its hard gate, Step 3 evidence verification, and Step 4. No tier skips, weakens, or auto-approves any gate. 1-e stays fixed at Sonnet/standard for every tier; Step 3 stays fixed at Sonnet for every tier and varies only in effort; 1-c has no subagent and is not tiered.

**Orthogonality (직교성)**: the tier and the **development direction (개발 방향, 1-b)** are two independent axes and must never be conflated. The tier decides how much model and reasoning effort a subagent gets; the development direction decides how much generality, reuse, and coverage the plan's content demands. The direction never raises or lowers a tier, and the tier never changes the direction's requirements. A 심화 job can be Small, and a Large job can be 단발성 — these two examples are the logical consequence of the two axes being independent, not a new policy or a new exception.
```

### S12. 1-b 재구성 (76-81행)

**기존 (절 전체)**

```
### 1-b. Context Gathering

Run `plan-context` Phase A in the orchestrator to build the context summary:

- Incorporate context from `docs\revision_history.md`, `docs\plan_history.md`, wiki knowledge, and change history — git history when `.git` exists, file-system mtime when `.git` is absent (handled by plan-context Phase A)
- If requirements are vague, interview the user here per plan-context Interview Mode mechanics — one question at a time, ambiguity ledger (모호성 원장), Refine gate, fact-confirmation routing (see plan-context references/planning-workflow.md, Interview Mode) — the planning agent cannot ask the user anything
```

**교체 문구**

```
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
```

### S13. 1-c 갱신 (92-93행)

**기존 92행 (항목 3, 문장 일부)**

```
3. **Tier decision (티어 판정, 1-d)** — the moment the user selects **Yes, proceed to planning**, run the Model & Effort Tiering checklist (Agent & Model Policy) against the confirmed scope — inputs: 1-a analysis, 1-b interview answers, the confirmed sentence.
```

**교체 문구 (문장 일부만 치환)**

```
3. **Tier decision (티어 판정, 1-d)** — the moment the user selects **Yes, proceed to planning**, run the Model & Effort Tiering checklist (Agent & Model Policy — defined there once; do not restate it here) against the confirmed scope — inputs: 1-a analysis, 1-b interview answers, the confirmed sentence. The 1-b development direction is **not** an input to this decision.
```

같은 항목의 나머지 문장(`Never decide earlier ... at this tier with the inputs item 4 describes.`)은 그대로 둔다.

**기존 93행 (항목 4)**

```
4. The confirmed sentence feeds the planning-agent input and the plan's Requirements Summary. Everything else from 1-b is passed to 1-d in full multi-section form — the restatement is the only place where one-line compression is the goal.
```

**교체 문구**

```
4. The confirmed sentence feeds the planning-agent input and the plan's Requirements Summary. Everything else from 1-b — including the recorded **development direction (개발 방향)** — is passed to 1-d in full multi-section form; the restatement is the only place where one-line compression is the goal.
```

### S14. 1-d 입력 목록과 필수 계획 섹션 갱신 (101-120행)

**S14-1. 입력 목록에 불릿 추가.** 기존 106행 뒤(=107행 `- The Required Plan Sections below ...` 앞)에 다음 한 줄을 삽입한다.

```
- The **development direction (개발 방향)** recorded in 1-b (단발성 / 간단한 / 심화) and the matching column of the Generality requirements table in 1-b
```

**S14-2. Required Plan Sections 3번 항목 보강.**

기존 115행

```
3. **Implementation Steps (구현 지침)** — per step: target file/function references, exact change specification, interfaces/signatures, data structures, algorithm outline, error handling, edge cases. Include pseudocode or an expected-diff sketch for any non-trivial change.
```

교체 문구

```
3. **Implementation Steps (구현 지침)** — per step: target file/function references, exact change specification, interfaces/signatures, data structures, algorithm outline, error handling, edge cases. Include pseudocode or an expected-diff sketch for any non-trivial change. State the configuration-externalization and reuse-interface/extension-point decisions at the level the development direction requires (1-b, Generality requirements table).
```

**S14-3. 5번 항목 보강.**

기존 117행

```
5. **Definition of Done (개발 완료조건)** — binary-checkable conditions only; performance targets quantified ("fast" → "p99 < 200ms")
```

교체 문구

```
5. **Definition of Done (개발 완료조건)** — binary-checkable conditions only; performance targets quantified ("fast" → "p99 < 200ms"). Include the development direction's boundary/exception-handling and test/documentation coverage requirements as binary items.
```

**S14-4. 6번 항목 보강.**

기존 118행

```
6. **Adversarial Test Environment (적대적 테스트 환경)** — how to set up and run tests designed to break the implementation: boundary values, malformed/hostile inputs, failure injection, concurrency/scale cases where relevant, plus expected results. Every Definition of Done item maps to at least one test.
```

교체 문구

```
6. **Adversarial Test Environment (적대적 테스트 환경)** — how to set up and run tests designed to break the implementation: boundary values, malformed/hostile inputs, failure injection, concurrency/scale cases where relevant, plus expected results. Depth of the boundary and failure cases follows the development direction (1-b table), but the section itself is mandatory at every direction. Every Definition of Done item maps to at least one test.
```

**S14-5. 목록 뒤 문단 추가.** 8번 항목(120행 `8. **Verification Steps**`) 바로 뒤, `### 1-e.` 헤딩 앞에 빈 줄을 두고 다음 문단을 삽입한다.

```
**Generality scaling (범용성 요구 반영)** — the development direction from 1-b sets *how demanding* sections 3 through 6 are along the four axes (설정 외부화, 재사용 인터페이스·확장점, 경계·예외 처리, 테스트·문서 커버리지). It never changes *which* sections exist: all 8 sections are mandatory for every direction, including 단발성. A plan that omits a section because "the job is one-off" fails the 1-e structure check.
```

### S15. Step 3 항목 1·4 갱신 (164·167행)

**기존 164행 (항목 1, 문장 일부)**

```
1. **Tier decision (티어 판정, Step 3)** — before any status change, run the Model & Effort Tiering checklist (Agent & Model Policy) against the approved plan's **Implementation Steps**: count distinct target files, estimate total change size from each step's expected-diff sketch/pseudocode, and scan the Implementation Steps and Risks sections for risk keywords. Orchestrator-only, no subagent, no extra user question. Print the Tier announcement line before proceeding. This tier is judged independently of the 1-d tier — the two may differ.
```

**교체 문구**

```
1. **Tier decision (티어 판정, Step 3)** — before any status change, run the Model & Effort Tiering checklist (Agent & Model Policy — defined there once; do not restate it here) against the approved plan's **Implementation Steps**: count distinct target files, estimate total change size from each step's expected-diff sketch/pseudocode, and scan the Implementation Steps and Risks sections for risk keywords. Orchestrator-only, no subagent, no extra user question. Here the tier selects **reasoning effort only** — the executor model is always Sonnet. Print the Tier announcement line (with `Sonnet` as the model) before proceeding. This tier is judged independently of the 1-d tier — the two may differ.
```

**기존 167행 (항목 4 첫 문장)**

```
4. Spawn the executor agent per the Agent & Model Policy at the tier decided in item 1 (Large default: Opus, max reasoning effort). Executor rules:
```

**교체 문구**

```
4. Spawn the executor agent per the Agent & Model Policy (model fixed: Sonnet; reasoning effort per the tier decided in item 1 — Large `max`, Medium `high`, Small standard). Executor rules:
```

167행 이하의 실행자 규칙(목표 계약, 목표 추구 루프, 반환 항목)과 172-174행은 변경하지 않는다.

### S16. 예외 표 갱신 (189행 + 행 1개 추가)

**기존 189행**

```
| Tier signals ambiguous, conflicting, or unestimable | Round up to the higher tier — Large is the default; never ask the user an extra tier-confirmation question |
```

**교체 문구 (2행으로 대체)**

```
| Tier signals ambiguous or unestimable | Resolve to **Medium** (the default). Large requires at least one signal positively in the Large band; conflicting but estimable signals take the highest tier they produce. Never ask the user an extra tier-confirmation question |
| User declines or cannot choose a development direction | Default to **간단한 (simple)**, state the assumption in the plan's Requirements Summary, and continue. Never block the workflow on this question |
```

### 예상 diff 스케치

```
 skills/dh-dev/SKILL.md | ~110 +++++++++++++++-------------
 1 file changed
```

- 3행: 1행 치환 (frontmatter description)
- 15·18행: 각 1행 치환
- 26·28행: 표 2행 치환
- 31행: 1행 치환 (S4-2, 모델 폴백 문장 1개 덧붙임)
- 36행: 1행 치환
- 38-42행: 표 5행 치환
- 46-48행: 3행 치환
- 51행: 1행 → 7행 (규칙 목록화)
- 56행: 1행 치환
- 63행: 1행 → 5행
- 65행: 1행 → 3행 (직교성 문단 추가)
- 76-81행: 6행 → 약 37행 (1-b 재구성, "Asked once per workflow run" 문단 포함)
- 92·93행: 2행 치환
- 106행 뒤: 1행 삽입
- 115·117·118행: 3행 치환
- 120행 뒤: 2행 삽입
- 164·167행: 2행 치환
- 189행: 1행 → 2행

최종 파일 길이는 약 240-250행이 된다.

---

## 4. Code Writing Guide (코드 작성 가이드)

편집 대상은 코드가 아니라 스킬 문서이므로, 아래는 문서 작성 규칙이다.

### 문체·형식

- 본문은 **영어**, 핵심 용어는 `English (한국어)` 병기 — 기존 SKILL.md 문체를 그대로 따른다. 새로 만드는 소제목도 `**Tier resolution rule (등급 결정 규칙)**`처럼 같은 형식으로 쓴다.
- 표는 GitHub 마크다운 파이프 표, 구분행은 `| --- |` 형식. 기존 표의 열 개수와 정렬을 바꾸지 않는다.
- 모델·effort 표기는 백틱 코드 표기로 통일: `sonnet`, `opus`, `fable`, `effort: "max"`, `effort: "high"`, standard는 백틱 없이 standard.
- 강조는 `**...**`만 사용. 이모지·색상 표기 금지.
- 파일 경로는 기존 문서를 따라 백슬래시 표기(`docs\plans\`)를 유지한다.

### 용어 통일 (문서 내 1개 표기만 사용)

| 개념 | 사용할 표기 | 쓰지 말 것 |
| --- | --- | --- |
| 등급 판정 | tier / 등급 | grade, level, rank |
| 개발 방향 | development direction (개발 방향) | mode, category, type, 개발 등급 |
| 방향 3분류 | 단발성 (one-off) / 간단한 (simple) / 심화 (deep) | 임시/보통/고급 등 임의 번역 |
| 추론 강도 | reasoning effort | thinking budget, reasoning level |

### 피해야 할 패턴

- 등급 판정 기준(파일 수·줄 수·로직·위험 키워드)을 1-c나 Step 3에 **다시 적지 않는다**. 두 곳은 `Agent & Model Policy`를 참조만 한다.
- 범용성 4축 표를 1-d에 복제하지 않는다. 1-b 표를 참조만 한다.
- `when in doubt, round up`, `Large is the conservative default`, `6+ files`, `150` 같은 옛 기준 표현을 어디에도 남기지 않는다.
- Step 3 문맥에서 `Opus`를 실행 모델로 언급하지 않는다(1-d Medium 모델로서의 Opus 언급은 정상).
- 게이트 관련 문장(1-e, Step 2 하드 게이트, Step 3 증거 검증, Step 4)을 "가볍게", "생략 가능", "단발성일 때는" 같은 조건부 표현으로 바꾸지 않는다.
- 섹션 기호(U+00A7) 사용 금지.

### 인코딩

- 파일은 **UTF-8(BOM 없음)** 로 저장한다. `Edit` 도구의 정확 문자열 치환만 사용하고, PowerShell 리다이렉션(`>`, `Out-File`)으로 파일을 다시 쓰지 않는다.
- 검사·확인용으로 Python을 쓸 경우 `PYTHONIOENCODING=utf-8`을 붙이고 `open(..., encoding='utf-8')`을 명시한다.
- 한글 문자열(단발성·간단한·심화, 개발 방향, 등급 결정 규칙 등)을 넣은 뒤 반드시 읽어서 깨짐 여부를 눈으로 확인한다.

---

## 5. Definition of Done (개발 완료조건)

모두 예/아니오로 판정 가능하다. 각 항목은 6장 검사와 1:1 이상 대응한다.

| DoD | 조건 | 대응 검사 |
| --- | --- | --- |
| DoD-1 | `skills\dh-dev\SKILL.md` 외의 파일이 수정되지 않았다 (`git status --porcelain skills/`) | T-1 |
| DoD-2 | 문서 전체에 `when in doubt, round up`, `Large is the conservative default`, `Round-up rule`, `6+ files`, `2–5 files`, `31–150`, `>150` 문자열이 0건이다 | T-2 |
| DoD-3 | 티어 표 Large 행이 `10+ files`·`>400 changed lines`·`cross-module contract (public interface)`·`risk-keyword hit`를 포함하고 `(default)` 표기가 없다 | T-3 |
| DoD-4 | 티어 표 Medium 행 제목이 `**Medium** (default)`이고 `2–9 files`·`31–400 changed lines`를 포함한다 | T-3 |
| DoD-5 | 체크리스트 1번이 `2–9 → Medium; 10+ → Large; unestimable → Medium`, 2번이 `≤30 → Small; 31–400 → Medium; >400 → Large; unestimable → Medium`이다 | T-3 |
| DoD-6 | 체크리스트 3번에서 새 알고리즘이 Medium 밴드에, 아키텍처·공개 인터페이스 변경이 Large 밴드에 있다 | T-4 |
| DoD-7 | 티어 표 Step 3 열의 3개 행 모델이 모두 Sonnet이다 | T-5 |
| DoD-8 | Agent & Model Policy 표 Step 3 행의 Model 칸에 `Sonnet — fixed for every tier`가 있고 Opus가 없다 | T-5 |
| DoD-9 | Step 3 항목 1에 "reasoning effort only", 항목 4에 `model fixed: Sonnet`이 있다 | T-5 |
| DoD-10 | 1-b에 개발 방향 3지선다 표와 범용성 4축 표(4행)가 각각 정확히 1개씩 존재한다 | T-6, T-9 |
| DoD-11 | 범용성 4축 표의 4개 축이 설정 외부화·재사용 인터페이스와 확장점·경계 예외 처리·테스트와 문서 커버리지이며, 3개 열이 단발성/간단한/심화다 | T-6 |
| DoD-12 | 1-d 입력 목록에 개발 방향 불릿이 있고, Required Plan Sections 3·5·6번에 방향 연동 문구가 있으며, 8개 섹션 번호·제목이 원문 그대로다 | T-7 |
| DoD-13 | 직교성 문단(Orthogonality)이 존재하고 "the direction never raises or lowers a tier" 취지 문장을 포함한다 | T-8 |
| DoD-14 | 등급 판정 기준(파일 수 숫자, 줄 수 숫자)이 `### Model & Effort Tiering` 절 밖에는 등장하지 않는다 | T-9 |
| DoD-15 | 1-e 절, Step 2 Hard gate 문단, Step 3 항목 6, Step 4 문단이 현행과 문자열 단위로 동일하다(추가 문구 없이) | T-10 |
| DoD-16 | 예외 표 데이터 행이 11개(현행 10개 + 1)이며 애매 신호 행이 Medium 반올림을 지시하고 개발 방향 미선택 행이 존재한다 | T-11 |
| DoD-17 | frontmatter description에 `Sonnet fixed`와 `Medium default`와 `단발성/간단한/심화`가 모두 있고 `Large default`가 없다 | T-12 |
| DoD-18 | 파일이 UTF-8로 읽히고 U+FFFD·`占쏙옙`·`ï»¿`·U+00A7이 0건이며 한글이 정상 출력된다 | T-13 |
| DoD-19 | 마크다운 표가 모두 유효하다(각 표의 모든 행이 동일한 파이프 개수) | T-14 |
| DoD-20 | 경계 사례 6종(1파일·9파일·10파일·30줄·400줄·401줄)을 새 문서 규칙으로 판정했을 때 의도한 등급이 나온다 | T-15 |
| DoD-21 | `Generality scaling (범용성 요구 반영)` 문단이 Required Plan Sections 8번 뒤·`### 1-e.` 헤딩 앞에 존재하고 `all 8 sections are mandatory for every direction` 문구를 포함한다 | T-7 |
| DoD-22 | 등급 고지 예시가 3개이며 1-d Small은 `→ Sonnet/standard`, 1-d Medium은 `→ Opus/high`, Step 3 Medium은 `→ Sonnet/high`로 끝난다 | T-16 |
| DoD-23 | 1-b에 `Asked once per workflow run` 문단이 있고, 1-c Missing scope 복귀 시 방향 질문을 다시 하지 않는다는 문장을 포함한다 | T-17 |
| DoD-24 | 31행 폴백 불릿에 `Model fallback:` 문장이 있고 "등급은 여전히 reasoning effort만 결정" 취지를 포함한다 | T-18 |
| DoD-25 | 1-b가 `**1. Development direction question`, `**2. Context summary.`, `**3. Interview.` 3개 항목으로 번호 매겨져 있다 | T-6 |

---

## 6. Adversarial Test Environment (적대적 테스트 환경)

모든 검사는 편집 완료 후 저장소 루트 `D:\001_Work\2026\017_claude\plugins\dh_skills`에서 실행한다. 문서 산출물이므로 "깨뜨리기"는 모순·잔존·중복·깨짐 탐지를 뜻한다. 하나라도 실패하면 완료로 보고하지 않는다.

공통 변수: `$F = "D:\001_Work\2026\017_claude\plugins\dh_skills\skills\dh-dev\SKILL.md"`

### T-1. 변경 범위 검사 (DoD-1)

```powershell
git -C D:\001_Work\2026\017_claude\plugins\dh_skills status --porcelain -- skills/
```
기대: `M skills/dh-dev/SKILL.md` 한 줄만. 다른 파일이 나오면 실패.

### T-2. 옛 기준 잔존 검사 (DoD-2)

```powershell
Select-String -Path $F -Pattern 'when in doubt','conservative default','Round-up rule','6\+ files','2–5 files','31–150','>150','상향 반올림'
```
기대: 출력 0줄. 한 건이라도 나오면 실패(옛 기준이 새 기준과 모순됨).

### T-3. 새 기준 정착 검사 (DoD-3, DoD-4, DoD-5)

```powershell
Select-String -Path $F -Pattern '10\+ files','>400 changed lines','2–9 files','31–400','\*\*Medium\*\* \(default\)','unestimable → Medium'
```
기대: 6개 패턴 모두 최소 1건. 추가로 `Select-String -Path $F -Pattern '\*\*Large\*\* \(default\)'` 는 0건이어야 한다.

### T-4. 로직 밴드 재분류 검사 (DoD-6)

체크리스트 3번 항목 한 줄을 읽어 다음을 눈으로 확인한다.

- "new algorithm" 표현이 **Medium** 설명 안에 있다.
- "public interface" 또는 "cross-module contract" 표현이 **Large** 설명 안에 있다.

실패 조건: 새 알고리즘이 여전히 Large 밴드에 있음 → 상향 목표 위반.

### T-5. Step 3 모델 고정 검사 (DoD-7, DoD-8, DoD-9)

```powershell
Select-String -Path $F -Pattern 'Step 3','Execute' -Context 0,2
Select-String -Path $F -Pattern 'model fixed: Sonnet','fixed for every tier','reasoning effort only'
```
추가 반증 검사: 티어 표와 Agent & Model Policy 표의 Step 3 관련 칸에 Opus가 남아 있으면 실패. 다음 명령의 결과 줄을 하나씩 확인해 Opus가 1-d 문맥에만 등장하는지 본다.

```powershell
Select-String -Path $F -Pattern 'Opus|opus'
```
기대: 1-d 관련 행/문장에만 등장. Step 3 행·항목 1·항목 4에는 0건.

육안 판단에 의존하지 않도록, Step 3 관련 범위만 잘라 자동 검사한다. 대상은 (a) Agent & Model Policy 표의 `Step 3 Execute` 행, (b) 등급 표의 마지막 열(Step 3 Execute), (c) `## Step 3` 헤딩부터 `## Step 4` 직전까지의 절이다.

```bash
PYTHONIOENCODING=utf-8 python - << 'PYEOF'
p = r"D:\001_Work\2026\017_claude\plugins\dh_skills\skills\dh-dev\SKILL.md"
lines = open(p, encoding="utf-8").read().split("\n")

# (a) Agent & Model Policy 표의 Step 3 행
a = [l for l in lines if l.startswith("| Step 3 Execute |")]

# (b) 등급 표 3개 행의 마지막 열
tier = [l for l in lines if l.startswith("| **Large**") or l.startswith("| **Medium**") or l.startswith("| **Small**")]
b = [l.split("|")[-2] for l in tier]

# (c) Step 3 절 전체
s = next(i for i, l in enumerate(lines) if l.startswith("## Step 3"))
e = next(i for i, l in enumerate(lines) if i > s and l.startswith("## Step 4"))
c = lines[s:e]

for name, block in (("policy-row", a), ("tier-last-col", b), ("step3-section", c)):
    hits = [x for x in block if "Opus" in x or "opus" in x]
    print(name, "opus hits:", len(hits))
    for h in hits:
        print("   ", h.strip()[:120])
    print(name, "sonnet ok:", all("Sonnet" in x or "sonnet" in x for x in b) if name == "tier-last-col" else "-")
PYEOF
```
기대: 세 블록 모두 `opus hits: 0`, 등급 표 마지막 열 3개 모두 Sonnet 포함. 한 건이라도 나오면 Step 3 모델 고정이 미완이다.

### T-6. 개발 방향 절 존재·구조 검사 (DoD-10, DoD-11, DoD-25)

```powershell
Select-String -Path $F -Pattern '단발성','간단한','심화','설정 외부화','재사용 인터페이스','경계','테스트·문서 커버리지'
```
기대: 각 최소 1건. 방향 표(3지선다)와 4축 표가 각각 1개씩만 존재해야 하며, 두 표가 서로 다른 정의를 주장하지 않아야 한다.

이어서 1-b의 3단계 구조와 4축 표의 행 수를 자동으로 확인한다.

```bash
PYTHONIOENCODING=utf-8 python - << 'PYEOF'
p = r"D:\001_Work\2026\017_claude\plugins\dh_skills\skills\dh-dev\SKILL.md"
lines = open(p, encoding="utf-8").read().split("\n")
start = next(i for i, l in enumerate(lines) if l.startswith("### 1-b."))
end = next(i for i, l in enumerate(lines) if i > start and l.startswith("### 1-c."))
sec = lines[start:end]
for k in ["**1. Development direction question",
          "**2. Context summary.",
          "**3. Interview.",
          "Asked once per workflow run"]:
    print(k, "->", sum(k in l for l in sec))          # 각 1
axis = [l for l in sec if l.startswith("| **") and l.count("|") == 5]
print("axis rows:", len(axis))                        # 기대: 4
PYEOF
```
기대: 3단계 표지 각 1건, `Asked once per workflow run` 1건, 4축 표 데이터 행 4개. 하나라도 어긋나면 실패.

### T-7. 필수 계획 섹션·방향 연동 문구 검사 (DoD-12, DoD-21)

```powershell
Select-String -Path $F -Pattern '^\d\. \*\*(Requirements Summary|Acceptance Criteria|Implementation Steps|Code Writing Guide|Definition of Done|Adversarial Test Environment|Risks and Mitigations|Verification Steps)'
```
기대: 8줄, 번호 1-8이 순서대로. 하나라도 사라지거나 번호가 밀리면 실패.

이어서 1-d에 추가된 방향 연동 문구 4종과 Generality scaling 문단을 검사한다.

```powershell
Select-String -Path $F -Pattern 'development direction \(개발 방향\)' `
  ,'configuration-externalization' `
  ,'boundary/exception-handling and test/documentation' `
  ,'Depth of the boundary and failure cases follows' `
  ,'Generality scaling \(범용성 요구 반영\)' `
  ,'all 8 sections are mandatory for every direction'
```
기대: 6개 패턴 모두 최소 1건.

- `development direction (개발 방향)` → S14-1 입력 불릿 (1-c·S11에도 등장하므로 히트 수는 2건 이상일 수 있다. 1-d 입력 목록 안에 최소 1건 있는지 줄 번호로 확인)
- `configuration-externalization` → S14-2, Required Plan Sections 3번
- `boundary/exception-handling and test/documentation` → S14-3, 5번
- `Depth of the boundary and failure cases follows` → S14-4, 6번
- 나머지 2개 → S14-5 Generality scaling 문단

실패 조건: 하나라도 0건이면 DoD-12 또는 DoD-21 미달.

### T-8. 직교성 문장 검사 (DoD-13)

```powershell
Select-String -Path $F -Pattern 'Orthogonality|never raises or lowers a tier|not a tier'
```
기대: 최소 2건. 반대로 개발 방향이 등급을 바꾼다는 문장이 있으면 실패.

### T-9. 중복 정의 검사 (DoD-10, DoD-14)

줄 번호를 하드코딩하지 않고, `### Model & Effort Tiering` 헤딩부터 다음 `## Step 1` 헤딩 직전까지를 동적으로 잘라 그 밖에 숫자 기준이 있는지 본다.

```bash
PYTHONIOENCODING=utf-8 python - << 'PYEOF'
import re
p = r"D:\001_Work\2026\017_claude\plugins\dh_skills\skills\dh-dev\SKILL.md"
lines = open(p, encoding="utf-8").read().split("\n")
start = next(i for i, l in enumerate(lines) if l.startswith("### Model & Effort Tiering"))
end = next(i for i, l in enumerate(lines) if i > start and l.startswith("## Step 1"))
print("tiering section:", start + 1, "-", end)
pat = re.compile(r"10\+|31–400|31-400|>400|2–9|2-9|≤30")
outside = [(i + 1, l) for i, l in enumerate(lines) if pat.search(l) and not (start <= i < end)]
for n, l in outside:
    print("OUTSIDE", n, l[:120])
print("outside count:", len(outside))
PYEOF
```
기대: `outside count: 0`. 1-c 항목 3이나 Step 3 항목 1에 숫자 기준이 다시 등장하면 실패(중복 정의 → 향후 불일치 위험). 절이 길어져도 헤딩 기준으로 잘라내므로 줄 번호 변화에 영향받지 않는다.

### T-10. 게이트 보존 검사 (DoD-15)

```powershell
Select-String -Path $F -Pattern 'Hard gate','1-e Adversarial Plan Preview','structure check \(gate\)','An executor "done" claim'
git -C D:\001_Work\2026\017_claude\plugins\dh_skills diff -- skills/dh-dev/SKILL.md
```
diff에서 1-e 절 본문(122-139행 영역), Step 2 Hard gate 문단(151-158행 영역), Step 3 항목 6, Step 4 절이 변경 대상에 포함되지 않았음을 확인한다. 이 영역에 `-` 줄이 하나라도 있으면 실패.

### T-11. 예외 표 검사 (DoD-16)

```bash
PYTHONIOENCODING=utf-8 python - << 'PYEOF'
p = r"D:\001_Work\2026\017_claude\plugins\dh_skills\skills\dh-dev\SKILL.md"
lines = open(p, encoding="utf-8").read().split("\n")
i = next(k for k, l in enumerate(lines) if l.startswith("## Exceptions"))
rows = [l for l in lines[i:] if l.startswith("|")]
data = [r for r in rows[2:]]          # 머리글 1행 + 구분행 1행 제외
print("data rows:", len(data))        # 기대: 11
print("stale:", sum("Large is the default" in r for r in data))   # 기대: 0
print("medium:", sum("Resolve to **Medium**" in r for r in data)) # 기대: 1
print("direction:", sum("development direction" in r for r in data)) # 기대: 1
PYEOF
```
기대: 데이터 행 11개(현행 10개 + 애매 신호 행 분리로 1개 증가), `Large is the default` 0건, Medium 반올림 행 1건, 개발 방향 미선택 행 1건. 애매 신호 행에 `Large is the default` 문구가 남아 있으면 실패(본문의 Medium 기본값과 모순).

### T-12. frontmatter 정합 검사 (DoD-17)

```powershell
Select-String -Path $F -Pattern 'Sonnet fixed','Medium default','단발성/간단한/심화'
Select-String -Path $F -Pattern 'Large default'
```
기대: 앞 3개 모두 히트, `Large default`는 0건. 추가로 frontmatter 설명과 본문 표를 나란히 읽어 다음 3쌍이 일치하는지 확인한다.

- frontmatter의 1-d 기본 모델 ↔ 티어 표 Medium 행 1-d 칸
- frontmatter의 Step 3 모델 ↔ 티어 표 Step 3 열
- frontmatter의 방향 3분류 명칭 ↔ 1-b 방향 표 명칭

### T-13. 한국어 깨짐·금지문자 검사 (DoD-18)

```bash
PYTHONIOENCODING=utf-8 python - << 'PYEOF'
p = r"D:\001_Work\2026\017_claude\plugins\dh_skills\skills\dh-dev\SKILL.md"
s = open(p, encoding="utf-8").read()
bad = ["\ufffd", "占쏙옙", "\u00ef\u00bb\u00bf", "\u00a7"]
for b in bad:
    print(repr(b), "->", s.count(b))
for kw in ["단발성", "간단한", "심화", "개발 방향", "등급 결정 규칙", "범용성"]:
    print(kw, s.count(kw))
PYEOF
```
기대: 금지 문자 카운트 전부 0, 한국어 키워드 카운트 전부 1 이상, 그리고 출력된 한글이 화면에서 정상 한글로 보일 것. 하나라도 깨져 보이면 실패로 처리하고 인코딩을 바로잡아 다시 검사한다.

### T-14. 마크다운 표 유효성 검사 (DoD-19)

```bash
PYTHONIOENCODING=utf-8 python - << 'PYEOF'
p = r"D:\001_Work\2026\017_claude\plugins\dh_skills\skills\dh-dev\SKILL.md"
prev = None
for i, line in enumerate(open(p, encoding="utf-8"), 1):
    if line.strip().startswith("|"):
        n = line.count("|")
        if prev and prev[1] != n:
            print("PIPE MISMATCH", prev[0], "->", i, prev[1], n)
        prev = (i, n)
    else:
        prev = None
PYEOF
```
기대: 출력 0줄(같은 표 블록 안에서 파이프 개수가 달라지지 않음).

### T-15. 경계 사례 판정 검사 (DoD-20)

문서의 새 규칙만 읽고 다음 6개를 손으로 판정해 기대값과 대조한다. 하나라도 어긋나면 규칙 문구가 모호한 것이므로 문구를 고친다.

| 사례 | 기대 등급 | 근거가 되어야 할 문장 |
| --- | --- | --- |
| 9개 파일, 200줄, 국소 로직, 위험 없음 | Medium | 체크리스트 1번 `2–9 → Medium` |
| 10개 파일, 200줄, 국소 로직, 위험 없음 | Large | 체크리스트 1번 `10+ → Large` |
| 3개 파일, 정확히 400줄, 국소 로직 | Medium | 체크리스트 2번 `31–400 → Medium` |
| 3개 파일, 401줄, 국소 로직 | Large | 체크리스트 2번 `>400 → Large` |
| 파일 수 추정 불가, 규모 추정 불가, 위험 없음 | Medium | 등급 결정 규칙 "ambiguous ... resolve to Medium" |
| 단일 파일, 20줄, 문서 수정, 위험 없음 | Small | Small은 4개 신호 모두 Small 밴드 |

추가 반증 사례 2개:

- 단일 파일, 10줄이지만 인증 토큰 처리 변경 → **Large** (위험 키워드가 단독으로 Large를 만든다). 이 판정이 나오지 않으면 위험 키워드 규칙이 상향 개정에 묻힌 것이다.
- 2개 파일, 50줄, 개발 방향 심화 → **Medium** (심화는 등급을 올리지 않는다). Large가 나오면 직교성 문장이 무력한 것이다.

### T-16. 등급 고지 예시 검사 (DoD-22)

```bash
PYTHONIOENCODING=utf-8 python - << 'PYEOF'
p = r"D:\001_Work\2026\017_claude\plugins\dh_skills\skills\dh-dev\SKILL.md"
lines = open(p, encoding="utf-8").read().split("\n")
ex = [l for l in lines if l.strip().startswith("- ") and "Tier: " in l and "rationale" in l]
print("examples:", len(ex))                    # 기대: 3
for l in ex:
    print("  ", l.strip()[:160])
print("small:",  sum("Sonnet/standard" in l for l in ex))   # 기대: 1
print("medium:", sum("Opus/high" in l for l in ex))         # 기대: 1
print("step3:",  sum("Sonnet/high" in l for l in ex))       # 기대: 1
PYEOF
```
기대: 예시 3개, Small `Sonnet/standard` 1건, 1-d Medium `Opus/high` 1건, Step 3 Medium `Sonnet/high` 1건. Step 3 예시가 `Opus/high`로 남아 있으면 표와 모순이므로 실패.

### T-17. 개발 방향 재질문 금지 검사 (DoD-23)

```powershell
Select-String -Path $F -Pattern 'Asked once per workflow run','Missing scope\*\* return to 1-b','do not re-ask the direction question'
```
기대: 3개 패턴 모두 1건. 추가 육안 확인: 1-c 항목 2의 **Missing scope** 선택지 설명이 1-b 전체 재실행처럼 읽히지 않아야 한다(1-b 항목 3 인터뷰로 복귀). 방향 질문을 다시 하라는 문장이 어디에도 없어야 한다.

### T-18. 모델 통제 불가 환경 폴백 검사 (DoD-24)

```powershell
Select-String -Path $F -Pattern 'Model fallback:','best-effort','it still selects reasoning effort only'
```
기대: 3개 패턴 모두 1건이며 모두 31행 폴백 불릿 안에 있다. 이 문장이 없으면 Codex 계열 환경에서 "Sonnet 고정"을 지킬 수 없을 때의 처리가 비어 있는 것이다.

---

## 7. Risks and Mitigations

| 위험 | 영향 | 완화 |
| --- | --- | --- |
| 상향된 Large 기준 때문에 위험 키워드(보안·결제 등) 작업이 Medium으로 떨어짐 | 민감 작업이 낮은 추론으로 처리됨 | 체크리스트 4번 "any hit forces Large"를 그대로 보존하고, T-15 반증 사례로 검증 |
| 옛 숫자(150, 6+)가 일부만 교체되어 표와 체크리스트가 어긋남 | 판정 결과가 실행 시점에 갈림 | T-2/T-3을 반드시 함께 수행. 표·체크리스트·예외 표를 한 번의 작업에서 모두 고친다 |
| 개발 방향이 등급으로 오해되어 티어링을 흔듦 | 정책 취지 붕괴 | 직교성 문단(S11) + 1-c 항목 3의 "not an input" 문구 + T-8/T-15 반증 사례 |
| 단발성 방향이 게이트 축소 구실로 사용됨 | 검증 체계 약화 | 1-b 방향 설명에 "never skips any gate" 명시 + Generality scaling 문단 + T-10 |
| 범용성 4축 표가 1-d에도 복제되어 향후 불일치 | 유지보수 비용·모순 | 1-b에 1벌만 두고 1-d는 참조. T-9로 중복 검사 |
| Step 3 Sonnet 고정이 Large 작업 품질을 낮춤 | 대형 작업 실패율 상승 | Large에서 `effort: "max"` 유지 + Step 3 목표 추구 루프와 증거 검증(항목 6)이 그대로 남아 미달을 잡아냄. 이 위험은 사용자가 확인한 결정 사항이므로 설계 변경 없이 문서에 기록만 한다 |
| 파일 재작성으로 한글 인코딩 손상 | 문서 깨짐 | `Edit` 정확 치환만 사용, 리다이렉션 금지, T-13 필수 |
| AskUserQuestion 미지원 환경(Codex)에서 방향 질문이 흐름을 막음 | 워크플로우 정지 | 1-b에 평문 질문 + 턴 종료 지침, 무응답 시 간단한 기본값 규칙 명시 + 예외 표 신규 행 |

---

## 8. Verification Steps

1. 편집 전 기준선 확보: `git -C D:\001_Work\2026\017_claude\plugins\dh_skills diff --stat -- skills/dh-dev/SKILL.md` 로 현재 상태가 깨끗한지 확인하고, 파일 줄 수(195)를 기록한다.
2. S1, S2, S3, S4, S4-2, S5 … S16 순서로 `Edit` 치환을 적용한다. 각 치환은 인용된 기존 문자열과 정확히 일치해야 하며, 불일치로 실패하면 해당 줄을 다시 읽어 공백·유니코드 기호(`–`, `≤`, `→`)까지 맞춘다.
3. T-1 실행 — 변경 파일이 SKILL.md 하나인지 확인.
4. T-2, T-3, T-4 실행 — 옛 기준 제거와 새 기준 정착 확인.
5. T-5 실행 — Step 3 Sonnet 고정과 Opus 잔존 여부 확인.
6. T-6, T-7 실행 — 개발 방향 절과 8개 필수 섹션 확인.
7. T-8, T-9 실행 — 직교성과 중복 정의 없음 확인.
8. T-10 실행 — `git diff`로 게이트 문단이 손대지지 않았음을 확인.
9. T-11, T-12 실행 — 예외 표 데이터 행 11개와 frontmatter 정합 확인.
10. T-13, T-14 실행 — 한글 무결성과 표 유효성 확인. 한글 출력이 화면에서 정상 한글로 보이는지 육안 확인까지 마친다.
11. T-15 수행 — 8개 경계·반증 사례를 문서 문구만으로 판정해 기대값과 대조.
11-1. T-16, T-17, T-18 실행 — 등급 고지 예시 3개, 개발 방향 재질문 금지 문구, 모델 통제 불가 환경 폴백 문장 확인.
12. 최종 통독: `Read`로 파일 전체를 한 번 읽어 (a) 표와 본문 서술이 서로 같은 숫자를 말하는지, (b) 1-b → 1-c → 1-d로 개발 방향이 끊김 없이 전달되는지, (c) 등급 고지 예시의 모델·effort가 표와 일치하는지 확인한다.
13. DoD 1-25를 체크리스트로 만들어 각 항목에 대응 검사 결과(통과/실패)를 기록하고, 전부 통과했을 때만 완료로 보고한다. 실패가 있으면 해당 S 단계로 돌아가 수정 후 3번부터 다시 수행한다.

---

## 부록. 1-e 적대적 검증 반영 내역

11개 지적 사항을 모두 반영했다. 미반영 항목은 없다.

| 지적 | 반영 위치 |
| --- | --- |
| HIGH-1 예외 표 행수 산수 오류 | AC-23(10 → 11로 정정), DoD-16, T-11(동적 행수 계산 스크립트로 교체) |
| HIGH-2 Requirements Summary 문면 모순 | 1장 재진술 문장의 "등급이 올라갈수록" → "개발 방향이 올라갈수록(단발성 → 간단한 → 심화)", 바로 아래 용어 확정 인용 블록 추가 |
| HIGH-3 Generality scaling 검증 부재 | AC-28, DoD-21, T-7 후반부 패턴 2개 추가 |
| HIGH-4 DoD-12와 T-7 불일치 | T-7에 방향 연동 문구 4종 패턴 추가 및 각 패턴의 출처 단계 명시 |
| MEDIUM-5 T-9 줄 범위 하드코딩 | T-9를 헤딩 기준 동적 스캔 파이썬 스크립트로 교체 |
| MEDIUM-6 Missing scope 복귀 시 방향 재질문 | S12 교체 문구에 "Asked once per workflow run" 문단 추가, AC-30·DoD-23·T-17 신설 |
| MEDIUM-7 등급 고지 예시 검증 부재 | DoD-22, T-16 신설 |
| LOW-8 Opus 잔존 검사의 육안 의존 | T-5에 Step 3 범위 한정 자동 검사 스크립트 추가 |
| LOW-9 모델 통제 불가 환경 폴백 | S4-2 신설(31행 문장 보강), AC-29·DoD-24·T-18 추가. 예외 표 해당 행은 이 불릿을 참조만 하므로 문구 변경 불필요 |
| LOW-10 1-b 3단계 구조 자동 검사 | AC-31, DoD-25, T-6에 구조 확인 스크립트 추가 |
| LOW-11 직교성 예시의 성격 명시 | S11 교체 문구 말미에 "논리적 귀결이며 신규 정책이 아님" 한 줄 추가 |
