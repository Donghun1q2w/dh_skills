# Product Development Process Agent (PDP Agent)

**"코드를 잘 짜는 개발자"가 아닌 "망하지 않는 제품을 만드는 빌더"를 위한 AI 에이전트**

## 개요 (Overview)

PDP Agent는 현업 시니어 개발자의 13년 경험을 토대로 설계된, 제품 개발 전 주기를 관리하는 멀티스테이지 AI 에이전트입니다.
단순히 기능 구현을 돕는 것이 아닌, **기획 → 설계 → 구현 → 검증 → 런칭 → 회고**까지 각 단계에서 리스크를 선제 차단하고 의사결정의 질을 높이는 것이 목표입니다.

```
기획 (Why) → 리스크 체크 (Safe?) → 구현 (Build) → 런칭 (Validate) → 회고 (Learn)
```

## 에이전트 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                      PDP Orchestrator                           │
│              (Supervisor Agent - 전체 단계 조율)                  │
└─────────┬───────────┬───────────┬───────────┬───────────────────┘
          │           │           │           │
  ┌───────▼───┐ ┌─────▼───┐ ┌────▼────┐ ┌────▼────────┐
  │ Planning  │ │  Risk   │ │  Build  │ │   Launch    │
  │  Agent    │ │  Agent  │ │  Agent  │ │   Agent     │
  │ (1~3단계) │ │(4~5단계)│ │(6~8단계)│ │ (9~12단계)  │
  └───────────┘ └─────────┘ └─────────┘ └─────────────┘
                                              │
                                      ┌───────▼───────┐
                                      │  Retro Agent  │
                                      │   (13단계)     │
                                      └───────────────┘
```

## 단계별 에이전트 상세 설계

### Phase 1 — Planning Agent (기획과 가설)

**담당 단계:** PF → FBS → RFD

**역할:**
- 비즈니스 가치 기반 우선순위 결정 지원
- North Star Metric / Kill Metric / Guardrail Metric 도출
- 1-Pager 기획안 생성 및 검토

**입력 (Input):**

```yaml
inputs:
  - idea_description: string    # 기능 아이디어 설명
  - business_context: string    # 현재 비즈니스 상황
  - available_resources: object  # 팀 규모, 기간, 예산
  - current_metrics: object      # 현재 주요 지표 (이탈률, 전환율 등)
```

**출력 (Output):**

```yaml
outputs:
  - priority_score: float        # 우선순위 점수 (0~10)
  - north_star_metric: string    # 핵심 성공 지표
  - kill_metric: string          # 실패 판단 기준
  - guardrail_metrics: list      # 보호 지표 목록
  - one_pager: markdown          # 1-Pager 기획 문서
  - go_decision: boolean         # 진행 여부 판단
```

**핵심 프롬프트 로직:**

1. "지금 가장 비싼 문제는 무엇인가?" 분석
2. 기능 성공 ≠ 제품 성공 관점에서 side effect 시뮬레이션
3. 실패 시나리오 3가지 이상 도출 후 GO/NO-GO 판단

---

### Phase 2 — Risk Agent (리스크 체크)

**담당 단계:** FBD → RFE

**역할:**
- UX 사용성 리스크 스캔
- 기술 구현 리스크 사전 탐지
- 법적/보안/개인정보 이슈 체크리스트

**입력 (Input):**

```yaml
inputs:
  - one_pager: markdown          # Planning Agent 출력
  - design_specs: object         # 디자인 명세 (와이어프레임 등)
  - tech_stack: list             # 기술 스택 정보
  - user_segments: list          # 타겟 유저 그룹
```

**출력 (Output):**

```yaml
outputs:
  - risk_report: object
      ux_risks: list             # UX 혼란 포인트
      tech_risks: list           # 기술 구현 위험 요소
      legal_risks: list          # 법적/규제 리스크
      edge_cases: list           # 반드시 처리해야 할 엣지케이스
  - critical_questions: list     # 킥오프 전 반드시 확인할 질문
  - risk_level: enum             # LOW / MEDIUM / HIGH / CRITICAL
```

**핵심 체크리스트:**

```
□ 네트워크 단절 시 처리 방식
□ 동시 접속 급증 시나리오 (트래픽 스파이크)
□ 환불/취소 케이스 처리
□ 개인정보 수집/저장 범위
□ 접근성 (a11y) 요구사항
□ 보안 취약점 (OWASP Top 10 기준)
□ 데이터 마이그레이션 필요 여부
□ 롤백 전략 존재 여부
```

---

### Phase 3 — Build Agent (구현과 검증)

**담당 단계:** FUE → RFQ → FUQ

**역할:**
- API 설계 협의 시뮬레이션 (BE/FE 관점 충돌 탐지)
- 성능 영향도 분석
- QA 시나리오 자동 생성

**입력 (Input):**

```yaml
inputs:
  - risk_report: object          # Risk Agent 출력
  - feature_spec: markdown       # 기능 명세
  - api_contracts: list          # 예상 API 목록
  - performance_sla: object      # 응답속도, 가용성 기준
