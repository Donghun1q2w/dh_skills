# plan-context Phase A에 Wiki 탐색 단계 통합

- **Date**: 2026-05-22 17:30:00
- **Plan**: [2026-05-22_173000_plan-context-wiki-integration.md](../plans/2026-05-22_173000_plan-context-wiki-integration.md)

## Summary

`plan-context` 스킬의 Phase A에 Step 5 "Search Wiki Knowledge Base"를 추가하고, Step 0 감지 매트릭스에 `docs\wiki\` 컬럼 및 분기 동작을 명시. Git/Non-Git Context Summary 템플릿(SKILL.md 본문 + references/templates.md) 양쪽에 `Wiki Knowledge (위키 지식)` 섹션 추가.

## Rationale / Plan

- dh-wiki 도입으로 영구 지식 베이스가 누적되었으나, 기존 plan-context Phase A는 wiki를 컨텍스트 소스로 인식하지 않음 → 계획 시 과거 결정·아키텍처·관습 누락 위험
- revision_history / plan_history / git history와 동등한 위상으로 wiki를 추가하는 것이 자연스러움
- 비-wiki 프로젝트 호환성: `docs\wiki\` 부재 시 Step 5가 자동 단락하도록 명시

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills/plan-context/SKILL.md` | modified | Step 0 매트릭스에 `docs\wiki\` 컬럼 추가, 신규 Step 5(Wiki Knowledge Base 탐색) 삽입, 기존 Step 5→6 재번호, Context Summary 템플릿(Git/Non-Git)에 Wiki Knowledge 섹션 추가 |
| `skills/plan-context/references/templates.md` | modified | Context Summary 템플릿(Git/Non-Git) 양쪽에 Wiki Knowledge 섹션 추가 — SKILL.md와 동기화 |
| `skills/plan-context/references/planning-workflow.md` | modified | 마크다운 포매터 부수 변경(테이블 헤더 정규화, HTML 엔티티 escape, 리스트 후 빈 줄 삽입). 내용 변경 없음 |
| `docs/plans/2026-05-22_173000_plan-context-wiki-integration.md` | added | 사후 기록 계획 문서 |
| `docs/plan_history.md` | modified | 신규 계획 항목 등록 (Status: Completed) |

## Details

### SKILL.md

- **Step 0 Detect Project State**: detection 표에 `Wiki knowledge base | docs\wiki\` 행 추가. Behavior matrix를 4컬럼에서 5컬럼으로 확장하여 wiki 분기 동작 명시 (`Step 5 skipped if docs\wiki\ missing` 등)
- **신규 Step 5 (Search Wiki Knowledge Base, 위키 지식 탐색)**:
  - 키워드 추출 (2-5개, 도메인 용어/컴포넌트명/기술 스택)
  - `dh_wiki_query({ query, tags?, category? })` 1차 호출, 필요 시 `dh_wiki_list()` 선행
  - 매칭 페이지에 대해 `dh_wiki_read({ page })`로 정독 → 아키텍처 결정/패턴/디버깅 노트/컨벤션/cross-reference 추출
  - 발견사항을 Context Summary의 Wiki Knowledge 섹션에 정리
- **Step 6 (구 Step 5)**: 기존 "Present Context Summary"를 6번으로 재번호
- **Context Summary 템플릿**: Git/Non-Git 양쪽 변형에 `### Wiki Knowledge (위키 지식)` 섹션 신설. 페이지 부재 시 생략 가능 명시

### references/templates.md

- SKILL.md와 동일한 Wiki Knowledge 섹션을 Git Variant / Non-Git Variant 템플릿 양쪽에 추가하여 단일 소스 동기화 유지

### references/planning-workflow.md

자동 포매터에 의한 부수 변경 (내용 동등):
- 테이블 헤더 구분선: `|------|----------|--------|` → `| --- | --- | --- |`
- HTML escape: `>=` → `&gt;=`, `<` → `&lt;` (RALPLAN-DR 옵션 개수, 성능 메트릭 예시)
- 리스트 항목 후 빈 줄 삽입 (Markdown lint 권장 형태)
- 파일 말미 newline 제거 (포매터 부작용)

## Verification

- 본 작업이 plan-context 적용 첫 사례 — 직전 dh-dev 워크플로에서 신규 Step 5가 정상 동작 (`docs/wiki/` 14페이지를 context로 인식, query 시도)
- `docs/wiki/`가 있는 본 프로젝트에서 Phase A Step 5가 실행됨
- 매트릭스 분기는 다른 프로젝트(wiki 부재) 시나리오에 대한 동작이므로 본 저장소에서는 직접 검증 불가 — 비-wiki 프로젝트 호환성은 다음 사용 시점에 확인 필요
