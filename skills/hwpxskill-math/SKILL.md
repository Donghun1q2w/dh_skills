---
name: math-hwpx
description: "Generate math worksheet and exam paper HWPX documents with Hancom equation script (hp:equation). Produces 2-column exam papers in Korean standardized test format (학력평가/수능) or simple worksheets. Supports grade 7-12 math (중1~고3), graph/geometry PNG generation (triangle, circle, coordinate, solid3d), and JSON-to-HWPX pipeline. Use when creating math worksheets, exam papers, equation documents, 수학 문제지, 시험지, 수식 문서, or 학력평가/수능 문제 generation."
---

# math-hwpx — 수학 수식 문제지 HWPX 생성 스킬

수학 수식(`hp:equation`)을 포함한 **2열 문제지**를 HWPX 파일로 생성하는 스킬.
중학교 1학년 ~ 고등학교 3학년 범위의 수학 문제를 한컴오피스 수식 편집기 스크립트 문법으로 작성한다.
hwpx 스킬과 동일한 XML-first 워크플로우를 따르며, 기존 hwpx 스킬의 빌드/검증 도구와 호환된다.

**두 가지 형식 지원:**
- **exam** (기본값, 학력평가/수능): 전국연합학력평가/수능 형식 시험지 (헤더, 가로 선택지, 배점, 페이지 번호 등)
- **worksheet** (`--exam-type worksheet` 명시 필요): 단순 2열 수학 문제지

## 환경

```
# SKILL_DIR는 이 SKILL.md가 위치한 디렉토리의 절대 경로로 설정
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"   # 스크립트 내에서

# hwpx 기본 스킬 경로 (검증/추출 도구 사용 시)
HWPX_SKILL_DIR="<hwpx 스킬 설치 경로>"

# Python 가상환경 (프로젝트에 맞게 설정)
VENV="<프로젝트>/.venv/bin/activate"
```

모든 Python 실행 시:
```bash
# 프로젝트의 .venv를 활성화 (pip install lxml 필요)
source "$VENV"
```

## 디렉토리 구조

```
.claude/skills/math-hwpx/
├── SKILL.md                              # 이 파일
├── scripts/
│   ├── build_math_hwpx.py                # CLI + build 오케스트레이션 (~170줄)
│   ├── xml_primitives.py                 # IDGen, STYLE 상수, 기본 문단/수식 생성기
│   ├── exam_helpers.py                   # 시험지 전용 XML 생성기 (배점, 선택지, 이미지)
│   ├── table_layout.py                   # 투명 테이블 2×2 레이아웃 로직
│   ├── section_generators.py             # worksheet/exam section0.xml 조립
│   ├── hwpx_utils.py                     # 검증/패키징/메타데이터
│   ├── graph_generator.py                # 그래프 PNG 생성 (matplotlib)
│   └── test_refactor.py                  # 리그레션 테스트 스크립트
├── templates/
│   ├── base/                             # 2단 레이아웃 기본 템플릿
│   │   ├── mimetype, META-INF/*, version.xml, settings.xml, Preview/*
│   │   └── Contents/ (header.xml, section0.xml, content.hpf)
│   └── worksheet/                        # (확장용) 오버레이 템플릿
├── examples/
│   ├── sample_middle_school.json          # 중학교 문제 예시
│   ├── sample_high_school.json            # 고등학교 문제 예시
│   ├── sample_exam_2020_march.json        # 학력평가 형식 예시
│   ├── 01_middle_school_worksheet.sh      # 빌드 예제
│   ├── 02_high_school_worksheet.sh        # 빌드 예제
│   └── 03_exam_paper.sh                   # 학력평가 시험지 빌드 예제
└── references/                           # 리그레션 테스트 레퍼런스 XML
```

### 모듈 의존 구조

```
build_math_hwpx.py (CLI + build 오케스트레이션)
  ├── hwpx_utils.py (validate_xml, pack_hwpx, validate_hwpx, update_metadata, _add_images_to_manifest)
  ├── section_generators.py (generate_worksheet_section_xml, generate_exam_section_xml)
  │     ├── table_layout.py (_make_problem_cell_content, make_problem_table)
  │     │     ├── xml_primitives.py (IDGen, STYLE, make_*_para, _make_equation_run)
  │     │     └── exam_helpers.py (make_exam_problem_para, make_picture_para)
  │     └── xml_primitives.py
  └── graph_generator.py (변경 없음)
```

