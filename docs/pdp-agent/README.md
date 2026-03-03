# PDP Agent — 사용 가이드

```
skills/pdp-agent/
├── SKILL.md              ← Orchestrator (Claude가 읽는 파일)
└── references/
    ├── planning.md       ← Phase 1: 기획
    ├── risk.md           ← Phase 2: 리스크
    ├── build.md          ← Phase 3: 구현
    ├── launch.md         ← Phase 4: 런칭
    └── retro.md          ← Phase 5: 회고

docs/pdp-agent/
├── README.md             ← 이 파일 (사용 가이드)
└── AGENT.md              ← 설계 문서
```

## 빠른 시작

### Claude Code에서 사용할 때

```bash
# 프로젝트 루트에 SKILL.md 배치
cp pdp-agent/SKILL.md ./SKILL.md

# 또는 references 폴더 전체를 참조
cp -r pdp-agent/references ./references/
```

Claude에게 아래처럼 말하면 됩니다:

> "SKILL.md를 읽고, 내 기능 기획을 도와줘.
> 새로운 소셜 로그인 기능을 추가하려고 하는데,
> 현재 가입 전환율은 34%야."

### Claude.ai (일반 채팅)에서 사용할 때

SKILL.md 내용을 System Prompt 또는 첫 메시지에 붙여넣고 대화를 시작합니다.

## 각 단계별 사용법

### 1단계 — 기획이 막막할 때 (Planning Agent)

> "planning.md 읽어줘.
> [기능 아이디어]를 만들까 고민 중인데, 우선순위 분석부터 해줘."

### 2단계 — 개발 전에 리스크가 걱정될 때 (Risk Agent)

> "risk.md 읽어줘.
> [기능명] 킥오프 전인데, 어떤 리스크를 확인해야 하는지 체크해줘.
> 기획 내용은 이거야: [내용]"

### 3단계 — 개발 중 막혔을 때 (Build Agent)

> "build.md 읽어줘.
> 프론트에서 [이런 데이터]가 필요한데 백엔드가 [이런 이유]로 안 된다고 해.
> 어떻게 해결할까?"

> "build.md 읽어줘.
> [기능명] QA 시나리오 만들어줘. 주요 기능은 [설명]이야."

### 4단계 — 배포/A/B 테스트 (Launch Agent)

> "launch.md 읽어줘.
> [기능명] 배포 전략 짜줘. MAU는 50만이고, 결제 관련 기능이야."

> "launch.md 읽어줘.
> A/B 테스트 결과가 나왔어: [결과 내용]. 이거 전체 배포해도 될까?"

### 5단계 — 장애 났을 때 (Retro Agent)

> "retro.md 읽어줘.
> 오늘 새벽에 결제 서버 장애가 났어. 타임라인이랑 원인 분석 도와줘."

## 주의사항

- SKILL.md는 Claude에게 주는 지시서입니다. 내용을 수정하면 에이전트 동작이 바뀝니다.
- 단계를 건너뛰려 하면 에이전트가 경고합니다. 의도적으로 건너뛸 경우 명시적으로 말해주세요.
- Kill Metric이 없으면 Planning → Risk 단계로 넘어가지 않습니다.
