---
name: dxf-to-pdf
description: "Convert engineering DXF drawings to A-series single-page PDFs using the bundled dxf_converter CLI (no external install required). Supports single-file and folder batch conversion with optional recursion. Use when converting DXF files to PDF, batch-converting DXF drawings, or when the user mentions 'DXF to PDF', 'DXF 변환', 'DXF PDF 변환', '도면 PDF 변환', 'dxf_converter'."
---

# DXF to PDF Conversion Guide

엔지니어링 DXF 도면을 A계열 단일 페이지 PDF로 일괄 변환하는 가이드.
번들된 `dxf_converter` CLI(v0.1.0)를 직접 실행한다. 별도 설치·다운로드가 필요 없다.

Invocation hint: accept DXF file/folder path(s), output folder, and optional paper/dpi/color/recursive/overwrite settings.

CLI 자체는 `--mode preview`(단일 파일 PNG 미리보기)를 제공하지만, 이 스킬은 convert 모드만 지원한다 (preview 미지원).

## Bundled CLI Location

```
skills/dxf-to-pdf/
├── SKILL.md
├── .gitattributes                    # references/cli/** -text (번들 바이트 보존)
├── scripts/
│   └── convert-dxf.ps1               # 작업폴더 복사 → settings 생성 → 실행 → 파싱 → 정리
└── references/
    └── cli/                          # dxf_converter CLI 번들 (24개 파일)
        ├── dxf_converter.exe         # 변환 backend (90,624 B)
        ├── dxf_converter.exe.config  # bindingRedirect (exe와 반드시 같은 폴더)
        ├── ACadSharp.dll             # 그 외 런타임 DLL 13개 (총 14개)
        ├── contracts/
        │   ├── settings.schema.json
        │   ├── progress-event.schema.json
        │   └── manifest.schema.json
        ├── settings.json             # 템플릿 (수정하지 않는다)
        ├── settings.ini              # 추가 폰트 검색 경로 템플릿
        ├── release-manifest.json     # 파일별 SHA-256 무결성 manifest
        ├── README.txt
        └── THIRD-PARTY-NOTICES.txt
```

> **경고**: `dxf_converter.exe`만 복사하면 sibling DLL 로드에 실패한다. `dxf_converter.exe.config`(bindingRedirect)도 exe와 반드시 동일 폴더에 있어야 한다. 번들은 항상 폴더 통째로 다뤄야 한다.

## 필수 정보 프롬프팅 워크플로우

| # | 정보 | 미제공 시 행동 |
|---|------|---------------|
| 1 | 입력 DXF 파일/폴더 경로 | **반드시 질문** (절대경로 요구) |
| 2 | 출력 폴더 | **반드시 질문** (절대경로 요구) |
| 3 | 용지/방향/DPI/색상 | 질문하지 않음 — A4/landscape/300/monochrome 기본값 적용 후 보고에 명시 |
| 4 | 하위 폴더 포함(recursive) | 질문하지 않음 — 기본 false, 사용자가 "하위 폴더/전체/재귀" 언급 시 true |
| 5 | 기존 PDF 덮어쓰기 | 질문하지 않음 — 기본 skip, 사용자가 "덮어써" 언급 시 `-Overwrite` |

## Running the Bundled CLI

