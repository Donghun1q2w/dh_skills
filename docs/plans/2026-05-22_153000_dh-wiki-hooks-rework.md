# dh-wiki Hook 이벤트 재구성 (SessionStart→UserPromptSubmit, SessionEnd 제거, FileChanged 신설)

- **Date**: 2026-05-22 15:30:00
- **Status**: Proposed

## Summary

dh-wiki 플러그인의 hook 라이프사이클을 재편성한다. (1) 컨텍스트 주입 시점을 `SessionStart`에서 `UserPromptSubmit`으로 옮기고, (2) 세션 종료 자동 캡처(`SessionEnd`)를 제거하며, (3) 신규 `FileChanged` hook으로 프로젝트 내 임의 `.md` 변경을 감지하여 `docs/wiki/`에 미러링 ingest 한다. 제외 경로: `docs/plans/**`, `docs/revisions/**`, `*history.md`.

## Background

- 현행 dh-wiki hooks(`SessionStart`, `PreCompact`, `SessionEnd`)는 컨텍스트 주입과 세션 로그 자동 캡처를 담당하지만, 사용자는 매 프롬프트마다 최신 wiki 상태 인지를 원함 → `UserPromptSubmit`이 더 적합
- `SessionEnd`에서 생성되는 `session-log-*.md`가 wiki 페이지 수를 부풀리고 query 신호-잡음비를 떨어뜨림 → 제거 요구
- 사용자가 작성한 일반 `.md` 문서(SKILL.md, README, references)들은 wiki와 분리되어 있어 `dh_wiki_query`로 검색 불가 → FileChanged 기반 자동 미러링으로 통합
- 제외 대상: 계획·리비전·history 문서는 별도 도구(plan-context, revision-tracker)가 관리하므로 wiki와 중복 방지
- 참고: `docs/claudehooks.md` — `FileChanged`는 디스크 변경 감지 이벤트, `matcher`는 리터럴 파일명만 지원(정규식·글로브 미지원)

## Proposal

### Step 1: `hooks.json` 재구성

`hooks/hooks.json`의 등록 hook을 다음과 같이 재편성한다.

**제거:**
- `SessionStart` 블록 전체
- `SessionEnd` 블록 전체

**유지:**
- `PreCompact` 블록 (그대로)

**신규 추가:**
- `UserPromptSubmit` 블록 — wiki 컨텍스트 주입 담당 (기존 SessionStart 역할 이관)
- `FileChanged` 블록 — `.md` 변경 미러링 담당

