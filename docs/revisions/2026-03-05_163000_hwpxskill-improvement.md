# hwpxskill & hwpxskill-math skill-creator compliance improvement

- **Date**: 2026-03-05 16:30:00
- **Author**: Claude Opus 4.6

## Rationale / Plan

Plan: [hwpxskill & hwpxskill-math Improvement](../plans/2026-03-05_163000_hwpxskill-improvement.md)

Both HWPX skills were analyzed against skill-creator guidelines. Five issues were found:
1. math-hwpx SKILL.md was 963 lines (nearly 2x the 500-line recommendation)
2. Both descriptions lacked trigger keywords
3. hwpxskill contained README.md (violates "no auxiliary documentation" guideline)
4. math-hwpx included test_refactor.py (unnecessary for distribution)
5. hwpx_utils.py duplicated functions from hwpxskill without documentation

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills/hwpxskill-math/SKILL.md` | Modified | Split out equation syntax and graph shapes to references, update description to English |
| `skills/hwpxskill-math/references/equation-syntax.md` | Added | Hancom equation script syntax reference with grade-level examples |
| `skills/hwpxskill-math/references/graph-shapes.md` | Added | Graph/geometry shape type JSON spec reference |
| `skills/hwpxskill-math/scripts/hwpx_utils.py` | Modified | Add intentional duplication documentation comment |
| `skills/hwpxskill-math/scripts/test_refactor.py` | Deleted | Removed test file from distributed skill |
| `skills/hwpxskill/SKILL.md` | Modified | Update description to English with trigger keywords |
| `skills/hwpxskill/README.md` | Deleted | Moved to project docs/ directory |
| `docs/hwpxskill-readme.md` | Added | Relocated README from skill directory |
| `docs/plans/2026-03-05_163000_hwpxskill-improvement.md` | Added | Plan document |
| `docs/plan_history.md` | Modified | Added plan entry |

## Details

### `skills/hwpxskill-math/SKILL.md` (Modified)

- Replaced 130-line equation syntax section with 3-line summary linking to `references/equation-syntax.md`
- Replaced 160-line graph shapes section with 3-line summary linking to `references/graph-shapes.md`
- Removed 120-line grade-level examples section (moved to equation-syntax.md)
- Updated frontmatter description from Korean to English with comprehensive trigger keywords
- **Result**: 963 lines -> 558 lines (405 lines reduced)

### `skills/hwpxskill-math/references/equation-syntax.md` (Added)

- Full Hancom equation script syntax reference (fractions, roots, integrals, matrices, Greek letters, etc.)
- Grade-level examples: middle school (Grade 7-9) through high school (Grade 10-12)
- Table of contents for navigation

### `skills/hwpxskill-math/references/graph-shapes.md` (Added)

- JSON spec for 5 geometry shape types: triangle, circle, quadrilateral, coordinate, solid3d
- Field tables with required/optional indicators
- Example JSON for each type

### `skills/hwpxskill-math/scripts/hwpx_utils.py` (Modified)

- Added docstring note explaining intentional duplication from hwpxskill/build_hwpx.py
- Documents that cross-repo imports would create fragile dependencies

### `skills/hwpxskill-math/scripts/test_refactor.py` (Deleted)

- Test file removed from distributed skill package

### `skills/hwpxskill/SKILL.md` (Modified)

- Updated frontmatter description from Korean to English
- Added trigger keywords: HWPX, Hancom, OWPML, document creation/editing, template types

### `skills/hwpxskill/README.md` (Deleted) -> `docs/hwpxskill-readme.md` (Added)

- Relocated from skill directory to project docs/ to comply with skill-creator "no auxiliary docs" guideline
- Content unchanged
