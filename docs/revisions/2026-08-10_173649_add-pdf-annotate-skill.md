# pdf-annotate 스킬 신규 추가 — pypdf 네이티브 PDF 주석(색상 박스 + 한글 라벨) 샘플

- **Date**: 2026-08-10 17:36:49
- **Author**: dh-dev 워크플로우 (pdf-annotate-planner → pdf-annotate-executor 서브에이전트)

## Rationale / Plan

계획: `docs/plans/2026-08-10_170632_pdf-annotate-skill.md` (Status: Completed)

ReportReviewer 저장소의 `cert-review-annotate` 스킬(및 실제 구현 `skills/cert-review/scripts/annotate_pdf.py`)이 쓰는 pypdf 네이티브 PDF 주석 기법 — 판정별 색상의 경계선 `/Square` + Acrobat `/Popup` 컴패니언 + PIL 래스터 기반 커스텀 appearance stream을 가진 한글 `/FreeText` 라벨 3종 묶음 — 을 참조 삼아, ReportReviewer의 케이스 관리 종속성(align_inputs/compliance_report/upright_pdf/crop, `<case>_annotations.json` 스키마) 없이 범용 재사용 가능한 샘플 코드로 일반화해 신규 스킬 `pdf-annotate`를 추가했다. `pdf2img`와 동일한 경량 배치 패턴(짧은 SKILL.md 가이드 + `refcode/pdf_annotate/` 참조 패키지)을 따른다.

dh-dev 워크플로우 전 과정(1-a 분석 → 1-b 컨텍스트 → 1-c 재진술 확인 → 1-d 계획 수립[Fable 5, max reasoning] → 1-e 적대적 검증[contrarian+gap_hunter, HIGH 7/MEDIUM 7/LOW 5 발견 후 1회 재작성으로 전부 해소] → Step 2 사용자 승인 → Step 3 실행[Opus, max reasoning] → 오케스트레이터 독립 재검증)을 거쳤다. Step 3 완료 후 `/simplify`(4개 병렬 리뷰 관점 — Reuse/Simplification/Efficiency/Altitude)를 실행해 안전한 개선 4건을 추가로 적용했다.

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `refcode/pdf_annotate/__init__.py` | Added | 공개 API 재노출, `__version__`, pypdf 메이저 버전 드리프트 경고 가드 |
| `refcode/pdf_annotate/__main__.py` | Added | `python -m pdf_annotate` 진입점 |
| `refcode/pdf_annotate/config.py` | Added | 캘리브레이션 상수, `PRESET_COLORS`, `DEFAULT_FONT` |
| `refcode/pdf_annotate/geometry.py` | Added | 좌표 변환 및 라벨 배치 순수 함수 (pypdf 비의존) |
| `refcode/pdf_annotate/appearance.py` | Added | PIL 라벨 래스터화, 이미지 XObject, 라벨 `/AP` Form 생성 |
| `refcode/pdf_annotate/annotator.py` | Added | `BoxAnnotation`, `AnnotateResult`, `annotate_pdf()` 핵심 진입점 |
| `refcode/pdf_annotate/demo.py` | Added | 합성 3페이지 PDF 데모 (`--demo`) |
| `refcode/pdf_annotate/main.py` | Added | `load_annotations()`, CLI `main()` |
| `skills/pdf-annotate/SKILL.md` | Added | 스킬 가이드 문서 (167줄) |
| `README.md` | Modified | 스킬 목록 표 1행 + 디렉토리 트리 2곳 추가 (4줄) |

## Details

### `refcode/pdf_annotate/` (Added, 8 files)

