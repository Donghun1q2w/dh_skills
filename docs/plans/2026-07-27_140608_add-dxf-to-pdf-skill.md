# 구현 계획: dxf-to-pdf 스킬 신규 작성 (번들 CLI 직접 실행형)

- **Date**: 2026-07-27 14:06:08
- **Status**: Completed

> Top-line goal: `skills/dxf-to-pdf/SKILL.md`를 새로 작성해, release-cli 전체(dxf_converter.exe + 종속 DLL들 + contracts 스키마)를 `skills/dxf-to-pdf/references/cli/`에 그대로 복사해 리포지에 커밋하고, 사용자가 DXF→PDF 변환을 요청하면 Claude가 settings.json을 생성해 이 CLI를 직접 실행함으로써(단일 파일과 폴더 배치 모두 지원, preview 모드는 제외) 실제 PDF 산출물을 생성하는 것을 성공 기준으로 한다.

> **⚠ 사용자 확인 필요 — 계획 작성자 임의 결정 3건 (dh-dev Step 2 리뷰에서 명시 확인 요망)**
> 확정된 5개 인터뷰 결정 외에 본 계획이 새로 내린 설계 판단입니다. 승인·거부·수정 지시가 가능합니다.
> 1. **기본값 무질문 정책**: 용지 A4/landscape·300dpi·monochrome은 사용자가 별도 지정하지 않으면 묻지 않고 적용하고, 완료 보고에 적용값을 명시한다 (근거: CLI 자체 기본 템플릿·README.txt L58-62와 동일값).
> 2. **자연어 의도 추론 정책**: "하위 폴더/전체/재귀" 언급 시 recursive=true, "덮어써" 언급 시 overwrite 모드. 언급 없으면 각각 false/skip.
> 3. **파라미터 노출**: convert-dxf.ps1에 PaperSize/Orientation/Dpi/ColorMode 옵션 파라미터를 노출한다 (기본값 재정의 수단).

