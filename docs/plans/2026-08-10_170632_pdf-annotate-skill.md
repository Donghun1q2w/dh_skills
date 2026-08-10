# pdf-annotate 스킬 신규 추가 (pdf2img 패턴)

- **Date**: 2026-08-10 17:06:32
- **Status**: Completed

## 1-e Adversarial Review — Revision Log

이 계획은 dh-dev 1-d(Fable 5, max reasoning)에서 초안 작성 후, 1-e 적대적 검증(contrarian + gap_hunter 병렬 레인, Sonnet/standard) 및 오케스트레이터 자체 구조 체크를 거쳐 **1회 재작성**되었습니다. 초안에서 HIGH 7건(중복 제거 후), MEDIUM 7건, LOW 5건이 발견되었고, 아래와 같이 전부 해소되었습니다.

**HIGH (7건, 전부 실질 해소)**
- D17("SKILL.md < 500줄")에 적대적 테스트 태그가 없던 구조 게이트 실패 → `[ADV-n]`/`[V-n]` 이원 태깅 도입, D14·D17을 `[V4]`로 태깅.
- `PRESET_COLORS`가 ReportReviewer의 판정(verdict) 라벨(주의/N/A/FAIL)을 그대로 키로 사용해 "ReportReviewer 고유 개념 재도입 금지" 조항과 모순 → 도메인 중립 키 `warning`/`neutral`/`critical`로 교체(hex 값은 유지, 원 사용 사례는 SKILL.md 산문으로만 설명).
- ADV-14(출력=입력 가드)에 매칭되는 DoD 항목 부재 → D18 신설 및 Step 4 산문에 가드 명시(원본 pseudocode에는 이미 존재하던 로직).
- Acceptance Criteria A5(1e-6)와 DoD D4(1e-9)의 회전 라운드트립 오차 허용치 불일치 → 1e-9(fractional)/0.01pt(/Rect)로 통일.
- D1·D2·D14 태그가 가리키는 ADV-0/V4 콘텐츠가 실제로 그 DoD를 검증하지 않던 불일치 → ADV-0을 "golden + 정적 스모크"로 확장(파일 존재·API 임포트·PRESET 값·경고 부재·데모 파일 존재까지 포함), D14 태그를 `[V4]`로 정정.

**MEDIUM (7건, 전부 해소)**
- "pdf2jpg 미러링" 표현이 실제 8파일 구조(pdf2jpg는 5파일)와 불일치 → "구조 원칙 준용, 파일 수는 도메인 복잡도에 따라 확장"으로 정정.
- DoD D13의 절대 시간 기준(200건/30초)이 1-b 비요청 사항이며 환경별 flaky 위험 → 상대 기준 `t(200) ≤ max(25×t(20), 10초)`로 대체.
- dedup(rect,color,label) 완전중복 제거가 API 우회 옵션 없는 암묵적 설계 결정 → `annotate_pdf(..., dedupe: bool = True)` opt-out 파라미터로 노출.
- pypdf 버전 드리프트를 리스크로만 인정하고 런타임 가드 부재 → `__init__.py`에 메이저 버전 불일치 시 `RuntimeWarning` 가드 추가.
- D7/D8이 API 직접호출 경로와 CLI 경유 경로를 뭉쳐 놓아 ADV 매핑이 불명확, 파일단위 JSON 파싱 실패 시나리오 부재 → D7a/D7b, D8a/D8b로 분리, ADV-15(파일단위 파싱 실패)/D19 신설.
- BoxAnnotation 직접 생성 실패 경로(공개 API 오용) 검증 부재 → ADV-16/D8a 신설.
- D6("라벨 칩 겹침 0건")의 보장 범위(배치 용량 내 한정 여부)와 밀집 폴백 시나리오 미검증 → D6 범위를 배치 용량 내로 명확화, ADV-17(45건 밀집)/D20 신설(무예외·페이지 내 배치만 보장, overlap은 best-effort).

**LOW (5건, 4건 해소 + 1건 오탐 확인)**
- CLI의 레코드단위 skip과 페이지단위 oob 집계를 최종 출력에서 어떻게 합산 보고할지 불명 → 출력 라인에 `skipped_invalid=` 필드 추가로 확정.
- 폰트 기본 경로가 절대경로인지 불명확하다는 지적 → **오탐 확인**: 원본 Step 1에 이미 `r"C:\Windows\Fonts\malgun.ttf"` 절대경로가 명시되어 있어 변경 없음.
- 데모 2·3페이지의 실제 `/Rotate` 값(90/180)을 assert하는 항목 부재 → ADV-1에 추가.
- `PDF_ANNOTATE_FONT` 환경변수 오버라이드 경로 미검증 → ADV-18/D21 신설.
- `PRESET_COLORS` 정확한 키·hex 값을 직접 assert하는 항목 부재 → ADV-0에 추가.

재작성 후 구조 체크(오케스트레이터 재실행) 결과: 8개 필수 섹션 전부 존재, DoD 전 항목(D1~D21) 이진 판정 가능, 전 항목이 내용상 실제로 일치하는 `[ADV-n]`/`[V-n]` 태그를 보유 — **HIGH 없음, 통과**. dh-dev 규칙에 따라 검증 레인은 재소집하지 않았습니다.

---

## 1. Requirements Summary

`dh_skills` 저장소에 새 스킬 `pdf-annotate`를 추가한다.

- **배치 패턴**: pdf2img 패턴. `skills/pdf-annotate/SKILL.md`(얇은 가이드, `references/` 없음) + `refcode/pdf_annotate/`(임포트 가능한 Python 참조 패키지).
- **기능**: 임의의 PDF에 pypdf 네이티브 주석 3종 묶음 — 경계선만 있는 색상 `/Square` + Acrobat 네이티브 `/Popup` 컴패니언 + 한글 라벨 `/FreeText`(PIL로 맑은 고딕을 래스터화한 자체 appearance stream, NoRotate 플래그) — 를 부착.
- **일반화**: ReportReviewer의 케이스 관리 종속성(`align_inputs`/`compliance_report`/`upright_pdf`/`crop`, `<case>_annotations.json` 스키마, `annotate_case` 드라이버)과 판정(verdict) 정규화 로직을 전부 제거. 주석별 **임의 hex 색상**을 받는 범용 API로 설계하되, 원 사용 사례의 색상 3종은 도메인 중립 키 프리셋 `PRESET_COLORS = {"warning": "FFEB9C", "neutral": "D9D9D9", "critical": "FFC7CE"}`로 보존(주의/N/A/FAIL 대응 관계는 SKILL.md 산문으로만 설명).
- **회전 처리 단순화**: 원본 `t = (R + A) % 360`에서 정렬 보정 회전 A(ReportReviewer 전용)를 매개변수째 제거, 페이지 자체 `/Rotate`(R)만 처리. 입력 bbox는 **display space**(뷰어에 보이는 방향, top-left origin, fractional 0..1) 기준.
- **API 명시 옵션**: 동일 (rect,color,label) 중복 제거는 `annotate_pdf(..., dedupe: bool = True)`로 opt-out 가능하게 노출.
- **안전 가드**: 입력=출력 경로 금지(ValueError), 암호화 PDF 거부(ValueError), 한글 폰트 로드 실패 시 즉시 OSError(silent fallback 금지), pypdf 메이저 버전 불일치 시 import 경고(RuntimeWarning, 비치명).
- **실행 가능성**: CLI(`python -m pdf_annotate input.pdf annotations.json`)와 합성 PDF 데모(`--demo`) 제공.
- **부수 변경**: README.md 스킬 목록 표 + 디렉토리 구조 트리 갱신. 그 외 파일(manifest, hooks, 기존 스킬) 일절 미수정.
- **범위 밖**: `docs/plans/*`, `docs/plan_history.md`, revision 로그(오케스트레이터 처리). 테스트 파일은 저장소에 커밋하지 않음 — 검증 스크립트는 scratchpad에서만 실행(저장소에 테스트 인프라 부재, pdf2jpg도 동일).

