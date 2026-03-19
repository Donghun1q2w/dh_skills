# skill-creator 가이드라인 기반 전체 스킬 재평가 및 개선

- **Date**: 2026-03-19
- **Status**: Completed

## Summary

skill-creator 스킬의 핵심 가이드라인(SKILL.md <500줄, progressive disclosure, references 분리)을 기준으로 프로젝트 내 16개 스킬을 재평가하고, 위반/개선 필요 항목을 수정.

## Background

- 이전 개선 작업(2026-03-05)에서 hwpxskill-math를 963→558줄로 축소했으나 여전히 500줄 초과
- hwpxskill(589줄)도 500줄 기준 초과 상태
- excel(305줄)은 금융 모델 규칙이 본문에 혼재하여 구조 개선 필요
- README.md가 실제 디렉토리 구조와 불일치 (3개 누락, 3개 유령 항목)

## Proposal

### 평가 기준
| 기준 | 규칙 |
|------|------|
| SKILL.md 본문 | < 500 lines |
| Description | 영문, 트리거 키워드 포함 |
| Progressive Disclosure | 무거운 내용은 references/로 분리 |

### 평가 결과

16개 스킬 중 13개 양호, 3개 개선 필요:

1. **hwpxskill** (589줄 → 416줄): section0 가이드, 스타일 ID 맵, Critical Rules를 references로 이동
2. **hwpxskill-math** (558줄 → 317줄): 스타일 ID 맵, 시험지 형식, 단위 변환을 references로 이동
3. **excel** (305줄 → 253줄): 금융 모델 규칙을 references로 이동
4. **README.md**: excel/hwpxskill/hwpxskill-math 추가, hwp-analyze/hwp-fill/hwp-template 제거

## Impact

| 영역 | 영향 |
|------|------|
| 변경 파일 수 | 10개 (SKILL.md 3개 수정, references 6개 신규, README 1개 수정) |
| 정보 손실 | 없음 (이동만 수행) |
| 리스크 | 낮음 — 기존 워크플로우/frontmatter 변경 없음 |
