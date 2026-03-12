# Revision History

Chronological log of project modifications.

---

## 2026-03-12 16:55:53 — Excel 스킬 추가 및 Windows/macOS 크로스플랫폼 최적화

[Detail](revisions/2026-03-12_165553_add-excel-skill.md)

- `skills/excel/SKILL.md` — Windows/macOS 크로스플랫폼 Excel 스킬 (UTF-8 우선, LibreOffice 제거)

---

## 2026-03-05 18:30:00 — plan-context 스킬에 omc-plan 워크플로우 내부 반영

[Detail](revisions/2026-03-05_183000_plan-context-embed-omc-plan.md)

- `skills/plan-context/SKILL.md` — Phase A-2를 내장 워크플로우로 교체 (4가지 모드 지원)
- `skills/plan-context/references/planning-workflow.md` — 상세 절차 참조 파일 (Added)

---

## 2026-03-05 18:00:00 — plan-context 스킬에 omc-plan 연동 추가

[Detail](revisions/2026-03-05_180000_plan-context-omc-plan.md)

- `skills/plan-context/SKILL.md` — Phase A-2 (omc-plan 연동) 추가, description 업데이트

---

## 2026-03-05 16:30:00 — hwpxskill & hwpxskill-math skill-creator compliance improvement

[Detail](revisions/2026-03-05_163000_hwpxskill-improvement.md)

- `skills/hwpxskill-math/SKILL.md` — Split equation syntax/graph shapes to references, English description (963->558 lines)
- `skills/hwpxskill-math/references/equation-syntax.md` — Hancom equation script syntax reference (Added)
- `skills/hwpxskill-math/references/graph-shapes.md` — Graph shape type JSON spec reference (Added)
- `skills/hwpxskill-math/scripts/hwpx_utils.py` — Add intentional duplication documentation
- `skills/hwpxskill-math/scripts/test_refactor.py` — Removed test file from skill package (Deleted)
- `skills/hwpxskill/SKILL.md` — English description with trigger keywords
- `skills/hwpxskill/README.md` — Moved to `docs/hwpxskill-readme.md` (Deleted)
- `docs/hwpxskill-readme.md` — Relocated README (Added)

---

## 2026-03-03 23:05:00 — plan-context 스킬 추가

[Detail](revisions/2026-03-03_230500_add-plan-context-skill.md)

- `skills/plan-context/SKILL.md` — 스킬 본문 (Phase A: 컨텍스트 탐색, Phase B: 계획 문서 저장)
- `skills/plan-context/references/templates.md` — Plan Document/History 템플릿 및 Status Values
- `README.md` — 스킬 테이블 행 추가 + 디렉토리 트리 업데이트

---

## 2026-03-03 22:36:21 — revision-tracker Section 5 "Git Commit" 기능 확장

[Detail](revisions/2026-03-03_223621_extend-git-commit-flow.md)

- `skills/revision-tracker/SKILL.md` — Section 5를 3단계 인터랙티브 커밋 흐름으로 교체 (제안 → 사용자 확인 → 실행/건너뛰기)
## 2026-03-05 10:30:00 — revision-tracker에 Code Quality Check 스텝 추가

[Detail](revisions/2026-03-05_103000_add-code-quality-step.md)

- `skills/revision-tracker/SKILL.md` — Step 5 "Code Quality Check" 추가, Git Commit을 Step 6으로 재번호

---

## 2026-03-05 10:00:00 — HWP 스킬 3종 개선

[Detail](revisions/2026-03-05_100000_hwp-skills-improvement.md)

- `skills/hwp-analyze/SKILL.md` — description 확장, 간결화, 에러 처리 추가
- `skills/hwp-analyze/references/hwpx-structure.md` — HWPX XML 구조 공통 참조 문서 (신규)
- `skills/hwp-fill/SKILL.md` — description 확장, 간결화, 에러 처리 추가
- `skills/hwp-template/SKILL.md` — description 확장, 스크립트 참조, 에러 처리 추가
- `skills/hwp-template/scripts/manage_template.py` — 템플릿 CRUD 관리 스크립트 (신규)
- `docs/plan_history.md` — 계획 이력 인덱스 (신규)
- `docs/plans/2026-03-05_100000_hwp-skills-improvement.md` — 개선 계획 문서 (신규)

---