## 2. Acceptance Criteria

**Baseline (착수 전 확인)**
- B1. `skills/pdf-annotate/`, `refcode/pdf_annotate/` 미존재.
- B2. README.md 스킬 표 21행(commit~dxf-to-pdf), 트리의 `refcode/` 항목은 `pdf2jpg`/`e3dstandalone` 2개.
- B3. `python -c "import pypdf, PIL"` 성공 (pypdf 6.6.2, Pillow 10.4.0 — 확인 완료).
- B4. 작업 트리에 무관한 기존 변경(`.mcp.json`, `hooks/hooks.json` 등) 존재 — 절대 미접촉.

**변경 후 조건**
- A1. `skills/pdf-annotate/SKILL.md` 존재, frontmatter `name: pdf-annotate` + 영문 description(트리거 문구 포함), `quick_validate.py` exit 0.
- A2. `refcode/pdf_annotate/` 8개 파일 구성, cwd=`refcode`에서 `from pdf_annotate import annotate_pdf, BoxAnnotation, AnnotateResult, PRESET_COLORS, load_annotations` 성공, pypdf 6.6.2 환경에서 import 경고 0건.
- A3. `python -m pdf_annotate --demo` exit 0, `demo_input.pdf`(3페이지, 2페이지 `/Rotate 90`, 3페이지 `/Rotate 180`)와 `demo_annotated.pdf` 두 파일이 디스크에 실재.
- A4. `demo_annotated.pdf` 재오픈 시: 항목 1건당 정확히 `/Square`+`/Popup`+`/FreeText` 3객체, `/C` 색상이 지정 hex와 일치(1/255 오차), `/Contents` 한글이 입력과 바이트 동일(U+FFFD·mojibake 0건), FreeText `/F`에 NoRotate 비트(16) on, `/AP /N` Form XObject 존재.
- A5. `/Rotate` 페이지 주석: fractional 라운드트립(순변환은 테스트 측 독립 구현) 오차 **1e-9** 이내, `/Rect`는 독립 계산 기대값과 **0.01pt** 이내 일치.
- A6. 50자 초과 라벨은 49자+`…`로 truncate(`/Contents` 길이 == 50).
- A7. 8건 겹침 케이스에서 라벨 칩 pairwise overlap 0건(폴백 소진 밀도에서는 best-effort — 무예외·페이지 내 배치 보장).
- A8. 잘못된 입력(폰트 부재, bad hex, malformed bbox, 범위 밖 페이지, 암호화 PDF, 파싱 불가 JSON 파일, BoxAnnotation 직접 오생성)이 각각 섹션 6 명세대로 처리 — crash/traceback 유출 없음.
- A9. README 표 22행 + 트리 2곳 추가, 한글 read-back 무결.
- A10. `validate_plugin.py .` exit 0.
- A11. 변경 파일이 정확히 `skills/pdf-annotate/**`(신규), `refcode/pdf_annotate/**`(신규), `README.md`(수정) 뿐.

## 3. Implementation Steps

### Step 0. 사전 확인
```powershell
$env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'
python -c "import pypdf, PIL; print(pypdf.__version__, PIL.__version__)"
Test-Path C:\Windows\Fonts\malgun.ttf   # True 여야 함
```

### Step 1. `refcode/pdf_annotate/config.py`
원본 상수를 그대로 옮기되 이름만 범용화. **캘리브레이션 수치 변경 금지**(원본 실측 검증값). 기본 폰트는 **절대경로**로 고정하고 `PDF_ANNOTATE_FONT` 환경변수로 오버라이드.

```python
"""Constants and presets for the pdf_annotate package."""
import os

from pypdf.constants import AnnotationFlag

DEFAULT_FONT = os.environ.get("PDF_ANNOTATE_FONT", r"C:\Windows\Fonts\malgun.ttf")
LABEL_MAX = 50

BORDER_W_PT = 2
LABEL_FONT_PT = 10.0
LABEL_GAP_PT = 4.0
LABEL_BOX_PAD = 2.0
AP_OVERSAMPLE = 4.0
CHIP_BORDER_W = 0.75
CHIP_BORDER_GRAY = 0.313725
ANNOT_AUTHOR = "pdf-annotate"
POPUP_W_PT, POPUP_H_PT = 180.0, 120.0
FREETEXT_FLAGS = AnnotationFlag.PRINT | AnnotationFlag.NO_ROTATE
VALID_ROTATIONS = frozenset({0, 90, 180, 270})

# Domain-neutral color presets. Hex values originate from a report-review
# use case (warning/neutral/critical highlight); any 6-digit hex is accepted.
PRESET_COLORS = {"warning": "FFEB9C", "neutral": "D9D9D9", "critical": "FFC7CE"}
```
`CERT_REVIEW_FONT` → **`PDF_ANNOTATE_FONT`** 개명. `/T` 작성자 `"pdf-annotate"`. ReportReviewer의 판정 라벨(주의/N/A/FAIL)은 코드 어디에도 키로 쓰지 않는다.

### Step 2. `refcode/pdf_annotate/geometry.py` — 순수 좌표/배치 함수 (pypdf 미의존)
원본 수식 재사용, A 제거, `/Rotate`(r)만 수용. **원본에서 본문이 생략됐던 함수는 아래 코드가 확정 명세 — 그대로 구현할 것.**

