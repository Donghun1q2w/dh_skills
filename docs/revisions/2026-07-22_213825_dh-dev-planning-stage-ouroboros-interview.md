# dh-dev/plan-context 플래닝 단계에 ouroboros interview 패턴 이식

- **Date**: 2026-07-22 21:38:25
- **Author**: Claude (dh-dev 오케스트레이터)

## Rationale / Plan

사용자가 오픈소스 저장소 `https://github.com/Q00/ouroboros.git`의 `interview` 스킬(MCP 서버 기반 Socratic 인터뷰)을 참고하여 `dh-dev`의 플래닝 단계(Step 1)를 개선해 달라고 요청. ouroboros의 MCP 아키텍처는 이식하지 않고(신규 MCP 서버 구축 금지), 대화 컨텍스트만으로 동작하는 4개 상호작용 패턴만 우리의 스킬/서브에이전트 구조에 맞게 이식하기로 결정.

계획: `docs\plans\2026-07-22_211702_dh-dev-planning-stage-ouroboros-interview.md` (Status: In Progress → 본 개정 완료 후 Completed로 갱신 예정).

사용자가 AskUserQuestion으로 4개 개선 묶음(적대적 플랜 프리뷰 패널, Restate 확인 게이트, 모호성 원장+Refine 게이트, 신뢰도 기반 사실확인 라우팅)을 전부 선택. Fable 5 전담 플래닝 에이전트가 계획을 작성하고, Opus 4.8 전담 실행 에이전트가 구현 후 12개 적대적 테스트(T-1~T-12)로 자체 검증, 오케스트레이터가 hard gate 불변성·라인 수·헤딩 순서를 독립 재검증.

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills\dh-dev\SKILL.md` | Modified | 1-c Restate Gate·1-e Adversarial Plan Preview 신설, 기존 1-c를 1-d로 재번호 |
| `skills\plan-context\SKILL.md` | Modified | Interview Mode 전용 Core Rules 불릿 2개 추가 |
| `skills\plan-context\references\planning-workflow.md` | Modified | Interview Mode에 Ambiguity Ledger·Refine Gate·Fact-Confirmation Routing 하위섹션 3개 추가, 절차 7→8단계 확장 |
| `skills\plan-context\references\templates.md` | Modified | Interview Mode Templates 섹션(원장 스냅샷, Refine 페이로드 형식) 추가 |

## Details

### `skills\dh-dev\SKILL.md` (Modified) — 121 → 158행

- frontmatter description에 Restate 게이트·적대적 프리뷰 문구 추가
- 다이어그램에 "Step 1 detail" 라인(1-a→1-b→1-c→1-d→1-e) 추가
- Agent & Model Policy 표에 `Step 1-e Adversarial Preview` 행 신설(Sonnet, 2 레인: contrarian/gap_hunter), `Step 1-c` → `Step 1-d`로 재번호
- Codex 폴백 문구에 1-e 순차 처리 규칙 추가
- 신규 `### 1-c. Restate Gate (재진술 확인 게이트)`: 1-b 직후, 플래닝 에이전트 호출 전 한 문장 목표 재확인(AskUserQuestion, 3옵션, 최대 3회 조정). "플랜 저작 승인일 뿐 구현 승인 아님" 명문화
- `### 1-c. Plan Authoring` → `### 1-d. Plan Authoring`로 재명명, 입력 목록에 1-c 확정 문장 추가
- 신규 `### 1-e. Adversarial Plan Preview (계획 초안 적대적 검증)`: contrarian(숨은 가정 공격) + gap_hunter(누락 탐색) 2-레인 병렬 스폰, 오케스트레이터 로컬 구조 검사(게이트), HIGH 발견 시 1-d 1회 재작성, "패널은 승인 주체 아님" 명문화. Post-processing 문단을 1-e 끝으로 이동
- Step 2 첫 문단에 Reviewer notes 제시 문구 추가; Comment 루프의 `Step 1-c` 참조 2건을 `Step 1-d`로 치환. **Hard gate 문단(현재 117–124행)은 바이트 단위 무변경**
- Exceptions 표에 3행 추가: Restate 3회 미수렴, 1-e HIGH 잔존, 병렬 서브에이전트 미지원 환경 폴백

### `skills\plan-context\SKILL.md` (Modified) — 268 → 269행

- Phase A-2 모드 표 Interview 행에 "tracked by an ambiguity ledger" 문구 추가
- Core Rules에 `Interview Mode only:` 불릿 2개 추가(모호성 원장+Refine 게이트 / 신뢰도 기반 라우팅+Dialectic Rhythm Guard) — 두 불릿 모두 상세 절차는 `references/planning-workflow.md`로 위임
- Phase A, Phase B, Direct/Consensus/Review 관련 행은 무변경

### `skills\plan-context\references\planning-workflow.md` (Modified) — 177 → 221행

- Invocation Contexts에 예외 불릿 추가: dh-dev 1-b 인터뷰에는 Interview Mode 메커니즘(원장/Refine/라우팅)이 적용되나, 플랜 저작 단계(7-8단계)는 dh-dev에서 진입하지 않음을 명시해 기존 "Phase A-2 미진입" 규칙과의 모순 제거
- Interview Mode 절차를 7단계 → 8단계로 확장(원장 초기화, Refine 게이트 반영, 트랙 미해결 시 확인 질문)
- Question Classification 표의 Codebase Fact 행이 Fact-Confirmation Routing을 참조하도록 수정
- 신규 하위섹션 3개: `### Ambiguity Ledger (모호성 원장)`(5트랙: Scope/Constraints/Success Criteria/Non-goals/Verification, 상태값 Open/Partially resolved/Resolved/Waived), `### Refine Gate (자유서술 구조화 게이트)`(Decision/Reasoning/Constraints/Out of scope/Codebase context 5필드 구조화 + 4옵션 확인), `### Fact-Confirmation Routing (신뢰도 기반 사실확인 라우팅)`(PATH 1a 자동채택/PATH 1b 근거확인/PATH 2 직접질문 + Dialectic Rhythm Guard — 3연속 비사용자 답변 시 강제 전환)
- Quality Criteria Final Checklist에 "원장 전 트랙 Resolved/Waived" 항목 추가
- Tool Usage에 Refine/PATH 1b 확인 도구 불릿 추가
- Direct/Consensus/Review Mode 섹션은 무변경

### `skills\plan-context\references\templates.md` (Modified) — 142 → 170행

- 신규 `## Interview Mode Templates (인터뷰 모드 템플릿)` 섹션을 Plan History Template과 Status Values 사이에 삽입: 원장 스냅샷 표 형식, Refine Gate 구조화 페이로드 형식
- 기존 Context Summary/Plan Document/Plan History/Status Values/Notes 섹션은 무변경

## 검증 요약

Opus 4.8 실행 에이전트가 T-1~T-12(헤딩 순서, `Step 1-c` 잔존 0건, 레인/심각도 존재, hard gate diff 무변경, 표 열 정합, 모드 격리, 상호참조 왕복, 라인 수, 신규 파일 0건, 인코딩 read-back, dry-run 트레이스, hard-gate 우회 시도 3건)를 실행해 DoD-1~13 전부 PASS 보고. 오케스트레이터가 hard gate 문단 byte-diff, `Step 1-c` 저장소 전체 grep, 라인 수, 헤딩 순서를 독립 재검증하여 일치 확인.
