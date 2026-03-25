"""
E3D Module Launcher (Python)
mon.exe를 통해 E3D Design/Drawing/Paragon/Admin 모듈을 프로세스로 실행한다.

Usage:
    python e3d_launcher.py --module design --project TESTPROJ [--mode CONSOLE] [--config config.json]
    python e3d_launcher.py --module admin --project TESTPROJ --mode NOCONSOLE
    python e3d_launcher.py --interactive   # 대화형 모드: 필수 정보를 순차 질문
"""

import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Optional


# ── 기본 경로 ──────────────────────────────────────────────

DEFAULT_DESIGN_PATHS = [
    r"C:\cae_prog\AVEVA\v2.x\e3d",
    r"C:\Program Files (x86)\AVEVA\Everything3D2.10",
]

DEFAULT_ADMIN_PATHS = [
    r"C:\cae_prog\AVEVA\v2.x\Administration",
    r"C:\Program Files (x86)\AVEVA\Administration",
]


# ── 모듈 정의 ──────────────────────────────────────────────

MODULE_SPECS = {
    "design": {
        "product": "E3D",
        "init_file": "launch.init",
        "install_key": "aveva_design_installed_dir",
        "cred_type": "user",
        "command": "design",
    },
    "drawing": {
        "product": "E3D",
        "init_file": "launch.init",
        "install_key": "aveva_design_installed_dir",
        "cred_type": "user",
        "command": "drawing",
    },
    "paragon": {
        "product": "CATALOGUE",
        "init_file": "catalogue.init",
        "install_key": "aveva_design_installed_dir",
        "cred_type": "user",
        "command": "paragon",
    },
    "admin": {
        "product": "ADMIN",
        "init_file": "admin.init",
        "install_key": "aveva_admin_installed_dir",
        "cred_type": "system",
        "command": "admin",
    },
}


@dataclass
class ProjectCredential:
    USERNAME: str
    PASSWORD: str
    MDB: str
    systemUSERNAME: str = ""
    systemPASSWORD: str = ""
    systeMDB: str = ""


@dataclass
class LaunchSettings:
    aveva_design_installed_dir: str = ""
    aveva_admin_installed_dir: str = ""
    target_dir: str = ""
    working_dir: str = ""
    batch_file: str = ""


# ── 경로 해석 ──────────────────────────────────────────────

def resolve_install_path(custom_path: Optional[str], default_paths: list[str]) -> str:
    """사용자 지정 경로 → 기본 경로 목록 → v2.x→v3.x 대체 순으로 탐색."""
    if custom_path and os.path.exists(custom_path):
        return custom_path
    for path in default_paths:
        if os.path.exists(path):
            return path
        v3 = path.replace("v2.x", "v3.x")
        if v3 != path and os.path.exists(v3):
            return v3
    return ""


# ── Temp Init 파일 ─────────────────────────────────────────

def create_temp_init(init_path: str, batch_file: str) -> str:
    """원본 init 파일을 읽고 batch file 호출을 추가한 temp init 파일을 생성한다."""
    with open(init_path, encoding="utf-8") as f:
        content = f.read().rstrip()
    content += f'\ncall "{batch_file}"\n'
    temp_path = init_path.replace(".init", "_temp.init")
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(content)
    return temp_path


def cleanup_temp_init(temp_path: str) -> None:
    """temp init 파일을 삭제한다."""
    try:
        if os.path.isfile(temp_path) and temp_path.endswith("_temp.init"):
            os.remove(temp_path)
    except OSError:
        pass


# ── Config 로드 ────────────────────────────────────────────

def load_config(config_path: str) -> tuple[LaunchSettings, dict[str, ProjectCredential]]:
    """JSON config 파일에서 설정과 프로젝트 인증 정보를 로드한다."""
    with open(config_path, encoding="utf-8") as f:
        data = json.load(f)

    settings = LaunchSettings(**data["settings"])
    projects = {
        code.upper(): ProjectCredential(**cred)
        for code, cred in data["projects"].items()
    }
    return settings, projects


# ── 대화형 프롬프팅 ────────────────────────────────────────

