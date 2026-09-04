# Plan History

Chronological log of project plans and decisions.

---

## 2026-09-04 15:26:46 — dh-dev 문서의 'Fable 5' 버전 표기를 버전 없는 'Fable'로 일반화

[Detail](plans/2026-09-04_152646_fable-version-label-generalization.md) | Status: **Completed**

Summary: `skills/dh-dev/SKILL.md`(3·26·40행)와 `skills/plan-context/references/planning-workflow.md`(21행)에 하드코딩된 'Fable 5' 표기 4곳을 버전 숫자 없는 'Fable'로 바꿔, Fable 모델이 갱신돼도 문서를 다시 고칠 필요가 없게 한다. 2026-07-25의 "Opus 4.8" → "Opus (`opus`)" 일반화 선례를 그대로 따르며, 도구가 실제로 받는 백틱 alias(`fable`)와 예제 코드의 API 모델 ID는 손대지 않는다. harness가 alias를 최신 모델로 해석하므로 동작 변화는 없다. 1-e 적대적 검증에서 HIGH 2건(무관한 미커밋 변경 때문에 경로 한정 없는 git diff 검증이 항상 실패, --numstat 파일별 기대값 오류)을 1회 재작성으로 전부 반영.

---

## 2026-09-02 10:10:02 — dh-loop 반복 오케스트레이터 스킬 신규 추가

[Detail](plans/2026-09-02_101002_add-dh-loop-skill.md) | Status: **Completed**

