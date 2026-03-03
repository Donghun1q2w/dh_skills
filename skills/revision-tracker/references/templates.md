# Revision Tracker Templates

## Revision Entry Template

File: `docs\revisions\YYYY-MM-DD_HHMMSS_<slug>.md`

```markdown
# <One-line summary>

- **Date**: YYYY-MM-DD HH:MM:SS
- **Author**: <agent or user>

## Rationale / Plan

<Why the change was made. If a plan was used, summarize the plan's goals and approach.
Include context such as: user request, bug report, feature requirement, refactoring goal.>

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `src/auth/login.py` | Modified | Add token refresh logic |
| `src/auth/tokens.py` | Added | New token utility module |
| `tests/test_login.py` | Modified | Add refresh token test cases |
| `config/settings.json` | Modified | Add token expiry config |

## Details

### `src/auth/login.py` (Modified)

- Added `refresh_token()` method to `AuthService` class
- Modified `login()` to return refresh token alongside access token
- Added import for new `tokens` module

### `src/auth/tokens.py` (Added)

- New module for token generation and validation
- `generate_refresh_token()` — creates signed refresh token
- `validate_token()` — verifies token signature and expiry

### `tests/test_login.py` (Modified)

- Added `test_refresh_token_success` and `test_refresh_token_expired`
- Updated `test_login_success` to assert refresh token presence
```

## Revision History Template

File: `docs\revision_history.md`

```markdown
# Revision History

Chronological log of project modifications.

---

## 2026-03-03 16:00:45 — Refactor auth module

[Detail](revisions/2026-03-03_160045_refactor-auth-module.md)

- `src/auth/login.py` — Add token refresh logic
- `src/auth/tokens.py` — New token utility module
- `tests/test_login.py` — Add refresh token test cases
- `config/settings.json` — Add token expiry config

---

## 2026-03-02 09:15:00 — Fix DB connection timeout

[Detail](revisions/2026-03-02_091500_fix-db-connection.md)

- `src/db/connection.py` — Increase timeout, add retry logic
- `config/db.json` — Add timeout configuration

---
```

## Notes

- Entries in `revision_history.md` are in reverse chronological order (newest first)
- Keep revision entry summaries concise — focus on what and why, not implementation minutiae
- The `Details` section in revision entries should summarize diffs, not paste raw diffs
- Link paths in `revision_history.md` are relative to the `docs\` directory