**FileChanged matcher 전략:**
- `FileChanged.matcher`가 리터럴 파일명만 지원하므로 글로브(`*.md`) 불가
- 대안 1(채택): matcher를 광범위하게 잡거나 비워두고 스크립트 내부에서 필터링 — 실제 동작은 검증 단계에서 확인
- 대안 2(폴백): matcher 미지원/미발화 시 `PostToolUse(Edit|Write|MultiEdit)` + `Stop` hook 조합으로 전환

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [{
          "type": "command",
          "command": "node \"$CLAUDE_PLUGIN_ROOT\"/skills/dh-wiki/hooks/dh-wiki-user-prompt-submit.mjs",
          "timeout": 5
        }]
      }
    ],
    "PreCompact": [ /* 기존 유지 */ ],
    "FileChanged": [
      {
        "matcher": "",
        "hooks": [{
          "type": "command",
          "command": "node \"$CLAUDE_PLUGIN_ROOT\"/skills/dh-wiki/hooks/dh-wiki-file-changed.mjs",
          "timeout": 10
        }]
      }
    ]
  }
}
```

### Step 2: SessionStart hook → UserPromptSubmit hook 리네임 및 출력 형식 조정

- 파일 리네임: `skills/dh-wiki/hooks/dh-wiki-session-start.mjs` → `dh-wiki-user-prompt-submit.mjs`
- JSON 출력의 `hookEventName`을 `"SessionStart"` → `"UserPromptSubmit"`으로 변경
- `UserPromptSubmit`은 매 프롬프트마다 발화되므로 컨텍스트 페이로드를 짧게 유지 (현행 index.md 30줄 인용 → 상위 5줄 + 페이지 수만)
- 동작 변화 명시: 프롬프트당 1회 주입 (세션당 1회 → 매 프롬프트 1회로 변경됨)

### Step 3: SessionEnd hook 제거

- 파일 삭제: `skills/dh-wiki/hooks/dh-wiki-session-end.mjs`
- 기존 자동 세션 로그(`session-log-YYYY-MM-DD-*.md`) 생성 중단
- 기존 생성된 session-log 페이지는 사용자가 수동으로 정리 (계획 외 — 사용자 판단)

### Step 4: FileChanged hook 스크립트 신규 작성

신규 파일: `skills/dh-wiki/hooks/dh-wiki-file-changed.mjs`

**책임:**
1. stdin JSON 파싱 — 변경된 파일 경로 수집
2. 필터링 (다음 모두 충족 시에만 처리):
   - 확장자 `.md`
   - 경로가 다음 제외 패턴에 매칭되지 않음:
     - `docs/plans/**`
     - `docs/revisions/**`
     - 파일명이 `*history.md` (예: `plan_history.md`, `revision_history.md`)
     - `docs/wiki/**` (자기 자신 루프 방지)
     - **경로 세그먼트 중 어느 것이라도 `.`으로 시작하면 제외** (예: `.git/`, `.omc/`, `.obsidian/`, `.claude/`, `.vscode/`, `.idea/` 등 모든 dot-디렉토리)
     - `node_modules/**` (의존성 디렉토리는 별도 명시 제외)
3. 이벤트 분기:
   - **생성/수정**: 파일 내용 읽기 → 제목 추출(첫 `#` 헤더 또는 파일명) → wiki 페이지 슬러그 결정 → `ingestKnowledge()` 호출하여 미러링
   - **삭제**: 슬러그 재계산 → `deletePage()` 호출
4. 메타데이터 규약:
   - `title`: 첫 `#` 헤더 (없으면 파일명 stem)
   - `tags`: `["mirrored", "<상위 디렉토리명>"]`
   - `category`: `reference` (기본)
   - `sources`: `[<원본 상대 경로>]`
   - `confidence`: `medium`
5. 슬러그 충돌 처리: 원본 경로 해시 접미사 부여 (`<base>-<hash6>.md`)로 동일 제목 다른 파일 구분
6. 무한 루프 방지: ingest 결과로 `docs/wiki/*.md`가 변경되어도 FileChanged가 자기 자신을 트리거하지 않도록 `docs/wiki/` 제외 (Step 2 필터에 이미 포함)
7. 오류 처리: 모든 예외는 stderr에 로그 후 `{continue: true, suppressOutput: true}` 반환 (사용자 워크플로 방해 금지)

**모듈 import:**
- `mcp-server/storage.mjs` 의 `titleToSlug`, `readPage`, `writePage`, `deletePage`, `appendLog`
- `mcp-server/ingest.mjs` 의 `ingestKnowledge`
- 두 모듈은 stdio MCP 서버와 동일 코드를 재사용 (책임 분리 위해 hook 스크립트에서는 별도 entrypoint로 호출)

### Step 5: 입력 스키마 검증 단계

`FileChanged` hook의 정확한 stdin 페이로드 스키마가 공식 문서에 미공개 — 다음 절차로 검증:

1. 매처 없는 FileChanged 등록 후 임의 `.md` 파일을 Edit 도구로 수정
2. 디버그 로그(`claude --debug-file`)에서 stdin JSON 캡처
3. 키 이름 확정: `file_path` / `path` / `paths`(배열) / `tool_input.file_path` 등
4. 캡처 결과 기반 스크립트 키 접근 패턴 확정

검증이 어려울 경우 폴백 (Step 1 대안 2): `PostToolUse(Edit|Write|MultiEdit)` 매처 + Bash 매처에서 `rm` 명령 파싱.

### Step 6: SKILL.md 업데이트

`skills/dh-wiki/SKILL.md` 끝에 새 섹션 추가:

```markdown
## Auto-Mirror (FileChanged)

`docs/wiki/` 외부의 모든 `.md` 파일 변경을 자동으로 wiki 페이지로 미러링한다.

**제외 대상**: `docs/plans/**`, `docs/revisions/**`, `*history.md`, `docs/wiki/**`, `node_modules/**`, 경로 세그먼트가 `.`으로 시작하는 모든 폴더(`.git/`, `.omc/`, `.obsidian/`, `.claude/` 등)

**미러링 규칙**:
- 제목: 첫 `#` 헤더 → 파일명 stem 폴백
- 슬러그: `titleToSlug` + 경로 해시 접미사로 충돌 회피
- 카테고리: `reference`
- 태그: `["mirrored", "<상위 디렉토리명>"]`
- 삭제 시 해당 wiki 페이지도 함께 삭제
```

기존 "Auto-Capture" 섹션은 제거 (SessionEnd 폐기에 따라).

## Impact

| Area | Description |
|------|-------------|
| Files (수정) | `hooks/hooks.json`, `skills/dh-wiki/SKILL.md` |
| Files (리네임) | `dh-wiki-session-start.mjs` → `dh-wiki-user-prompt-submit.mjs` |
| Files (삭제) | `skills/dh-wiki/hooks/dh-wiki-session-end.mjs` |
| Files (신규) | `skills/dh-wiki/hooks/dh-wiki-file-changed.mjs` |
| Dependencies | 변경 없음 (기존 mcp-server 모듈 재사용) |
| Risk | **Medium** — `FileChanged` 입력 스키마 미확정으로 검증 단계 필요. UserPromptSubmit 매 프롬프트 발화로 컨텍스트 누적 우려 → 페이로드 축소로 완화. 자동 미러링이 의도치 않게 wiki 페이지 폭증 가능 → 제외 필터 엄격 적용 |

## Acceptance Criteria

1. 새 세션에서 `SessionStart`/`SessionEnd` hook이 더 이상 발화되지 않음 (`/hooks` 메뉴로 확인)
2. `UserPromptSubmit` hook이 등록되고, 신규 프롬프트 시 stdout 또는 `additionalContext`로 wiki 컨텍스트가 주입됨
3. 임의 위치의 `.md` 파일 생성/수정 시 `docs/wiki/`에 대응 페이지가 생성/갱신됨
4. 제외 대상(`docs/plans/foo.md`, `docs/revisions/bar.md`, `plan_history.md`, `revision_history.md`) 수정 시 wiki에 변화 없음
5. `.md` 파일 삭제 시 해당 wiki 페이지도 삭제됨
6. `docs/wiki/*.md` 자체 변경이 FileChanged hook을 무한 재귀 트리거하지 않음
7. Hook 오류 발생 시 사용자 프롬프트/턴이 차단되지 않음 (`exit 0` + suppressOutput)
8. 기존 PreCompact hook은 영향 없이 정상 동작
9. `docs/wiki/log.md`에 자동 미러링 ingest/delete 이벤트가 기록됨

## Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| `FileChanged` 입력 스키마 미확정 | Step 5 검증으로 사전 확인. 실패 시 `PostToolUse`+`Stop` 조합 폴백 |
| UserPromptSubmit 매 프롬프트 발화로 컨텍스트 노이즈 | 페이로드를 페이지 수+상위 5줄로 축소 |
| 자동 미러링으로 wiki 페이지 폭증 | 제외 필터(plans/revisions/history/wiki/node_modules) 엄격화. 카테고리 `reference` 고정으로 식별 가능 |
| 무한 루프 (wiki 변경 → FileChanged → wiki 변경) | 스크립트 필터에서 `docs/wiki/` 경로 무조건 제외 |
| 슬러그 충돌 (다른 경로, 같은 제목) | 경로 해시 접미사로 구분 |
| Bash `rm`을 통한 외부 삭제 미감지 | FileChanged가 디스크 감시 기반이라면 자동 처리. 만약 누락 시 `PostToolUse(Bash)` 보조 hook 추가 검토 (백로그) |

## Verification Steps

1. `git status`로 변경 파일 목록 확인
2. Claude Code 재시작 후 `/hooks` 메뉴에서 등록 상태 확인
3. 임의 위치에 테스트 `.md` 생성 → `docs/wiki/log.md`에 ingest 기록 확인
4. 동일 파일 수정 → 로그에 update 기록 확인
5. 파일 삭제 → 로그에 delete 기록 확인
6. `docs/plans/test.md` 생성 → wiki 변화 없음 확인
7. `revision_history.md` 수정 → wiki 변화 없음 확인

## Open Questions

- ~~`FileChanged` matcher가 빈 문자열일 때 모든 변경에 발화하는지~~ — **해결**: 발화하지 않음(아래 Resolution 참조)
- 기존 `session-log-*.md` 페이지를 일괄 삭제할지 보존할지 — 사용자 판단 영역 (계획 범위 외)

## Resolution (2026-05-22 16:00)

런타임 검증 결과 `FileChanged` 매처가 빈 문자열이면 감시 목록이 비어 hook이 발화하지 않음을 확인. `claudehooks.md`의 매처 규칙(FileChanged는 matcher가 watch list 자체)에 부합. 계획 Step 1의 폴백(대안 2)으로 전환:

- **신규 트리거**: `PostToolUse` 매처 `Edit|Write|MultiEdit` + `Stop` (매처 없음)
- **PostToolUse**: 도구 호출 시 즉시 동기화 (`tool_input.file_path` 사용)
- **Stop**: 턴 종료 시 `git status --porcelain` 스캔 + orphan sweep (sources 경로가 사라진 mirror 페이지 자동 삭제)
- **write 전략 변경**: `ingestKnowledge`의 append-merge가 미러용으로 부적합(매번 `## Update` 섹션 누적) → `storage.writePage` 직접 호출로 덮어쓰기

검증 완료:
- PostToolUse Write로 신규 .md 생성 → `hook-test-6ad278.md` 미러 페이지 생성됨
- Stop git scan으로 untracked `.md` 함께 미러됨 (`claudehooks-58b0fc.md`, `dh-wiki-workflow-report-536403.md`)
- 원본 삭제 → orphan sweep으로 미러 페이지 자동 삭제됨
