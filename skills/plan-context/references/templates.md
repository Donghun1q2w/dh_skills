# Plan Context Templates

## Context Summary Templates

Two variants. Pick based on `.git` presence at project root.

### Git Variant

```markdown
## Project Context

### Recent Changes (최근 변경)
- <date> — <summary> (from revision_history)

### Change History (변경 이력) — git
- Recent commits: <last 10 commits summary>
- Unstaged changes: <file list or "none">
- Untracked in revision_history: <commits not in revision_history, if any>

### Related Past Plans (관련 과거 계획)
- <date> — <title> (Status: <status>) — <key takeaway>

### Similar Cases (유사 사례)
- <plan title> — <relevance and lessons>

### Wiki Knowledge (위키 지식)
- <page-slug> — <key fact / constraint relevant to this plan>
- (omit section if `docs\wiki\` is absent or no relevant pages found)

### Notes
- <any important context, caveats, or dependencies>
```

### Non-Git Variant

```markdown
## Project Context

### Recent Changes (최근 변경)
- <date> — <summary> (from revision_history, if exists)

### Change History (변경 이력) — file system (no git)
- Recent file modifications (last 7 days): <file list with mtime, top 10>
- Recent revision entries: <last 5 entries from docs/revisions/, if exists>
- Untracked in revision_history: <files modified but not logged, if any>

### Related Past Plans (관련 과거 계획)
- <date> — <title> (Status: <status>) — <key takeaway>

### Similar Cases (유사 사례)
- <plan title> — <relevance and lessons>

### Wiki Knowledge (위키 지식)
- <page-slug> — <key fact / constraint relevant to this plan>
- (omit section if `docs\wiki\` is absent or no relevant pages found)

### Notes
- No git tracking: change history is mtime-based and approximate
- <any important context, caveats, or dependencies>
```

### Bootstrap State (no history files, no git)

Output the Non-Git variant with `Recent Changes` and `Recent revision entries` set to `(none — first documented plan)`. Add a Note: `Bootstrap state: no prior tracking. Consider initializing git and revision-tracker after this plan.`

## Plan Document Template

File: `docs\plans\YYYY-MM-DD_HHMMSS_<slug>.md`

```markdown
# <계획 제목>

- **Date**: YYYY-MM-DD HH:MM:SS
- **Status**: Proposed

## Summary

<2-3문장 요약. 이 계획이 무엇을 달성하려 하는지 간결하게 기술.>

## Background

<배경/동기. 왜 이 계획이 필요한지, 어떤 문제를 해결하려는지.>

## Proposal

<제안 내용 — 단계별로 기술.>

1. Step 1: ...
2. Step 2: ...
3. Step 3: ...

## Impact

| Area | Description |
|------|-------------|
| Files | `src/auth/login.py`, `src/auth/tokens.py` |
| Dependencies | 신규/변경 의존성 |
| Risk | 영향 범위 및 위험 요소 |

## Open Questions

- <미결 사항. 없으면 이 섹션 제거.>
```

## Plan History Template

File: `docs\plan_history.md`

```markdown
# Plan History

Chronological log of project plans and decisions.

---

## YYYY-MM-DD HH:MM:SS — <제목>

[Detail](plans/<파일명>.md) | Status: **Proposed**

Summary: <2-3문장 요약>

---
```

## Interview Mode Templates (인터뷰 모드 템플릿)

Chat-display formats used by Interview Mode (`planning-workflow.md`). Not saved to files.

### Ambiguity Ledger Snapshot (모호성 원장 스냅샷)

```markdown
### Ambiguity Ledger (모호성 원장)
| Track | Status | Latest resolution |
| --- | --- | --- |
| Scope (범위) | Resolved | <one-line pointer> |
| Constraints (제약) | Partially resolved | <one-line pointer> |
| Success Criteria (성공 기준) | Open | — |
| Non-goals (제외 범위) | Open | — |
| Verification (검증 방법) | Waived | user: "decide for me" |
```

Status values: `Open` / `Partially resolved` / `Resolved` / `Waived`.

### Refine Gate Structured Payload (자유서술 구조화 페이로드)

```markdown
Decision: <the decision>
Reasoning: <user's rationale, faithful to their wording>
Constraints (user-stated): <explicit constraints>
Out of scope (user-stated): <explicit exclusions>
Codebase context (orchestrator-verified): <file/config facts verified this session>
```

## Status Values

| Status | 의미 |
|--------|------|
| Proposed | 새로 생성, 미실행 |
| In Progress | 구현 진행 중 |
| Completed | 완료 |
| Deferred | 보류 |
| Superseded | 후속 계획으로 대체 |
| Rejected | 사용자 반려 — 계획 거부, 미실행 종료 |

## Notes

- Entries in `plan_history.md` are in reverse chronological order (newest first)
- Keep plan summaries concise — focus on goals and approach
- Status is updated manually as the plan progresses
- Link paths in `plan_history.md` are relative to the `docs\` directory
