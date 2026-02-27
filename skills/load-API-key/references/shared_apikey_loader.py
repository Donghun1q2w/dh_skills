"""
shared_apikey_loader.py
========================
부서 공용서버에 위치한 .env 파일에서 API 키를 로드하는 유틸리티.

사용법:
    from shared_apikey_loader import load_shared_keys, get_key

    load_shared_keys()
    api_key = get_key("OPENAI_API_KEY")

설정:
    settings.ini 파일에서 공용서버 경로를 관리합니다.
    settings.ini는 이 스크립트와 같은 디렉토리에 위치해야 합니다.

의존성:
    pip install python-dotenv
"""

import os
import configparser
from pathlib import Path
from dotenv import load_dotenv


# ---------------------------------------------------------------------------
# 설정 로드
# ---------------------------------------------------------------------------
def _get_settings_path() -> Path:
    """settings.ini 경로를 반환한다. 스크립트와 같은 디렉토리에서 찾는다."""
    return Path(__file__).parent / "settings.ini"


def _read_settings() -> configparser.ConfigParser:
    """settings.ini를 읽어 ConfigParser 객체로 반환한다."""
    settings_path = _get_settings_path()
    if not settings_path.exists():
        raise FileNotFoundError(
            f"설정 파일을 찾을 수 없습니다: {settings_path}\n"
            f"settings.ini 파일을 생성한 뒤 공용서버 경로를 입력하세요."
        )
    config = configparser.ConfigParser()
    config.read(str(settings_path), encoding="utf-8")
    return config


# ---------------------------------------------------------------------------
# 키 로드
# ---------------------------------------------------------------------------
def load_shared_keys() -> bool:
    """
    settings.ini에 지정된 공용서버 .env 파일을 읽어 환경변수로 로드한다.

    Returns:
        True  - 공용서버 .env 로드 성공
        False - 폴백(.env 로컬) 사용 또는 실패
    """
    config = _read_settings()

    env_path = config.get("server", "env_path", fallback="")
    encoding = config.get("options", "encoding", fallback="utf-8")
    use_fallback = config.getboolean("options", "use_local_fallback", fallback=True)
    local_env = config.get("options", "local_env_path", fallback=".env")

    # 1) 공용서버 경로 시도
    if env_path and Path(env_path).is_file():
        load_dotenv(dotenv_path=env_path, encoding=encoding, override=True)
        print(f"[INFO] 공용서버 .env 로드 완료: {env_path}")
        return True

    print(f"[WARN] 공용서버 .env 접근 불가: {env_path}")

    # 2) 로컬 폴백
    if use_fallback:
        local_path = Path(local_env) if Path(local_env).is_absolute() else Path.cwd() / local_env
        if local_path.is_file():
            load_dotenv(dotenv_path=str(local_path), encoding=encoding, override=True)
            print(f"[INFO] 로컬 폴백 .env 로드 완료: {local_path}")
            return False

    print("[ERROR] 사용 가능한 .env 파일이 없습니다.")
    return False


def get_key(key_name: str, default: str | None = None) -> str | None:
    """
    환경변수에서 API 키를 가져온다.

    Args:
        key_name: 환경변수 이름 (예: 'OPENAI_API_KEY')
        default:  키가 없을 때 반환할 기본값

    Returns:
        API 키 문자열 또는 default
    """
    value = os.getenv(key_name, default)
    if value is None:
        print(f"[WARN] 키를 찾을 수 없습니다: {key_name}")
    return value


def list_keys() -> dict[str, str]:
    """
    현재 로드된 API 키 목록을 반환한다.
    키 값은 앞 8자만 표시하고 나머지는 마스킹한다.
    """
    config = _read_settings()
    env_path = config.get("server", "env_path", fallback="")

    keys = {}
    # .env 파일을 직접 파싱하여 키 이름 목록 확보
    for path in [env_path, config.get("options", "local_env_path", fallback=".env")]:
        p = Path(path)
        if p.is_file():
            with open(p, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        name = line.split("=", 1)[0].strip()
                        val = os.getenv(name, "")
                        if val:
                            masked = val[:8] + "*" * max(0, len(val) - 8)
                            keys[name] = masked
            break
    return keys


# ---------------------------------------------------------------------------
# 직접 실행 시 테스트
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("공용서버 API 키 로더 테스트")
    print("=" * 50)

    load_shared_keys()

    print("\n--- 로드된 키 목록 (마스킹) ---")
    for name, masked in list_keys().items():
        print(f"  {name}: {masked}")

    print("\n--- 개별 키 조회 예시 ---")
    openai_key = get_key("OPENAI_API_KEY")
    anthropic_key = get_key("ANTHROPIC_API_KEY")
    print(f"  OPENAI_API_KEY    = {openai_key}")
    print(f"  ANTHROPIC_API_KEY = {anthropic_key}")
