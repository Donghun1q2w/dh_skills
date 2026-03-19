# 학력평가/수능 시험지 형식 (exam format)

학력평가 형식이 math-hwpx의 기본값이다. 모든 문제 JSON은 반드시 `"exam_type": "학력평가"`를 포함하고, 각 문제에 `"points"` 배점을 지정해야 한다.

## 시험지 전용 JSON 필드

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

## 시험지 레이아웃 구조

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

## 페이지 설정 (문제지 최적화)

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

## 단 전환 기법

exam 형식에서는 `hp:colPr`을 이용해 섹션 내 단 수를 전환한다:
1. secPr 문단에서 `colCount="1"`로 시작 (헤더 영역 전체너비)
2. 헤더 문단들 출력 후 `hp:colPr colCount="2"`로 전환 (본문 2단)
3. 본문 문제들 출력
4. (선택) `hp:colPr colCount="1"`로 전환 (하단 페이지 번호)

## 가로 선택지

tabPr ID 3에 정의된 5개 탭스톱을 이용해 선택지를 한 줄에 배치:
```
① -1    ② -1/2    ③ 0    ④ 1/2    ⑤ 1
```
각 선택지 사이에 `<hp:tab/>`을 삽입하여 균등 간격으로 배치한다.

## 빌드 예제

```bash
# 학력평가 형식 (기본값)
python3 "$SKILL_DIR/scripts/build_math_hwpx.py" \
    --problems problems.json \
    --creator "교육청" \
    --output exam.hwpx
```

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

## 단위 변환 (HWPUNIT)

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
