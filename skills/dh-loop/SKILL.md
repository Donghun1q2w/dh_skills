---
name: dh-loop
description: "Iterative wrapper around the dh-dev workflow. Reads skills\\dh-dev\\SKILL.md and runs its plan → review → execute → commit procedure round after round on a dedicated dh-loop branch: the user approves only the first plan, then an independent verification agent (separate from the executor, evidence required) checks every Definition of Done item; unmet items send the run back to replanning with the previous round's failure evidence attached, and the loop repeats without an iteration cap. Stops and calls the user when the same item fails twice in a row with no change in its failure signature. Round state is kept in docs\\dh-loop\\ so the loop survives context compaction and can be resumed. Use when: a task should keep iterating unattended until every completion condition is met, or a dh-dev run needs repeated replan-execute-verify cycles. Triggers: '반복 개발', '완료될 때까지', '무인 반복', 'dh-loop', 'loop until done', 'keep iterating', 'autonomous dev loop'."
---
# dh-loop

dh-dev의 계획→실행→검토→커밋 절차를 회차 단위로 감싸는 반복 오케스트레이터다. 절차 본문은 만들지 않고 `DHDEV_PATH`를 읽어 그대로 수행한다.

```
승인(1회) ──→ [ Round-Plan → Round-Execute → Round-Verify → Round-Commit ] ──→ Stagnation-Check
                        ↑                                                          │
                        └──────────── 미충족 시 재계획 (무인) ──────────────────────┘
```

> **Effort:** 이 워크플로는 최대 추론 강도로 오케스트레이터를 운용한다. 회차 안의 하위 에이전트(계획·실행·검증)는 각각 dh-dev Model & Effort Tiering과 아래 `VERIFIER_EFFORT`가 정한 강도를 따른다. Small 티어라 해도 이 규칙 위반이 아니다.

## 위임 계약 (Delegation Contract)

1. 루프 시작 시 `DHDEV_PATH` 문서를 처음부터 끝까지 한 번 읽는다. 요약본이나 기억에 의존하지 않는다.
2. 각 회차의 계획·실행·검토·커밋은 dh-dev가 정의한 순서(Step 1 → Step 2 → Step 3 → Step 4)를 그대로 따른다. dh-loop은 어느 단계를 언제 부를지만 정한다.
3. dh-loop 문서는 dh-dev의 규칙을 이름과 절 번호로만 가리킨다. 규칙 내용을 옮겨 적지 않는다. 규칙을 언급하는 줄에는 반드시 `dh-dev`라는 낱말이 같은 줄에 있어야 한다.
4. dh-dev 문서를 수정하지 않는다. dh-loop이 필요로 하는 차이는 전부 `## 루프 재정의` 표로 처리한다.
5. dh-dev가 개정되면 dh-loop은 다음 실행에서 자동으로 새 절차를 따른다. 재정의 표의 대상 규칙 이름이 dh-dev에서 사라진 경우, 해당 행을 적용하지 않고 사용자에게 한 줄로 알린다.

## 루프 상수 (Loop Constants)

