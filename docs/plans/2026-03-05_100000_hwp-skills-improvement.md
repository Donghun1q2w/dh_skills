# HWP 스킬 3종 개선

- **Date**: 2026-03-05 10:00:00
- **Status**: Completed

## Summary

hwp-analyze, hwp-fill, hwp-template 3개 스킬의 description 트리거 확장, 공통 코드 references 분리, 에러 처리 가이드 추가, 템플릿 관리 스크립트 작성을 수행하여 스킬 품질을 개선한다.

## Background

skill-creator 가이드라인 기준으로 분석한 결과, 5가지 개선사항이 도출됨:
1. description이 짧아 트리거 키워드 부족
2. hwp-analyze/hwp-fill 간 OS별 처리 코드 중복
3. 에러 처리 가이드 부재
4. hwp-template에 관리 스크립트 없음
5. `$ARGUMENTS` 플레이스홀더 확인 필요

## Proposal

1. 3개 스킬 description에 트리거 키워드 확장
2. `hwp-analyze/references/hwpx-structure.md` 공통 참조 파일 생성
3. 각 SKILL.md에 에러 처리 테이블 추가
4. `hwp-template/scripts/manage_template.py` CRUD 스크립트 작성
5. SKILL.md 전반 간결화 (Progressive Disclosure 적용)

## Impact

| Area | Description |
|------|-------------|
| Files | `skills/hwp-analyze/SKILL.md`, `skills/hwp-fill/SKILL.md`, `skills/hwp-template/SKILL.md` |
| New Files | `skills/hwp-analyze/references/hwpx-structure.md`, `skills/hwp-template/scripts/manage_template.py` |
| Dependencies | 없음 (기존 의존성 유지) |
| Risk | 낮음 — 기존 동작 변경 없이 구조 개선만 수행 |