의존 방향: `primitives → helpers → table → section → build` (순환 없음)

---

## 핵심 워크플로우: JSON → HWPX 문제지

### 1. 문제 JSON 작성

**반드시 아래 형식을 따를 것. `exam_type`, `year`, `month`, `grade`, `points`, `choices` 등 학력평가 필드를 포함해야 한다.**

```json
{
  "exam_type": "학력평가",
  "year": 2025,
  "month": 3,
  "grade": "중2",
  "session": 2,
  "subject_area": "수학",
  "total_pages": 4,
  "question_type_label": "5지선다형",
  "problems": [
    {
      "text": "의 값은?",
      "equation": "2x + 3 = 7",
      "points": 4,
      "choices": ["1", "2", "3", "4", "5"]
    },
    {
      "text": "을 간단히 한 것은?",
      "equation": "sqrt 12 + sqrt 27",
      "points": 5,
      "choices": ["$3 sqrt 3$", "$4 sqrt 3$", "$5 sqrt 3$", "$6 sqrt 3$", "$7 sqrt 3$"]
    },
    {
      "text": "다음 중 옳은 것은?",
      "points": 4,
      "choices": ["$sqrt 4 = 2$", "$sqrt 9 = +- 3$", "$(-2)^2 = -4$", "$sqrt {16} = 4$", "$sqrt 25 = -5$"]
    },
    {
      "section_label": "주관식",
      "text": "을 인수분해하시오.",
      "equation": "x^2 - 5x + 6",
      "points": 5
    }
  ]
}
```

### 2. 빌드

```bash
source "$VENV"

# 학력평가 형식 (기본값 — exam_type 지정 불필요)
python3 "$SKILL_DIR/scripts/build_math_hwpx.py" \
    --problems problems.json \
    --creator "수학교사" \
    --output exam.hwpx

# 단순 worksheet 형식 (명시적 지정 필요)
python3 "$SKILL_DIR/scripts/build_math_hwpx.py" \
    --problems problems.json \
    --exam-type worksheet \
    --title "중2 일차방정식" \
    --output worksheet.hwpx
```

### 3. 검증 (hwpx 스킬의 validate.py 사용)

```bash
python3 "$HWPX_SKILL_DIR/scripts/validate.py" worksheet.hwpx
```

---

## 문제 JSON 형식 (학력평가 — 기본값)

**중요: 모든 문제 JSON은 반드시 학력평가 형식으로 작성한다. title/subtitle/info는 사용하지 않는다.**

```json
{
  "exam_type": "학력평가",
  "year": 2025,
  "month": 3,
  "grade": "중3",
  "session": 2,
  "subject_area": "수학",
  "total_pages": 4,
  "question_type_label": "5지선다형",
  "problems": [
    {
      "text": "문제 본문 (수식 앞뒤 텍스트)",
      "equation": "한컴 수식 스크립트",
      "points": 4,
      "choices": ["선택지1", "$수식선택지$", "선택지3", "선택지4", "선택지5"]
    },
    {
      "text": "소문제가 있는 경우",
      "equation": "메인 수식",
      "points": 5,
      "sub_problems": [
        {"equation": "소문제 수식"}
      ],
      "choices": ["1", "2", "3", "4", "5"]
    },
    {
      "section_label": "주관식",
      "text": "을 인수분해하시오.",
      "equation": "x^2 - 5x + 6",
      "points": 5
    }
  ]
}
```

### 필드 설명

| 필드 | 필수 | 설명 |
|------|------|------|
| `exam_type` | **O** | **반드시 `"학력평가"` 지정** |
| `year` | O | 학년도 (예: 2025) |
| `month` | O | 시행 월 (예: 3, 6, 9, 11) |
| `grade` | O | 학년 (예: "중1", "중2", "중3", "고1", "고2", "고3") |
| `session` | X | 교시 (기본: 2) |
| `subject_area` | X | 과목 영역 (기본: "수학") |
| `total_pages` | X | 총 페이지 (기본: 문제 수에 따라 자동) |
| `question_type_label` | X | 문항유형 라벨 (기본: "5지선다형") |
| `problems` | O | 문제 배열 |
| `problems[].text` | X | 문제 텍스트 |
| `problems[].equation` | X | 독립 수식 (display 모드) |
| `problems[].points` | **O** | **배점 (정수, `[N점]` 형태로 표시)** |
| `problems[].choices` | X | 객관식 5지선다 (`$...$`로 감싸면 수식) |
| `problems[].sub_problems` | X | 소문제 배열 [{text, equation}] |
| `problems[].section_label` | X | 섹션 구분 라벨 (예: "주관식") |

