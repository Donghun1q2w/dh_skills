# HWP 스킬 3종 개선 — description 확장, 공통 코드 분리, 에러 처리, 스크립트 추가

- **Date**: 2026-03-05 10:00:00
- **Author**: Claude

## Rationale / Plan

skill-creator 가이드라인 기준 분석 결과, 3개 HWP 스킬(hwp-analyze, hwp-fill, hwp-template)에서 5가지 개선사항이 도출됨. description 트리거 키워드 부족, OS별 처리 코드 중복, 에러 처리 가이드 부재, 템플릿 관리 스크립트 없음 등을 해결.

관련 계획: [HWP 스킬 3종 개선](../plans/2026-03-05_100000_hwp-skills-improvement.md)

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills/hwp-analyze/SKILL.md` | Modified | description 확장, 간결화, 에러 처리 추가, references 참조 |
| `skills/hwp-analyze/references/hwpx-structure.md` | Added | HWPX XML 구조 공통 참조 문서 |
| `skills/hwp-fill/SKILL.md` | Modified | description 확장, 간결화, 에러 처리 추가, 공통 references 참조 |
| `skills/hwp-template/SKILL.md` | Modified | description 확장, 스크립트 참조, 에러 처리 추가 |
| `skills/hwp-template/scripts/manage_template.py` | Added | 템플릿 CRUD 관리 스크립트 |
| `docs/plan_history.md` | Added | 계획 이력 인덱스 신규 생성 |
| `docs/plans/2026-03-05_100000_hwp-skills-improvement.md` | Added | 이번 개선 계획 문서 |

## Details

### `skills/hwp-analyze/SKILL.md` (Modified)

- description에 트리거 키워드 추가: "hwpx 분석", "서식 필드 확인", "한글 파일 열기", "hwp 읽기", "한글 서식 파악", "hwp 필드 목록"
- OS별 처리 코드를 간결화하고 `references/hwpx-structure.md` 참조로 변경
- XML 네임스페이스, 태그 설명 등 상세 내용을 references로 이동
- 에러 처리 테이블 추가 (5개 시나리오)

### `skills/hwp-analyze/references/hwpx-structure.md` (Added)

- HWPX ZIP 구조, XML 네임스페이스, 주요 태그 설명
- 표 구조 예시, 필드 추출 패턴
- XML 특수문자 이스케이프 규칙
- 압축/해제 명령, OS별 지원 매트릭스, pyhwpx 설치 안내

### `skills/hwp-fill/SKILL.md` (Modified)

- description에 트리거 키워드 추가: "hwpx 채우기", "서식 입력", "한글 서식 작성", "hwp 필드 채우기", "서식에 데이터 넣기", "한글 문서 자동 작성"
- hwp-analyze의 `references/hwpx-structure.md`를 상대경로로 참조
- 에러 처리 테이블 추가 (6개 시나리오, 누름틀 fallback 포함)

### `skills/hwp-template/SKILL.md` (Modified)

- description에 트리거 키워드 추가: "서식 관리", "hwp 템플릿", "템플릿 삭제", "등록된 서식", "서식 목록 확인"
- `scripts/manage_template.py` 사용법 섹션 추가
- 에러 처리 테이블 추가 (4개 시나리오)

### `skills/hwp-template/scripts/manage_template.py` (Added)

- argparse 기반 CLI: `save`, `list`, `info`, `delete` 서브커맨드
- `templates/index.json` JSON 메타데이터 관리
- 동일 이름 덮어쓰기 처리, 존재하지 않는 템플릿 에러 처리
- `--templates-dir` 옵션으로 저장 경로 변경 가능
