# Revision History

Chronological log of project modifications.

---

## 2026-04-15 15:00:00 — dh-wiki 독립 로컬 MCP 서버 구축

[Detail](revisions/2026-04-15_150000_add-dh-wiki-mcp-server.md)

- `skills/dh-wiki/SKILL.md` — 경로를 docs/wiki/로 변경, OMC 의존 제거
- `skills/dh-wiki/mcp-server/*` — 독립 MCP 서버 (7개 도구, 6개 파일 신규)
- `skills/dh-wiki/hooks/*` — Hook 3개 내재화 (session-start, pre-compact, session-end)
- `hooks/hooks.json` — 플러그인 루트 hook 등록 (신규)
- `.mcp.json` — MCP 서버 등록 (신규)

---

## 2026-04-01 22:10:00 — plan-context Phase A에 git 이력 탐색 단계 추가

[Detail](revisions/2026-04-01_221000_add-git-history-to-plan-context.md)

- `skills/plan-context/SKILL.md` — Phase A Step 3 "Explore Git History" 추가, Step 번호 재조정, Context Summary에 Git History 섹션 추가
- `skills/dh-dev/SKILL.md` — Step 1-b 컨텍스트 소스에 git history 참조 추가

---

## 2026-03-25 16:38:00 — E3D Launcher 스킬 추가 (프로세스 기반 E3D 모듈 실행)

[Detail](revisions/2026-03-25_163800_add-e3d-launcher-skill.md)

- `skills/e3d-launcher/SKILL.md` — E3D Launcher 스킬 정의 (모듈별 launch 패턴, 경로 규칙, config 구조)
- `skills/e3d-launcher/references/config-sample.json` — 프로젝트 인증/경로 config 샘플
- `skills/e3d-launcher/references/e3d-launcher-sample.py` — Python subprocess 런처 샘플
- `skills/e3d-launcher/references/e3d-launcher-sample.cs` — C# Process.Start 런처 샘플

---

## 2026-03-24 10:00:00 — E3D Standalone 스킬 계획 항목을 plan_history.md에 추가

[Detail](revisions/2026-03-24_100000_add-e3d-plan-entry.md)

- `docs/plan_history.md` — E3D Standalone 스킬 계획 항목 추가

---

## 2026-03-23 15:00:00 — e3d-standalone 스킬 테스트 및 런타임 DLL 로딩 패턴 추가

[Detail](revisions/2026-03-23_150000_e3d-standalone-test-and-fix.md)

- `skills/e3d-standalone/SKILL.md` — AssemblyResolve 필수 패턴 및 evarProj.bat 환경변수 로드 섹션 추가
- `skills/e3d-standalone/references/e3d-connection-template.cs` — RegisterAssemblyResolver 정적 메서드 추가
- `refcode/e3dstandalone/E3DStandaloneTest/` — ALP 프로젝트 대상 E3D Standalone 접속 테스트 앱 (Added)

---

## 2026-03-20 08:30:07 — NotebookLM 스킬 추가 및 csharp-coding-guide.skill 정리

[Detail](revisions/2026-03-20_083007_add-notebooklm-cleanup-csharp.md)

- `skills/notebooklm-skill/` — NotebookLM Research Assistant 스킬 추가 (Added)
- `csharp-coding-guide.skill` — 구 형식 바이너리 파일 삭제 (Deleted)

---

## 2026-03-19 16:00:00 — skill-creator 가이드라인 기반 전체 스킬 재평가 및 개선

[Detail](revisions/2026-03-19_160000_skill-creator-reevaluation.md)

- `skills/hwpxskill/SKILL.md` — 589→416줄 축소 (section0 가이드, 스타일 맵, Critical Rules를 references로 이동)
- `skills/hwpxskill/references/section0-guide.md` — section0.xml 작성 가이드 (Added)
- `skills/hwpxskill/references/style-id-map.md` — 5개 템플릿 스타일 ID 맵 (Added)
- `skills/hwpxskill/references/critical-rules.md` — Critical Rules 1~17 상세 (Added)
- `skills/hwpxskill-math/SKILL.md` — 558→317줄 축소 (스타일 맵, 시험지 형식, 단위 변환을 references로 이동)
- `skills/hwpxskill-math/references/style-id-map.md` — charPr/paraPr/tabPr/borderFill ID 맵 (Added)
- `skills/hwpxskill-math/references/exam-format.md` — 시험지 레이아웃, 수식 XML, 단위 변환 (Added)
- `skills/excel/SKILL.md` — 305→253줄 축소 (금융 모델 규칙을 references로 이동)
- `skills/excel/references/financial-model-rules.md` — 색상 코딩, 숫자 포맷, 수식 규칙 (Added)
- `README.md` — 누락 스킬 3개 추가, 삭제된 스킬 3개 제거, 트리 정합성 수정

