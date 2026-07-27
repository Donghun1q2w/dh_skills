DXF PDF Converter (CLI) v0.1.0
========================================

엔지니어링 DXF 도면을 A계열 단일 페이지 PDF로 일괄 변환하는 커맨드라인 프로그램입니다.
WPF UI 없이 backend 변환기(dxf_converter.exe)만 포함합니다.

실행 환경
---------
- Windows 10/11 64비트
- .NET Framework 4.8
- 쓰기 가능한 폴더에 전체 폴더를 복사하여 사용

빠른 시작
---------
1. settings.json을 편집합니다(아래 "설정" 참조). 최소한 다음을 지정:
   - input_sources: 변환할 DXF 파일 또는 폴더 경로 목록
   - output_folder: PDF를 생성할 폴더
2. 변환 실행:
     dxf_converter.exe --mode convert --settings settings.json --progress json
3. 미리보기(단일 파일 PNG) 실행 예:
     dxf_converter.exe --mode preview --settings settings.json --progress json ^
       --preview-file-id <id> --preview-width 1600 --preview-height 1200

명령행 옵션
-----------
  --mode <convert|preview>   변환 또는 미리보기 모드 (필수)
  --settings <path>          설정 JSON 경로 (필수)
  --progress <json|plain>    진행 이벤트 출력 형식 (json 권장)
  --cancel-file <path>       이 파일이 생기면 협조적 취소
  --preview-file-id <id>     preview 모드 대상 파일 id
  --preview-width <px>       preview 픽셀 너비
  --preview-height <px>      preview 픽셀 높이
  --version                  버전 출력
  --help, -h                 도움말 출력

출력 계약
---------
- --progress json의 stdout은 UTF-8 no-BOM JSON Lines 전용입니다.
  마지막 정상 이벤트는 정확히 하나의 "result"이며, 파일별 결과와
  incremental manifest는 별도로 보존됩니다.
- 입력 DXF와 같은 상대경로/stem의 .pdf가 output_folder에 생성됩니다.
- 실행별 dxf_conversion_manifest_*.json과 logs\dxf_converter_*.log가 남습니다.
- 종료 코드 0 = 성공. 0이 아니면 진단(JSON) 또는 stderr를 확인하십시오.

설정 (settings.json)
--------------------
  input_sources   : 입력 DXF 파일/폴더 경로 목록
  output_folder   : PDF 출력 폴더
  paper           : size(A4 등)/orientation(landscape)/margin_mm/fit_to_page
  render.dpi      : 출력 DPI (기본 300)
  render.color_mode : "monochrome"(흑백, DeviceGray) 또는 "color"(컬러, DeviceRGB)
  render.model_space_only : Model space만 변환
  render.fail_on_unsupported : 미지원 엔티티에서 실패 처리 여부
  render.font_paths : 추가 폰트 검색 경로 (settings.ini로도 지정 가능)
  behavior.overwrite / skip_if_exists / continue_on_error
  behavior.max_parallelism / file_timeout_seconds / batch_deadline_seconds

기본 변환 설정
--------------
- A4 landscape, 5mm margin, fit-to-page, 300 DPI, monochrome
- 텍스트 supersampling과 해칭/화살촉 정상화가 적용된 렌더링 품질
- monochrome은 DeviceGray(1채널)로 저장되어 파일 크기가 작습니다

포함 파일
---------
- dxf_converter.exe / dxf_converter.exe.config : 변환 backend CLI
- *.dll : 런타임 의존성 (ACadSharp, Core/Contracts, System.* 등)
- settings.json : 기본 설정 템플릿
- settings.ini  : 추가 폰트 검색 경로
- contracts\    : settings/progress/manifest JSON schema
- THIRD-PARTY-NOTICES.txt : 서드파티 라이선스 고지
- release-manifest.json : 파일별 SHA-256 무결성 manifest

입력 DXF는 수정하지 않습니다. 출력은 같은 디렉터리의 임시 파일에 완성한 뒤
원자적으로 commit하며, 누락 폰트/미지원 엔티티/worker crash/timeout/취소는
구조화된 진단으로 노출됩니다.