| 상수 | 값 | 뜻 |
| --- | --- | --- |
| `DHDEV_PATH` | `skills\dh-dev\SKILL.md` | 절차 원본 문서 |
| `LEDGER_DIR` | `docs\dh-loop\` | 회차 기록 파일 폴더 |
| `MAX_ROUNDS` | `0` | 회차 상한. `0`이면 상한 없음 |
| `STAGNATION_LIMIT` | `2` | 같은 항목 연속 불합격 허용 횟수 |
| `CUMULATIVE_FAIL_LIMIT` | `4` | 같은 항목 누적 불합격 허용 횟수 (보조 안전장치) |
| `VERIFIER_MODEL` | `opus` | 검증 에이전트 모델 |
| `VERIFIER_EFFORT` | Large 회차 `max`, 그 밖에는 `high` | 검증 에이전트 추론 강도 |
| `VERIFIER_RETRY` | `1` | 출력 형식 위반 시 재호출 횟수 |
| `SCOPE_GUARD` | `on` | 승인 파일 범위 이탈 시 정지할지 여부 |
| `LOOP_BRANCH_PREFIX` | `dh-loop/` | 루프 전용 브랜치 이름 앞머리 |
| `PROTECTED_BRANCHES` | `main`, `master` | 회차 커밋을 쌓으면 안 되는 브랜치 |

**Large 회차의 뜻** — 그 회차 dh-dev Step 3 티어 판정이 `Large`로 나온 회차를 말한다. 티어 판정은 dh-dev Agent & Model Policy가 정한 대로 오케스트레이터가 한다.

**비기본값일 때의 동작**

| 상수 | 비기본값일 때 |
| --- | --- |
| `MAX_ROUNDS` | `1` 이상이면 그 회차를 끝낸 뒤 정지한다. 정체와 같은 형식으로 보고하되 사유를 `round-limit`으로 적고, `## 정체 판정`의 선택 표를 그대로 제시한다 |
| `SCOPE_GUARD` | `off`면 범위 이탈을 정지 사유로 삼지 않고 회차 기록에 `scope-exceeded`로 남긴 뒤 진행한다. 이때 OV-1 자동 승인 조건 (나)는 충족한 것으로 본다 |

## 루프 재정의 (Loop Overrides)

> 이 표의 행은 `LEDGER_DIR` 안에 `**Status**: Running`인 회차 기록 파일이 있는 동안에만 효력이 있다. 루프가 끝나 Status가 `Completed`·`Stopped`로 바뀌는 순간 dh-dev 원문이 그대로 되살아난다. 재정의는 dh-dev 파일을 고치는 방식이 아니라 dh-loop 실행 중에만 적용되는 상위 규칙이다. 표에 없는 모든 것은 dh-dev를 그대로 따른다. 각 단계는 시작 전에 이 파일의 Status를 다시 읽어 Running임을 확인한다.

| 번호 | 대상 (dh-dev/revision-tracker 규칙) | 재정의 내용 | 안전장치 |
| --- | --- | --- | --- |
| OV-1 | dh-dev Step 2 하드 게이트 | 1회차는 원문 그대로 사용자 승인. 2회차 이후 재계획은 자동 승인하고 회차 기록에 `Auto-approved (round N)`으로 남긴다 | 자동 승인은 (가) 목표 문장이 그대로이고 (나) 대상 파일이 승인 파일 범위 안이며 (다) 직전 회차 실패 항목만 다루고 (라) 그 회차 dh-dev 1-e 구조 점검과 단일 재수정 뒤에도 미해결 `HIGH` 발견이 없을 때만 가능. 하나라도 어기면 사용자 호출 후 정지 |
| OV-2 | revision-tracker 6절 Git Commit의 3지선다 | 무인 회차에서는 `Commit`을 자동 선택해 그대로 실행한다 | 커밋 대상 브랜치는 반드시 `LOOP_BRANCH_PREFIX`로 시작해야 한다. 커밋 메시지는 `/commit` 형식을 지키고, 귀속 표기를 넣지 않는다. 제목 끝에 `(dh-loop round N)`을 붙인다 |
| OV-3 | dh-dev Step 4 2항 (`Completed` 갱신) | 검증 에이전트가 전 항목 합격을 낸 회차에서만 `Completed`로 바꾼다. 불합격 회차는 Status를 `Superseded`로 두고, Summary 텍스트 맨 앞에 `[dh-loop round N 검증 불합격]`을 붙인다 | Status 값은 plan-context가 정한 표준 6개 값만 쓴다. 새 Status 값을 만들지 않는다. 실행자 주장만으로는 절대 `Completed`로 바꾸지 않는다 |
| OV-4 | dh-dev 1-b 개발 방향 질문, 1-c 재진술 게이트 | 1회차에만 수행하고 2회차 이후는 1회차 결과를 재사용한다 | 매 재계획 뒤 오케스트레이터가 계획 문서의 목표 문장과 기록 파일 `Goal`을 문자열로 견준다. 다르면 루프를 멈추고 사용자를 부른다 |
| OV-5 | dh-dev Step 3 7항 (오류 시 사용자 확인) | 오류를 실패 증거로 기록하고 다음 회차 재계획으로 넘긴다 | 같은 오류가 정체 판정에 걸리면 사용자 호출 |
| OV-6 | dh-dev 예외 표 "완료조건 달성 실패 시 사용자 질문" | 해당 항목을 불합격으로 처리하고 재계획한다 | 정체 판정 적용 |