```

**출력 (Output):**

```yaml
outputs:
  - api_review:
      conflicts: list            # BE/FE 관점 충돌 포인트
      optimization_suggestions: list
  - performance_impact_analysis: object
      estimated_latency_change: string
      db_query_complexity: string
      caching_requirements: list
  - qa_scenarios: list           # 테스트 시나리오 (해피패스 + 엣지케이스)
  - definition_of_done: list     # 완료 기준 체크리스트
```

**API 충돌 탐지 예시:**

```
프론트 요청: "응답에 user_profile 추가해주세요"
백엔드 분석: DB JOIN 3회 추가, 캐시 무효화 필요, p95 레이턴시 +120ms 예상
→ 대안 제시: 별도 API 분리 or GraphQL 도입 검토
```

---

### Phase 4 — Launch Agent (런칭과 결정)

**담당 단계:** RFT → FUT → FL / FNL

**역할:**
- 점진적 배포 전략 설계
- A/B 테스트 설계 및 통계적 유의성 계산
- 데이터 해석 및 최종 런칭/롤백 판단

**입력 (Input):**

```yaml
inputs:
  - qa_results: object           # QA 통과 결과
  - north_star_metric: string    # Planning Agent에서 정의한 핵심 지표
  - kill_metric: string
  - guardrail_metrics: list
  - deployment_config: object    # 배포 환경 설정
```

**출력 (Output):**

```yaml
outputs:
  - deployment_strategy:
      type: enum                 # CANARY / BLUE-GREEN / FEATURE_FLAG
      rollout_plan: list         # 단계별 트래픽 비율 (1% → 10% → 50% → 100%)
      rollback_trigger: object   # 자동 롤백 조건
  - ab_test_design:
      hypothesis: string
      control_group: object
      experiment_group: object
      minimum_sample_size: int
      test_duration_days: int
  - launch_decision:
      recommendation: enum       # LAUNCH / HOLD / ROLLBACK
      rationale: string
      data_evidence: object
```

**자동 롤백 트리거 예시:**

```yaml
rollback_triggers:
  - metric: error_rate
    threshold: "> 1%"
    window: "5분"
  - metric: p99_latency
    threshold: "> 3000ms"
    window: "10분"
  - metric: kill_metric
    threshold: "통계적 유의성 p<0.05로 악화"
    window: "24시간"
```

---

### Phase 5 — Retro Agent (회고)

**담당 단계:** Post-Mortem

**역할:**
- 장애 원인 분석 (사람이 아닌 시스템 관점)
- 5 Whys 자동 수행
- 개선 액션 아이템 도출 및 추적

**입력 (Input):**

```yaml
inputs:
  - incident_timeline: list      # 사건 발생 타임라인
  - monitoring_logs: object      # 알람, 에러 로그
  - team_retrospective: string   # 팀 회고 내용
  - previous_actions: list       # 이전 회고 액션아이템 이행 현황
```

**출력 (Output):**

```yaml
outputs:
  - root_cause_analysis:
      contributing_factors: list
      five_whys: list            # 5단계 Why 분석
      system_failure_points: list # 사람이 아닌 시스템 관점
  - action_items:
      - title: string
        owner: string
        due_date: date
        priority: enum           # P0 / P1 / P2
        expected_outcome: string
  - process_improvements: list   # 프로세스 개선 제안
  - blameless_summary: markdown  # Blameless Post-Mortem 문서
```

## Orchestrator 설계

### 상태 관리 (State Machine)

```
[IDEA]
  → Planning Agent
    → [GO/NO-GO]
      ├─ NO-GO → [ARCHIVED] (매몰 비용 없이 종료)
      └─ GO → Risk Agent
               → [RISK_ASSESSED]
                 → Build Agent
                   → [BUILT]
                     → Launch Agent
                       → [LAUNCHED / NOT_LAUNCHED]
                         → Retro Agent
                           → [LEARNED]