```python
"""Pure coordinate transforms and label placement (no pypdf imports)."""
from .config import LABEL_BOX_PAD, LABEL_GAP_PT, LABEL_MAX


def hex_to_rgb(h):
    """'FFFFC7CE'(ARGB)/'FFC7CE'/'#FFC7CE' -> (r, g, b). ValueError on bad input."""
    s = str(h).lstrip("#")
    if len(s) == 8:
        s = s[2:]
    if len(s) != 6:
        raise ValueError(f"bad hex colour: {h!r}")
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


def truncate_label(text, limit=LABEL_MAX):
    collapsed = " ".join(str(text).split())
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[: limit - 1] + "…"


def rects_overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def display_to_page_frac(u, v, r):
    """display-space fractional (top-left origin) -> unrotated page fractional.
    r = page /Rotate (0/90/180/270)."""
    if r == 0:
        return (u, v)
    if r == 90:
        return (v, 1.0 - u)
    if r == 180:
        return (1.0 - u, 1.0 - v)
    if r == 270:
        return (1.0 - v, u)
    raise ValueError(f"unsupported rotation: {r}")


def display_page_size(wp, hp, r):
    """Displayed page size in pt — width/height swap at 90/270."""
    return (hp, wp) if r in (90, 270) else (wp, hp)


def bbox_to_user_rect(bbox, mx0, my0, wp, hp, r):
    """fractional display bbox (l, t, r, b) -> user-space /Rect (pt, bottom-left origin).
    두 코너 모두 변환 후 min/max 정규화 (90/270에서 최소 코너가 바뀜)."""
    l, t, rr, b = bbox
    corners = [display_to_page_frac(l, t, r), display_to_page_frac(rr, b, r)]
    xs = [mx0 + xf * wp for xf, _ in corners]
    ys = [my0 + (1.0 - yf) * hp for _, yf in corners]
    return (min(xs), min(ys), max(xs), max(ys))


def bbox_to_display_box(bbox, ws, hs):
    """fractional bbox -> display-space pt box (top-left origin, y-down). 라벨 배치 전용."""
    l, t, r, b = bbox
    return (l * ws, t * hs, r * ws, b * hs)


def label_rect_for_norotate(chip_topleft_frac, chip_size_pt, mx0, my0, wp, hp, r):
    """NoRotate FreeText의 /Rect. 좌상단 '한 점만' 변환 — min/max 정규화 금지
    (90/270에서 라벨이 반대 방향으로 펼쳐지는 것을 막기 위함)."""
    u, v = chip_topleft_frac
    xf, yf = display_to_page_frac(u, v, r)
    px = mx0 + xf * wp
    py = my0 + (1.0 - yf) * hp
    w, h = chip_size_pt
    return (px, py - h, px + w, py)


def place_label(box_disp, tw, th, page_w, page_h, placed, pad=LABEL_GAP_PT):
    """위/아래/오른쪽 순서로 겹치지 않는 위치 탐색, 실패 시 아래로 스택 (원본 로직 그대로).
    후보·스택(최대 40회) 내 배치 가능 밀도에서는 무겹침 보장, 소진 시 best-effort
    (마지막 시도 위치 반환 — 겹침 가능하나 항상 페이지 내로 클램프됨)."""
    left, top, right, bottom = box_disp
    candidates = [
        (left, top - th - pad),
        (left, bottom + pad),
        (right + pad, top),
    ]
    for cx, cy in candidates:
        x = max(0, min(cx, page_w - tw))
        y = max(0, min(cy, page_h - th))
        rect = (x - LABEL_BOX_PAD, y - LABEL_BOX_PAD, x + tw + LABEL_BOX_PAD, y + th + LABEL_BOX_PAD)
        if not any(rects_overlap(rect, p) for p in placed):
            return x, y
    x = max(0, min(left, page_w - tw))
    y = max(0, min(bottom + pad, page_h - th))
    for _ in range(40):
        rect = (x - LABEL_BOX_PAD, y - LABEL_BOX_PAD, x + tw + LABEL_BOX_PAD, y + th + LABEL_BOX_PAD)
        if not any(rects_overlap(rect, p) for p in placed):
            break
        y = min(y + th + pad, page_h - th)
    return x, y
```

(수식 검산: r=90에서 display 좌상단 (0,0)→page frac (0,1)→user-space 좌하단 — /Rotate 90 시계방향 회전과 정합. 원본 `_aligned_to_user_frac`의 t를 r로 치환한 것과 동일.)

### Step 3. `refcode/pdf_annotate/appearance.py` — PIL 래스터화 + appearance stream
원본을 시그니처만 범용화(verdict → rgb255 직접 전달)해 이식. **content stream 문자열, `/Matrix` 미사용, flate 위치(이미지만 `flate_encode()`, Form은 비압축)를 원본과 동일하게 유지.**

- `load_font(font_path)`: `int(round(LABEL_FONT_PT * AP_OVERSAMPLE))` 크기로 `ImageFont.truetype`; 실패 시 `f"Korean label font not loadable: {font_path!r} ({e}). Set PDF_ANNOTATE_FONT or install a Hangul-capable TTF."`로 `OSError` 재발생 — silent fallback 금지(한글 무결성 원칙).
- `render_label_image(label, font, bg_rgb255)`: 원본 `_render_label_image` 그대로 (textbbox → RGB 이미지 → 검은 글리프).
- `chip_size_pt(img)`: `(img.size[0] / AP_OVERSAMPLE, img.size[1] / AP_OVERSAMPLE)`.
- `rgb01(rgb255)`: `ArrayObject([FloatObject(c / 255.0) for c in rgb255])`.
- `image_xobject(writer, img)`: 원본 `_image_xobject` 문자 그대로 (`writer._add_object(st.flate_encode())`).
- `label_ap(writer, img, rgb255)`: 원본 `_label_ap` 문자 그대로 — content 조립식(`q ... rg ... re f ... RG ... re S Q q ... cm /Im0 Do Q`), latin-1 인코딩, `/BBox`=(0,0,w,h), `/Matrix` 없음. 상수 참조만 `CHIP_BORDER_W`/`CHIP_BORDER_GRAY`/`LABEL_BOX_PAD`로 교체.
- `writer._add_object`는 private API지만 public 대체가 없어 의도적 유지 — Key Rules 문서화 + `__init__.py` 버전 가드(Step 6)로 드리프트 감시.

### Step 4. `refcode/pdf_annotate/annotator.py` — 데이터 모델 + 빌더 + 핵심 진입점

임포트:
```python
from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.annotations import FreeText, Popup, Rectangle
from pypdf.generic import DictionaryObject, NameObject, NumberObject, TextStringObject
```

**데이터 모델** (검증은 `__post_init__` 한 곳에 집중 — 직접 생성/CLI 양쪽이 동일 규칙):
```python
@dataclass(frozen=True)
class BoxAnnotation:
    page: int                                   # 1-based
    bbox: tuple[float, float, float, float]     # display-space fractional (l, t, r, b), top-left origin
    label: str                                  # 한글 가능, 50자 초과 시 자동 truncate
    color: str = "FFC7CE"                       # hex RGB (ARGB/#-prefix 허용)
    subject: str = ""                           # /Subj (빈 문자열이면 미기록)

    def __post_init__(self):
        if not isinstance(self.page, int) or isinstance(self.page, bool) or self.page < 1:
            raise ValueError(f"page must be int >= 1: {self.page!r}")
        bb = tuple(float(v) for v in self.bbox)
        if len(bb) != 4:
            raise ValueError(f"bbox must have 4 values: {self.bbox!r}")
        l, t, r, b = bb
        if not (0.0 <= l < r <= 1.0 and 0.0 <= t < b <= 1.0):
            raise ValueError(f"bbox must satisfy 0<=l<r<=1, 0<=t<b<=1: {bb}")
        object.__setattr__(self, "bbox", bb)
        if not str(self.label).strip():
            raise ValueError("label must be non-empty")
        hex_to_rgb(self.color)  # 잘못된 hex는 여기서 ValueError


@dataclass(frozen=True)
class AnnotateResult:
    out_path: Path
    drawn: int          # Square+Popup+FreeText 묶음 1개 = 1
    page_count: int
    skipped_oob: int
```

