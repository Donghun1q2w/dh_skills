---
name: hwp-fill
description: 한글 서식(.hwp, .hwpx)의 빈 필드에 내용을 채워 완성된 문서를 생성합니다. "서식 채우기", "hwp 작성", "한글 파일 채우기", "hwpx 채우기", "서식 입력", "한글 서식 작성", "hwp 필드 채우기", "서식에 데이터 넣기", "한글 문서 자동 작성" 요청시 사용합니다.
---

# 한글 파일 채우기

## 입력
$ARGUMENTS

HWPX XML 구조 상세: [../hwp-analyze/references/hwpx-structure.md](../hwp-analyze/references/hwpx-structure.md)

## 처리 방법

### Windows: pyhwpx

```python
from pyhwpx import Hwp

hwp = Hwp()
hwp.open("서식.hwp")

hwp.put_field_text("연구과제명", "AI 기반 진단 시스템")
hwp.put_field_text("연구책임자", "홍길동")

hwp.save_as("결과.hwp")
hwp.quit()
```

**참고**: pyhwpx는 "누름틀" 필드 사용. 누름틀이 없으면 표 셀을 직접 찾아서 수정.

### macOS/Linux: XML 직접 수정 (.hwpx만)

1. `mkdir -p {임시} && unzip -o {서식}.hwpx -d {임시}/`
2. `{임시}/Contents/section0.xml` 읽어서 표와 필드 파악
3. 입력 내용에서 필드-값 매핑 추출
4. **스마트 매칭** 수행 (아래 참조)
5. 사용자에게 매칭 결과 확인 받기
6. Edit 도구로 XML의 빈 `<hp:t>` 태그에 값 채우기
7. `cd {임시} && zip -r {출력}.hwpx *`
8. `rm -rf {임시}`

### 스마트 매칭

필드명이 정확히 일치하지 않아도 유연하게 매칭:
- `과제명` → `연구과제명` (부분 포함)
- `책임자` → `연구책임자` (유사어)
- `연구 기간` → `연구기간` (띄어쓰기 무시)

**반드시 사용자 확인**이 필요한 경우:
- 여러 후보가 있을 때
- 의미가 다를 수 있을 때
- 매칭할 필드를 못 찾았을 때

### 매칭 결과 표시 형식

```
매칭 결과:
- 연구과제명 ← "AI 기반 진단 시스템"
- 연구책임자 ← "홍길동"
- 연구기간 ← (내용 없음)

진행하시겠습니까?
```

## 출력

- 기본 파일명: `{원본}_filled.hwpx` (또는 `.hwp`)
- 사용자 지정 파일명 우선
- 채워진 필드 / 못 채운 필드 목록 표시
- 원본 파일은 수정하지 않음 (새 파일 생성)

## 에러 처리

| 상황 | 대응 |
|------|------|
| `.hwp` on macOS/Linux | `.hwpx`로 재저장 안내 |
| pyhwpx 미설치 (Windows) | `pip install pyhwpx` 안내, 한글 프로그램 설치 여부 확인 |
| 한글 프로그램 실행 중 충돌 | 한글을 닫고 재시도 안내 |
| 깨진 HWPX (unzip 실패) | 파일 손상 안내, 한글에서 다시 저장 권고 |
| XML 특수문자 | `&`→`&amp;`, `<`→`&lt;`, `>`→`&gt;` 이스케이프 |
| 누름틀 없는 서식 (Windows) | 표 셀 직접 수정 방식으로 fallback |