**재정의하지 않는 것** — dh-dev 1-e 적대적 계획 미리보기, dh-dev 1-d의 필수 계획 섹션 8개, dh-dev Step 3 실행 후 증거 대조, revision-tracker의 수정내역 기록과 품질 점검, dh-dev 모델·추론 강도 티어링, plan-context의 Status 값 목록은 모든 회차에서 원문대로 적용한다.

## 단계 계약 (Stage Contracts)

`Load`를 뺀 모든 단계의 입력 첫 칸은 기록 파일 Status 확인(Running이어야 진행)이다.

| 단계 | 입력 | 출력 | 실패 처리 |
| --- | --- | --- | --- |
| `Load` | `DHDEV_PATH` | dh-dev 절차 본문(문맥에 적재) | 읽기 실패 → 탐색 순서(아래 예외 절) → 전부 실패 시 즉시 중단 |
| `Round-Plan` | 기록 파일 Status 확인, 목표 문장, 1회차 맥락(dh-dev 1-a 분석 산출물·1-b 맥락 요약), 직전 회차 실패 항목·증거·시도 이력, 승인 파일 범위 | 계획 문서 경로, 목표 문장 변경 여부 판정, 대상 파일 목록 | 계획이 승인 파일 범위를 벗어남 → 사용자 호출 후 정지 |
| `Round-Execute` | 기록 파일 Status 확인, 계획 문서 경로 | 변경 파일 목록, 실행자 주장 체크리스트 | 실행 오류 → 실패 증거로 기록하고 다음 회차로 (OV-5) |
| `Round-Verify` | 기록 파일 Status 확인, 계획 문서 경로, 완료조건 목록, 적대적 테스트 절, 변경 파일 목록, 실행자 주장, 직전 회차 실패 이력 | 항목별 판정 표 | 형식 위반 → `VERIFIER_RETRY`회 재호출 → 그래도 위반이면 회차 전체 불합격 |
| `Round-Commit` | 기록 파일 Status 확인, 변경 파일 목록, 회차 번호, 작업 브랜치 이름 | 커밋 해시 | 커밋 실패 → 회차 기록에 남기고 다음 회차 진행, 정지하지 않음 |
| `Stagnation-Check` | 기록 파일 Status 확인, 이번 회차 실패 항목, 직전 회차 실패 항목 | 정체 여부와 대상 항목 | 직전 회차 기록이 없으면 정체 아님으로 판정 |
| `Stop-Report` | 회차 기록 파일 전체 | 사용자 보고문과 세 선택지 | 해당 없음 (마지막 단계) |

## 회차 기록 파일 (Round Ledger)

회차 상태는 `LEDGER_DIR` 안 마크다운 파일 한 개에 남긴다. 세션 기억에 의존하지 않는다 — 대화가 압축되어도 이 파일만 읽으면 재개할 수 있어야 한다.

```markdown
# dh-loop run: 2026-09-02_101500_add-dh-loop

**Goal**: <dh-dev 1-c에서 확정한 문장 한 줄>
**Status**: Running
**Started**: 2026-09-02 10:15:00
**Last updated**: 2026-09-02 11:40:12
**Current round**: 2
**Current phase**: verify
**Approved file scope**: skills/dh-loop/SKILL.md, README.md
**Working branch**: dh-loop/add-dh-loop

## 1회차 맥락 (재계획용 보존)

- dh-dev 1-a 분석 산출물: <경로 또는 요지 5줄 이내>
- dh-dev 1-b 맥락 요약: <본문 그대로 보존>
- dh-dev 1-b 개발 방향: 간단한 (simple)

## 회차 요약

| 회차 | 계획 문서 | 변경 파일 수 | 판정 | 불합격 항목 키 | 커밋 |
| --- | --- | --- | --- | --- | --- |
| 1 | docs\plans\2026-09-02_101800_....md | 2 | FAIL | ledger-format, verifier-contract | a1b2c3d |

## 회차 1 상세

### 불합격 항목
| 항목 번호 | 안정 키 | 완료조건 원문 | 실패 요지 | failure_signature |
| --- | --- | --- | --- | --- |
| DOD-06 | ledger-format | 회차 기록 형식 예시가 문서에 있다 | 예시 표에 커밋 열 없음 | missing-column:commit |

### 시도했다가 실패한 접근
- 회차 기록을 plan_history.md에 합쳐 쓰기 — 인덱스 형식이 깨져 되돌림

### 정체 계수기
| 안정 키 | 연속 불합격 | 누적 불합격 | 직전 failure_signature |
| --- | --- | --- | --- |
| ledger-format | 1 | 1 | missing-column:commit |
```

