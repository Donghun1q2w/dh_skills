[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string[]]$InputPath,
    [Parameter(Mandatory = $true)][string]$OutputFolder,
    [switch]$Recursive,
    [ValidateSet('A4', 'A3', 'A2', 'A1', 'A0')][string]$PaperSize = 'A4',
    [ValidateSet('landscape', 'portrait')][string]$Orientation = 'landscape',
    [ValidateRange(72, 1200)][int]$Dpi = 300,
    [ValidateSet('monochrome', 'color')][string]$ColorMode = 'monochrome',
    [switch]$Overwrite,
    [switch]$KeepWorkFolder
)

$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

function Fail([string]$msg) {
    [Console]::Error.WriteLine("[dxf-to-pdf] $msg")
    exit 10
}

# (1) 번들 위치 해석 — 스킬 설치 위치와 무관하게 $PSScriptRoot 기준으로 찾는다.
$bundleSource = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\references\cli'))
if (-not (Test-Path (Join-Path $bundleSource 'dxf_converter.exe'))) {
    Fail "번들 CLI 없음: $bundleSource"
}

# (2) 사전 검증 — 여기서 실패하면 작업 폴더는 아직 생성되지 않는다.
function Assert-AbsolutePath([string]$p, [string]$label) {
    # IsPathRooted 단독 사용 금지: .NET Framework는 drive-relative("C:foo")에도 true를 반환한다.
    # PS 5.1의 .NET 4.x에는 Path.IsPathFullyQualified가 없어 정규식으로 판정한다.
    $normalized = $p -replace '/', '\'
    if (-not ($normalized -match '^[A-Za-z]:\\' -or $normalized -match '^\\\\')) {
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
$outputFolderFull = [System.IO.Path]::GetFullPath($OutputFolder)

$outFull = $outputFolderFull.TrimEnd('\') + '\'
foreach ($p in $InputPath) {
    if (Test-Path $p -PathType Container) {
        $inFull = [System.IO.Path]::GetFullPath($p).TrimEnd('\') + '\'
        if ($outFull.StartsWith($inFull, [System.StringComparison]::OrdinalIgnoreCase)) {
            Fail "출력 폴더가 입력 폴더 내부에 있습니다 (output_inside_input): $OutputFolder"
        }
    }
}
New-Item -ItemType Directory -Force -Path $OutputFolder | Out-Null

# (3) 작업 폴더 생성 + 번들 전체 복사 (exe 옆 sibling DLL과 exe.config가 함께 있어야 기동된다)
$work = Join-Path $env:TEMP ('dxf2pdf_' + [guid]::NewGuid().ToString('N').Substring(0, 8))
Copy-Item -Path $bundleSource -Destination $work -Recurse

# (4) run-settings.json 생성
$sources = @()
$i = 0
foreach ($p in $InputPath) {
    $i++
    $isFolder = Test-Path $p -PathType Container
    $sources += [ordered]@{
        source_id     = "s$i"
        kind          = $(if ($isFolder) { 'folder' } else { 'file' })
        path          = [System.IO.Path]::GetFullPath($p)
        recursive     = [bool]($isFolder -and $Recursive)
        output_prefix = ''
    }
}
$settings = [ordered]@{
    schema_version = 1
    input_sources  = $sources
    # CLI가 직접 확장하도록 빈 배열로 둔다 — 여기서 미리 채우면 입력 해시가 어긋날 수 있다.
    resolved_inputs = @()
    output_folder  = $outputFolderFull
    paper          = [ordered]@{ size = $PaperSize; orientation = $Orientation; margin_mm = 5.0; fit_to_page = $true }
    render         = [ordered]@{ dpi = $Dpi; color_mode = $ColorMode; model_space_only = $true; fail_on_unsupported = $true; font_paths = @() }
    behavior       = [ordered]@{
        overwrite              = [bool]$Overwrite
        # 동시 true는 preflight 위반이므로 두 값을 항상 반대로 묶는다.
        skip_if_exists         = (-not [bool]$Overwrite)
        continue_on_error      = $true
        max_parallelism        = 1
        file_timeout_seconds   = 900
        batch_deadline_seconds = 21600
        cancel_grace_seconds   = 15
    }
}
$settingsPath = Join-Path $work 'run-settings.json'
# 중첩 프로퍼티로 직렬화해야 원소 1개짜리 input_sources가 배열로 유지된다(ConvertTo-Json 언랩 회피).
[System.IO.File]::WriteAllText($settingsPath, ($settings | ConvertTo-Json -Depth 6), (New-Object System.Text.UTF8Encoding($false)))

# (5) 실행 — 콘솔 코드페이지와 무관하게 stdout/stderr를 UTF-8로 직접 디코딩한다.
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = (Join-Path $work 'dxf_converter.exe')
$psi.Arguments = '--mode convert --settings "' + $settingsPath + '" --progress json'
$psi.WorkingDirectory = $work
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.StandardOutputEncoding = [System.Text.Encoding]::UTF8
$psi.StandardErrorEncoding = [System.Text.Encoding]::UTF8
$proc = [System.Diagnostics.Process]::Start($psi)
$stderrTask = $proc.StandardError.ReadToEndAsync()   # 두 스트림을 동기로 읽으면 파이프 버퍼가 차서 데드락이 난다.
$stdout = $proc.StandardOutput.ReadToEnd()
$proc.WaitForExit()
$exitCode = $proc.ExitCode
$stderr = $stderrTask.Result
[System.IO.File]::WriteAllText((Join-Path $work 'progress.jsonl'), $stdout, (New-Object System.Text.UTF8Encoding($false)))
$stdoutLines = $stdout -split "`r?`n"

# (6) JSON Lines 파싱
$fileResults = @()
$finalResult = $null
$errors = @()
$badLines = 0
foreach ($line in $stdoutLines) {
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    $evt = $null
    try { $evt = $line | ConvertFrom-Json } catch { $badLines++; continue }
    if ($evt.type -eq 'file_result') { $fileResults += $evt }
    elseif ($evt.type -eq 'result') { $finalResult = $evt }
    elseif ($evt.type -eq 'error') { $errors += $evt }
}

# (7) 요약 출력
$exitMeaning = 'Unknown'
switch ($exitCode) {
    0 { $exitMeaning = 'Success' }
    1 { $exitMeaning = 'PartialFailure' }
    2 { $exitMeaning = 'ConfigurationError' }
    3 { $exitMeaning = 'Cancelled' }
    4 { $exitMeaning = 'InternalError' }
}
Write-Output "[dxf-to-pdf] 종료 코드: $exitCode ($exitMeaning)"

if ($null -ne $finalResult) {
    Write-Output ("[dxf-to-pdf] 성공 {0} / 실패 {1} / 스킵 {2} / 취소 {3} (elapsed {4}ms)" -f `
            $finalResult.succeeded, $finalResult.failed, $finalResult.skipped, $finalResult.cancelled, $finalResult.elapsed_ms)
    Write-Output "[dxf-to-pdf] Manifest: $($finalResult.manifest_file)"
    if ($exitCode -eq 1 -and $finalResult.failed -eq 0 -and $finalResult.skipped -gt 0) {
        Write-Output "[dxf-to-pdf] 실패 없음 — 기존 PDF 스킵으로 인한 부분완료"
    }
}
else {
    Write-Output "[dxf-to-pdf] result 이벤트가 없습니다 — 비정상 조기 종료"
    Write-Output "[dxf-to-pdf] stderr:"
    Write-Output $stderr
    Write-Output "[dxf-to-pdf] stdout(앞 20줄):"
    foreach ($line in ($stdoutLines | Select-Object -First 20)) { Write-Output $line }
}

foreach ($e in $errors) {
    Write-Output "[dxf-to-pdf] 오류 이벤트: $($e.code): $($e.message)"
}
foreach ($fr in $fileResults) {
    if ($fr.status -ne 'success' -and $fr.status -notlike 'skipped*') {
        Write-Output "  실패: $($fr.input_file) — $($fr.status): $($fr.message)"
    }
}
if ($badLines -gt 0) {
    Write-Output "[dxf-to-pdf] 경고: JSON 파싱 실패 라인 $badLines개 — progress.jsonl 확인 필요"
}

# (8) 정리 — 스킵만 발생한 부분완료(exit 1)도 정상 종결로 보고 지워야 %TEMP%에 누적되지 않는다.
$skipOnly = ($null -ne $finalResult) -and ($finalResult.failed -eq 0) -and ($finalResult.cancelled -eq 0)
$isCleanRun = ($exitCode -eq 0) -or (($exitCode -eq 1) -and $skipOnly)
if ($isCleanRun -and -not $KeepWorkFolder) {
    Remove-Item -Path $work -Recurse -Force
}
else {
    Write-Output "[dxf-to-pdf] 작업 폴더 보존(로그 포함): $work"
}
exit $exitCode
