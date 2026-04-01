# plan-context Phase A에 git 이력 탐색 단계 추가

**Date**: 2026-04-01  
**Status**: Completed

## Summary

plan-context 스킬의 Phase A (Pre-Planning Context Check)에 git 기반 이력 탐색 단계를 추가하여, git 저장소인 프로젝트에서 `git log`와 `git diff`로 실시간 변경 컨텍스트를 수집할 수 있도록 개선.

## Background

- `docs\revision_history.md`는 수동 관리되어 커밋이 누락될 수 있음
- git은 프로젝트의 실제 변경 이력을 정확하게 제공하는 권위 있는 소스
- 두 소스를 교차 참조하면 계획 수립 시 더 완전한 컨텍스트를 확보할 수 있음

## Proposal

1. Phase A에 새 Step 3 "Explore Git History" 삽입 (`.git` 존재 시 조건부 실행)
   - `git log --oneline -10`: 최근 10개 커밋 확인
   - `git diff --stat`: 현재 unstaged 변경 확인
   - revision_history와 교차 참조: 누락된 커밋 식별
2. 기존 Step 3 → Step 4, Step 4 → Step 5로 번호 재조정
3. Context Summary 템플릿에 Git History 섹션 추가

## Impact

| File | Change |
|------|--------|
| `skills/plan-context/SKILL.md` | Step 추가, 번호 재조정, 템플릿 확장 |

### Risk

| Risk | Impact | Mitigation |
|------|--------|------------|
| git 없는 프로젝트에서 에러 | 스킬 실행 중단 | `.git` 존재 여부 사전 체크, 조건부 실행 |
| git log 출력이 너무 길면 컨텍스트 낭비 | 토큰 낭비 | `--oneline -10`으로 제한 |