규칙:

1. 각 회차가 끝날 때마다 바로 갱신한다. 회차 도중 단계가 바뀌면 `Current phase`도 그때그때 갱신한다.
2. 완료조건 항목마다 회차 안 번호(`DOD-<n>`)와 안정 키를 함께 적는다. 안정 키는 `<검증 대상>-<검증 성질>` 꼴의 소문자 하이픈 낱말이다.
3. `Approved file scope`는 1회차에 사용자가 승인한 계획 문서의 "변경 대상 파일" 표에 적힌 경로 목록을 그대로 옮겨 적는다. 승인 시점에 따로 되묻지 않는다. 이후 회차에서 이 값을 늘리려면 사용자 확인이 필요하다.
4. `## 1회차 맥락` 절은 1회차에 한 번 채우고 이후 회차에서 지우지 않는다. 대화가 압축되어도 이 절만 읽으면 dh-dev 1-d 입력 계약을 다시 갖출 수 있어야 한다.
5. 기록 파일이 없거나 형식이 깨져 읽히지 않으면 새 기록 파일을 만들고 회차 번호를 1로 되돌린 뒤, 그 사실을 사용자에게 한 줄로 알린다. 깨진 파일은 지우지 않고 `**Status**: Corrupted`로 표시한다.

## 독립 검증 에이전트 (Verification Agent)

| 항목 | 규정 |
| --- | --- |
| 모델·강도 | `VERIFIER_MODEL` / `VERIFIER_EFFORT` |
| 스폰 방식 | dh-dev Agent & Model Policy의 스폰 방식을 그대로 따르되, 에이전트에 파일 읽기 도구와 명령 실행 도구를 반드시 포함한다. 파일 쓰기 도구는 주지 않는다 |
| 격리 | 실행 에이전트와 별개의 새 에이전트로 띄운다. 실행 에이전트 맥락을 물려받지 않는다(fork 금지). 실행과 검증을 같은 회차에 동시에 돌리지 않고 순서대로 돌린다 |
| 입력 | 계획 문서 경로, 완료조건 목록(번호+안정 키), 적대적 테스트 절, 변경 파일 목록, 실행자 주장 체크리스트(반드시 "주장"이라고 표시), 직전 회차 실패 이력 |
| 금지 | 실행자 주장만으로 합격 금지. 파일을 직접 읽거나 명령을 직접 돌려 확인한 것만 근거가 된다 |
| 출력 형식 | 첫 줄 `VERDICT: PASS` 또는 `VERDICT: FAIL`, 이어서 `항목 번호 \| 안정 키 \| 판정 \| 증거 \| failure_signature` 표 |

증거 칸은 실행한 명령과 출력 일부, 또는 `파일경로:줄번호` 인용이어야 한다. 합격 항목도 증거를 반드시 적는다. `failure_signature`는 합격 항목에서 빈칸, 불합격 항목에서 `<실패 유형>:<관측값>` 한 줄이다.

증거 누락 처리:

1. 오케스트레이터가 표의 각 합격 행을 확인해, 증거 칸이 비었거나 명령·파일 인용이 없으면 그 항목을 불합격으로 강등하고 `failure_signature`를 `no-evidence`로 적는다.
2. 응답에 표 자체가 없거나 첫 줄 판정이 없으면 `VERIFIER_RETRY`회까지 형식을 다시 지정해 재호출한다.
3. 재호출 후에도 형식을 못 갖추면 그 회차는 전체 불합격으로 처리하고, 모든 항목의 `failure_signature`를 `verifier-format-error`로 기록한다.