**빌더** — 원본 `_pdf_now`/`_build_square`/`_popup_rect`/`_build_popup`/`_build_label_annot`을 시그니처만 변경해 이식:
- `_build_square(rect_pt, rgb255, label, subject, nm, stamp)`: `Rectangle(rect=rect_pt, interior_color=None)`(→ /IC 없음, 경계선만), `/C`=rgb01(rgb255), `/BS`={W: BORDER_W_PT, S: /S}, `/F`=4(Print), `/Contents`=label, `/T`=ANNOT_AUTHOR, `/Subj`는 subject truthy일 때만, `/NM`=nm, `/M`=`/CreationDate`=stamp.
- `_popup_rect(sq_rect, mx0, my0, wp, hp)`: 원본 그대로(오른쪽 배치 + CropBox 클램프, POPUP_W_PT×POPUP_H_PT).
- `_build_popup(square, rect_pt, nm, stamp)`: `Popup(rect=rect_pt, parent=square, open=False)` — kwarg 이름은 `parent`. `/NM`=f"{nm}-popup", `/M`=stamp.
- `_build_label_annot(writer, rect_pt, rgb255, label, subject, img, nm, stamp)`: `FreeText(text=label, rect=rect_pt, font_size=f"{LABEL_FONT_PT:g}pt", background_color="{:02x}{:02x}{:02x}".format(*rgb255))` 생성 직후 `ft[NameObject("/DA")] = TextStringObject(f"/Helv {LABEL_FONT_PT:g} Tf 0 g")` **수동 덮어쓰기**(pypdf 6.6.2 /DA 오염 버그 회피), `/F`=FREETEXT_FLAGS, **`border_color` kwarg 전달 자체 금지**(None도 금지 — /BS W=0 추가됨), `/AP`={/N: label_ap(writer, img, rgb255)}, `/NM`=f"{nm}-label", `/Popup` 없음(라벨 오버레이).

**핵심 진입점** — 두 가지 안전 가드(입력=출력 금지, 암호화 거부)를 함수 서두에 배치하고, dedup은 `dedupe` 파라미터(기본 True)로 opt-out 가능:
```python
def annotate_pdf(pdf_path, annotations, out_pdf, font_path=DEFAULT_FONT, dedupe=True) -> AnnotateResult:
    pdf_path, out_pdf = Path(pdf_path), Path(out_pdf)
    if pdf_path.resolve() == out_pdf.resolve():
        raise ValueError("out_pdf must differ from pdf_path (in-place overwrite is not allowed)")
    reader = PdfReader(str(pdf_path))
    if reader.is_encrypted:
        raise ValueError(f"Encrypted PDF not supported: {pdf_path}")
    n_pages = len(reader.pages)

    by_page: dict[int, list[BoxAnnotation]] = defaultdict(list)
    for ann in annotations:
        by_page[ann.page].append(ann)
    oob = sum(len(v) for p, v in by_page.items() if not 1 <= p <= n_pages)
    has_valid = any(1 <= p <= n_pages for p in by_page)

    font = load_font(font_path) if has_valid else None   # lazy — 주석 0건이면 폰트 불필요
    writer = PdfWriter(clone_from=reader)                # 페이지 바이트 그대로 복제, /Annots만 추가
    stamp = _pdf_now()
    drawn = 0
    for p in sorted(by_page):
        if not 1 <= p <= n_pages:
            continue
        page = reader.pages[p - 1]
        box = page.cropbox
        mx0, my0 = float(box.left), float(box.bottom)
        wp, hp = float(box.width), float(box.height)
        r = int(page.get("/Rotate") or 0) % 360
        if r not in VALID_ROTATIONS:
            r = 0
        ws, hs = display_page_size(wp, hp, r)
        placed, seen, seq = [], set(), 0
        for ann in by_page[p]:
            rgb = hex_to_rgb(ann.color)
            label = truncate_label(ann.label)
            rect = bbox_to_user_rect(ann.bbox, mx0, my0, wp, hp, r)
            key = (tuple(round(v, 2) for v in rect), ann.color, label)
            if dedupe and key in seen:                    # 완전 중복 제거 (opt-out 가능)
                continue
            seen.add(key); seq += 1
            nm = f"pdf-annotate-p{p:02d}-{seq:02d}"
            sq = _build_square(rect, rgb, label, ann.subject, nm, stamp)
            writer.add_annotation(p - 1, sq)               # (1) Square 먼저
            pop = _build_popup(sq, _popup_rect(rect, mx0, my0, wp, hp), nm, stamp)
            writer.add_annotation(p - 1, pop)              # (2) Popup
            sq[NameObject("/Popup")] = pop.indirect_reference  # (3) 역링크
            img = render_label_image(label, font, rgb)
            tw, th = chip_size_pt(img)
            box_disp = bbox_to_display_box(ann.bbox, ws, hs)
            lx, ly = place_label(box_disp, tw, th, ws, hs, placed, pad=LABEL_GAP_PT)
            chip = (lx - LABEL_BOX_PAD, ly - LABEL_BOX_PAD,
                    lx + tw + LABEL_BOX_PAD, ly + th + LABEL_BOX_PAD)
            placed.append(chip)
            label_rect = label_rect_for_norotate(
                (chip[0] / ws, chip[1] / hs),
                (chip[2] - chip[0], chip[3] - chip[1]),
                mx0, my0, wp, hp, r,
            )
            ft = _build_label_annot(writer, label_rect, rgb, label, ann.subject, img, nm, stamp)
            writer.add_annotation(p - 1, ft)
            drawn += 1
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    with open(out_pdf, "wb") as fh:
        writer.write(fh)
    return AnnotateResult(out_pdf, drawn, n_pages, oob)
```
**순서 제약(위반 시 링크 파손)**: Square를 `add_annotation`으로 먼저 추가해 `indirect_reference`를 얻은 뒤 `Popup(parent=sq)` 생성 — 3단계 순서는 코드 순서 자체로 보존.

