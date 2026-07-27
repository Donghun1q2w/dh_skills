# dxf-to-pdf 스킬 신규 추가 (번들 CLI 직접 실행형)

- **Date**: 2026-07-27 14:49:40
- **Author**: Claude (dh-dev 워크플로우)

## Rationale / Plan

계획 문서: [2026-07-27_140608_add-dxf-to-pdf-skill.md](../plans/2026-07-27_140608_add-dxf-to-pdf-skill.md)

사용자 요청: `D:\002_C_Sharp\dxf_to_pdf\dxf_converter\release-cli`의 dxf_converter CLI를 활용해 DXF→PDF 변환용 신규 스킬 `dxf-to-pdf`를 생성. dh-dev 워크플로우(탐색→인터뷰→재진술→계획 작성→적대적 검증 1회 재작성→사용자 승인→실행→검증)를 전 과정 수행. 1-e 검증에서 HIGH 5건을 포함한 19건을 1회 재작성으로 전부 반영했고, 실행 에이전트가 Definition of Done 15개 항목을 실제 exe 실행 기반 적대적 테스트(AT-1~AT-20) 20종으로 실측 검증했다. 이후 `/simplify` 4개 병렬 레인(Reuse/Simplification/Efficiency/Altitude) 리뷰를 거쳐 안전한 개선 4건을 추가 반영했다.

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills/dxf-to-pdf/SKILL.md` | Added | 스킬 메인 문서 — 번들 위치, 실행법, settings.json 스키마, preflight 규칙, 출력 계약, 에러 처리, DLL 의존성 |
| `skills/dxf-to-pdf/.gitattributes` | Added | `references/cli/** -text` — 번들 바이너리·텍스트 파일의 CRLF 정규화 방지 |
| `skills/dxf-to-pdf/scripts/convert-dxf.ps1` | Added | 작업폴더 복사 → settings 생성 → CLI 실행 → JSON Lines 파싱 → 정리를 수행하는 PowerShell 자동화 스크립트 (UTF-8 BOM) |
| `skills/dxf-to-pdf/references/cli/` | Added | `D:\002_C_Sharp\dxf_to_pdf\dxf_converter\release-cli`의 dxf_converter CLI 번들 사본 24개 파일(exe+DLL 14개+contracts 3종+템플릿/문서, `logs/` 제외) |
| `README.md` | Modified | 스킬 목록 표에 dxf-to-pdf 행 추가, 디렉토리 구조 트리에 dxf-to-pdf 블록 추가 |
| `docs/plans/2026-07-27_140608_add-dxf-to-pdf-skill.md` | Added | 계획 문서 (1-e 재작성 반영 내역 포함) |
| `docs/plan_history.md` | Modified | dxf-to-pdf 계획 항목 등록 |

## Details

### `skills/dxf-to-pdf/SKILL.md` (Added)

- frontmatter `name: dxf-to-pdf` + 영문 description(트리거 문구 포함)
- 12개 섹션: 개요/Invocation hint/preview 미지원 명시 → Bundled CLI Location → 필수 정보 프롬프팅 워크플로우 → Running the Bundled CLI(표준 실행 커맨드) → CLI 인자 구조 → Configuration(run-settings.json 스키마+Preflight 불변 규칙) → Output Contract & Reporting(종료코드/이벤트/manifest/해석 규칙) → Encoding Rules → Dependent DLLs → Error Handling → When to Use → References
- 실행 에이전트가 계획의 `powershell -File` 예시 커맨드를 실측한 결과 `-File` 모드가 `[string[]]` 배열 인자를 하나만 바인딩하고 나머지를 조용히 버리는 PowerShell 동작을 발견 — `powershell -Command "& '...' -InputPath 'a','b' ..."` 형식으로 교체하고 `-File` 사용 금지 경고 블록 추가 (계획 대비 유일한 편차, 문서 범위 한정)

### `skills/dxf-to-pdf/scripts/convert-dxf.ps1` (Added)

- 계획의 pseudocode를 그대로 구현: `$PSScriptRoot` 기준 번들 위치 해석 → 절대경로/존재/확장자/output_inside_input 사전 검증(위반 시 exit 10, 작업폴더 미생성) → `%TEMP%\dxf2pdf_<8hex>`로 번들 복사 → `run-settings.json` 생성(input_sources 배열, resolved_inputs 빈 배열, paper/render/behavior 고정값) → `ProcessStartInfo` 기반 UTF-8 강제 디코딩 실행(stderr 비동기 읽기로 데드락 회피) → JSON Lines 파싱(파싱 실패 라인 카운트) → 사람이 읽는 요약 출력 → skip-only(exit 1, failed==0, cancelled==0)도 clean run으로 간주하는 정리 로직
- `/simplify` 4개 레인 리뷰 후 안전한 개선 4건 적용: (1) `Assert-AbsolutePath`의 `$n`→`$normalized` 변수명 명확화, (2) `$OutputFolder`의 `GetFullPath` 중복 계산 제거(`$outputFolderFull` 1회 계산으로 `$outFull` prefix 비교와 `settings.output_folder` 양쪽에서 재사용), (3) `$stdout -split "` `r?`n"` 중복 계산 제거(`$stdoutLines` 1회 계산으로 JSON 파싱 루프와 비정상 종료 시 stdout 앞 20줄 출력 양쪽에서 재사용), (4) 비정상 종료 출력 루프의 변수명 `$l`→`$line`으로 통일
- 스킵한 개선 1건: `$InputPath`에 대한 3개 foreach 루프(사전검증/output_inside_input/source 구성) 중 첫 두 개를 병합하는 안 — 리뷰 레인은 "안전, 트레이드오프 없음"이라 했으나 직접 분석한 결과 여러 입력이 동시에 서로 다른 문제(예: item1 overlap + item2 미존재)를 가질 때 어떤 에러가 먼저 노출되는지가 바뀌는 부작용이 있고, 실제 중복 계산(Test-Path/GetFullPath)은 loop2-loop3 사이에서 발생하므로 이 병합으로는 해소되지 않음 — 20종 실측 테스트를 통과한 현재 3-루프 구조를 보존하기 위해 적용하지 않음
- 개선 적용 후 BOM(EF BB BF) 유지 확인, PowerShell 파서로 구문 오류 0건 확인, 단일 파일 변환·output_inside_input 가드·KeepWorkFolder+settings 무결성 3개 시나리오를 재실행해 동작 동일함을 재검증

### `skills/dxf-to-pdf/references/cli/` (Added)

- `D:\002_C_Sharp\dxf_to_pdf\dxf_converter\release-cli`(v0.1.0)에서 robocopy `/E /XD logs`로 복사한 24개 파일 — 원본과 바이트 단위로 동일(`dxf_converter.exe` 90,624B 등 실측 확인)
- `logs/`는 실행 시 자동 생성되므로 제외

### `skills/dxf-to-pdf/.gitattributes` (Added)

- `references/cli/** -text` 1줄 — git의 자동 텍스트 판별·`core.autocrlf` 정규화로부터 번들 전체를 보호해 `release-manifest.json`의 SHA-256 무결성이 향후 clone 환경에서도 유지되도록 함

### `README.md` (Modified, dxf-to-pdf 관련 부분만)

- 스킬 목록 표에 `| [dxf-to-pdf](skills/dxf-to-pdf/) | DXF 도면을 A계열 단일 페이지 PDF로 일괄 변환 (번들 dxf_converter CLI 실행) | C# CLI |` 행 추가
- 디렉토리 구조 트리에 `dxf-to-pdf/`(SKILL.md, .gitattributes, scripts/convert-dxf.ps1, references/cli/) 블록 추가
- (참고: 이 파일에는 이번 작업과 무관한 기존 미커밋 변경이 이미 섞여 있었음 — 이번 리비전은 dxf-to-pdf 관련 hunk만 다룸)

## 검증 결과 요약

Definition of Done D-1~D-12, D-14, D-15 전부 pass (D-13 커밋은 이 리비전으로 충족). 실행 에이전트가 AT-1~AT-20(단일/배치/재귀/혼합입력/한글경로/preflight 위반 4종/멱등성/인코딩 무결성/번들 원본 무변경 등)을 실제 exe 실행으로 검증했고, 오케스트레이터가 SKILL.md·gitattributes·파일 카운트·exe 크기·BOM·README 반영을 직접 재확인했다. `/simplify` 적용 후에는 BOM·구문·3개 핵심 시나리오(단일 변환/output_inside_input 가드/settings 무결성)를 재실행해 회귀 없음을 확인했다.