**목표 문장 변경 판정** — 검증과 별개로, 재계획이 끝날 때마다 오케스트레이터가 직접 한다. 에이전트에 맡기지 않는다.

1. 새 계획 문서의 목표 문장과 기록 파일 `Goal` 값을 꺼낸다.
2. 앞뒤 공백 제거와 연속 공백 축소만 하고 두 문자열을 견준다.
3. 다르면 자동 승인을 하지 않고 정지해 사용자를 부른다. 같으면 OV-1 조건 (가)를 충족한 것으로 본다.

## 정체 판정 (Stagnation Rule)

**같은 항목인가** — 안정 키가 같으면 같은 항목이다. 완료조건 문구가 바뀌어도, 회차 안 번호가 바뀌어도 안정 키가 같으면 같은 항목으로 본다. 재계획할 때 계획 에이전트에게 직전 회차의 안정 키 목록을 넘기고, 같은 것을 검증하는 항목에는 반드시 같은 안정 키를 다시 쓰라고 지시한다. 새 안정 키는 검증 대상이 실제로 새로 생겼을 때만 만든다. 미충족 항목을 재계획에서 지우는 것은 금지한다. 지워야 한다면 루프를 멈추고 사용자를 부른다.

**개선이 없었는가** — 아래 둘이 모두 참이면 그 항목의 연속 불합격 계수를 1 올린다.

1. 같은 안정 키가 이번 회차와 직전 회차 모두 불합격이다.
2. 두 회차의 `failure_signature`가 정규화 후 같다. 정규화는 앞뒤 공백 제거, 연속 공백 하나로 축소, 영문 소문자화, 숫자를 `#`로 치환하는 네 가지만 한다.

`failure_signature`가 다르면 진전이 있었다고 보고 그 항목의 연속 계수를 0으로 되돌린다. 다만 누적 불합격은 계속 올린다.

정지 조건 — 어느 항목의 연속 불합격이 `STAGNATION_LIMIT`에 이르면 정지한다. 보조 안전장치로, 실패 요지가 계속 바뀌더라도 어느 항목의 누적 불합격이 `CUMULATIVE_FAIL_LIMIT`에 이르면 정지한다(보고문에 "실패 양상이 계속 바뀌었으나 누적 한도 도달"이라고 밝힌다). 직전 회차 기록이 없는 1회차에서는 정체 판정을 하지 않는다.

정지 보고문에 담을 것: 목표 문장, 회차 수, 정체 항목의 안정 키와 완료조건 원문, 회차별 `failure_signature` 나열, 시도했다 실패한 접근 목록, 회차별 커밋 해시, 작업 브랜치 이름, 회차 기록 파일 경로.

**사용자 선택별 처리** — 보고 뒤 아래 세 선택지를 제시하고, 고른 대로만 움직인다.

| 선택 | 처리 |
| --- | --- |
| 계속 | 정체 항목의 연속 계수만 0으로 되돌리고 누적 계수는 그대로 둔다. 기록 파일 Status를 `Running`으로 되돌리고 다음 회차 재계획부터 재개한다. 누적 계수가 이미 `CUMULATIVE_FAIL_LIMIT`에 있으면 사용자에게 그 한도를 올릴지 한 번 더 묻고, 올리지 않으면 중단으로 처리한다 |
| 계획 수정 | 사용자가 준 수정 사항을 `## 재계획 입력`에 항목으로 더한다. 정체 항목의 연속·누적 계수를 둘 다 0으로 되돌린다. Status를 `Running`으로 되돌리고 재계획부터 재개한다 |
| 중단 | 기록 파일 Status를 `Stopped`로 확정하고 루프를 끝낸다. 작업 브랜치와 회차 커밋은 그대로 남긴다. plan_history의 해당 계획은 `Superseded`로 두고 Summary 앞에 `[dh-loop round N 검증 불합격]`을 붙인다 |

