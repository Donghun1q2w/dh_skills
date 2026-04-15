# dh-wiki 독립 로컬 MCP 서버 구축

- **Date**: 2026-04-15 15:00:00
- **Author**: Claude (dh-dev orchestrator)

## Rationale / Plan

OMC 플러그인(`oh-my-claudecode`)의 wiki 기능을 독립 로컬 MCP 서버로 포팅. 사용자 요구: (1) 저장 경로를 `.omc/wiki/` → `docs/wiki/`로 변경하여 git 추적 가능하게, (2) OMC 없는 환경에서도 독립 구동 가능하게.

계획 문서: `docs/plans/2026-04-15_150000_dh-wiki-local-mcp-server.md`

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills/dh-wiki/SKILL.md` | Modified | 경로를 `docs/wiki/`로 변경, frontmatter 수정, OMC 의존성 제거 문구 추가 |
| `skills/dh-wiki/mcp-server/package.json` | Added | MCP 서버 프로젝트 정의 (`@modelcontextprotocol/sdk`, `zod`) |
| `skills/dh-wiki/mcp-server/index.mjs` | Added | MCP 서버 진입점 — 7개 도구 등록 (stdio transport) |
| `skills/dh-wiki/mcp-server/types.mjs` | Added | 상수/카테고리 정의 (OMC types.ts 포팅) |
| `skills/dh-wiki/mcp-server/storage.mjs` | Added | 파일 I/O 레이어 — `docs/wiki/` 경로, OMC 유틸 제거 |
| `skills/dh-wiki/mcp-server/ingest.mjs` | Added | 지식 수집/병합 로직 (append strategy) |
| `skills/dh-wiki/mcp-server/query.mjs` | Added | 키워드+CJK bi-gram 검색 |
| `skills/dh-wiki/mcp-server/lint.mjs` | Added | 위키 헬스체크 (orphan, stale, broken-ref 등) |
| `skills/dh-wiki/hooks/session-start.mjs` | Added | SessionStart hook — wiki 컨텍스트 주입 |
| `skills/dh-wiki/hooks/pre-compact.mjs` | Added | PreCompact hook — 압축 전 wiki 요약 주입 |
| `skills/dh-wiki/hooks/session-end.mjs` | Added | SessionEnd hook — 세션 로그 자동 캡처 |
| `hooks/hooks.json` | Added | 플러그인 루트 hook 등록 (3개 wiki hook) |
| `.mcp.json` | Added | 프로젝트 MCP 서버 등록 (`dh-wiki`) |
| `docs/plans/2026-04-15_150000_dh-wiki-local-mcp-server.md` | Added | 계획 문서 |
| `docs/plan_history.md` | Modified | 계획 인덱스에 항목 추가 |

## Details

### `skills/dh-wiki/SKILL.md` (Modified)

- 경로 설명을 `.omc/wiki/` → `docs/wiki/`로 변경
- 카테고리에 `reference`, `convention` 추가
- Auto-Capture 설명 단순화, Hard Constraints에 standalone MCP 문구 추가

### `skills/dh-wiki/mcp-server/storage.mjs` (Added)

- OMC `getOmcRoot()` → `join(root, WIKI_ROOT)` 환경변수 기반 경로로 교체
- OMC `atomicWriteFileSync()` → `fs.writeFileSync()` 단순화
- OMC `withFileLockSync()` 제거 (단일 프로세스 MCP 서버)
- git-ignore 자동 생성 로직 제거 (git 추적이 목적)
- 나머지 API (parseFrontmatter, serializePage, titleToSlug 등) 그대로 포팅

### `skills/dh-wiki/mcp-server/index.mjs` (Added)

- `@modelcontextprotocol/sdk` 기반 stdio MCP 서버
- 7개 도구: wiki_ingest, wiki_query, wiki_lint, wiki_add, wiki_list, wiki_read, wiki_delete
- `PROJECT_ROOT` 환경변수 또는 `process.cwd()`를 프로젝트 루트로 사용

### `skills/dh-wiki/hooks/*.mjs` (Added)

- OMC `session-hooks.ts`의 3개 함수를 독립 스크립트로 포팅
- `getClaudeConfigDir()` 제거, `feedProjectMemory()` 제거
- config 로딩: `wiki.config.json` 로컬 파일 기반으로 변경

### `hooks/hooks.json` (Added)

- dh-skills 플러그인 루트 레벨 hook 등록 파일 (최초 생성)
- SessionStart, PreCompact, SessionEnd 3개 이벤트에 wiki hook 등록
