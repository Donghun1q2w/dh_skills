# 2026-04-01 22:10:00 — plan-context Phase A에 git 이력 탐색 단계 추가

## Summary

plan-context 스킬의 Phase A (Pre-Planning Context Check)에 git 기반 이력 탐색 단계를 추가하여, git 저장소인 프로젝트에서 실시간 변경 컨텍스트를 수집할 수 있도록 개선.

## Rationale / Plan

- `docs\revision_history.md`는 수동 관리되어 누락 가능성이 있음
- `git log`와 `git diff`는 실시간으로 정확한 변경 이력을 제공
- revision_history와 git history를 교차 참조하면 누락된 변경 사항을 식별할 수 있음

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills/plan-context/SKILL.md` | Modified | Phase A Step 3 "Explore Git History" 추가, Step 번호 재조정 (3→4, 4→5), Context Summary 템플릿에 Git History 섹션 추가 |
| `skills/dh-dev/SKILL.md` | Modified | Step 1-b 컨텍스트 소스에 git history 참조 추가 |

## Details

### `skills/plan-context/SKILL.md`

- **Added**: Step 3 "Explore Git History (git 이력 탐색)" — `.git` 존재 시 조건부 실행, `git log --oneline -10`, `git diff --stat`, revision_history 교차 참조
- **Renumbered**: 기존 Step 3 "Search Similar Past Plans" → Step 4, 기존 Step 4 "Present Context Summary" → Step 5
- **Added**: Context Summary 템플릿에 "Git History (git 이력)" 섹션 — Recent commits, Unstaged changes, Untracked in revision_history 항목