---

## 한컴 수식 스크립트 문법 (hp:equation)

Full syntax reference including fractions, roots, integrals, matrices, Greek letters, special symbols, and grade-level examples (middle school through high school): see [references/equation-syntax.md](references/equation-syntax.md).

Key rules: `{ }` for grouping, `a over b` for fractions, `sqrt {x}` for roots, `x^2` / `x_i` for super/subscripts, `$...$` in JSON choices for inline equations. **Use Hancom script syntax, NOT LaTeX.**

---

## 수식 XML 구조

section0.xml에서 수식은 다음과 같이 삽입된다:

```xml
<hp:p id="고유ID" paraPrIDRef="22" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
  <hp:run charPrIDRef="9">
    <hp:equation id="고유ID" type="0" textColor="#000000"
                 baseUnit="1000" letterSpacing="0" lineThickness="100">
      <hp:sz width="0" height="0" widthRelTo="ABS" heightRelTo="ABS"/>
      <hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="0"
              allowOverlap="0" holdAnchorAndSO="0" rgroupWithPrevCtrl="0"
              vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT"
              vertOffset="0" horzOffset="0"/>
      <hp:script>x = {-b +- sqrt {b^2 - 4ac}} over {2a}</hp:script>
    </hp:equation>
  </hp:run>
</hp:p>
```

### 수식 속성

| 속성 | 값 | 설명 |
|------|----|----|
| `baseUnit` | 1000 | 기본 10pt (100 HWPUNIT = 1pt) |
| `textColor` | #000000 | 수식 색상 |
| `lineThickness` | 100 | 분수선/루트선 두께 |
| `treatAsChar` | 1 | 인라인 수식 (텍스트와 같은 줄) |

### 텍스트 + 수식 혼합

한 문단에 텍스트와 수식을 함께 배치:

```xml
<hp:p id="..." paraPrIDRef="21" ...>
  <hp:run charPrIDRef="9"><hp:t>방정식 </hp:t></hp:run>
  <hp:run charPrIDRef="9">
    <hp:equation ...>
      <hp:script>2x + 3 = 7</hp:script>
    </hp:equation>
  </hp:run>
  <hp:run charPrIDRef="9"><hp:t> 의 해를 구하라.</hp:t></hp:run>
</hp:p>
```

---

## 2단 레이아웃 설정

section0.xml 첫 문단의 `hp:colPr`으로 설정:

```xml
<hp:colPr id="" type="NEWSPAPER" layout="LEFT" colCount="2" sameSz="1" sameGap="2268"/>
```

| 속성 | 값 | 설명 |
|------|----|----|
| `type` | NEWSPAPER | 좌→우 순서로 채움 |
| `colCount` | 2 | 2단 |
| `sameSz` | 1 | 동일 너비 |
| `sameGap` | 2268 | 단간격 8mm |

### 페이지 설정 (문제지 최적화)

```xml
<hp:pagePr landscape="WIDELY" width="59528" height="84186" gutterType="LEFT_ONLY">
  <hp:margin header="4252" footer="4252" gutter="0"
             left="5668" right="5668" top="4252" bottom="4252"/>
</hp:pagePr>
```

- 좌우 여백: 20mm (표준 30mm보다 좁음 → 내용 영역 확대)
- 상하 여백: 15mm
- 본문폭: 48192 HWPUNIT (170mm)
- 단 너비: (48192 - 2268) / 2 = 22962 HWPUNIT (약 81mm)

---

## 스타일 ID 맵

### charPr (글자 스타일)