def prompt_install_path(module: str) -> str:
    """설치 경로를 자동 탐색하고, 없으면 사용자에게 질문한다."""
    spec = MODULE_SPECS[module]
    defaults = DEFAULT_DESIGN_PATHS if "design" in spec["install_key"] else DEFAULT_ADMIN_PATHS

    resolved = resolve_install_path(None, defaults)
    if resolved:
        print(f"[자동 감지] 설치 경로: {resolved}")
        use = input("이 경로를 사용하시겠습니까? (Y/n): ").strip().lower()
        if use in ("", "y", "yes"):
            return resolved

    while True:
        path = input("E3D 설치 경로를 입력하세요: ").strip()
        if os.path.exists(path):
            return path
        print(f"[ERROR] 경로를 찾을 수 없습니다: {path}")


def prompt_module() -> str:
    """실행할 모듈을 사용자에게 질문한다."""
    print("\n실행할 모듈을 선택하세요:")
    for i, name in enumerate(MODULE_SPECS.keys(), 1):
        print(f"  {i}. {name}")
    print(f"  {len(MODULE_SPECS) + 1}. 매크로 경로 직접 입력")

    while True:
        choice = input("선택 (번호 또는 이름): ").strip().lower()
        if choice in MODULE_SPECS:
            return choice
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(MODULE_SPECS):
                return list(MODULE_SPECS.keys())[idx]
            if idx == len(MODULE_SPECS):
                return "design"  # 매크로 경로는 command로 전달
        except ValueError:
            pass
        print("[ERROR] 올바른 모듈을 선택하세요.")


def prompt_credential(module: str) -> tuple[str, str, str, str]:
    """프로젝트 코드와 로그인 정보를 질문한다."""
    project_code = input("\n프로젝트 코드: ").strip().upper()
    spec = MODULE_SPECS[module]

    if spec["cred_type"] == "system":
        print("(Admin 모듈: system 계정 정보를 입력하세요)")

    username = input("USERNAME: ").strip()
    password = input("PASSWORD: ").strip()
    mdb = input("MDB (기본: MASTER): ").strip() or "MASTER"

    return project_code, username, password, mdb


def prompt_start_mode() -> str:
    """시작 모드를 질문한다 (기본: CONSOLE)."""
    mode = input("\n시작 모드 (TTY/CONSOLE/NOCONSOLE, 기본: CONSOLE): ").strip().upper()
    if mode in ("TTY", "CONSOLE", "NOCONSOLE"):
        return mode
    return "CONSOLE"


def interactive_launch() -> None:
    """대화형 모드로 모든 필수 정보를 수집하고 실행한다."""
    print("=" * 50)
    print("  E3D Module Launcher (대화형)")
    print("=" * 50)

    module = prompt_module()
    install_dir = prompt_install_path(module)
    project_code, username, password, mdb = prompt_credential(module)
    start_mode = prompt_start_mode()
    command_input = input("\nCOMMAND 오버라이드 (Enter=기본값): ").strip() or None
    batch_file = input("환경변수 배치 파일 경로 (Enter=없음): ").strip() or None

    spec = MODULE_SPECS[module]
    init_path = os.path.join(install_dir, spec["init_file"])
    exe_path = os.path.join(install_dir, "mon.exe")

    # temp init 생성 (배치 파일이 있는 경우)
    actual_init = init_path
    if batch_file and os.path.isfile(batch_file):
        actual_init = create_temp_init(init_path, batch_file)
        print(f"[Temp Init] {actual_init}")

    cmd = command_input or spec["command"]
    args = (
        f'PROD {spec["product"]} init "{actual_init}" '
        f'{start_mode} {project_code} {username}/{password} /{mdb} {cmd}'
    )

    print(f"\n[E3D Launcher] Exe: {exe_path}")
    print(f"[E3D Launcher] Args: {args}")

    confirm = input("\n실행하시겠습니까? (Y/n): ").strip().lower()
    if confirm not in ("", "y", "yes"):
        print("[취소됨]")
        cleanup_temp_init(actual_init)
        return

    process = subprocess.Popen([exe_path] + args.split())
    print(f"[E3D Launcher] Started PID: {process.pid}")

    # 프로세스 종료 대기 후 cleanup
    process.wait()
    if actual_init != init_path:
        cleanup_temp_init(actual_init)
        print(f"[Cleanup] Temp init 삭제: {actual_init}")


# ── Launcher ───────────────────────────────────────────────

def build_arguments(
    spec: dict,
    init_path: str,
    start_mode: str,
    project_code: str,
    username: str,
    password: str,
    mdb: str,
    command: Optional[str] = None,
) -> str:
    """모듈 스펙에 따라 mon.exe 인자 문자열을 조립한다."""
    cmd = command or spec["command"]
    return (
        f'PROD {spec["product"]} init "{init_path}" '
        f'{start_mode} {project_code} {username}/{password} /{mdb} {cmd}'
    )