- pypdf 네이티브 주석 3종(Square 경계선 박스 + Popup 컴패니언 + FreeText 한글 라벨) 부착 API `annotate_pdf(pdf_path, annotations, out_pdf, font_path=DEFAULT_FONT, dedupe=True)` 제공
- 좌표계는 display-space fractional(0..1, top-left origin) bbox — OCR/비전 모델 출력과 호환. 페이지 자체 `/Rotate`(0/90/180/270)를 반영해 user-space `/Rect`로 변환
- 한글 라벨은 PIL로 맑은 고딕(`C:\Windows\Fonts\malgun.ttf`, `PDF_ANNOTATE_FONT` 오버라이드 가능)을 래스터화해 자체 appearance stream(Form XObject)을 생성 — 어떤 PDF 뷰어에서도 한글이 깨지지 않음
- 안전 가드: 입력=출력 경로 금지, 암호화 PDF 거부, 폰트 로드 실패 시 즉시 OSError(silent fallback 없음), pypdf 메이저 버전 불일치 시 import 시 RuntimeWarning
- `PRESET_COLORS = {"warning": "FFEB9C", "neutral": "D9D9D9", "critical": "FFC7CE"}` — 도메인 중립 키(원 사용 사례인 주의/N/A/FAIL 대응은 문서로만 설명, 코드에는 verdict 개념 재도입하지 않음)
- CLI: `python -m pdf_annotate input.pdf annotations.json [-o out.pdf] [--font path]` 및 `python -m pdf_annotate --demo`

### `skills/pdf-annotate/SKILL.md` (Added)

- pdf2img와 동일한 섹션 순서(Reference Code Location → Dependencies → Core Pattern → Key Rules 표 → Annotation Anatomy → Preset Colors → JSON Format → Running → When to Use → Additional Context)
- Key Rules 표에 pypdf 6.6.2 `/DA` 버그 회피, `border_color` kwarg 금지, Popup 연결 순서, NoRotate 라벨 좌상단 단일 코너 변환, `/Matrix` 미사용, `writer._add_object()` private API 사용 등 비자명한 워크어라운드를 명시

### `README.md` (Modified)

- 스킬 목록 표에 `pdf-annotate` 행 추가 (dxf-to-pdf 다음)
- 스킬 디렉토리 트리와 `refcode/` 트리에 각각 신규 항목 추가

### `/simplify` 적용 내역 (4건 적용, 1건 스킵)

- `geometry.py`/`annotator.py` — 라벨 칩 패딩 사각형 계산이 3곳에 중복되어 있던 것을 `pad_rect()` 순수 함수로 추출
- `annotator.py` — `_build_square`/`_build_label_annot`의 공통 주석 메타데이터(`/T`, `/Subj`, `/NM`, `/M`, `/CreationDate`) 설정 블록을 `_set_common_meta()` 헬퍼로 추출
- `annotator.py` — `BoxAnnotation.__post_init__`에서 검증용으로 호출 후 버려지던 `hex_to_rgb(self.color)` 결과를 `_rgb`로 캐시해 `annotate_pdf()` 루프에서 재파싱하지 않도록 함
- `annotator.py`/`appearance.py` — `chip_size_pt(img)`가 호출부와 `label_ap()` 내부에서 두 번 계산되던 것을 호출부에서 한 번만 계산해 `label_ap(writer, img, rgb255, tw, th)`로 전달하도록 변경(라벨 배치 크기와 `/AP /BBox` 크기가 서로 어긋날 여지도 제거)
- (스킵) dedup 키가 `hex_to_rgb` 정규화를 거치지 않은 원본 색상 문자열을 사용하는 점(Altitude 관점 지적) — 이 키 정의는 승인된 계획 문서(Step 4)에 명시적으로 지정된 동작이라, 코드 품질 정리 범위를 벗어나는 동작 변경으로 판단해 스킵
- 적용 후 `verify_demo.py`(116개 체크) + `adv_test.py`(54개 체크) 재실행 — 170/170 전체 통과 확인(회귀 없음)

## Verification

- 오케스트레이터가 executor 보고를 그대로 신뢰하지 않고 독립 재실행: `git status --porcelain`, 8개 파일 실재 확인, `python -c "from pdf_annotate import ..."`, 데모 CLI 재실행, `quick_validate.py`/`validate_plugin.py`(둘 다 exit 0), `verify_demo.py`(116/116)·`adv_test.py`(54/54) 재실행, README/SKILL.md 한글 read-back 육안 확인 — 전부 executor 보고와 일치
- `/simplify` 적용 후 재검증: `quick_validate.py`/`validate_plugin.py` exit 0, `verify_demo.py`/`adv_test.py` 170/170 재통과, `git status --porcelain` 변경 범위가 지정 3경로(`refcode/pdf_annotate/`, `skills/pdf-annotate/`, `README.md`)로 한정됨을 재확인
- 계획의 Definition of Done D1~D21 전 항목 PASS