| ID | 설명 | 크기 | 굵기 | 기울임 | 비고 |
|----|------|------|------|--------|------|
| 0 | 기본 본문 | 10pt | 보통 | - | 함초롬바탕 |
| 1 | 돋움 기본 | 10pt | 보통 | - | 함초롬돋움 |
| 2~6 | Skeleton 호환 | 다양 | 보통 | - | |
| **7** | **문제지 제목** | **16pt** | **볼드** | - | worksheet용 |
| **8** | **문제 번호** | **11pt** | **볼드** | - | worksheet용 |
| **9** | **문제 본문** | **10pt** | 보통 | - | 공통 |
| **10** | **단원명/소제목** | **12pt** | **볼드** | - | 공통 |
| **11** | **선택지/보기** | **9pt** | 보통 | - | 공통 |
| **12** | **시험 제목줄** | **10pt** | 보통 | - | exam용 |
| **13** | **과목 영역** | **18pt** | **볼드** | - | exam용 "수학 영역" |
| **14** | **교시 라벨** | **10pt** | 보통 | - | exam용 "제 2 교시" |
| **15** | **시험 문제번호** | **10pt** | **볼드** | **이탤릭** | exam용 |
| **16** | **배점** | **9pt** | 보통 | - | exam용 "[2점]" |
| **17** | **페이지 번호** | **9pt** | 보통 | - | exam용 |

### paraPr (문단 스타일)

| ID | 정렬 | 줄간격 | 용도 |
|----|------|--------|------|
| 0 | JUSTIFY | 160% | 기본 본문 |
| 1~19 | 다양 | 다양 | Skeleton 호환 |
| **20** | **CENTER** | **160%** | **제목** (worksheet) |
| **21** | **LEFT** | **150%** | **문제 본문** (공통) |
| **22** | **LEFT** | **140%** | **수식 표시** (공통) |
| **23** | **LEFT** | **140%** | **선택지/보기 세로** (공통) |
| **24** | **CENTER** | **130%** | **시험 제목줄** (exam) |
| **25** | **LEFT** | **130%** | **교시+과목 라인** (exam) |
| **26** | **CENTER** | **150%** | **과목 영역 대제목** (exam) |
| **27** | **LEFT** | **140%** | **선택지 가로** (exam, tabPr=3) |
| **28** | **LEFT** | **140%** | **문항유형 라벨** (exam, 테두리) |
| **29** | **CENTER** | **130%** | **페이지 하단 번호** (exam) |

### tabPr (탭 설정)

| ID | 설명 |
|----|------|
| 0 | 기본 (탭 없음) |
| 1 | 좌측 자동탭 |
| 2 | 우측 자동탭 |
| **3** | **가로 선택지용 5개 탭스톱** (4590, 9180, 13770, 18360) |

### borderFill (테두리)

| ID | 설명 |
|----|------|
| 1 | 없음 (페이지 보더) |
| 2 | 없음 + 투명배경 |
| 3 | SOLID 4면 (표용) |
| 4 | SOLID + #E8E8E8 배경 (헤더 셀) |
| 5 | 하단 DASH 선 (문제 구분) |
| **6** | **SOLID 테두리 (교시/문항유형 라벨)** |
| **7** | **두꺼운 SOLID 테두리 (페이지번호 박스)** |

---

## 도형 그래프 타입 (Geometry Shapes)

`graph_generator.py` supports function graphs plus 5 geometry shape types: triangle, circle, quadrilateral, coordinate, solid3d. Full JSON spec for each type: see [references/graph-shapes.md](references/graph-shapes.md).

Specify `"graph"` field in problem JSON to auto-generate PNG images.

---

## 직접 section0.xml 작성 (고급)

JSON 대신 직접 section0.xml을 작성하여 더 세밀한 제어 가능:

