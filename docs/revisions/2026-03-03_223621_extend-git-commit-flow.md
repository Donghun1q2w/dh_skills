# revision-tracker Section 5 "Git Commit" 기능 확장

- **Date**: 2026-03-03 22:36:21
- **Author**: Claude (agent)

## Rationale / Plan

사용자가 revision-tracker 스킬의 Section 5를 확장 요청. 기존에는 커밋 명령어를 텍스트로 제안만 하고 "Do not execute the commit"이라고 명시되어 있었다. 이를 3단계 인터랙티브 워크플로우(제안 → 사용자 확인 → 실행/건너뛰기)로 변경하여, 승인 시 실제 git commit을 실행하도록 개선.

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills/revision-tracker/SKILL.md` | Modified | Section 5를 "Suggest Git Commit"에서 "Git Commit"으로 이름 변경, 3단계 인터랙티브 커밋 흐름으로 교체 |

## Details

### `skills/revision-tracker/SKILL.md` (Modified)

- Section 5 제목 변경: "Suggest Git Commit" → "Git Commit"
- 도입부 변경: "suggest a commit at the end of the revision log output" → "propose a commit after logging the revision"
- 기존 단일 제안 포맷 블록 삭제 ("Suggested commit:" + "Do not execute the commit" 문구)
- 3단계 서브섹션 추가:
  - **Step 1: Present the commit proposal** — "Proposed commit:" 포맷으로 제안 표시
  - **Step 2: Ask the user** — Commit / Edit then commit / Skip 3가지 선택지 제공
  - **Step 3: Execute or skip** — 승인 시 `git add` + `git commit` 실행 후 커밋 해시 보고, 건너뛰기 시 제안만 남김
