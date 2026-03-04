---
name: hwp-analyze
description: 한글 파일(.hwp, .hwpx)의 구조를 분석하여 표 구조, 필드 목록, 채워야 할 빈 칸을 식별합니다. "hwp 분석", "hwpx 분석", "서식 분석", "한글 파일 구조", "서식 필드 확인", "한글 파일 열기", "hwp 읽기", "한글 서식 파악", "hwp 필드 목록" 요청시 사용합니다.
---

# 한글 파일 분석

## 입력
$ARGUMENTS

HWPX XML 구조 상세: [references/hwpx-structure.md](references/hwpx-structure.md)

## 처리 방법

### Windows: pyhwpx

```python
from pyhwpx import Hwp

hwp = Hwp()
hwp.open("서식.hwp")

fields = hwp.get_field_list()
for field in fields:
    value = hwp.get_field_text(field)
    print(f"{field}: {value}")

hwp.quit()
```

### macOS/Linux: XML 파싱 (.hwpx만)

1. `unzip -o {파일}.hwpx -d {임시}/`
2. Read 도구로 `{임시}/Contents/section0.xml` 읽기
3. `<hp:tbl>` → `<hp:tr>` → `<hp:tc>` → `<hp:t>` 순서로 표 파싱
4. 2열 표: 첫 번째 열 = 필드명, 두 번째 열 = 값
5. `rm -rf {임시}`

## 출력

- 발견된 표 개수
- 채워야 할 필드 목록 (빈 칸)
- 이미 채워진 필드 (있다면)
- 다음 단계 안내 (`/hwp-fill`로 채우기)

## 에러 처리

| 상황 | 대응 |
|------|------|
| `.hwp` on macOS/Linux | `.hwpx`로 재저장 안내 |
| pyhwpx 미설치 (Windows) | `pip install pyhwpx` 안내, 한글 프로그램 설치 여부 확인 |
| 한글 프로그램 실행 중 | 한글을 닫고 재시도하거나 `hwp.quit()` 후 재실행 안내 |
| 깨진 HWPX (unzip 실패) | 파일 손상 안내, 한글에서 다시 저장 권고 |
| 병합 셀 포함 표 | 구조가 다르게 보일 수 있음 경고, 수동 확인 권고 |
