# HWPX 파일 구조

## 개요

HWPX는 ZIP 형식의 압축 파일. `.hwpx` 확장자를 가진 한글 Open Document.

## 디렉토리 구조

```
hwpx파일/
├── Contents/
│   ├── section0.xml    # 본문 내용 (첫 번째 섹션)
│   ├── section1.xml    # 추가 섹션 (있는 경우)
│   └── header.xml      # 헤더 정보
├── settings.xml        # 문서 설정
└── mimetype            # 파일 타입 정보
```

## XML 네임스페이스

`hp` = `http://www.hancom.co.kr/hwpml/2011/paragraph`

## 주요 태그

| 태그 | 의미 |
|------|------|
| `<hp:tbl>` | 표 (table) |
| `<hp:tr>` | 행 (table row) |
| `<hp:tc>` | 셀 (table cell) |
| `<hp:t>` | 텍스트 내용 |
| `<hp:p>` | 문단 (paragraph) |

## 표 구조 예시

```xml
<hp:tbl>
  <hp:tr>
    <hp:tc><hp:p><hp:t>필드명</hp:t></hp:p></hp:tc>
    <hp:tc><hp:p><hp:t>값</hp:t></hp:p></hp:tc>
  </hp:tr>
</hp:tbl>
```

## 필드 추출 패턴

2열 표에서 첫 번째 열은 필드명, 두 번째 열은 값.

## XML 특수문자 이스케이프

| 원본 | 이스케이프 |
|------|-----------|
| `&` | `&amp;` |
| `<` | `&lt;` |
| `>` | `&gt;` |

## 줄바꿈

줄바꿈이 필요한 경우 여러 `<hp:p>` 태그 사용.

## 압축/해제 명령

```bash
# 해제
unzip -o {파일}.hwpx -d {임시디렉토리}/

# 재압축 (반드시 임시디렉토리 안에서 실행)
cd {임시디렉토리}
zip -r {출력파일}.hwpx *
```

## OS별 지원

| OS | .hwp | .hwpx |
|----|------|-------|
| Windows (pyhwpx) | O | O |
| macOS/Linux (XML) | X | O |

macOS/Linux에서 `.hwp`는 지원 불가 → 한글에서 `.hwpx`로 다시 저장하라고 안내.

## pyhwpx 설치

```bash
pip install pyhwpx
```

Windows + 한글 프로그램 설치 필수. 한글의 COM API를 사용.