플래닝 중 실측 확인 완료: `D:\002_C_Sharp\dxf_to_pdf\dxf_converter\release-cli\`(커밋 대상 24개 파일 + logs/ 2개), `release-cli\settings.json`(템플릿), `contracts\settings.schema.json`·`progress-event.schema.json`·`manifest.schema.json`(필드명 실측), `sampleDxf\`(DoD 대상 샘플 2개 존재), 리포지 `README.md`(L153-187 컨벤션), `skills/pdf2img/SKILL.md`, `skills/e3d-launcher/SKILL.md`, `skills/e3d-standalone/SKILL.md`.

---

## 1. Requirements Summary

- **신규 스킬** `skills/dxf-to-pdf/` 생성. 구성: `SKILL.md` + `references/cli/`(release-cli 전체 사본, 바이너리 포함) + `scripts/convert-dxf.ps1`(실행 자동화 스크립트) + `.gitattributes`(번들 바이너리 보호).
- **주 용도(확정)**: Claude가 직접 변환을 실행하는 직접 실행형 스킬 (pdf2img 스타일). 코드 생성용 아님.
- **exe 경로(확정)**: 번들 사본(`references/cli/`)이 유일한 진실원. 개발 원본 경로 fallback 탐색 없음.
- **바이너리 커밋(확정)**: exe/dll git 커밋 승인됨. `.gitignore` 예외 처리 불필요.
- **preview 모드(확정)**: 스킬 범위 제외. SKILL.md에 "지원하지 않음" 명시 문구 1개 포함 (AC-13/D-14로 검증).
- **배치 변환(확정)**: 단일 파일(kind=file)과 폴더(kind=folder, recursive 옵션), 그리고 파일+폴더 혼합 배열 입력 모두 지원.
- **핵심 기술 제약**: CLI는 exe 옆 sibling DLL 14개 + `dxf_converter.exe.config`(bindingRedirect) 필수. 실행 시 BundleRoot에 `logs/` 자동 생성 + output_folder에 쓰기 프로브. 스킬 설치 위치(`.claude/plugins/cache/...`)는 쓰기 보장이 없으므로 **매 실행 시 `%TEMP%` 하위 작업 폴더로 번들을 복사 후 사본에서 실행** (release-cli `README.txt` L11 "쓰기 가능한 폴더에 전체 폴더를 복사하여 사용"과 일치). 실행이 번들 원본에 어떤 쓰기도 하지 않음은 AT-14로 실측 검증.
- **기본값·추론·파라미터 정책**: 서두 "사용자 확인 필요" 박스의 3건 참조 (계획 작성자 결정, Step 2 승인 대상). **반드시 물어야 하는 것은 입력 경로와 출력 폴더 2개뿐**.
- **overwrite 정책**: 기본 `overwrite=false, skip_if_exists=true`. 덮어쓰기 요청 시 `overwrite=true, skip_if_exists=false`. 동시 true는 preflight 위반이므로 스크립트 구조상 발생 불가능. `(false,false)` 조합은 제공된 스펙에 의미가 정의되어 있지 않아 의도적으로 노출하지 않는다(결정론적 동작 보장 — 두 조합만 지원).
- **스코프 명시 제외**: preview 모드, `--cancel-file` 워크플로우, `file_timeout_seconds`/`batch_deadline_seconds` 초과 시나리오, 동일 output_folder 동시 실행 경쟁, 출력 폴더 ACL 쓰기 거부 시나리오 (§7 R-13·R-14).

## 2. Acceptance Criteria

Baseline: **현재 이 스킬은 존재하지 않음** (`skills/dxf-to-pdf/` 없음, README.md 스킬 목록 L7-28에 미등재). Before = "DXF→PDF 변환 요청 시 Claude가 수행할 방법 없음" → After = "스킬 존재 + 번들 CLI로 실제 변환 성공".

| # | 기준 | 판정 방법 |
|---|------|-----------|
| AC-1 | `skills/dxf-to-pdf/SKILL.md`가 존재하고 frontmatter `name: dxf-to-pdf`, `description`(영문, 트리거 문구 포함)이 유효 | AT-16, AT-18 |
| AC-2 | `references/cli/`에 정확히 24개 파일(루트 21 + contracts 3), `logs/` 미포함, `skills/dxf-to-pdf/.gitattributes` 존재 | AT-15 |
| AC-3 | 핵심 파일 존재: `dxf_converter.exe`(90,624B), `dxf_converter.exe.config`, `ACadSharp.dll`, `DxfToPdfConverter.Core.dll`, `DxfToPdfConverter.Contracts.dll`, contracts 스키마 3종 | AT-15 |
| AC-4 | `scripts/convert-dxf.ps1`이 파라미터로 입력/출력/옵션을 받아 작업 폴더 복사→settings 생성→실행→JSON Lines 파싱→요약 출력→정리를 수행 | AT-1~AT-14 |
| AC-5 | sampleDxf의 `001_110020-SIL-001-U-001(40)_Rev.0.dxf`, `002_110020-SIL-001-U-002(620)_Rev.0.dxf` 2개를 실제 변환하여 exit 0, output_folder에 `.pdf` 2개 + `dxf_conversion_manifest_*.json` 생성, manifest `summary.succeeded==2` | AT-2 |
| AC-6 | 단일 파일 변환 exit 0 + `.pdf` 1개 | AT-1 |
| AC-7 | preflight 위반 입력(비절대경로·drive-relative 포함, 비.dxf, output_inside_input)이 명확한 에러 메시지로 거부됨 | AT-4~AT-7 |
| AC-8 | 작업 폴더 수명주기: 성공(exit 0) 및 skip-only(exit 1, failed==0, cancelled==0) 시 삭제, 실패(failed>0 또는 exit 2/3/4) 시 보존+경로 보고, 사전검증 실패 시 애초 미생성 | AT-1·AT-4·AT-8·AT-13 |
| AC-9 | 리포지 `README.md` 스킬 목록 표와 디렉토리 구조 트리에 dxf-to-pdf 반영 | AT-19 |
| AC-10 | `quick_validate.py .\skills\dxf-to-pdf` exit 0 | AT-18 |
| AC-11 | progress.jsonl·SKILL.md·README.md·한글 경로 산출물의 한글이 read-back 시 무결 (모지바케 시그니처 0건) | AT-10, AT-12 |
| AC-12 | 바이너리 포함 커밋 생성 (dh-dev Step 4) | AT-20 |
| AC-13 | preview 제외가 산출물에 반영됨: SKILL.md에 preview 미지원 명시 문구 존재 + convert-dxf.ps1에 `preview` 문자열 0건 | AT-16 |

## 3. Implementation Steps (구현 지침)

### Step 1 — CLI 번들 복사 + .gitattributes

```powershell
robocopy "D:\002_C_Sharp\dxf_to_pdf\dxf_converter\release-cli" "D:\001_Work\2026\017_claude\plugins\dh_skills\skills\dxf-to-pdf\references\cli" /E /XD logs
if ($LASTEXITCODE -ge 8) { throw "robocopy 실패: $LASTEXITCODE" }   # robocopy는 0~7이 성공
```

- **`/XD logs`로 `logs/` 제외 (결정: `.gitkeep` 불필요)**. 근거: CLI는 실행 시 BundleRoot(=작업 사본) 안에 `logs/`를 스스로 생성하므로 리포지에 빈 logs/를 유지할 이유가 없고, git은 빈 디렉터리를 추적하지 못하며, 원본 logs/에는 실제 실행 로그 2개가 있어 커밋 오염이 된다.
- **`skills/dxf-to-pdf/.gitattributes` 신규 생성** (내용 정확히 1줄):

  ```
  references/cli/** -text
  ```

  근거: git 자동 텍스트 판별·`core.autocrlf` 정규화로부터 번들 전체(바이너리뿐 아니라 README.txt 등 텍스트 포함)를 보호. 번들 파일의 바이트가 원본과 동일하게 유지되어야 `release-manifest.json`의 SHA-256 무결성 대조가 성립한다.
- 복사 대상 24개 파일 (실측, 총 약 4.1MB):
  - 루트 21개: `ACadSharp.dll`(1,293,824B), `dxf_converter.exe`(90,624B), `dxf_converter.exe.config`(2,033B), `DxfToPdfConverter.Contracts.dll`(30,208B), `DxfToPdfConverter.Core.dll`(104,448B), `Microsoft.Bcl.AsyncInterfaces.dll`, `Microsoft.Bcl.HashCode.dll`, `OpenMcdf.dll`, `README.txt`, `release-manifest.json`, `settings.ini`, `settings.json`, `System.Buffers.dll`, `System.Memory.dll`, `System.Numerics.Vectors.dll`, `System.Runtime.CompilerServices.Unsafe.dll`, `System.Text.Encodings.Web.dll`, `System.Text.Json.dll`(644,904B), `System.Threading.Tasks.Extensions.dll`, `System.ValueTuple.dll`, `THIRD-PARTY-NOTICES.txt`
  - `contracts/` 3개: `manifest.schema.json`, `progress-event.schema.json`, `settings.schema.json`
- `settings.json`(placeholder)과 `settings.ini`([fonts] 빈 값)는 그대로 커밋. 실사용 설정은 매 실행 시 작업 폴더에 `run-settings.json`으로 생성 — 번들 템플릿은 절대 수정하지 않는다.
- 복사 후 검증: 파일 수 24, `logs` 부재 (AT-15와 동일 명령).

### Step 2 — 실행 스크립트 신규 작성: `skills/dxf-to-pdf/scripts/convert-dxf.ps1`

쓰기 가능성 문제의 해결책 본체. **파일 인코딩: UTF-8 with BOM** (PS 5.1은 BOM 없는 .ps1을 cp949로 읽어 한글 리터럴이 깨짐; pwsh 7은 BOM 유무 모두 UTF-8). PS 5.1/7 겸용 문법만 사용(삼항연산자·`??` 금지).

파라미터 시그니처:

```powershell
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string[]]$InputPath,      # .dxf 파일 및/또는 폴더, 절대경로 (혼합 허용)
    [Parameter(Mandatory = $true)][string]$OutputFolder,     # 절대경로, 없으면 생성
    [switch]$Recursive,                                       # 폴더 입력에만 적용
    [ValidateSet('A4','A3','A2','A1','A0')][string]$PaperSize = 'A4',
    [ValidateSet('landscape','portrait')][string]$Orientation = 'landscape',
    [ValidateRange(72,1200)][int]$Dpi = 300,
    [ValidateSet('monochrome','color')][string]$ColorMode = 'monochrome',
    [switch]$Overwrite,                                       # 지정 시 overwrite=true, skip_if_exists=false
    [switch]$KeepWorkFolder                                   # 디버깅용: 결과와 무관하게 작업 폴더 보존
)
```

처리 흐름 (전체 로직 — 구현자는 이 pseudocode를 그대로 코드화):

```powershell
$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }
function Fail([string]$msg) { [Console]::Error.WriteLine("[dxf-to-pdf] $msg"); exit 10 }

# (1) 번들 위치 해석 — $PSScriptRoot 기준 (스킬 설치 위치 무관)
$bundleSource = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\references\cli'))
if (-not (Test-Path (Join-Path $bundleSource 'dxf_converter.exe'))) { Fail "번들 CLI 없음: $bundleSource" }

# (2) 사전 검증 (preflight 위반을 CLI 실행 전에 차단, 전부 exit 10 — 이 단계 실패 시 작업 폴더는 아직 생성되지 않음)
function Assert-AbsolutePath([string]$p, [string]$label) {
    # IsPathRooted 단독 사용 금지: .NET Framework에서 drive-relative 경로("C:foo")도 true를 반환하는 오탐 존재.
    # PS 5.1의 .NET 4.x에는 Path.IsPathFullyQualified가 없으므로 정규식으로 판정 (슬래시 정규화 후).
    $n = $p -replace '/', '\'
    if (-not ($n -match '^[A-Za-z]:\\' -or $n -match '^\\\\')) {
        Fail "$label 이 절대경로가 아닙니다 (드라이브 문자 포함 전체 경로 필요): $p"
    }
}
foreach ($p in $InputPath) {
    Assert-AbsolutePath $p "입력 경로"
    if (-not (Test-Path $p)) { Fail "경로가 존재하지 않습니다: $p" }
    if ((Test-Path $p -PathType Leaf) -and ([System.IO.Path]::GetExtension($p).ToLowerInvariant() -ne '.dxf')) {
        Fail ".dxf 파일이 아닙니다: $p"
    }
}
Assert-AbsolutePath $OutputFolder "출력 폴더"
# output_inside_input 가드: 각 폴더형 입력의 FullPath+'\'가 OutputFolder FullPath+'\'의 접두사(OrdinalIgnoreCase)이면 Fail
$outFull = [System.IO.Path]::GetFullPath($OutputFolder).TrimEnd('\') + '\'
foreach ($p in $InputPath) {
    if (Test-Path $p -PathType Container) {
        $inFull = [System.IO.Path]::GetFullPath($p).TrimEnd('\') + '\'
        if ($outFull.StartsWith($inFull, [System.StringComparison]::OrdinalIgnoreCase)) {
            Fail "출력 폴더가 입력 폴더 내부에 있습니다 (output_inside_input): $OutputFolder"
        }
    }
}
New-Item -ItemType Directory -Force -Path $OutputFolder | Out-Null

# (3) 작업 폴더 생성 + 번들 복사
$work = Join-Path $env:TEMP ('dxf2pdf_' + [guid]::NewGuid().ToString('N').Substring(0, 8))
Copy-Item -Path $bundleSource -Destination $work -Recurse    # exe+DLL 14개+exe.config 통째 복사 (sibling DLL/bindingRedirect 요구 충족)

# (4) run-settings.json 생성 — contracts/settings.schema.json의 required 필드 전부 포함
$sources = @(); $i = 0
foreach ($p in $InputPath) {
    $i++; $isFolder = Test-Path $p -PathType Container
    $sources += [ordered]@{
        source_id = "s$i"
        kind = $(if ($isFolder) { 'folder' } else { 'file' })
        path = [System.IO.Path]::GetFullPath($p)
        recursive = [bool]($isFolder -and $Recursive)
        output_prefix = ''
    }
}
$settings = [ordered]@{
    schema_version = 1
    input_sources = $sources
    resolved_inputs = @()                      # 반드시 빈 배열 — CLI가 자동 확장 (해시 불일치 위험 제거)
    output_folder = [System.IO.Path]::GetFullPath($OutputFolder)
    paper = [ordered]@{ size = $PaperSize; orientation = $Orientation; margin_mm = 5.0; fit_to_page = $true }   # fit_to_page 반드시 true
    render = [ordered]@{ dpi = $Dpi; color_mode = $ColorMode; model_space_only = $true; fail_on_unsupported = $true; font_paths = @() }  # model_space_only 반드시 true
    behavior = [ordered]@{
        overwrite = [bool]$Overwrite
        skip_if_exists = (-not [bool]$Overwrite)   # (true,true) 구조적 불가능. (false,false)는 스펙상 의미 미정의라 미노출
        continue_on_error = $true
        max_parallelism = 1                        # 반드시 1 (parallelism_not_supported)
        file_timeout_seconds = 900; batch_deadline_seconds = 21600; cancel_grace_seconds = 15
    }
}
$settingsPath = Join-Path $work 'run-settings.json'
[System.IO.File]::WriteAllText($settingsPath, ($settings | ConvertTo-Json -Depth 6), (New-Object System.Text.UTF8Encoding($false)))  # UTF-8 no BOM

# (5) 실행 — System.Diagnostics.Process + UTF-8 강제 디코딩 (콘솔 코드페이지 cp949 무관화)
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = (Join-Path $work 'dxf_converter.exe')
$psi.Arguments = '--mode convert --settings "' + $settingsPath + '" --progress json'
$psi.WorkingDirectory = $work
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true; $psi.RedirectStandardError = $true
$psi.StandardOutputEncoding = [System.Text.Encoding]::UTF8
$psi.StandardErrorEncoding = [System.Text.Encoding]::UTF8
$proc = [System.Diagnostics.Process]::Start($psi)
$stderrTask = $proc.StandardError.ReadToEndAsync()   # 데드락 방지: stderr는 비동기로
$stdout = $proc.StandardOutput.ReadToEnd()
$proc.WaitForExit()
$exitCode = $proc.ExitCode; $stderr = $stderrTask.Result
[System.IO.File]::WriteAllText((Join-Path $work 'progress.jsonl'), $stdout, (New-Object System.Text.UTF8Encoding($false)))  # 원본 보존

# (6) JSON Lines 파싱 — contracts/progress-event.schema.json 실측 필드명 사용
#     공통: protocol_version, run_id, sequence, timestamp_utc, type, code
#     type='file_result' → file_id, status, input_file, output_file, elapsed_ms
#     type='result'(마지막 1개) → status, manifest_state, succeeded, failed, skipped, cancelled, elapsed_ms, manifest_file
$fileResults = @(); $finalResult = $null; $errors = @(); $badLines = 0
foreach ($line in ($stdout -split "`r?`n")) {
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    try { $evt = $line | ConvertFrom-Json } catch { $badLines++; continue }   # 조용히 버리지 않고 카운트
    if ($evt.type -eq 'file_result') { $fileResults += $evt }
    elseif ($evt.type -eq 'result') { $finalResult = $evt }
    elseif ($evt.type -eq 'error') { $errors += $evt }
}

# (7) 요약 출력 (Claude가 이 출력을 그대로 사용자 보고에 인용)
#  - "[dxf-to-pdf] 종료 코드: N (의미)" — 0 Success / 1 PartialFailure / 2 ConfigurationError / 3 Cancelled / 4 InternalError
#  - $finalResult 있으면: "성공 S / 실패 F / 스킵 K / 취소 C (elapsed Xms)", "Manifest: $($finalResult.manifest_file)"
#  - 실패 file_result마다: "  실패: {input_file} — {status}: {message}"
#  - $badLines -gt 0 이면: "경고: JSON 파싱 실패 라인 $badLines개 — progress.jsonl 확인 필요"
#  - $finalResult 없으면(비정상 조기 종료): stderr 전문 + stdout 앞 20줄 출력
#  - exit 1이면서 failed==0, skipped>0: "실패 없음 — 기존 PDF 스킵으로 인한 부분완료" 문구로 구분 보고

# (8) 정리 — skip-only 부분완료는 정상 종결로 취급해 삭제 (반복 재실행 시 %TEMP% 누적 방지)
$skipOnly = ($finalResult -ne $null) -and ($finalResult.failed -eq 0) -and ($finalResult.cancelled -eq 0)
$isCleanRun = ($exitCode -eq 0) -or (($exitCode -eq 1) -and $skipOnly)
if ($isCleanRun -and -not $KeepWorkFolder) {
    Remove-Item -Path $work -Recurse -Force
} else {
    Write-Output "[dxf-to-pdf] 작업 폴더 보존(로그 포함): $work"
}
exit $exitCode   # 스크립트 종료 코드 = CLI 종료 코드 (사전검증 실패만 10)
```

- **주의**: `--internal-worker`, `--request`, `--response`, `--run-id`, preview 계열 옵션(`--preview-file-id/width/height`)은 절대 사용·언급하지 않는다. 스크립트 본문·주석에 `preview` 문자열이 없어야 한다 (AT-16 판정 대상).
- **주의**: `ConvertTo-Json`의 단일 원소 배열 언랩 함정 — 중첩 프로퍼티(`input_sources = $sources`)로 넣으면 배열이 보존된다. `$sources | ConvertTo-Json` 형태로 배열 자체를 파이프하지 말 것. AT-9가 생성 JSON을 검증한다.

### Step 3 — `skills/dxf-to-pdf/SKILL.md` 신규 작성

인코딩 UTF-8(no BOM). frontmatter (README.md L157-167 컨벤션 — `argument-hint` 금지, 인자 힌트는 본문 첫머리):

```yaml
---
name: dxf-to-pdf
description: "Convert engineering DXF drawings to A-series single-page PDFs using the bundled dxf_converter CLI (no external install required). Supports single-file and folder batch conversion with optional recursion. Use when converting DXF files to PDF, batch-converting DXF drawings, or when the user mentions 'DXF to PDF', 'DXF 변환', 'DXF PDF 변환', '도면 PDF 변환', 'dxf_converter'."
---
```

본문 섹션 구성 (선례 매핑 명시 — 구현자는 이 순서·형식 그대로):

1. **제목 + 개요 + Invocation hint** — `pdf2img/SKILL.md` L6-10 스타일. "Invocation hint: accept DXF file/folder path(s), output folder, and optional paper/dpi/color/recursive/overwrite settings." + **preview 문구(정확히 이 문장 포함, AT-16 판정 대상)**: "CLI 자체는 `--mode preview`(단일 파일 PNG 미리보기)를 제공하지만, 이 스킬은 convert 모드만 지원한다 (preview 미지원)."
2. **Bundled CLI Location** — `pdf2img` "Reference Code Location" 스타일 코드블록 트리: `references/cli/` 구조(exe, exe.config, DLL 14개, contracts/ 3종, settings.json·ini 템플릿) + "exe만 복사하면 sibling DLL 로드 실패, `dxf_converter.exe.config`는 exe와 반드시 동일 폴더" 경고.
3. **필수 정보 프롬프팅 워크플로우** — `e3d-launcher/SKILL.md` L15-24 표 형식:

   | # | 정보 | 미제공 시 행동 |
   |---|------|---------------|
   | 1 | 입력 DXF 파일/폴더 경로 | **반드시 질문** (절대경로 요구) |
   | 2 | 출력 폴더 | **반드시 질문** (절대경로 요구) |
   | 3 | 용지/방향/DPI/색상 | 질문하지 않음 — A4/landscape/300/monochrome 기본값 적용 후 보고에 명시 |
   | 4 | 하위 폴더 포함(recursive) | 질문하지 않음 — 기본 false, 사용자가 "하위 폴더/전체/재귀" 언급 시 true |
   | 5 | 기존 PDF 덮어쓰기 | 질문하지 않음 — 기본 skip, 사용자가 "덮어써" 언급 시 -Overwrite |

4. **Running the Bundled CLI** — 표준 실행법은 **`scripts/convert-dxf.ps1` 호출 1가지로 통일**:

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File "<skill>\scripts\convert-dxf.ps1" `
     -InputPath "D:\dwg\a.dxf","D:\dwg\folder" -OutputFolder "D:\out" [-Recursive] [-Overwrite] `
     [-PaperSize A3] [-Orientation portrait] [-Dpi 600] [-ColorMode color] [-KeepWorkFolder]
   ```

   + "왜 작업 폴더 복사인가" 3줄(스킬 설치 위치는 쓰기 보장 없음 / CLI가 BundleRoot에 logs/ 생성 / release README.txt 지시사항) + 작업 폴더 수명주기 규칙(성공·skip-only=삭제, 실패=보존+경로 보고).
5. **CLI 인자 구조** — e3d-launcher "인자 구조 요약" 스타일 표: `--mode convert`(고정) / `--settings <path>`(매 실행 생성) / `--progress json`(고정 — 구조화 파싱용) / `--cancel-file`(협조적 취소, 스킬 기본 워크플로우 미사용) / 내부 전용 옵션 사용 금지 목록.
6. **Configuration (run-settings.json)** — `pdf2img` L98-131 패턴: 전체 JSON 템플릿 + 필드 설명 표 + **Preflight 불변 규칙 표** (절대경로 필수 / .dxf만 / max_parallelism=1 고정 / model_space_only=true 고정 / fit_to_page=true 고정 / overwrite·skip_if_exists 동시 true 금지 / output_inside_input 금지 / input_source_overlap 금지 / output_collision 금지 / resolved_inputs는 빈 배열로).
7. **Output Contract & Reporting** — 종료 코드 표(0~4 + 스크립트 10), JSON Lines 이벤트 5종과 핵심 필드, manifest 파일(`dxf_conversion_manifest_*.json`, status enum 6종), 사용자 보고 형식(성공/실패/스킵 수 + 실패 파일 목록 + 적용 설정 명시), "exit 1 + failed==0 + skipped>0은 실패가 아니라 스킵 완료" 해석 규칙 (AT-8 실측 결과를 문구에 반영).
8. **Encoding Rules** — stdout은 UTF-8 no-BOM JSON Lines 계약. PowerShell 직접 캡처 시 cp949 콘솔 코드페이지로 한글 깨짐 → 반드시 `StandardOutputEncoding = UTF8` 방식(스크립트가 수행). progress.jsonl은 UTF-8로 읽기. 한글 무결성 read-back 확인 절차(전역 CLAUDE.md 정책 준수).
9. **Dependent DLLs** — `e3d-standalone/SKILL.md` L10-24 관례의 표: DLL 14개 + 용도(ACadSharp: DXF 파싱 / DxfToPdfConverter.Core·Contracts: 변환 엔진·계약 / OpenMcdf: 복합문서 / System.*·Microsoft.Bcl.*: .NET 4.8 BCL 백포트, bindingRedirect 대상).
10. **Error Handling** — e3d-launcher L211-220 스타일 표: exit 2(설정 오류 → run-settings.json과 preflight 규칙 대조) / exit 1(부분 실패 → 실패 파일 목록 보고, 스킵-only는 완료로 보고) / exit 3(취소) / exit 4(내부 오류 → 보존된 작업 폴더 logs/ 확인) / exe 기동 실패(.NET 4.8/x64 미설치, 0x80131700 등 안내) / AV의 %TEMP% exe 실행 차단(예외 등록 안내, 우회 시도 금지) / **출력 폴더 쓰기 거부(ACL/읽기전용) — CLI 자체 쓰기 프로브가 ConfigurationError로 노출, 권한 확인 안내** / **MAX_PATH 초과 진단 노출 시 입력·출력 경로 단축 안내** / 작업 폴더 잔존 시 `%TEMP%\dxf2pdf_*` 수동 삭제 안내.
11. **When to Use This Skill** — pdf2img L145-150 스타일 불릿.
12. **References** — e3d-launcher L222-227 스타일 마크다운 링크: `[references/cli/README.txt]`, `[references/cli/contracts/settings.schema.json]`, `[references/cli/contracts/progress-event.schema.json]`, `[references/cli/contracts/manifest.schema.json]`, `[scripts/convert-dxf.ps1]`, 원본 참조 `D:\002_C_Sharp\dxf_to_pdf\dxf_converter\release-cli` (v0.1.0).

### Step 4 — 리포지 `README.md` 갱신

- 스킬 목록 표(L7-28) 끝에 행 추가: `| [dxf-to-pdf](skills/dxf-to-pdf/) | DXF 도면을 A계열 단일 페이지 PDF로 일괄 변환 (번들 dxf_converter CLI 실행) | C# CLI |`
- 디렉토리 구조 트리(L30-151)의 `skills/` 아래에 추가:

  ```
  │   ├── dxf-to-pdf/
  │   │   ├── SKILL.md              ← DXF→PDF 변환 실행 가이드
  │   │   ├── .gitattributes        ← 번들 바이너리 -text 보호
  │   │   ├── scripts/
  │   │   │   └── convert-dxf.ps1   ← 작업폴더 복사·실행·파싱 자동화
  │   │   └── references/
  │   │       └── cli/              ← dxf_converter CLI 번들 (exe+DLL+contracts)
  ```

### Step 5 — 스킬 검증 실행

```powershell
$env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'
python C:\Users\donghun.lee\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\skills\dxf-to-pdf
python C:\Users\donghun.lee\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .   # 2차(권장)
```

### Step 6 — 실전 변환 테스트 (§6 AT 스위트 전체 수행 후 DoD 판정)

## 4. Code Writing Guide (코드 작성 가이드)

- **CLI 스펙 불변**: 인자·스키마·preflight 규칙은 본 계획 기재 스펙 그대로. 재추측·변경 금지. `release-cli\README.txt` L28은 `--progress <json|plain>`으로 표기되어 있으나 소스 기준 정확한 값은 `json|console` — 스킬은 `json`만 사용하므로 SKILL.md에는 `json`만 문서화하고 번들 README.txt를 "수정"하려 들지 말 것 (번들 무수정 원칙).
- **PowerShell 호환성**: `convert-dxf.ps1`은 PS 5.1/7 겸용 — 삼항연산자, `??`, `?.` 금지. 조건식은 `$(if ... else ...)` 서브식. **절대경로 판정은 정규식 방식만 사용** (`IsPathRooted` 단독 금지 — drive-relative `C:foo` 오탐, `IsPathFullyQualified`는 .NET 4.x 부재).
- **인코딩 (전역 CLAUDE.md 정책)**:
  - `.ps1` → **UTF-8 with BOM** (PS 5.1의 cp949 오해석 방지 — 유일한 BOM 예외).
  - `SKILL.md`, `README.md`, `.gitattributes`, `run-settings.json`, `progress.jsonl` → UTF-8 no BOM.
  - CLI stdout 캡처는 반드시 `ProcessStartInfo.StandardOutputEncoding = UTF8` 경로로만. PowerShell `>` 리다이렉트 금지 (PS 5.1이 콘솔 인코딩으로 재인코딩).
  - Python 검증 스크립트 실행 전 `$env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'`.
  - 한글 산출물은 반드시 read-back 후 모지바케 시그니처(U+FFFD, `占쏙옙`, `ï»¿`) 검사.
- **네이밍**: 스킬명 kebab-case `dxf-to-pdf`(디렉토리명 일치). 스크립트 파라미터 PascalCase(PowerShell 관례). settings JSON 키는 CLI 스키마 그대로 snake_case.
- **SKILL.md 스타일**: frontmatter는 `name`/`description`만(영문 description, 트리거 문구 포함). 본문 한국어+영문 혼용(기존 스킬 관례), 표 중심, 번들 파일은 마크다운 링크로 명시 참조 (README.md L187).
- **의존성 제약**: 새 외부 의존성 금지. 스크립트는 PowerShell 내장 + .NET Framework 타입만. CLI는 .NET Framework 4.8 x64 전제 — 스킬 코드가 이를 대체 설치하려 시도하지 말 것.
- **preview 격리**: 스크립트·SKILL.md 실행 지침 어디에도 preview 옵션을 노출하지 않는다. SKILL.md의 preview 언급은 Step 3-1의 미지원 문구 1곳뿐.
- **주석 최소화**: WHY가 비자명한 곳만 (`resolved_inputs` 빈 배열 이유, ConvertTo-Json 언랩 함정, stderr 비동기 이유, 절대경로 정규식 이유, cleanup skip-only 규칙 이유).

## 5. Definition of Done (개발 완료조건 — 전부 이진 판정, 각 항목 ≥1개 AT 매핑)

| # | 조건 | 판정 AT |
|---|------|---------|
| D-1 | `skills/dxf-to-pdf/SKILL.md` 존재, frontmatter `name: dxf-to-pdf` + 영문 description | AT-16, AT-18 |
| D-2 | `references/cli/` 파일 수 == 24, `logs/` 부재, 핵심 7파일 존재, `skills/dxf-to-pdf/.gitattributes` 존재(내용 `references/cli/** -text`) | AT-15 |
| D-3 | `references/cli/dxf_converter.exe` 크기 == 90,624 bytes | AT-15 |
| D-4 | `scripts/convert-dxf.ps1` 존재, 앞 3바이트 == EF BB BF (UTF-8 BOM) | AT-17 |
| D-5 | quick_validate.py exit 0 | AT-18 |
| D-6 | **실전 배치 변환 성공**: in_flat(001+002) 폴더 입력 → exit 0, `.pdf` 정확히 2개 + manifest ≥1개, manifest `summary.succeeded==2, failed==0` | AT-2 (보강: AT-3, AT-11) |
| D-7 | **실전 단일 변환 성공**: 파일 1개 → exit 0, `.pdf` 1개, 크기 > 0 | AT-1 |
| D-8 | preflight 위반 4종(존재하지 않는 경로/비.dxf/output_inside_input/상대·drive-relative 경로)이 각각 비-0 종료 + 에러 메시지, 스크립트 가드는 CLI 판정과 교차 일치 | AT-4, AT-5, AT-6+6b, AT-7 |
| D-9 | 작업 폴더 수명주기: 성공 시 삭제 / skip-only 시 삭제 / 변환 실패 시 보존+경로 보고 / 사전검증 실패 시 미생성 | AT-1, AT-8, AT-13, AT-4 |
| D-10 | 재실행 멱등성: 기본 모드 재실행 시 manifest의 해당 파일 status가 `skipped_*`이고 PDF mtime 불변; `-Overwrite` 재실행 시 status `success`이고 mtime 갱신. **exit code는 참고 기록일 뿐 판정 기준이 아님** | AT-8 |
| D-11 | README.md 표+트리에 dxf-to-pdf 반영 | AT-19 |
| D-12 | 한글 무결성: progress.jsonl·한글 경로 산출물·SKILL.md·README.md read-back에서 모지바케 시그니처 0건 | AT-10, AT-12 |
| D-13 | 바이너리 포함 커밋 존재 (dh-dev Step 4에서 판정) | AT-20 |
| D-14 | preview 제외 반영: SKILL.md에 "preview 미지원" 명시 문구 존재 + convert-dxf.ps1에 `preview` 문자열 0건 | AT-16 |
| D-15 | 실행 AT 전체 수행 후 `references/cli/` 번들 원본 무변경 (스냅샷 비교 차이 0건) | AT-14 |

## 6. Adversarial Test Environment (적대적 테스트 환경)

**원칙: 실행 AT는 모킹 금지 — 실제 번들 exe를 실제로 실행.** 테스트 루트: 실행 세션 scratchpad 하위 `dxf-at\`. 준비 (AT-2/11/12/13 재현 코드 포함 — 이 블록만으로 전체 재현 가능):

```powershell
$AT = "<scratchpad>\dxf-at"
$S  = "D:\002_C_Sharp\dxf_to_pdf\dxf_converter\sampleDxf"
$F1 = "001_110020-SIL-001-U-001(40)_Rev.0.dxf"
$F2 = "002_110020-SIL-001-U-002(620)_Rev.0.dxf"
New-Item -ItemType Directory -Force -Path "$AT\in_single","$AT\in_flat","$AT\in_batch\sub","$AT\in_broken","$AT\한글 도면 폴더" | Out-Null
Copy-Item "$S\$F1" "$AT\in_single\"
Copy-Item "$S\$F1","$S\$F2" "$AT\in_flat\"                  # AT-2(D-6 본체) 입력
Copy-Item "$S\$F1" "$AT\in_batch\"
Copy-Item "$S\$F2" "$AT\in_batch\sub\"
Copy-Item "$S\$F1" "$AT\한글 도면 폴더\"                     # 공백+한글 경로 케이스
Set-Content -Path "$AT\in_batch\not_a_dxf.txt" -Value "dummy"
Set-Content -Path "$AT\in_broken\broken.dxf" -Value "this is not a valid dxf"   # 손상 DXF
# AT-14용 번들 스냅샷 (실행 AT 시작 전 1회)
$snapBefore = Get-ChildItem "<repo>\skills\dxf-to-pdf\references\cli" -Recurse -File | Select-Object FullName, Length, LastWriteTimeUtc
```

(샘플 파일명의 괄호가 인용 처리 결함을 자연 검출. 파일당 변환 약 3초 — 2026-07-27 스모크 로그 실측.)

### 실행 AT (실제 exe 실행)

| ID | 시나리오 | 실행 | 기대 결과 (이진 판정) | 대응 DoD |
|----|----------|------|----------------------|----------|
| AT-1 | 단일 파일 정상 변환 | `convert-dxf.ps1 -InputPath "$AT\in_single\$F1" -OutputFolder "$AT\out1"` | exit 0, out1에 `.pdf` 1개(>0B) + manifest, 요약 "성공 1", 해당 런 `%TEMP%\dxf2pdf_*` 삭제됨 | D-7, D-9 |
| AT-2 | **평면 폴더 배치 (D-6 본체)** | `-InputPath "$AT\in_flat" -OutputFolder "$AT\out2"` | exit 0, `.pdf` 2개(001·002), manifest `summary.succeeded==2, failed==0` | D-6 |
| AT-3 | recursive on/off 대비 | off: `-InputPath "$AT\in_batch" -OutputFolder "$AT\out3a"` / on: 동일+`-Recursive` `-OutputFolder "$AT\out3b"` | out3a PDF 1개(001만, .txt 자연 제외) vs out3b PDF 2개(sub\002 포함) | D-6 보강 |
| AT-4 | 존재하지 않는 경로 | `-InputPath "$AT\ghost.dxf" -OutputFolder "$AT\out4"` (실행 전후 `(Get-ChildItem $env:TEMP -Filter dxf2pdf_*).Count` 기록) | exit 10, "경로가 존재하지 않습니다", out4 산출물 0, **TEMP 폴더 수 증가 0 (작업 폴더 미생성)** | D-8, D-9(미생성측) |
| AT-5 | 비-.dxf 확장자 | `-InputPath "$AT\in_batch\not_a_dxf.txt" -OutputFolder "$AT\out5"` | exit 10, ".dxf 파일이 아닙니다" | D-8 |
| AT-6 | output_inside_input (스크립트 가드) | `-InputPath "$AT\in_batch" -OutputFolder "$AT\in_batch\out"` | exit 10, "출력 폴더가 입력 폴더 내부" | D-8 |
| AT-6b | output_inside_input (CLI 교차 확인, **필수**) | AT-9에서 보존된 작업 폴더의 exe를 직접 실행: output_folder를 `$AT\in_batch\out`로 넣은 `bad-settings.json`을 수동 작성 후 `dxf_converter.exe --mode convert --settings bad-settings.json --progress json` | CLI exit 2, JSON error 이벤트에 `output_inside_input` — 스크립트 가드와 CLI preflight 판정 일치 확인 | D-8 |
| AT-7 | 상대경로 + drive-relative | `-InputPath ".\in_single\$F1" ...` 및 `-InputPath "C:foo.dxf" -OutputFolder "$AT\out7"` 각 1회 | 둘 다 exit 10, "절대경로가 아닙니다" (drive-relative가 IsPathRooted 오탐으로 통과하지 않음을 실증) | D-8 |
| AT-8 | skip/overwrite 멱등성 | AT-1 완료된 out1 대상 동일 명령 재실행 → 이어 `-Overwrite` 재실행 | **판정 기준**: 1차 재실행 = manifest 해당 파일 status `skipped_*` + PDF mtime 불변 + 작업 폴더 삭제됨(skip-only cleanup); 2차 `-Overwrite` = status `success` + mtime 갱신 + exit 0. exit code 실측값은 기록만 하고(1이면 요약의 "스킵 완료" 문구 확인) 판정 기준으로 쓰지 않음 | D-9, D-10 |
| AT-9 | 생성 settings 무결성 | AT-2 입력에 `-KeepWorkFolder` 추가 실행 | 보존된 `run-settings.json`: input_sources가 JSON 배열, (overwrite,skip_if_exists)==(false,true), max_parallelism==1, model_space_only==true, fit_to_page==true, resolved_inputs==[] | D-2 보강, AT-6b 사전 조건 |
| AT-10 | 인코딩 무결성 | AT-9 보존 폴더의 `progress.jsonl`을 UTF-8 read-back | U+FFFD·`占쏙옙` 0건, 전 라인 JSON 파싱 성공, type=="result" 정확히 1개 | D-12 |
| AT-11 | 파일+폴더 혼합 입력 | `-InputPath "$AT\in_single\$F1","$AT\in_batch\sub" -OutputFolder "$AT\out11"` | exit 0, `.pdf` 2개(001+002), manifest succeeded==2 | D-6 보강 |
| AT-12 | 공백+한글 경로 | `-InputPath "$AT\한글 도면 폴더" -OutputFolder "$AT\한글 출력\out12"` | exit 0, `.pdf` 1개, manifest·요약 출력의 한글 경로 무결(read-back) | D-6·D-12 보강 |
| AT-13 | 손상 DXF (변환 단계 실패 → 보존 검증) | `-InputPath "$AT\in_broken" -OutputFolder "$AT\out13"` | exit ≠ 0 (1 또는 4 — 실측 기록), file_result/manifest에 `failure` 기록, **작업 폴더 보존 + 경로 보고** (사전검증이 아닌 CLI 내부 실패이므로 작업 폴더가 생성된 후 실패함) | D-9(보존측) |
| AT-14 | 번들 원본 무변경 (R-1 대체 검증) | 실행 AT 전체 종료 후 `$snapAfter` 채취, `Compare-Object $snapBefore $snapAfter -Property FullName,Length,LastWriteTimeUtc` | 차이 0건 — 실행이 번들 원본을 읽기만 함을 실증 | D-15 |

### 정적 AT (실행 없이 판정)

| ID | 검증 | 판정 명령 | 대응 DoD |
|----|------|-----------|----------|
| AT-15 | 파일 인벤토리 | cli 재귀 파일 수 ==24, `Test-Path ...\cli\logs` ==False, exe Length ==90624, 핵심 7파일(exe, exe.config, ACadSharp.dll, Core.dll, Contracts.dll, settings.schema.json, progress-event.schema.json) Test-Path 전수, `.gitattributes` 존재+내용 일치 | D-2, D-3 |
| AT-16 | SKILL.md·스크립트 내용 계약 | SKILL.md에 `name: dxf-to-pdf` frontmatter + "preview 미지원" 문구 Select-String ≥1건; `Select-String scripts\convert-dxf.ps1 -Pattern 'preview'` ==0건 | D-1, D-14 |
| AT-17 | 스크립트 BOM | convert-dxf.ps1 앞 3바이트 == EF BB BF | D-4 |
| AT-18 | 스킬 검증기 | quick_validate.py exit 0 (validate_plugin.py 권장 2차) | D-1, D-5 |
| AT-19 | README 반영 | README.md에 `dxf-to-pdf` 행+트리 Select-String | D-11 |
| AT-20 | 커밋 검증 (dh-dev Step 4에서 수행) | `git log --stat -1`에 references/cli/*.dll 포함 | D-13 |

각 AT 실행 후 결과(exit code, 산출 파일 목록, 특이사항)를 기록하고, AT-8·AT-13의 실측 exit code는 SKILL.md Output Contract 해석 규칙 문구에 반영한다.

## 7. Risks and Mitigations

| # | 리스크 | 완화 |
|---|--------|------|
| R-1 | 스킬 설치 위치(플러그인 캐시)가 읽기 전용 → CLI가 logs/·프로브 쓰기 실패 | 매 실행 `%TEMP%\dxf2pdf_<8hex>`로 번들 전체 복사 후 사본 실행. 번들 원본은 읽기 전용 접근만 — AT-14가 "원본 무쓰기"를 실측 검증 (읽기 전용 ACL 재현 테스트는 개발 머신 상태 오염 위험 대비 검증 가치가 낮아 대체) |
| R-2 | 작업 폴더 %TEMP% 누적 / 실패 시 로그 유실 | 성공·skip-only(부분완료, failed==0·cancelled==0)=삭제, 변환 실패=보존+경로 보고, `-KeepWorkFolder`=명시 보존 (Step 2-(8), D-9). 반복 멱등 재실행에서도 누적 없음 |
| R-3 | .NET Framework 4.8 또는 x64 미지원 환경에서 exe 기동 실패 | SKILL.md Error Handling에 전제조건·증상(0x80131700 등)·안내 명시. 스킬이 설치를 시도하지 않음 |
| R-4 | PS 5.1이 BOM 없는 .ps1의 한글 리터럴을 cp949로 오해석 | convert-dxf.ps1을 UTF-8 BOM으로 저장 (AT-17 바이트 검증) |
| R-5 | PowerShell 리다이렉트/콘솔 cp949로 stdout 한글 깨짐 | `StandardOutputEncoding=UTF8` 직접 디코딩 + WriteAllText(UTF8 no BOM) 보존 (AT-10·AT-12 검증) |
| R-6 | ConvertTo-Json 단일 원소 배열 언랩으로 스키마 위반 JSON 생성 | 중첩 프로퍼티 직렬화 패턴 고정 + AT-9 실측 검증 |
| R-7 | stdout/stderr 동기 읽기 데드락 | stderr `ReadToEndAsync()` 비동기 패턴 고정 (Step 2-(5)) |
| R-8 | skip 발생 시 exit 1(PartialFailure)을 실패로 오보고 / 오판정 | 보고: result 이벤트 failed/skipped 카운트로 구분 문구 출력. 정리: skip-only는 clean run으로 삭제. 판정: D-10은 manifest status+mtime만 사용 (AT-8) |
| R-9 | 사용자 입력/출력 경로의 MAX_PATH 초과 (깊은 경로+긴 도면 파일명) | **스크립트가 통제할 수 없는 영역** — 입력·출력은 사용자 지정 절대경로에 그대로 남고 작업 폴더에는 짧은 이름의 번들 파일만 복사되므로 작업 폴더명 단축은 이 문제의 완화책이 아님. 완화는 SKILL.md Error Handling의 안내 문구(진단 노출 시 경로 단축 권고)로 한정 |
| R-10 | 바이너리 커밋(~4.1MB)으로 리포지 증가 | 사용자 명시 승인 완료(재논의 불가). 1회성. `.gitattributes -text`로 바이트 보존 + release-manifest.json SHA-256으로 무결성 추적 |
| R-11 | 번들 README.txt의 `--progress plain` 표기가 구현자를 오도 | Code Writing Guide에 불일치 명시 — 스킬은 `json`만 사용, 번들 무수정 원칙 |
| R-12 | AV/조직 정책이 %TEMP% exe 실행 차단 | Error Handling에 증상·대응(예외 등록 요청) 안내. 우회 시도 금지 |
| R-13 | **스코프 명시 제외**: `file_timeout_seconds`(900)/`batch_deadline_seconds`(21600) 초과 동작, 동일 output_folder 동시 실행 경쟁 | 이번 스킬 범위에서 의도적으로 제외 (기본값 그대로 전달, 재현에 15분+ 소요·동시성 하네스 필요 대비 스킬 사용 시나리오에서 발생 빈도 낮음). CLI 자체의 원자적 커밋(임시파일→move)이 반쪽 파일을 방지하는 1차 방어선임을 SKILL.md에 언급 |
| R-14 | **스코프 명시 제외**: 출력 폴더가 존재하나 ACL로 쓰기 거부되는 경우 | 스크립트는 검사하지 않고 CLI 자체 쓰기 프로브가 ConfigurationError(exit 2)로 노출 — SKILL.md Error Handling에 권한 확인 안내 행 추가. AT는 ACL 조작의 개발 머신 오염 위험 대비 가치가 낮아 추가하지 않음 |

## 8. Verification Steps

구현 완료 후 아래 순서로 실행 (전부 실측 — 자가 선언 금지):

1. **정적 AT 일괄 수행**: AT-15(인벤토리) → AT-17(BOM) → AT-16(SKILL.md/스크립트 내용 계약) → AT-18(quick_validate + validate_plugin) → AT-19(README) (D-1~D-5, D-11, D-14).
2. **AT 환경 구축**: §6 준비 블록 실행 + AT-14용 번들 스냅샷 채취.
3. **실행 AT 순차 수행**: AT-1 → AT-2 → AT-3 → AT-4 → AT-5 → AT-6 → AT-7 → AT-9 → AT-6b(AT-9의 보존 폴더 재사용) → AT-8 → AT-10 → AT-11 → AT-12 → AT-13 → AT-14(스냅샷 비교) — 각각 exit code·산출물 실측 기록 (D-6~D-10, D-12, D-15). AT-2는 manifest를 열어 `summary.succeeded==2` JSON 값까지 확인.
4. **작업 폴더 위생**: AT 종료 후 `Get-ChildItem $env:TEMP -Filter dxf2pdf_*` — 남은 항목이 AT-13(실패 보존)과 AT-9(KeepWorkFolder)의 2건뿐인지 확인 후 수동 정리 (D-9). skip-only 런(AT-8 1차)의 폴더는 삭제 규칙에 따라 남아 있지 않아야 함.
5. **scratchpad 정리**: `dxf-at\` 전체(복사 DXF, out1~out13 PDF/manifest, bad-settings)를 삭제하거나 보존 사유를 검증 보고에 명시 — 세션 산출물이 무단 잔존하지 않게 한다.
6. **한글 read-back**: SKILL.md·README.md·AT-10의 progress.jsonl·AT-12의 한글 경로 산출물·스크립트 요약 출력 샘플을 UTF-8로 다시 읽어 출력 — 모지바케 시그니처(U+FFFD, `占쏙옙`, `ï»¿`, 한글 자리 `?`) 0건 육안 확인 (D-12). 검증 보고에 "무엇을 읽어서 어떻게 확인했는지" 명기 (전역 CLAUDE.md 정책).
7. **커밋**(dh-dev Step 4): `git status`로 스테이징 대상 검토 — 현재 워킹트리에 기존 미커밋 수정(`.mcp.json`, `hooks/hooks.json` 등)이 있으므로 `skills/dxf-to-pdf/**`와 README.md의 dxf-to-pdf 행/트리 변경만 선별 add. 커밋 후 AT-20(`git log --stat`) 실측 (D-13).

**계획 외 참고 (구현자 주의)**: sampleDxf 폴더에는 `.PDF`/`.pdf`/`plot.log` 등 비-DXF 파일이 섞여 있으나 CLI가 `*.dxf`만 enumerate하므로 AT 준비 시 복사본 폴더만 사용하면 됨.

---

## 부록: 1-e 재작성 반영 내역 (19건 disposition)

| ID | disposition |
|----|-------------|
| H1 | **반영** — §6에 정적 AT(AT-15~AT-20) 신설, §5 DoD 판정 컬럼을 전부 AT-# 참조로 교체. D-1·D-3·D-4·D-5·D-11·D-13 → AT-16·15·17·18·19·20 매핑 완결 |
| H2 | **반영** — D-9 실패측을 손상 DXF 시나리오(AT-13, 작업 폴더 생성 후 CLI 내부 실패 → 보존 검증)로 교체. AT-4는 "TEMP 폴더 수 증가 0(미생성)" 판정으로 정정 |
| H3 | **반영** — Step 2-(8) cleanup을 `exit 0 OR (exit 1 AND failed==0 AND cancelled==0)`이면 삭제로 확장. AT-8에 skip-only 삭제 확인 추가, R-2·AC-8·Verification 4 갱신 |
| H4 | **반영** — §6 준비 블록에 `in_flat` 생성 + 001·002 Copy-Item 명시. AT-2가 in_flat 대상으로 완결 재현 가능 |
| H5 | **반영** — AC-13·D-14 신설(SKILL.md preview 미지원 문구 존재 + 스크립트 `preview` 문자열 0건), 판정용 정확한 문구를 Step 3-1에 고정, AT-16으로 검증 |
| M1 | **반영** — R-9 재작성: 작업 폴더명 단축은 이 문제의 완화책이 아님을 명시, 완화를 Error Handling 안내 문구로 한정 (경로 공간 혼동 정정) |
| M2 | **반영** — Step 2-(2)에 `Assert-AbsolutePath`(슬래시 정규화 후 `^[A-Za-z]:\\|^\\\\` 정규식) 도입, IsPathRooted 단독 사용 금지와 사유(drive-relative 오탐, IsPathFullyQualified 부재)를 코드 주석+Code Writing Guide에 명시. AT-7에 `C:foo.dxf` 케이스 추가 |
| M3 | **반영** — Step 1에 `skills/dxf-to-pdf/.gitattributes`(`references/cli/** -text`) 신설. 바이너리+텍스트 번들 전체를 정규화로부터 보호(SHA-256 대조 성립 근거 포함). D-2·AT-15·R-10에 반영 |
| M4 | **반영** — 문서 서두에 "사용자 확인 필요 — 계획 작성자 임의 결정 3건" 박스 신설(기본값 무질문/자연어 추론/파라미터 노출), dh-dev Step 2 리뷰 대상으로 명시 |
| M5 | **반영** — AT-11(파일+폴더 혼합 단일 호출, 겹침 없는 조합) 추가, D-6 보강 매핑 |
| M6 | **반영** — R-13 신설: 타임아웃 초과·동시 실행은 의도적 스코프 제외로 명문화(사유 포함), §1 스코프 제외 목록에도 등재 |
| M7 | **반영** — 준비 블록에 `한글 도면 폴더`(공백+한글) 생성, AT-12로 입력·출력 모두 한글+공백 경로 실행 검증, D-12 매핑 |
| M8 | **부분 반영(스코프 제외 명시)** — AT는 추가하지 않음: ACL 조작은 개발 머신 상태 오염 위험이 있고 CLI 자체 쓰기 프로브가 이미 ConfigurationError로 노출함(README.txt 실측 근거). 대신 R-14 신설 + SKILL.md Error Handling에 권한 거부 행 추가 |
| M9 | **반영** — D-10 판정 기준을 "manifest status `skipped_*` + PDF mtime 불변 / `-Overwrite` 시 success + mtime 갱신"만으로 한정, exit code는 참고 기록으로 격하 (AT-8 동일 적용) |
| L1 | **반영** — Step 2-(6)에 `$badLines` 카운터 추가, 1건 이상이면 요약에 경고 문구 출력 |
| L2 | **반영** — settings.schema.json 재확인 결과 두 boolean에 상호 제약 없음(금지는 동시 true뿐, 소스 스펙 기준). `(false,false)`는 의미 미정의로 의도적 미노출 — §1과 Step 2-(4) 주석에 사유 명시 |
| L3 | **대체 검증으로 반영** — 읽기 전용 ACL 재현 대신 AT-14(번들 원본 전후 스냅샷 비교, 쓰기 0건 실증) 신설. TEMP 복사 전략은 원본을 읽기만 하므로 "원본 무쓰기"가 R-1의 검증 가능한 등가 명제임을 R-1에 명시. D-15 신설 |
| L4 | **반영** — Verification Step 5 신설: scratchpad `dxf-at\` 정리 또는 보존 사유 보고 의무화 |
| L5 | **반영** — AT-6b "(선택)" 제거, 필수화. AT-9의 보존 작업 폴더를 재사용해 CLI 직접 실행으로 `output_inside_input` exit 2 교차 확인, D-8 판정에 "가드-CLI 판정 일치" 포함 |