---

## 2026-03-16 15:00:00 — dh-dev 스킬 추가 (코드 기능개선 오케스트레이터)

[Detail](revisions/2026-03-16_150000_add-dh-dev-skill.md)

- `skills/dh-dev/SKILL.md` — 코드 기능개선 오케스트레이터 스킬 본문 (4단계 워크플로우)
- `docs/plans/2026-03-16_150000_add-dh-dev-skill.md` — 기획 문서
- `docs/plan_history.md` — dh-dev 계획 항목 추가
- `README.md` — 스킬 테이블 + 디렉토리 트리 업데이트

---

## 2026-03-12 16:55:53 — Excel 스킬 추가 및 Windows/macOS 크로스플랫폼 최적화

[Detail](revisions/2026-03-12_165553_add-excel-skill.md)

- `skills/excel/SKILL.md` — Windows/macOS 크로스플랫폼 Excel 스킬 (UTF-8 우선, LibreOffice 제거)

---

## 2026-03-05 18:30:00 — plan-context 스킬에 omc-plan 워크플로우 내부 반영

[Detail](revisions/2026-03-05_183000_plan-context-embed-omc-plan.md)

- `skills/plan-context/SKILL.md` — Phase A-2를 내장 워크플로우로 교체 (4가지 모드 지원)
- `skills/plan-context/references/planning-workflow.md` — 상세 절차 참조 파일 (Added)

---

## 2026-03-05 18:00:00 — plan-context 스킬에 omc-plan 연동 추가

[Detail](revisions/2026-03-05_180000_plan-context-omc-plan.md)

- `skills/plan-context/SKILL.md` — Phase A-2 (omc-plan 연동) 추가, description 업데이트

---

## 2026-03-05 16:30:00 — hwpxskill & hwpxskill-math skill-creator compliance improvement

[Detail](revisions/2026-03-05_163000_hwpxskill-improvement.md)

- `skills/hwpxskill-math/SKILL.md` — Split equation syntax/graph shapes to references, English description (963->558 lines)
- `skills/hwpxskill-math/references/equation-syntax.md` — Hancom equation script syntax reference (Added)
- `skills/hwpxskill-math/references/graph-shapes.md` — Graph shape type JSON spec reference (Added)
- `skills/hwpxskill-math/scripts/hwpx_utils.py` — Add intentional duplication documentation
- `skills/hwpxskill-math/scripts/test_refactor.py` — Removed test file from skill package (Deleted)
- `skills/hwpxskill/SKILL.md` — English description with trigger keywords
- `skills/hwpxskill/README.md` — Moved to `docs/hwpxskill-readme.md` (Deleted)
- `docs/hwpxskill-readme.md` — Relocated README (Added)

---

## 2026-03-03 23:05:00 — plan-context 스킬 추가

[Detail](revisions/2026-03-03_230500_add-plan-context-skill.md)

- `skills/plan-context/SKILL.md` — 스킬 본문 (Phase A: 컨텍스트 탐색, Phase B: 계획 문서 저장)
- `skills/plan-context/references/templates.md` — Plan Document/History 템플릿 및 Status Values
- `README.md` — 스킬 테이블 행 추가 + 디렉토리 트리 업데이트

---

## 2026-03-03 22:36:21 — revision-tracker Section 5 "Git Commit" 기능 확장

[Detail](revisions/2026-03-03_223621_extend-git-commit-flow.md)

- `skills/revision-tracker/SKILL.md` — Section 5를 3단계 인터랙티브 커밋 흐름으로 교체 (제안 → 사용자 확인 → 실행/건너뛰기)
## 2026-03-05 10:30:00 — revision-tracker에 Code Quality Check 스텝 추가

[Detail](revisions/2026-03-05_103000_add-code-quality-step.md)

- `skills/revision-tracker/SKILL.md` — Step 5 "Code Quality Check" 추가, Git Commit을 Step 6으로 재번호

---

## 2026-03-05 10:00:00 — HWP 스킬 3종 개선

[Detail](revisions/2026-03-05_100000_hwp-skills-improvement.md)

- `skills/hwp-analyze/SKILL.md` — description 확장, 간결화, 에러 처리 추가
- `skills/hwp-analyze/references/hwpx-structure.md` — HWPX XML 구조 공통 참조 문서 (신규)
- `skills/hwp-fill/SKILL.md` — description 확장, 간결화, 에러 처리 추가
- `skills/hwp-template/SKILL.md` — description 확장, 스크립트 참조, 에러 처리 추가
- `skills/hwp-template/scripts/manage_template.py` — 템플릿 CRUD 관리 스크립트 (신규)
- `docs/plan_history.md` — 계획 이력 인덱스 (신규)
- `docs/plans/2026-03-05_100000_hwp-skills-improvement.md` — 개선 계획 문서 (신규)

---
