---
name: e3d-launcher
description: "Launch AVEVA E3D modules (Design, Drawing, Paragon, Admin) as external processes via mon.exe. Generates Python or C# launcher code with proper arguments, paths, and config. Use when launching E3D applications, starting E3D modules, running mon.exe, or automating E3D process startup. Triggers on: 'E3D launch', 'E3D 실행', 'mon.exe', 'E3D design launch', 'E3D drawing', 'E3D paragon', 'E3D admin launch', 'E3D process start', 'E3D 모듈 실행'."
argument-hint: "<module> [--lang python|csharp] -- Launch E3D module (design|drawing|paragon|admin)"
---

# E3D Launcher Guide

E3D 모듈(Design, Drawing, Paragon, Admin)을 **외부 프로세스**로 실행하는 가이드.
`mon.exe`에 적절한 인자를 전달하여 E3D 애플리케이션을 기동한다.

> **e3d-standalone과의 차이**: `e3d-standalone`은 DLL 참조를 통한 프로그래매틱 접근(Standalone API), 이 스킬은 `Process.Start` / `subprocess`를 통한 프로세스 기동.

## 필수 정보 프롬프팅 워크플로우

사용자가 필수 정보를 제공하지 않은 경우 **반드시 물어본다**.

| # | 필수 정보 | 미제공 시 행동 |
|---|-----------|---------------|
| 1 | **설치 경로** | 기본 경로 2개 자동 탐색 후 발견된 경로 제시. 둘 다 없으면 사용자에게 질문 |
| 2 | **모듈** | `design`, `drawing`, `paragon`, `admin` 중 선택 요청. 매크로 경로도 가능 |
| 3 | **로그인 정보** | USERNAME, PASSWORD, MDB를 사용자에게 질문 (config 파일 경로 대안 제시) |
| 4 | **시작 모드** | 미지정 시 **CONSOLE**을 기본값으로 사용 (질문하지 않음) |

## 필수 경로

| 변수 | 설명 | 기본 경로 |
|------|------|-----------|
| `aveva_design_installed_dir` | E3D Design 설치 경로 | 1순위: `C:\cae_prog\AVEVA\v2.x\e3d\` |
|  |  | 2순위: `C:\Program Files (x86)\AVEVA\Everything3D2.10\` |
| `aveva_admin_installed_dir` | E3D Admin 설치 경로 | 1순위: `C:\cae_prog\AVEVA\v2.x\Administration\` |
|  |  | 2순위: `C:\Program Files (x86)\AVEVA\Administration\` |
| Target (공통) | 사용자 데이터 디렉토리 | `%PUBLIC%\Documents\AVEVA\USERDATA\` |

## 시작 모드

| 모드 | 설명 |
|------|------|
| `TTY` | 텍스트 터미널 모드 (배치 작업용) |
| `CONSOLE` | 콘솔 창 표시 (디버깅용) — **기본값** |
| `NOCONSOLE` | 콘솔 없이 실행 (일반 사용) |

사용자가 지정하지 않으면 `CONSOLE`로 진행한다.

## 모듈별 Launch 패턴

### Design / Drawing

```
fileName:  %aveva_design_installed_dir%\mon.exe
Argument:  PROD E3D init "%aveva_design_installed_dir%\launch.init" {시작모드} {PROJCODE} {USERNAME}/{PASSWORD} /{MDB} {COMMAND}
COMMAND:   design | drawing
```

### Paragon (Catalogue)

```
fileName:  %aveva_design_installed_dir%\mon.exe
Argument:  PROD CATALOGUE init "%aveva_design_installed_dir%\catalogue.init" {시작모드} {PROJCODE} {USERNAME}/{PASSWORD} /{MDB} paragon
COMMAND:   paragon (고정)
```

### Admin

```
fileName:  %aveva_admin_installed_dir%\mon.exe
Argument:  PROD ADMIN init "%aveva_admin_installed_dir%\admin.init" {시작모드} {PROJCODE} {USERNAME}/{PASSWORD} /{MDB} admin
COMMAND:   admin (고정)
```

### 인자 구조 요약

```
PROD {PRODUCT} init "{INIT_FILE}" {START_MODE} {PROJCODE} {USER}/{PASS} /{MDB} {COMMAND}
```

| 위치 | 필드 | 설명 |
|------|------|------|
| 1 | `PROD` | 고정 키워드 |
| 2 | `{PRODUCT}` | `E3D`, `CATALOGUE`, `ADMIN` |
| 3 | `init` | 고정 키워드 |
| 4 | `"{INIT_FILE}"` | init 파일 경로 (따옴표 필수) |
| 5 | `{START_MODE}` | `TTY` / `CONSOLE` / `NOCONSOLE` |
| 6 | `{PROJCODE}` | 프로젝트 코드 (대문자) |
| 7 | `{USER}/{PASS}` | 인증 정보 |
| 8 | `/{MDB}` | MDB 이름 (슬래시 접두사) |
| 9 | `{COMMAND}` | 모듈명 또는 매크로 경로 (선택) |

`COMMAND` 필드에 매크로 파일 경로를 넣으면 해당 매크로를 시작 시 자동 실행한다.

## Init 파일 커스터마이징 (Temp Init)

E3D 실행 전 환경변수를 설정하는 배치 파일을 init 파일에 추가해야 하는 경우가 있다.
원본 init 파일을 수정하지 않고, **temp init 파일**을 생성하여 사용한다.

### 절차

```
1. 원본 init 파일 전체를 읽는다 (예: launch.init)
2. 끝에 batch file 호출 라인을 추가한다
3. temp init 파일로 저장한다 (예: temp_launch.init)
4. mon.exe 인자에 temp init 파일 경로를 전달한다
5. 프로세스 종료 후 temp init 파일을 삭제한다 (cleanup)
```

### 추가되는 라인 예시

```
call "J:\cae_proj\evarProj.bat"
```

### Temp Init 파일 생성 (Python)

```python
def create_temp_init(init_path: str, batch_file: str) -> str:
    content = open(init_path, encoding="utf-8").read().rstrip()
    content += f'\ncall "{batch_file}"\n'
    temp_path = init_path.replace(".init", "_temp.init")
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(content)
    return temp_path