```bash
SECTION=$(mktemp /tmp/section0_XXXX.xml)
cat > "$SECTION" << 'XMLEOF'
<?xml version='1.0' encoding='UTF-8'?>
<hs:sec xmlns:hp="http://www.hancom.co.kr/hwpml/2011/paragraph"
        xmlns:hs="http://www.hancom.co.kr/hwpml/2011/section"
        xmlns:hc="http://www.hancom.co.kr/hwpml/2011/core">
  <!-- base/section0.xml의 첫 문단(secPr+colPr) 그대로 복사 -->
  <!-- ... -->

  <!-- 제목 -->
  <hp:p id="1000000002" paraPrIDRef="20" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
    <hp:run charPrIDRef="7"><hp:t>수학 문제지</hp:t></hp:run>
  </hp:p>

  <!-- 수식 문단 -->
  <hp:p id="1000000003" paraPrIDRef="22" styleIDRef="0" pageBreak="0" columnBreak="0" merged="0">
    <hp:run charPrIDRef="9">
      <hp:equation id="1000000099" type="0" textColor="#000000"
                   baseUnit="1000" letterSpacing="0" lineThickness="100">
        <hp:sz width="0" height="0" widthRelTo="ABS" heightRelTo="ABS"/>
        <hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="0"
                allowOverlap="0" holdAnchorAndSO="0" rgroupWithPrevCtrl="0"
                vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT"
                vertOffset="0" horzOffset="0"/>
        <hp:script>x = {-b +- sqrt {b^2 - 4ac}} over {2a}</hp:script>
      </hp:equation>
    </hp:run>
  </hp:p>
</hs:sec>
XMLEOF

python3 "$SKILL_DIR/scripts/build_math_hwpx.py" --section "$SECTION" --output result.hwpx
rm -f "$SECTION"
```

---

## hwpx 스킬과의 연동

math-hwpx는 hwpx 스킬의 도구를 재사용할 수 있다:

| 도구 | 경로 | 용도 |
|------|------|------|
| validate.py | `$HWPX_SKILL_DIR/scripts/validate.py` | HWPX 구조 검증 |
| unpack.py | `$HWPX_SKILL_DIR/scripts/office/unpack.py` | HWPX → 디렉토리 |
| pack.py | `$HWPX_SKILL_DIR/scripts/office/pack.py` | 디렉토리 → HWPX |
| text_extract.py | `$HWPX_SKILL_DIR/scripts/text_extract.py` | 텍스트 추출 |

```bash
# 생성된 문제지 구조 확인
python3 "$HWPX_SKILL_DIR/scripts/office/unpack.py" worksheet.hwpx ./unpacked/
# → ./unpacked/Contents/section0.xml 편집 후
python3 "$HWPX_SKILL_DIR/scripts/office/pack.py" ./unpacked/ edited.hwpx
```

---

## 단위 변환 (hwpx 스킬과 동일)

| 값 | HWPUNIT | 의미 |
|----|---------|------|
| 1pt | 100 | 기본 단위 |
| 10pt | 1000 | 기본 글자크기 |
| 1mm | 283.5 | 밀리미터 |
| A4 폭 | 59528 | 210mm |
| A4 높이 | 84186 | 297mm |
| 문제지 좌우여백 | 5668 | 20mm |
| 문제지 본문폭 | 48192 | 170mm |
| 단간격 | 2268 | 8mm |
| 단 너비 | 22962 | 약 81mm |

---

## Critical Rules

1. **항상 학력평가 형식**: JSON에 반드시 `"exam_type": "학력평가"`를 포함. worksheet 형식은 사용 금지
2. **배점 필수**: 모든 문제에 `"points"` 필드 필수. 객관식은 `"choices"` 5개, 주관식은 `"section_label": "주관식"` 포함
3. **수식 스크립트는 `<hp:script>` 안에**: LaTeX가 아닌 한컴 수식 문법 사용
4. **secPr 필수**: section0.xml 첫 문단에 secPr 반드시 포함
5. **mimetype 순서**: ZIP 패키징 시 mimetype은 첫 번째 엔트리, ZIP_STORED
6. **ID 고유성**: 문단 ID, 수식 ID 모두 문서 내 유일해야 함
7. **charPrIDRef 정합성**: section0.xml에서 참조하는 charPr ID가 header.xml에 존재해야 함
8. **venv 사용**: 프로젝트의 `.venv/bin/activate` (lxml 패키지 필요)
9. **검증 필수**: 생성 후 validate.py로 무결성 확인
10. **수식 크기**: `baseUnit="1000"` = 10pt (본문과 동일), 필요시 `1200`(12pt) 등 조절
11. **선택지 수식**: JSON에서 `$...$`로 감싸면 수식으로 처리. **반드시 한컴 수식 스크립트 문법** 사용 (`$3 sqrt 2$` ✓, `$3\sqrt{2}$` ✗ LaTeX 안됨). 예: `$30 pi$`, `$sqrt 3$`, `${x^2} over 2$`
12. **hp:sz width/height 0**: 한컴오피스가 렌더링 시 자동 계산하므로 0으로 설정 가능

