---
name: load-API-key
description: Shared API key loader using settings.ini and .env files from a department server. Use when the user asks to "load API keys", "read API key from server", "set up shared API key", "configure .env loading", "write API key loader code", or when implementing centralized API key management in Python, C#, or VBA projects. Also use when referencing shared server paths for .env files or setting up settings.ini-based configuration.
argument-hint: "[optional: target language (python/csharp/vba) or specific API key name]"
---

# Shared API Key Loader

부서 공용서버의 `.env` 파일에서 API 키를 로드하는 표준 패턴.

## 핵심 구조

```
project/
├── settings.ini              ← 공용서버 경로 설정 (Git 추적 가능)
├── shared_apikey_loader.py   ← 키 로드 유틸리티
├── .env                      ← 로컬 폴백 (Git 제외, .gitignore에 추가)
└── your_app.py               ← 실제 애플리케이션
```

## 동작 방식

1. `settings.ini`에서 공용서버 `.env` 경로를 읽음
2. 해당 경로의 `.env` 파일을 `python-dotenv`로 환경변수에 로드
3. 공용서버 접근 실패 시 로컬 `.env`로 폴백
4. `os.getenv()`로 개별 키를 참조

## settings.ini 형식

```ini
[server]
# UNC 경로 또는 로컬 마운트 경로
env_path = \\192.168.1.100\shared\config\.env

[options]
encoding = utf-8
use_local_fallback = true
local_env_path = .env
```

공용서버 경로는 반드시 `settings.ini`에서만 관리한다. 코드에 경로를 하드코딩하지 않는다.

## 사용 패턴

### Python
```python
from shared_apikey_loader import load_shared_keys, get_key

load_shared_keys()
api_key = get_key("OPENAI_API_KEY")
```

### C#
```csharp
var loader = new SharedApiKeyLoader();
loader.LoadSharedKeys();
string apiKey = loader.GetKey("OPENAI_API_KEY");
```

### VBA
```vb
LoadSharedKeys
Dim apiKey As String
apiKey = GetKey("OPENAI_API_KEY")
```

## 코드 작성 시 준수사항

1. **API 키를 소스코드에 직접 쓰지 않는다** — 항상 `get_key()` 함수를 통해 참조
2. **서버 경로는 settings.ini에서만 관리** — 경로 변경 시 코드 수정 불필요
3. **로컬 .env는 .gitignore에 반드시 추가** — `echo ".env" >> .gitignore`
4. **키 값 출력/로깅 시 마스킹** — `list_keys()` 함수는 자동 마스킹 적용
5. **폴백 메커니즘 유지** — 공용서버 접속 불가 시 로컬 개발 가능하도록

## 레퍼런스 코드

전체 구현 코드는 `references/` 디렉토리를 참조:

### Python
- `references/shared_apikey_loader.py` — 핵심 로더 모듈
- `references/usage_example.py` — 사용 예제

### C#
- `references/SharedApiKeyLoader.cs` — C# 구현 (IniParser 기반)

### VBA
- `references/SharedApiKeyLoader.bas` — VBA 모듈 (Excel/Access 등에서 사용)

### 공통
- `references/settings.ini` — 설정 파일 템플릿
- `references/sample.env` — .env 파일 샘플

새 프로젝트에 API 키 로딩을 추가할 때는 위 레퍼런스 파일들을 기반으로 프로젝트에 맞게 커스터마이징한다.

## 보안 주의사항

- 공용서버 `.env` 파일에는 NTFS 권한으로 부서원만 읽기 가능하게 설정
- `settings.ini`는 Git에 포함해도 무방 (경로 정보만 포함, 키 미포함)
- `.env` 파일은 절대 Git에 커밋하지 않음
- 키 순환 시 공용서버 `.env`만 업데이트하면 전체 반영
