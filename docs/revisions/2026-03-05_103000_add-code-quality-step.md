# revision-tracker에 Code Quality Check 스텝 추가

- **Date**: 2026-03-05 10:30:00
- **Author**: Claude

## Rationale / Plan

revision-tracker의 Post-Modification 흐름에서, Git Commit 전에 코드 품질을 검토하는 단계가 없었음. 별도 리팩토링 로직을 구현하는 대신 기존 `/simplify`와 `/code-review` 스킬을 활용하는 조건부 스텝을 추가하여, 스킬 생태계 내 재사용성을 높임.

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills/revision-tracker/SKILL.md` | Modified | Step 5 "Code Quality Check" 추가, 기존 Step 5를 Step 6으로 재번호 |

## Details

### `skills/revision-tracker/SKILL.md` (Modified)

- Step 4 (Update Project Documentation)와 기존 Step 5 (Git Commit) 사이에 새 Step 5 "Code Quality Check (Optional)" 삽입
- Trigger/Skip 조건 명시: 소스코드 변경 시만 실행, docs-only 변경 시 스킵
- 실행 순서: `/simplify` 우선 → 변경 시 revision entry 업데이트 → `/code-review`는 복잡한 변경에만 선택적
- 기존 Git Commit 스텝을 Step 6으로 재번호
