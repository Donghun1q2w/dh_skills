# skill-creator 가이드라인 기반 전체 스킬 재평가 및 개선

- **Date**: 2026-03-19 16:00:00
- **Author**: Claude (plan-context → ultrawork)

## Rationale / Plan

skill-creator 가이드라인(<500줄, progressive disclosure, references 분리)을 기준으로 16개 스킬을 재평가한 결과, 3개 스킬이 기준 위반 또는 구조 개선이 필요하여 수정. README.md도 실제 디렉토리 구조와 불일치하여 정합성 수정.

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills/hwpxskill/SKILL.md` | Modified | 589→416줄 축소 (3개 섹션을 references로 이동) |
| `skills/hwpxskill/references/section0-guide.md` | Added | section0.xml 작성 가이드 (XML 예시, 표 크기 계산) |
| `skills/hwpxskill/references/style-id-map.md` | Added | 5개 템플릿별 스타일 ID 맵 전체 테이블 |
| `skills/hwpxskill/references/critical-rules.md` | Added | Critical Rules 1~17 상세 설명 |
| `skills/hwpxskill-math/SKILL.md` | Modified | 558→317줄 축소 (4개 섹션을 references로 이동) |
| `skills/hwpxskill-math/references/style-id-map.md` | Added | charPr/paraPr/tabPr/borderFill ID 맵 |
| `skills/hwpxskill-math/references/exam-format.md` | Added | 시험지 레이아웃, 수식 XML, 단위 변환 |
| `skills/excel/SKILL.md` | Modified | 305→253줄 축소 (금융 모델 규칙을 references로 이동) |
| `skills/excel/references/financial-model-rules.md` | Added | 색상 코딩, 숫자 포맷, 수식 규칙, 검증 체크리스트 |
| `README.md` | Modified | 누락 스킬 3개 추가, 삭제된 스킬 3개 제거, 트리 정합성 수정 |

## Details

### `skills/hwpxskill/SKILL.md` (Modified)

- section0.xml 작성 가이드 (문단/빈줄/서식/표 XML 예시) → `references/section0-guide.md`로 이동
- 5개 템플릿별 스타일 ID 맵 상세 테이블 → `references/style-id-map.md`로 이동 (본문에 빠른 참조 테이블만 유지)
- Critical Rules 17개 상세 설명 → `references/critical-rules.md`로 이동 (본문에 요약 목록만 유지)
- 워크플로우 구조, frontmatter 변경 없음

### `skills/hwpxskill-math/SKILL.md` (Modified)

- 스타일 ID 맵 (charPr/paraPr/tabPr/borderFill 4개 테이블) → `references/style-id-map.md`로 이동
- 수식 XML 구조 + 2단 레이아웃 설정 + 페이지 설정 + 단위 변환 + 학력평가/수능 시험지 형식 상세 → `references/exam-format.md`로 이동
- 워크플로우 구조, frontmatter, 기존 references 참조 변경 없음

### `skills/excel/SKILL.md` (Modified)

- Financial models 섹션의 Color Coding Standards, Number Formatting Standards, Formula Construction Rules, Formula Verification Checklist → `references/financial-model-rules.md`로 이동
- 본문에 한 줄 요약 + 참조 링크만 유지
- 핵심 워크플로우 (인코딩 규칙, 읽기/편집/생성, 수식 재계산) 전부 유지

### `README.md` (Modified)

- 스킬 목록 테이블에 excel, hwpxskill, hwpxskill-math 3개 항목 추가
- 디렉토리 트리에서 삭제된 hwp-analyze, hwp-fill, hwp-template 제거
- 디렉토리 트리에 excel, hwpxskill, hwpxskill-math 디렉토리 구조 추가
- docs/ 하위에 hwpxskill-readme.md 항목 추가