계수를 되돌리지 않고 재개하면 다음 회차에 곧바로 다시 정지하므로, "계속"에서 연속 계수 초기화는 필수다.

## 재계획 입력 (Replan Inputs)

2회차 이후 dh-dev 1-d 계획 에이전트에 아래를 추가로 넘긴다. 1번과 2번은 dh-dev 1-d가 요구하는 입력 계약을 무인 회차에서도 채우기 위한 것이다.

1. 회차 기록 파일 `## 1회차 맥락` 절의 dh-dev 1-a 분석 산출물 (경로 또는 요지)
2. 회차 기록 파일 `## 1회차 맥락` 절의 dh-dev 1-b 맥락 요약과 개발 방향
3. 목표 문장 (기록 파일 `Goal` 값 그대로)
4. 직전 회차의 불합격 항목 표 (번호, 안정 키, 완료조건 원문, 실패 요지, `failure_signature`)
5. 누적 "시도했다가 실패한 접근" 목록 전체
6. 직전 회차 계획 문서 경로
7. 합격 항목 목록과 "이미 충족 — 이번 회차에서는 되돌아가지 않았는지만 확인" 지시
8. 승인 파일 범위
9. 지시문: "직전 회차와 같은 접근을 되풀이하지 말 것. 되풀이가 불가피하면 이번에는 무엇이 다른지 한 줄로 적을 것."
10. 지시문: "직전 회차의 안정 키를 그대로 다시 쓸 것. 미충족 항목을 지우지 말 것."

## 커밋·브랜치 정책 (Commit and Branch Policy)

**브랜치**

- 루프는 1회차 승인 직후, 첫 실행 전에 `<LOOP_BRANCH_PREFIX><slug>` 브랜치를 만들어(`git checkout -b`) 그리로 옮긴다. 같은 이름이 이미 있으면 새로 만들지 않고 그 브랜치로 옮긴다. 이 방식은 `skills/autoresearch/SKILL.md`의 전용 브랜치 격리를 그대로 따르되 이름 앞머리만 다르다.
- 현재 브랜치가 `PROTECTED_BRANCHES` 안에 있으면 브랜치 전환 없이는 어떤 회차 커밋도 하지 않는다.
- 전환에 실패하면 정지하고 사용자를 부른다. 미커밋 변경은 전환 시 함께 따라온다.
- 브랜치 이름을 회차 기록 파일 `Working branch`에 남긴다. 매 커밋 전에 현재 브랜치가 그 값과 같은지 확인한다.
- 루프가 끝나도 dh-loop은 병합하지 않는다. 병합·되돌림은 사용자만 결정한다.

**커밋**

- 회차마다 커밋한다. 합격 회차든 불합격 회차든 마찬가지다.
- 실패한 회차의 변경은 되돌리지 않는다. 다음 회차가 그 위에서 고친다. 되돌림은 사용자만 결정한다.
- 회차별 커밋이 있으므로 어느 회차로든 사용자가 직접 돌아갈 수 있다. 정지 보고문에 회차별 커밋 해시를 넣는 이유가 이것이다.
- 커밋 제목 끝에 `(dh-loop round N)`을 붙여 회차를 구분한다.

## 중단과 재개 (Stop and Resume)

시작할 때 `LEDGER_DIR`를 훑어 `Running` 또는 `Paused`인 기록 파일을 찾는다.

| 찾은 개수 | 처리 |
| --- | --- |
| 0개 | 새 루프를 시작한다 |
| 1개 | Status를 `Paused`로 바꾸고 사용자에게 이어서 할지, 새로 시작할지, 끝낼지 묻는다 |
| 2개 이상 | 모두 `Paused`로 바꾸고 목록(파일 경로, 목표 문장, 회차, 작업 브랜치)을 보여준 뒤 어느 것을 이어갈지 사용자에게 고르게 한다. 고르지 않은 것은 `Paused`로 남긴다. 루프는 한 번에 하나만 돈다 |

이 물음은 루프가 돌기 전이므로 무인 규칙을 어기지 않는다. 이어서 하기로 하면 `Current phase`에 따라 재개한다. 재개 전에 `Working branch`로 옮긴다.