```

### 단계 간 Context 전달

```python
class PDPContext:
    feature_id: str
    current_phase: PhaseEnum
    planning_output: PlanningOutput
    risk_output: RiskOutput
    build_output: BuildOutput
    launch_output: LaunchOutput
    retro_output: RetroOutput

    # 전 단계 결정사항이 다음 단계로 자동 전달
    # Kill Metric을 Planning에서 정의 → Launch에서 자동 검증에 사용
```

### 도구 연동 (Tool Integration)

| 단계 | 연동 도구 | 용도 |
|------|----------|------|
| Planning | Notion, Confluence | 1-Pager 자동 작성 |
| Risk | Jira, Linear | 리스크 티켓 자동 생성 |
| Build | GitHub, GitLab | PR 템플릿, 체크리스트 생성 |
| Build | Swagger/OpenAPI | API 계약 리뷰 |
| Launch | AWS CloudWatch, DataDog | 배포 후 모니터링 연동 |
| Launch | LaunchDarkly, Split | Feature Flag 관리 |
| Retro | Slack | 회고 문서 자동 공유 |

## 사용 시나리오 예시

### 입력

```
사용자: "결제 단계에 간편결제(카카오페이) 추가하고 싶어요.
현재 결제 전환율 72%, 이탈률 28%입니다."
```

### PDP Agent 처리 흐름

```
1. Planning Agent:
   → 우선순위 분석: 이탈률 28% → 높은 비즈니스 임팩트 (Priority: 9.2/10)
   → North Star: 결제 완료율 +5%p 향상
   → Kill Metric: 기존 결제 전환율 72% 미만으로 하락 시 롤백
   → Guardrail: CS 문의 건수, 환불률, 에러율

2. Risk Agent:
   → 카카오페이 API 장애 시 폴백 처리 필요
   → PG사 변경에 따른 정산 프로세스 검토 필요
   → 개인정보: 간편결제 토큰 저장 방식 법적 검토 필요

3. Build Agent:
   → API 충돌: 결제 상태 Enum 타입 통일 필요 (BE/FE 불일치 발견)
   → 성능: 카카오페이 API 호출 타임아웃 설정 (현재 미설정)
   → QA 시나리오 47개 자동 생성 (네트워크 단절, 중복 결제, 환불 등)

4. Launch Agent:
   → Canary 배포: 1% → 5% → 20% → 100% (각 24시간 관찰)
   → A/B 테스트 최소 샘플: 4,200명 / 예상 기간: 14일
   → 자동 롤백 트리거 설정 완료

5. 결과: GO 결정, 전체 실행 계획 문서 자동 생성
```

## 핵심 설계 원칙

### 1. 선제적 실패 탐지 (Fail Early)

각 단계에서 리스크를 발견할수록 수정 비용이 기하급수적으로 낮아집니다.
에이전트는 매 단계마다 **"이 상태로 다음 단계로 가면 어떤 일이 벌어지는가?"**를 시뮬레이션합니다.

### 2. 데이터 기반 의사결정 (Data-Driven)

의견이 아닌 데이터로 결정합니다. Launch Agent는 통계적 유의성 없이는 절대 LAUNCH 추천을 하지 않습니다.

### 3. Blameless Culture 지원

Retro Agent는 절대 특정 담당자를 지목하지 않습니다. 모든 분석은 **"왜 시스템이 막지 못했는가"** 관점으로만 작성됩니다.

### 4. 컨텍스트 연속성 (Context Continuity)

기획 단계에서 정의한 Kill Metric이 런칭 단계에서 자동으로 롤백 트리거가 됩니다. 에이전트 간 정보 손실이 없습니다.

### 5. 멈출 줄 아는 용기 (Courage to Stop)

NO-GO 판단은 실패가 아닙니다. Planning Agent의 GO/NO-GO 판단은 팀의 매몰 비용을 줄이는 가장 중요한 결정입니다.

## 향후 확장 로드맵

| 버전 | 내용 |
|------|------|
| v1.0 현재 | 5개 에이전트 기본 파이프라인 |
| v1.5 예정 | Slack/Notion 실시간 연동 + 자동 문서화 |
| v2.0 예정 | 과거 프로젝트 학습 기반 Kill Metric 자동 예측 |
| v2.5 예정 | 실시간 모니터링 연동 (CloudWatch/DataDog) + 자율 롤백 |
| v3.0 예정 | 멀티 프로젝트 동시 관리 + 리소스 최적화 자동화 |

---

> *"실무에서 가장 비싼 비용은 개발자의 연봉이 아니라, 잘못된 방향으로 세 달 동안 전력 질주하는 것이다."*
> *PDP Agent는 그 질주를 시작하기 전에, 방향이 맞는지 먼저 확인합니다.*