표준 실행법은 `scripts/convert-dxf.ps1` 호출 1가지로 통일한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "& '<skill>\scripts\convert-dxf.ps1' -InputPath 'D:\dwg\a.dxf','D:\dwg\folder' -OutputFolder 'D:\out' [-Recursive] [-Overwrite] [-PaperSize A3] [-Orientation portrait] [-Dpi 600] [-ColorMode color] [-KeepWorkFolder]"
```

`-InputPath`는 파일·폴더를 섞어서 배열로 넘길 수 있다. `-Recursive`는 폴더 입력에만 적용된다.

> **`-File`을 쓰지 말 것**: `powershell -File`은 `[string[]]` 파라미터에 값을 하나만 바인딩하고 나머지를 조용히 버린다. 입력이 2개 이상이면 뒤쪽 경로가 경고 없이 무시되므로 반드시 위의 `-Command "& ..."` 형식을 사용한다.
>
> 이미 PowerShell 세션 안이라면 `& "<skill>\scripts\convert-dxf.ps1" -InputPath "a","b" -OutputFolder "out"` 처럼 직접 호출해도 된다. 경로에 작은따옴표가 있으면 `''`로 이스케이프한다.

### 왜 작업 폴더로 복사해서 실행하는가

- 스킬 설치 위치(플러그인 캐시 등)는 쓰기 가능이 보장되지 않는다.
- CLI는 실행 시 BundleRoot에 `logs\`를 생성하고 output_folder에 쓰기 프로브를 수행한다.
- 번들 `README.txt`도 "쓰기 가능한 폴더에 전체 폴더를 복사하여 사용"을 지시한다.

스크립트가 매 실행마다 `%TEMP%\dxf2pdf_<8hex>`로 번들 전체를 복사한 뒤 그 사본에서 실행한다. 번들 원본은 읽기 전용으로만 접근한다.

### 작업 폴더 수명주기

| 실행 결과 | 작업 폴더 |
|-----------|-----------|
| 성공(exit 0) | 삭제 |
| 스킵만 발생한 부분완료(exit 1, failed==0, cancelled==0) | 삭제 |
| 변환 실패(failed>0) 또는 exit 2/3/4 | **보존 + 경로 보고** (logs 포함) |
| 사전 검증 실패(exit 10) | 애초에 생성되지 않음 |
| `-KeepWorkFolder` 지정 | 결과와 무관하게 보존 |

## CLI 인자 구조

```
dxf_converter.exe --mode convert --settings <path> --progress json
```

| 인자 | 스킬에서의 값 | 설명 |
|------|---------------|------|
| `--mode` | `convert` (고정) | 변환 모드 |
| `--settings` | 매 실행 생성한 `run-settings.json` | 설정 JSON 경로 (필수) |
| `--progress` | `json` (고정) | JSON Lines 출력 — 구조화 파싱용 |
| `--cancel-file` | 사용 안 함 | 협조적 취소용. 이 스킬의 기본 워크플로우는 사용하지 않는다 |

> 번들 `README.txt` L28은 `--progress <json|plain>`으로 표기하지만 실제 허용값은 `json|console`이다. 스킬은 `json`만 사용한다. 번들 파일은 수정하지 않는다.

**사용 금지 옵션**: `--internal-worker`, `--request`, `--response`, `--run-id` 등 내부 전용 옵션과 미리보기 계열 옵션은 이 스킬에서 사용하지 않는다.

## Configuration (run-settings.json)

스크립트가 작업 폴더에 생성하는 설정 파일이다. 번들의 `settings.json` 템플릿은 절대 수정하지 않는다.

```json
{
  "schema_version": 1,
  "input_sources": [
    { "source_id": "s1", "kind": "folder", "path": "D:\\dwg", "recursive": false, "output_prefix": "" }
  ],
  "resolved_inputs": [],
  "output_folder": "D:\\out",
  "paper": { "size": "A4", "orientation": "landscape", "margin_mm": 5.0, "fit_to_page": true },
  "render": {
    "dpi": 300,
    "color_mode": "monochrome",
    "model_space_only": true,
    "fail_on_unsupported": true,
    "font_paths": []
  },
  "behavior": {
    "overwrite": false,
    "skip_if_exists": true,
    "continue_on_error": true,
    "max_parallelism": 1,
    "file_timeout_seconds": 900,
    "batch_deadline_seconds": 21600,
    "cancel_grace_seconds": 15
  }
}
```

| 필드 | 기본값 | 설명 |
|------|--------|------|
| `input_sources[].kind` | — | `file` 또는 `folder` |
| `input_sources[].recursive` | false | 폴더 입력에만 유효. 하위 폴더 재귀 열거 |
| `input_sources[].output_prefix` | `""` | 출력 상대경로 접두사 |
| `resolved_inputs` | `[]` | CLI가 자동 확장. 스킬은 항상 빈 배열로 넘긴다 |
| `paper.size` | `A4` | `A4`/`A3`/`A2`/`A1`/`A0` |
| `paper.orientation` | `landscape` | `landscape`/`portrait` |
| `paper.margin_mm` | 5.0 | 0~50 |
| `render.dpi` | 300 | 72~1200 |
| `render.color_mode` | `monochrome` | `monochrome`(DeviceGray) / `color`(DeviceRGB) |
| `render.fail_on_unsupported` | true | 미지원 엔티티에서 실패 처리 |
| `behavior.continue_on_error` | true | 한 파일 실패해도 배치 계속 |
| `behavior.file_timeout_seconds` | 900 | 파일당 타임아웃 |
| `behavior.batch_deadline_seconds` | 21600 | 배치 전체 데드라인 |

### Preflight 불변 규칙

| 규칙 | 내용 |
|------|------|
| 절대경로 필수 | 입력·출력 모두 드라이브 문자 포함 전체 경로. drive-relative(`C:foo`)도 거부 |
| `.dxf`만 | 파일 입력은 확장자 `.dxf`만 허용 |
| `max_parallelism` == 1 | 고정. 다른 값은 `parallelism_not_supported` |
| `model_space_only` == true | 고정 |
| `fit_to_page` == true | 고정 |
| overwrite/skip_if_exists 동시 true 금지 | 스크립트가 항상 반대값으로 묶는다 |
| `output_inside_input` 금지 | 출력 폴더가 입력 폴더 내부에 있으면 안 됨 |
| `input_source_overlap` 금지 | 입력 소스끼리 경로가 겹치면 안 됨 |
| `output_collision` 금지 | 서로 다른 입력이 같은 출력 경로로 수렴하면 안 됨 |
| `resolved_inputs` == `[]` | 스킬은 항상 빈 배열로 넘겨 CLI가 확장하게 한다 |

## Output Contract & Reporting

### 종료 코드

| 코드 | 의미 | 해석 |
|------|------|------|
| 0 | Success | 전건 성공 |
| 1 | PartialFailure | 일부 실패 **또는 스킵만 발생** — 아래 해석 규칙 참조 |
| 2 | ConfigurationError | 설정/preflight 위반 |
| 3 | Cancelled | 취소됨 |
| 4 | InternalError | 내부 오류 |
| 10 | (스크립트 전용) | `convert-dxf.ps1`의 사전 검증 실패. CLI는 실행되지 않았다 |

> **해석 규칙**: `exit 1`이면서 `result` 이벤트의 `failed == 0`, `skipped > 0`이면 실패가 아니라 **기존 PDF 스킵으로 인한 부분완료**다. 사용자에게 실패로 보고하지 말 것. 스크립트도 이 경우를 정상 종결로 보고 작업 폴더를 삭제한다.

### JSON Lines 이벤트 (stdout)

공통 필드: `protocol_version`, `run_id`, `sequence`, `timestamp_utc`, `type`, `code`

| `type` | 핵심 필드 |
|--------|-----------|
| `progress` | `step`, `current`, `total`, `message` |
| `log` | `level`, `message` |
| `error` | `message`, `code` |
| `file_result` | `file_id`, `status`, `input_file`, `output_file`, `elapsed_ms` |
| `result` (마지막 정확히 1개) | `status`, `manifest_state`, `succeeded`, `failed`, `skipped`, `cancelled`, `elapsed_ms`, `manifest_file` |

### Manifest

실행별로 output_folder에 `dxf_conversion_manifest_*.json`이 생성된다. `summary`(total/succeeded/failed/skipped/cancelled)와 파일별 `status`를 담는다.

| `status` | 의미 |
|----------|------|
| `success` | 변환 성공 |
| `failure` | 변환 실패 |
| `skipped_verified` | 기존 출력이 있고 검증됨 → 스킵 |
| `skipped_unverified` | 기존 출력이 있으나 미검증 → 스킵 |
| `cancelled` | 취소됨 |
| `not_run` | 실행되지 않음 |

### 사용자 보고 형식

1. 성공/실패/스킵 건수 (`result` 이벤트 기준)
2. 실패한 파일 목록 (입력 경로 + status + message)
3. 출력 폴더 경로와 manifest 파일 경로
4. **적용된 설정 명시** (예: "A4 landscape, 300dpi, monochrome, recursive 미적용, 기존 파일 스킵")

출력은 원자적으로 commit된다(임시 파일 완성 후 move). 따라서 중단되더라도 반쪽짜리 PDF는 남지 않는다.

## Encoding Rules

- CLI stdout은 **UTF-8 no-BOM JSON Lines** 계약이다.
- PowerShell로 직접 캡처하면 콘솔 코드페이지(cp949)로 재해석되어 한글이 깨진다. 반드시 `ProcessStartInfo.StandardOutputEncoding = UTF8` 경로로 읽어야 한다 — `convert-dxf.ps1`이 이를 수행한다. `>` 리다이렉트로 받지 말 것.
- 작업 폴더의 `progress.jsonl`은 UTF-8 no BOM으로 보존된다. 읽을 때도 UTF-8로 읽는다.
- `convert-dxf.ps1`은 **UTF-8 with BOM**이다. PS 5.1이 BOM 없는 `.ps1`의 한글 리터럴을 cp949로 오해석하기 때문이다.
- 한글 경로·한글 파일명 산출물을 다룬 뒤에는 반드시 read-back으로 모지바케 시그니처(U+FFFD, `占쏙옙`, `ï»¿`, 한글 자리의 `?`)를 확인한다 (전역 인코딩 정책).

## Dependent DLLs

`references/cli/`의 런타임 DLL 14개. 전부 exe와 같은 폴더에 있어야 한다.

| DLL | 용도 |
|-----|------|
| `ACadSharp.dll` | DXF 파싱 |
| `DxfToPdfConverter.Core.dll` | 변환 엔진 |
| `DxfToPdfConverter.Contracts.dll` | settings/progress/manifest 계약 타입 |
| `OpenMcdf.dll` | 복합 문서(Compound File) 처리 |
| `Microsoft.Bcl.AsyncInterfaces.dll` | .NET 4.8 BCL 백포트 (bindingRedirect 대상) |
| `Microsoft.Bcl.HashCode.dll` | 〃 |
| `System.Buffers.dll` | 〃 |
| `System.Memory.dll` | 〃 |
| `System.Numerics.Vectors.dll` | 〃 |
| `System.Runtime.CompilerServices.Unsafe.dll` | 〃 |
| `System.Text.Encodings.Web.dll` | 〃 |
| `System.Text.Json.dll` | JSON 직렬화 (BCL 백포트) |
| `System.Threading.Tasks.Extensions.dll` | .NET 4.8 BCL 백포트 |
| `System.ValueTuple.dll` | 〃 |

전제조건: Windows 10/11 64비트 + .NET Framework 4.8.

## Error Handling

| 상황 | 처리 |
|------|------|
| exit 2 (ConfigurationError) | 보존된 작업 폴더의 `run-settings.json`을 Preflight 불변 규칙 표와 대조 |
| exit 1 (PartialFailure) | `failed>0`이면 실패 파일 목록 보고. `failed==0 & skipped>0`이면 **스킵 완료**로 보고 |
| exit 3 (Cancelled) | 취소 요청 여부 확인. 이 스킬은 취소 워크플로우를 사용하지 않는다 |
| exit 4 (InternalError) | 보존된 작업 폴더의 `logs\dxf_converter_*.log` 확인 |
| exit 10 (스크립트 사전 검증) | stderr 메시지대로 경로 수정. CLI는 실행되지 않았으므로 산출물·작업 폴더 없음 |
| exe 기동 실패 | .NET Framework 4.8 미설치 또는 32비트 환경. `0x80131700` 등 CLR 로드 오류 안내. 스킬이 런타임을 설치하지 않는다 |
| 출력 폴더 쓰기 거부 (ACL/읽기전용) | CLI 자체 쓰기 프로브가 ConfigurationError로 노출. 폴더 권한 확인을 안내 |
| MAX_PATH 초과 진단 노출 | 입력·출력 경로를 더 짧은 위치로 옮기도록 안내 (작업 폴더 복사로는 해결되지 않는다) |
| AV/조직 정책이 `%TEMP%` exe 실행 차단 | 관리자에게 예외 등록 요청 안내. 우회 시도 금지 |
| 작업 폴더 잔존 | `%TEMP%\dxf2pdf_*` 확인 후 불필요하면 수동 삭제 |

## When to Use This Skill

- 사용자가 DXF 도면을 PDF로 변환해 달라고 요청할 때
- 폴더 단위로 DXF를 일괄 변환할 때 (하위 폴더 포함 여부 선택)
- 파일과 폴더를 섞어 한 번에 변환할 때
- 용지 크기·DPI·흑백/컬러를 지정한 도면 PDF 출력이 필요할 때

## References

- 번들 README: [references/cli/README.txt](references/cli/README.txt)
- 설정 스키마: [references/cli/contracts/settings.schema.json](references/cli/contracts/settings.schema.json)
- 진행 이벤트 스키마: [references/cli/contracts/progress-event.schema.json](references/cli/contracts/progress-event.schema.json)
- Manifest 스키마: [references/cli/contracts/manifest.schema.json](references/cli/contracts/manifest.schema.json)
- 실행 스크립트: [scripts/convert-dxf.ps1](scripts/convert-dxf.ps1)
- 원본 참조: `D:\002_C_Sharp\dxf_to_pdf\dxf_converter\release-cli` (v0.1.0)
