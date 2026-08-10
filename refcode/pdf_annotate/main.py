"""CLI entry point: python -m pdf_annotate input.pdf annotations.json [-o out.pdf]."""

import argparse
import json
import sys
from pathlib import Path

from pypdf.errors import PyPdfError

from .annotator import BoxAnnotation, annotate_pdf
from .config import DEFAULT_FONT
from .demo import run_demo


def load_annotations(path) -> tuple[list[BoxAnnotation], list[str]]:
    """Parse the annotation JSON. File-level failures raise; bad records are collected."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except OSError as e:
        raise ValueError(f"cannot read annotations file {path}: {e}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"invalid JSON in {path}: {e}") from e
    if not isinstance(data, list):
        raise ValueError(f"annotations JSON must be a top-level list: {path}")

    annotations, skips = [], []
    for i, record in enumerate(data):
        try:
            if not isinstance(record, dict):
                raise ValueError("record must be an object")
            annotations.append(
                BoxAnnotation(
                    page=record.get("page"),
                    bbox=record.get("bbox"),
                    label=record.get("label", ""),
                    color=record.get("color", "FFC7CE"),
                    subject=record.get("subject", ""),
                )
            )
        except (ValueError, TypeError) as e:
            skips.append(f"record[{i}]: {e}")
    return annotations, skips


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="pdf_annotate",
        description="Add pypdf-native Square + Popup + Korean FreeText annotations to a PDF.",
    )
    ap.add_argument("input_pdf", nargs="?", help="source PDF path")
    ap.add_argument("annotations_json", nargs="?", help="UTF-8 JSON list of annotations")
    ap.add_argument("-o", "--output", help="output PDF (or output directory with --demo)")
    ap.add_argument("--font", default=DEFAULT_FONT, help="Hangul-capable TTF path")
    ap.add_argument("--demo", action="store_true", help="build and annotate a synthetic 3-page PDF")
    args = ap.parse_args(argv)

    try:
        if args.demo:
            result = run_demo(Path(args.output) if args.output else Path("demo_output"),
                              font_path=args.font)
            skips = []
        else:
            if not args.input_pdf or not args.annotations_json:
                ap.error("input_pdf and annotations_json are required unless --demo is given")
            src = Path(args.input_pdf)
            annotations, skips = load_annotations(args.annotations_json)
            for skip in skips:
                print(f"skip: {skip}", file=sys.stderr)
            out = Path(args.output) if args.output else src.with_name(f"{src.stem}_annotated.pdf")
            result = annotate_pdf(src, annotations, out, font_path=args.font)
    except (ValueError, OSError, PyPdfError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    print(
        f"out={result.out_path} drawn={result.drawn} pages={result.page_count} "
        f"skipped_oob={result.skipped_oob} skipped_invalid={len(skips)}"
    )
    return 0
