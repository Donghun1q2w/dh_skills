# dh-dev Agent & Model Policy에 3단계 모델·effort 티어링 도입

- **Date**: 2026-07-23 14:12:26
- **Author**: Claude (dh-dev 오케스트레이터)

## Rationale / Plan

사용자가 dh-dev의 Plan Authoring(1-d)·Execute(Step 3) 서브에이전트가 항상 최고 등급 모델(Fable 5 / Opus 4.8)과 max effort로 고정되어 있는 점을 지적하고, "유저 요구사항 및 계획에 따라 plan/execute model과 effort를 탄력적으로 조정"하되 "보수적으로 높은 모델을 사용하되 실행 목표가 매우 작은 경우 작은 모델이나 effort로 진행 가능"하도록 개선을 요청.

계획: `docs\plans\2026-07-23_105547_dh-dev-model-effort-tiering.md` (Status: In Progress → 본 개정 완료 후 Completed로 갱신 예정).

플랜 단계에서 plan-context Interview Mode의 새 메커니즘(모호성 원장, Refine 게이트)을 실제로 적용해 사용자와 3라운드 상호작용 끝에 3단계(Large/Medium/Small) 체계를 확정했고, 1-c Restate Gate로 2회 재진술 확인을 거쳐 목표를 확정. Fable 5 전담 플래닝 에이전트가 계획을 작성한 뒤, 1-e Adversarial Plan Preview(contrarian+gap_hunter 병렬 레인)가 13건(HIGH 4, MEDIUM 6, LOW 3)을 발견 — 주로 DoD 항목과 실제 검증 테스트 간의 매핑 허점(예: 항목 재번호가 부분 적용돼도 기존 테스트가 못 잡는 문제, 위험 키워드 6종 중 일부 누락이 안 걸리는 문제). 1-d를 1회 재작성해 전부 반영(DoD-15~17, T-11/T-12 신규 테스트 추가) 후 구조 검사 재실행으로 미해결 HIGH 없음 확인.

Opus 4.8 전담 실행 에이전트가 구현 후 T-1~T-12 적대적 테스트로 17개 DoD 전부 자체 검증, 오케스트레이터가 hard gate 불변성·항목 순번 완전성·라인 수를 독립 재검증.

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills\dh-dev\SKILL.md` | Modified | Agent & Model Policy에 `### Model & Effort Tiering` 섹션 신설, 1-c/Step 3에 티어 판정 항목 삽입 및 재번호 (158→194행) |
| `skills\plan-context\references\planning-workflow.md` | Modified | Invocation Contexts의 dh-dev 플래닝 에이전트 모델 서술을 티어링 반영 문구로 1줄 수정 |

## Details

### `skills\dh-dev\SKILL.md` (Modified) — 158 → 194행

- frontmatter description에 "tiered Large/Medium/Small model/effort" 문구 추가 (1-d·Step 3 각각)
- Effort 블록쿼트(18행)에 carve-out 문장 추가: 오케스트레이터 자신의 "항상 max 유지" 규칙과 서브에이전트 티어링 정책이 모순되지 않음을 명문화
- Agent & Model Policy 표의 1-d·Step 3 행을 "tiered — decided in 1-c / at Step 3 item 1"로 갱신(모델·effort 값은 Large 기본값으로 표기), 1-e 행은 무변경
- Claude Code 불릿에 티어→effort/사고 지시어 매핑 추가(Large: max/`ultrathink`, Medium: high/`think hard`, Small: harness default/지시어 없음)
- Codex 불릿에 "effort 제어 불가 환경에서는 티어와 무관하게 항상 max reasoning" 폴백 추가
- 신규 `### Model & Effort Tiering (모델·effort 티어링)` 섹션: 3단계 표(판정 기준×1-d×Step 3), 4가지 판정 신호(파일 수/변경 규모/로직 신규성/위험 키워드) 체크리스트, worst-wins 상향 반올림 규칙, 판정 시점 규칙(1-d=1-c 확정 시점, Step 3=승인된 Implementation Steps 기반, 독립 판정), Comment 루프 티어 단조 규칙(상승만 허용), 등급 고지 포맷, 불변 조건(모든 티어가 동일한 워크플로우를 거침 — Step 2 hard gate·1-e 프리뷰 생략 불가)
- 1-c 목록에 항목 3 `**Tier decision (티어 판정, 1-d)**` 신설, 기존 항목이 4로 재번호
- Step 3 목록에 항목 1 `**Tier decision (티어 판정, Step 3)**` 신설, 기존 1-6이 2-7로 재번호
- Exceptions 표에 2행 추가(등급 신호 애매 시 상향 처리, 서브에이전트 effort 제어 불가 환경 폴백 갱신)
- Step 2 hard gate 문단은 바이트 단위 무변경

### `skills\plan-context\references\planning-workflow.md` (Modified) — 221행 (무변화, 1줄 in-place 치환)

- Invocation Contexts 21행의 "plan authoring is done by dh-dev's dedicated planning agent (Fable 5, max reasoning effort)"를 "(model/effort per dh-dev's Model & Effort Tiering; Large default: Fable 5, max reasoning effort)"로 갱신 — 재진술 확정 범위 밖의 정합성 수정(Step 2에서 사용자에게 별도 고지됨)

## 검증 요약

Opus 4.8 실행 에이전트가 T-1~T-12(구조 grep 9종, diff hunk 격리, 네거티브 검사, dry-run 4종, hard-gate 우회 공격 5건, 목록 순번 완전성, Comment 루프 단조성 양방향 검사, 인코딩 read-back)를 실행해 DoD-1~17 전부 PASS 보고. 오케스트레이터가 라인 수(194/221), hard gate 구간 diff hunk 부재, 1-c(1-4)·Step 3(1-7) 순번 완전성, plan-context 단일 hunk, haiku/§ 0건을 독립 재검증하여 일치 확인.
