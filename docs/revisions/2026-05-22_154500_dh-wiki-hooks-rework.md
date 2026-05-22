# dh-wiki Hook 이벤트 재구성

- **Date**: 2026-05-22 15:45:00
- **Plan**: [2026-05-22_153000_dh-wiki-hooks-rework.md](../plans/2026-05-22_153000_dh-wiki-hooks-rework.md)

## Summary

dh-wiki 플러그인의 hook 라이프사이클을 재편성. `SessionStart` → `UserPromptSubmit` 이관, `SessionEnd` 폐기, 신규 `FileChanged` hook으로 임의 `.md` 변경을 `docs/wiki/`에 자동 미러링.

## Rationale / Plan

- 사용자 요청: 매 프롬프트마다 최신 wiki 상태 인지(SessionStart→UserPromptSubmit), 세션 종료 자동 캡처 중단(SessionEnd 삭제), 그리고 프로젝트 내 일반 `.md` 문서들을 wiki와 통합(FileChanged 미러링)
- 제외 대상: `docs/plans/**`, `docs/revisions/**`, `*history.md`, `docs/wiki/**`, `node_modules/**`, 그리고 경로 세그먼트가 `.`으로 시작하는 모든 폴더(`.git/`, `.omc/`, `.obsidian/`, `.claude/` 등)
- 슬러그는 `<file stem> (<6-char path hash>)`로 통일하여 upsert/delete 양쪽이 동일한 wiki 파일명을 가리키도록 보장

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `hooks/hooks.json` | modified | SessionStart/SessionEnd 블록 제거, UserPromptSubmit/FileChanged 블록 추가, PreCompact 유지 |
| `skills/dh-wiki/SKILL.md` | modified | "Auto-Capture" 섹션 제거, "Auto-Mirror (FileChanged)" 섹션 추가 |
| `skills/dh-wiki/hooks/dh-wiki-session-start.mjs` | deleted | UserPromptSubmit hook으로 이관됨 |
| `skills/dh-wiki/hooks/dh-wiki-session-end.mjs` | deleted | 자동 세션 로그 캡처 폐기 |
| `skills/dh-wiki/hooks/dh-wiki-user-prompt-submit.mjs` | added | wiki 컨텍스트를 매 프롬프트마다 주입 (페이로드 축약: 페이지 수 + 상위 5줄) |
| `skills/dh-wiki/hooks/dh-wiki-file-changed.mjs` | added | `.md` 변경을 wiki 페이지로 미러링/삭제 |
| `docs/plans/2026-05-22_153000_dh-wiki-hooks-rework.md` | added | 신규 계획 문서 |
| `docs/plan_history.md` | modified | 신규 계획 항목 등록 (Status: In Progress) |

## Details

### hooks/hooks.json

- 제거: `SessionStart` 블록, `SessionEnd` 블록
- 추가: `UserPromptSubmit` (matcher 비움, timeout 5s), `FileChanged` (matcher 비움, timeout 10s)
- 유지: `PreCompact`

### skills/dh-wiki/hooks/dh-wiki-user-prompt-submit.mjs (신규)

- 기존 SessionStart 로직 기반, `hookEventName`을 `UserPromptSubmit`으로 변경
- 페이로드 축약: `[LLM Wiki: N pages...]` + index.md 상위 5줄 (기존 30줄에서 축소)
- `docs/wiki/`가 없거나 페이지 0개면 조용히 통과

### skills/dh-wiki/hooks/dh-wiki-file-changed.mjs (신규)

- stdin 페이로드 다중 스키마 지원: `file_path`, `paths[]`, `tool_input.file_path`, `changes[]`
- 필터: `.md` 확장자, 경로 세그먼트 dot-시작 제외, `docs/plans|revisions|wiki/**` 제외, `*history.md` 제외, `node_modules/**` 제외
- 슬러그 통일: `buildMirrorTitle(relPath) = "<stem> (<6-char hash>)"` — upsert/delete가 같은 슬러그 도출
- ingest/storage 모듈은 동적 `import()`로 mcp-server 코드 재사용
- 모든 예외는 stderr 로그 후 `{continue: true, suppressOutput: true}` 반환 (사용자 프롬프트 비차단)

### skills/dh-wiki/SKILL.md

- `## Auto-Capture` 섹션 삭제 (SessionEnd 폐기)
- `## Auto-Mirror (FileChanged)` 섹션 신설 — 트리거, 제외 경로, 슬러그 규약, 카테고리·태그 명시

## Verification

- `node --check` 통과: `dh-wiki-user-prompt-submit.mjs`, `dh-wiki-file-changed.mjs`
- `hooks/hooks.json` JSON parse 통과
- Smoke test:
  - FileChanged with 6 excluded paths(`docs/plans/`, `docs/revisions/`, `*history.md`, `.obsidian/`, `node_modules/`, `docs/wiki/`) → `suppressOutput: true`로 정상 단락
  - UserPromptSubmit → `hookEventName: "UserPromptSubmit"` + 9페이지 컨텍스트 정상 주입
- 런타임 검증(계획 Step 5)은 Claude Code 재시작 후 `/hooks` 메뉴에서 등록 상태와 실제 발화를 확인해야 완료