| 기록된 단계 | 재개 지점 |
| --- | --- |
| `plan` | 그 회차의 재계획부터 다시 |
| `execute` | 그 회차의 실행부터 다시 (부분 변경이 남아 있어도 실행 에이전트가 이어서 고침) |
| `verify` | 그 회차의 검증부터 다시 |
| `commit` | 그 회차의 커밋부터 다시. 이미 커밋되어 있으면 건너뛰고 다음 회차로 |

어느 경우든 회차 중간부터가 아니라 그 단계의 처음부터 다시 한다. 같은 단계를 두 번 돌려도 결과가 같도록 각 단계는 이전 산출물을 덮어쓴다.

## 예외 (Exceptions)

| 상황 | 처리 |
| --- | --- |
| `DHDEV_PATH` 문서를 읽을 수 없음 | 탐색 순서 (1) 작업 폴더 기준 `skills\dh-dev\SKILL.md` (2) 플러그인 설치 경로의 같은 파일 (3) 사용자에게 경로를 한 번 묻기. 셋 다 실패하면 절차를 짐작해 대신 수행하지 않고 즉시 중단 |
| 회차 기록 파일이 깨짐 | 새 파일을 만들고 회차 1부터. 깨진 파일은 `Corrupted`로 표시하고 남김 |
| `Running`·`Paused` 기록 파일이 2개 이상 | 목록을 보여주고 사용자가 하나를 고름. 나머지는 `Paused`로 남김 |
| 검증 응답 형식 위반 | `VERIFIER_RETRY`회 재호출 후 회차 전체 불합격 |
| 재계획이 승인 파일 범위를 벗어남 | `SCOPE_GUARD`가 `on`이면 정지하고 사용자에게 범위 확장을 확인. `off`면 기록만 남기고 진행 |
| 재계획이 목표 문장을 바꾸려 함 | 정지하고 사용자 호출 |
| 재계획에 미해결 `HIGH` 발견이 남음 | 자동 승인하지 않고 정지해 사용자에게 발견을 보임 |
| 보호 브랜치에서 루프를 시작함 | 전용 브랜치를 만들어 옮긴 뒤 진행. 전환 실패 시 정지 |
| `MAX_ROUNDS`에 도달 | 그 회차를 끝내고 사유 `round-limit`으로 정지, 정체 판정 선택 표 제시 |
| 커밋 실패 | 회차 기록에 남기고 다음 회차 진행. 정지하지 않음 |
| `git` 저장소가 아님 | 브랜치·커밋 단계를 건너뛰고 회차 기록에 `no-git`으로 남긴 뒤 계속 |
| 재정의 표의 대상 규칙이 dh-dev에서 사라짐 | 그 행을 적용하지 않고 사용자에게 한 줄로 알림 |
| 사용자가 중간에 끊음 | 다음 실행 때 `## 중단과 재개`로 재개 |

## 용어 정리

| 용어 | 뜻 |
| --- | --- |
| 개발 완료조건 | 참·거짓으로 판정할 수 있는 완료 판단 기준 목록 |
| 독립 검증 에이전트 | 실행 에이전트와 분리되어 완료조건 충족 여부만 판정하는 에이전트 |
| 보호 브랜치 | 무인 회차 커밋을 쌓으면 안 되는 브랜치. `main`과 `master` |
| 안정 키 | 완료조건 항목을 회차가 바뀌어도 같은 것으로 알아보게 하는 식별자 |
| 위임형 래퍼 | 절차 본문을 복제하지 않고 원본 문서를 읽어 그대로 수행하는 감싸개 |
| 작업 브랜치 | 루프가 회차 커밋을 쌓는 전용 브랜치. `dh-loop/<slug>` 꼴 |
| 정체 | 같은 항목이 개선 없이 되풀이해 불합격하는 상태 |
| 하드 게이트 | dh-dev Step 2처럼 사용자의 명시적 승인 없이는 다음 단계로 못 가게 막는 장치 |
| 회차 기록 파일 | 루프의 회차별 계획·판정·실패 이력을 남기는 저장소 안 마크다운 파일 |
