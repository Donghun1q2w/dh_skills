# dh-dev Opus 버전 표기 일반화

- **Date**: 2026-07-25 15:33:52
- **Status**: Completed

---

## 1. Requirements Summary

dh-dev/SKILL.md에서 Large 등급 Step 3 실행 모델을 가리키는 "Opus 4.8" 버전 명시 표기를 Medium 등급과 동일한 범용 "Opus (`opus`)" alias 표기로 일반화. Alias 자체는 변경 대상 아님, 사람이 읽는 텍스트의 하드코딩된 버전만 제거.

**배경**: 2026-07-24에 Claude Opus 5(`claude-opus-5`)가 Opus 4.8과 동일 가격($5/$25)으로, Opus 4.8과 병행 운영되는 형태로 출시됨(공식 문서 확인 완료). dh-dev의 모델 선택은 harness의 범용 alias(`opus`, `fable` 등)를 사용하며 이는 서버 측에서 자동으로 최신 모델로 해석되므로 이미 올바르게 동작 중 — 문제는 사람이 읽는 설명 텍스트에 "Opus 4.8"이 하드코딩되어 있어 다음 Opus 갱신 때 또 낡은 텍스트가 되는 것.

**티어 판정(1-c)**: Tier: Small — rationale: 단일 파일(skills/dh-dev/SKILL.md), 예상 8줄 미만 변경, 버전 문자열 치환뿐(신규 로직 없음), 위험 키워드 없음 → Sonnet/standard

## 2. Acceptance Criteria

대상 파일: `skills\dh-dev\SKILL.md` — **모든 grep/diff 검증은 이 파일 하나로 스코프를 한정**한다. Baseline: 파일 내 "Opus 4.8" 정확히 4건(3, 28, 40, 167행). 변경 후: 4곳 모두 "Opus"로 치환, 파일 내 "Opus 4.8" 매치 0, `` Opus (`opus`) `` 매치 4건(기존 41행 Medium 행 2건 + Edit 2·Edit 3으로 신규 생성 2건), 다른 라인 무변경. 참고: 저장소 전체를 스코프 없이 grep하면 4개 역사 문서(docs\plans, docs\revisions 하위)에 "Opus 4.8" 합계 17건이 별도로 존재하지만 이는 애초부터 변경/검증 대상이 아니다 — 상세는 섹션 5 DoD-5 참조.

## 3. Implementation Steps (구현 지침)

Edit 도구로 아래 4건을 각각 독립적으로 수행한다. old_string은 파일 내 고유 앵커이며 exact-match여야 한다. `replace_all`은 사용하지 않는다.

**Edit 1** (3행, frontmatter description 부분 문자열):
- old_string: `Large default: Opus 4.8 at max reasoning effort`
- new_string: `Large default: Opus at max reasoning effort`

**Edit 2** (28행, 해당 셀 내 부분 문자열만 — Step 3 Execute 컬럼 셀 내부, 표 나머지 무변경):
- old_string: `Large (default): Opus 4.8 (\`opus\`)`
- new_string: `Large (default): Opus (\`opus\`)`

**Edit 3** (40행, Step 3 컬럼 셀 내 부분 문자열):
- old_string: `Opus 4.8 (\`opus\`) — \`effort: "max"\``
- new_string: `Opus (\`opus\`) — \`effort: "max"\``

**Edit 4** (167행):
- old_string: `Large default: Opus 4.8, max reasoning effort`
- new_string: `Large default: Opus, max reasoning effort`

## 4. Code Writing Guide (코드 작성 가이드)