### Step 5. `refcode/pdf_annotate/demo.py` — 합성 PDF 데모 (외부 파일·추가 의존성 없음)
```python
"""Self-contained demo: synthetic 3-page PDF + preset-colored Korean annotations."""
A4_W, A4_H = 595.0, 842.0

def make_demo_pdf(path) -> Path:
    # PdfWriter().add_blank_page(width=A4_W, height=A4_H) x3;
    # 2페이지 page[NameObject("/Rotate")] = NumberObject(90), 3페이지 180. parent mkdir 후 write.

def demo_annotations() -> list[BoxAnnotation]:
    return [
        BoxAnnotation(1, (0.10, 0.10, 0.45, 0.18), "인장강도 기준 미달", PRESET_COLORS["critical"], "critical"),
        BoxAnnotation(1, (0.10, 0.30, 0.45, 0.38), "치수 재확인 필요", PRESET_COLORS["warning"], "warning"),
        # 겹침 두 건 — 라벨 충돌 회피 시연
        BoxAnnotation(1, (0.55, 0.30, 0.90, 0.38), "해당 없음 — 시험 생략", PRESET_COLORS["neutral"], "neutral"),
        BoxAnnotation(1, (0.55, 0.31, 0.90, 0.39), "중복 영역 두 번째 항목", PRESET_COLORS["warning"], "warning"),
        # 50자 초과 — truncate 시연
        BoxAnnotation(1, (0.10, 0.55, 0.90, 0.62),
                      "이 라벨은 오십 글자를 초과하도록 일부러 아주 길게 작성한 한글 문장으로서 말줄임 처리 동작을 보여준다",
                      PRESET_COLORS["critical"], "critical"),
        BoxAnnotation(2, (0.20, 0.20, 0.60, 0.30), "회전 페이지(90도) 주석", PRESET_COLORS["warning"], "warning"),
        BoxAnnotation(3, (0.20, 0.20, 0.60, 0.30), "회전 페이지(180도) 주석", PRESET_COLORS["critical"], "critical"),
    ]

def run_demo(out_dir, font_path=DEFAULT_FONT) -> AnnotateResult:
    # make_demo_pdf(out_dir/"demo_input.pdf") 후 annotate_pdf(src, demo_annotations(), out_dir/"demo_annotated.pdf")
```

### Step 6. `main.py`, `__main__.py`, `__init__.py`

**CLI JSON 스키마** (UTF-8, 최상위 리스트):
```json
[
  {"page": 1, "bbox": [0.1, 0.2, 0.4, 0.3], "label": "치수 불일치", "color": "FFC7CE", "subject": "critical"},
  {"page": 2, "bbox": [0.5, 0.5, 0.8, 0.6], "label": "확인 필요", "color": "FFEB9C"}
]
```

**`main.py`**:
- `load_annotations(path) -> tuple[list[BoxAnnotation], list[str]]`: `json.loads(Path(path).read_text(encoding="utf-8"))`; **파일 단위 실패**(OSError/JSONDecodeError/최상위가 리스트 아님)는 `ValueError`로 승격 → CLI exit 1, **레코드 단위 실패**(BoxAnnotation의 ValueError/TypeError)는 `record[i]: 사유`로 skips 수집 후 계속.
- `main(argv=None) -> int`: argparse — positional `input_pdf`/`annotations_json`(둘 다 `nargs="?"`), `-o/--output`(기본 `<input>_annotated.pdf`; --demo 시 출력 디렉토리, 기본 `demo_output`), `--font`(기본 DEFAULT_FONT), `--demo` 플래그. --demo 아니면 두 positional 필수(`ap.error`). skips는 stderr에 `skip: ...` 출력.
- **최종 요약 라인(확정 형식)**: 두 집계를 한 줄에 병기 — `out={path} drawn={n} pages={k} skipped_oob={m} skipped_invalid={j}` (j=len(skips), --demo 경로는 j=0). 성공 시 return 0.
- `except (ValueError, OSError, PyPdfError)` → stderr `error: {e}` 한 줄 후 return 1 (traceback 유출 금지). `from pypdf.errors import PyPdfError`.

**`__main__.py`** (pdf2jpg 형식):
```python
"""Allow running as python -m pdf_annotate."""
from .main import main
import sys

if __name__ == "__main__":
    sys.exit(main())
```

**`__init__.py`** — 공개 API + pypdf 버전 드리프트 경량 가드(비치명 경고):
```python
"""Native PDF box-annotation package (pypdf Square + Popup + Korean FreeText labels)."""
import warnings

import pypdf

if not pypdf.__version__.startswith("6."):
    warnings.warn(
        f"pdf_annotate was validated against pypdf 6.6.2 (found {pypdf.__version__}); "
        "re-check FreeText /DA handling and writer._add_object before trusting output.",
        RuntimeWarning,
    )

from .annotator import AnnotateResult, BoxAnnotation, annotate_pdf
from .config import PRESET_COLORS
from .main import load_annotations

__version__ = "1.0.0"
__all__ = ["AnnotateResult", "BoxAnnotation", "annotate_pdf", "PRESET_COLORS", "load_annotations"]
```

### Step 7. `skills/pdf-annotate/SKILL.md` (pdf2img 본문 순서 준수, 목표 200줄 내외, 500줄 미만)

frontmatter:
```yaml
---
name: pdf-annotate
description: "Native PDF annotation guide using pypdf. Adds colored border-only Square boxes with Popup companions and always-visible Korean FreeText labels rendered via custom PIL-rasterized appearance streams, so Hangul displays correctly in any PDF viewer. Use when adding annotations or markup boxes to PDF files, highlighting regions in a PDF with colored rectangles and labels, implementing pypdf annotation code in Python, or when the user mentions 'PDF annotate', 'PDF 주석', 'PDF에 주석 추가', 'PDF 박스 표시', 'annotate PDF'. References the pdf_annotate package at refcode/pdf_annotate."
---
```

본문 섹션 순서: (1) 제목+소개+Invocation hint(선택 인자: PDF 경로/주석 JSON/출력 경로/폰트 경로) → (2) Reference Code Location(8개 파일 트리+한 줄 설명) → (3) Required Dependencies 표: pypdf(tested with 6.6.2 — import 시 메이저 버전 불일치 경고), Pillow(라벨 글리프 래스터화 전용 — 페이지는 래스터화 안 함), 한글 TTF(기본 `C:\Windows\Fonts\malgun.ttf`, `PDF_ANNOTATE_FONT` 오버라이드) + `pip install pypdf Pillow` → (4) Core Implementation Pattern: BoxAnnotation 리스트 + `annotate_pdf()` 최소 예제(한글 라벨 포함) + 좌표계 설명(display-space fractional, top-left origin — OCR/비전 출력과 동일 좌표계) + **`dedupe=True` 기본 동작 설명**(동일 rect·color·label은 1건만 부착, `dedupe=False`로 해제) → (5) **Key Rules 표**(섹션 4의 표 그대로) → (6) Annotation Anatomy: 항목 1건 = Square+Popup+FreeText 3종 묶음, 뷰어에서 개별 선택/이동/삭제 가능, /Rotate 페이지에서 Acrobat 선택 핸들 어긋남 가능하나 콘텐츠 정상(원본 주의사항), **라벨 배치는 밀집 시 best-effort**(후보 3곳+하향 스택 40회) → (7) Preset Colors 표: `warning` FFEB9C / `neutral` D9D9D9 / `critical` FFC7CE — 산문으로 "보고서 검토 워크플로우의 주의/N/A/FAIL 하이라이트에서 유래한 값이며 임의 hex 사용 가능" 명시 → (8) Annotation JSON Format(위 스키마) → (9) Running the Reference Code: `$env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'` 선행, `cd refcode`, `python -m pdf_annotate input.pdf annotations.json -o out.pdf`, `python -m pdf_annotate --demo` → (10) When to Use This Skill → (11) Additional Context($ARGUMENTS 처리, pdf2img 형식).

