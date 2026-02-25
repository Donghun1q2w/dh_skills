---
name: commit-guide
description: Git commit message writing guide. Use when creating git commits, writing commit messages, or when the user asks to commit changes. Enforces conventional commit format with clear subject and description.
argument-hint: "[optional: commit context or ticket number]"
---

# Git Commit Message Guide

Write commit messages following the rules below. Apply this guide whenever creating a git commit.

## Format

```
<type>(<scope>): <subject>

<description>
```

## Subject Line Rules

| Rule | Detail |
|------|--------|
| Type | **Required.** One of the types listed below |
| Scope | Optional. Module, component, or file area affected (e.g., `auth`, `api`, `ui`) |
| Subject | Imperative mood, no period at end |
| Length | Max 50 characters (hard limit: 72) |
| Language | **Korean preferred.** Type과 scope는 영문 유지, subject 본문은 한국어로 작성 |

### Allowed Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `refactor` | Code restructuring without behavior change |
| `docs` | Documentation only |
| `style` | Formatting, whitespace, semicolons (no logic change) |
| `test` | Adding or updating tests |
| `chore` | Build, CI, tooling, dependencies |
| `perf` | Performance improvement |
| `ci` | CI/CD configuration changes |
| `revert` | Reverting a previous commit |

### Subject Examples

```
feat(auth): OAuth2 로그인 플로우 추가
fix(api): 결제 게이트웨이 null 응답 처리
refactor(cart): 가격 계산 로직 분리
docs(readme): 배포 가이드 추가
test(user): 이메일 검증 엣지 케이스 테스트 추가
chore(deps): React v19로 업그레이드
perf(query): 사용자 조회 인덱스 추가
```

## Description (Body) Rules

| Rule | Detail |
|------|--------|
| When required | Changes that need context: why, trade-offs, side effects |
| When optional | Trivial changes where the subject says it all |
| Blank line | Always separate subject and body with a blank line |
| Line width | Wrap at 72 characters |
| Content | Explain **why**, not what (the diff shows what) |

### What to Include in Description

1. **Motivation**: Why is this change needed?
2. **Approach**: Why this solution over alternatives? (if non-obvious)
3. **Side effects**: What else does this change affect?
4. **Breaking changes**: Start with `BREAKING CHANGE:` if applicable

### Description Examples

```
fix(api): 결제 게이트웨이 null 응답 처리

판매자 계정이 정지된 경우 결제 게이트웨이가 에러 객체 대신 null을
반환하여 체크아웃 과정에서 TypeError가 발생했음.

null 체크와 적절한 에러 메시지 및 로깅 추가.
```

```
refactor(cart): 가격 계산 로직 분리

CartService와 OrderService에서 가격 계산이 중복되어 있었고,
미묘한 차이로 인해 합계가 일치하지 않는 문제가 있었음.

PriceCalculator로 통합하고 할인/세금 전략을 명시적 파라미터로 변경.

BREAKING CHANGE: CartService.getTotal()에 TaxStrategy 인자 필수
```

## Additional Context

If `$ARGUMENTS` is provided, incorporate it as context:
- Ticket numbers: reference in the description (e.g., `Closes #123`)
- File context: tailor the scope and type accordingly

## Commit Checklist

Before committing, verify:
- [ ] Subject uses correct type
- [ ] Subject는 한국어로 작성 (type/scope는 영문)
- [ ] Subject is under 50 characters
- [ ] Description explains WHY (if body is included)
- [ ] No unrelated changes are staged
- [ ] Sensitive files (.env, credentials) are NOT staged