- 파일 인코딩 UTF-8 유지, BOM 추가 금지
- 이모지 및 "§" 특수문자 사용 금지
- 표(Markdown table) 행 편집 시 파이프(`|`) 개수와 컬럼 정렬 유지 — 백틱(`` ` ``) 짝 깨짐 주의 (특히 28·40행의 `` `opus` `` 인라인 코드 표기)
- 3행은 frontmatter YAML의 한 줄 문자열 값 내부이므로, 큰따옴표(`"`)로 감싸인 라인 전체 구조를 건드리지 말고 내부 부분 문자열만 치환

## 5. Definition of Done (개발 완료조건)

1. `grep -c "Opus 4.8" skills\dh-dev\SKILL.md` = 0
2. `grep -o "Opus (\`opus\`)" skills\dh-dev\SKILL.md` 매치 수 = 4 (기존 41행 Medium 행 2건 + Edit 2·Edit 3으로 신규 생성 2건)
3. `skills\dh-dev\SKILL.md` 기준 git diff에서 정확히 4개 라인만 변경(삽입 4 / 삭제 4)
4. `skills\plan-context\references\planning-workflow.md` 무변경(원래 "Opus 4.8" 없었음)
5. (스코프 명시) `docs\plans\2026-07-23_105547_dh-dev-model-effort-tiering.md`(11건), `docs\revisions\2026-07-23_141226_dh-dev-model-effort-tiering.md`(3건), `docs\plans\2026-07-22_211702_dh-dev-planning-stage-ouroboros-interview.md`(1건), `docs\revisions\2026-07-22_213825_dh-dev-planning-stage-ouroboros-interview.md`(2건) — 이 4개 역사 문서의 "Opus 4.8" 합계 17건(그중 2026-07-23_105547 문서는 `` Opus (`opus`) `` 패턴도 2건 보유)은 애초부터 변경 대상이 아니며, 모든 grep을 `skills\dh-dev\SKILL.md` 단일 파일로 스코프를 한정하므로 검사 대상에서 자동 제외된다.

## 6. Adversarial Test Environment (적대적 테스트 환경)

1. `grep -n "Opus 4.8" skills\dh-dev\SKILL.md` → 빈 결과 확인 (DoD-1 검증; 파일 스코프 한정이므로 역사 문서 4건·17건은 집계되지 않음)
2. `grep -o "Opus (\`opus\`)" skills\dh-dev\SKILL.md | wc -l` → 4 확인 (DoD-2 직접 검증). 참고: "Opus"가 등장하는 라인은 3·28·40·41·167의 5개 라인이며, 41행에서 패턴이 2회 매치되어 occurrence 합계가 6이 되는 것일 뿐 라인 수 자체는 5다.
3. `git diff --numstat skills\dh-dev\SKILL.md` → 삽입 4 / 삭제 4 확인 (DoD-3 검증)
4. `git diff --stat -- skills\plan-context\references\planning-workflow.md` → 빈 결과 확인 (DoD-4 검증)

## 7. Risks and Mitigations

- YAML frontmatter 따옴표/괄호 깨짐 위험 → old_string을 문장 중간 부분 문자열로 정확히 지정
- 표 행 다른 컬럼 오염 위험 → old_string을 행 전체가 아닌 해당 셀 내부 부분 문자열로 지정
- grep 스코프 누락으로 인한 역사 문서 오탐 위험 → 모든 grep/diff 명령에 `skills\dh-dev\SKILL.md` 파일 경로를 명시적으로 고정

## 8. Verification Steps

Edit 1-4 적용 → `grep -c "Opus 4.8" skills\dh-dev\SKILL.md` = 0 확인 → `grep -o "Opus (\`opus\`)" skills\dh-dev\SKILL.md | wc -l` = 4 확인 → `git diff --numstat skills\dh-dev\SKILL.md`로 삽입 4/삭제 4 확인 → `git diff --stat -- skills\plan-context\references\planning-workflow.md` 빈 결과 재확인 → DoD 1-5 전항목 판정

---

## 부록: 1-e Adversarial Plan Preview 검토 노트 (검토 노트)

contrarian·gap_hunter 두 레인이 초안을 검토해 6건(HIGH 4, MEDIUM 2)을 발견 — 주로 grep/diff 검증 명령의 파일 스코프 누락(저장소 내 4개 역사 문서에 "Opus 4.8" 합계 17건이 정당하게 존재해 스코프 없는 grep이 거짓 실패를 유발), DoD-테스트 매핑 불완전(Test-2/3이 대응 DoD의 정확한 수치를 검증 못함, DoD-4는 테스트 자체가 누락)이었음. 1-d를 1회 재작성해 전부 반영 — **미해결 HIGH 없음**.

| 발견 ID | 심각도 | 조치 |
| --- | --- | --- |
| HIGH-1 | HIGH | 모든 grep(DoD-1·2, Test-1·2)에 `skills\dh-dev\SKILL.md` 파일 경로 명시, DoD-5에 4개 역사 문서 스코프 제외 사유 기재 |
| HIGH-2 | HIGH | Test-2를 `grep -o "Opus (\`opus\`)" | wc -l` = 4 검증으로 교체, "6건 라인" 주장 삭제 및 실제 라인 수(5) 명시 |
| HIGH-3 | HIGH | Test-3을 `git diff --numstat`으로 교체해 삽입 4/삭제 4를 정확히 검증 |
| HIGH-4 | HIGH | Test-4 신규 추가: `git diff --stat -- skills\plan-context\references\planning-workflow.md` 빈 결과 확인(DoD-4 대응) |
| MEDIUM-1 | MEDIUM | Edit 2 라벨을 "해당 셀 내 부분 문자열만"으로 정정 |
| MEDIUM-2 | MEDIUM | Acceptance Criteria 문장의 미정리된 사고 흔적("아니") 제거, 확정 문장으로 재작성 |

미해결 HIGH: 없음.