### Step 8. `README.md` 갱신 (정확한 위치)
(1) 스킬 목록 표 dxf-to-pdf 행(현 29행) 바로 아래:
```markdown
| [pdf-annotate](skills/pdf-annotate/) | PDF에 pypdf 네이티브 주석 추가 (색상 박스 + 한글 라벨, PIL appearance stream) | Python |
```
(2) 트리 `│   ├── pdf2img/` 블록(현 57~58행) 아래:
```
│   ├── pdf-annotate/
│   │   └── SKILL.md
```
(3) 트리 하단 refcode 블록(현 155행~)의 pdf2jpg 행 다음(pdf2jpg 행 끝을 `├──` 유지):
```
    ├── pdf_annotate/             ← PDF 네이티브 주석 패키지 레퍼런스 구현
```

## 4. Code Writing Guide

**컨벤션**
- 패키지 구조는 `refcode/pdf2jpg`의 **구조 원칙을 준용**(패키지 레이아웃: `__init__.py` 버전+공개 API, `__main__.py` 모듈 실행, `config.py` 상수, 핵심 모듈, `main.py` CLI)하되, 파일 수는 도메인 복잡도에 따라 8개로 확장(pdf2jpg는 5개; geometry/appearance 분리와 합성 데모 `demo.py`는 이 도메인 고유 필요). 모듈 첫 줄 한 문장 docstring.
- SKILL.md는 영문 frontmatter+영문 본문, `argument-hint` frontmatter 금지(본문에 기술).
- 문서·주석에 "§" 문자 사용 금지.
- 주석은 원칙적으로 최소화하되, 원본에서 이식하는 **비자명한 워크어라운드 주석**(/DA 버그, NoRotate 단일 코너 변환, border_color 생략 사유, /Matrix 미사용 사유)은 짧게 유지 — 지우면 미래에 "정리"하다 버그를 재도입할 load-bearing 주석.

**Key Rules 표 (SKILL.md 수록용)**

| Rule | Detail |
|------|--------|
| Imports | `from pypdf.annotations import FreeText, Popup, Rectangle` / `from pypdf.constants import AnnotationFlag` / low-level은 `pypdf.generic`. `Rectangle`이 PDF `/Square` 서브타입 생성 (이름 혼동 주의) |
| pypdf version | Tested with pypdf 6.6.2. `FreeText` 생성자의 색상 kwarg가 `/DA`를 오염시키므로 생성 직후 반드시 `/DA` 수동 덮어쓰기. 패키지 import 시 메이저 버전 불일치면 RuntimeWarning |
| FreeText border | `border_color` kwarg 전달 자체 금지 (truthy 기본은 /DA 오염, `None`은 `/BS W=0` 추가) |
| Border-only box | `Rectangle(rect=..., interior_color=None)` → `/IC` 미기록 = 채움 없는 경계선 |
| Popup linkage | Square를 `add_annotation()`으로 **먼저** 추가 후 `Popup(parent=square)` 생성, Popup 추가 후 `square[/Popup] = popup.indirect_reference` — 순서 위반 시 링크 파손 |
| NoRotate label | FreeText `/F` = Print+NoRotate. `/Rect`는 칩 좌상단 **한 점만** 변환 — 두 코너 min/max 정규화 금지 (90/270에서 라벨이 반대로 펼쳐짐) |
| No /Matrix | 라벨 `/AP` Form XObject에 `/Matrix` 금지 — NoRotate + /BBox→/Rect 항등 매핑이 모든 회전에서 정확 |
| Page bytes | `PdfWriter(clone_from=reader)`로 페이지 바이트 그대로 복제, `/Annots`만 추가 — 재인코딩 금지 |
| Private API | XObject 등록은 `writer._add_object()` (public 대체 없음 — pypdf 업그레이드 시 확인 지점) |
| Content stream | appearance content는 ASCII뿐이므로 `latin-1` 인코딩 — 한글은 PIL 래스터와 `TextStringObject`(/Contents)로만 흐름 |
| Korean font | 폰트 실패 시 즉시 `OSError`, silent fallback 금지. 기본 `C:\Windows\Fonts\malgun.ttf`(절대경로), `PDF_ANNOTATE_FONT` 오버라이드 |
| Dedupe | 동일 (rect, color, label)은 기본 1건만 부착 — `annotate_pdf(..., dedupe=False)`로 해제 |
| Encoding | JSON은 `read_text(encoding="utf-8")`, PowerShell 실행 전 `$env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'` |

**금지 사항**: pymupdf/`import fitz` 사용 금지(pypdf 전용 스킬), reportlab 등 신규 의존성 금지(pypdf+Pillow 2개 고정), ReportReviewer 고유 로직 재도입 금지 — 구체적으로 `_canon_verdict` 류 판정 정규화, verdict 문자열을 키로 쓰는 분기, case 디렉토리 개념, aligned rotation `a`, `CERT_REVIEW_FONT` (단, 색상 hex 값 자체는 중립 키 `PRESET_COLORS`로 보존하는 것이 확정 요구사항), requirements.txt 생성 금지(pdf2img처럼 SKILL.md 표로만 선언), 캘리브레이션 상수 값 변경 금지.

## 5. Definition of Done (전부 바이너리 판정, 태그: `[ADV-n]`=섹션 6 / `[V-n]`=섹션 8)

