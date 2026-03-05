# hwpxskill & hwpxskill-math Improvement

- **Date**: 2026-03-05 16:30:00
- **Status**: Completed

## Summary

Improve two HWPX skills (hwpxskill, hwpxskill-math) to comply with skill-creator guidelines: split oversized SKILL.md, enhance descriptions in English, relocate README.md, remove test files, and resolve code duplication.

## Background

Analysis against skill-creator guidelines revealed 5 issues:
1. hwpxskill-math SKILL.md is 963 lines (nearly 2x the 500-line recommendation) with equation syntax and graph specs that should be in references/
2. Both skills have terse descriptions lacking trigger keywords
3. hwpxskill contains README.md (violates "no auxiliary documentation" guideline)
4. hwpxskill-math includes test_refactor.py (unnecessary for distribution)
5. hwpx_utils.py in math-hwpx duplicates 4 functions from hwpxskill's build_hwpx.py

Follows the same pattern as the previous HWP skills improvement plan (2026-03-05).

## Proposal

### Task 1: Split hwpxskill-math SKILL.md

Move large reference sections to dedicated files:
- Lines covering Hancom equation script syntax (~170 lines) -> `references/equation-syntax.md`
- Lines covering graph/geometry shape specs (~160 lines) -> `references/graph-shapes.md`
- Add navigation links in SKILL.md body pointing to these files
- Target: reduce SKILL.md from 963 to ~600 lines

### Task 2: Enhance descriptions (English)

Rewrite `description` field in both SKILL.md frontmatters in English with comprehensive trigger keywords:
- hwpxskill: include HWPX, Hancom, OWPML, document creation/editing/reading, template, XML
- hwpxskill-math: include math worksheet, exam paper, equation, 학력평가, 수능, graph generation

### Task 3: Relocate README.md

Move `skills/hwpxskill/README.md` to `docs/hwpxskill-readme.md` as project-level documentation. Remove from skill directory.

### Task 4: Remove test_refactor.py

Delete `skills/hwpxskill-math/scripts/test_refactor.py` from the skill package. Test files are not needed in distributed skills.

### Task 5: Resolve code duplication

hwpxskill-math's `hwpx_utils.py` duplicates these functions from hwpxskill's `build_hwpx.py`:
- `validate_xml()`
- `update_metadata()`
- `pack_hwpx()`
- `validate_hwpx()`

Options:
- (A) Make hwpx_utils.py import from hwpxskill if co-installed
- (B) Add a comment noting the intentional duplication for standalone use
- (C) Extract shared code to a common module

Recommended: (B) since these are independent git repos, cross-repo imports create fragile dependencies. Document the duplication with a comment header.

## Impact

| Area | Description |
|------|-------------|
| Modified | `skills/hwpxskill/SKILL.md`, `skills/hwpxskill-math/SKILL.md`, `skills/hwpxskill-math/scripts/hwpx_utils.py` |
| New | `skills/hwpxskill-math/references/equation-syntax.md`, `skills/hwpxskill-math/references/graph-shapes.md`, `docs/hwpxskill-readme.md` |
| Deleted | `skills/hwpxskill/README.md`, `skills/hwpxskill-math/scripts/test_refactor.py` |
| Dependencies | None (no behavioral changes) |

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| SKILL.md split breaks context flow | Low | Medium | Add clear navigation links with "when to read" guidance |
| Description change affects trigger accuracy | Low | Low | Include all existing Korean keywords alongside English |
| Removing test file loses regression coverage | Low | Low | Tests belong in the git repo, not the distributed skill |
