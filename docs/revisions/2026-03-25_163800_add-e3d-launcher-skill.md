# E3D Launcher 스킬 추가

- **Date**: 2026-03-25 16:38:00
- **Author**: Claude (dh-dev → skill-creator)

## Rationale / Plan

사용자 요청으로 E3D 모듈(Design, Drawing, Paragon, Admin)을 외부 프로세스로 실행하는 스킬을 신규 생성.
기존 `e3d-standalone` 스킬(DLL 기반 Standalone API)과 구분되는 프로세스 기동 방식(`mon.exe` + 인자 조립).
참조 코드: `D:\001_Work\2026\029_E3D_Login\E3D_Proj_Login\E3DLogin\Services\E3DLauncher.cs`

## Changed Files

| File | Status | Description |
|------|--------|-------------|
| `skills/e3d-launcher/SKILL.md` | Added | E3D Launcher 스킬 정의 (모듈별 launch 패턴, 경로 규칙, config 구조) |
| `skills/e3d-launcher/references/config-sample.json` | Added | 프로젝트 인증 정보 및 설치 경로 config 샘플 |
| `skills/e3d-launcher/references/e3d-launcher-sample.py` | Added | Python subprocess 기반 E3D 모듈 런처 샘플 |
| `skills/e3d-launcher/references/e3d-launcher-sample.cs` | Added | C# Process.Start 기반 E3D 모듈 런처 샘플 |

## Details

### `skills/e3d-launcher/SKILL.md` (Added)

- 150줄, 500줄 제한 이내
- 모듈별 Launch 패턴 정의: Design/Drawing (E3D + launch.init), Paragon (CATALOGUE + catalogue.init), Admin (ADMIN + admin.init)
- 인자 구조 테이블: `PROD {PRODUCT} init "{INIT_FILE}" {MODE} {PROJ} {USER}/{PASS} /{MDB} {COMMAND}`
- 시작 모드: TTY / CONSOLE / NOCONSOLE
- 경로 해석 규칙: v2.x → v3.x 자동 대체
- Config JSON 구조 및 인증 타입 분리 (user vs system)

### `skills/e3d-launcher/references/config-sample.json` (Added)

- settings: aveva_design_installed_dir, aveva_admin_installed_dir, target_dir, working_dir
- projects: 프로젝트별 USERNAME/PASSWORD/MDB + system 계정 정보

### `skills/e3d-launcher/references/e3d-launcher-sample.py` (Added)

- MODULE_SPECS 딕셔너리로 모듈별 product/init_file/install_key/cred_type/command 정의
- `resolve_versioned_path()`: v2.x → v3.x 대체 로직
- `build_arguments()`: mon.exe 인자 문자열 조립
- `launch_module()`: subprocess.Popen으로 프로세스 기동
- CLI: argparse 기반 (--module, --project, --mode, --config, --command)

### `skills/e3d-launcher/references/e3d-launcher-sample.cs` (Added)

- E3DModule enum: Design, Drawing, Paragon, Admin
- StartMode enum: TTY, CONSOLE, NOCONSOLE
- `E3DModuleLauncher.Launch()`: 모듈별 switch → 전용 메서드 호출
- `LaunchE3D()`, `LaunchCatalogue()`, `LaunchAdmin()`: 각 모듈별 인자 조립 + Process.Start
- `ResolvePath()`: v2.x → v3.x 대체 로직
- Usage 예제 주석 포함