- D1. `refcode/pdf_annotate/` 8개 파일(`__init__.py`,`__main__.py`,`config.py`,`geometry.py`,`appearance.py`,`annotator.py`,`demo.py`,`main.py`)이 존재하고, cwd=refcode에서 공개 API 5종 임포트 성공 + `PRESET_COLORS == {"warning":"FFEB9C","neutral":"D9D9D9","critical":"FFC7CE"}` + pypdf 6.6.2 환경에서 import 경고 0건. [ADV-0]
- D2. `--demo` 실행 exit 0, `demo_input.pdf`·`demo_annotated.pdf` 두 파일 `os.path.exists` True, stdout `drawn=7 pages=3 skipped_oob=0 skipped_invalid=0`. [ADV-0]
- D3. demo_annotated.pdf에서 항목당 3객체(Square/Popup/FreeText), /C 색상 1/255 오차 일치, /Contents 한글 바이트 동일(U+FFFD·`占쏙옙` 0건), FreeText `/F & 16 != 0`, `/AP /N` 존재, Square↔Popup 양방향 링크, **demo_input.pdf 2·3페이지 `/Rotate`가 각각 90·180**. [ADV-1]
- D4. r∈{0,90,180,270} fractional 라운드트립 오차 **<1e-9**, demo 2·3페이지 /Rect가 독립 계산 기대값과 **0.01pt** 이내. [ADV-2]
- D5. 50자 초과 라벨 → 정확히 50자(49+`…`). [ADV-3]
- D6. 8건 겹침 케이스에서 라벨 칩 pairwise overlap 0건 + 라벨 앵커 rect 페이지 내(칩 rect는 LABEL_BOX_PAD=2pt까지 초과 허용). 이 보장은 배치 후보·스택 용량 내 밀도에 한정(밀집 폴백은 D20). [ADV-4]
- D7a. API 직접 호출에서 폰트 부재 → `OSError`, 메시지에 폰트 경로와 `PDF_ANNOTATE_FONT` 문자열 포함. [ADV-5]
- D7b. CLI 경유 폰트 부재 → exit 1, stderr `error:` 1줄, traceback 미출력. [ADV-5]
- D8a. `BoxAnnotation` 직접 생성 시 잘못된 입력 8종 각각 `ValueError`, 정상 입력은 생성 성공. [ADV-16]
- D8b. CLI JSON의 불량 레코드 8건+정상 1건 → exit 0, `skip:` 8줄, `drawn=1`. [ADV-6]
- D9. 범위 밖 페이지 → 예외 없이 `skipped_oob` 집계, 출력 정상. [ADV-7]
- D10. 빈 리스트 + 불량 폰트 경로 → 폰트 미로드(lazy)로 예외 없이 출력 생성(drawn=0), 페이지 수 보존. [ADV-8]
- D11. 암호화 PDF → API `ValueError`("Encrypted" 포함), CLI exit 1. [ADV-9]
- D12. 완전 중복 2건: `dedupe=True`(기본) → drawn=1·/Annots 3개, `dedupe=False` → drawn=2·/Annots 6개. [ADV-10]
- D13. 규모: 1페이지 200건 부착 후 재오픈 시 주석 600개, 소요시간 `t(200) ≤ max(25 × t(20), 10초)` (같은 실행 내 20건 대비 상대 측정 — 환경 독립적 선형성 가드). [ADV-11]
- D14. `quick_validate.py .\skills\pdf-annotate` 및 `validate_plugin.py .` 모두 exit 0. [V4]
- D15. README 3곳 갱신 + README·SKILL.md 한글 read-back 무결(mojibake 시그니처 0건). [ADV-12]
- D16. 이번 작업 변경 파일이 `skills/pdf-annotate/**`, `refcode/pdf_annotate/**`, `README.md`로 한정(착수 전 git 스냅샷 대비). [ADV-13]
- D17. SKILL.md 총 줄 수 < 500. [V4]
- D18. `annotate_pdf(p, anns, p)` (입력=출력 동일 경로) → `ValueError`. [ADV-14]
- D19. 파싱 불가 JSON 파일 3종(구문 오류 JSON / 최상위 dict / 파일 부재) 각각 → CLI exit 1 + stderr `error:` 1줄. [ADV-15]
- D20. 밀집 폴백(같은 bbox 45건): 예외 없이 45건 전부 부착, 모든 라벨 앵커 rect 페이지 내(칩은 2pt 초과 허용), overlap은 best-effort로 허용. [ADV-17]
- D21. `PDF_ANNOTATE_FONT` 오버라이드 유효: 불량 경로 env 주입 + `--font` 미지정 → exit 1·메시지에 해당 경로, 유효 경로(`C:\Windows\Fonts\malgun.ttf`) env 주입 → exit 0. [ADV-18]

## 6. Adversarial Test Environment

