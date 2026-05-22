# plan-context Phase A에 Wiki 탐색 단계 통합

- **Date**: 2026-05-22 17:30:00
- **Status**: Completed

## Summary

`plan-context` 스킬의 Phase A에 신규 Step 5 "Search Wiki Knowledge Base"를 추가하여, `docs/wiki/` 디렉토리가 존재할 때 `dh-wiki` MCP 도구로 관련 지식을 사전 탐색하도록 한다. 기존 Step 5(Context Summary)는 Step 6으로 재번호되고, Git/Non-Git Context Summary 템플릿 양쪽에 `Wiki Knowledge (위키 지식)` 섹션이 추가된다.

## Background

- `dh-wiki` 도입으로 `docs/wiki/`에 영구 지식 베이스가 누적되기 시작했으나, 계획 작성 시 wiki 컨텐츠가 컨텍스트로 활용되지 않았음
- 과거 결정·아키텍처·관습이 wiki에 누적되면, 계획 단계에서 이를 무시할 경우 중복 결정이나 컨벤션 위반이 발생함
- Phase A의 다른 컨텍스트 소스(revision_history, plan_history, git history)와 동등한 위상으로 wiki를 추가하는 것이 자연스러움

## Proposal

### Step 1: Phase A 감지 매트릭스 확장

`SKILL.md`의 Step 0 detection 표에 `docs\wiki\` 열 추가. Behavior matrix는 다음과 같이 변경:

- 컬럼 추가: `docs\wiki\`
- 모든 행에 wiki 존재 여부 분기 명시 (`Step 5 skipped if docs\wiki\ missing`)

### Step 2: 신규 Step 5 (Search Wiki Knowledge Base) 추가

- `docs\wiki\` 존재 시에만 실행
- 워크플로: 키워드 추출(2-5개) → `dh_wiki_query` 호출 (필요 시 `dh_wiki_list` 선행) → 매칭 페이지 `dh_wiki_read`로 정독 → 발견 사항을 Context Summary의 Wiki Knowledge 섹션에 정리
- 카테고리 힌트: `architecture`, `decision`, `pattern`, `convention`

### Step 3: 기존 Step 5 → Step 6 재번호

"Present Context Summary"가 Step 6으로 이동.

### Step 4: Context Summary 템플릿에 Wiki Knowledge 섹션 추가

- `SKILL.md` 본문의 Git/Non-Git 양쪽 템플릿
- `references/templates.md`의 양쪽 템플릿 (SKILL.md와 동기화)

### Step 5: planning-workflow.md 자동 포매팅 정리

마크다운 포매터에 의한 부수 변경:
- 테이블 헤더 구분선 정규화 (`|----|----|` → `| --- | --- |`)
- HTML 엔티티 escape (`>=` → `&gt;=`, `<` → `&lt;`)
- 리스트 후 빈 줄 삽입
- 파일 말미 개행 제거 (의도치 않음, 표시만 남김)

내용 변경 없으므로 별도 검토는 생략.

## Impact

| Area | Description |
|------|-------------|
| Files | `skills/plan-context/SKILL.md`, `skills/plan-context/references/templates.md`, `skills/plan-context/references/planning-workflow.md` |
| Dependencies | `dh-wiki` MCP 서버 (이미 도입됨) |
| Risk | Low — wiki 디렉토리 부재 시 Step 5가 정상 단락하도록 명시되어 있어 비-wiki 프로젝트에 영향 없음 |

## Acceptance Criteria

1. `docs/wiki/`가 있는 프로젝트에서 plan-context 실행 시 wiki 탐색 단계가 수행됨
2. `docs/wiki/`가 없는 프로젝트에서 Step 5는 자동 단락
3. Context Summary 출력에 Wiki Knowledge 섹션이 (페이지 발견 시) 추가됨
4. Step 0 매트릭스가 `docs\wiki\` 컬럼을 포함

## Verification

- 본 계획 자체가 plan-context 적용 사례 — 이번 작업의 Phase A에서 wiki context를 활용함 (현재 14페이지)
- 변경된 SKILL.md/templates.md의 Step 5 본문이 dh_wiki_query/list/read 호출 방법을 명시함
