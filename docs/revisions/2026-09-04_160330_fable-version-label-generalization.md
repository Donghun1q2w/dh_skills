# dh-dev 문서의 'Fable 5' 버전 표기를 버전 없는 'Fable'로 일반화

- **Date**: 2026-09-04 16:03:30
- **Author**: Claude Code (dh-dev 워크플로)

## Rationale / Plan

사용자 요청: 등록된 스킬에서 모델명을 지정할 때 버전 숫자를 빼고 제품군 이름만 쓰도록 정리.

`skills/` 아래 문서에는 `Fable 5`라는 버전 박힌 표기가 4곳 남아 있었다. 도구가 실제로 받는 값은
백틱 alias(`fable`, `opus`, `sonnet`)이고 이 alias는 harness가 최신 모델로 해석하므로, 버전 숫자는
사람이 읽는 설명 텍스트에만 존재하는 낡을 값이었다. Fable 모델이 갱신될 때마다 문서를 다시 고쳐야
하는 상황을 없애기 위해 버전 숫자를 뺐다.

2026-07-25에 같은 목적으로 `Opus 4.8` → ``Opus (`opus`)`` 일반화를 한 선례가 있으며
(`docs/revisions/2026-07-25_182150_dh-dev-opus-label-generalization.md`), 이번 변경도 같은 표기
규칙(버전 숫자 없는 제품군 이름 + 백틱 alias)을 따랐다.

계획서: `docs/plans/2026-09-04_152646_fable-version-label-generalization.md`
개발 방향: 단발성(one-off). 1-e 적대적 검증에서 HIGH 2건(무관한 미커밋 변경 때문에 경로 한정 없는
`git diff` 검증이 항상 실패, `--numstat` 파일별 기대값 오류)이 나와 1회 재작성으로 반영했다.

범위 밖으로 두어 손대지 않은 것: 백틱 alias 문자열, `docs/`의 과거 기록, `node_modules/`,
`skills/load-API-key/references/usage_example.py`의 API 모델 ID(사용자가 명시적으로 제외).

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills/dh-dev/SKILL.md` | Modified | 3·26·40행의 `Fable 5` → `Fable` |
| `skills/plan-context/references/planning-workflow.md` | Modified | 21행의 `Fable 5` → `Fable` |
| `docs/plans/2026-09-04_152646_fable-version-label-generalization.md` | Added | 계획서 |
| `docs/plan_history.md` | Modified | 계획 인덱스 항목 추가 |
| `docs/revisions/2026-09-04_160330_fable-version-label-generalization.md` | Added | 이 개정 기록 |
| `docs/revision_history.md` | Modified | 개정 인덱스 항목 추가 |

## Details

### `skills/dh-dev/SKILL.md` (Modified)

- 3행 frontmatter `description`: `Large: Fable 5 at max reasoning effort` → `Large: Fable at max reasoning effort`
- 26행 Agent & Model Policy 표: ``Large: Fable 5 (`fable`)`` → ``Large: Fable (`fable`)``
- 40행 Model & Effort Tiering 표 Large 행: ``Fable 5 (`fable`); fallback `opus``` → ``Fable (`fable`); fallback `opus```
- 백틱 alias `` `fable` ``는 두 곳 모두 그대로 유지(도구 호출 값)

### `skills/plan-context/references/planning-workflow.md` (Modified)

- 21행: `Large default: Fable 5, max reasoning effort` → `Large default: Fable, max reasoning effort`

## 검증

문서 전용 변경이므로 `/simplify`는 실행하지 않았다(스킵 조건: 문서·설정 파일만 변경).
계획서 8절 검증 절차를 실행하고 오케스트레이터가 결과를 다시 확인했다.

| 항목 | 결과 |
|---|---|
| `grep -rniE "fable ?5" skills/ --exclude-dir=node_modules` 잔여 건수 | 0 (변경 전 4) |
| `git diff --numstat` (대상 2개 파일 한정) | `3 3` SKILL.md / `1 1` planning-workflow.md, 합계 4 4 |
| `` `fable` `` alias 잔존 | 2회 (변경 전과 동일) |
| `Fable` 단어 총 등장 | 4회 (변경 전과 동일) |
| 26·40행 표 구분자 `|` 개수 | 각 5개 (변경 전과 동일) |
| frontmatter 3행 한국어 | `단발성/간단한/심화`, `기능 개선` 정상, 깨짐 문자 없음 |
| 두 파일 총 행 수 | 236행 / 221행 (변경 전과 동일) |
| 범위 밖 파일 | 작업 전 `git status` 기준선 대비 새로 바뀐 파일은 대상 2개뿐 |

Definition of Done 10개 항목 전부 합격.