scratchpad(`...\scratchpad\pdf_annotate_adv\`)에 작성·실행, **저장소 커밋 금지**. 실행 형식: `PYTHONUTF8=1`/`PYTHONIOENCODING=utf-8` 설정, CLI 케이스는 `subprocess.run([sys.executable, "-m", "pdf_annotate", ...], cwd=refcode, env=...)`로 exit code·stderr 검사. **실행 위치**: ADV-1~4는 `verify_demo.py`(V2), ADV-0·5~11·14~18은 `adv_test.py`(V3), ADV-12는 `adv_test.py` 스캔+V5 육안, ADV-13은 V6에서 수행. 동시성 케이스는 해당 없음(단일 프로세스 파일 변환, 공유 상태 없음), 규모는 ADV-11, 밀집은 ADV-17이 담당.

| ID | 시나리오 | 입력 | 기대 결과 |
|----|----------|------|-----------|
| ADV-0 | golden + 정적 스모크 | 파일 검사 + import + `--demo` | 8개 파일 존재 assert; 공개 API 5종 임포트 성공; `PRESET_COLORS == {"warning":"FFEB9C","neutral":"D9D9D9","critical":"FFC7CE"}` assert; import 시 "pdf_annotate was validated" 경고 미발생(catch_warnings로 포집); 데모 exit 0; `os.path.exists(demo_input.pdf)`·`os.path.exists(demo_annotated.pdf)` 모두 True; stdout `drawn=7 pages=3 skipped_oob=0 skipped_invalid=0` |
| ADV-1 | 구조·한글 무결성·회전값 | demo 산출물 재오픈 | 항목당 3객체, /C 색상 일치(1/255), /Contents==입력 원문(truncate 반영), `\ufffd`·`占쏙옙` 0건, NoRotate 비트 on, /AP /N의 /BBox 존재, Square /Popup ↔ Popup /Parent 양방향 링크, **demo_input.pdf 2·3페이지 `/Rotate`==90·180** |
| ADV-2 | 회전 경계값 | r∈{0,90,180,270} 난수 1000점 라운드트립 + demo 2·3페이지 /Rect | fractional 오차 **<1e-9**, /Rect **<0.01pt**. 순변환(page→display)은 테스트에 **독립 구현**(패키지 함수 재사용 금지 — 자기참조 검증 방지) |
| ADV-3 | 51자+ 한글 라벨 | 60자 한글 | /Contents 길이==50, 끝 문자 `…` |
| ADV-4 | 라벨 겹침(용량 내) | 같은 bbox 8건(라벨 상이) | 8건 부착, FreeText /Rect를 display로 역변환해 pairwise overlap 0건, 앵커 rect 페이지 내(칩 2pt 초과 허용) |
| ADV-5 | 폰트 실패 주입 (2경로) | `font_path="Z:\\nope\\ghost.ttf"` | (a) API: `OSError`, 메시지에 경로+`PDF_ANNOTATE_FONT` 포함 → D7a. (b) CLI `--font` 동일 경로: exit 1, stderr `error:` 1줄, traceback 없음 → D7b |
| ADV-6 | CLI 적대적 레코드 | JSON에 `color:"GGGGGG"`, `color:"12345"`, `bbox l>r`, `bbox 3개`, `bbox 음수`, `page:"1"`, `page:0`, `label:"  "` 8건 + 정상 1건 | exit 0, `skip:` 8줄, `drawn=1 skipped_invalid=8` |
| ADV-7 | 범위 밖 페이지 | page=999, page=4 (3페이지 문서) | 예외 없음, skipped_oob=2, 출력 정상 |
| ADV-8 | 빈 입력+불량 폰트 | `annotations=[]`, 폰트 경로 불량 | 출력 생성(drawn=0), 폰트 lazy 로드로 예외 없음, 페이지 수 보존 |
| ADV-9 | 암호화 PDF | `writer.encrypt("pw")` 산출물 | API `ValueError`("Encrypted" 포함), CLI exit 1 |
| ADV-10 | dedupe 양 모드 | 동일 (page,bbox,label,color) 2건 | `dedupe=True`(기본): drawn=1·/Annots 3개. `dedupe=False`: drawn=2·/Annots 6개 |
| ADV-11 | 규모(상대 성능) | 같은 스크립트 내 20건·200건 각각 부착, `time.perf_counter` 측정 | 200건 재오픈 시 주석 600개; `t(200) ≤ max(25 × t(20), 10.0초)` |
| ADV-12 | 문서 한글 무결성 | README·SKILL.md UTF-8 read-back | `\ufffd`/`占쏙옙`/`ï»¿` 0건, 추가 행 한글 원문 일치 (스캔은 adv_test.py, 육안 확인은 V5) |
| ADV-13 | 변경 격리 | `git status --porcelain` 착수 전/후 비교 (V6에서 수행) | 신규 diff가 지정 3경로뿐 |
| ADV-14 | 출력=입력 가드 | `annotate_pdf(p, anns, p)` | `ValueError` (in-place 금지 메시지) |
| ADV-15 | 파일 단위 JSON 실패 | (a) 구문 오류 JSON, (b) 최상위가 dict인 JSON, (c) 존재하지 않는 경로 | 3건 모두 CLI exit 1, stderr `error:` 1줄, traceback 없음 |
| ADV-16 | BoxAnnotation 직접 오생성 | ADV-6과 동일한 8종 불량값으로 생성자 직접 호출 + 정상 1건 | 불량 8종 각각 `ValueError`(try/except로 검증), 정상 1건 생성 성공 |
| ADV-17 | 밀집 폴백 트리거 | 같은 bbox 45건(스택 40회 용량 초과 유도) | 예외 없음, drawn=45, 모든 라벨 앵커 rect 페이지 내(칩 2pt 초과 허용); overlap 0을 요구하지 않음(best-effort 명세) |
| ADV-18 | 환경변수 오버라이드 | subprocess env에 `PDF_ANNOTATE_FONT` 주입, `--font` 미지정 | (a) 불량 경로 주입: exit 1, 메시지에 그 경로 포함(env가 실제 적용됨을 증명). (b) `C:\Windows\Fonts\malgun.ttf` 주입: exit 0 |

## 7. Risks and Mitigations

| 리스크 | 영향 | 완화 |
|--------|------|------|
| pypdf 버전 드리프트(`_add_object` private, /DA 버그 변동) | AP 등록 실패/이중 워크어라운드 | `__init__.py` import 경고 가드(메이저≠6 시 RuntimeWarning), SKILL.md "tested with 6.6.2" 명시, Key Rules에 확인 지점. 수동 /DA 덮어쓰기는 버그 유무 무관 멱등·무해 |
| `add_blank_page` 페이지에 `/Rotate` 직접 설정 충돌 가능성 | 데모 회전 페이지 실패 | ADV-1이 demo_input.pdf의 /Rotate 90/180을 직접 assert. 실패 시 `page.rotate(90)` 메서드로 대체(동일 효과) |
| 비-Windows/malgun.ttf 부재 | 폰트 로드 실패 | 의도된 fail-fast + 메시지에 PDF_ANNOTATE_FONT 안내, ADV-18이 오버라이드 경로 실검증. 주 사용 환경이 Windows 한글이므로 기본값 유지 |
| 회전 수식 이식 오류(가장 틀리기 쉬움) | 90/270에서 위치 어긋남 | 수식을 계획에 확정 코드로 명시(Step 2), ADV-2가 독립 구현 순변환으로 교차 검증 |
| 밀집 배치에서 place_label 폴백 소진 | 라벨 겹침 발생 | 설계상 best-effort로 명세(D6/D20 범위 분리), SKILL.md Anatomy에 문서화, ADV-17이 무예외·페이지 내 배치를 보장선으로 검증 |
| 한글 콘솔 mojibake | 검증 판독 불가 | 전 실행에 PYTHONUTF8/PYTHONIOENCODING 선행, 파일 read-back 검증을 1차 근거로 |
| 데모가 빈 페이지라 시각 확인 밋밋 | 검증 주관성 | 검증은 전적으로 프로그램적 read-back(ADV-1~4), 시각 확인은 보조(V7) |

## 8. Verification Steps (구현 완료 후 순서대로)

공통 전제:
```powershell
cd D:\001_Work\2026\017_claude\plugins\dh_skills
$env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'
git status --porcelain > $env:TEMP\pdfannotate_git_before.txt   # 착수 전 1회 (ADV-13 기준선)
```

**V1. 임포트·데모 (D1, D2 예비 확인)**
```powershell
cd refcode
python -c "from pdf_annotate import annotate_pdf, BoxAnnotation, AnnotateResult, PRESET_COLORS, load_annotations; print('import OK')"
python -m pdf_annotate --demo -o C:\tmp\claude\D--001-Work-2026-017-claude-plugins-dh-skills\1db9d60b-0cd7-413d-b7ec-8c71d924db0a\scratchpad\demo_out
# 기대 stdout: out=...demo_annotated.pdf drawn=7 pages=3 skipped_oob=0 skipped_invalid=0
```

**V2. 구조·한글·회전 검증 = ADV-1~4 실행 (D3~D6)** — scratchpad에 `verify_demo.py` 작성 후 실행(기대: 전체 PASS, exit 0). 필수 내용: PdfReader로 demo_annotated.pdf 오픈 → NM 접두 `pdf-annotate-` 주석 분류(항목당 3개) → /C vs hex, /Contents vs 기대 문자열(truncate 반영) `==` 비교 + mojibake 시그니처 부재 + **한글 라벨 전체를 stdout 인쇄해 시각 판독**(전역 한글 무결성 정책) → FreeText `/F & 16` 및 /AP /N → Square↔Popup 링크 → demo_input.pdf 2·3페이지 /Rotate==90·180 → 2·3페이지 /Rect 독립 수식 기대값(0.01pt) → fractional 라운드트립 1000점(1e-9) → truncate 길이 50 → 겹침 칩 역변환 후 overlap 0건·앵커 페이지 내.

**V3. 적대적 스위트 = ADV-0·5~12·14~18 실행 (D1, D2, D7a/b, D8a/b, D9~D13, D18~D21)** — scratchpad `adv_test.py`(섹션 6 표 구현) 실행, 해당 항목 전체 PASS + PASS/FAIL 요약 출력.

**V4. 스킬·플러그인 검증 (D14, D17 게이트)**
```powershell
cd D:\001_Work\2026\017_claude\plugins\dh_skills
python C:\Users\donghun.lee\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\skills\pdf-annotate
python C:\Users\donghun.lee\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .
(Get-Content .\skills\pdf-annotate\SKILL.md | Measure-Object -Line).Lines   # < 500 확인
```

**V5. 문서 한글 read-back (D15 육안 게이트, ADV-12 보완)** — README.md·SKILL.md를 UTF-8로 읽어 추가 행 주변 인쇄 + mojibake 스캔(Bash 도구 heredoc, `PYTHONIOENCODING=utf-8` prefix). 한글 온전함을 눈으로 확인한 후에만 완료 보고.

**V6. 변경 격리 (D16 게이트, ADV-13 수행 지점)** — `git status --porcelain` after 스냅샷을 before와 비교, 신규 항목이 `skills/pdf-annotate/`, `refcode/pdf_annotate/`, `README.md` 뿐인지 확인.

**V7. 시각 확인(보조, 게이트 아님)** — 가능하면 demo_annotated.pdf를 뷰어로 열어 3색 박스·한글 라벨 칩·회전 페이지 라벨 수평 유지(NoRotate) 육안 확인. 불가 시 V2 프로그램적 검증을 근거로 보고하되 육안 생략 사실 명시.
