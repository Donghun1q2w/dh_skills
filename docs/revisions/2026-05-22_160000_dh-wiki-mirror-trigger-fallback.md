# dh-wiki .md 미러링 트리거 전환 (FileChanged → PostToolUse + Stop)

- **Date**: 2026-05-22 16:00:00
- **Plan**: [2026-05-22_153000_dh-wiki-hooks-rework.md](../plans/2026-05-22_153000_dh-wiki-hooks-rework.md) (Resolution 섹션)

## Summary

런타임 검증 결과 `FileChanged` 이벤트는 matcher가 리터럴 파일명 화이트리스트라 `*.md` 와일드카드 미러링에 부적합함을 확인. 계획 Step 1의 폴백(대안 2)인 `PostToolUse(Edit|Write|MultiEdit)` + `Stop` 조합으로 전환하고, append-merge 부적합 문제 해결 위해 write 전략을 `writePage` 덮어쓰기로 변경.

## Rationale / Plan

- `FileChanged.matcher: ""` 등록 후 신규 `.md` 생성 → hook 미발화 확인
- `claudehooks.md`: "FileChanged matcher 값은 정규식으로 평가되지 않고 리터럴 파일 이름으로 분할" — 빈 matcher = 빈 watch list = 영구 미발화
- 폴백 채택: PostToolUse(Edit|Write|MultiEdit) 즉시 동기화 + Stop 턴 종료 시 git scan 안전망
- 추가 발견: `ingestKnowledge`는 동일 페이지에 대해 매번 `## Update (timestamp)` 섹션을 append → 미러에는 부적합. `storage.writePage` 직접 호출로 덮어쓰기 전환
- Orphan sweep 추가: untracked 원본 삭제는 git status에 잡히지 않으므로, Stop 시 mirror 페이지의 `sources`가 실재하는지 검사하여 부재 시 자동 삭제

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `hooks/hooks.json` | modified | `FileChanged` 블록 제거, `PostToolUse(Edit\|Write\|MultiEdit)` + `Stop` 블록 추가 |
| `skills/dh-wiki/hooks/dh-wiki-file-changed.mjs` | modified | (1) `ingestKnowledge` → `storage.writePage` 직접 호출, (2) Stop event에서 `git status --porcelain` 스캔, (3) `sweepOrphans()` 추가 — mirrored 페이지 중 sources가 디스크에 없으면 자동 삭제 |
| `skills/dh-wiki/SKILL.md` | modified | Auto-Mirror 섹션 트리거를 PostToolUse+Stop으로, write 전략·FileChanged 거부 사유 명시 |
| `docs/plans/2026-05-22_153000_dh-wiki-hooks-rework.md` | modified | Resolution 섹션 추가 — 검증 결과와 폴백 채택 기록 |

## Details

### hooks/hooks.json

- 제거: `FileChanged` 블록
- 추가:
  - `PostToolUse`: `matcher: "Edit|Write|MultiEdit"`, timeout 10s
  - `Stop`: matcher 없음(이벤트는 모든 발생에서 발화), timeout 15s

### dh-wiki-file-changed.mjs

- `mirrorUpsert`: 기존 `ingestKnowledge` 호출 → 페이지 객체 직접 구성 후 `storage.writePage(root, page)` + `appendLog` 명시 호출. 매번 깨끗한 덮어쓰기
- `gitScanChanges(root)`: Stop event용. `git status --porcelain` 파싱하여 `.md` 변경(modify/delete) 수집. 비-git 환경에서는 빈 배열 반환
- `sweepOrphans(storage, root)`: `readAllPages`로 wiki 전체 순회, `tags`에 `"mirrored"` 포함하고 `sources[0]`의 절대 경로가 `existsSync` 실패면 `deletePage` + log
- `main()`: payload에서 changes 추출 → 0개이고 `hook_event_name === "Stop"`이면 git scan으로 폴백 → 모든 처리 후 Stop 이벤트라면 orphan sweep 추가 실행

### SKILL.md Auto-Mirror

- 섹션 제목에서 `(FileChanged)` 제거
- 트리거 두 종(PostToolUse / Stop) 각각 역할 명시
- write 전략, orphan sweep, FileChanged 거부 사유 추가

## Verification

- `node --check` 통과
- `hooks.json` JSON parse 통과
- 시뮬레이션 1 — PostToolUse Write payload(`tool_input.file_path`): `tmp/hook-test.md` 생성 → `hook-test-6ad278.md` mirror 페이지 정상 생성
- 시뮬레이션 2 — Stop payload(빈 페이로드): git scan으로 untracked `docs/claudehooks.md`, `docs/dh-wiki-workflow-report.md` 각각 mirror 생성됨
- 시뮬레이션 3 — orphan sweep: `tmp/hook-test.md` 삭제 후 Stop 재실행 → log에 `swept orphan page (source tmp/hook-test.md gone)` 기록, `hook-test-6ad278.md` 제거됨
- 실제 Claude Code 발화는 다음 세션 재시작 후 `/hooks` 메뉴에서 PostToolUse/Stop 등록 확인 필요
