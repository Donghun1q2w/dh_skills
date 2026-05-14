# plan-context 스킬에 비-git 프로젝트 컨텍스트 파이프라인 추가

- **Date**: 2026-05-14 12:05:00
- **Author**: dh-dev (Claude)

## Rationale / Plan

기존 plan-context 스킬의 Phase A Step 3은 `.git` 부재 시 단순히 "skip"으로만 처리되어, 비-git 프로젝트에서는 컨텍스트 수집 절차가 사실상 비어있는 상태였다. revision_history/plan_history도 없는 신규 프로젝트("bootstrap state")에서는 더욱 빈약했다.

이번 변경으로 (1) Phase A 진입부에 프로젝트 상태 감지 매트릭스를 추가하고, (2) Step 3을 Git/Non-Git 분기로 재구성하며, (3) Context Summary 템플릿을 두 변형(+ Bootstrap)으로 제공하여 비-git 환경에서도 일관된 플래닝 워크플로우를 보장한다.

관련 계획: [2026-05-14_120000_plan-context-non-git-pipeline.md](../plans/2026-05-14_120000_plan-context-non-git-pipeline.md)

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills/plan-context/SKILL.md` | Modified | Phase A에 Step 0 (감지 매트릭스), Step 3 분기(3-A/3-B), Step 5 Context Summary 이중 템플릿 추가 |
| `skills/plan-context/references/templates.md` | Modified | Context Summary Templates 섹션(Git/Non-Git/Bootstrap) 신설 |
| `skills/dh-dev/SKILL.md` | Modified | Step 1-b의 git 의존 표현을 plan-context Phase A Step 3 위임 형태로 갱신 |
| `docs/plans/2026-05-14_120000_plan-context-non-git-pipeline.md` | Added | 본 변경에 대한 계획 문서 |
| `docs/plan_history.md` | Modified | 신규 계획 항목 추가 (In Progress) |

## Details

### `skills/plan-context/SKILL.md` (Modified)

- Phase A에 "### 0. Detect Project State" 추가 — `.git`, `revision_history.md`, `plan_history.md` 존재 여부 체크 표 및 동작 매트릭스 4행
- "### 3. Explore Git History" → "### 3. Explore Change History (변경 이력 탐색)"로 명칭 변경
- 하위에 "#### 3-A. Git Repository" (기존 git 명령 내용 유지) 와 "#### 3-B. Non-Git Project" 신설
- 3-B: `docs\revisions\` 활용, PowerShell/Bash mtime 명령, revision_history 교차참조, bootstrap 안내 포함
- "### 5. Present Context Summary"의 단일 코드블록을 **Git variant** / **Non-Git variant** 두 블록으로 분리
- Non-Git variant에 "No git tracking: change history is mtime-based and approximate" 노트 명시
- templates.md 참조 포인터 추가

### `skills/plan-context/references/templates.md` (Modified)

- 문서 상단에 "## Context Summary Templates" 섹션 신설
- 하위 3개 변형: Git Variant / Non-Git Variant / Bootstrap State
- Bootstrap state는 Non-Git variant 기반으로 "(none — first documented plan)" 플레이스홀더와 "git/revision-tracker 초기화 권장" 노트 사용

### `skills/dh-dev/SKILL.md` (Modified)

- Step 1-b 컨텍스트 소스 문구를 "git history (if `.git` exists)" → "change history — git history when `.git` exists, file-system mtime when `.git` is absent (handled by plan-context Phase A Step 3)"로 변경

### `docs/plans/2026-05-14_120000_plan-context-non-git-pipeline.md` (Added)

- 본 변경에 대한 계획 문서. Summary, Background, Proposal(5단계), Impact 테이블 포함. Status: In Progress

### `docs/plan_history.md` (Modified)

- 최상단에 신규 항목 prepend: "2026-05-14 12:00:00 — plan-context 비-git 프로젝트 파이프라인 추가" (Status: In Progress)
