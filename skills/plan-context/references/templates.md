# Plan Context Templates

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

## Status Values

| Status | 의미 |
|--------|------|
| Proposed | 새로 생성, 미실행 |
| In Progress | 구현 진행 중 |
| Completed | 완료 |
| Deferred | 보류 |
| Superseded | 후속 계획으로 대체 |

## Notes

- Entries in `plan_history.md` are in reverse chronological order (newest first)
- Keep plan summaries concise — focus on goals and approach
- Status is updated manually as the plan progresses
- Link paths in `plan_history.md` are relative to the `docs\` directory