def launch_module(
    module: str,
    project_code: str,
    settings: LaunchSettings,
    credential: ProjectCredential,
    start_mode: str = "CONSOLE",
    command: Optional[str] = None,
) -> subprocess.Popen:
    """E3D 모듈을 프로세스로 실행한다."""
    module = module.lower()
    if module not in MODULE_SPECS:
        raise ValueError(f"지원하지 않는 모듈: {module}. 가능: {list(MODULE_SPECS.keys())}")

    spec = MODULE_SPECS[module]

    # 경로 해석: 사용자 지정 → 기본 경로 목록
    defaults = DEFAULT_DESIGN_PATHS if "design" in spec["install_key"] else DEFAULT_ADMIN_PATHS
    install_dir = resolve_install_path(
        getattr(settings, spec["install_key"]), defaults
    )
    if not install_dir:
        raise FileNotFoundError("E3D 설치 경로를 찾을 수 없습니다.")

    exe_path = os.path.join(install_dir, "mon.exe")
    if not os.path.isfile(exe_path):
        raise FileNotFoundError(f"mon.exe를 찾을 수 없습니다: {exe_path}")

    # init 파일 (batch_file이 있으면 temp init 생성)
    init_path = os.path.join(install_dir, spec["init_file"])
    temp_init_path = None
    if settings.batch_file and os.path.isfile(settings.batch_file):
        temp_init_path = create_temp_init(init_path, settings.batch_file)
        init_path = temp_init_path

    # 인증 정보 선택 (user vs system)
    if spec["cred_type"] == "system":
        username = credential.systemUSERNAME
        password = credential.systemPASSWORD
        mdb = credential.systeMDB
    else:
        username = credential.USERNAME
        password = credential.PASSWORD
        mdb = credential.MDB

    args = build_arguments(
        spec, init_path, start_mode.upper(),
        project_code.upper(), username, password, mdb, command,
    )

    print(f"[E3D Launcher] Module: {module}")
    print(f"[E3D Launcher] Exe: {exe_path}")
    print(f"[E3D Launcher] Args: {args}")
    if temp_init_path:
        print(f"[E3D Launcher] Temp Init: {temp_init_path}")

    working_dir = settings.working_dir if settings.working_dir and os.path.isdir(settings.working_dir) else None

    process = subprocess.Popen(
        [exe_path] + args.split(),
        cwd=working_dir,
    )
    print(f"[E3D Launcher] Started PID: {process.pid}")

    # NOTE: cleanup은 호출자가 프로세스 종료 후 수행해야 함
    # cleanup_temp_init(temp_init_path) if temp_init_path else None

    return process


# ── CLI ────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(description="E3D Module Launcher")
    parser.add_argument("--interactive", action="store_true",
                        help="대화형 모드 (필수 정보를 순차 질문)")
    parser.add_argument("--module", choices=list(MODULE_SPECS.keys()),
                        help="실행할 모듈 (design, drawing, paragon, admin)")
    parser.add_argument("--project", help="프로젝트 코드 (예: TESTPROJ)")
    parser.add_argument("--mode", default="CONSOLE", choices=["TTY", "CONSOLE", "NOCONSOLE"],
                        help="시작 모드 (기본: CONSOLE)")
    parser.add_argument("--config", default="config.json", help="config 파일 경로")
    parser.add_argument("--command", default=None,
                        help="COMMAND 오버라이드 (매크로 경로 등)")

    args = parser.parse_args()

    # 대화형 모드
    if args.interactive:
        interactive_launch()
        return

    # CLI 모드: 필수 인자 확인
    if not args.module or not args.project:
        print("[ERROR] --module과 --project는 필수입니다. 또는 --interactive를 사용하세요.")
        parser.print_help()
        sys.exit(1)

    settings, projects = load_config(args.config)

    project_code = args.project.upper()
    if project_code not in projects:
        print(f"[ERROR] 프로젝트 '{project_code}'를 config에서 찾을 수 없습니다.")
        print(f"        등록된 프로젝트: {list(projects.keys())}")
        sys.exit(1)

    credential = projects[project_code]

    process = launch_module(
        module=args.module,
        project_code=project_code,
        settings=settings,
        credential=credential,
        start_mode=args.mode,
        command=args.command,
    )

    print(f"[E3D Launcher] 프로세스 실행 완료 (PID: {process.pid})")


if __name__ == "__main__":
    main()
