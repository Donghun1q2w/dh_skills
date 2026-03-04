---
name: hwp-template
description: 한글 서식 파일을 재사용 가능한 템플릿으로 저장하고 관리(목록, 상세, 삭제)합니다. "템플릿 저장", "서식 등록", "템플릿 목록", "서식 관리", "hwp 템플릿", "템플릿 삭제", "등록된 서식", "서식 목록 확인" 요청시 사용합니다.
---

# 한글 템플릿 관리

## 입력
$ARGUMENTS

## 명령어

| 명령어 | 설명 | 예시 |
|--------|------|------|
| `save <이름> <파일>` | 템플릿으로 저장 | `/hwp-template save IRB IRB서식.hwpx` |
| `list` | 저장된 템플릿 목록 | `/hwp-template list` |
| `info <이름>` | 템플릿 상세 정보 | `/hwp-template info IRB` |
| `delete <이름>` | 템플릿 삭제 | `/hwp-template delete IRB` |

## 스크립트 사용

[scripts/manage_template.py](scripts/manage_template.py) 실행:

```bash
python scripts/manage_template.py save IRB "IRB서식.hwpx"
python scripts/manage_template.py list
python scripts/manage_template.py info IRB
python scripts/manage_template.py delete IRB
```

`--templates-dir` 옵션으로 저장 경로 변경 가능 (기본: `./templates`).

## 저장 구조

```
{프로젝트}/
└── templates/
    ├── index.json      # 템플릿 메타데이터
    └── {이름}.hwpx     # 템플릿 파일들
```

## 활용

저장된 템플릿은 `/hwp-fill`에서 파일 경로 대신 이름으로 사용:

```
/hwp-fill IRB 내용.md
```

→ `templates/IRB.hwpx`를 자동으로 찾아서 사용

## 에러 처리

| 상황 | 대응 |
|------|------|
| 동일 이름 저장 | 덮어쓰기 확인 |
| 존재하지 않는 템플릿 조회/삭제 | 등록된 목록 표시 안내 |
| templates/ 디렉토리 없음 | 자동 생성 |
| 템플릿 이름 특수문자 | 영문/한글/숫자만 허용 안내 |

## 주의사항

- `templates/` 디렉토리는 `.gitignore`에 추가 권장 (개인 서식)
- 필드 목록은 `save` 시 자동 추출되지 않음 → `/hwp-analyze`로 별도 분석
