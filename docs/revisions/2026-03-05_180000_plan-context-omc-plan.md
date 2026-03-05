# plan-context 스킬에 omc-plan 연동 추가

- **Date**: 2026-03-05 18:00:00
- **Status**: Completed

## Summary

plan-context 스킬에 Phase A-2 단계를 추가하여 oh-my-claudecode:plan 스킬이 있을 때 자동으로 위임하도록 개선.

## Rationale / Plan

계획 수립 시 omc-plan 스킬의 인터뷰/architect/consensus 워크플로우를 활용하면 더 체계적인 계획을 수립할 수 있다. plan-context가 컨텍스트를 수집한 후 omc-plan에 위임하고, 결과를 받아 Phase B에서 문서화하는 흐름으로 개선.

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills/plan-context/SKILL.md` | Modified | Phase A-2 (omc-plan 연동) 추가, description 업데이트 |

## Details

### `skills/plan-context/SKILL.md`

- **description**: `Delegate actual planning to oh-my-claudecode:plan (omc-plan) when available.` 문구 추가
- **Phase A-2 섹션 신규 추가** (Phase A와 Phase B 사이):
  - `oh-my-claudecode:plan` 스킬 가용 여부 확인
  - 가용 시: 수집한 컨텍스트를 전달하여 omc-plan으로 계획 수립 위임
  - 미가용 시: 기존 방식으로 일반 계획 수립 진행
