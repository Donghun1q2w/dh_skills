# plan-context 스킬에 omc-plan 워크플로우 내부 반영

- **Date**: 2026-03-05 18:30:00
- **Status**: Completed

## Summary

plan-context 스킬에서 omc-plan을 외부 호출하는 대신, 계획 수립 워크플로우(Interview/Direct/Consensus/Review)를 내부에 직접 반영. 모든 plan 파일은 `docs\plans\`에 저장 (`.omc\plans\` 사용 금지).

## Rationale / Plan

이전 커밋(7d82b54)에서는 omc-plan 스킬을 외부 호출하는 방식이었으나, 스킬 자체에 계획 수립 워크플로우를 내장하여 독립적으로 동작하도록 개선. `.omc\plans\` 대신 `docs\plans\`로 저장 경로 통일.

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills/plan-context/SKILL.md` | Modified | Phase A-2를 omc-plan 호출에서 내장 워크플로우로 교체, description 업데이트 |
| `skills/plan-context/references/planning-workflow.md` | Added | 4가지 모드(Interview/Direct/Consensus/Review) 상세 절차, RALPLAN-DR, 품질 기준 |

## Details

### `skills/plan-context/SKILL.md`

- **description**: omc-plan 위임 문구 제거, 4가지 모드 지원 및 트리거 키워드 추가
- **Phase A-2**: 모드 선택 테이블, 핵심 규칙(질문 분류, 코드 탐색 우선, 80%/90% 품질 기준), Plan Output Format 포함
- **References**: `planning-workflow.md` 링크 추가

### `skills/plan-context/references/planning-workflow.md` (신규)

- Interview Mode: 질문 분류표, 디자인 옵션 프레젠테이션 패턴
- Direct Mode: 즉시 계획 생성 절차
- Consensus Mode: RALPLAN-DR 8단계 (Planner -> Architect -> Critic 순차 실행, 최대 5회 반복, ADR 포함)
- Review Mode: Critic 평가 절차
- Quality Criteria: 최종 체크리스트
- Tool Usage: 에이전트/MCP 사용 가이드
