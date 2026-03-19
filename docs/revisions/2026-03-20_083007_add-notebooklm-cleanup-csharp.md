# NotebookLM 스킬 추가 및 csharp-coding-guide.skill 정리

- **Date**: 2026-03-20 08:30:07
- **Author**: Claude (revision-tracker)

## Rationale / Plan

NotebookLM Research Assistant 스킬을 추가하여 Google NotebookLM 노트북을 Claude Code에서 직접 쿼리할 수 있도록 한다. Gemini 기반 소스 근거 답변을 통해 문서 기반 정보 검색의 정확도를 높인다.

기존 `csharp-coding-guide.skill` 바이너리 파일은 이미 `skills/csharp/` 디렉토리 기반 스킬로 대체되었으므로 삭제 정리한다.

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills/notebooklm-skill/` | Added | NotebookLM Research Assistant 스킬 (브라우저 자동화, 노트북 관리, 인증) |
| `csharp-coding-guide.skill` | Deleted | 구 형식 바이너리 .skill 파일 정리 (skills/csharp/로 대체됨) |

## Details

### `skills/notebooklm-skill/` (Added)

- `SKILL.md` — 스킬 본문 (270줄): 인증 관리, 노트북 라이브러리, 질의 워크플로우, 후속 질문 메커니즘
- `scripts/` — 자동화 스크립트 (run.py, ask_question.py, notebook_manager.py, auth_manager.py, cleanup_manager.py)
- `references/` — API 참조, 트러블슈팅, 사용 패턴 문서
- `requirements.txt` — Python 의존성
- 자체 `.git` 저장소로 독립 관리 (별도 origin)

### `csharp-coding-guide.skill` (Deleted)

- 2,292바이트 바이너리 파일 제거
- 이미 `skills/csharp/SKILL.md` 디렉토리 기반 스킬로 이전 완료된 레거시 파일