Summary: dh-dev의 계획→실행→검토→커밋 절차를 위임 방식으로 감싸는 반복 오케스트레이터 스킬 `skills/dh-loop/SKILL.md`를 신규 추가한다. dh-dev 본문을 복제하지 않고 `skills\dh-dev\SKILL.md`를 읽어 그 절차를 회차마다 수행하므로 dh-dev 개정을 자동으로 따라간다. 초기 계획 1회만 사용자 승인을 받고 이후에는 무인으로 돌며, 실행 에이전트와 분리된 독립 검증 에이전트가 증거를 요구하며 개발 완료조건을 항목별로 판정한다. 미충족 항목은 직전 회차의 실패 증거와 함께 재계획으로 되돌아가고, 반복 횟수 상한은 없다. 같은 항목이 개선 없이 2회 연속 불합격하거나 누적 4회 불합격하면 증거와 실패 이력을 모아 사용자를 호출하고 멈춘다. 회차 상태는 `docs\dh-loop\`의 기록 파일에 남겨 대화 압축 이후에도 재개할 수 있다. 무인 커밋은 `dh-loop/<slug>` 전용 브랜치에서만 수행하고 보호 브랜치에서는 금지한다. 1-e 적대적 검증(contrarian + gap_hunter, HIGH 9/MEDIUM 6/LOW 1)을 1회 재작성으로 전부 반영 — README 기준선 행 수 정정, 브랜치 격리 정책 신설, 분량 상한 280줄로 상향, 자동 승인 조건에 미해결 HIGH 없음 추가, plan_history Status 표준값 준수, 축소 실동 예행 신설.

---

## 2026-08-14 13:57:18 — dh-dev 스킬 모델·effort 정책 및 워크플로우 개정

[Detail](plans/2026-08-14_135718_dh-dev-policy-revision.md) | Status: **Completed**

Summary: dh-dev 스킬의 (1) Step 3 구현 에이전트를 모든 등급에서 Sonnet 고정(등급은 reasoning effort만 선택), (2) Large(최대 추론) 판정 기준을 10개 이상 파일·400줄 초과·아키텍처 또는 모듈 간 계약 변경·위험 키워드로 대폭 상향하고 기본 등급을 Medium으로 변경(애매한 신호는 Large가 아니라 Medium으로 반올림), (3) 1-b 초반에 개발 방향을 단발성/간단한/심화로 묻는 절차 신설, (4) 개발 방향이 올라갈수록 설정 외부화·재사용 인터페이스와 확장점·경계 예외 처리·테스트와 문서 커버리지 요구가 단계적으로 높아지는 범용성 4축 표 도입. 개발 방향은 등급·게이트와 직교하며 어떤 게이트도 축소하지 않는다.

---

## 2026-08-10 17:06:32 — pdf-annotate 스킬 신규 추가 (pdf2img 패턴)

[Detail](plans/2026-08-10_170632_pdf-annotate-skill.md) | Status: **Completed**

Summary: ReportReviewer 저장소의 `cert-review-annotate` 스킬(및 실제 구현 `skills/cert-review/scripts/annotate_pdf.py`)이 쓰는 pypdf 네이티브 PDF 주석 기법 — 판정별 색상의 경계선 `/Square` + Acrobat `/Popup` 컴패니언 + PIL 래스터 기반 커스텀 appearance stream을 가진 한글 `/FreeText` 라벨 3종 묶음 — 을 ReportReviewer의 케이스 관리 종속성 없이 범용 재사용 가능한 샘플로 일반화해 `skills/pdf-annotate/`(얇은 SKILL.md, pdf2img 패턴) + `refcode/pdf_annotate/`(8파일 참조 패키지)로 신규 추가. 1-e 적대적 검증(contrarian+gap_hunter, HIGH 7/MEDIUM 7/LOW 5, 중복 제거 후)을 1회 재작성으로 전부 반영 — DoD-적대적테스트 태그 불일치 다수 정정(`[ADV-n]`/`[V-n]` 이원화), ReportReviewer 판정 라벨(주의/N/A/FAIL)을 키로 쓰던 PRESET_COLORS를 도메인 중립 키로 교체, 회전 라운드트립 오차 허용치 통일(1e-9), 출력=입력 가드용 DoD 신설, 절대 성능 기준을 상대 기준으로 완화.

---

## 2026-07-27 14:06:08 — dxf-to-pdf 스킬 신규 작성 (번들 CLI 직접 실행형)

[Detail](plans/2026-07-27_140608_add-dxf-to-pdf-skill.md) | Status: **Completed**

Summary: `D:\002_C_Sharp\dxf_to_pdf\dxf_converter\release-cli`의 dxf_converter CLI(exe+DLL 14개+contracts 스키마, 총 24개 파일)를 `skills/dxf-to-pdf/references/cli/`에 그대로 복사해 커밋하고, `scripts/convert-dxf.ps1`이 매 실행 시 %TEMP% 작업 폴더로 번들을 복사한 뒤 settings.json을 생성해 CLI를 직접 실행함으로써 단일 파일·폴더 배치(재귀 옵션 포함) DXF→PDF 변환을 수행하는 신규 스킬. 1-e 적대적 검증(contrarian+gap_hunter, HIGH 5/MEDIUM 9/LOW 5 총 19건)을 1회 재작성으로 전부 반영 — 정적 AT 6종 신설로 DoD-AT 매핑 완결, skip-only 재실행 시 %TEMP% 누적 버그 수정, AT-2 `in_flat` 준비 코드 누락 수정, preview 제외 검증 항목 추가. 계획 서두에 사용자 재확인이 필요한 계획 작성자 임의 결정 3건(기본값 무질문 정책·자연어 의도 추론·파라미터 노출)을 명시.

---

## 2026-07-25 15:33:52 — dh-dev Opus 버전 표기 일반화

[Detail](plans/2026-07-25_153352_dh-dev-opus-label-generalization.md) | Status: **Completed**

Summary: 2026-07-24 Claude Opus 5 출시(Opus 4.8과 동일 가격, 병행 운영)에 대응해, dh-dev/SKILL.md의 Large 등급 Step 3 모델 표기 4곳에서 하드코딩된 "Opus 4.8" 버전 문자열을 Medium 등급과 동일한 범용 "Opus (`opus`)" alias 표기로 일반화 — 향후 Opus 갱신 시 문서 수정 불필요. 신규 티어링 시스템으로 Small 등급 판정(Sonnet/standard). 1-e 검토에서 6건(HIGH 4) 발견 후 1회 재작성으로 전부 반영.

---

## 2026-07-23 10:55:47 — dh-dev Agent & Model Policy 모델·effort 3단계 티어링 도입

[Detail](plans/2026-07-23_105547_dh-dev-model-effort-tiering.md) | Status: **Completed**

Summary: dh-dev의 Agent & Model Policy(1-d Plan Authoring, Step 3 Execute)에 작업 규모(파일 수·변경 라인 수·위험 영역) 기반 3단계(Large/Medium/Small) 모델·effort 티어링을 도입. 1-d 티어는 1-c Restate 확정 시점에, Step 3 티어는 승인된 계획의 Implementation Steps로 각각 독립 판정하며, 신호가 애매하면 항상 상위 등급으로 반올림하고 Large를 보수적 기본값으로 유지. Step 2 hard gate는 무변경. 1-e contrarian/gap_hunter 검토에서 발견된 13건(HIGH 4)을 1회 재작성으로 전부 반영.

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
