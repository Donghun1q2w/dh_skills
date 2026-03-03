# plan-context 스킬 추가

- **Date**: 2026-03-03 23:05:00
- **Author**: agent

## Rationale / Plan

revision-tracker의 자매 스킬로, 파일 수정 이력 대신 계획 문서를 관리하는 스킬이 필요했다. plan mode에서 제안서/계획서/사양서/검토서 등을 작성할 때 프로젝트의 이전 컨텍스트를 먼저 탐색하고, 완료된 계획을 `docs\plans\`에 문서로 저장하며 `docs\plan_history.md`에 인덱싱하는 2단계 워크플로우를 구현한다.

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills/plan-context/SKILL.md` | Added | 스킬 본문 — Phase A(Pre-Planning Context Check) + Phase B(Post-Planning Logging) |
| `skills/plan-context/references/templates.md` | Added | Plan Document/History 템플릿 및 Status Values 정의 |
| `README.md` | Modified | 스킬 목록 테이블에 plan-context 행 추가, 디렉토리 트리에 plan-context/, docs/plans/, docs/plan_history.md 추가 |

## Details

### `skills/plan-context/SKILL.md` (Added)

- frontmatter: name=plan-context, description에 트리거 조건 명시
- Phase A: revision_history.md/plan_history.md 읽기, 키워드 유사 사례 탐색, 컨텍스트 요약 제시
- Phase B: 계획 문서 생성(docs\plans\), plan_history.md 업데이트, 디렉토리 생성, 프로젝트 문서 트리 업데이트
- revision-tracker와의 경계 테이블 포함

### `skills/plan-context/references/templates.md` (Added)

- Plan Document Template: 제목, Date, Status, Summary, Background, Proposal, Impact, Open Questions
- Plan History Template: 역시간순 인덱스 형식
- Status Values: Proposed, In Progress, Completed, Deferred, Superseded

### `README.md` (Modified)

- 스킬 목록 테이블에 `plan-context` 행 삽입 (revision-tracker 바로 위)
- 디렉토리 트리 skills/ 섹션에 plan-context/ 추가
- 디렉토리 트리 docs/ 섹션에 plan_history.md, plans/ 추가
