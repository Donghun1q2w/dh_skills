# plan-context 비-git 프로젝트 파이프라인 추가

- **Date**: 2026-05-14 12:00:00
- **Status**: Completed

## Summary

plan-context 스킬의 Phase A에 git 부재 시 동작하는 대체 컨텍스트 수집 파이프라인을 추가한다. 파일시스템 mtime 기반 최근 변경 탐색, `revision_history.md` 단독 의존 경로, Context Summary 템플릿의 조건부 분기를 도입하여 비-git 프로젝트에서도 일관된 플래닝 컨텍스트를 제공한다.

## Background

2026-04-01 작업으로 Phase A에 git 이력 탐색(Step 3)이 추가되었으나, `.git`이 없는 프로젝트에서는 단순히 단계를 건너뛰도록만 명시되어 있다. 이 경우 비-git 프로젝트는 `revision_history.md`/`plan_history.md`만으로 컨텍스트를 구성하게 되며, 두 파일이 없는 신규 프로젝트에서는 컨텍스트 수집이 사실상 비어버린다. dh-dev 오케스트레이터도 git 의존 표현을 그대로 노출하고 있어, 비-git 환경에서 일관된 플래닝 워크플로우를 보장하지 못한다.

## Proposal

1. **SKILL.md Phase A 진입부에 사전 체크 매트릭스 추가**
   - `.git`, `docs/revision_history.md`, `docs/plan_history.md` 존재 여부 조합별 동작 정의
2. **Phase A Step 3을 "Explore Change History"로 명칭 변경 후 분기**
   - 3-A. Git Repository (기존 내용 유지)
   - 3-B. Non-Git Project 신설 — mtime 기반 최근 변경 파일 수집, `docs/revisions/` 메타데이터 활용
3. **Context Summary 템플릿 조건부 분기**
   - "### Git History" → "### Change History (변경 이력)"로 통합
   - git 유무에 따른 출력 예시 양쪽 제시
4. **`references/templates.md`에 비-git 전용 Context Summary 템플릿 등록**
5. **`skills/dh-dev/SKILL.md` Step 1-b의 git 의존 표현 보강**

## Impact

| Area | Description |
|------|-------------|
| Files | `skills/plan-context/SKILL.md`, `skills/plan-context/references/templates.md`, `skills/dh-dev/SKILL.md` |
| Dependencies | 없음 |
| Risk | 낮음 — 기존 git 경로 동작은 보존, 분기만 추가 |

## Open Questions

없음.
