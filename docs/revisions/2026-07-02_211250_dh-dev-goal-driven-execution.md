# Revision: dh-dev 실행 단계를 goal 기반으로 전환

- **Date**: 2026-07-02 21:12:50
- **Slug**: dh-dev-goal-driven-execution

## Summary

dh-dev 스킬의 목표 명확화·최대 effort 기본값·ultrawork 제거·goal 기반 구현 전환.

## Rationale / Plan

사용자 요청에 따라 dh-dev 오케스트레이터를 개선:
1. 플랜 진행 시 목표(Goals)를 더 명확히 제시하도록 강제
2. 명시적 언급이 없으면 reasoning effort를 `max`로 설정하여 진행
3. OMC `ultrawork` 관련 참조 전면 삭제
4. 구현 단계에서 플랜의 명확한 목표를 네이티브 `/goal` 기능으로 활성화한 뒤 구현

## Changed Files

| File | Status | Description |
| --- | --- | --- |
| `skills/dh-dev/SKILL.md` | modified | frontmatter description·다이어그램 하단·Step 1-b·Step 3 개정 |

## Details

### `skills/dh-dev/SKILL.md`

- **frontmatter `description`**: `ultrawork (parallel implementation)` → `goal-driven implementation`
- **다이어그램 하단**: `> **Effort:**` 노트 추가 — 명시적 하향 요청이 없으면 Step 1 이전에 `max`로 상향하고 구현까지 유지
- **Step 1-b (Planning)**: 첫 bullet로 "플랜의 Goals를 명확·구체적으로 선(先) 제시" 요구 추가 — Step 3에 그대로 넘길 수 있을 만큼 self-contained
- **Step 3 (Execute)**: `/ultrawork` 호출 제거 → (2) 네이티브 `/goal` 기능 활성화 및 플랜 Goals 등록, (3) 목표 기준 Implementation Steps 순차 구현·effort `max` 유지, (4) 에러 처리로 재번호
