# dh-wiki 독립 로컬 MCP 서버 구축

- **Date**: 2026-04-15 15:00:00
- **Status**: Completed

## Summary

OMC 플러그인의 wiki 기능을 독립 로컬 MCP 서버로 포팅하여 `docs/wiki/` 경로에 마크다운 기반 지식 베이스를 운영한다. OMC 의존성 없이 `@modelcontextprotocol/sdk` 기반 stdio 서버로 7개 도구(wiki_add, wiki_ingest, wiki_query, wiki_list, wiki_read, wiki_delete, wiki_lint)를 제공한다.

## Background

- 현재 wiki 기능은 OMC 플러그인(`oh-my-claudecode`)의 MCP 서버에 번들되어 제공됨
- 저장 경로가 `.omc/wiki/`로 고정되어 있고, git-ignored 기본 정책
- 사용자 요구: (1) `docs/wiki/`에 저장하여 git 추적 가능하게, (2) OMC 없는 환경에서도 독립 구동
- OMC 소스 분석 결과, wiki 로직은 6개 TypeScript 파일(types, storage, ingest, query, lint, session-hooks)로 구성되며, OMC 의존은 유틸리티 4개(`getOmcRoot`, `atomicWriteFileSync`, `withFileLockSync`, `getClaudeConfigDir`)뿐

## Proposal

### Step 1: 프로젝트 초기화

`skills/dh-wiki/mcp-server/` 디렉토리에 Node.js ESM 프로젝트 생성

- `package.json` — `@modelcontextprotocol/sdk`, `zod` 의존
- 진입점: `index.mjs` (stdio transport)

### Step 2: 핵심 모듈 포팅 (OMC → 독립)

| 원본 (OMC) | 포팅 파일 | 변경 사항 |
|---|---|---|
| `types.ts` | `types.mjs` | 그대로 (타입→JSDoc/순수 JS 상수) |
| `storage.ts` | `storage.mjs` | `getOmcRoot()` → `join(root, WIKI_ROOT_ENV)`, `atomicWriteFileSync` → `writeFileSync`, `withFileLockSync` → 제거 |
| `ingest.ts` | `ingest.mjs` | import 경로만 변경 |
| `query.ts` | `query.mjs` | import 경로만 변경 |
| `lint.ts` | `lint.mjs` | import 경로만 변경 |

### Step 3: MCP 서버 구현 (index.mjs)

- `McpServer` + `StdioServerTransport`로 서버 생성
- 7개 도구를 `server.tool()`로 등록
- 경로 설정: 환경변수 `WIKI_ROOT` (기본값: `docs/wiki`)
- 원본 `wiki-tools.ts`의 handler 로직 포팅

### Step 4: SKILL.md 업데이트

- 경로 설명을 `docs/wiki/`로 변경
- MCP 도구명 프리픽스 안내 추가
- frontmatter YAML 오류 수정

### Step 5: Hook 내재화

dh-skills 플러그인의 `hooks.json`에 wiki 전용 hook 3개를 등록한다. OMC의 hook 스크립트를 독립 스크립트로 포팅.

| Hook 이벤트 | 스크립트 | 역할 |
|---|---|---|
| `SessionStart` | `skills/dh-wiki/hooks/session-start.mjs` | wiki 존재 시 index 요약을 컨텍스트로 주입 |
| `PreCompact` | `skills/dh-wiki/hooks/pre-compact.mjs` | 압축 전 wiki 페이지 수/카테고리/최종 업데이트 요약 주입 |
| `SessionEnd` | `skills/dh-wiki/hooks/session-end.mjs` | autoCapture 설정 시 세션 로그 자동 캡처 |

**OMC 의존 제거 방법:**
- `session-hooks.ts`의 3개 함수(`onSessionStart`, `onSessionEnd`, `onPreCompact`)를 순수 JS로 포팅
- `getOmcRoot()` → MCP 서버와 동일한 `docs/wiki` 경로 사용
- `getClaudeConfigDir()` → 제거 (config는 환경변수 또는 프로젝트 루트 `wiki.config.json`으로 대체)
- `feedProjectMemory()` → 제거 (OMC project-memory 전용 기능)
- Hook 등록: `skills/dh-wiki/hooks/hooks.json` 파일 생성

### Step 6: MCP 등록 및 통합 테스트

- 프로젝트 루트 `.mcp.json`에 `dh-wiki` 서버 등록
- `npm install` 실행하여 의존성 설치
- Hook 동작 확인 (SessionStart 시 컨텍스트 주입 로그 확인)

## Impact

| Area | Description |
|------|-------------|
| Files | `skills/dh-wiki/SKILL.md` (수정), `skills/dh-wiki/mcp-server/*` (신규 6개 파일), `skills/dh-wiki/hooks/*` (신규 4개 파일), `.mcp.json` (수정/신규) |
| Dependencies | `@modelcontextprotocol/sdk` ^1.12.1, `zod` ^3.24.0 (npm 패키지) |
| Risk | 낮음 — 기존 OMC wiki 도구와 도구명 충돌 가능 (`wiki_add` vs `mcp__dh-wiki__wiki_add`). 프리픽스로 구분되므로 공존 가능. Hook은 OMC hook과 독립적으로 동작하며, wiki 디렉토리가 다르므로(`docs/wiki` vs `.omc/wiki`) 데이터 충돌 없음 |

## Acceptance Criteria

1. `npm start`로 MCP 서버가 정상 기동됨
2. Claude Code에서 `dh-wiki` MCP 도구 7개가 인식됨
3. `wiki_add`로 페이지 생성 시 `docs/wiki/` 하위에 `.md` 파일 생성됨
4. `wiki_query`로 키워드 검색이 동작함
5. `wiki_lint`로 헬스체크가 동작함
6. OMC 플러그인 비활성화 상태에서도 독립 동작함
7. SessionStart hook 실행 시 wiki 컨텍스트가 대화에 주입됨
8. SessionEnd hook 실행 시 `docs/wiki/`에 세션 로그가 자동 캡처됨

## Design Decisions

- 한글 제목 slug: OMC의 hash 방식(`page-0a1b2c3d.md`) 유지
