# Plan History

Chronological log of project plans and decisions.

---

## 2026-07-22 21:17:02 — dh-dev/plan-context 플래닝 단계 개선 — ouroboros interview 패턴 이식

[Detail](plans/2026-07-22_211702_dh-dev-planning-stage-ouroboros-interview.md) | Status: **Completed**

Summary: ouroboros `interview` 스킬(MCP 기반 Socratic 인터뷰)에서 착안한 4개 패턴을 MCP 서버 없이 스킬/서브에이전트 구조에 이식. `dh-dev`에 Restate 확인 게이트(1-c, 값비싼 플래닝 에이전트 호출 전 한 문장 목표 재확인)와 계획 초안 적대적 프리뷰 패널(1-e, contrarian+gap_hunter 병렬 레인, HIGH 발견 시 1회 재작성)을 추가. `plan-context` Interview Mode에는 모호성 원장(Scope/Constraints/Success Criteria/Non-goals/Verification), Refine 게이트(자유서술 답변 구조화), 신뢰도 기반 사실확인 라우팅(PATH 1a/1b + Dialectic Rhythm Guard)을 추가. 전부 Interview Mode 전용 범위로 한정, Direct/Consensus/Review 모드와 기존 Step 2 hard gate는 무변경.

---

## 2026-06-26 15:58:21 — Codex 스킬 호환성 보완

[Detail](plans/2026-06-26_155821_codex-skill-compatibility.md) | Status: **Completed**

Summary: 저장소의 Claude Code 중심 스킬/플러그인 구성을 Codex에서도 안정적으로 사용할 수 있도록 `dh-dev` 승인 게이트, `plan-context` 호출 규칙, Codex plugin manifest, MCP/hook 경로, skill validation 실패 항목, 설치본 동기화 절차를 보완한다. 특히 `dh-dev`는 계획 후 명시적 사용자 승인 없이는 구현 단계로 진입하지 않도록 강화한다.

---

## 2026-05-22 17:30:00 — plan-context Phase A에 Wiki 탐색 단계 통합

[Detail](plans/2026-05-22_173000_plan-context-wiki-integration.md) | Status: **Completed**

Summary: plan-context 스킬의 Phase A에 신규 Step 5 "Search Wiki Knowledge Base" 추가. `docs/wiki/` 존재 시 `dh_wiki_query/list/read`로 관련 지식을 사전 탐색하고 Context Summary의 Wiki Knowledge 섹션에 정리. Step 0 감지 매트릭스에 `docs\wiki\` 컬럼 추가, 기존 Step 5→6 재번호, Git/Non-Git 템플릿(SKILL.md + templates.md) 양쪽에 Wiki Knowledge 섹션 동기화.

---

## 2026-05-22 15:30:00 — dh-wiki Hook 이벤트 재구성 (FileChanged 미러링 도입)

[Detail](plans/2026-05-22_153000_dh-wiki-hooks-rework.md) | Status: **Completed**

Summary: dh-wiki 플러그인의 hook을 재편성. `SessionStart` → `UserPromptSubmit`으로 이관, `SessionEnd` 폐기, 신규 `FileChanged` hook으로 프로젝트 내 임의 `.md` 변경(생성·수정·삭제)을 `docs/wiki/`에 자동 미러링. 제외 대상: `docs/plans/**`, `docs/revisions/**`, `*history.md`, `docs/wiki/**`.

---

## 2026-05-14 12:00:00 — plan-context 비-git 프로젝트 파이프라인 추가

[Detail](plans/2026-05-14_120000_plan-context-non-git-pipeline.md) | Status: **Completed**

Summary: plan-context 스킬의 Phase A에 `.git` 부재 시 동작하는 대체 컨텍스트 수집 파이프라인을 추가. 파일시스템 mtime 기반 최근 변경 탐색, `revision_history.md` 단독 의존 경로, Context Summary 템플릿의 git/non-git 조건부 분기를 도입.

---

## 2026-04-20 14:00:00 — dh-wiki MCP 배포 정상화

[Detail](plans/2026-04-20_140000_fix-dh-wiki-mcp-deployment.md) | Status: **In Progress**

Summary: 배포 환경에서 dh-wiki MCP 서버 기동 실패 원인 2가지를 수정. (1) `node_modules/`가 Git에 추적되지 않아 플러그인 캐시에 미배포 → Git에 포함. (2) `.mcp.json`의 상대 경로를 `${CLAUDE_PLUGIN_ROOT}` 기반 절대 경로로 전환.

---

## 2026-04-15 15:00:00 — dh-wiki 독립 로컬 MCP 서버 구축

[Detail](plans/2026-04-15_150000_dh-wiki-local-mcp-server.md) | Status: **Completed**

Summary: OMC wiki 기능을 독립 로컬 MCP 서버로 포팅. `docs/wiki/` 경로 기반, `@modelcontextprotocol/sdk` stdio 서버로 7개 도구 제공. Hook 3개(SessionStart/PreCompact/SessionEnd) 내재화 포함.

---

## 2026-04-01 22:10:00 — plan-context Phase A에 git 이력 탐색 단계 추가

Detail | Status: **Completed**

Summary: plan-context 스킬의 Phase A에 git 기반 이력 탐색 단계(Step 3)를 추가. git 저장소인 프로젝트에서 `git log`, `git diff`를 활용하여 실시간 변경 컨텍스트를 수집하고, revision_history와 교차 참조하여 누락된 변경 사항을 식별.

---

## 2026-03-23 12:00:00 — E3D Standalone 스킬 추가

Detail | Status: **Completed**

Summary: AVEVA E3D Standalone 모드 C# 개발 가이드 스킬 신규 추가. 접속(Standalone.Start/Open) → PML 매크로 실행(Command) → 종료(Finish) 워크플로우 가이드, 9개 DLL 참조, 환경변수 구성 템플릿 포함.

---

## 2026-03-19 16:00:00 — skill-creator 가이드라인 기반 전체 스킬 재평가 및 개선

Detail | Status: **Completed**

Summary: skill-creator 가이드라인(&lt;500줄, progressive disclosure)을 기준으로 16개 스킬 재평가. hwpxskill(589→416줄), hwpxskill-math(558→317줄), excel(305→253줄) 3개 스킬의 상세 내용을 references 파일로 분리. README.md 정합성 수정(누락 3개 추가, 삭제 3개 제거).

---

## 2026-03-16 15:00:00 — dh-dev 스킬 추가 (코드 기능개선 오케스트레이터)

Detail | Status: **Completed**

Summary: 기존 코드의 기능 개선에 특화된 end-to-end 오케스트레이터 스킬 신규 추가. plan-context → 사용자 리뷰 → ultrawork → revision-tracker 4단계 워크플로우를 하나의 스킬로 자동화.

---

## 2026-03-05 16:30:00 — hwpxskill & hwpxskill-math Improvement

Detail | Status: **Completed**

Summary: Improve two HWPX skills to comply with skill-creator guidelines: split oversized SKILL.md (963 -&gt; \~600 lines), enhance descriptions in English, relocate README.md to docs/, remove test files, and document code duplication.

---

## 2026-03-05 10:00:00 — HWP 스킬 3종 개선

Detail | Status: **Completed**

Summary: hwp-analyze, hwp-fill, hwp-template 스킬의 description 확장, 공통 코드 references 분리, 에러 처리 추가, 템플릿 관리 스크립트 작성으로 skill-creator 가이드라인 준수 수준 향상.

---
