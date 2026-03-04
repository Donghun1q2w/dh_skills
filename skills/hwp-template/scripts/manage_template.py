"""한글 템플릿 관리 스크립트.

Usage:
    python manage_template.py save <name> <file> [--templates-dir DIR]
    python manage_template.py list [--templates-dir DIR]
    python manage_template.py info <name> [--templates-dir DIR]
    python manage_template.py delete <name> [--templates-dir DIR]
"""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


def get_templates_dir(base: str | None) -> Path:
    d = Path(base) if base else Path.cwd() / "templates"
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_index(templates_dir: Path) -> dict:
    index_path = templates_dir / "index.json"
    if index_path.exists():
        return json.loads(index_path.read_text(encoding="utf-8"))
    return {"templates": []}


def save_index(templates_dir: Path, data: dict) -> None:
    index_path = templates_dir / "index.json"
    index_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_save(args):
    templates_dir = get_templates_dir(args.templates_dir)
    src = Path(args.file)
    if not src.exists():
        print(f"Error: 파일을 찾을 수 없습니다: {src}", file=sys.stderr)
        sys.exit(1)

    dest = templates_dir / f"{args.name}{src.suffix}"
    index = load_index(templates_dir)

    # 기존 항목 확인
    existing = [t for t in index["templates"] if t["name"] == args.name]
    if existing:
        print(f"기존 템플릿 '{args.name}'을 덮어씁니다.")
        index["templates"] = [t for t in index["templates"] if t["name"] != args.name]

    shutil.copy2(src, dest)

    entry = {
        "name": args.name,
        "file": dest.name,
        "fields": [],  # 필드 목록은 hwp-analyze로 별도 추출
        "created": datetime.now().strftime("%Y-%m-%d"),
    }
    index["templates"].append(entry)
    save_index(templates_dir, index)
    print(f"템플릿 '{args.name}' 저장 완료: {dest}")


def cmd_list(args):
    templates_dir = get_templates_dir(args.templates_dir)
    index = load_index(templates_dir)

    if not index["templates"]:
        print("등록된 템플릿이 없습니다.")
        return

    print(f"{'이름':<15} {'파일':<25} {'필드 수':<10} {'등록일':<12}")
    print("-" * 62)
    for t in index["templates"]:
        fields_count = len(t.get("fields", []))
        print(f"{t['name']:<15} {t['file']:<25} {fields_count:<10} {t.get('created', 'N/A'):<12}")


def cmd_info(args):
    templates_dir = get_templates_dir(args.templates_dir)
    index = load_index(templates_dir)

    entry = next((t for t in index["templates"] if t["name"] == args.name), None)
    if not entry:
        print(f"Error: 템플릿 '{args.name}'을 찾을 수 없습니다.", file=sys.stderr)
        sys.exit(1)

    print(f"이름: {entry['name']}")
    print(f"파일: {templates_dir / entry['file']}")
    print(f"등록일: {entry.get('created', 'N/A')}")
    fields = entry.get("fields", [])
    if fields:
        print(f"필드 ({len(fields)}개):")
        for f in fields:
            print(f"  - {f}")
    else:
        print("필드: (미분석 - /hwp-analyze로 분석 필요)")


def cmd_delete(args):
    templates_dir = get_templates_dir(args.templates_dir)
    index = load_index(templates_dir)

    entry = next((t for t in index["templates"] if t["name"] == args.name), None)
    if not entry:
        print(f"Error: 템플릿 '{args.name}'을 찾을 수 없습니다.", file=sys.stderr)
        sys.exit(1)

    file_path = templates_dir / entry["file"]
    if file_path.exists():
        file_path.unlink()

    index["templates"] = [t for t in index["templates"] if t["name"] != args.name]
    save_index(templates_dir, index)
    print(f"템플릿 '{args.name}' 삭제 완료.")


def main():
    parser = argparse.ArgumentParser(description="한글 템플릿 관리")
    parser.add_argument("--templates-dir", help="템플릿 저장 디렉토리 (기본: ./templates)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_save = sub.add_parser("save", help="템플릿 저장")
    p_save.add_argument("name", help="템플릿 이름")
    p_save.add_argument("file", help="원본 파일 경로")

    sub.add_parser("list", help="템플릿 목록")

    p_info = sub.add_parser("info", help="템플릿 상세")
    p_info.add_argument("name", help="템플릿 이름")

    p_del = sub.add_parser("delete", help="템플릿 삭제")
    p_del.add_argument("name", help="템플릿 이름")

    args = parser.parse_args()
    {"save": cmd_save, "list": cmd_list, "info": cmd_info, "delete": cmd_delete}[args.command](args)


if __name__ == "__main__":
    main()