---

## 학력평가/수능 시험지 형식 (기본값)

**학력평가 형식이 기본값이다.** 모든 문제 JSON은 반드시 `"exam_type": "학력평가"`를 포함하고, 각 문제에 `"points"` 배점을 지정해야 한다. 객관식은 5개 `"choices"`를 포함하고, 주관식은 `"section_label": "주관식"`을 지정한다.

### 시험지 JSON 형식

```json
{
  "exam_type": "학력평가",
  "year": 2020,
  "month": 3,
  "grade": "고1",
  "session": 2,
  "subject_area": "수학",
  "total_pages": 12,
  "question_type_label": "5지선다형",
  "problems": [
    {
      "text": "의 값은?",
      "equation": "-{7} over {2} times (-3) + 4 times left | -{5} over {2} right |",
      "points": 2,
      "choices": ["-1", "$-{1} over {2}$", "0", "${1} over {2}$", "1"]
    },
    {
      "section_label": "주관식",
      "text": "의 값을 구하시오.",
      "equation": "2x + 3 = 7",
      "points": 4
    }
  ]
}
```

### 시험지 전용 JSON 필드

| 필드 | 필수 | 설명 |
|------|------|------|
| `exam_type` | O | `"학력평가"`, `"수능"`, `"exam"` 중 하나 |
| `year` | X | 학년도 (예: 2020) |
| `month` | X | 시행 월 (예: 3) |
| `grade` | X | 학년 (예: "고1") |
| `session` | X | 교시 (기본: 2) |
| `subject_area` | X | 과목 영역 (기본: "수학") |
| `total_pages` | X | 총 페이지 수 (기본: 12) |
| `question_type_label` | X | 문항유형 라벨 (기본: "5지선다형") |
| `problems[].points` | X | 배점 (정수, `[2점]` 형태로 표시) |
| `problems[].section_label` | X | 섹션 구분 라벨 (예: "주관식") |

### 시험지 레이아웃 구조

```
┌─────────────────────────────────────────┐
│  2020학년도 3월 고1 전국연합학력평가 문제지   │ ← 1단 (전체너비)
│                                          │
│  제 2 교시        수학 영역               │ ← 1단 (전체너비)
├────────────────────┬────────────────────┤
│ ┌──────────┐       │                    │
│ │ 5지선다형  │       │                    │ ← 2단 시작
│ └──────────┘       │                    │
│                    │                    │
│ 1. 문제... [2점]   │ 3. 문제... [2점]   │
│  ① a ② b ③ c ④ d ⑤ e│  ① a ② b ③ c ④ d│ ← 가로 선택지
│                    │                    │
│ 2. 문제... [2점]   │ 4. 문제... [3점]   │
│  ① a ② b ③ c ④ d ⑤ e│  ① a ② b ③ c ④ d│
├────────────────────┴────────────────────┤
│                1 / 12                    │ ← 1단 (전체너비)
└─────────────────────────────────────────┘
```

### 단 전환 기법

exam 형식에서는 `hp:colPr`을 이용해 섹션 내 단 수를 전환한다:
1. secPr 문단에서 `colCount="1"`로 시작 (헤더 영역 전체너비)
2. 헤더 문단들 출력 후 `hp:colPr colCount="2"`로 전환 (본문 2단)
3. 본문 문제들 출력
4. (선택) `hp:colPr colCount="1"`로 전환 (하단 페이지 번호)

### 가로 선택지

tabPr ID 3에 정의된 5개 탭스톱을 이용해 선택지를 한 줄에 배치:
```
① -1    ② -1/2    ③ 0    ④ 1/2    ⑤ 1
```
각 선택지 사이에 `<hp:tab/>`을 삽입하여 균등 간격으로 배치한다.

### 빌드 예제

```bash
# 학력평가 형식 (기본값)
python3 "$SKILL_DIR/scripts/build_math_hwpx.py" \
    --problems problems.json \
    --creator "교육청" \
    --output exam.hwpx
```
