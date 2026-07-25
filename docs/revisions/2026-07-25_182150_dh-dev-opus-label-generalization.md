# dh-dev의 Opus 버전 표기를 범용 alias로 일반화

- **Date**: 2026-07-25 18:21:50
- **Author**: Claude (dh-dev 오케스트레이터)

## Rationale / Plan

2026-07-24 Claude Opus 5(`claude-opus-5`)가 출시됨을 웹 검색과 공식 문서(anthropic.com/news, platform.claude.com)로 확인 — Opus 4.8과 동일 가격($5/$25), Opus 4.8과 병행 운영(대체 아님). dh-dev의 모델 선택은 harness의 범용 alias(`opus`, `fable`)를 쓰며 서버 측에서 자동으로 최신 모델로 해석되므로 alias 자체는 이미 올바르게 Opus 5를 가리키지만, `skills\dh-dev\SKILL.md`의 Large 등급 Step 3 실행 모델 설명 텍스트 4곳에는 "Opus 4.8"이 하드코딩되어 있어 다음 Opus 갱신 때 또 낡은 텍스트가 될 상황이었음.

계획: `docs\plans\2026-07-25_153352_dh-dev-opus-label-generalization.md` (Status: In Progress → 본 개정 완료 후 Completed로 갱신 예정).

사용자가 "버전명 제거(alias로 일반화)"를 선택 — Medium 등급과 동일한 "Opus (`opus`)" 스타일로 통일해 향후 Opus 갱신 때마다 반복되는 문서 수정을 근본적으로 없앰. 직전 세션에서 구축한 모델 티어링 시스템의 첫 실사용 사례로, 1-c에서 Small 등급(Sonnet/standard)으로 판정되어 계획·실행 전 과정이 저비용 모델로 진행됨. 1-e Adversarial Plan Preview(contrarian+gap_hunter)에서 grep 검증 명령의 파일 스코프 누락(저장소 내 4개 역사 문서에 "Opus 4.8"이 합계 17건 정당하게 존재해 스코프 없는 grep이 거짓 실패를 유발할 뻔함) 등 6건(HIGH 4)을 발견 — 1-d 1회 재작성으로 전부 반영 후 승인.

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills\dh-dev\SKILL.md` | Modified | Large 등급 Step 3 모델 표기 4곳("Opus 4.8") → 버전 없는 "Opus"로 일반화 |

## Details

### `skills\dh-dev\SKILL.md` (Modified) — 4줄 변경(삽입 4 / 삭제 4)

- frontmatter description(3행): "Large default: Opus 4.8 at max reasoning effort" → "Large default: Opus at max reasoning effort"
- Agent & Model Policy 표, Step 3 Execute 행(28행): "Large (default): Opus 4.8 (`opus`)" → "Large (default): Opus (`opus`)"
- Model & Effort Tiering 표, Large 등급 행의 Step 3 Execute 컬럼(40행): "Opus 4.8 (`opus`) — `effort: \"max\"`" → "Opus (`opus`) — `effort: \"max\"`"
- Step 3 목록 항목 4(167행): "Large default: Opus 4.8, max reasoning effort" → "Large default: Opus, max reasoning effort"
- Medium 등급 행(41행)의 기존 "Opus (`opus`)" 표기 2건은 무변경(이미 올바른 스타일이었음)
- 그 외 라인(1-c/1-d/1-e 섹션, Step 2 hard gate, Exceptions 표 등)은 전부 무변경

## 검증 요약

Sonnet 실행 에이전트가 4개 DoD(`grep -c "Opus 4.8"`=0, `grep -o "Opus (\`opus\`)"` 카운트=4, `git diff --numstat`으로 삽입4/삭제4, `plan-context/references/planning-workflow.md` 무변경)를 전부 파일 스코프 한정 명령으로 검증해 PASS 보고. 오케스트레이터가 동일 4개 명령을 독립 재실행하고 `git diff` 전체 출력을 육안으로 재확인하여 정확히 계획된 4줄만 변경되고 Medium 등급 등 다른 내용은 전혀 손상되지 않았음을 확인.