```

### Temp Init 파일 생성 (C#)

```csharp
string CreateTempInit(string initPath, string batchFile)
{
    var content = File.ReadAllText(initPath).TrimEnd()
        + Environment.NewLine
        + $"call \"{batchFile}\""
        + Environment.NewLine;
    var tempPath = initPath.Replace(".init", "_temp.init");
    File.WriteAllText(tempPath, content);
    return tempPath;
}
```

`batch_file`이 config에 지정되어 있으면 자동 적용, 없으면 원본 init 파일을 그대로 사용한다.

## Config 파일 구조

JSON config 파일로 프로젝트별 인증 정보와 설치 경로를 관리한다.

샘플: [references/config-sample.json](references/config-sample.json)

```json
{
  "settings": {
    "aveva_design_installed_dir": "C:\\cae_prog\\AVEVA\\v2.x\\e3d",
    "aveva_admin_installed_dir": "C:\\cae_prog\\AVEVA\\v2.x\\Administration",
    "target_dir": "%PUBLIC%\\Documents\\AVEVA\\USERDATA",
    "batch_file": "J:\\cae_proj\\evarProj.bat"
  },
  "projects": {
    "PROJCODE": {
      "USERNAME": "user",
      "PASSWORD": "pass",
      "MDB": "MASTER",
      "systemUSERNAME": "SYSTEM",
      "systemPASSWORD": "XXXXXX",
      "systeMDB": "MASTER"
    }
  }
}
```

- Design/Drawing/Paragon: `USERNAME` / `PASSWORD` / `MDB` 사용
- Admin: `systemUSERNAME` / `systemPASSWORD` / `systeMDB` 사용
- `batch_file`: 환경변수 배치 파일 경로 (선택, 있으면 temp init 자동 생성)

## 코드 생성 워크플로우

1. 사용자에게 언어 확인 (Python / C#)
2. 실행할 모듈 확인 (design, drawing, paragon, admin, 또는 매크로 경로)
3. 설치 경로 확인 — 기본 경로 2개 자동 탐색, 없으면 질문
4. 로그인 정보 확인 — config 파일 또는 직접 입력
5. 배치 파일 경로 확인 (환경변수 설정 필요 여부)
6. 해당 언어의 샘플 코드를 기반으로 런처 생성

Python 샘플: [references/e3d-launcher-sample.py](references/e3d-launcher-sample.py)
C# 샘플: [references/e3d-launcher-sample.cs](references/e3d-launcher-sample.cs)

## 경로 해석 규칙

1. 사용자 지정 경로가 있고 존재하면 → 사용
2. 기본 경로 1순위 탐색 (`C:\cae_prog\AVEVA\v2.x\e3d\`)
3. 1순위에서 `v2.x` → `v3.x` 대체 시도
4. 기본 경로 2순위 탐색 (`C:\Program Files (x86)\AVEVA\Everything3D2.10\`)
5. 모두 실패 → 사용자에게 경로 질문

```python
DEFAULT_DESIGN_PATHS = [
    r"C:\cae_prog\AVEVA\v2.x\e3d",
    r"C:\Program Files (x86)\AVEVA\Everything3D2.10",
]

def resolve_install_path(custom_path: str | None = None) -> str:
    if custom_path and os.path.exists(custom_path):
        return custom_path
    for path in DEFAULT_DESIGN_PATHS:
        if os.path.exists(path):
            return path
        v3 = path.replace("v2.x", "v3.x")
        if v3 != path and os.path.exists(v3):
            return v3
    raise FileNotFoundError("E3D 설치 경로를 찾을 수 없습니다.")
```

## Error Handling

| 상황 | 처리 |
|------|------|
| mon.exe 경로 없음 | `v2.x` → `v3.x` 대체 시도, 실패 시 에러 |
| init 파일 없음 | 설치 경로 재확인 안내 |
| 프로젝트 코드 없음 | config.json 확인 안내 |
| 프로세스 시작 실패 | 경로/권한 확인, UseShellExecute=false 확인 |
| 인증 실패 | USERNAME/PASSWORD/MDB 확인 (Admin은 system 계정 사용) |
| temp init 파일 잔존 | cleanup 실패 시 `*_temp.init` 파일 수동 삭제 안내 |

## References

- Config 샘플: [references/config-sample.json](references/config-sample.json)
- Python 런처: [references/e3d-launcher-sample.py](references/e3d-launcher-sample.py)
- C# 런처: [references/e3d-launcher-sample.cs](references/e3d-launcher-sample.cs)
- 원본 참조: `D:\001_Work\2026\029_E3D_Login\E3D_Proj_Login\E3DLogin\Services\E3DLauncher.cs`
